#!/usr/bin/env python3
# 多场采样 + 手机 H5(Midnight Quantum 暗色玻璃拟态设计)
import json, os, sys, math, datetime, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'data'); DOCS = os.path.join(ROOT, 'docs')
os.makedirs(DATA_DIR, exist_ok=True); os.makedirs(DOCS, exist_ok=True)
KEY = os.environ.get('ODDS_API_KEY', '').strip()
if not KEY: sys.exit('缺少 ODDS_API_KEY 环境变量')
AFKEY = os.environ.get('API_FOOTBALL_KEY', '').strip()
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
COL = {'home':'#CCFF00', 'draw':'#8e9379', 'away':'#FF0055'}  # 移盘曲线用色
AFID = {'belgium_egypt':1489377, 'saudi_uruguay':1489379, 'france_senegal':1489383, 'argentina_algeria':1489381}
REASON = {
 'belgium_egypt': ['市场基准(锐庄去水位):比利时 ≈62% / 平 ≈24% / 埃及 ≈16%',
  '分档:② 中热门——比利时是黄金一代大牌,正是大众情绪最易高估的格口',
  '修正① 揭幕效应:世界杯首轮热门常熄火(本届巴西/瑞士已被逼平)→ 热门胜率打折',
  '修正② 阵容相克:比利时后防老化、转身慢;埃及有萨拉赫+马尔穆什速度反击 → 埃及上调',
  '修正③ 交锋史:埃及 4 次交锋胜 2,不怵比利时 → 平/埃及再上调',
  '结论:比利时 62%→50%、平 24%→27%、埃及 16%→23% → 价值在 平 / 埃及 / 小球'],
 'saudi_uruguay': ['市场基准:乌拉圭 ≈66% / 平 ≈22% / 沙特 ≈12%',
  '分档:① 悬殊(乌66%),但带揭幕+冷门基因 → 按②的逆向思路处理',
  '修正① 揭幕效应:强热门首战遇硬骨头,易被拖入苦战',
  '修正② 阵容:乌拉圭后防伤兵多(Giménez/Araújo/Cáceres 存疑)→ 失球风险升,乌下调',
  '修正③ 冷门基因:沙特 2022 掀翻阿根廷,Al-Dawsari 反击犀利 → 沙特/平上调',
  '结论:乌 66%→56%、平 22%→26%、沙 12%→18% → 价值在 平 / 沙特受让 / 小球。⚡'],
 'france_senegal': ['市场基准:法国 ≈65% / 平 ≈21% / 塞内加尔 ≈13%',
  '分档:① 临界 ②(法65%),球星光环(姆巴佩)易被高估',
  '修正① 揭幕效应 + 法国揭幕翻车史(2002 正是负塞内加尔出局)',
  '修正② 阵容:塞内加尔高大强壮+反击快(Jackson/Ndiaye),实力被低估',
  '修正③ 交锋史:塞内加尔历史交锋占优(前 3 次胜 2)',
  '结论:法 65%→58%、平 21%→26%、塞 13%→16% → 价值在 平 / 塞内加尔 / 小球'],
 'argentina_algeria': ['市场基准:阿根廷 ≈69% / 平 ≈21% / 阿尔及利亚 ≈10%',
  '分档:① 悬殊(阿69%),阿根廷卫冕冠军+近 5 场全胜状态火热',
  '修正① 揭幕效应:阿根廷 2022 揭幕战曾爆冷负沙特 → 胜率略打折',
  '修正② 阵容:阿尔及利亚有 Mahrez/Amoura/Gouiri 反击质量,但整体差距大',
  '修正③ 实力差距真实 → 不过度逆向(①档热门基本会赢)',
  '结论:阿 69%→62%、平 21%→23%、阿尔 10%→15% → 价值主要在 砍屠杀 + 小球(不反胜负)。⚡'],
}

