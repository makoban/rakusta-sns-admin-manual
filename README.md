# 楽スタ 新店舗SNS連携マニュアル

社内管理者向けの静的HTMLマニュアルです。

## 開くファイル

- まず迷ったら: `simple-customer-onboarding.html`
- 全体版: `index.html`
- 村上さん練習用: `murakami.html`

## 重要

- 実パスワード、Meta token、LINE Channel secret、App Secretはこのリポジトリに入れない。
- GitHub Pagesに置く場合、URLを知っている人が閲覧できる前提で扱う。
- 認証情報は1Password、Bitwarden、社内の安全な共有手段で別途渡す。
- 新規顧客追加の通常作業ではGraph API Explorerのtoken生成画面を開かない。
- 新規顧客追加の通常作業ではRenderの `INSTAGRAM_ACCESS_TOKEN` を変更しない。
