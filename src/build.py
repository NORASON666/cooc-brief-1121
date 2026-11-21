# 產生 docs/index.html：content.py（版面與講稿）＋ supplements.json（補充資料）
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import importlib
CONTENT = os.environ.get('DECK', 'content')
_m = importlib.import_module(CONTENT)
S, SHOT, ILL = _m.S, _m.SHOT, _m.ILL
COVER = getattr(_m, 'COVER', None)
OUT = getattr(_m, 'OUT', 'index.html')
BARTEXT = getattr(_m, 'BARTEXT', '臺北市數位學習中心')

BASE = os.path.dirname(__file__)
sup_path = os.path.join(BASE, "supplements.json")
SUP = json.load(open(sup_path)) if os.path.exists(sup_path) else {}
ILL_EXT = {}
for f in os.listdir(os.path.join(BASE, "..", "docs", ILL)) if os.path.isdir(os.path.join(BASE, "..", "docs", ILL)) else []:
    ILL_EXT[os.path.splitext(f)[0]] = f


def e(s):
    # 跳脫後支援 **粗體** 與換行
    s = html.escape(s or "")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s.replace("\n", "<br>")


def ill(name):
    f = ILL_EXT.get(name)
    return f'<img class="ill" src="{ILL}{f}" alt="">' if f else f'<div class="ill missing">插圖 {name} 製作中</div>'


def dv_img(d):
    # 章節頁右側：有 img 用實機截圖，否則用插圖
    if d.get("img"):
        return f'<img class="ill" style="height:auto;border-radius:24px;box-shadow:0 12px 40px rgba(30,58,110,.18)" src="{SHOT}{d["img"]}" alt="">'
    return ill(d["ill"])


def head(d):
    k = f'<div class="kicker">{e(d["kicker"])}</div>' if d.get("kicker") else ""
    cls = "title sr" if d.get("hide_title") else "title"
    t = f'<h2 class="{cls}"><span>{e(d["title"])}</span></h2>' if d.get("title") else ""
    return k + t


def foot(d):
    out = ""
    if d.get("rel"):
        out += f'<div class="rel"><span class="tag">{e(d["rel"][0])}</span><span>{e(d["rel"][1])}</span></div>'
    if d.get("foot"):
        out += f'<p class="foot">{e(d["foot"])}</p>'
    if d.get("link"):
        out += f'<a class="link" href="{html.escape(d["link"])}" target="_blank" rel="noopener">{html.escape(d["link"])}</a>'
    if d.get("dls"):
        out += '<div class="dls">' + "".join(f'<a class="dl big" href="{html.escape(h)}" download>⬇ {e(l)}</a>' for h, l in d["dls"]) + "</div>"
    if d.get("src"):
        out += f'<p class="src">資料來源｜{e(d["src"])}</p>'
    return out