CSS = """*{box-sizing:border-box}
:root{--navy:#020617;--bg:#051424;--low:#0d1c2d;--surf:#122131;--high:#1c2b3c;--on:#d4e4fa;--sec:#bec6e0;--lime:#CCFF00;--crim:#FF0055;--line:rgba(255,255,255,.1)}
body{margin:0 auto;max-width:520px;background:var(--bg);color:var(--on);font-family:Inter,system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased;padding:70px 16px 84px}
a{color:inherit;text-decoration:none}
.mono{font-family:'JetBrains Mono',monospace}
.material-symbols-outlined{font-family:'Material Symbols Outlined';font-weight:400;font-size:20px;line-height:1;vertical-align:middle}
.appbar{position:fixed;top:0;left:0;right:0;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;background:rgba(2,6,23,.72);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);z-index:50}
.brand{display:flex;align-items:center;gap:6px;color:var(--lime);font-weight:800;font-size:18px;letter-spacing:-.02em}
.barIcons{display:flex;gap:14px;color:var(--sec);opacity:.7}
h1.title{font-size:24px;font-weight:800;letter-spacing:-.02em;color:var(--lime);margin:0 0 6px}
.sub{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec);opacity:.7;letter-spacing:.04em;line-height:1.6}
.back{display:inline-flex;align-items:center;gap:2px;color:var(--sec);font-family:'JetBrains Mono',monospace;font-size:12px;margin-bottom:10px;opacity:.8}
.glass{background:rgba(13,28,45,.7);border:1px solid var(--line);backdrop-filter:blur(10px);border-radius:8px;padding:16px;margin-bottom:16px}
h2.sec{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--lime);margin:0 0 12px}
.mcard{display:block;background:rgba(13,28,45,.7);border:1px solid var(--line);backdrop-filter:blur(10px);border-radius:8px;padding:16px;margin-bottom:14px}
.mtitle{font-size:20px;font-weight:700;letter-spacing:-.01em;display:flex;align-items:center;gap:4px}
.chev{color:var(--sec);opacity:.5;font-size:18px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.chip{font-family:'JetBrains Mono',monospace;font-size:10px;padding:2px 6px;border-radius:3px;border:1px solid rgba(190,198,224,.2);color:var(--sec);letter-spacing:.03em}
.chip.val{border-color:rgba(204,255,0,.4);color:var(--lime);background:rgba(204,255,0,.06)}
.chip.warn{border-color:rgba(255,0,85,.45);color:var(--crim);background:rgba(255,0,85,.06)}
.chip.dim{border:none;color:rgba(190,198,224,.55)}
.probrow{display:flex;gap:10px;margin:14px 0;font-size:14px}
.probrow>div{flex:1}
.fav{color:var(--lime);font-weight:700}
.dimv{color:var(--sec);opacity:.6}
.pills{display:flex;flex-wrap:wrap;gap:8px}
.pill{background:var(--lime);color:var(--navy);font-weight:700;font-size:14px;padding:6px 12px;border-radius:9999px;box-shadow:0 0 12px rgba(204,255,0,.25)}
.pill.none{background:var(--high);color:var(--sec);box-shadow:none}
.row{display:flex;gap:8px;margin-bottom:16px}
.card{flex:1;background:rgba(13,28,45,.7);border:1px solid var(--line);border-radius:8px;padding:12px 6px;text-align:center}
.lbl{font-size:12px;color:var(--sec);opacity:.7}
.big{font-size:26px;font-weight:800;letter-spacing:-.04em;margin:3px 0}
.chg{font-size:12px}
table{width:100%;border-collapse:collapse;font-size:14px}
th{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.6;text-align:left;padding:5px 6px;text-transform:uppercase;letter-spacing:.03em}
td{padding:8px 6px;border-bottom:1px solid rgba(255,255,255,.06)}
td.num{font-family:'JetBrains Mono',monospace}
tr.val td{background:rgba(204,255,0,.09)}
tr.bad td{background:rgba(255,0,85,.09)}
.sc{display:flex;flex-wrap:wrap;gap:8px}
.scb{background:var(--high);border:1px solid var(--line);border-radius:3px;padding:7px 10px;font-family:'JetBrains Mono',monospace;font-size:13px}
.scb b{color:var(--lime)}
.mtag{font-size:13px;color:var(--sec);margin:5px 0;line-height:1.65}
.mtag b{color:var(--on)}
.note{font-size:12px;color:var(--sec);opacity:.8;line-height:1.7}
.note b{color:var(--lime)}
.nav{position:fixed;bottom:0;left:0;right:0;height:64px;display:flex;justify-content:space-around;align-items:center;background:rgba(2,6,23,.9);backdrop-filter:blur(14px);border-top:1px solid var(--line);z-index:50;max-width:520px;margin:0 auto}
.nav a{display:flex;flex-direction:column;align-items:center;gap:2px;color:var(--sec);opacity:.55;font-family:'JetBrains Mono',monospace;font-size:11px}
.nav a.on{color:var(--lime);opacity:1;font-weight:700}
.foot{text-align:center;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.5;margin:16px 0 4px}"""

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
def fetch_bulk():
    return get("https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
               f"?apiKey={KEY}&regions=eu,uk&markets=h2h,totals,spreads&oddsFormat=decimal&dateFormat=iso")
