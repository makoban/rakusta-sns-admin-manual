# 楽スタ マニュアルサイト

GitHub Pagesで公開する静的HTMLマニュアルです。Renderは使いません。

## 開くファイル

- 一覧: `index.html`
- まず迷ったら: `simple-customer-onboarding.html`
- お客様用スマホ設定: `store-settings-mobile.html`
- 管理側初期設定: `setup-admin.html`
- 全体版: `operator-full.html`
- 村上さん練習用: `murakami.html`

## GitHub Pages

- まずはGitHub Pages標準URLで公開する。
- 後で `rakusuta-manual.bantex.jp` に切り替える。
- DNSを切り替える時は、`CNAME.example` を `CNAME` に変更し、GitHub PagesのCustom domainにも同じドメインを設定する。
- DNSのCNAME先は `makoban.github.io`。

## 重要

- 実パスワード、Meta token、LINE Channel secret、App Secretはこのリポジトリに入れない。
- GitHub Pagesに置く場合、URLを知っている人が閲覧できる前提で扱う。
- 認証情報は1Password、Bitwarden、社内の安全な共有手段で別途渡す。
- 新規顧客追加の通常作業ではGraph API Explorerのtoken生成画面を開かない。
- 新規顧客追加の通常作業ではRenderの `INSTAGRAM_ACCESS_TOKEN` を変更しない。
