#!/usr/bin/env python3
# 采样 The Odds API + 生成手机版 H5(GitHub Actions 每 3h 调用)
# 依赖:仅 Python 标准库;key 从环境变量 ODDS_API_KEY 读取
import json, os, sys, datetime, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data', 'france_senegal.jsonl')
DOCS = os.path.join(ROOT, 'docs')
os.makedirs(os.path.dirname(DATA), exist_ok=True)
os.makedirs(DOCS, exist_ok=True)

KEY = os.environ.get('ODDS_API_KEY', '').strip()
if not KEY:
    sys.exit('缺少 ODDS_API_KEY 环境变量(本地测试:export ODDS_API_KEY=...)')

# ===== 试点比赛配置 =====
HOME, AWAY = 'France', 'Senegal'
TITLE = '法国 vs 塞内加尔'
KO = datetime.datetime(2026, 6, 16, 19, 0, 0, tzinfo=datetime.timezone.utc)
MY = {'home': 0.58, 'draw': 0.26, 'away': 0.16}   # 我的 v3.0 概率(②档修正)
LBL = {'home': '法国', 'draw': '平局', 'away': '塞内加尔'}
COL = {'home': '#2563eb', 'draw': '#6b7280', 'away': '#d97706'}
# ========================

def fetch():
    url = ("https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
           f"?apiKey={KEY}&regions=eu,uk&markets=h2h,totals&oddsFormat=decimal")
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

def h2h(b):
    mk = next((x for x in b['markets'] if x['key'] == 'h2h'), None)
    if not mk: return None
    o = {}
    for oc in mk['outcomes']:
        if oc['name'] == HOME: o['home'] = oc['price']
        elif oc['name'] == AWAY: o['away'] = oc['price']
        else: o['draw'] = oc['price']
    return o if len(o) == 3 else None

def tot25(b):
    mk = next((x for x in b['markets'] if x['key'] == 'totals'), None)
    if not mk: return None
    o = {}
    for oc in mk['outcomes']:
        if abs(oc.get('point', 0) - 2.5) < 0.01:
            o[oc['name'].lower()] = oc['price']
    return o or None

now = datetime.datetime.now(datetime.timezone.utc)
try:
    data = fetch()
    match = next((m for m in data if m['home_team'] == HOME and m['away_team'] == AWAY), None)
except Exception as e:
    match = None
    print('fetch error:', e)

if match:
    books = match['bookmakers']
    pin = next((b for b in books if b['key'] == 'pinnacle'), None)
    pin_h2h = h2h(pin) if pin else None
    allh = [x for x in (h2h(b) for b in books) if x]
    soft = {k: round(sum(x[k] for x in allh) / len(allh), 3) for k in ('home', 'draw', 'away')} if allh else None
    src = pin_h2h or soft
    if src:
        inv = {k: 1 / src[k] for k in src}; s = sum(inv.values())
        devig = {k: round(inv[k] / s, 4) for k in src}
        rec = {'ts': now.isoformat(timespec='minutes'),
               'hrs_to_ko': round((KO - now).total_seconds() / 3600, 1),
               'pin_h2h': pin_h2h, 'soft_h2h': soft,
               'pin_tot25': tot25(pin) if pin else None,
               'devig': devig, 'n_books': len(allh)}
        with open(DATA, 'a') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print('appended:', rec['ts'], rec['hrs_to_ko'], 'h')
else:
    print('未找到比赛(可能已开赛),仅刷新页面')

# ---------- 生成 H5 ----------
rows = [json.loads(l) for l in open(DATA)] if os.path.exists(DATA) else []
for r in rows:                                  # 兼容旧脚本格式(devig_pin)
    if 'devig' not in r and 'devig_pin' in r:
        r['devig'] = r['devig_pin']
rows = [r for r in rows if r.get('devig')]      # 丢弃无去水位的脏行