def render(d):
    t = d["t"]
    if t == "cover" and COVER:
        return f'''<div class="cover"><div class="cover-text">
<div class="org">{e(COVER["org"])}</div><h1>{COVER["h1"]}</h1><div class="hand">{e(COVER["hand"])}</div>
<div class="meta">{e(COVER["meta"])}</div><div class="who"><span>{e(COVER["who"])}</span></div></div></div>'''
    if t == "closing" and COVER:
        return f'''<div class="cover"><div class="cover-text"><h1><mark>謝謝聆聽！</mark></h1><div class="hand">{e(COVER["end"])}</div>
<div class="who"><span>{e(COVER["who"])}</span></div></div></div>'''
    if t == "cover":
        return f'''<div class="cover"><div class="cover-text">
<div class="org">B3 數位教學指引儲備講師培訓工作坊｜試講</div>
<h1>把指引帶進<br><mark>臺北教室</mark></h1>
<div class="hand">少講理論，多看新聞與工具</div>
<div class="meta">2026.11.21（六）　國立臺中教育大學</div>
<div class="who"><span>臺北市數位學習中心 <b>周凡淇</b></span></div>
</div></div>'''
    if t == "closing":
        return f'''<div class="cover"><div class="cover-text">
<h1><mark>謝謝大家！</mark></h1><div class="hand">講指引，就用老師看得到的例子</div>
<div class="meta">臺北的教育型 AI：酷AI（酷課雲）</div>
<div class="who"><span>周凡淇｜臺北市數位學習中心｜nora@hhups.tp.edu.tw</span></div></div></div>'''
    if t == "divider":
        return f'''<div class="divider"><div class="dv-text"><div class="kicker big">{e(d["kicker"])}</div>
<h2 class="dv-title">{e(d["title"])}</h2><div class="dv-sub">{e(d["sub"])}</div></div>
<div class="dv-ill">{dv_img(d)}</div></div>'''
    if t == "bullets":
        tag = "ol" if d.get("numbered") else "ul"
        lis = "".join(f'<li class="{"hl" if i in d.get("hl", []) else ""}">{e(x)}</li>' for i, x in enumerate(d["items"]))
        return f'{head(d)}<{tag} class="bul">{lis}</{tag}>{foot(d)}'
    if t == "shot":
        cls = "shot wide" if d.get("wide") else "shot"
        return f'{head(d)}<div class="{cls}"><img src="{SHOT}{d["img"]}" alt=""></div>{foot(d)}'
    if t == "news":
        cs = "".join(f'<a class="news{" has-shot" if n.get("shot") else ""}" href="{html.escape(n["url"])}" target="_blank" rel="noopener">{f'<img class="nw-shot" src="{SHOT}{n["shot"]}" alt="">' if n.get("shot") else ""}<div class="nw-text"><div class="nw-k"><b>{e(n["outlet"])}</b><span>{e(n["date"])}</span></div><h3>{e(n["head"])}</h3><p>{e(n["line"])}</p><span class="nw-go">看原文 ↗</span></div></a>' for n in d["items"])
        return f'{head(d)}<div class="newsgrid n{len(d["items"])}">{cs}</div>{foot(d)}'
    if t == "newsimg":
        lis = "".join(f'<li><b>{e(h)}</b><span>{e(b)}</span></li>' for h, b in d["items"])
        return f'{head(d)}<div class="ni"><div class="ni-img"><img src="{SHOT}{d["img"]}" alt=""></div><ol class="ni-steps">{lis}</ol></div>{foot(d)}'
    if t == "galaxy":
        # 功能版圖：左側四層文字，右側 three.js 星系（核心＋六大服務節點）；WebGL 不可用時顯示節點清單
        rings = "".join(f'<li><b>{e(h)}</b><span>{e(x)}</span></li>' for h, x in d["rings"])
        nodes = "".join(f'<span class="gx-node">{e(n)}</span>' for n in d["nodes"])
        data = html.escape(json.dumps({"core": d["core"], "nodes": d["nodes"]}, ensure_ascii=False))
        return f'{head(d)}<div class="gx"><ol class="gx-rings">{rings}</ol><div class="gx-stage" data-galaxy="{data}"><div class="gx-fallback"><span class="gx-core">{e(d["core"])}</span>{nodes}</div></div></div>{foot(d)}'
    if t == "nav":
        cs = "".join(f'<button class="navcard" data-go="{g}"><span class="nv-k">{e(k)}</span><span class="nv-t">{e(tt)}</span><span class="nv-m">{e(m)}</span><span class="nv-d">{e(dd)}</span><span class="nv-go">進入 ➜</span></button>' for g, k, tt, m, dd in d["items"])
        return f'{head(d)}<div class="navgrid">{cs}</div>{foot(d)}'
    if t == "flow5":
        cs = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(x)}</p></div>' for h, x in d["steps"])
        return f'{head(d)}<div class="cards c{len(d["steps"])} arrows flow5">{cs}</div>{foot(d)}'
    if t == "shot2":
        imgs = "".join(f'<img src="{SHOT}{i}" alt="">' for i in d["imgs"])
        cls = "three" if len(d["imgs"]) == 3 else "two"
        return f'{head(d)}<div class="shot {cls}">{imgs}</div>{foot(d)}'
    if t == "qrpage":
        lis = "".join(f"<li>{e(x)}</li>" for x in d["lines"])
        return f'{head(d)}<div class="qrpage"><img src="{SHOT}{d["img"]}" alt="LINE 群組 QR Code"><ul class="bul">{lis}</ul></div>{foot(d)}'
    if t == "compare":
        figs = "".join(f'<figure><img src="{SHOT}{i}" alt=""><figcaption>{e(c)}</figcaption></figure>' for i, c in d["imgs"])
        return f'{head(d)}<div class="shot two">{figs}</div>{foot(d)}'
    if t == "shotText":
        ps = "".join(f"<p>{e(x)}</p>" for x in d["text"])
        return f'{head(d)}<div class="st{' small' if d.get('small') else ''}"><div class="st-img"><img src="{SHOT}{d["img"]}" alt=""></div><div class="st-text">{ps}</div></div>{foot(d)}'
    if t == "video":
        if d.get("yt"):
            return f'{head(d)}<div class="shot video"><iframe src="https://www.youtube.com/embed/{d["yt"]}" title="{e(d["title"])}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>{foot(d)}'
        return f'{head(d)}<div class="vid"><video controls preload="metadata" playsinline poster="assets/video/{d["poster"]}" src="assets/video/{d["src_file"]}"></video></div>{foot(d)}'
    if t == "illus":
        if d.get("ill_img"):
            return f'{head(d)}<div class="illus"><img class="ill" src="{SHOT}{d["ill_img"]}" alt=""></div>{foot(d)}'
        return f'{head(d)}<div class="illus">{ill(d["ill"])}</div>{foot(d)}'
    if t == "cards":
        cs = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(b)}</p>{f"<div class=note>{e(n)}</div>" if n else ""}</div>' for h, b, n in d["cards"])
        return f'{head(d)}<div class="cards c{d["cols"]}">{cs}</div>{foot(d)}'
    if t == "redesign":
        cs = "".join(f'<div class="card rd{i}"><h3>{e(h)}</h3><p>{e(b)}</p>{f"<div class=note>{e(n)}</div>" if n else ""}</div>'
                     for i, (h, b, n) in enumerate(d["cols"]))
        return f'{head(d)}<div class="cards c3 arrows">{cs}</div>{foot(d)}'
    if t == "flow":
        cs = "".join(f'<div class="card"><div class="num">{i + 1}</div><h3>{e(h)}</h3><p>{e(b)}</p></div>' for i, (h, b) in enumerate(d["steps"]))
        return f'{head(d)}<div class="cards c4 arrows">{cs}</div>{foot(d)}'
    if t == "steps":
        cs = "".join(f'<li><span class="num">{i + 1}</span><span>{e(x)}</span></li>' for i, x in enumerate(d["steps"]))
        cls = "steps compact" if d.get("compact") else "steps"
        return f'{head(d)}<ol class="{cls}">{cs}</ol>{foot(d)}'
    if t == "case":
        mark = "ABC" if d.get("letters") else "123"
        qs = "".join(f'<li><span class="num">{"" if d.get("letters") else mark[i]}</span><span>{e(q)}</span></li>' for i, q in enumerate(d["qs"]))
        ask = f'<p class="foot">{e(d["ask"])}</p>' if d.get("ask") else ""
        return f'''<div class="kicker">{e(d["kicker"])}</div><div class="situation"><span class="tag">情境</span>{e(d["situation"])}</div>
<ol class="steps qs">{qs}</ol>{ask}{foot(d)}'''
    if t == "table":
        th = "".join(f"<th>{e(x)}</th>" for x in d["head"])
        trs = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in d["rows"])
        cls = "tbl compact" if d.get("compact") else "tbl"
        return f'{head(d)}<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>{foot(d)}'
    if t == "stats":
        cs = "".join(f'<div class="card stat"><div class="big">{e(n)}</div><h3>{e(l)}</h3>{f"<p>{e(s)}</p>" if s else ""}</div>' for n, l, s in d["stats"])
        return f'{head(d)}<div class="cards c{len(d["stats"])}">{cs}</div>{foot(d)}'
    if t == "quote":
        return f'{head(d)}<blockquote class="quote">{e(d["text"])}</blockquote>{foot(d)}'
    if t == "check":
        cs = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(b)}</p></div>' for h, b in d["cols"])
        return f'<div class="kicker">{e(d["kicker"])}</div><blockquote class="quote q2">{e(d["q"])}</blockquote><div class="cards c2">{cs}</div>'
    if t == "aiday":
        lis = "".join(f"<li>{e(x)}</li>" for x in d["lines"])
        qr = f'<img class="qr" src="{SHOT}{d["qr"]}" alt="QR code">' if d.get("qr") else ""
        return f'''<div class="kicker">案例激盪｜從 AI Day 看到什麼？</div><h2 class="title"><span>{e(d["title"])}</span></h2>
<div class="aiday"><ul class="bul">{lis}</ul>{qr}</div>{foot(d)}'''
    if t == "prompt":
        size = " small" if d.get("small") else (" mid" if d.get("mid") else (" big" if len(d["text"]) <= 220 else ""))
        return f'{head(d)}<div class="prompt code{size}"><button class="copy">複製</button><pre>{html.escape(d["text"])}</pre></div>{foot(d)}'
    if t == "sources":
        cols = "".join("<ul>" + "".join(f"<li>{e(x)}</li>" for x in c) + "</ul>" for c in d["cols"])
        return f'<div class="kicker">來源</div><h2 class="title"><span>{e(d["title"])}</span></h2><div class="srcs">{cols}</div>'
    raise ValueError(t)


