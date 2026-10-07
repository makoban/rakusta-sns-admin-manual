# ココトモSNS 新規顧客BOTの標準マニュアル

2026年10月7日のユーザー指示により、今後作成する全新規顧客BOTを今回の手順に統一する。

村上さん用：https://makoban.github.io/rakusta-sns-admin-manual/murakami.html

一覧：https://makoban.github.io/rakusta-sns-admin-manual/

## 必ず守る順序

BANTEXが店舗調査・専用BOT作成 → 全設定保存・再確認 → お客様専用URLを案内 → お客様本人がInstagram承認 → BANTEXが対象Instagram・投稿権限・接続を確認 → 専用LINE配布。

挨拶は「写真・動画を、このLINEに送るだけ」の使い方を登録し、初回のみ送信ON・挨拶ON・Webhook ON、チャットOFF・応答メッセージOFFを再確認する。Provider BANTEX、1日1枠17:00、月間総投稿31回、AI動画編集月31回、加工・即時投稿・完了通知・顔ぼかしONを初期値にする。店舗情報とタグは実際の店舗の情報で作る。明確な別指定のある項目だけ調整する。

## 正本と生成

`manual-data.json` に共通設定と挨拶本文、`tools/build_manuals.py` に全操作手順を置く。12ページと3種類のPDFを同じ版から生成する。個別HTMLだけ手修正して内容を分岐させない。

```bash
python3 tools/build_manuals.py
python3 tools/build_pdfs.py
python3 tools/sync_local_manuals.py --workspace /path/to/ココトモ関係まとめ
```

PDF生成にはPythonのreportlab・pypdf・lxmlと日本語フォントを使う。BANTEX環境ではbundled Pythonを使用し、長いCLI処理は共通ジョブルーターに従う。

PDF：`downloads/admin.pdf`（社内）、`downloads/customer.pdf`（お客様）、`downloads/complete.pdf`（一式）。挨拶のLINE登録用原文は `assets/manual/greeting.txt`。PDFでは絵文字を省略しており、LINEへはWebのコピーボタンまたはTXTの原文を使う。

`sync_local_manuals.py` は手元の旧配布用HTML・Markdownを最新URLへの案内にし、既存の配布用PDFと最新版名のPDFを更新する。変更前の旧資料はローカルのarchiveへ一度だけ退避する。旧版の画面証拠・無関係な資料は変更しない。

## 公開

既存GitHub Pagesのmain・rootから公開する。DNSやドメインは変更しない。push後にPagesの成功SHA、実HTTP、スマートフォン・PCの表示、PDFの取得を確認する。既存の全マニュアルURLも最新版へ更新する。

## 掲載しないもの

実顧客の署名付きお客様URL、LINE配布URL、Channel secret、token、パスワード、コード、Cookieは掲載しない。Instagram承認はお客様本人の端末で行う。全店舗共通tokenの上書きや代理認証で代用しない。

noindex・robotsは検索除外であり、閲覧の認証ではない。このサイトには操作手順だけを公開する。顧客への外部送信は送信先と送信指示がある場合に行う。
