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

# 用途別チートシート

## 状況確認・ログ

* `gst` → `git status`
* `gsb` → `git status -sb`（簡潔表示）
* `glog` → oneline + decorate + graph
* `glgg` → `git log --graph`
* `glol` / `glola` → 装飾ログ（全ブランチは `glola`）

## 追加・コミット

* `ga` / `gaa` / `gapa` / `gau`
* `gc` → `git commit -v`
* `gc!` → `git commit -v --amend`（直前修正）
* `gcam` → `git commit -a -m`
* `gcmsg` → `git commit -m`
* 署名: `gcs`（`commit -S`）

## 差分

* `gd` → 作業差分
* `gds` / `gdca` → ステージ差分
* `gdw` → `--word-diff`
* `gdup` → `diff @{upstream}`（リモートとの差分）

## ブランチ

* 一覧: `gb` / `gba` / `gbr`
* 生成切替: `gswc`（推奨） or `gcb`（checkout派）
* 切替: `gsw` / `gswm` / `gswd`
* 削除: `gbd` / 強制 `gbD`
* マージ済み掃除: `gbda`

## 取得・送信（同期）

* 取得: `gf`（単純）/ `gfa`（全＋prune）
* 取得/送信（現ブランチ）:

  * `ggl` → `git pull origin $(current_branch)`
  * `ggp` → `git push origin $(current_branch)`
  * 連続: `ggpnp`（pull→push）
* 追跡設定: `gpsup` / `ggsup`

## マージ・リベース

* マージ: `gm`、中止 `gma`
* リベース開始: `grb`
* 続行/中止/スキップ: `grbc` / `grba` / `grbs`
* mainに合わせる: `grbm`（`rebase $(git_main_branch)`）

## リセット・復元

* `grh` → `git reset`
* `grhh` → `git reset --hard`（注意）
* `grst` → `git restore --staged`
* `grs` → `git restore`

## スタッシュ

* 保存: `gsta`（または `stash save`）
* 一覧: `gstl`
* 適用/ポップ: `gstaa` / `gstp`
* 破棄: `gstd`
* すべて: `gstall`（未追跡含む）

## タグ

* `gtv` → バージョン順一覧
* 関数 `gtl {pattern}` → 新しい順で詳細表示
* 署名タグ: `gts`

## サブモジュール

* 初期化/更新: `gsi` / `gsu`
* チェックアウト時に再帰: `gcor`

# 危険度つき（掃除・強制系）

| エイリアス           | コマンド                                  | 作用                 | 危険度   |
| --------------- | ------------------------------------- | ------------------ | ----- |
| `gclean`        | `git clean -id`                       | 未追跡を対話削除           | 低（安全） |
| `git clean -df` | —                                     | 未追跡ファイル・ディレクトリを即削除 | 高     |
| `gpristine`     | `git reset --hard && git clean -dffx` | 追跡の差分も無視ファイルも全消し   | 最高    |
| `gpf!`          | `git push --force`                    | 強制上書き push         | 高     |
| `ggf` / `ggfl`  | `--force` / `--force-with-lease`      | 現ブランチを強制 push      | 高     |

※ 迷ったらまず `gclean`（対話）を使う。履歴を書き換える場合は基本 `--force-with-lease` 優先。

# 便利ワンライナー

* **現在ブランチを upstream 設定して push**: `gpsup`
* **全ブランチ＆タグを push**: `gpoat`
* **削除済みファイルを一括ステージ**: `gwip`（WIPコミット作成も兼ねる）
* **main を取り込む**: `gmom`（`merge origin/main`）／`grbom`（`rebase origin/main`）