def sup_html(n):
    items = SUP.get(str(n), []) + CUR_SUP
    out = []
    for it in items:
        pts = "".join(f"<li>{e(p)}</li>" for p in it.get("points", []))
        cl = "".join(f"<li>{e(p)}</li>" for p in it.get("classroom", []))
        cl = f'<div class="cl"><b>課堂可以這樣做</b><ol>{cl}</ol></div>' if cl else ""
        rd = "".join(f"<p>{e(x)}</p>" for x in it.get("read", []))
        rd = f'<details class="rd" open><summary>深入閱讀</summary>{rd}</details>' if rd else ""
        lm = "".join(f"<li>{e(x)}</li>" for x in it.get("limits", []))
        lm = f'<div class="lm"><b>研究限制・引用提醒</b><ul>{lm}</ul></div>' if lm else ""
        tk = f'<div class="tk"><b>上台可以這樣說</b><p>{e(it["talk"])}</p></div>' if it.get("talk") else ""
        url = f' <a href="{html.escape(it["url"])}" target="_blank" rel="noopener">原文</a>' if it.get("url") else ""
        ev = it.get("evidence", "")
        code = ""
        if it.get("code"):
            code = f'<div class="code"><button class="copy">複製</button><pre>{html.escape(it["code"])}</pre></div>'
        if it.get("download"):
            code += f'<p><a class="dl" href="{html.escape(it["download"])}" download>⬇ {e(it.get("download_label","下載"))}</a></p>'
        out.append(f'''<article class="sup"><div class="sup-k"><span class="kind">{e(it.get("kind",""))}</span><span class="ev ev-{html.escape(ev)}">{e(ev)}</span></div>
<h4>{e(it["title"])}</h4><ul>{pts}</ul>{rd}{lm}{tk}{cl}{code}<p class="sup-src">{e(it.get("source",""))}{url}</p></article>''')
    return "".join(out), len(items)


