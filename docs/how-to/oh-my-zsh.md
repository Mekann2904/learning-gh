# oh-my-zsh の Git エイリアス チートシート

- 対象読者: oh-my-zsh を使って Git 操作を効率化したい人
- 前提条件: oh-my-zsh が導入済み、git が利用可能
- TL;DR: 代表的なエイリアス（`gst`, `gaa`, `gcmsg`, `glog` など）を把握して日常操作を短縮。

## 目的

よく使う Git 操作用の oh-my-zsh エイリアスを一覧し、日常の時短に役立てる。

---

| 目的        | エイリアス   | 実コマンド                                  | メモ      |
| --------- | ------- | -------------------------------------- | ------- |
| 変更確認      | `gst`   | `git status`                           | 全体の状況   |
| 追加（全部）    | `gaa`   | `git add --all`                        | 一括ステージ  |
| 追加（対話）    | `gapa`  | `git add --patch`                      | 部分追加    |
| コミット      | `gcmsg` | `git commit -m`                        | メッセージ付き |
| 差分（未ステージ） | `gd`    | `git diff`                             | 作業中の差分  |
| 差分（ステージ済） | `gds`   | `git diff --staged`                    | コミット前確認 |
| ブランチ切替    | `gsw`   | `git switch`                           | 既存に移動   |
| 新規ブランチ    | `gswc`  | `git switch -c`                        | 作る＋移動   |
| mainへ     | `gswm`  | `git switch $(git_main_branch)`        | main優先  |
| 取得        | `gl`    | `git pull`                             | まず同期    |
| 送信        | `gp`    | `git push`                             | デフォルトへ  |
| ログ（見やすい）  | `glog`  | `git log --oneline --decorate --graph` | 履歴俯瞰    |

## 用途別チートシート

### 状況確認・ログ

- `gst` → `git status`
- `gsb` → `git status -sb`（簡潔表示）
- `glog` → oneline + decorate + graph
- `glgg` → `git log --graph`
- `glol` / `glola` → 装飾ログ（全ブランチは `glola`）

### 追加・コミット

- `ga` / `gaa` / `gapa` / `gau`
- `gc` → `git commit -v`
- `gc!` → `git commit -v --amend`（直前修正）
- `gcam` → `git commit -a -m`
- `gcmsg` → `git commit -m`
- 署名: `gcs`（`commit -S`）

### 差分

- `gd` → 作業差分
- `gds` / `gdca` → ステージ差分
- `gdw` → `--word-diff`
- `gdup` → `diff @{upstream}`（リモートとの差分）

### ブランチ

- `gsw` / `gswc` / `gswm`
- `gb` → 一覧、`gbD` → 強制削除（注意）

### リモート

- `gl` / `gp` 基本操作
- `gpoat` → すべてのタグを push（注意）

## 参考

- oh-my-zsh Git plugin: https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git

