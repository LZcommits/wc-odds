#!/usr/bin/env python3
# 多场采样 + 手机 H5(目录 + 详情页:移盘曲线/+EV/比分概率矩阵/全盘口/对阵分析)
import json, os, sys, math, datetime, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'data'); DOCS = os.path.join(ROOT, 'docs')
os.makedirs(DATA_DIR, exist_ok=True); os.makedirs(DOCS, exist_ok=True)
KEY = os.environ.get('ODDS_API_KEY', '').strip()
if not KEY: sys.exit('缺少 ODDS_API_KEY 环境变量')
TZ = datetime.timezone.utc
def ko(y, mo, d, h): return datetime.datetime(y, mo, d, h, 0, 0, tzinfo=TZ)

MATCHES = [
 {'slug': 'belgium_egypt', 'home': 'Belgium', 'away': 'Egypt', 'cn_h': '比利时', 'cn_a': '埃及',
  'ko': ko(2026,6,15,19), 'tier': '②中热门 · 价值区', 'my': {'home':0.50,'draw':0.27,'away':0.23},
  'st': {'h2h':'4 次友谊赛交锋,埃及胜 2(2022年2-1、2005年4-0),比利时最大胜2018年3-0。埃及交锋不落下风。',
   'fh':'4-2-3-1/4-3-3','fa':'4-2-3-1(保守反击)',
   'xh':'库尔图瓦把门,德布劳内组织,卢卡库锋线;黄金一代但老化',
   'xa':'萨拉赫(刚经历利物浦低迷赛季)+马尔穆什 双快;整体退守(主帅Hossam Hassan)',
   'mu':['德布劳内创造力 vs 埃及密集中场:能否撕开铁桶是胜负手',
         '萨拉赫/马尔穆什速度 vs 比利时老化后防(转身慢):埃及反击最大威胁',
         '卢卡库支点 vs 埃及中卫身体对抗'],
   'note':'Opta:比利时37% vs 埃及36%(几乎五五开)→②档价值区铁证。价值:平/小球/埃及受让'}},
 {'slug': 'saudi_uruguay', 'home': 'Saudi Arabia', 'away': 'Uruguay', 'cn_h': '沙特', 'cn_a': '乌拉圭',
  'ko': ko(2026,6,15,22), 'tier': '①悬殊 · ⚡冷门警报', 'my': {'home':0.18,'draw':0.26,'away':0.56},
  'st': {'h2h':'历史交锋很少、无重要正赛记录,参考价值低。',
   'fh':'4-2-3-1(主帅Donis)','fa':'4-2-3-1(比尔萨)',
   'xh':'Al-Buraikan锋线,Al-Juwayr 10号,Al-Dawsari边路(2022绝杀阿根廷的人);门将Al-Owais(Al-Aqidi伤)',
   'xa':'Darwin Núñez锋线,Valverde+Ugarte+Bentancur中场;后防伤兵多(Giménez/Araújo/Cáceres存疑)',
   'mu':['乌拉圭中场三人组(Valverde/Ugarte/Bentancur)控场 vs 沙特',
         'Al-Dawsari反击 vs 乌拉圭边路:沙特爆冷的火种(他2022掀翻阿根廷)',
         '乌拉圭后防伤兵 → 沙特定位球/反击有机会'],
   'note':'①档(乌66%)但乌后防伤兵+沙特爆冷基因+揭幕效应→平/沙受让/小球。⚡冷门警报'}},
 {'slug': 'france_senegal', 'home': 'France', 'away': 'Senegal', 'cn_h': '法国', 'cn_a': '塞内加尔',
  'ko': ko(2026,6,16,19), 'tier': '①临界② · 已追踪', 'my': {'home':0.58,'draw':0.26,'away':0.16},
  'st': {'h2h':'第4次交锋,塞内加尔历史占优(前3次胜2)。经典:2002世界杯揭幕战塞1-0爆冷卫冕冠军法国(P.B.Diop),法国小组赛一场不胜出局。',
   'fh':'4-2-3-1','fa':'4-3-3',
   'xh':'姆巴佩领衔(距法国队史射手王仅2球);中前场出球强',
   'xa':'Nicolas Jackson(拜仁)顶锋线,Iliman Ndiaye(埃弗顿)踢10号;整体高大+反击快',
   'mu':['姆巴佩(速度) vs 塞内加尔中卫(转身):法国边路爆点的胜负手',
         '塞内加尔反击箭头 vs 法国回追:法国压上易被打身后',
         '中场对抗:法国技术 vs 塞内加尔身体'],
   'note':'死亡之组;法国揭幕战有翻车史(2002负塞)。①档(法65%)但塞实力被低估→平/塞/小球有价值'}},
 {'slug': 'argentina_algeria', 'home': 'Argentina', 'away': 'Algeria', 'cn_h': '阿根廷', 'cn_a': '阿尔及利亚',
  'ko': ko(2026,6,17,1), 'tier': '①悬殊 · ⚡冷门警报', 'my': {'home':0.62,'draw':0.23,'away':0.15},
  'st': {'h2h':'交锋少。阿根廷卫冕冠军近5场友谊赛全胜仅失1球;阿尔及利亚世界杯历史从未进过8强。',
   'fh':'4-3-3','fa':'4-2-3-1/4-3-3',
   'xh':'Emi Martínez门将;Molina-Romero-Lisandro-Tagliafico;De Paul-Mac Allister-Almada;Messi+Lautaro+Enzo(梅西第200次出场、第6届世界杯)',
   'xa':'Zidane门将;Belghali-Mandi-Chergui-Aït-Nouri;Bentaleb-Boudaoui;Mahrez-Maza-Amoura;Gouiri顶前',
   'mu':['梅西 vs 马赫雷斯:两队头牌的隔空对决',
         '阿尔及利亚Amoura/Gouiri速度 vs 阿根廷中卫:反击能否打身后',
         '马赫雷斯(右路) vs Tagliafico(阿左后卫)'],
   'note':'①档(阿71%)。阿根廷强,但揭幕战警惕(2022曾负沙特);价值在砍屠杀+小球。⚡冷门警报'}},
]
COL = {'home':'#2563eb','draw':'#6b7280','away':'#d97706'}

