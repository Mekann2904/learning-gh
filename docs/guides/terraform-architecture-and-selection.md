# Terraform 構成と技術選定の理由

- 対象読者: インフラ運用/開発メンバー、リポジトリ管理者
- 前提条件: 本リポジトリは GitHub（プライベート）＋ Terraform Cloud（TFC）連携を採用
- TL;DR: PR駆動で一貫実行・最小権限・秘密集中管理を実現するため、TFCを採用。小規模は無料枠で開始し、将来は代替（S3+CI等）へ移行可能な設計とする。

## 目的

- なぜこのTerraform構成（GitHub Private × TFC）を選ぶかを技術的観点で説明する。
- セキュリティ/運用/コスト/拡張性の要件に対して、代替案と比較しながら位置付ける。

## 要件整理

- セキュリティ: ローカルに秘密を置かない、最小権限、状態（state）の安全保管、監査可能性。
- 運用性: PR起点でplan→レビュー→apply、ローカル差異を排除、失敗時の可観測性を確保。
- 共同開発: オンボーディング容易、バージョン固定、再現性の高い実行環境。
- コスト: 小規模は無料で開始、段階的に拡張可能。

## 採用構成（概要）

```mermaid
graph LR
  Dev[Developer];
  GH["GitHub (Private Repo)"];
  TFC["Terraform Cloud (Workspace)"];
  Cloud["Cloud Provider"];

  Dev -->|PR作成/更新| GH;
  GH -->|VCSトリガー| TFC;
  TFC -->|Plan/Logs| GH;
  TFC -->|"Apply(承認後)"| Cloud;
  Dev -->|terraform login| TFC;
```

特性

- VCS連携でPRイベントを起点にPlanを自動実行する。
- Applyは権限者のみ承認。実行ログと差分はTFCに集約する。
- 変数/秘密（API鍵等）はTFCのWorkspace/Variable Setに一元管理する。

## 代替案と比較

- ローカル実行 + remote backend（S3/DynamoDB等）
  - 長所: 完全自前、柔軟。インターネット不要な閉域も構築可能。
  - 短所: 開発者ローカルに認証情報が残りやすい。state鍵管理やロック運用が煩雑。
- GitHub Actions + remote backend
  - 長所: CIと統合、OIDC等でクラウド権限を安全に付与可能。
  - 短所: state/秘密の保管・権限分離の設計が必要。ワークフロー設計/メンテ負荷が上がる。
- Atlantis 等の自前PR駆動ツール
  - 長所: PRベース運用を自前で実現。拡張性高い。
  - 短所: ホスティング/スケーリング/セキュリティ運用の負荷が増大。
- Terraform Cloud（採用）
  - 長所: VCS連携/Workspace/RBAC/変数管理/実行ログ/状態管理を一体で提供。PR駆動を少ない設定で実現。
  - 短所: SaaS依存。細粒度要件や閉域要件では適合しない場合がある。

## TFCを選ぶ理由（技術的根拠）

- セキュリティ
  - ローカルに秘密を置かない。Workspace Variables（Sensitive）に集約し、アクセスをRBACで制御する。
  - stateをTFCで暗号化・ロック管理し、直接露出を防ぐ。
  - 実行環境をSaaS側に固定し、開発端末の権限を最小化する。
- 運用・可観測性
  - PRベースでplan結果を可視化、差分をレビューに載せる。
  - 承認付きapply、実行履歴・ログ・差分が一元化され監査しやすい。
  - バージョン固定（tfenv/asdf）＋リモート実行で再現性を高める。
- コスト/開始容易性
  - 小規模は無料枠で開始し、過不足が出た時に有償機能へ段階移行できる。
  - 自前でstate/ロック/秘密管理の基盤を構築・運用するコストを回避する。
- 将来の移行性
  - HCLとモジュール設計はSaaS非依存。必要に応じてS3+CI等へ移行できる。

## セキュリティ設計の要点

- 資格情報: 長期鍵の配布を避け、変数はTFCで管理。必要最小限のクラウド権限のみ付与する。
- 権限分離: Plan実行とApply承認を分離。管理者は変数管理、開発者はPR駆動を主とする。
- 状態管理: TFCのstate暗号化/ロックに依存。ローカル保存を禁ずる。
- 監査性: すべての実行・差分・コメント・承認を記録し、事後追跡を容易にする。

