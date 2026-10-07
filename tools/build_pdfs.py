"""公開マニュアルと同じ標準から、社内・お客様・一式のPDFを生成する。"""
import html
import json
import re
from pathlib import Path

from lxml import html as lhtml
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

from build_manuals import ALL, BASE, CUSTOMER_APPROVAL, CUSTOMER_PRO, CUSTOMER_USE, GREETING, ROOT, VERSION, copy_box, section

font_dir=Path('/Users/banmako/dev/ココトモ関係まとめ/tmp/pdfs/rakusta_manuals/fonts')
regular=font_dir/'NotoSansJP-Regular.ttf'
bold=font_dir/'NotoSansJP-Bold.ttf'
if not regular.exists():
    regular=Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
if not bold.exists():
    bold=regular
pdfmetrics.registerFont(TTFont('JP',str(regular)))
pdfmetrics.registerFont(TTFont('JP-Bold',str(bold)))
pdfmetrics.registerFontFamily('JP',normal='JP',bold='JP-Bold',italic='JP',boldItalic='JP-Bold')
styles={
    'body':ParagraphStyle('body',fontName='JP',fontSize=9.3,leading=16.5,spaceAfter=8,wordWrap='CJK',textColor=colors.HexColor('#172b26')),
    'title':ParagraphStyle('title',fontName='JP-Bold',fontSize=21,leading=31,spaceAfter=18,wordWrap='CJK',textColor=colors.HexColor('#172b26')),
    'heading':ParagraphStyle('heading',fontName='JP-Bold',fontSize=14,leading=23,spaceBefore=16,spaceAfter=11,wordWrap='CJK',keepWithNext=True,textColor=colors.HexColor('#157349')),
    'small':ParagraphStyle('small',fontName='JP',fontSize=8,leading=14,spaceAfter=8,wordWrap='CJK',textColor=colors.HexColor('#52645d')),
    'note':ParagraphStyle('note',fontName='JP',fontSize=8.6,leading=15,spaceAfter=11,spaceBefore=8,wordWrap='CJK',borderColor=colors.HexColor('#d8e4dc'),borderWidth=.6,borderPadding=8,backColor=colors.HexColor('#f3f7f3'),textColor=colors.HexColor('#172b26')),
    'label':ParagraphStyle('label',fontName='JP-Bold',fontSize=8.5,leading=15,wordWrap='CJK'),
}

def normalize(text):
    for emoji in ('😊','📷','✨'):
        text=text.replace(emoji,'')
    return text

def rich(node):
    out=html.escape(normalize(node.text or ''))
    for child in node:
        inner=rich(child)
        if child.tag in ('strong','b'):
            inner='<b>'+inner+'</b>'
        elif child.tag=='a' and child.get('href'):
            url=child.get('href')
            if url.startswith('#'):
                inner=inner
            else:
                if '://' not in url:url=BASE+url
                inner='<a href="'+html.escape(url,quote=True)+'" color="#157349">'+inner+'</a>'
        out+=inner+html.escape(normalize(child.tail or ''))
    return out

def p(text,kind='body'):
    return Paragraph(text,styles[kind])

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#d8e4dc'))
    canvas.line(36,35,A4[0]-36,35)
    canvas.setFont('JP',7)
    canvas.setFillColor(colors.HexColor('#52645d'))
    canvas.drawString(36,23,'ココトモSNS 標準ルール '+VERSION)
    canvas.drawRightString(A4[0]-36,23,str(doc.page))

def build(path,title,sections):
    story=[p(html.escape(title),'title'),p('2026年10月7日 更新 / BANTEX','small'),p('全ての新規顧客BOTで、今回の作成手順に統一します。'),p('BANTEXで調査・BOT作成 → 全設定を保存・確認 → お客様専用URLを案内 → お客様がInstagramを承認 → BANTEXが接続確認 → 確認後にLINEを配布','note'),p('操作画面・コピー用の挨拶・最新手順：<a href="'+BASE+'murakami.html" color="#157349">'+BASE+'murakami.html</a>','small'),p('PDFの挨拶表示では絵文字を省いています。LINE登録用にはWebのコピーボタンまたは標準テキストを使ってください。','small')]
    for sec in sections:
        if path.name=='customer.pdf' and sec['id']=='use':
            story.append(PageBreak())
        story.append(p(html.escape(sec['title'])+' <font size="8">'+html.escape(sec['role'])+'</font>','heading'))
        container=lhtml.fragment_fromstring(sec['body'],create_parent='div')
        for node in container:
            if node.tag=='p':
                story.append(p(rich(node),'note' if 'note' in node.get('class','') else 'body'))
            elif node.tag in ('ol','ul'):
                for i,li in enumerate(node,1):
                    story.append(p((str(i)+'. ' if node.tag=='ol' else '・ ')+rich(li)))
            elif node.tag=='dl':
                rows=[[p(rich(row.find('dt')),'label'),p(rich(row.find('dd')))] for row in node]
                table=Table(rows,colWidths=[118,A4[0]-72-118],hAlign='LEFT')
                table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.45,colors.HexColor('#d8e4dc')),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#f3f7f3')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
                story.extend([table,Spacer(1,12)])
            elif node.tag=='div' and 'copy-box' in node.get('class',''):
                text=node.find('pre').text_content()
                text=html.escape(normalize(text)).replace('\n','<br/>')
                story.append(p(text,'note'))
            elif node.tag=='div' and 'checklist' in node.get('class',''):
                for label in node:
                    story.append(p('[ ] '+rich(label.find('span'))))
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=36,rightMargin=36,topMargin=38,bottomMargin=48,title=title,author='BANTEX')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(str(path))
    text='\n'.join(page.extract_text() or '' for page in reader.pages)
    assert '2026年10月7日' in text
    assert 'お客様がInstagramを承認' in text
    assert '\u25a0' not in text
    return {'file':path.name,'pages':len(reader.pages),'bytes':path.stat().st_size}

def main():
    out=ROOT/'downloads'
    out.mkdir(exist_ok=True)
    customer=[CUSTOMER_PRO,CUSTOMER_APPROVAL,CUSTOMER_USE,section('hello','友だち追加時に届く使い方',copy_box(GREETING),'お客様')]
    report=[build(out/'admin.pdf','新規顧客BOT 作成・設定マニュアル',ALL),build(out/'customer.pdf','店舗用 Instagram承認とLINEの使い方',customer),build(out/'complete.pdf','ココトモSNS 新規顧客マニュアル一式',ALL+[CUSTOMER_PRO,CUSTOMER_USE])]
    (out/'pdf-verification.json').write_text(json.dumps({'version':VERSION,'pdfs':report},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