CSS = """body{font-family:-apple-system,system-ui,sans-serif;margin:0;background:#f7f7f8;color:#1a1a1a;padding:16px;max-width:480px;margin:0 auto}
h1{font-size:19px;font-weight:600;margin:0 0 2px}a{color:inherit;text-decoration:none}
.sub{color:#666;font-size:13px;margin-bottom:16px}
.row{display:flex;gap:8px;margin-bottom:16px}
.card{flex:1;background:#fff;border-radius:12px;padding:12px 8px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.lbl{font-size:12px;color:#666}.big{font-size:24px;font-weight:600;margin:2px 0}.chg{font-size:12px}
.panel{background:#fff;border-radius:12px;padding:14px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.panel h2{font-size:14px;font-weight:600;margin:0 0 10px}
table{width:100%;border-collapse:collapse;font-size:14px}
td{padding:7px 6px;border-bottom:1px solid #f0f0f0}th{font-size:12px;color:#888;text-align:left;padding:4px 6px}
.foot{color:#999;font-size:12px;text-align:center;margin-top:18px}.note{font-size:12px;color:#666;line-height:1.6}
.mcard{display:block;background:#fff;border-radius:12px;padding:13px;margin-bottom:11px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.mtitle{font-size:16px;font-weight:600;margin-bottom:2px}.mtier{font-size:12px;color:#888;margin-bottom:8px}
.mprob{font-size:13px;color:#444}.mval{font-size:13px;margin-top:6px}
.pill{display:inline-block;padding:2px 8px;border-radius:20px;font-size:12px;margin-right:4px;margin-bottom:3px}
.sc{display:flex;flex-wrap:wrap;gap:6px}.scb{background:#eef2ff;border-radius:8px;padding:6px 9px;font-size:13px}
.scb b{color:#1e3a8a}.mtag{font-size:13px;color:#444;margin:4px 0}.mtag b{color:#111}"""

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)

