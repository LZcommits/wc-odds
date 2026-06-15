#!/usr/bin/env python3
# 多场采样 The Odds API + 生成手机 H5(目录页 + 每场详情页)
# 依赖:仅标准库;key 从环境变量 ODDS_API_KEY 读取;每次仅 1 次 API 调用覆盖全部比赛
import json, os, sys, datetime, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
DOCS = os.path.join(ROOT, 'docs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS, exist_ok=True)
KEY = os.environ.get('ODDS_API_KEY', '').strip()
if not KEY:
    sys.exit('缺少 ODDS_API_KEY 环境变量')

TZ = datetime.timezone.utc
def ko(y, mo, d, h):
    return datetime.datetime(y, mo, d, h, 0, 0, tzinfo=TZ)

# ===== 追踪的比赛(改这里增删)=====
MATCHES = [
    {'slug': 'belgium_egypt', 'home': 'Belgium', 'away': 'Egypt', 'cn_h': '比利时', 'cn_a': '埃及',
     'ko': ko(2026, 6, 15, 19), 'tier': '②中热门 · 价值区', 'my': {'home': 0.50, 'draw': 0.27, 'away': 0.23}},
    {'slug': 'saudi_uruguay', 'home': 'Saudi Arabia', 'away': 'Uruguay', 'cn_h': '沙特', 'cn_a': '乌拉圭',
     'ko': ko(2026, 6, 15, 22), 'tier': '①悬殊 · ⚡冷门警报', 'my': {'home': 0.18, 'draw': 0.26, 'away': 0.56}},
    {'slug': 'france_senegal', 'home': 'France', 'away': 'Senegal', 'cn_h': '法国', 'cn_a': '塞内加尔',
     'ko': ko(2026, 6, 16, 19), 'tier': '①临界② · 已追踪', 'my': {'home': 0.58, 'draw': 0.26, 'away': 0.16}},
    {'slug': 'argentina_algeria', 'home': 'Argentina', 'away': 'Algeria', 'cn_h': '阿根廷', 'cn_a': '阿尔及利亚',
     'ko': ko(2026, 6, 17, 1), 'tier': '①悬殊 · ⚡冷门警报', 'my': {'home': 0.62, 'draw': 0.23, 'away': 0.15}},
]
COL = {'home': '#2563eb', 'draw': '#6b7280', 'away': '#d97706'}

CSS = """body{font-family:-apple-system,system-ui,sans-serif;margin:0;background:#f7f7f8;color:#1a1a1a;padding:16px;max-width:480px;margin:0 auto}
h1{font-size:19px;font-weight:600;margin:0 0 2px}a{color:inherit;text-decoration:none}
.sub{color:#666;font-size:13px;margin-bottom:16px}
.row{display:flex;gap:8px;margin-bottom:16px}
.card{flex:1;background:#fff;border-radius:12px;padding:12px 8px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.lbl{font-size:12px;color:#666}.big{font-size:24px;font-weight:600;margin:2px 0}.chg{font-size:12px}
.panel{background:#fff;border-radius:12px;padding:14px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.panel h2{font-size:14px;font-weight:600;margin:0 0 10px}
table{width:100%;border-collapse:collapse;font-size:14px}
td{padding:7px 6px;border-bottom:1px solid #f0f0f0}
th{font-size:12px;color:#888;text-align:left;padding:4px 6px}
.foot{color:#999;font-size:12px;text-align:center;margin-top:18px}
.note{font-size:12px;color:#666;line-height:1.6}
.mcard{display:block;background:#fff;border-radius:12px;padding:13px;margin-bottom:11px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.mtitle{font-size:16px;font-weight:600;margin-bottom:2px}
.mtier{font-size:12px;color:#888;margin-bottom:8px}
.mprob{font-size:13px;color:#444}.mval{font-size:13px;margin-top:6px}
.pill{display:inline-block;padding:2px 8px;border-radius:20px;font-size:12px;margin-right:4px}"""

def fetch():
    url = ("https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
           f"?apiKey={KEY}&regions=eu,uk&markets=h2h,totals&oddsFormat=decimal")
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

def h2h_book(b, home, away):
    mk = next((x for x in b['markets'] if x['key'] == 'h2h'), None)
    if not mk: return None
    o = {}
    for oc in mk['outcomes']:
        if oc['name'] == home: o['home'] = oc['price']
        elif oc['name'] == away: o['away'] = oc['price']
        else: o['draw'] = oc['price']
    return o if len(o) == 3 else None

def tot25_book(b):
    mk = next((x for x in b['markets'] if x['key'] == 'totals'), None)
    if not mk: return None
    o = {}
    for oc in mk['outcomes']:
        if abs(oc.get('point', 0) - 2.5) < 0.01:
            o[oc['name'].lower()] = oc['price']
    return o or None

now = datetime.datetime.now(TZ)
try:
    data = fetch()
except Exception as e:
    data = []; print('fetch error', e)

def find(cfg):
    return next((m for m in data if m['home_team'] == cfg['home'] and m['away_team'] == cfg['away']), None)

def load_rows(slug):
    p = os.path.join(DATA_DIR, slug + '.jsonl')
    rows = [json.loads(l) for l in open(p)] if os.path.exists(p) else []
    for r in rows:
        if 'devig' not in r and 'devig_pin' in r:
            r['devig'] = r['devig_pin']
    return [r for r in rows if r.get('devig')]

def sample(cfg):
    m = find(cfg)
    if not m: return
    books = m['bookmakers']
    pin = next((b for b in books if b['key'] == 'pinnacle'), None)
    pin_h2h = h2h_book(pin, cfg['home'], cfg['away']) if pin else None
    allh = [x for x in (h2h_book(b, cfg['home'], cfg['away']) for b in books) if x]
    soft = {k: round(sum(x[k] for x in allh) / len(allh), 3) for k in ('home', 'draw', 'away')} if allh else None
    src = pin_h2h or soft
    if not src: return
    inv = {k: 1 / src[k] for k in src}; s = sum(inv.values())
    devig = {k: round(inv[k] / s, 4) for k in src}
    rec = {'ts': now.isoformat(timespec='minutes'),
           'hrs_to_ko': round((cfg['ko'] - now).total_seconds() / 3600, 1),
           'pin_h2h': pin_h2h, 'soft_h2h': soft,
           'pin_tot25': tot25_book(pin) if pin else None, 'devig': devig, 'n_books': len(allh)}
    with open(os.path.join(DATA_DIR, cfg['slug'] + '.jsonl'), 'a') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print('sampled', cfg['slug'], rec['hrs_to_ko'], 'h')

def lbl(cfg):
    return {'home': cfg['cn_h'], 'draw': '平局', 'away': cfg['cn_a']}

def sparkline(rows):
    if len(rows) < 2:
        return '<p style="color:#888;font-size:13px">采样 ≥2 档后显示移盘曲线</p>'
    W, H, pad, ymax = 320, 120, 24, 0.90
    n = len(rows)
    def pts(key):
        return ' '.join(f'{pad + i*(W-2*pad)/(n-1):.1f},{H-pad-(r["devig"][key]/ymax)*(H-2*pad):.1f}'
                        for i, r in enumerate(rows))
    lines = ''.join(f'<polyline fill="none" stroke="{COL[k]}" stroke-width="2" points="{pts(k)}"/>'
                    for k in ('home', 'draw', 'away'))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:340px">'
            f'<line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="#ddd"/>{lines}</svg>'
            '<div style="font-size:12px;color:#666;margin-top:4px">左=早 → 右=临场</div>')