CUR_SUP = []
slides, side = [], []
main, spare = 0, 0
sec = "home"
for d in S:
    sec = d.get("sec", sec)
    # 主體頁編 1、2、3…；備用段（spare=True）編「備1、備2…」
    if d.get("spare"):
        spare += 1; label = f"備{spare}"
    else:
        main += 1; label = str(main)
    note = d.get("notes", "")
    body = render(d)
    if d.get("art"):  # 右側配圖：公版原圖或 Codex 插圖
        src = d["art"] if "/" in d["art"] else SHOT + d["art"]
        body = f'<div class="wa"><div class="wa-main">{body}</div><figure class="wa-art"><img src="{src}" alt="">{f"<figcaption>{e(d[chr(97)+chr(114)+chr(116)+chr(99)+chr(97)+chr(112)])}</figcaption>" if d.get("artcap") else ""}</figure></div>'
    CUR_SUP = d.get("sup", [])
    sh, cnt = sup_html(label)
    badge = f'<button class="supbtn" title="補充資料（S）">📎 補充（{cnt} 則）</button>' if cnt else ""
    slides.append(f'<section class="slide t-{d["t"]}" id="p{label}" data-label="{label}" data-sec="{sec}"><div class="inner">{body}</div>{badge}<div class="pno">{label}</div></section>')
    side.append({"n": label, "notes": note, "sup": sh})

tpl = open(os.path.join(BASE, "template.html")).read()
out = tpl.replace("<!--SLIDES-->", "\n".join(slides)).replace("/*SIDE*/[]", json.dumps(side, ensure_ascii=False)).replace("/*BARTEXT*/'臺北市數位學習中心'", json.dumps(BARTEXT, ensure_ascii=False))
open(os.path.join(BASE, "..", "docs", OUT), "w").write(out)
print("slides", len(slides), "with supplements", sum(1 for s in side if s["sup"]))