def fetch_bulk():
    return get("https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
               f"?apiKey={KEY}&regions=eu,uk&markets=h2h,totals,spreads&oddsFormat=decimal&dateFormat=iso")

def fetch_extra(eid):
    try:
        return get("https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/events/"
                   f"{eid}/odds?apiKey={KEY}&regions=eu&markets=btts,double_chance&oddsFormat=decimal")
    except Exception:
        return None

def mkt(book, key):
    return next((m for m in book.get('markets', []) if m['key'] == key), None) if book else None

def h2h(b, home, away):
    m = mkt(b, 'h2h')
    if not m: return None
    o = {}
    for oc in m['outcomes']:
        o['home' if oc['name'] == home else ('away' if oc['name'] == away else 'draw')] = oc['price']
    return o if len(o) == 3 else None

def totals(b):
    m = mkt(b, 'totals')
    if not m: return None
    o = {}
    for oc in m['outcomes']:
        if abs(oc.get('point', 0) - 2.5) < .01: o[oc['name'].lower()] = oc['price']
    return o or None

def spreads(b, home):
    m = mkt(b, 'spreads')
    if not m: return None
    for oc in m['outcomes']:
        if oc['name'] == home:
            other = next((x for x in m['outcomes'] if x['name'] != home), None)
            return {'pt': oc.get('point'), 'home': oc['price'], 'away': other['price'] if other else None}
    return None

def devig(d):
    inv = {k: 1/v for k, v in d.items() if v}; s = sum(inv.values())
    return {k: inv[k]/s for k in inv}

# ---- 泊松比分概率 ----
def pois(k, lam): return math.exp(-lam) * lam**k / math.factorial(k)
def solve_mu(under_prob):
    if not under_prob: return 2.6
    lo, hi = 0.2, 6.0
    cdf2 = lambda mu: math.exp(-mu)*(1+mu+mu*mu/2)
    for _ in range(60):
        mid = (lo+hi)/2
        if cdf2(mid) > under_prob: lo = mid
        else: hi = mid
    return (lo+hi)/2
def split_lambda(mu, p_home, p_away):
    target = p_home/(p_home+p_away) if (p_home+p_away) > 0 else 0.5
    lo, hi = 0.05, mu-0.05
    for _ in range(34):
        lh = (lo+hi)/2; la = mu-lh
        ph = pa = 0.0
        for i in range(8):
            for j in range(8):
                p = pois(i, lh)*pois(j, la)
                if i > j: ph += p
                elif i < j: pa += p
        share = ph/(ph+pa) if (ph+pa) > 0 else .5
        if share < target: lo = lh
        else: hi = lh
    lh = (lo+hi)/2
    return lh, mu-lh
def scoreline_top(p_h, p_a, under_prob, n=6):
    mu = solve_mu(under_prob)
    lh, la = split_lambda(mu, p_h, p_a)
    grid = []
    for i in range(6):
        for j in range(6):
            grid.append((f'{i}-{j}', pois(i, lh)*pois(j, la)))
    grid.sort(key=lambda x: -x[1])
    return lh, la, grid[:n]

now = datetime.datetime.now(TZ)
try: data = fetch_bulk()
except Exception as e: data = []; print('bulk error', e)

def find(cfg): return next((m for m in data if m['home_team'] == cfg['home'] and m['away_team'] == cfg['away']), None)
def load_rows(slug):
    p = os.path.join(DATA_DIR, slug+'.jsonl')
    rows = []
    if os.path.exists(p):
        for l in open(p):
            l = l.strip()
            if not l: continue
            try: r = json.loads(l)
            except Exception: continue
            if 'devig' not in r and 'devig_pin' in r: r['devig'] = r['devig_pin']
            rows.append(r)
    return [r for r in rows if r.get('devig')]