## クラウド別のOIDCベース認証設計

目的: 長期秘密鍵を排し、短期トークンで最小権限を付与する。

```mermaid
sequenceDiagram
  participant GH as "GitHub Actions"
  participant IDP as "GitHub OIDC Provider"
  participant Cloud as "Cloud STS/Token Service"
  participant TFC as "Terraform Cloud (実行者)"

  GH->>IDP: OIDCトークン要求
  IDP-->>GH: OIDC IDトークン(JWT)
  GH->>Cloud: IDトークンを提示して一時認証要求
  Cloud-->>GH: 短期クレデンシャル発行
  GH->>TFC: Terraform実行時に短期クレデンシャルを使用
```

共通方針

- 信頼バインド: リポジトリ/環境/ブランチ等の`aud`/`sub`制約でスコープを限定。
- IAM最小権限: Plan/Applyに必要な権限を分離し、承認フローと組み合わせる。
- 秘密非保持: 長期キーを排除。必要に応じてローカルはTFC実行へ委譲。

AWS（GitHub OIDC → STS:AssumeRoleWithWebIdentity）

- 設計: `identity provider`を作成し、`condition`で`sub`（リポジトリ/環境）を厳格化。`AssumeRolePolicy`で信頼関係を限定。
- 付与: Terraform用IAMロールに必要最小のポリシーを付与（例: S3, DynamoDB, 各サービス）
- 参考ポリシー断片（概念）:
  - Trust policy: `aud: sts.amazonaws.com`かつ`sub: repo:<owner>/<repo>:ref:refs/heads/main` 等
  - Session duration: 15〜60分（最小）

GCP（Workload Identity Federation）

- 設計: `Workload Identity Pool`と`Provider`を作成し、`attribute.condition`で`repository`, `ref`を制限。
- 付与: `Service Account`と`Workload Identity User`ロールを紐付け、必要権限のみ付与。
- 取得: `gcloud auth workforce/iam`経由で短期クレデンシャルを払い出し。

Azure（Federated Credentials for Service Principal）

- 設計: Entra IDアプリ（SP）に`federated credential`を追加。`issuer`, `subject`, `audience`でリポジトリ/ブランチを固定。
- 付与: SPに必要な`Role Assignment`を最小で付与（例: Contributorではなくサービス単位の細分化）。
- 実行: `az login --federated-token`相当で短期トークンを利用。

比較と利点

- 長期キー配布/ローテーション不要、漏えい面積を縮小。
- トークンは短命で、権限は実行コンテキスト（PR/ブランチ）へ限定可能。
- 監査性が高く、誤用時の影響範囲を限定できる。

注意点

- 条件式（sub, repository, environment）の厳格化を徹底。ワイルドカード広すぎに注意。
- ローカル実行を許容する場合も、原則はTFC実行へ委譲し秘密非保持を維持。
- 役割分離（Plan/Apply）とレビュー/承認プロセスを必ず組み合わせる。

## 運用フロー（PR駆動）

1. featureブランチで変更を作成
2. PR作成で自動Plan実行（TFC）
3. レビューで差分・影響を確認
4. 権限者がApplyを承認
5. マージ後に状態が更新される

## コストと無料枠

- 無料プランで小規模運用を開始できる前提で設計する。
- チーム規模/実行頻度が増えた場合は有償機能（より高度なRBAC/ポリシー/監査）を検討する。
- 代替: 省コストが最優先なら S3 + GitHub Actions へ移行も可能（state/秘密管理の設計は別途必要）。

## リスクと回避策

- SaaS依存: 重要運用の単一依存を避け、エクスポート/バックアップ手段を確保する。
- 閉域要件: 企業要件によっては自前CI＋remote backendへ切替える計画を準備する。
- ベンダー機能差: ポリシー/承認/変数管理の運用ルールを文書化し、代替構成でも再現可能にする。

## 結論

- セキュリティ/運用容易性/監査性のバランスから、まずはTFC採用でPR駆動と秘密集中管理を実現する。
- ベースはポータブルなHCLとモジュール分割に置き、成長や制約に応じてS3+CI等へ移行できる余地を維持する。

## 参考

- Terraform Cloud 公式ドキュメント（VCS連携, Workspaces, Variables）
- Terraform CLI と Remote Backend の設計比較
- PR駆動インフラ運用（Atlantis, GitHub Actions, TFC）の比較記事