def sparkline(rows):
    if len(rows) < 2:
        return '<p style="color:#888;font-size:13px">采样 ≥2 档后显示移盘曲线</p>'
    W, H, pad, ymax = 320, 120, 24, 0.80
    n = len(rows)
    def pts(key):
        out = []
        for i, r in enumerate(rows):
            x = pad + i * (W - 2 * pad) / (n - 1)
            y = H - pad - (r['devig'][key] / ymax) * (H - 2 * pad)
            out.append(f'{x:.1f},{y:.1f}')
        return ' '.join(out)
    lines = ''.join(
        f'<polyline fill="none" stroke="{COL[k]}" stroke-width="2" points="{pts(k)}"/>'
        for k in ('home', 'draw', 'away'))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:340px">'
            f'<line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="#ddd"/>'
            f'{lines}</svg>'
            '<div style="font-size:12px;color:#666;margin-top:4px">'
            '左=早 → 右=临场 · '
            '<span style="color:#2563eb">法国</span> '
            '<span style="color:#6b7280">平</span> '
            '<span style="color:#d97706">塞内加尔</span></div>')

def cards(rows):
    if not rows: return ''
    last = rows[-1]; first = rows[0]
    out = ''
    for k in ('home', 'draw', 'away'):
        cur = last['devig'][k] * 100
        dv = (last['devig'][k] - first['devig'][k]) * 100
        arr = '▲' if dv > 0.2 else ('▼' if dv < -0.2 else '–')
        ac = '#16a34a' if dv > 0.2 else ('#dc2626' if dv < -0.2 else '#999')
        out += (f'<div class="card"><div class="lbl">{LBL[k]}</div>'
                f'<div class="big" style="color:{COL[k]}">{cur:.1f}%</div>'
                f'<div class="chg" style="color:{ac}">{arr} {dv:+.1f}pt</div></div>')
    return out

def evtable(rows):
    if not rows: return ''
    last = rows[-1]; p = last['pin_h2h']
    if not p: return ''
    out = ''
    for k in ('home', 'draw', 'away'):
        ev = MY[k] * p[k]
        if ev > 1.03: tag, bg = '✅ 有价值', '#dcfce7'
        elif ev > 0.99: tag, bg = '— 临界', '#fef9c3'
        else: tag, bg = '❌ 别碰', '#fee2e2'
        out += (f'<tr style="background:{bg}"><td>{LBL[k]}</td>'
                f'<td>{MY[k]:.0%}</td><td>{p[k]}</td><td>{ev:.2f}</td><td>{tag}</td></tr>')
    return out

last = rows[-1] if rows else None
hrs = last['hrs_to_ko'] if last else '?'
tot = (last.get('pin_tot25') or {}) if last else {}
tot_html = (f"大小球 2.5 ｜ 大 {tot.get('over','-')} · 小 {tot.get('under','-')}"
            if tot else '')
updated = last['ts'] if last else '无数据'

TPL = """<!DOCTYPE html><html lang="zh"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · 移盘追踪</title>
<style>
body{font-family:-apple-system,system-ui,sans-serif;margin:0;background:#f7f7f8;color:#1a1a1a;padding:16px;max-width:480px;margin:0 auto}
h1{font-size:19px;font-weight:600;margin:0 0 2px}
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
</style></head><body>
<h1>__TITLE__</h1>
<div class="sub">距开赛约 <b>__HRS__h</b> · 数据档数 __N__ · 更新 __UPDATED__ UTC</div>
<div class="row">__CARDS__</div>
<div class="panel"><h2>移盘曲线(锐庄去水位概率)</h2>__SPARK__</div>
<div class="panel"><h2>实时 +EV(我的概率 × 锐庄赔率)</h2>
<table><tr><th>结果</th><th>我估</th><th>锐庄</th><th>EV</th><th>判定</th></tr>__EV__</table>
<div class="note" style="margin-top:8px">__TOT__</div></div>
<div class="panel note"><b>读法:</b>EV&gt;1 才有价值;重点看曲线方向——若锐庄持续抬法国=实火(撤),若不动/下行=价值坐实。临场最后一档最准。</div>
<div class="foot">自动每 3h 更新 · 仅供研究,非投注建议</div>
</body></html>"""

html = (TPL.replace('__TITLE__', TITLE).replace('__HRS__', str(hrs))
        .replace('__N__', str(len(rows))).replace('__UPDATED__', updated)
        .replace('__CARDS__', cards(rows)).replace('__SPARK__', sparkline(rows))
        .replace('__EV__', evtable(rows)).replace('__TOT__', tot_html))

with open(os.path.join(DOCS, 'index.html'), 'w') as f:
    f.write(html)
print('index.html 已生成,共', len(rows), '档')
