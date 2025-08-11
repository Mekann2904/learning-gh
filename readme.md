# 学習用ドキュメント集（learning-gh）

開発まわりの手順・知見を素早く参照できるように整理するドキュメント集である。目的別に「ガイド」「How-to」「運用」に分類する。

## 使い方（入口）

- ガイド
  - GitHub（プライベート）と Terraform Cloud の VCS 連携: [docs/guides/github-private-tfc-vcs-integration.md](docs/guides/github-private-tfc-vcs-integration.md)
  - Terraform 構成と技術選定の理由: [docs/guides/terraform-architecture-and-selection.md](docs/guides/terraform-architecture-and-selection.md)

- How-to（短手順）
  - oh-my-zsh の Git エイリアス: [docs/how-to/oh-my-zsh.md](docs/how-to/oh-my-zsh.md)
  - 基本操作チートシート: [docs/how-to/basic-operations.md](docs/how-to/basic-operations.md)

- 運用（Ops）
  - GitHub Issues の CLI 操作例: [docs/ops/issues.md](docs/ops/issues.md)

## リポジトリ構成

```
.
├─ README.md              # 入口（目的・使い方・構成・執筆ルール要約）
├─ CONTRIBUTING.md        # 詳細な執筆ルール
├─ .markdownlint.json     # Lintルール
└─ docs/
   ├─ guides/            # 背景・設計込みの長文ガイド
   ├─ how-to/            # 短い実用手順
   ├─ ops/               # 運用ルール・ログ
   └─ _template.md       # 新規ドキュメント雛形
```

## 執筆ルール（要約）

- 構成: 目的 / 前提 / 手順 / 検証 / トラブルシュート / 参考
- 見出し: 文書内の H1 は 1 つ。節は H2（##）から開始
- 記法: コードブロックに言語指定（例: `bash`, `zsh`, `json`, `hcl`）
- 命名: ファイル名は ASCII の kebab-case（本文は日本語で可）
- 配慮: 画像・図に代替テキストを付与、UI差異は注記

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照する。

## 検証（ローカルLint）

以下いずれかでMarkdownのLintを実行する（Node.jsが必要）。

```bash
# 1) markdownlint-cli を使う
npx -y markdownlint-cli "**/*.md"

# 2) markdownlint-cli2 を使う（推奨）
npx -y markdownlint-cli2 "**/*.md"
```

補足: ルールは `.markdownlint.json` を使用する。H1は1つ、コードブロックは言語指定を付ける。

## Mermaid 記法

- GitHub では ` ```mermaid ` を用いた図の描画をサポートする。
- 一部クライアントではプレビュー差異が出る場合があるため、最終確認はGitHub上で行う。

## 新規ドキュメントの追加手順

- 雛形をコピーして配置する。

```bash
cp docs/_template.md docs/how-to/<new-doc>.md
# または docs/guides/ や docs/ops/ へ配置
```

- ファイル名は kebab-case。本文H1は1つ、章立てはテンプレに準拠。