def fetch_extra(eid):
    try:
        return get("https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/events/"
                   f"{eid}/odds?apiKey={KEY}&regions=eu&markets=btts,double_chance&oddsFormat=decimal")
    except Exception: return None
def fetch_exact_score(afid):
    if not AFKEY or not afid: return None
    try:
        req = urllib.request.Request(f"https://v3.football.api-sports.io/odds?fixture={afid}&bet=10",
                                     headers={'x-apisports-key': AFKEY})
        d = json.load(urllib.request.urlopen(req, timeout=30))
    except Exception as e: print('api-football error', e); return None
    resp = d.get('response', [])
    if not resp: return None
    cands = []
    for bm in resp[0].get('bookmakers', []):
        vals = bm['bets'][0]['values'] if bm.get('bets') else []
        parsed = {}
        for v in vals:
            try: parsed[v['value'].replace(':', '-').strip()] = float(v['odd'])
            except Exception: pass
        if parsed: cands.append((len(parsed), bm['name'], parsed))
    if not cands: return None
    cands.sort(key=lambda x: -x[0])
    _, name, parsed = cands[0]
    return {'book': name, 'odds': parsed}

def mkt(book, key): return next((m for m in book.get('markets', []) if m['key'] == key), None) if book else None
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

def pois(k, lam): return math.exp(-lam) * lam**k / math.factorial(k)
def solve_mu(under_prob):
    if not under_prob: return 2.6
    lo, hi = 0.2, 6.0; cdf2 = lambda mu: math.exp(-mu)*(1+mu+mu*mu/2)
    for _ in range(60):
        mid = (lo+hi)/2
        if cdf2(mid) > under_prob: lo = mid
        else: hi = mid
    return (lo+hi)/2
def split_lambda(mu, p_home, p_away):
    target = p_home/(p_home+p_away) if (p_home+p_away) > 0 else 0.5
    lo, hi = 0.05, mu-0.05
    for _ in range(34):
        lh = (lo+hi)/2; la = mu-lh; ph = pa = 0.0
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
def poisson_calc(p_h, p_a, under_prob):
    mu = solve_mu(under_prob); lh, la = split_lambda(mu, p_h, p_a)
    grid = {f'{i}-{j}': pois(i, lh)*pois(j, la) for i in range(6) for j in range(6)}
    return lh, la, grid

now = datetime.datetime.now(TZ)
try: data = fetch_bulk()
except Exception as e: data = []; print('bulk error', e)

def find(cfg): return next((m for m in data if m['home_team'] == cfg['home'] and m['away_team'] == cfg['away']), None)
def load_rows(slug):
    p = os.path.join(DATA_DIR, slug+'.jsonl'); rows = []
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
    m = find(cfg); rich = {}
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
            so = fetch_exact_score(AFID.get(cfg['slug']))
            if so: rich['score_odds'] = so
    return rich

def L(cfg): return {'home': cfg['cn_h'], 'draw': '平局', 'away': cfg['cn_a']}

# ---------- UI 组件 ----------
def head(title):
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title} · PRO ANALYTICS</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">'
            '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style>')
APPBAR = ('<header class="appbar"><div class="brand"><span class="material-symbols-outlined">analytics</span>PRO ANALYTICS</div>'
          '<div class="barIcons"><span class="material-symbols-outlined">search</span>'
          '<span class="material-symbols-outlined">notifications</span></div></header>')