def cards(rows, cfg):
    L = lbl(cfg); last = rows[-1]; first = rows[0]; out = ''
    for k in ('home', 'draw', 'away'):
        cur = last['devig'][k] * 100
        dv = (last['devig'][k] - first['devig'][k]) * 100
        arr = '▲' if dv > 0.2 else ('▼' if dv < -0.2 else '–')
        ac = '#16a34a' if dv > 0.2 else ('#dc2626' if dv < -0.2 else '#999')
        out += (f'<div class="card"><div class="lbl">{L[k]}</div>'
                f'<div class="big" style="color:{COL[k]}">{cur:.1f}%</div>'
                f'<div class="chg" style="color:{ac}">{arr} {dv:+.1f}pt</div></div>')
    return out

def evtable(rows, cfg):
    L = lbl(cfg); p = rows[-1].get('pin_h2h')
    if not p: return ''
    out = ''
    for k in ('home', 'draw', 'away'):
        ev = cfg['my'][k] * p[k]
        if ev > 1.03: tag, bg = '✅ 有价值', '#dcfce7'
        elif ev > 0.99: tag, bg = '— 临界', '#fef9c3'
        else: tag, bg = '❌ 别碰', '#fee2e2'
        out += (f'<tr style="background:{bg}"><td>{L[k]}</td><td>{cfg["my"][k]:.0%}</td>'
                f'<td>{p[k]}</td><td>{ev:.2f}</td><td>{tag}</td></tr>')
    return out

