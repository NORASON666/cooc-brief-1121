# 簡報數字核對：從原始資料重算，再比對 content.py 裡出現的每個數字
import openpyxl, re, sys
sys.path.insert(0,'/Volumes/WD2T/Projects/cooc-brief-1121/src')
X='/Users/nora/Library/CloudStorage/GoogleDrive-nora@hhups.tp.edu.tw/我的雲端硬碟/02Tools/00NoraWiki/raw/meeting-notes/115聯席會/酷課雲相關數據資料_截至1151115.xlsx'
wb=openpyxl.load_workbook(X,data_only=True)
ok=lambda c,msg: print(('✅ ' if c else '❌ ')+msg)
# ── 第 35 次紀錄表1（人工判讀 300dpi，兩次一致）
y115=dict(cooc=26843397,onoV=6162183,onoP=227922,yt=5705188,cp=1112137,ai=393002,tot=40215907)
y114=dict(cooc=23934611,onoV=10844663,onoP=270386,yt=5189810,cp=962217,ai=363244,tot=41294545)
cum=dict(cooc=226121791,onoV=242037134,onoP=1908137,yt=35247906,cp=2729592,ai=1140917,tot=507277340)
for n,d in [('115小計',y115),('114同期',y114),('累計',cum)]:
    ok(d['cooc']+d['onoV']+d['yt']+d['cp']+d['ai']==d['tot'], f"PDF {n} 五欄加總＝總量 {d['tot']:,}")
# ── xlsx 115 年工作表與 PDF 比對
ws=wb['115年總計報表']
rows={str(r[0].value).split('\n')[0].strip():[c.value for c in r[1:8]] for r in ws.iter_rows(min_row=1) if r[0].value}
sub=rows['115年小計']; ok(sub==[y115[k] for k in ['cooc','onoV','onoP','yt','cp','ai','tot']], f"xlsx 115年小計＝PDF：{sub}")
m=[rows[f'115/{i}'] for i in range(1,12)]
for j,k in enumerate(['cooc','onoV','onoP','yt','cp','ai']):
    ok(round(sum(r[j] for r in m))==y115[k], f"xlsx 115/1～11 逐月加總 {k}＝{y115[k]:,}")
# ── 總表逐年
T={}
for r in wb['總表'].iter_rows(min_row=2):
    k=str(r[0].value).split('\n')[0].strip().replace('.0','')
    if k[:3].isdigit(): T[k[:3]]=r[7].value if r[7].value is not None else None
print('總表逐年(各年度總瀏覽)：',T)
# 105 列欄位錯位：r[4]
r105=[c.value for c in list(wb['總表'].iter_rows(min_row=3,max_row=3))[0]]
print('105 列原值',r105)
# ── 成長率
for k in ['cooc','onoV','yt','cp','ai','tot']: print(f"  {k}: {(y115[k]/y114[k]-1)*100:+.1f}%")
# ── 酷AI
ai=wb['酷AI']; tot=[r for r in ai.iter_rows(values_only=True) if r[0]=='總計'][0]; print('酷AI 總計列',tot[:11])
yt=wb['學科影片YT觀看數']; print('YT 總計',[r for r in yt.iter_rows(values_only=True) if r[0]=='總計'][0][:2])