def process(cfg):
    m = find(cfg)
    rich = {}
    if m:
        books = m['bookmakers']
        pin = next((b for b in books if b['key'] == 'pinnacle'), None)
        ph = h2h(pin, cfg['home'], cfg['away']) if pin else None
        allh = [x for x in (h2h(b, cfg['home'], cfg['away']) for b in books) if x]
        soft = {k: round(sum(x[k] for x in allh)/len(allh), 3) for k in ('home','draw','away')} if allh else None
        src = ph or soft
        hrs = round((cfg['ko']-now).total_seconds()/3600, 1)
        if src:
            dv = {k: round(v, 4) for k, v in devig(src).items()}
            rec = {'ts': now.isoformat(timespec='minutes'), 'hrs_to_ko': hrs, 'pin_h2h': ph,
                   'soft_h2h': soft, 'pin_tot25': totals(pin) if pin else None, 'devig': dv, 'n_books': len(allh)}
            with open(os.path.join(DATA_DIR, cfg['slug']+'.jsonl'), 'a') as f:
                f.write(json.dumps(rec, ensure_ascii=False)+'\n')
            print('sampled', cfg['slug'], hrs, 'h')
        # 富盘口快照(仅未开赛)
        rich['spread'] = spreads(pin, cfg['home']) if pin else None
        rich['tot'] = totals(pin) if pin else None
        if 0 < hrs < 48:
            ev = fetch_extra(m['id'])
            if ev and ev.get('bookmakers'):
                bks = ev['bookmakers']
                bt = next((mkt(b, 'btts') for b in bks if mkt(b, 'btts')), None)
                dc = next((mkt(b, 'double_chance') for b in bks if mkt(b, 'double_chance')), None)
                rich['btts'] = {o['name']: o['price'] for o in bt['outcomes']} if bt else None
                rich['dc'] = {o['name']: o['price'] for o in dc['outcomes']} if dc else None
    return rich

def L(cfg): return {'home': cfg['cn_h'], 'draw': '平局', 'away': cfg['cn_a']}

def sparkline(rows):
    if len(rows) < 2: return '<p style="color:#888;font-size:13px">采样 ≥2 档后显示移盘曲线</p>'
    W, H, pad, ymax = 320, 120, 24, 0.95; n = len(rows)
    pts = lambda k: ' '.join(f'{pad+i*(W-2*pad)/(n-1):.1f},{H-pad-(r["devig"][k]/ymax)*(H-2*pad):.1f}' for i, r in enumerate(rows))
    lines = ''.join(f'<polyline fill="none" stroke="{COL[k]}" stroke-width="2" points="{pts(k)}"/>' for k in ('home','draw','away'))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:340px"><line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="#ddd"/>{lines}</svg>')

def cards(rows, cfg):
    l = L(cfg); last = rows[-1]; first = rows[0]; out = ''
    for k in ('home','draw','away'):
        cur = last['devig'][k]*100; dv = (last['devig'][k]-first['devig'][k])*100
        arr = '▲' if dv > .2 else ('▼' if dv < -.2 else '–'); ac = '#16a34a' if dv > .2 else ('#dc2626' if dv < -.2 else '#999')
        out += f'<div class="card"><div class="lbl">{l[k]}</div><div class="big" style="color:{COL[k]}">{cur:.1f}%</div><div class="chg" style="color:{ac}">{arr} {dv:+.1f}pt</div></div>'
    return out

