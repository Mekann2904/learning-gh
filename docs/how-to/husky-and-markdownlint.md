# Husky と markdownlint-cli2 導入解説

## 目的

- コミット前に Markdown 品質検証を自動化する
- docs 配下の Mermaid 構文検証を将来拡張で追加する

## 前提

- Node.js と npm が利用可能
- Git フックは Husky 管理を前提

## Husky 導入

- 目的: Git フックを npm 管理して安定運用する
- 手順:
  1. devDependencies に追加: `npm i -D husky@^8`
  2. prepare スクリプト追加: `"prepare": "husky install"`
  3. 初期化実行: `npm run prepare`
  4. フック作成: `npx husky add .husky/pre-commit "npx lint-staged"`
- 現状のフック:

  ```sh
  # .husky/pre-commit
  #!/bin/sh
  . "$(dirname "$0")/_/husky.sh"

  npx lint-staged
  ```

## lint-staged 連携

- 目的: 変更ファイルのみを対象に高速検証する
- 手順:
  1. 追加: `npm i -D lint-staged`
  2. 設定を package.json に追加

     ```jsonc
     {
       "lint-staged": {
         "*.md": ["markdownlint-cli2 --fix", "git add"]
       }
     }
     ```

- 動作: ステージ済みの Markdown に
  markdownlint-cli2 を適用し、自動修正後に再ステージする

## markdownlint-cli2 導入

- 目的: Markdown のスタイル・構文を統一
- 追加: `npm i -D markdownlint-cli2`
- 設定ファイル: `.markdownlint-cli2.jsonc`

  ```jsonc
  {
    "ignores": ["node_modules", "dist", "build"]
  }
  ```

- 実行例:
  - 全体: `npx markdownlint-cli2 "**/*.md"`
  - docs 配下のみ: `npx markdownlint-cli2 "docs/**/*.md"`
- ルール拡張例:
  - MD013(行長)を緩和 → `.markdownlint.jsonc` に
    `{ "MD013": false }` を追加
  - ルールファイル併用時:
    `markdownlint-cli2-config` を devDependencies に追加して継承

## Mermaid 検証(将来拡張)

- 目的: docs の ```mermaid コードブロック構文エラーを検出
- 要件:
  - 成功: `Mermaid syntax OK: docs` を出力、終了コード 0
  - 失敗: ファイル別にエラー列挙、件数出力、
    終了コード 非0
- 実装案A: Node スクリプトでパース
  - 追加: `npm i -D @mermaid-js/mermaid`
  - スクリプト例: `scripts/validate-mermaid.mjs`

    ```js
    import { readFileSync } from 'node:fs';
    import { globby } from 'globby';
    import mermaid from 'mermaid';

    const files = await globby(['docs/**/*.md']);
    let errors = [];
    for (const f of files) {
      const text = readFileSync(f, 'utf8');
      const blocks = [...text.matchAll(/```mermaid\n([\s\S]*?)\n```/g)];
      blocks.forEach((m, i) => {
        try { mermaid.parse(m[1]); } catch (e) {
          errors.push(`${f} #${i + 1}: ${e.message}`);
        }
      });
    }
    if (errors.length === 0) {
      console.log('Mermaid syntax OK: docs');
      process.exit(0);
    }
    console.error(errors.join('\n'));
    console.error(`Errors: ${errors.length}`);
    process.exit(1);
    ```

  - 連携: `.husky/pre-commit` で
    `node scripts/validate-mermaid.mjs` を
    lint-staged の前に実行
- 実装案B: CLI 利用
  - 追加: `npm i -D @mermaid-js/mermaid-cli`
  - 各ブロックを一時ファイルに書き出し `mmdc` で検証
- 注意: 依存導入前はフックに追加しない。
  導入後に動作確認して有効化する

## 運用

- コミット前検証: Husky が `lint-staged` を起動し
  Markdown を自動整形
- 手動検証: `npx markdownlint-cli2 "docs/**/*.md"`
- CI 連携案: `markdownlint-cli2` と
  Mermaid 検証をワークフローに統合

## トラブルシュート

- コミット時に `markdownlint-cli2` が見つからない
  - 対応: `npm i -D markdownlint-cli2` を実行
- 自動修正が過剰
  - 対応: 固定したいルールを `.markdownlint.jsonc` で上書き
- Mermaid 検証が遅い
  - 対応: 変更ファイルのみ対象にする、又は並列化

## まとめ

- Husky でフックを npm 管理
- lint-staged で差分に限定
- markdownlint-cli2 で Markdown 品質を担保
- Mermaid 検証は依存導入後に段階的に有効化