def nav(active='value'):
    items = [('matches','sports_soccer','Matches'),('value','trending_up','Value'),('signals','sensors','Signals'),('account','person','Account')]
    a = ''.join(f'<a class="{"on" if k==active else ""}"><span class="material-symbols-outlined">{ic}</span>{lb}</a>' for k, ic, lb in items)
    return f'<nav class="nav">{a}</nav>'
def tier_chips(cfg, hrs):
    out = ''
    for p in [x.strip() for x in cfg['tier'].split('·')]:
        cls = 'chip val' if '价值' in p else ('chip warn' if ('冷门' in p or '警报' in p) else 'chip')
        out += f'<span class="{cls}">{p}</span>'
    out += f'<span class="chip dim">{("距开赛 "+str(hrs)+"h") if hrs>0 else "已开赛"}</span>'
    return f'<div class="chips">{out}</div>'
def probrow(d, cfg):
    l = L(cfg); mx = max(d, key=d.get); al = {'home':'left','draw':'center','away':'right'}
    cells = ''.join(f'<div class="{"fav" if k==mx else "dimv"}" style="text-align:{al[k]}">{l[k]} {d[k]*100:.0f}%</div>' for k in ('home','draw','away'))
    return f'<div class="probrow">{cells}</div>'
def value_pills(p, cfg):
    l = L(cfg); pills = ''
    for k in ('home','draw','away'):
        if p and cfg['my'][k]*p[k] > 1.03:
            pills += f'<span class="pill">{l[k]} +{(cfg["my"][k]*p[k]-1)*100:.0f}%</span>'
    if not pills: pills = '<span class="pill none">暂无明显价值</span>'
    return f'<div class="pills">{pills}</div>'

def sparkline(rows):
    if len(rows) < 2: return '<p class="note">采样 ≥2 档后显示移盘曲线</p>'
    W, H, pad, ymax = 320, 120, 24, 0.95; n = len(rows)
    pts = lambda k: ' '.join(f'{pad+i*(W-2*pad)/(n-1):.1f},{H-pad-(r["devig"][k]/ymax)*(H-2*pad):.1f}' for i, r in enumerate(rows))
    lines = ''.join(f'<polyline fill="none" stroke="{COL[k]}" stroke-width="2" points="{pts(k)}"/>' for k in ('home','draw','away'))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:340px"><line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="#273647"/>{lines}</svg>')

def cards(rows, cfg):
    l = L(cfg); last = rows[-1]; first = rows[0]; d = last['devig']; mx = max(d, key=d.get); out = ''
    for k in ('home','draw','away'):
        cur = d[k]*100; dv = (d[k]-first['devig'][k])*100
        if dv >= 0.05: arr, ac = '↑', '#CCFF00'
        elif dv <= -0.05: arr, ac = '↓', '#FF0055'
        else: arr, ac = '→', '#8e9379'
        out += (f'<div class="card"><div class="lbl">{l[k]}</div>'
                f'<div class="big" style="color:{"#CCFF00" if k==mx else "#d4e4fa"}">{cur:.1f}%</div>'
                f'<div class="chg mono" style="color:{ac}">{arr} {abs(dv):.1f}%</div></div>')
    return out

def evtable(rows, cfg):
    l = L(cfg); p = rows[-1].get('pin_h2h')
    if not p: return ''
    out = ''
    for k in ('home','draw','away'):
        ev = cfg['my'][k]*p[k]
        cls, tag = ('val','✅ 有价值') if ev > 1.03 else (('','— 临界') if ev > .99 else ('bad','❌ 别碰'))
        out += f'<tr class="{cls}"><td>{l[k]}</td><td class="num">{cfg["my"][k]:.0%}</td><td class="num">{p[k]}</td><td class="num">{ev:.2f}</td><td>{tag}</td></tr>'
    return out

