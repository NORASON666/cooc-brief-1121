# 把 xlsx 指定工作表的「值」原樣排成表格截圖（佐證用，不改任何數字）
import openpyxl, html, asyncio, datetime
from playwright.async_api import async_playwright
X='/Users/nora/Library/CloudStorage/GoogleDrive-nora@hhups.tp.edu.tw/我的雲端硬碟/02Tools/00NoraWiki/raw/meeting-notes/115聯席會/酷課雲相關數據資料_截至1151115.xlsx'
E='/Volumes/WD2T/Projects/cooc-brief-1121/docs/assets/evidence/'
wb=openpyxl.load_workbook(X,data_only=True)
def fmt(v):
    if v is None: return ''
    if isinstance(v,datetime.datetime): return ''   # 年度列的月欄是誤存的日期，原檔即如此
    if isinstance(v,float) and v.is_integer(): v=int(v)
    if isinstance(v,int): return f'{v:,}'
    return html.escape(str(v)).replace('\n','<br>')
def page(sheet,maxc,maxr=None,span=''):
    ws=wb[sheet]; rows=[]
    for r in ws.iter_rows(min_row=1,max_row=maxr or ws.max_row,max_col=maxc,values_only=True):
        if any(v not in (None,'') for v in r): rows.append(r)
    tr=''.join('<tr>'+''.join(f'<{"th" if i==0 else "td"}>{fmt(v)}</{"th" if i==0 else "td"}>' for v in r)+'</tr>' for i,r in enumerate(rows))
    return f'''<html><head><meta charset=utf-8><style>body{{margin:0;padding:24px;font-family:"Noto Sans TC","PingFang TC",sans-serif;background:#fff}}
h1{{font-size:20px;margin:0 0 12px;color:#1E3A6E}}table{{border-collapse:collapse;font-size:15px}}td,th{{border:1px solid #9fb3c8;padding:5px 9px;text-align:right;white-space:nowrap}}
th{{background:#E3ECF5;text-align:center}}td:first-child{{text-align:center;background:#F5F8FB;font-weight:700}}</style></head>
<body><h1>酷課雲相關數據資料.xlsx｜工作表「{sheet}」（數位學習中心彙整；{span}）</h1><table>{tr}</table></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(device_scale_factor=2,viewport={"width":800,"height":400})
        for sheet,mc,mr,out,span in [('總表',9,None,'xls_total','105 年～115/11/15'),('酷AI',11,16,'xls_kuai','112 年～115 年 9 月'),('學科影片YT觀看數',2,None,'xls_yt','自發布至 114/12/31')]:
            await pg.set_content(page(sheet,mc,mr,span)); await pg.wait_for_timeout(300)
            el=await pg.query_selector('body'); bb=await pg.evaluate("()=>[document.body.scrollWidth,document.body.scrollHeight]")
            await pg.set_viewport_size({"width":max(bb[0],1100),"height":bb[1]})
            await pg.wait_for_timeout(200); box=await (await pg.query_selector('body')).bounding_box(); t=await (await pg.query_selector('table')).bounding_box()
            await pg.screenshot(path=E+out+'.png',clip={'x':0,'y':0,'width':max(t['x']+t['width'],(await (await pg.query_selector('h1')).bounding_box())['width']+t['x'])+24,'height':t['y']+t['height']+24}); print(out,bb)
        await b.close()
asyncio.run(main())