def build_detail(cfg, rows):
    L = lbl(cfg)
    title = f'{cfg["cn_h"]} vs {cfg["cn_a"]}'
    if not rows:
        body = '<div class="panel note">暂无数据(比赛可能已开赛或尚未采样)</div>'
        hrs, n, updated, tot = '?', 0, '无', ''
    else:
        last = rows[-1]; hrs = last['hrs_to_ko']; n = len(rows); updated = last['ts']
        t = last.get('pin_tot25') or {}
        tot = f"大小球 2.5 ｜ 大 {t.get('over','-')} · 小 {t.get('under','-')}" if t else ''
        body = (f'<div class="row">{cards(rows, cfg)}</div>'
                f'<div class="panel"><h2>移盘曲线(锐庄去水位概率)</h2>{sparkline(rows)}'
                f'<div style="font-size:12px;color:#666;margin-top:2px">'
                f'<span style="color:#2563eb">{L["home"]}</span> '
                f'<span style="color:#6b7280">平</span> '
                f'<span style="color:#d97706">{L["away"]}</span></div></div>'
                f'<div class="panel"><h2>实时 +EV(我的概率 × 锐庄赔率)</h2>'
                f'<table><tr><th>结果</th><th>我估</th><th>锐庄</th><th>EV</th><th>判定</th></tr>'
                f'{evtable(rows, cfg)}</table>'
                f'<div class="note" style="margin-top:8px">{tot}</div></div>'
                f'<div class="panel note"><b>读法:</b>EV&gt;1 才有价值;看曲线方向——锐庄持续抬热门=实火(撤),不动/下行=价值坐实。临场最后一档最准。</div>')
    html = (f'<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title} · 移盘追踪</title><style>{CSS}</style></head><body>'
            f'<div class="sub"><a href="index.html">← 返回目录</a></div>'
            f'<h1>{title}</h1>'
            f'<div class="sub">{cfg["tier"]} · 距开赛约 <b>{hrs}h</b> · 数据档数 {n} · 更新 {updated} UTC</div>'
            f'{body}<div class="foot">自动每 3h 更新 · 仅供研究,非投注建议</div></body></html>')
    with open(os.path.join(DOCS, cfg['slug'] + '.html'), 'w') as f:
        f.write(html)

def build_index(items):
    mc = ''
    for cfg, rows in items:
        title = f'{cfg["cn_h"]} vs {cfg["cn_a"]}'
        if not rows:
            mc += (f'<a class="mcard" href="{cfg["slug"]}.html"><div class="mtitle">{title}</div>'
                   f'<div class="mtier">{cfg["tier"]} · 暂无数据</div></a>')
            continue
        last = rows[-1]; d = last['devig']; p = last.get('pin_h2h') or {}
        L = lbl(cfg)
        prob = (f'<span style="color:#2563eb">{L["home"]} {d["home"]:.0%}</span> · '
                f'<span style="color:#6b7280">平 {d["draw"]:.0%}</span> · '
                f'<span style="color:#d97706">{L["away"]} {d["away"]:.0%}</span>')
        vals = ''
        for k in ('home', 'draw', 'away'):
            if p and cfg['my'][k] * p[k] > 1.03:
                vals += f'<span class="pill" style="background:#dcfce7">{L[k]} +{(cfg["my"][k]*p[k]-1)*100:.0f}%</span>'
        if not vals: vals = '<span class="pill" style="background:#f0f0f0">暂无明显价值</span>'
        ko_status = f'距开赛 {last["hrs_to_ko"]}h' if last['hrs_to_ko'] > 0 else '已开赛'
        mc += (f'<a class="mcard" href="{cfg["slug"]}.html"><div class="mtitle">{title} ›</div>'
               f'<div class="mtier">{cfg["tier"]} · {ko_status}</div>'
               f'<div class="mprob">{prob}</div><div class="mval">{vals}</div></a>')
    updated = now.isoformat(timespec='minutes')
    html = (f'<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>世界杯赔率追踪</title><style>{CSS}</style></head><body>'
            f'<h1>世界杯赔率价值追踪</h1>'
            f'<div class="sub">{len(items)} 场 · 每 3h 自动更新 · {updated} UTC(北京 +8h)</div>'
            f'{mc}'
            f'<div class="panel note"><b>读法:</b>绿色药丸=我模型算出的 +EV 方向(该下注处);点卡片看移盘曲线。'
            f'⚡冷门警报=强热门首战遇硬骨头。仅供研究,非投注建议。</div>'
            f'<div class="foot">The Odds API · GitHub Actions</div></body></html>')
    with open(os.path.join(DOCS, 'index.html'), 'w') as f:
        f.write(html)

# ---- 主流程 ----
items = []
for cfg in MATCHES:
    sample(cfg)
    rows = load_rows(cfg['slug'])
    build_detail(cfg, rows)
    items.append((cfg, rows))
build_index(items)
print('完成:', len(items), '场;首页 + 各详情页已生成')