def evtable(rows, cfg):
    l = L(cfg); p = rows[-1].get('pin_h2h')
    if not p: return ''
    out = ''
    for k in ('home','draw','away'):
        ev = cfg['my'][k]*p[k]
        tag, bg = ('✅ 有价值', '#dcfce7') if ev > 1.03 else (('— 临界', '#fef9c3') if ev > .99 else ('❌ 别碰', '#fee2e2'))
        out += f'<tr style="background:{bg}"><td>{l[k]}</td><td>{cfg["my"][k]:.0%}</td><td>{p[k]}</td><td>{ev:.2f}</td><td>{tag}</td></tr>'
    return out

def scores_html(rows):
    last = rows[-1]; d = last['devig']; u = (last.get('pin_tot25') or {}).get('under')
    up = None
    if u and (last.get('pin_tot25') or {}).get('over'):
        up = devig({'over': last['pin_tot25']['over'], 'under': u})['under']
    lh, la, top = scoreline_top(d['home'], d['away'], up)
    chips = ''.join(f'<div class="scb"><b>{s}</b> {p*100:.0f}%</div>' for s, p in top)
    return (f'<div class="sc">{chips}</div>'
            f'<div class="note" style="margin-top:8px">由赔率反推:预期进球 主 {lh:.2f} / 客 {la:.2f}。'
            f'(The Odds API 无逐比分赔率,此为泊松模型概率)</div>')

def markets_html(cfg, rows, rich):
    l = L(cfg); p = rows[-1].get('pin_h2h'); t = rich.get('tot') or rows[-1].get('pin_tot25')
    rowshtml = ''
    if p: rowshtml += f'<tr><td>胜平负</td><td>{l["home"]} {p["home"]} · 平 {p["draw"]} · {l["away"]} {p["away"]}</td></tr>'
    if t: rowshtml += f'<tr><td>大小球 2.5</td><td>大 {t.get("over","-")} · 小 {t.get("under","-")}</td></tr>'
    sp = rich.get('spread')
    if sp and sp.get('pt') is not None:
        rowshtml += f'<tr><td>让球(亚盘)</td><td>{l["home"]} {sp["pt"]:+g} @{sp["home"]} · {l["away"]} {-sp["pt"]:+g} @{sp.get("away","-")}</td></tr>'
    if rich.get('btts'): rowshtml += f'<tr><td>双方进球</td><td>是 {rich["btts"].get("Yes","-")} · 否 {rich["btts"].get("No","-")}</td></tr>'
    if rich.get('dc'):
        dc = ' · '.join(f'{k} {v}' for k, v in rich['dc'].items())
        rowshtml += f'<tr><td>双重机会</td><td>{dc}</td></tr>'
    return f'<table>{rowshtml}</table>' if rowshtml else '<p class="note">暂无盘口数据</p>'

def analysis_html(cfg):
    s = cfg['st']; l = L(cfg)
    mu = ''.join(f'<div class="mtag">• {x}</div>' for x in s['mu'])
    return (f'<div class="mtag"><b>历史交锋:</b>{s["h2h"]}</div>'
            f'<div class="mtag"><b>阵型:</b>{l["home"]} {s["fh"]} ｜ {l["away"]} {s["fa"]}</div>'
            f'<div class="mtag"><b>{l["home"]}:</b>{s["xh"]}</div>'
            f'<div class="mtag"><b>{l["away"]}:</b>{s["xa"]}</div>'
            f'<div class="mtag" style="margin-top:6px"><b>关键对位:</b></div>{mu}'
            f'<div class="note" style="margin-top:8px;color:#b45309">{s["note"]}</div>')

