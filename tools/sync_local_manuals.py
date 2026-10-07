"""新旧の手元の配布資料を同じ標準版に揃える。顧客固有情報は扱わない。"""
import argparse
import json
import shutil
from pathlib import Path
from build_manuals import BASE, ROOT, VERSION

def main():
    args=argparse.ArgumentParser()
    args.add_argument('--workspace',type=Path,required=True)
    workspace=args.parse_args().workspace.resolve()
    if not (workspace/'docs').is_dir():
        raise SystemExit('ココトモ資料ワークスペースのdocsが必要です')
    output=workspace/'output'
    output.mkdir(exist_ok=True)
    backup=output/('archive-manuals-before-'+VERSION.replace('-',''))
    report=[]
    def save(path,data):
        path=workspace/path
        if path.exists():
            old=backup/path.relative_to(workspace)
            if not old.exists():
                old.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(path,old)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        report.append(str(path.relative_to(workspace)))
    def redirect(page,title):
        url=BASE+page
        return ('<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta http-equiv="refresh" content="0;url={url}"><title>{title} 最新版</title>'
            '<style>body{font-family:sans-serif;max-width:680px;margin:40px auto;padding:0 20px;line-height:1.8}a{overflow-wrap:anywhere}</style>'
            f'<h1>{title} 最新版</h1><p>{VERSION}更新。最新手順へ移動します。</p><p><a href="{url}">{url}</a></p>'
            '<p>店舗設定 → お客様専用URL → お客様本人のInstagram承認 → 接続確認 → LINE配布。挨拶はONを標準にします。</p></html>').encode()
    html_map={
        'output/ココトモ_新規契約_インスタ連携_作業順マニュアル_20260817.html':'murakami.html',
        'output/ココトモ_新規契約_インスタ連携_作業順マニュアル_送付用_20260818.html':'murakami.html',
        'output/ココトモ_新規契約_インスタ連携_作業順マニュアル_20260820.html':'murakami.html',
        'output/お客様用_BANTEXメール受信後のInstagram連携_20260820.html':'customer-approval.html',
        'output/お客様用_Instagramプロアカウント確認と切替_20260820.html':'customer-approval.html',
        'output/ココトモSNS_新規契約マニュアル_20260928/index.html':'murakami.html',
    }
    for path,page in html_map.items():
        save(path,redirect(page,'ココトモSNSマニュアル'))
    for path in [
        'output/ココトモ_新規契約_インスタ連携_作業順マニュアル_20260817.md',
        'output/ココトモ_新規契約_インスタ連携_作業順マニュアル_20260820.md',
        'output/楽スタ_新規顧客開通_時系列チェックリスト_20260813.md',
    ]:
        save(path,('# ココトモSNS 新規顧客マニュアル 最新版\n\n'+VERSION+'更新。\n\n'+
            '[村上さん用の最新手順]('+BASE+'murakami.html) / [全マニュアル]('+BASE+')\n\n'+
            '店舗設定 → お客様専用URL → お客様本人のInstagram承認 → 接続確認 → LINE配布に統一します。挨拶は標準本文を保存し、初回のみ送信ON・挨拶ONまで確認します。\n\n'+
            '配布用PDFは同じoutput/pdfの「最新版」を使用してください。旧本文はarchive-manuals-before-20261007へ保存しています。\n').encode())
    pdf_map={
        'output/pdf/新規契約_BOT作成とココトモ設定_最新版.pdf':'admin.pdf',
        'output/pdf/お客様用_Instagram承認とLINEの使い方_最新版.pdf':'customer.pdf',
        'output/pdf/ココトモSNS_新規顧客マニュアル一式_最新版.pdf':'complete.pdf',
        'output/社内用_ココトモ新規契約_インスタ連携_作業順マニュアル_20260820.pdf':'admin.pdf',
    }
    for date in ('20260812','20260813'):
        pdf_map.update({
            f'output/pdf/楽スタ_BANTEX新規契約_LINEBot設定マニュアル_{date}.pdf':'admin.pdf',
            f'output/pdf/楽スタ_店舗向け_Instagram_LINEかんたん設定_{date}.pdf':'customer.pdf',
            f'output/pdf/楽スタ_新規契約マニュアル_2冊セット_{date}.pdf':'complete.pdf',
        })
    for path,filename in pdf_map.items():
        save(path,(ROOT/'downloads'/filename).read_bytes())
    current=output/('manual-standard-'+VERSION.replace('-',''))
    current.mkdir(exist_ok=True)
    portable=(ROOT/'murakami.html').read_text().replace(f'<link rel="stylesheet" href="assets/manual/style.css?v={VERSION}">',
        '<style>'+(ROOT/'assets/manual/style.css').read_text()+'</style>').replace(f'<script src="assets/manual/manual.js?v={VERSION}" defer></script>',
        '')
    portable=portable.replace('</body>','<script>'+(ROOT/'assets/manual/manual.js').read_text()+'</script></body>')
    portable=portable.replace('<head>','<head><base href="'+BASE+'">')
    (current/'村上さん用_新規顧客標準手順.html').write_text(portable)
    for filename in ('admin.pdf','customer.pdf','complete.pdf'):
        shutil.copy2(ROOT/'downloads'/filename,current/filename)
    shutil.copy2(ROOT/'manual-data.json',workspace/'docs/新規顧客BOT_標準設定.json')
    shutil.copy2(ROOT/'assets/manual/greeting.txt',workspace/'docs/LINEあいさつメッセージ_標準.txt')
    (current/'updated-files.json').write_text(json.dumps({'version':VERSION,'updated':report,'archive':str(backup)},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'version':VERSION,'updated_files':len(report),'output':str(current)},ensure_ascii=False))

if __name__=='__main__':main()