def scores_html(lh, la, grid):
    top = sorted(grid.items(), key=lambda x: -x[1])[:6]
    chips = ''.join(f'<div class="scb"><b>{s}</b> {p*100:.0f}%</div>' for s, p in top)
    return f'<div class="sc">{chips}</div><div class="note" style="margin-top:8px">由赔率反推:预期进球 主 {lh:.2f} / 客 {la:.2f}(泊松模型公允概率)</div>'

def score_odds_html(rich, grid):
    so = rich.get('score_odds')
    if not so: return '<p class="note">逐比分赔率暂无(部分书商临近开赛才上盘)</p>'
    odds = so['odds']; top = sorted(odds.items(), key=lambda x: x[1])[:12]
    h = (f'<div class="note" style="margin-bottom:8px">书商:{so["book"]} · 共 {len(odds)} 个比分 · EV=模型推测×盘口,&gt;1 即有价值</div>'
         f'<table><tr><th>比分</th><th>盘口</th><th>模型推测</th><th>期望值</th></tr>')
    for s, o in top:
        pp = grid.get(s, 0); ev = pp*o
        h += f'<tr class="{"val" if ev>1.05 else ""}"><td class="num">{s}</td><td class="num">{o}</td><td class="num">{pp*100:.0f}%</td><td class="num">{ev:.2f}</td></tr>'
    return h + '</table>'

def markets_html(cfg, rows, rich):
    l = L(cfg); p = rows[-1].get('pin_h2h'); t = rich.get('tot') or rows[-1].get('pin_tot25'); r = ''
    if p: r += f'<tr><td>胜平负</td><td class="num">{l["home"]} {p["home"]} · 平 {p["draw"]} · {l["away"]} {p["away"]}</td></tr>'
    if t: r += f'<tr><td>大小球 2.5</td><td class="num">大 {t.get("over","-")} · 小 {t.get("under","-")}</td></tr>'
    sp = rich.get('spread')
    if sp and sp.get('pt') is not None:
        r += f'<tr><td>让球(亚盘)</td><td class="num">{l["home"]} {sp["pt"]:+g} @{sp["home"]} · {l["away"]} {-sp["pt"]:+g} @{sp.get("away","-")}</td></tr>'
    if rich.get('btts'): r += f'<tr><td>双方进球</td><td class="num">是 {rich["btts"].get("Yes","-")} · 否 {rich["btts"].get("No","-")}</td></tr>'
    if rich.get('dc'):
        r += f'<tr><td>双重机会</td><td class="num">{" · ".join(f"{k} {v}" for k,v in rich["dc"].items())}</td></tr>'
    return f'<table>{r}</table>' if r else '<p class="note">暂无盘口数据</p>'

def analysis_html(cfg):
    s = cfg['st']; l = L(cfg)
    mu = ''.join(f'<div class="mtag">• {x}</div>' for x in s['mu'])
    return (f'<div class="mtag"><b>历史交锋:</b>{s["h2h"]}</div>'
            f'<div class="mtag"><b>阵型:</b>{l["home"]} {s["fh"]} ｜ {l["away"]} {s["fa"]}</div>'
            f'<div class="mtag"><b>{l["home"]}:</b>{s["xh"]}</div>'
            f'<div class="mtag"><b>{l["away"]}:</b>{s["xa"]}</div>'
            f'<div class="mtag" style="margin-top:6px"><b>关键对位:</b></div>{mu}'
            f'<div class="note" style="margin-top:8px;color:var(--lime)">{s["note"]}</div>')

def reasoning_html(cfg):
    steps = REASON.get(cfg['slug'], [])
    if not steps: return '<p class="note">暂无推理</p>'
    return ''.join(f'<div class="mtag"><b>{i+1}.</b> {s}</div>' for i, s in enumerate(steps))