def build_detail(cfg, rows, rich):
    l = L(cfg); title = f'{cfg["cn_h"]} vs {cfg["cn_a"]}'
    if not rows:
        body = '<div class="panel note">暂无数据(比赛可能已开赛或尚未采样)</div>'; hrs = n = updated = '?'
    else:
        last = rows[-1]; hrs = last['hrs_to_ko']; n = len(rows); updated = last['ts']
        body = (f'<div class="row">{cards(rows, cfg)}</div>'
                f'<div class="panel"><h2>移盘曲线(锐庄去水位概率)</h2>{sparkline(rows)}'
                f'<div style="font-size:12px;color:#666;margin-top:2px"><span style="color:#2563eb">{l["home"]}</span> <span style="color:#6b7280">平</span> <span style="color:#d97706">{l["away"]}</span> · 左早→右临场</div></div>'
                f'<div class="panel"><h2>实时 +EV(我的概率 × 锐庄赔率)</h2><table><tr><th>结果</th><th>我估</th><th>锐庄</th><th>EV</th><th>判定</th></tr>{evtable(rows, cfg)}</table></div>'
                f'<div class="panel"><h2>比分概率(泊松反推 Top6)</h2>{scores_html(rows)}</div>'
                f'<div class="panel"><h2>全盘口快照(锐庄)</h2>{markets_html(cfg, rows, rich)}</div>'
                f'<div class="panel"><h2>对阵分析</h2>{analysis_html(cfg)}</div>')
    html = (f'<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title} · 移盘追踪</title><style>{CSS}</style></head><body>'
            f'<div class="sub"><a href="index.html">← 返回目录</a></div><h1>{title}</h1>'
            f'<div class="sub">{cfg["tier"]} · 距开赛约 <b>{hrs}h</b> · 数据档数 {n} · 更新 {updated} UTC</div>'
            f'{body}<div class="foot">自动每 3h 更新 · 仅供研究,非投注建议</div></body></html>')
    open(os.path.join(DOCS, cfg['slug']+'.html'), 'w').write(html)

def build_index(items):
    mc = ''
    for cfg, rows, rich in items:
        title = f'{cfg["cn_h"]} vs {cfg["cn_a"]}'; l = L(cfg)
        if not rows:
            mc += f'<a class="mcard" href="{cfg["slug"]}.html"><div class="mtitle">{title}</div><div class="mtier">{cfg["tier"]} · 暂无数据</div></a>'; continue
        last = rows[-1]; d = last['devig']; p = last.get('pin_h2h') or {}
        prob = f'<span style="color:#2563eb">{l["home"]} {d["home"]:.0%}</span> · <span style="color:#6b7280">平 {d["draw"]:.0%}</span> · <span style="color:#d97706">{l["away"]} {d["away"]:.0%}</span>'
        vals = ''
        for k in ('home','draw','away'):
            if p and cfg['my'][k]*p[k] > 1.03:
                vals += f'<span class="pill" style="background:#dcfce7">{l[k]} +{(cfg["my"][k]*p[k]-1)*100:.0f}%</span>'
        if not vals: vals = '<span class="pill" style="background:#f0f0f0">暂无明显价值</span>'
        ks = f'距开赛 {last["hrs_to_ko"]}h' if last['hrs_to_ko'] > 0 else '已开赛'
        mc += (f'<a class="mcard" href="{cfg["slug"]}.html"><div class="mtitle">{title} ›</div>'
               f'<div class="mtier">{cfg["tier"]} · {ks}</div><div class="mprob">{prob}</div><div class="mval">{vals}</div></a>')
    html = (f'<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>世界杯赔率追踪</title><style>{CSS}</style></head><body><h1>世界杯赔率价值追踪</h1>'
            f'<div class="sub">{len(items)} 场 · 每 3h 自动更新 · {now.isoformat(timespec="minutes")} UTC(北京 +8h)</div>{mc}'
            f'<div class="panel note"><b>读法:</b>绿药丸=我模型算出的 +EV 方向;点卡片看移盘曲线/比分概率/全盘口/对阵分析。仅供研究,非投注建议。</div>'
            f'<div class="foot">The Odds API · GitHub Actions</div></body></html>')
    open(os.path.join(DOCS, 'index.html'), 'w').write(html)

items = []
for cfg in MATCHES:
    rich = process(cfg)
    rows = load_rows(cfg['slug'])
    build_detail(cfg, rows, rich)
    items.append((cfg, rows, rich))
build_index(items)
print('完成', len(items), '场')
