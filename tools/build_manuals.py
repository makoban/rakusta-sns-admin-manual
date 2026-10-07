"""標準ルールから全公開マニュアルを生成する。顧客の認証情報は扱わない。"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / 'manual-data.json').read_text())
VERSION = RULES['version']
BASE = 'https://makoban.github.io/rakusta-sns-admin-manual/'
GREETING = RULES['line']['greeting_text']

def e(value):
    return html.escape(str(value))

def display(value):
    text=e(value)
    for term in ('ココトモSNS','新規顧客','Instagram','Messaging API','LINE','BANTEX','村上さん'):
        text=text.replace(term,'<span class="keep">'+term+'</span>')
    return text

def paragraph(text):
    return f'<p>{text}</p>'

def steps(*items):
    return '<ol class="actions">' + ''.join(f'<li>{item}</li>' for item in items) + '</ol>'

def table(*rows):
    return '<dl class="field-map">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in rows) + '</dl>'

def note(text):
    return f'<p class="note">{text}</p>'

def copy_box(text, label='本文をコピー'):
    return f'<div class="copy-box"><button type="button" class="copy-button">{label}</button><pre>{e(text)}</pre><span class="copy-status" aria-live="polite"></span></div>'

def section(key, title, body, role='BANTEX'):
    return {'id':key, 'title':title, 'body':body, 'role':role}

FLOW = '<ol class="flow">' + ''.join(f'<li><b>{i}</b><span>{display(text)}</span></li>' for i,text in enumerate(['店舗調査・専用BOT作成','全設定を保存・確認','お客様専用URLを案内','お客様がInstagramを承認','BANTEXで接続確認','確認後にLINEを配布'],1)) + '</ol>'

COMMON_NOTICE = note('この順序を全ての新規顧客BOTで使います。Instagramのログイン・承認はお客様の端末で行います。LINEを案内するのは、承認と接続確認が終わってからです。')

INITIAL = table(('予約投稿枠','1日1枠'),('月間の総投稿上限','31回。即時投稿と予約投稿の合計。'),('予約時刻','17:00。お客様の明確な指定がある場合だけ調整。'),('AI動画編集上限','月31回'),('画像加工・動画AI編集','ON'),('すぐ投稿','ON'),('投稿完了LINE通知','ON'),('顔ぼかし','ON'))

LINE_SETTINGS = table(('チャット','<strong class="off">OFF</strong>'),('あいさつメッセージ','<strong class="on">ON</strong>'),('あいさつの送信条件','初めて友だち追加された時のみ'),('応答メッセージ','<strong class="off">OFF</strong>'),('Webhook','<strong class="on">ON</strong>'),('Webhook再送・エラー統計','両方ON'),('グループ・複数人トーク参加','OFF'),('写真・動画の受信','ON'))

PREP = section('research','01 店舗とInstagramを確認する',
    steps('店舗名、公式サイト、Instagramユーザー名を確認する。公開プロフィールと公式サイトが同じ店舗か照合する。','公式サイト・公開Instagram・お客様の説明から、所在地、公式電話、予約先、業種、商品・サービス、想定するお客様、文章の雰囲気を整理する。','営業時間・定休日・料金に表記差があれば、その項目は未確認として扱う。担当者名、食材、産地、数量、イベントの開催状況を推測しない。','Instagramがプロアカウントのビジネスであることをお客様に確認してもらう。')+
    note('店舗ごとの設定は、その店舗の情報から作ります。他店の名前・住所・ハッシュタグをそのまま使いません。店舗Instagramのパスワードを預かる必要はありません。'))

CREATE_LINE = section('line-create','02 店舗専用LINEを新しく作る',
    steps('<a href="https://manager.line.biz/" target="_blank" rel="noopener">LINE Official Account Manager</a>へBANTEX管理用アカウントでログインし、「作成」を開く。','表示名を「店舗名 インスタ連携」にする。20文字以内に収める。会社名は株式会社バンテックス、業種は店舗の実際の業種を選ぶ。','BANTEX管理用の既存ビジネスマネージャー組織を選ぶ。今回の作成例は「bantex」。','表示された規約と追加同意を担当者が確認し、同意して作成を完了する。アカウント名とLINE IDを確認する。')+
    note('Instagramアカウント1つに、新しい専用LINE BOTを1つ作ります。既存の他店舗BOTを流用・共用しません。AIで作業する場合も、画面で必要な規約同意や権限付与の確認は省略しません。'))

API = section('line-api','03 Messaging APIとWebhookを設定する',
    steps('新しいLINEの「設定」→「Messaging API」→「Messaging APIを利用する」を開き、既存Provider「BANTEX」を選ぶ。','<a href="https://developers.line.biz/console/" target="_blank" rel="noopener">LINE Developers</a>で「BANTEX」→今作った店舗のチャネルを開く。','「Messaging API設定」でWebhook URLを下の値にし、「Webhookの利用」「Webhookの再送」「エラーの統計情報」をONにする。','「検証」を押して「成功」を確認する。チャネル基本設定のChannel ID・Channel secretを新規契約フォームへ直接登録する。')+
    table(('Provider','BANTEX'),('Webhook URL','<code class="technical">https://kokotomo-toc-bot.onrender.com/callback</code>'),('プライバシーポリシー','<a class="technical" href="https://www.bantex.jp/privacy.html">https://www.bantex.jp/privacy.html</a>'),('利用規約','<a class="technical" href="https://www.bantex.jp/terms.html">https://www.bantex.jp/terms.html</a>'))+
    note('アクセストークンはココトモの新規契約登録時に自動発行されます。Channel secret・token・パスワード・認証コードは、マニュアル、チャット、メール、公開スクリーンショットへ載せません。Provider BANTEXが出ない場合は管理権限を確認します。'))

HELLO = section('greeting','04 「LINEに送るだけ」の挨拶を登録する',
    steps('LINE Official Account Managerの「あいさつメッセージ」を開く。LINE Developersの挨拶「編集」からも同じ設定画面へ進める。','初期の「最新情報を配信します」という定型文を、下の標準本文に置き換えて保存する。','「はじめて友だち追加されたときにのみ送信」をONにする。','「設定」→「応答設定」で下の状態に揃える。','ページを再読込し、本文・初回のみ送信・あいさつON・Webhook ONを確認する。')+
    copy_box(GREETING)+LINE_SETTINGS+
    note('本文を保存するだけでは配信されません。あいさつメッセージをONにするところまでが作成作業です。以前の「挨拶をOFF」は、新規顧客BOTでは使いません。'))

PROFILE = section('line-profile','05 LINEの店舗プロフィールを公開する',
    steps('公式サイトや店舗提供の画像から、店舗が分かるアイコンを設定する。','ステータスメッセージは「写真・動画でInstagram投稿」を標準にする。紹介文は店舗の内容に合わせる。','確認済みの郵便番号、所在地、アクセス、公式電話、公式サイト・予約先、店舗Instagramを登録する。','不要な空のSNS欄を除き、店舗に合わせたブランド色を設定する。','「公開」を実行し、公開済みの表示を確認する。')+
    note('責任者名、営業時間、定休日、支払方法、予算など、確認できていない情報を埋めるために推測しません。'))

CONTRACT = section('registration','06 ココトモで新規契約を登録する',
    steps('<a href="https://kokotomo-sns.bantex.jp/sns-admin/onboarding" target="_blank" rel="noopener">ココトモの新規契約センター</a>をBANTEX管理者で開く。','予約投稿枠を1日1枠、月間総投稿上限を31回にする。新しく作った専用LINEであること、Provider BANTEXであることを確認してチェックする。','専用チャネルのChannel ID・Channel secretを保護された入力欄へ直接登録する。','作成を実行し、token発行・Webhook設定・疎通確認の成功、店舗ID、お客様専用画面の発行を確認する。','管理画面で店舗名、予定するInstagramユーザー名とプロフィールURLを登録し、次の店舗設定へ進む。')+
    note('初期フォームにない項目は、登録後の店舗画面で保存します。「登録できた」だけで設定完了とはしません。料金・請求条件は顧客との合意に従い、投稿枠の設定から新たな支払いや有料契約を発生させません。'))

SETTINGS = section('settings','07 投稿・通知・編集の初期値を揃える',
    paragraph('お客様が別の条件を明確に指定していない場合、今回の作成と同じ初期値に揃えます。フォーム初期値のまま終了せず、登録後に保存してください。')+
    INITIAL+steps('店舗画面の「設定」を開き、投稿時刻・通知・加工・顔ぼかしを保存する。','管理画面で月間総投稿上限・動画編集上限を確認する。','保存後にページを再読込し、1日1枠・17:00・月31回・通知ON・顔ぼかしONが一致することを確認する。'))

BUSINESS = section('business','08 店舗情報とAIのルールを全て入れる',
    table(('店舗プロフィール','業種、店舗名、業態・紹介、所在地、責任者、必須表示情報、商品・サービス、店内・設備、想定するお客様。'),('投稿文の雰囲気','その店舗に合う丁寧な日本語。大げさな最上級を避け、写真や説明で確認できる魅力を具体的に伝える。'),('投稿文ルール','料理名・商品名・食材・産地・価格・数量・キャンペーンを推測しない。読みやすく改行し、最後に店舗名・所在地・公式予約先を案内する。'),('ハッシュタグ','本文末尾に5個。地域名と地域＋業種の2タグを店舗ごとに固定し、残り3タグは投稿内容に合わせる。飲食店なら地域グルメ、他業種ならその業種に合うタグにする。未確認のブランド・産地・食材タグは使わない。'),('画像加工','元の被写体・実物・数量・盛り付けを保ち、自然な明るさと色補正で見せる。文字入れは店舗から指定がある場合に行う。'),('動画編集','実際の素材と店舗らしさを保ち、短く分かりやすく伝える。料理名・価格・企画のテロップは確認済みの情報だけ使う。BGMは会話や調理音を妨げない音量にする。'),('避ける内容','未確認の営業情報、値引き、期間限定、在庫・空席、周年イベントを創作しない。顔・個人情報は判別できないよう配慮する。'))+
    note('肉バルでの例：地域タグは #銀座 #銀座グルメ。料理の説明で黒毛和牛使用が確認できたハンバーグ投稿では #銀座ディナー #ハンバーグ #黒毛和牛 を組み合わせます。この地域・料理タグを他店舗にそのまま移しません。')+
    steps('公式情報から各欄を記入し、店舗設定を保存する。','保存後に再取得し、入力した文章・ルール・ON/OFFが残っていることを照合する。','公式情報とお客様の説明が違う場合は、未確認の点をお客様に確認する。'))

APPROVAL_MESSAGE = ('ココトモSNSの店舗設定が完了しました。\n'
    '以下の店舗専用URLを開いてください。\n\n'
    '【発行されたお客様専用URLをここに貼る】\n\n'
    '設定の「Instagram連携」から「Instagramを接続」を押し、店舗のInstagramでログインして連携を許可してください。\n'
    'Instagramの認証はお客様の端末で行います。パスワードを当社にお知らせいただく必要はありません。\n\n'
    '承認が終わりましたら、このLINEにご返信ください。こちらで接続を確認した後、写真・動画の送信用LINEをご案内します。')

INVITE = section('invite','09 お客様には承認用URLだけを渡す',
    steps('管理画面で、この店舗の「お客様URL」を取得する。店舗ごとの専用リンクを使う。','管理者としてログインしていない環境で専用URLを開き、正しい店舗画面が表示されることを確認する。','下の案内文へその店舗の専用URLを貼り、宛先と送信指示を確認してお客様へ案内する。','この段階では投稿用LINEの友だち追加URL・QRコードを渡さない。')+
    copy_box(APPROVAL_MESSAGE)+
    note('使うのはID・パスワード不要のお客様専用URLです。通常の管理画面URLだけ、他店舗のリンク、期限付きのInstagram OAuth URLをそのまま渡さないでください。実顧客の専用URLはこの公開マニュアルに掲載しません。'))

CUSTOMER_APPROVAL = section('customer-approval','10 お客様が自分の端末でInstagramを承認する',
    steps('BANTEXから届いた店舗専用URLを開く。店舗名が自分のお店になっていることを確認する。','「設定」→「Instagram連携」→「Instagramを接続」を押す。','店舗のInstagramでログインする。表示されるユーザー名が予定する店舗アカウントと一致するか確認する。','必要な権限を確認して「許可」を押す。別のアカウントが表示された場合は、許可せず店舗アカウントに切り替える。','連携完了の表示を確認し、BANTEXへ「承認完了」と連絡する。')+
    note('BANTEX側でお客様のInstagramへ代理ログイン・代理承認は行いません。認証コードやパスワードをメール・LINEへ送る必要もありません。'), 'お客様')

CHECK_CONNECTION = section('connection','11 承認後に対象店舗の接続を確認する',
    steps('対象店舗の開通状況・管理画面を再読込する。','Instagramの接続済み表示とユーザー名を確認する。別店舗やテストアカウントが接続されていないか照合する。','投稿に必要なプロフィール参照・コンテンツ公開の権限が揃っていることと、投稿を開始できる状態を確認する。','保存済みの店舗設定、専用LINE、予定するInstagramが同じ店舗に紐づくことを確認する。')+
    note('お客様が「承認した」と連絡しただけで開通完了にはしません。管理画面の実体で確認します。確認待ち・権限不足のままLINEを配布しません。'))

LINE_DISTRIBUTION_MESSAGE = ('Instagramとの接続を確認できました。\n'
    '写真・動画の送信用LINEはこちらです。\n\n'
    '【この店舗専用のLINE友だち追加URLをここに貼る】\n\n'
    '友だち追加すると使い方が届きます。写真・動画と紹介したい内容を、このLINEに送ってください。\n'
    '「明るくして」「この文字を入れて」などの編集希望もLINEで伝えられます。')

DISTRIBUTE = section('distribute','12 接続確認後に専用LINEを配布する',
    steps('対象店舗専用のLINE友だち追加URLを取得する。別店舗のURLを混ぜない。','下の文面へその店舗のLINE URLを貼り、接続確認後にお客様へ案内する。','お客様の友だち追加時に「写真・動画を、このLINEに送るだけ」の挨拶が届くことを確認する。','公開してよい素材で初回投稿を行う場合は、お客様と内容・公開タイミングを確認してから実施する。')+
    copy_box(LINE_DISTRIBUTION_MESSAGE)+
    note('投稿用LINEは店舗スタッフ用です。一般のお客様への宣伝用LINEや公開配布用QRとして案内しません。接続成功と、実際のInstagram投稿成功は分けて確認します。'))

CHECKLIST_TEXT = [
    '専用LINEが新規作成され、店舗Instagramと1対1である',
    'Provider BANTEXと既存組織を確認した',
    '挨拶本文を保存し、初回のみ送信と挨拶ONを再読込で確認した',
    'Webhook利用・再送・エラー統計ONと、検証「成功」を確認した',
    'LINEプロフィールを公開済み表示まで確認した',
    '1日1枠・17:00・月31投稿・月31動画編集を保存して照合した',
    '完了LINE通知・画像加工・動画編集・顔ぼかしONを確認した',
    '店舗情報・文章・ハッシュタグ・画像・動画・避ける内容を保存して照合した',
    '管理者ログインなしで、お客様専用URLから正しい店舗画面を開けた',
    'お客様自身がInstagramを承認した',
    '対象Instagram・必要権限・接続完了を管理画面で確認した',
    '接続確認後に専用LINEを配布した',
]
CHECKLIST = section('checklist','作成・配布前の完了チェック',
    '<p>チェックはこの端末のブラウザにだけ保存されます。次の顧客ではリセットしてください。</p><div class="checklist">'+
    ''.join(f'<label><input type="checkbox" data-check="{i}"><span>{e(text)}</span></label>' for i,text in enumerate(CHECKLIST_TEXT))+
    '</div><button class="reset-checks" type="button">チェックをリセット</button>'+note('承認前は上の9項目まで、承認後に残りを確認します。公開テスト投稿は、このチェックリストとは別にお客様の許可を得て実施します。'))

ERRORS = section('errors','止まった画面に合わせて確認する',
    table(('専用URLでログインを求められる','管理画面の「お客様URL」か確認する。署名付きの店舗専用リンクを再案内する。'),('違うInstagramが表示される','お客様がアカウントを切り替える。BANTEXのテストアカウントで代理承認しない。'),('Instagramの権限が足りない','お客様へ専用URLを再案内し、必要な権限を含めて承認してもらう。承認後に管理画面で再確認する。'),('Webhook検証が失敗する','対象チャネル、URL、Webhookの利用ON、ココトモ登録時の結果を確認する。'),('友だち追加で説明が届かない','挨拶本文保存と、応答設定の挨拶ONを確認する。初回のみ送信の場合、ブロック解除では再送されない。'),('素材にLINEが応答しない','Webhook ON、専用LINEと店舗の紐づき、接続状態、処理結果を確認する。'),('公式の営業情報が食い違う','投稿ルールで断定を避け、お客様に現在の情報を確認する。'))+
    note('お客様のパスワードを聞く、別店舗BOTを流用する、全店舗共通のInstagram tokenを上書きする、承認前にLINEを配布する、といった対処は行いません。'))

CUSTOMER_USE = section('use','LINEに送るだけで投稿を準備する',
    steps('BANTEXから接続確認後に届いた専用LINEを友だち追加する。最初に使い方の挨拶が届く。','写真・動画を送る。複数の写真は続けて送れる。','商品名・料理名・紹介したい内容を続けて送る。希望があれば「明るくして」「この文字を入れて」などの編集依頼も送る。','LINEに届く案内から「すぐ投稿して！」または「定時投稿して！」を選ぶ。投稿内容の確認・修正も案内から行える。','投稿完了のLINE通知と、Instagramの実際の投稿を確認する。')+
    note('予約投稿の初期時刻は17:00です。変更したい場合は、店舗専用画面の設定から変更できます。Instagramの投稿上限は月31回、AI動画編集の上限も月31回を初期値にしています。'), 'お客様')

CUSTOMER_PRO = section('professional','Instagramが個人アカウントの場合',
    steps('店舗のInstagramプロフィールを、お客様本人の端末で開く。','Instagramの設定から、アカウントの種類を確認する。新規運用の標準はプロアカウントの「ビジネス」。','個人アカウントなら、お客様自身がプロアカウントへの切替を行う。カテゴリは店舗の実際の業種を選ぶ。','切替完了後に、店舗専用URLからInstagram連携を承認する。')+
    note('Instagramアプリの画面名はバージョンで変わる場合があります。<a href="https://www.facebook.com/help/instagram/257516379077270" target="_blank" rel="noopener">Instagram公式のプロアカウント案内</a>も確認してください。'), 'お客様')

SOURCES = section('sources','操作画面・公式資料',
    '<ul class="links"><li><a href="https://manager.line.biz/" target="_blank" rel="noopener">LINE Official Account Manager</a></li><li><a href="https://developers.line.biz/console/" target="_blank" rel="noopener">LINE Developers</a></li><li><a href="https://kokotomo-sns.bantex.jp/sns-admin/onboarding" target="_blank" rel="noopener">ココトモ新規契約センター</a></li><li><a href="https://www.lycbiz.com/jp/manual/OfficialAccountManager/greeting-message/" target="_blank" rel="noopener">LINE公式：あいさつメッセージの設定</a></li><li><a href="https://developers.line.biz/ja/docs/messaging-api/building-bot/" target="_blank" rel="noopener">LINE公式：Messaging APIの設定</a></li></ul>'+note('このページは操作手順だけを公開しています。実顧客の専用URL、LINE友だち追加URL、パスワード、Channel secret、tokenは掲載していません。'))

ALL = [PREP, CREATE_LINE, API, HELLO, PROFILE, CONTRACT, SETTINGS, BUSINESS, INVITE, CUSTOMER_APPROVAL, CHECK_CONNECTION, DISTRIBUTE, CHECKLIST, ERRORS, SOURCES]

PAGES = {
    'new-store-onboarding.html':('新規顧客BOTの作成・設定 完全手順','BANTEX・村上さん用','この順番で、調査から承認後のLINE配布まで進めます。',ALL),
    'murakami.html':('村上さんの新規顧客作成手順','村上さん用','開く画面・押すボタン・入力内容・確認結果を、上から順に揃えます。',ALL),
    'simple-customer-onboarding.html':('新規顧客追加 やることだけ','BANTEX用','最短でも省略しない作業と、承認前後の分担です。',[PREP,CREATE_LINE,API,HELLO,PROFILE,CONTRACT,SETTINGS,BUSINESS,INVITE,CUSTOMER_APPROVAL,CHECK_CONNECTION,DISTRIBUTE,CHECKLIST]),
    'setup-admin.html':('LINE BOT・ココトモ 管理側初期設定','BANTEX用','専用LINE、挨拶、Webhook、店舗設定を作成するページです。',[CREATE_LINE,API,HELLO,PROFILE,CONTRACT,SETTINGS,BUSINESS,CHECKLIST,SOURCES]),
    'operator-full.html':('ココトモSNS 新規運用マニュアル','BANTEX・店舗担当者用','全体の分担と、初期設定からLINE運用までを確認できます。',ALL+[CUSTOMER_USE]),
    'instagram-login-onboarding.html':('お客様専用URLとInstagram承認','BANTEX・お客様用','お客様が自分の端末で承認し、接続確認後にLINEを配布します。',[INVITE,CUSTOMER_PRO,CUSTOMER_APPROVAL,CHECK_CONNECTION,DISTRIBUTE,ERRORS]),
    'murakami-instagram-permission-error.html':('Instagram連携・LINE設定の確認','BANTEX・村上さん用','止まった場所を確認し、対象のお客様の承認をやり直します。',[ERRORS,INVITE,CUSTOMER_APPROVAL,CHECK_CONNECTION,HELLO,SOURCES]),
    'store-settings-mobile.html':('スマホで店舗情報・投稿設定を変更する','お客様用','店舗専用URLから、店舗情報と投稿時刻・編集ルールを変更できます。',[section('open','店舗専用の設定画面を開く',steps('BANTEXから届いた店舗専用URLを開く。店舗名を確認する。','画面の「設定」を開く。通常の管理画面ログインID・パスワードは不要。'),'お客様'),section('customer-settings','投稿時刻と編集・通知を変更する',paragraph('初期設定は1日1枠・17:00、画像加工・動画編集・顔ぼかし・投稿完了LINE通知はONです。')+steps('「設定」で投稿時刻、通知、画像・動画の加工、顔ぼかしを確認する。','希望の値に変更し、保存する。','画面を再読込して変更が残っていることを確認する。')+note('月間総投稿上限31回・AI動画編集上限31回は管理側の契約設定です。上限変更を希望する場合はBANTEXへ連絡してください。'),'お客様'),section('customer-business','店舗情報・文章・ハッシュタグを変更する',steps('店舗プロフィールで、店舗名・所在地・商品やサービス・お店の雰囲気を確認する。','文章の雰囲気、投稿文とハッシュタグ、画像加工、動画編集、避ける内容の各ルールを確認する。','現在の店舗情報に合わせて変更し、保存後に再読込して確認する。')+note('分からない情報を推測して入れる必要はありません。営業時間・価格・商品名など、確認できる情報だけ登録してください。'),'お客様'),CUSTOMER_APPROVAL,CUSTOMER_USE,ERRORS]),
    'greeting-message.html':('全新規BOT共通の挨拶メッセージ','BANTEX用','「写真・動画を、このLINEに送るだけ」を標準にします。',[HELLO,CREATE_LINE,API,SOURCES]),
    'customer-approval.html':('Instagram連携の承認をお願いします','お客様用','初めに専用URLで承認し、その後で投稿用LINEをご案内します。',[CUSTOMER_PRO,CUSTOMER_APPROVAL,section('after','承認が終わったら',steps('BANTEXへ「承認完了」と連絡する。','BANTEXが店舗Instagramとの接続を確認する。','確認後に届く投稿用LINEを友だち追加する。'),'お客様'),ERRORS]),
    'customer-line-use.html':('写真・動画をLINEで送る使い方','お客様用','編集の希望や紹介文も、同じLINEに送れます。',[CUSTOMER_USE,section('hello','友だち追加時の使い方',copy_box(GREETING),'お客様'),ERRORS]),
}

def render_page(filename, title, audience, intro, sections):
    toc=''.join(f'<a href="#{sec["id"]}">{display(sec["title"])}</a>' for sec in sections)
    body=''.join(f'<section id="{sec["id"]}" class="manual-section"><header><span class="role">{e(sec["role"])}</span><h2>{display(sec["title"])}</h2></header>{sec["body"]}</section>' for sec in sections)
    download='customer.pdf' if filename.startswith('customer') or filename=='store-settings-mobile.html' else 'admin.pdf'
    return shell(title,audience,intro, f'{FLOW}{COMMON_NOTICE}<div class="manual-layout"><aside class="toc"><details open><summary>このページの目次</summary><nav>{toc}</nav></details></aside><article>{body}</article></div>', download)

def shell(title,audience,intro,body,download='complete.pdf'):
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{e(title)} | ココトモSNS</title><meta name="description" content="{e(intro)}"><link rel="stylesheet" href="assets/manual/style.css?v={VERSION}"><script src="assets/manual/manual.js?v={VERSION}" defer></script></head><body data-version="{VERSION}"><header class="site-head"><a class="brand" href="index.html">BANTEX <span>ココトモSNS マニュアル</span></a><nav><a href="murakami.html">村上さん用</a><a href="customer-approval.html">お客様の承認</a><a href="greeting-message.html">挨拶の標準文</a></nav></header><main class="page"><div class="hero"><p class="eyebrow">{e(audience)} / {VERSION} 更新</p><h1>{display(title)}</h1><p class="intro">{e(intro)}</p><div class="hero-actions"><a class="button" href="new-store-onboarding.html">新規顧客の作成手順</a><a class="button secondary" href="downloads/{download}">PDFで保存・印刷</a></div></div>{body}</main><footer><p>標準ルール {VERSION}。全ての新規顧客BOTに適用。</p><p><a href="index.html">マニュアル一覧</a> / <a href="greeting-message.html">挨拶全文</a> / <a href="downloads/complete.pdf">PDF一式</a></p></footer></body></html>'''

def main():
    for filename,(title,audience,intro,sections) in PAGES.items():
        (ROOT/filename).write_text(render_page(filename,title,audience,intro,sections))
    cards=''.join(f'<a class="card" href="{file}"><span>{e(audience)}</span><h2>{display(title)}</h2><p>{e(intro)}</p><b>手順を開く →</b></a>' for file,(title,audience,intro,_) in PAGES.items())
    content=f'{FLOW}{COMMON_NOTICE}<section class="manual-section"><h2>今回の作りを、全ての新規顧客の標準に</h2>{INITIAL}<p>挨拶はON、WebhookはON、チャット・応答メッセージはOFF。公式情報から店舗設定・ハッシュタグ・画像／動画ルールを埋め、保存後の再確認まで行います。</p></section><div class="cards">{cards}</div>'
    (ROOT/'index.html').write_text(shell('新規顧客の作成・承認・LINE配布','村上さん・BANTEX・店舗担当者用','このURLを開けば、全ての最新手順と標準の挨拶文を読めます。',content))
    (ROOT/'assets/manual/greeting.txt').write_text(GREETING+'\n')
    report={'version':VERSION,'pages':['index.html']+list(PAGES),'shared_rules':'manual-data.json','greeting_characters':len(GREETING)}
    (ROOT/'manual-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':
    main()
