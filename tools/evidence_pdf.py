import asyncio, base64, os
from playwright.async_api import async_playwright
D='/private/tmp/claude-502/m35/pdfimg/'
OUT=os.environ['OUT']
P=[("一、第 35 次臺北市數位學習聯席會議紀錄（115/11/17 會議，核定簽）表1「酷課雲平臺」量化成效表","統計至 115/11/15。簡報用到：各平臺累計 507,277,340；115 年小計 40,215,907；114 年同期 41,294,545；各平臺 115 年與 114 年同期。","m35_table1.png"),
("二、同紀錄 伍、業務報告 一（酷AI 學習系統推廣情形）","截至 115/10/25：已辦理 361 場教育訓練，培訓講師回報約 9,269 位教師。","m35_kuai.png"),
("三、同紀錄 表3 二代「CooC+」影片支數統計表","彙整至 115/11/16：合計 5,281 支，其中新課綱動畫影片（與均一合作）2,310 支。","m35_table3.png"),
("四、數位學習中心彙整《酷課雲相關數據資料》.xlsx 工作表「總表」","105 年～115/11/15 各平臺逐年瀏覽；簡報「十年軌跡」長條圖依「各年度總瀏覽人次」欄（110 年 173,879,902）。","xls_total.png"),
("五、同檔 工作表「酷AI」","112 年～115 年 9 月：授課總堂數 53,361；AI 出題題目數 171,294；市／校／班課程包 3,448／3,528／1,031（合計 8,007）；教師公開分享教學包 599。","xls_kuai.png"),
("六、同檔 工作表「學科影片YT觀看數」","各播放清單自發布至 114/12/31 觀看數，總計 11,491,515。","xls_yt.png"),
("七、臺北酷課雲首頁「酷課雲使用數據」（https://cooc.tp.edu.tw/，2026-11-21 擷取）","註冊帳號數 1,470,939；總瀏覽人次 226,815,498（不含酷AI、OnO、YouTube）。","cooc_stats.png"),
("八、臺北酷課雲 YouTube 頻道 @CooC-Cloud（2026-11-21 擷取）","9,052 部影片、16.4 萬位訂閱者。","yt_head.png"),
("九、教育部 AI 人才方舟計畫 A2 數位學習平臺推薦名單（https://pads.moe.edu.tw/teacher_list.php，2026-11-21 擷取）","臺北酷課雲列入推薦名單，效期 115.10.16～118.12.31。","a2_list.png")]
def b64(f): return base64.b64encode(open(D+f,'rb').read()).decode()
LAND={"xls_total.png","xls_kuai.png","a2_list.png","cooc_stats.png","yt_head.png"}
pages=''.join(f'''<section class="{'land' if f in LAND else ''}"><h2>{t}</h2><p class=n>{n}</p><div class=img><img src="data:image/png;base64,{b64(f)}"></div></section>''' for t,n,f in P)
html=f'''<html><head><meta charset=utf-8><style>
@page{{size:A4;margin:14mm 12mm}}body{{font-family:"Noto Sans TC","PingFang TC",sans-serif;color:#1d2b3a;margin:0}}
.cover{{page-break-after:always;padding-top:60mm}}.cover h1{{font-size:28pt;color:#1E3A6E;margin:0 0 6mm}}.cover p{{font-size:13pt;line-height:1.7}}
.cover ol{{font-size:12pt;line-height:1.8}}
section{{page-break-after:always;display:flex;flex-direction:column;height:268mm}}@page land{{size:A4 landscape}}section.land{{page:land;height:180mm}}section:last-child{{page-break-after:auto}}
h2{{font-size:14pt;color:#1E3A6E;margin:0 0 2mm;line-height:1.4}}.n{{font-size:11pt;margin:0 0 4mm;color:#444;line-height:1.5;border-left:3px solid #F0A23B;padding-left:3mm}}
.img{{flex:1;min-height:0;display:flex;align-items:flex-start;justify-content:center}}img{{max-width:100%;max-height:100%;object-fit:contain;border:1px solid #c9d4df}}
</style></head><body><div class=cover><h1>臺北酷課雲 局處長官簡報<br>數據佐證資料</h1>
<p>簡報網址：https://norason666.github.io/cooc-brief-1121/<br>整理：臺北市數位學習中心｜2026-11-21</p>
<p>簡報上的數字依下列原始資料；每頁一份，原樣擷取、未改動數值。</p><ol>{''.join(f"<li>{t.split('、',1)[1]}</li>" for t,_,_ in P)}</ol></div>{pages}</body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.set_content(html); await pg.wait_for_timeout(800)
        await pg.pdf(path=OUT,format='A4',print_background=True,margin={"top":"14mm","bottom":"14mm","left":"12mm","right":"12mm"})
        await b.close()
asyncio.run(main())
