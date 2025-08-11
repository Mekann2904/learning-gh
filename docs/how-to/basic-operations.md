# 基本操作チートシート（ローカル）

- 対象読者: Git と GH CLI を使う開発者
- 前提条件: oh-my-zsh と Git、GitHub CLI（`gh`）が利用可能
- TL;DR: よく使う基本操作を短いコマンド例で素早く参照。

## 目的

日常の基本操作（add/commit/push や `gh` の参照など）の最短コマンド例をまとめる。

## コマンド例

```zsh
# 変更の追加
gaa

# コミット（変更すべて）
gca

# メッセージ付きコミット
gcmsg "sample"

# push（mainへ）
gp origin main

# リポジトリURL確認
gh repo view
```