def build_detail(cfg, rows, rich):
    l = L(cfg); title = f'{cfg["cn_h"]} vs {cfg["cn_a"]}'
    if not rows:
        inner = '<div class="glass"><p class="note">暂无数据(比赛可能已开赛或尚未采样)</p></div>'; hrs = n = updated = '?'
    else:
        last = rows[-1]; hrs = last['hrs_to_ko']; n = len(rows); updated = last['ts']
        d = last['devig']; t25 = last.get('pin_tot25') or {}
        up = devig({'over': t25['over'], 'under': t25['under']})['under'] if (t25.get('over') and t25.get('under')) else None
        lh, la, grid = poisson_calc(d['home'], d['away'], up)
        inner = (f'<div class="row">{cards(rows, cfg)}</div>'
                 f'<div class="glass"><h2 class="sec">移盘曲线</h2>{sparkline(rows)}'
                 f'<div class="note" style="margin-top:4px"><span style="color:{COL["home"]}">{l["home"]}</span> · <span style="color:{COL["draw"]}">平</span> · <span style="color:{COL["away"]}">{l["away"]}</span> · 左早→右临场</div></div>'
                 f'<div class="glass"><h2 class="sec">实时 期望值</h2><table><tr><th>结果</th><th>我估</th><th>锐庄</th><th>期望值</th><th>判定</th></tr>{evtable(rows, cfg)}</table></div>'
                 f'<div class="glass"><h2 class="sec">推理过程</h2>{reasoning_html(cfg)}</div>'
                 f'<div class="glass"><h2 class="sec">逐比分赔率</h2>{score_odds_html(rich, grid)}</div>'
                 f'<div class="glass"><h2 class="sec">比分概率 Top6</h2>{scores_html(lh, la, grid)}</div>'
                 f'<div class="glass"><h2 class="sec">全盘口快照</h2>{markets_html(cfg, rows, rich)}</div>'
                 f'<div class="glass"><h2 class="sec">对阵分析</h2>{analysis_html(cfg)}</div>')
    body = (f'{APPBAR}<main>'
            f'<a class="back" href="index.html"><span class="material-symbols-outlined">chevron_left</span>返回目录</a>'
            f'<h1 class="title">{title}</h1>'
            f'<div class="sub">{cfg["tier"]} · 距开赛 {hrs}h · 数据档数 {n} · {updated} UTC</div>'
            f'<div style="height:12px"></div>{inner}'
            f'<div class="foot">自动每 3h 更新 · 仅供研究,非投注建议</div></main>{nav("value")}')
    open(os.path.join(DOCS, cfg['slug']+'.html'), 'w').write(f'<!DOCTYPE html><html lang="zh" class="dark"><head>{head(title)}</head><body>{body}</body></html>')

def build_index(items):
    mc = ''
    for cfg, rows, rich in items:
        title = f'{cfg["cn_h"]} vs {cfg["cn_a"]}'
        if not rows:
            mc += f'<a class="mcard" href="{cfg["slug"]}.html"><div class="mtitle">{title}</div>{tier_chips(cfg, 0)}</a>'; continue
        last = rows[-1]; d = last['devig']; p = last.get('pin_h2h') or {}
        mc += (f'<a class="mcard" href="{cfg["slug"]}.html">'
               f'<div class="mtitle">{title} <span class="material-symbols-outlined chev">chevron_right</span></div>'
               f'{tier_chips(cfg, last["hrs_to_ko"])}{probrow(d, cfg)}{value_pills(p, cfg)}</a>')
    body = (f'{APPBAR}<main>'
            f'<h1 class="title">世界杯赔率价值追踪</h1>'
            f'<div class="sub">{len(items)} 场 · 每 3h 自动更新 · {now.isoformat(timespec="minutes")} UTC(北京 +8h)</div>'
            f'<div style="height:14px"></div>{mc}'
            f'<div class="glass"><h2 class="sec">读法指南</h2><p class="note"><b>绿药丸</b> = 模型算出的 +EV 方向(价值投注机会);点卡片看移盘曲线 / 比分概率 / 全盘口 / 对阵分析。仅供研究,非投注建议。</p></div>'
            f'<div class="foot">The Odds API · API-Football · GitHub Actions</div></main>{nav("value")}')
    open(os.path.join(DOCS, 'index.html'), 'w').write(f'<!DOCTYPE html><html lang="zh" class="dark"><head>{head("世界杯赔率追踪")}</head><body>{body}</body></html>')

items = []
for cfg in MATCHES:
    rich = process(cfg); rows = load_rows(cfg['slug'])
    build_detail(cfg, rows, rich); items.append((cfg, rows, rich))
build_index(items)
print('完成', len(items), '场')
