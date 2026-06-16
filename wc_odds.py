#!/usr/bin/env python3
# 多场采样 + 手机 H5(Midnight Quantum 暗色玻璃拟态设计)
import json, os, sys, math, datetime, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'data'); DOCS = os.path.join(ROOT, 'docs')
os.makedirs(DATA_DIR, exist_ok=True); os.makedirs(DOCS, exist_ok=True)
AFKEY = os.environ.get('API_FOOTBALL_KEY', '').strip()
if not AFKEY: sys.exit('缺少 API_FOOTBALL_KEY 环境变量')
KEY = os.environ.get('ODDS_API_KEY', '').strip()  # The Odds API 已弃用,保留仅作可选回退
TZ = datetime.timezone.utc
def ko(y, mo, d, h): return datetime.datetime(y, mo, d, h, 0, 0, tzinfo=TZ)

MATCHES = [
 {'slug': 'spain_capeverde', 'home': 'Spain', 'away': 'Cape Verde Islands', 'cn_h': '西班牙', 'cn_a': '佛得角',
  'ko': ko(2026,6,15,16), 'tier': '①悬殊 · 砍屠杀', 'my': {'home':0.87,'draw':0.09,'away':0.04},
  'st': {'h2h':'双方历史无任何交锋记录——佛得角首次跻身世界杯决赛圈,这是两队首次正式碰面。',
   'fh':'4-3-3','fa':'4-4-2(低位防反)',
   'xh':'2024 欧洲杯冠军班底:亚马尔边路爆点、佩德里组织,技术控球渗透流,板凳深度世界顶级。',
   'xa':'非洲岛国"蓝鲨",球员多旅欧(葡超/葡甲为主),身体强壮、纪律性好,主打密集防守+快速反击,世界杯首秀拼劲足。',
   'mu':['西班牙控球渗透 vs 佛得角密集铁桶:能否撕开低位防线是看点',
         '亚马尔/边路速度 vs 佛得角边后卫:西班牙打开局面的胜负手',
         '佛得角反击速度 vs 西班牙高位防线身后:爆冷唯一火种'],
   'oh':91,'oa':3,'osrc':'去水位','otag':'西班牙一边倒','val':'砍屠杀 / 小球 / 佛得角高让受',
   'note':'①档极悬殊(西91%)。西班牙实力碾压、胜负无悬念;市场赌血洗(大2.5@1.29),价值在反向小球+佛得角高让受。'}},
 {'slug': 'belgium_egypt', 'home': 'Belgium', 'away': 'Egypt', 'cn_h': '比利时', 'cn_a': '埃及',
  'ko': ko(2026,6,15,19), 'tier': '②中热门 · 价值区', 'my': {'home':0.50,'draw':0.27,'away':0.23},
  'st': {'h2h':'4 次友谊赛交锋,埃及胜 2(2022年2-1、2005年4-0),比利时最大胜2018年3-0。埃及交锋不落下风。',
   'fh':'4-2-3-1/4-3-3','fa':'4-2-3-1(保守反击)',
   'xh':'库尔图瓦把门,德布劳内组织,卢卡库锋线;黄金一代但老化',
   'xa':'萨拉赫(刚经历利物浦低迷赛季)+马尔穆什 双快;整体退守(主帅Hossam Hassan)',
   'mu':['德布劳内创造力 vs 埃及密集中场:能否撕开铁桶是胜负手',
         '萨拉赫/马尔穆什速度 vs 比利时老化后防(转身慢):埃及反击最大威胁',
         '卢卡库支点 vs 埃及中卫身体对抗'],
   'oh':37,'oa':36,'osrc':'OPTA','otag':'几乎五五开','val':'平局 / 小球 / 埃及受让',
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
   'oh':12,'oa':66,'osrc':'去水位','otag':'乌强但隐患多','val':'平局 / 沙特受让 / 小球 ⚡',
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
   'oh':65,'oa':13,'osrc':'去水位','otag':'法占优·塞被低估','val':'平局 / 塞内加尔 / 小球',
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
   'oh':69,'oa':10,'osrc':'去水位','otag':'阿大热·防屠杀','val':'砍屠杀 / 小球 ⚡',
   'note':'①档(阿71%)。阿根廷强,但揭幕战警惕(2022曾负沙特);价值在砍屠杀+小球。⚡冷门警报'}},
 {'slug': 'iraq_norway', 'home': 'Iraq', 'away': 'Norway', 'cn_h': '伊拉克', 'cn_a': '挪威',
  'ko': ko(2026,6,16,22), 'tier': '①悬殊 · 反砍屠杀', 'my': {'home':0.08,'draw':0.16,'away':0.76},
  'st': {'h2h':'两队历史正式交锋记录极少,基本无参考价值。',
   'fh':'5-4-1(低位防守反击)','fa':'4-3-3(哈兰德中锋领衔)',
   'xh':'依赖整体阵型压缩空间,锋线威胁有限;世界杯首次遇顶级对手。',
   'xa':'哈兰德(曼城,欧洲金靴常客)+厄德高(阿森纳,10号)+ Sörloth 第二锋线;进攻火力极强。',
   'mu':['哈兰德 vs 伊拉克中卫:高空球+禁区得分能力 → 伊拉克最大威胁',
         '厄德高组织 vs 伊拉克中场压迫:挪威短传渗透节奏',
         '伊拉克反击 vs 挪威高位防线身后:唯一爆冷火种'],
   'oh':7,'oa':80,'osrc':'去水位','otag':'挪威一边倒','val':'反砍屠杀 / 小球(伊拉克密集防守压低总进球)',
   'note':'①档极悬殊(挪80%)。哈兰德火力强,但对阵低级别防守阵营首轮总进球未必爆发;价值在小球≤2。'}},
 {'slug': 'austria_jordan', 'home': 'Austria', 'away': 'Jordan', 'cn_h': '奥地利', 'cn_a': '约旦',
  'ko': ko(2026,6,17,4), 'tier': '①悬殊 · ⚡约旦被低估', 'my': {'home':0.63,'draw':0.23,'away':0.14},
  'st': {'h2h':'两队极少正式交锋,无充分历史数据。',
   'fh':'4-2-3-1(兰格尼克体系,高位压迫)','fa':'4-3-3(反击反压)',
   'xh':'Sabitzer/Laimer/Alaba(伤情待确认)中场强;兰格尼克高位压迫体系风格鲜明。',
   'xa':'约旦2023亚洲杯亚军!主力中场Al-Naimat/Bani Yaseen,半决赛淘汰韩国 → 实力被严重低估。',
   'mu':['奥地利高位压迫 vs 约旦快速转换反击:两强对抗关键点',
         'Sabitzer/Laimer中场强度 vs 约旦防守意志:消耗战走向',
         '约旦定位球威胁 vs 奥地利后防身高短板'],
   'oh':71,'oa':11,'osrc':'去水位','otag':'奥强·约旦黑马','val':'反砍屠杀 / 约旦受让 / 小球',
   'note':'①档(奥71%)。约旦2023亚洲杯亚军,击败韩国等强队,实力明显被市场低估;价值在反屠杀+小球。⚡黑马警报'}},
 {'slug': 'portugal_congodr', 'home': 'Portugal', 'away': 'Congo DR', 'cn_h': '葡萄牙', 'cn_a': '刚果(金)',
  'ko': ko(2026,6,17,17), 'tier': '①悬殊 · 砍屠杀', 'my': {'home':0.72,'draw':0.19,'away':0.09},
  'st': {'h2h':'两队几乎无历史交锋,葡萄牙与非洲球队首轮鲜有压倒性胜利记录。',
   'fh':'4-3-3(B费/B席/鲁本涅维斯+C罗)','fa':'4-3-3(低位防守+快速反击)',
   'xh':'C罗(仍是队长核心)+B费/B席中场组织;葡甲联赛顶级深度;身价欧洲前三。',
   'xa':'刚果(金)旅欧球员为主(法甲/比甲为骨干);身体条件好,速度快;AFCON常客但世界杯经验不足。',
   'mu':['C罗 vs 刚果中卫:禁区内得分能力 → 葡萄牙最大火力',
         'B费/B席创造力 vs 刚果防守组织:能否撕开低位阵型',
         '刚果反击 vs 葡萄牙高位防线:唯一得分机会'],
   'oh':75,'oa':8,'osrc':'去水位','otag':'葡大热·反小球','val':'反砍屠杀 / 小球',
   'note':'①档(葡75%)。葡萄牙攻击力强但刚果(金)防守态度坚定;首轮强队不一定爆发;价值在小球≤2。'}},
 {'slug': 'england_croatia', 'home': 'England', 'away': 'Croatia', 'cn_h': '英格兰', 'cn_a': '克罗地亚',
  'ko': ko(2026,6,17,20), 'tier': '②中热门 · 价值区', 'my': {'home':0.48,'draw':0.28,'away':0.24},
  'st': {'h2h':'2018世界杯半决赛:克罗地亚2-1逆转英格兰(加时);2020欧洲杯小组赛:英格兰1-0。英克历史2:1克胜多。',
   'fh':'4-3-3(贝林厄姆/萨卡/凯恩)','fa':'4-3-2-1(莫德里奇/科瓦契奇/格瓦迪奥尔)',
   'xh':'贝林厄姆(皇马赛季低迷)+ 萨卡(阿森纳稳定)+ 凯恩(拜仁金靴);中场经验相对稚嫩。',
   'xa':'莫德里奇(老将,仍是核心)+科瓦契奇(曼城)+格瓦迪奥尔(曼城左后);老道稳健战术执行力强。',
   'mu':['贝林厄姆创造力 vs 莫德里奇经验:中场掌控权决定比赛走向',
         '萨卡边路 vs 格瓦迪奥尔防守:克罗地亚最强边后对位',
         '凯恩 vs 克罗地亚中卫(洛夫伦/埃尔利奇):英格兰锋线核心'],
   'oh':56,'oa':20,'osrc':'去水位','otag':'英强但高估','val':'平局 / 克罗地亚 / 双重机会@2.10',
   'note':'②档(英56%)价值区。英格兰被情绪高估;克罗地亚战术成熟、交锋史占优 → 双重机会"平或克罗地亚"@2.10有真实价值。'}},
 {'slug': 'ghana_panama', 'home': 'Ghana', 'away': 'Panama', 'cn_h': '加纳', 'cn_a': '巴拿马',
  'ko': ko(2026,6,17,23), 'tier': '③势均 · 轻偏巴拿马', 'my': {'home':0.40,'draw':0.29,'away':0.31},
  'st': {'h2h':'历史交锋极少且非正式赛,无参考价值。',
   'fh':'4-2-3-1(Thomas Partey领衔)','fa':'4-4-2(低位防守反击)',
   'xh':'Thomas Partey(阿森纳)+Kudus(阿贾克斯);中场质量非洲前列;两翼快速。',
   'xa':'首次参加世界杯2018后再度晋级;整体防守纪律性好;Fajardo顶锋;泛美赛事经验丰富。',
   'mu':['Kudus技术 vs 巴拿马密集防守:加纳能否打开局面',
         '巴拿马低位反击 vs 加纳高位后防:唯一得分机会',
         '定位球对抗:两队均有身体优势,争夺激烈'],
   'oh':43,'oa':29,'osrc':'去水位','otag':'势均力敌','val':'平局 / 巴拿马 / 小球',
   'note':'③档势均(加43%/巴29%)。市场对加纳略有偏好但差距不大;巴拿马防守纪律好,赔率略被低估 → 平/巴拿马轻微价值。'}},
 {'slug': 'uzbekistan_colombia', 'home': 'Uzbekistan', 'away': 'Colombia', 'cn_h': '乌兹别克', 'cn_a': '哥伦比亚',
  'ko': ko(2026,6,18,2), 'tier': '①悬殊 · 反砍屠杀', 'my': {'home':0.10,'draw':0.22,'away':0.68},
  'st': {'h2h':'两队从未正式交锋,历史无数据。',
   'fh':'4-4-2(低位防守)','fa':'4-3-3(路易斯-迪亚斯/科塔斯/阿里亚斯)',
   'xh':'乌兹别克斯坦首届世界杯!亚洲区第三轮晋级;整体以防守为主,对抗顶级球队经验为零。',
   'xa':'路易斯-迪亚斯(利物浦,赛季MVP级表现)+ 科塔斯(曼城)+ 詹姆斯-罗德里格斯(复出);攻击质量极高。',
   'mu':['路易斯-迪亚斯速度 vs 乌兹别克左后卫:哥伦比亚最大火力点',
         '乌兹别克紧密防守 vs 哥伦比亚阵地进攻:总进球上限',
         '哥伦比亚定位球 vs 乌兹别克高度短板'],
   'oh':10,'oa':68,'osrc':'去水位','otag':'哥大热·防屠杀','val':'反砍屠杀 / 小球(乌兹别克首届防守态度坚定)',
   'note':'①档(哥68%)。哥伦比亚攻击强悍,但乌兹别克首届世界杯防守求稳,总进球≤2有价值;价值在小球。'}},
]
COL = {'home':'#CCFF00', 'draw':'#8e9379', 'away':'#FF0055'}  # 移盘曲线用色
# 抖音评论区万人竞猜数据 (2026-06-16 采集, ~150条/场)
CROWD_DATA = {
 'spain_capeverde':    {'n':349, 'top':[('0-0',41),('1-1',4),('1-0',2),('3-0',2),('4-0',2)]},
 'iran_newzealand':    {'n':147, 'top':[('2-2',17),('2-0',4),('1-0',3),('3-1',2),('0-0',2),('0-1',2)]},
 'belgium_egypt':      {'n':150, 'top':[('1-1',2),('0-1',2),('2-1',1),('0-2',1),('1-2',1)]},
 'netherlands_japan':  {'n':149, 'top':[('2-2',23),('1-1',6),('2-1',5),('1-2',3),('3-3',2),('3-1',2)]},
 'germany_curacao':    {'n':147, 'top':[('7-1',33),('4-1',7),('2-0',5),('6-1',5),('3-1',4),('4-0',3)]},
 'qatar_switzerland':  {'n':148, 'top':[('1-1',14),('0-1',4),('0-3',3),('0-2',2),('3-0',2),('0-5',1)]},
 'brazil_morocco':     {'n':149, 'top':[('1-1',22),('2-1',4),('1-2',4),('2-2',3),('0-1',3),('0-0',2)]},
 'southkorea_czechia': {'n':148, 'top':[('2-1',19),('1-0',4),('1-1',3),('1-2',2),('2-0',1),('3-1',1)]},
 'mexico_southafrica': {'n':148, 'top':[('2-0',21),('2-1',9),('3-0',5),('1-0',5),('3-1',5),('1-1',3)]},
 'argentina_algeria': {'n':502, 'scored':163, 'top':[('2-2',16),('2-0',14),('1-2',14),('3-1',14),('1-1',13),('0-1',12),('7-0',10),('1-0',9)]},
 'france_senegal':    {'n':505, 'scored':200, 'top':[('2-0',25),('0-1',22),('3-1',21),('1-0',15),('0-0',15),('1-1',13),('3-3',11),('3-0',11)]},
 'iraq_norway':       {'n':500, 'scored':141, 'top':[('2-0',24),('1-5',22),('0-2',22),('0-1',12),('1-1',9),('1-2',8),('0-3',8),('0-0',4)]},
}
# 精确比分赔率(Pinnacle，bet=10)：用于计算大众/庄家价差比
CROWD_SCORE_ODDS = {
 'argentina_algeria': {'2-2':21.0,'2-0':6.0,'1-2':21.0,'3-1':13.0,'1-1':8.5,'0-1':17.0,'7-0':101.0,'1-0':6.0},
 'france_senegal':    {'2-0':7.0,'0-1':15.0,'3-1':11.0,'1-0':7.0,'0-0':13.0,'1-1':8.5,'3-3':34.0,'3-0':10.5},
 'iraq_norway':       {'2-0':41.0,'1-5':26.0,'0-2':6.0,'0-1':7.5,'1-1':13.0,'1-2':10.0,'0-3':6.5,'0-0':17.0},
}
# 万人竞猜回测：6场已结束小组赛，赔率来源 Pinnacle/Bet365
# 西班牙/伊朗已做赛前时间戳过滤；荷兰/巴西 ⚠️ 含赛后评论风险
BACKTEST = [
 {'cn':'墨西哥 vs 南非',   'p1':('2-0',5.40), 'p2':('2-1',8.50),  'actual':'2-0'},
 {'cn':'韩国 vs 捷克',     'p1':('2-1',11.0), 'p2':('1-0',7.50),  'actual':'2-1'},
 {'cn':'巴西 vs 摩洛哥',   'p1':('1-1',6.75), 'p2':('0-0',10.0),  'actual':'1-1', 'warn':1},
 {'cn':'荷兰 vs 日本',     'p1':('2-2',12.5), 'p2':('2-0',9.00),  'actual':'2-2', 'warn':1},
 {'cn':'西班牙 vs 佛得角', 'p1':('4-1',17.0), 'p2':('0-0',29.0),  'actual':'0-0', 'vr':3.2},
 {'cn':'伊朗 vs 新西兰',   'p1':('2-0',7.50), 'p2':('2-1',9.50),  'actual':'2-2'},
]
AFID = {'belgium_egypt':1489377, 'saudi_uruguay':1489379, 'france_senegal':1489383,
        'argentina_algeria':1489381, 'spain_capeverde':1489380,
        'iraq_norway':1539016, 'austria_jordan':1489382, 'portugal_congodr':1539003,
        'england_croatia':1489384, 'ghana_panama':1489385, 'uzbekistan_colombia':1489386}
# API-Football team id(供"最近5场"调用;FIFA排名/身价静态表已弃用,数据不准)
TID = {'Belgium':1, 'Egypt':32, 'Saudi Arabia':23, 'Uruguay':7, 'France':2, 'Senegal':13,
       'Argentina':26, 'Algeria':1532, 'Spain':9, 'Cape Verde Islands':1533,
       'Iraq':1567, 'Norway':1090, 'Austria':775, 'Jordan':1548,
       'Portugal':27, 'Congo DR':1508, 'England':10, 'Croatia':3,
       'Ghana':1504, 'Panama':11, 'Uzbekistan':1568, 'Colombia':8}
# 全量球队表(API 英文名 → 中文名, 国旗 emoji);供未来比赛与过去赛果对账共用
TEAM = {
 'Belgium':('比利时','🇧🇪'), 'Egypt':('埃及','🇪🇬'), 'Saudi Arabia':('沙特','🇸🇦'), 'Uruguay':('乌拉圭','🇺🇾'),
 'France':('法国','🇫🇷'), 'Senegal':('塞内加尔','🇸🇳'), 'Argentina':('阿根廷','🇦🇷'), 'Algeria':('阿尔及利亚','🇩🇿'),
 'Mexico':('墨西哥','🇲🇽'), 'South Africa':('南非','🇿🇦'), 'South Korea':('韩国','🇰🇷'), 'Czechia':('捷克','🇨🇿'),
 'Canada':('加拿大','🇨🇦'), 'Bosnia & Herzegovina':('波黑','🇧🇦'), 'USA':('美国','🇺🇸'), 'Paraguay':('巴拉圭','🇵🇾'),
 'Qatar':('卡塔尔','🇶🇦'), 'Switzerland':('瑞士','🇨🇭'), 'Brazil':('巴西','🇧🇷'), 'Morocco':('摩洛哥','🇲🇦'),
 'Haiti':('海地','🇭🇹'), 'Scotland':('苏格兰','🏴󠁧󠁢󠁳󠁣󠁴󠁿'), 'Australia':('澳大利亚','🇦🇺'), 'Türkiye':('土耳其','🇹🇷'),
 'Germany':('德国','🇩🇪'), 'Curaçao':('库拉索','🇨🇼'), 'Netherlands':('荷兰','🇳🇱'), 'Japan':('日本','🇯🇵'),
 'Ivory Coast':('科特迪瓦','🇨🇮'), 'Ecuador':('厄瓜多尔','🇪🇨'), 'Sweden':('瑞典','🇸🇪'), 'Tunisia':('突尼斯','🇹🇳'),
 'Spain':('西班牙','🇪🇸'), 'Cape Verde Islands':('佛得角','🇨🇻'),
 'Austria':('奥地利','🇦🇹'), 'Jordan':('约旦','🇯🇴'), 'Iraq':('伊拉克','🇮🇶'), 'Norway':('挪威','🇳🇴'),
 'Colombia':('哥伦比亚','🇨🇴'), 'Congo DR':('刚果(金)','🇨🇩'), 'Croatia':('克罗地亚','🇭🇷'),
 'England':('英格兰','🏴󠁧󠁢󠁥󠁮󠁧󠁿'), 'Ghana':('加纳','🇬🇭'), 'Iran':('伊朗','🇮🇷'),
 'New Zealand':('新西兰','🇳🇿'), 'Panama':('巴拿马','🇵🇦'), 'Portugal':('葡萄牙','🇵🇹'), 'Uzbekistan':('乌兹别克斯坦','🇺🇿'),
}
FLAG = {k: v[1] for k, v in TEAM.items()}  # 兼容旧引用
def cn_of(en): return TEAM.get(en, (en, ''))[0]
def flag_of(en): return TEAM.get(en, ('', ''))[1]
def team_badge(team_en, cn):
    fg = FLAG.get(team_en)
    return f'<span class="flag-xl">{fg}</span>' if fg else f'<span class="bigtxt-xl">{cn[0]}</span>'
REASON = {
 'spain_capeverde': [
  ('市场基准 (锐庄去水位)', '西班牙 ≈91% / 平 ≈7% / 佛得角 ≈3%'),
  ('分档:① 极悬殊', '西班牙是夺冠大热、2024 欧洲杯冠军,实力碾压'),
  ('修正① 揭幕效应', '首轮热门常交学费,但西班牙与佛得角差距过大,胜负无悬念'),
  ('修正② 市场过热(大球)', '大 2.5 仅 1.29,市场一边倒赌血洗 → 反向小球出现价值'),
  ('修正③ ①档铁律', '①档只反屠杀、不反胜负 → 不押佛得角赢,只在让球/大小球找价值'),
  ('最终结论', '西班牙稳胜;价值锁定 砍屠杀(佛得角高让受) + 小球')],
 'belgium_egypt': [
  ('市场基准 (锐庄去水位)', '比利时 ≈62% / 平 ≈24% / 埃及 ≈16%'),
  ('分档:② 中热门', '比利时是黄金一代大牌,正是大众情绪最易高估的格口'),
  ('修正① 揭幕效应', '世界杯首轮热门常熄火(本届巴西/瑞士已验证)→ 热门胜率打折'),
  ('修正② 阵容相克', '比利时后防老化、转身慢;埃及有萨拉赫+马尔穆什速度反击 → 埃及上调'),
  ('修正③ 交锋史', '埃及 4 次交锋胜 2,不怵比利时 → 平/埃及再上调'),
  ('最终结论', '比利时 62%→50%、平 24%→27%、埃及 16%→23% → 价值锁定 平 / 埃及 / 小球')],
 'saudi_uruguay': [
  ('市场基准 (锐庄去水位)', '乌拉圭 ≈66% / 平 ≈22% / 沙特 ≈12%'),
  ('分档:① 悬殊', '乌66% 但带揭幕+冷门基因 → 按②的逆向思路处理'),
  ('修正① 揭幕效应', '强热门首战遇硬骨头,易被拖入苦战'),
  ('修正② 阵容', '乌拉圭后防伤兵多(Giménez/Araújo/Cáceres 存疑)→ 失球风险升,乌下调'),
  ('修正③ 冷门基因', '沙特 2022 掀翻阿根廷,Al-Dawsari 反击犀利 → 沙特/平上调'),
  ('最终结论', '乌 66%→56%、平 22%→26%、沙 12%→18% → 价值锁定 平 / 沙特受让 / 小球 ⚡')],
 'france_senegal': [
  ('市场基准 (锐庄去水位)', '法国 ≈65% / 平 ≈21% / 塞内加尔 ≈13%'),
  ('分档:① 临界 ②', '球星光环(姆巴佩)易被高估'),
  ('修正① 揭幕效应', '法国揭幕翻车史(2002 正是负塞内加尔出局)'),
  ('修正② 阵容', '塞内加尔高大强壮+反击快(Jackson/Ndiaye),实力被低估'),
  ('修正③ 交锋史', '塞内加尔历史交锋占优(前 3 次胜 2)'),
  ('最终结论', '法 65%→58%、平 21%→26%、塞 13%→16% → 价值锁定 平 / 塞内加尔 / 小球')],
 'argentina_algeria': [
  ('市场基准 (锐庄去水位)', '阿根廷 ≈69% / 平 ≈21% / 阿尔及利亚 ≈10%'),
  ('分档:① 悬殊', '阿根廷卫冕冠军+近 5 场全胜状态火热'),
  ('修正① 揭幕效应', '阿根廷 2022 揭幕战曾爆冷负沙特 → 胜率略打折'),
  ('修正② 阵容', '阿尔及利亚有 Mahrez/Amoura/Gouiri 反击质量,但整体差距大'),
  ('修正③ 实力差距', '差距真实 → 不过度逆向(①档热门基本会赢)'),
  ('最终结论', '阿 69%→62%、平 21%→23%、阿尔 10%→15% → 价值锁定 砍屠杀 + 小球 ⚡')],
 'iraq_norway': [
  ('市场基准 (锐庄去水位)', '挪威 ≈80% / 平 ≈13% / 伊拉克 ≈7%'),
  ('分档:① 极悬殊', '哈兰德领衔挪威,实力差距明显'),
  ('修正① 哈兰德因素', '欧洲金靴+进球机器,伊拉克门将压力极大 → 胜负无悬念'),
  ('修正② 总进球评估', '伊拉克密集防守策略 → 压缩空间,挪威未必能打多球;大2.5不确定'),
  ('修正③ ①档铁律', '①档只反屠杀不反胜负 → 不押伊拉克赢,押小球≤2更安全'),
  ('最终结论', '挪 80%→76%、平 13%→16%、伊 7%→8% → 价值锁定 小球 ≤2 / 伊拉克高让受')],
 'austria_jordan': [
  ('市场基准 (锐庄去水位)', '奥地利 ≈71% / 平 ≈18% / 约旦 ≈11%'),
  ('分档:① 悬殊', '奥地利欧洲强队,兰格尼克执教高位压迫'),
  ('修正① 约旦实力', '约旦2023亚洲杯亚军!半决赛淘汰韩国 → 市场严重低估约旦上限'),
  ('修正② 交锋史', '两队极少交锋,奥地利未必占优;亚洲杯证明约旦能对抗高水准'),
  ('修正③ 首轮效应', '大热门首轮教学费:约旦防守纪律+反击能力有一定爆冷概率'),
  ('最终结论', '奥 71%→63%、平 18%→23%、约 11%→14% → 价值锁定 反屠杀 / 约旦受让 / 小球 ⚡')],
 'portugal_congodr': [
  ('市场基准 (锐庄去水位)', '葡萄牙 ≈75% / 平 ≈17% / 刚果(金) ≈8%'),
  ('分档:① 悬殊', '葡萄牙 C罗+B费+B席,攻击火力欧洲顶级'),
  ('修正① 刚果防守', '刚果(金)旅欧球员为骨干,防守组织有一定韧性;非洲大赛常客'),
  ('修正② 总进球上限', '首轮强队压制型战术:葡萄牙未必会血洗,5球+不现实'),
  ('修正③ ①档铁律', '①档只反屠杀 → 不押刚果赢,押小球≤2/刚果高让受'),
  ('最终结论', '葡 75%→72%、平 17%→19%、刚 8%→9% → 价值锁定 小球 ≤2 / 刚果高让受')],
 'england_croatia': [
  ('市场基准 (锐庄去水位)', '英格兰 ≈56% / 平 ≈25% / 克罗地亚 ≈20%'),
  ('分档:② 中热门', '英格兰情绪热门,历届赛事被高估是惯例'),
  ('修正① 交锋史', '2018世界杯半决赛:克罗地亚2-1逆转英格兰 → 交锋史克略占优'),
  ('修正② 阵容对比', '莫德里奇经验+格瓦迪奥尔防守 vs 贝林厄姆状态起伏 → 克罗地亚战术成熟'),
  ('修正③ 情绪修正', '英格兰舆论永远高估 → 市场过热,实际胜率应下调'),
  ('最终结论', '英 56%→48%、平 25%→28%、克 20%→24% → 价值锁定 双重机会"平或克罗地亚"@2.10 ⭐')],
 'ghana_panama': [
  ('市场基准 (锐庄去水位)', '加纳 ≈43% / 平 ≈28% / 巴拿马 ≈29%'),
  ('分档:③ 势均', '三强局面,很难找到明确价值方向'),
  ('修正① 巴拿马防守', '巴拿马历史上防守纪律强,能打硬仗;2018世界杯首次亮相表现稳'),
  ('修正② 加纳进攻', 'Thomas Partey+Kudus是真实威胁,但加纳整体依赖个人发挥'),
  ('修正③ 势均价值', '③档轻微偏巴拿马受让:29%被低估一点点 → 偏小球/平或巴拿马'),
  ('最终结论', '加 43%→40%、平 28%→29%、巴 29%→31% → 价值锁定 小球 / 平或巴拿马 (轻微偏向)')],
 'uzbekistan_colombia': [
  ('市场基准 (锐庄去水位)', '哥伦比亚 ≈70% / 平 ≈20% / 乌兹别克 ≈10%'),
  ('分档:① 悬殊', '哥伦比亚有路易斯-迪亚斯(利物浦MVP)+詹姆斯-罗德里格斯,攻击力强'),
  ('修正① 乌兹别克首届', '首次参加世界杯,心态保守防守优先;亚洲区防守数据不俗'),
  ('修正② 总进球预期', '乌兹别克低位防守 → 压低空间,哥伦比亚未必打穿'),
  ('修正③ ①档铁律', '①档只反屠杀 → 押小球而非乌兹别克赢'),
  ('最终结论', '哥 70%→68%、平 20%→22%、乌 10%→10% → 价值锁定 小球 ≤2 / 乌兹别克高让受')],
}

CSS = """*{box-sizing:border-box}
:root{--navy:#020617;--bg:#051424;--low:#0d1c2d;--surf:#122131;--high:#1c2b3c;--on:#d4e4fa;--sec:#bec6e0;--lime:#CCFF00;--crim:#FF0055;--line:rgba(255,255,255,.1)}
body{margin:0 auto;max-width:520px;background:var(--bg);color:var(--on);font-family:Inter,system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased;padding:12px 16px 24px}
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
.mcard{display:block;position:relative;background:linear-gradient(145deg,rgba(20,35,52,.85),rgba(9,21,36,.72));border:1px solid var(--line);border-left:3px solid var(--line);backdrop-filter:blur(10px);border-radius:10px;padding:15px 16px;margin-bottom:14px;box-shadow:0 6px 20px rgba(0,0,0,.28);transition:transform .15s ease,box-shadow .15s ease}
.mcard:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(0,0,0,.36)}
.mtop{display:flex;align-items:center;justify-content:space-between;gap:8px}
.mtitle{font-size:20px;font-weight:700;letter-spacing:-.01em;display:flex;align-items:center;gap:5px}
.mvs{color:var(--sec);opacity:.5;font-weight:600;margin:0 1px}
.chev{color:var(--sec);opacity:.5;font-size:20px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:9px}
.chip{font-family:'JetBrains Mono',monospace;font-size:10px;padding:2px 6px;border-radius:3px;border:1px solid rgba(190,198,224,.2);color:var(--sec);letter-spacing:.03em}
.chip.val{border-color:rgba(204,255,0,.4);color:var(--lime);background:rgba(204,255,0,.06)}
.chip.warn{border-color:rgba(255,0,85,.45);color:var(--crim);background:rgba(255,0,85,.06)}
.chip.dim{border:none;color:rgba(190,198,224,.55)}
.probrow{display:flex;gap:10px;margin:13px 0 9px}
.probrow>div{flex:1}
.pn{font-size:12px;opacity:.85}
.pv{font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:700;margin-left:2px}
.fav{color:var(--lime)}
.dimv{color:var(--sec);opacity:.65}
.minibar{display:flex;gap:3px;height:6px;border-radius:3px;overflow:hidden;margin-bottom:1px}
.minibar i{display:block;border-radius:2px}
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
.foot{text-align:center;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.5;margin:16px 0 4px}
.sech{display:flex;align-items:center;gap:8px;margin:0 0 14px}
.sech-ic{width:30px;height:30px;border-radius:7px;background:rgba(204,255,0,.12);color:var(--lime);display:flex;align-items:center;justify-content:center;flex:0 0 30px}
.sech-ic .material-symbols-outlined{font-size:18px}
.sech-t{font-size:17px;font-weight:800;letter-spacing:-.01em}
.sech-sub{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.6}
.vshead{position:relative}
.hotpick{position:absolute;top:0;right:0;display:flex;align-items:center;gap:3px;background:var(--lime);color:var(--navy);font-weight:800;font-size:12px;padding:4px 10px;border-radius:6px;box-shadow:0 0 14px rgba(204,255,0,.4)}
.vsrow{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin:6px 0 2px}
.vsteam{display:flex;flex-direction:column;align-items:center;gap:6px;width:84px}
.shield{width:54px;height:54px;border-radius:14px;background:var(--high);display:flex;align-items:center;justify-content:center}
.shield .material-symbols-outlined{font-size:28px;color:#c9b97a}
.shield .flag{font-size:38px;line-height:1}
.shield .bigtxt{font-size:24px;font-weight:800;color:var(--on)}
.flag-xl{font-size:60px;line-height:1}
.bigtxt-xl{font-size:38px;font-weight:800;color:var(--on)}
.lockbox{position:relative;border-radius:8px;overflow:hidden;margin-top:4px}
.lockbox .locked{filter:blur(9px);pointer-events:none;user-select:none;transition:filter .3s}
.lockbox.open .locked{filter:none;pointer-events:auto}
.lockmask{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;background:rgba(5,20,36,.55);text-align:center;padding:16px}
.lockbox.open .lockmask{display:none}
.lockmask .material-symbols-outlined{font-size:30px}
.lockicon{color:var(--lime)}
.lockttl{font-size:13px;color:var(--on);font-weight:600}
.lockrow{display:flex;gap:8px}
.lockinput{width:140px;background:rgba(0,0,0,.3);border:1px solid var(--line);border-radius:7px;padding:8px 12px;color:var(--on);font-family:'JetBrains Mono',monospace;font-size:15px;text-align:center;letter-spacing:.18em;outline:none}
.lockinput:focus{border-color:var(--lime)}
.lockbtn{background:var(--lime);color:var(--navy);font-weight:800;font-size:14px;border:none;border-radius:7px;padding:8px 16px;cursor:pointer}
.lockhint{font-size:11px;color:var(--crim);min-height:14px}
.tn{font-size:13px;color:var(--on);font-weight:500;text-align:center}
.vsmid{flex:1;text-align:center;padding-top:6px}
.kol{font-size:11px;color:var(--sec);opacity:.7}
.kot{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:500;margin:2px 0 8px}
.kot small{font-size:13px;color:var(--sec);opacity:.7}
.tierpill{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--lime);border:1px solid rgba(204,255,0,.4);background:rgba(204,255,0,.08);border-radius:999px;padding:3px 12px}
.prob3{display:flex;gap:8px;margin-top:14px}
.ph{flex:1;text-align:center}
.ph-lbl{font-size:11px;color:var(--sec);opacity:.7}
.ph-big{font-size:22px;font-weight:800;letter-spacing:-.03em;margin:2px 0}
.ph-chg{font-size:11px}
.pbar{display:flex;height:6px;overflow:hidden;margin-top:14px;gap:3px}
.pbar>div{border-radius:2px}
.evhead{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.evhead .l{display:flex;align-items:center;gap:7px;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:.04em;color:var(--lime)}
.evhead .dot{width:8px;height:8px;border-radius:50%;background:var(--lime);box-shadow:0 0 8px var(--lime)}
.evhead .r{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.6}
.evc{display:flex;align-items:center;gap:12px;background:rgba(13,28,45,.5);border:1px solid var(--line);border-radius:8px;padding:13px;margin-bottom:10px}
.evc.val{border-color:var(--lime);box-shadow:0 0 14px rgba(204,255,0,.16)}
.evc.bad{opacity:.55}
.evbar{width:4px;align-self:stretch;border-radius:2px;background:var(--sec)}
.evc.val .evbar{background:var(--lime)}
.evc.bad .evbar{background:#475569}
.evmain{flex:1}
.evteam{font-size:18px;font-weight:700}
.evstat{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec);opacity:.85;margin-top:3px}
.evright{text-align:right;flex:0 0 auto}
.evev{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec);margin-bottom:5px}
.evc.val .evev{color:var(--lime);font-weight:700}
.evtag{display:inline-flex;align-items:center;gap:3px;font-size:12px;font-weight:700;padding:5px 12px;border-radius:999px;border:1px solid var(--line);color:var(--sec)}
.evc.val .evtag{background:var(--lime);color:var(--navy);border-color:var(--lime)}
.tl-item{display:flex;gap:12px;padding-bottom:18px;position:relative}
.tl-item:not(:last-child)::before{content:'';position:absolute;left:17px;top:38px;bottom:0;width:2px;background:rgba(204,255,0,.22)}
.tl-icon{width:36px;height:36px;flex:0 0 36px;border-radius:8px;background:var(--high);display:flex;align-items:center;justify-content:center;color:var(--sec);z-index:1}
.tl-icon .material-symbols-outlined{font-size:19px}
.tl-item.final .tl-icon{background:var(--lime);color:var(--navy);box-shadow:0 0 16px rgba(204,255,0,.5)}
.tl-t{font-weight:700;font-size:15px;margin-bottom:3px}
.tl-item.final .tl-t{color:var(--lime)}
.tl-d{font-size:13px;color:var(--sec);opacity:.85;line-height:1.6}
.scg{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.scg-cell{background:rgba(13,28,45,.5);border:1px solid var(--line);border-radius:8px;padding:14px 6px;text-align:center}
.scg-cell.hot{border-color:var(--lime);box-shadow:0 0 14px rgba(204,255,0,.2)}
.scg-s{font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;letter-spacing:.05em;color:var(--on)}
.scg-cell.hot .scg-s{color:var(--lime)}
.scg-p{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--sec);opacity:.85;margin-top:5px}
.xg{display:flex;align-items:center;gap:10px;background:rgba(13,28,45,.5);border:1px solid var(--line);border-radius:8px;padding:12px;margin-top:12px}
.xg-badge{background:var(--lime);color:var(--navy);font-weight:800;font-size:12px;padding:3px 8px;border-radius:5px}
.xg-l{font-size:13px;color:var(--on)}
.xg-v{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--sec)}
table.so thead tr,table.so tr:first-child{background:rgba(255,255,255,.03)}
table.so tr.val td{background:rgba(204,255,0,.1)}
table.so tr.val td.s,table.so tr.val td.e{color:var(--lime);font-weight:700}
.muah{display:flex;align-items:center;gap:8px;margin:0 0 10px}
.muah .material-symbols-outlined{font-size:20px;color:var(--lime)}
.muah-t{font-size:16px;font-weight:800;letter-spacing:-.01em;color:var(--on)}
.mua-h2h{background:rgba(13,28,45,.7);border:1.5px solid rgba(204,255,0,.55);border-radius:12px;padding:16px;margin-bottom:14px;box-shadow:0 0 18px rgba(204,255,0,.18)}
.mua-h2h p{margin:0;font-size:13px;color:var(--sec);line-height:1.7}
.mua-forms{display:flex;gap:10px;margin-bottom:14px}
.mua-fc{flex:1;border-radius:12px;padding:14px;border:1.5px solid}
.mua-fc.home{border-color:rgba(204,255,0,.4);background:rgba(204,255,0,.06)}
.mua-fc.away{border-color:rgba(255,0,85,.4);background:rgba(255,0,85,.06)}
.mua-fc h4{margin:0 0 8px;font-size:15px;font-weight:800;letter-spacing:-.01em}
.mua-fc.home h4{color:var(--lime)}
.mua-fc.away h4{color:var(--crim)}
.mua-fc p{margin:0;font-size:12.5px;color:var(--sec);line-height:1.65}
.mua-div{height:1px;background:rgba(255,255,255,.08);margin:12px 0}
.mua-mu{list-style:none;margin:0;padding:0}
.mua-mu li{display:flex;align-items:flex-start;gap:8px;font-size:13px;color:var(--on);line-height:1.6;margin:9px 0}
.mudot{flex:0 0 6px;width:6px;height:6px;border-radius:50%;background:var(--lime);margin-top:7px}
.muvs{color:var(--lime);font-weight:700;font-style:normal}
.opta-row{display:flex;align-items:center;gap:10px}
.opta-pill{background:var(--lime);color:var(--navy);font-weight:800;font-size:12px;letter-spacing:.05em;padding:3px 10px;border-radius:6px;flex:0 0 auto}
.opta-txt{font-size:14px;color:var(--on);font-weight:600}
.opta-tag{color:var(--sec);font-weight:500;margin-left:4px}
.opta-bar{display:flex;gap:3px;height:8px;margin:12px 0 10px}
.opta-bar i{display:block;border-radius:999px}
.opta-val{font-style:italic;font-size:12.5px;color:var(--sec)}
.sec-h{display:flex;align-items:baseline;gap:8px;margin:24px 2px 12px}
.sec-h .t{font-size:15px;font-weight:800;color:var(--on);letter-spacing:-.01em}
.sec-h .c{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.7}
.track{background:linear-gradient(135deg,rgba(204,255,0,.12),rgba(13,28,45,.7));border:1px solid rgba(204,255,0,.32);border-radius:12px;padding:14px 16px;margin-bottom:6px;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.track-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.track-l{display:flex;align-items:center;gap:7px;font-size:14px;font-weight:800;color:var(--on)}
.track-l .material-symbols-outlined{color:var(--lime);font-size:20px}
.track-r{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec);white-space:nowrap}
.track-r b{color:var(--lime);font-size:18px}
.track-bar{height:6px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden;margin:10px 0 8px}
.track-bar i{display:block;height:100%;background:var(--lime);border-radius:3px}
.track-note{font-size:11px;color:var(--sec);opacity:.7;font-style:italic;line-height:1.5}
.pnl{font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:800;margin:8px 0 4px;display:flex;align-items:baseline;gap:8px}
.pnl.pos{color:var(--lime)} .pnl.neg{color:var(--crim)}
.pnl small{font-size:12px;font-weight:500;color:var(--sec);opacity:.8}
.pnl-row{display:flex;flex-wrap:wrap;gap:4px 14px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec);margin-bottom:8px}
.tkwrap{margin-bottom:8px}
.tk{border:1px solid var(--line);border-left:3px solid var(--line);border-radius:10px;padding:13px 14px;margin-bottom:10px;background:rgba(13,28,45,.5)}
.tk.green{border-left-color:#3ddc84} .tk.amber{border-left-color:#ffcc33} .tk.red{border-left-color:var(--crim)}
.tk-top{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:10px;flex-wrap:wrap}
.tk-tag{font-size:14px;font-weight:800;color:var(--on)}
.tk-stake{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec)}
.tk-stake b{color:var(--lime);font-size:14px}
.tk-leg{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:7px 0;border-top:1px solid rgba(255,255,255,.05);font-size:13px}
.tk-vs{color:var(--on)}
.tk-bet{flex:0 0 auto;font-family:'JetBrains Mono',monospace;color:var(--sec);white-space:nowrap}
.tk-bet b{color:var(--lime)}
.tk-foot{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.75;margin-top:9px}
.tk-warn{font-size:11px;color:var(--sec);opacity:.6;line-height:1.5;margin-top:4px}
.fxday{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--lime);opacity:.85;margin:16px 2px 8px;font-weight:700}
.fxrow{display:flex;align-items:center;gap:12px;padding:10px 12px;background:rgba(13,28,45,.4);border:1px solid var(--line);border-radius:8px;margin-bottom:6px}
.fx-tm{flex:0 0 auto;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--sec)}
.fx-tt{flex:1;font-size:14px;color:var(--on)}
.fx-vs{color:var(--sec);opacity:.5;font-size:12px;margin:0 4px}
.mtime{display:flex;align-items:center;gap:6px;margin-top:9px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec)}
.mtime .material-symbols-outlined{font-size:14px;opacity:.7}
.filt{position:sticky;top:0;z-index:40;display:flex;gap:8px;padding:10px 0;background:var(--bg)}
.filt a{flex:1;text-align:center;font-size:13px;font-weight:700;color:var(--sec);background:rgba(13,28,45,.8);border:1px solid var(--line);border-radius:8px;padding:9px 0}
.round-head{scroll-margin-top:112px;display:flex;align-items:center;gap:7px;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:800;color:var(--lime);margin:20px 2px 10px}
.round-head .material-symbols-outlined{font-size:17px}
.tl-day{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.65;margin:14px 2px 6px}
.tl-row{display:flex;align-items:center;gap:10px;padding:11px 12px;background:rgba(13,28,45,.45);border:1px solid var(--line);border-radius:8px;margin-bottom:6px}
.tl-row.done{opacity:.82}
.tl-tm{flex:0 0 42px;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--sec)}
.tl-tt{flex:1;font-size:14px;color:var(--on)}
.tl-sc{font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--on);margin:0 5px}
.tl-vs{color:var(--sec);opacity:.5;font-size:12px;margin:0 4px}
.tl-pl{flex:0 0 auto;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:800}
.tl-pl.pos{color:var(--lime)} .tl-pl.neg{color:var(--crim)}
.tl-go{flex:0 0 auto;color:var(--lime);font-size:12px;font-weight:600;white-space:nowrap}
.tl-live{flex:0 0 auto;color:var(--crim);font-size:11px;font-weight:700}
.tl-row.cur{border-color:rgba(204,255,0,.55);box-shadow:0 0 14px rgba(204,255,0,.18)}
.fxbig{display:block;background:linear-gradient(150deg,rgba(20,35,52,.82),rgba(9,21,36,.72));border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:10px;box-shadow:0 4px 16px rgba(0,0,0,.22);transition:transform .15s,box-shadow .15s}
a.fxbig.star{border-color:rgba(204,255,0,.35)}
a.fxbig:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.34)}
.fxbig.cur{border-color:rgba(204,255,0,.6);box-shadow:0 0 18px rgba(204,255,0,.2)}
.fxbig-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.fxbig-tm{display:flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--sec)}
.fxbig-tm .material-symbols-outlined{font-size:14px;opacity:.7}
.fxbig-tag{font-size:11px;font-weight:700;color:var(--lime);background:rgba(204,255,0,.1);border:1px solid rgba(204,255,0,.3);border-radius:5px;padding:2px 8px}
.fxbig-vs{display:flex;align-items:center;justify-content:center;gap:14px;margin-bottom:16px}
.fxbig-team{flex:1;font-size:18px;font-weight:700;color:var(--on);text-align:center;letter-spacing:-.01em}
.fxbig-mid{flex:0 0 auto;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--sec);opacity:.5}
.fxbig-ph{display:flex;align-items:center;justify-content:center;gap:7px;height:40px;background:rgba(255,255,255,.03);border:1px dashed rgba(255,255,255,.13);border-radius:8px;font-size:12px;color:var(--sec);opacity:.65}
.fxbig-ph .material-symbols-outlined{font-size:15px}
.fxbig-cta{display:flex;align-items:center;justify-content:center;gap:6px;height:40px;background:rgba(204,255,0,.1);border:1px solid rgba(204,255,0,.3);border-radius:8px;font-size:13px;font-weight:700;color:var(--lime)}
.fxbig-cta .material-symbols-outlined{font-size:16px}
.track-grid{display:flex;gap:8px;margin:12px 0 10px}
.tg{flex:1;text-align:center;background:rgba(0,0,0,.18);border-radius:8px;padding:10px 4px}
.tg-v{font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:800;color:var(--lime)}
.tg-l{font-size:11px;color:var(--on);margin-top:3px}
.tg-n{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--sec);opacity:.6;margin-top:2px}
.pcard{display:block;background:rgba(13,28,45,.55);border:1px solid var(--line);border-left:3px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:10px;transition:background .15s}
.pcard:hover{background:rgba(20,38,58,.7)}
.pmore{margin-left:auto;font-size:11px;color:var(--lime);font-weight:600;white-space:nowrap}
.pd-flags{font-size:38px;line-height:1.1}
.pd-sc{font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:800;color:var(--on);margin:0 10px;vertical-align:middle}
.pd-tn{font-size:15px;color:var(--sec);margin-top:6px}
.pd-meta{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--sec);opacity:.7;margin-top:6px}
.pva{display:flex;align-items:center;justify-content:space-around;gap:8px;margin-bottom:12px}
.pva-col{flex:1;text-align:center}
.pva-lbl{font-size:11px;color:var(--sec);opacity:.7;margin-bottom:6px}
.pva-sc{font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:800;color:var(--on);letter-spacing:.02em}
.pva-sc.lime{color:var(--lime)}
.pva-sub{font-size:10px;color:var(--sec);opacity:.6;margin-top:4px}
.pva-vs{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--sec);opacity:.5;flex:0 0 auto}
.pva-note{font-size:12px;color:var(--sec);line-height:1.6;border-top:1px solid rgba(255,255,255,.06);padding-top:10px}
.pva-note b{color:var(--lime)}
.rec-row{display:flex;align-items:center;gap:10px;margin:9px 0}
.rec-lbl{font-size:12px;color:var(--sec);flex:0 0 64px}
.rec-wdl{font-size:16px;font-weight:800;color:var(--lime)}
.rec-scs{display:flex;gap:8px}
.rec-sc{font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:700;color:var(--on);background:rgba(204,255,0,.1);border:1px solid rgba(204,255,0,.3);border-radius:7px;padding:4px 12px}
.rectab{width:100%;border-collapse:collapse}
.rectab td{padding:10px 6px;border-bottom:1px solid rgba(255,255,255,.06)}
.rt-l{font-size:12px;color:var(--sec);width:72px}
.rt-m{font-size:14px;color:var(--on)}
.rt-r{text-align:right;font-weight:800;font-size:15px;width:30px}
.rt-r.ok{color:var(--lime)}
.rt-r.no{color:var(--crim)}
.bet{display:flex;align-items:center;gap:10px;padding:11px 2px;border-bottom:1px solid rgba(255,255,255,.06)}
.bet-tag{flex:0 0 auto;font-size:10px;font-family:'JetBrains Mono',monospace;color:var(--sec);border:1px solid var(--line);border-radius:4px;padding:2px 6px}
.bet.main .bet-tag{background:var(--lime);color:var(--navy);border-color:var(--lime);font-weight:700}
.bet-mid{flex:1;min-width:0}
.bet-mid b{font-size:15px;color:var(--on);font-weight:700}
.bet-od{display:block;font-size:11px;color:var(--sec);font-family:'JetBrains Mono',monospace;margin-top:2px}
.bet-amt{flex:0 0 auto;text-align:right;font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:800;color:var(--lime)}
.bet-amt small{display:block;font-size:10px;color:var(--sec);font-weight:400;margin-top:2px}
.plan-sum{font-size:12px;color:var(--sec);line-height:1.65;margin-top:12px}
.plan-sum b{color:var(--lime)}
.pva-hits{display:flex;gap:6px;justify-content:center;margin-bottom:12px}
.ph3{font-size:11px;padding:4px 9px;border-radius:999px;font-weight:700;background:rgba(255,255,255,.06);color:var(--sec)}
.ph3.y{background:rgba(204,255,0,.15);color:var(--lime)}
.ptop{display:flex;align-items:center;justify-content:space-between;gap:8px}
.pteams{font-size:15px;font-weight:600;color:var(--on)}
.psc{font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;margin:0 6px;letter-spacing:.02em}
.pres{flex:0 0 auto;font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px}
.pres.ok{color:var(--navy);background:var(--lime)}
.pres.no{color:var(--sec);background:rgba(255,255,255,.08)}
.pmeta{display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin-top:8px}
.pchip{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--sec);border:1px solid rgba(190,198,224,.2);border-radius:3px;padding:1px 6px}
.pval{font-size:12px;color:var(--sec)}
.pval b{color:var(--lime);font-weight:600}
.vstat{width:100%;border-collapse:collapse;margin-bottom:14px}
.vstat td{padding:10px 6px;border-bottom:1px solid rgba(255,255,255,.06)}
.vstat .vh,.vstat .va{font-family:'JetBrains Mono',monospace;font-size:15px;color:var(--sec);width:34%}
.vstat .vh{text-align:left}
.vstat .va{text-align:right}
.vstat .vc{text-align:center;font-size:11px;color:var(--sec);opacity:.6;font-family:'JetBrains Mono',monospace}
.vstat .vstrong{color:var(--lime);font-weight:700}
.form-blk{display:flex;flex-direction:column;gap:9px}
.form-row{display:flex;align-items:center;gap:10px}
.form-team{font-size:13px;color:var(--on);flex:0 0 72px}
.form-dots{display:flex;gap:5px}
.fdot{width:22px;height:22px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:var(--navy);font-family:'JetBrains Mono',monospace}
.fdmin{font-size:12px;color:var(--sec);opacity:.6}
.vs-note{font-size:11px;color:var(--sec);opacity:.6;margin-top:10px;font-style:italic;line-height:1.5}
.tp-pct{display:flex;justify-content:space-between;font-size:14px;font-weight:700;margin-bottom:8px}
.tp-bar{display:flex;gap:3px;height:8px;margin-bottom:14px}
.tp-bar i{display:block;border-radius:2px}
.tp-adv{display:flex;align-items:center;gap:8px;background:rgba(204,255,0,.08);border:1px solid rgba(204,255,0,.25);border-radius:8px;padding:10px 12px;font-size:13px;color:var(--on);margin-bottom:14px}
.tp-adv .material-symbols-outlined{color:var(--lime);font-size:18px}
.cmp-blk{display:flex;flex-direction:column;gap:9px}
.cmp-row{display:flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-size:12px}
.cmp-l,.cmp-r{flex:0 0 28px;color:var(--sec)}
.cmp-l{text-align:right;color:var(--lime)}
.cmp-r{text-align:left;color:var(--crim)}
.cmp-bar{flex:1;height:6px;background:rgba(255,0,85,.35);border-radius:3px;overflow:hidden}
.cmp-bar i{display:block;height:100%;background:var(--lime);border-radius:3px}
.cmp-c{flex:0 0 56px;color:var(--sec);opacity:.7;font-size:11px}"""

# ---------- API-Football 赔率源(单次 /odds 调用拿全 14 家书商×所有盘口)----------
PIN = 4  # Pinnacle(锐庄)bookmaker id
def af_get(url):  # 带重试的 API-Football GET(网络抖动时最多重试 3 次)
    for k in range(3):
        try:
            req = urllib.request.Request(url, headers={'x-apisports-key': AFKEY})
            return json.load(urllib.request.urlopen(req, timeout=45))
        except Exception as e:
            if k == 2: print('api-football error', e); return None
    return None
def fetch_af_odds(afid):
    """返回该场全部 bookmakers(每家含全部 bet 种类),失败返回 None。每场每次仅 1 个请求。"""
    if not AFKEY or not afid: return None
    d = af_get(f"https://v3.football.api-sports.io/odds?fixture={afid}")
    if not d: return None
    resp = d.get('response', [])
    return resp[0].get('bookmakers') if resp else None
def af_book(bms, bid): return next((b for b in bms if b['id'] == bid), None) if bms else None
def af_bet(book, betid):
    if not book: return None
    bt = next((x for x in book.get('bets', []) if x['id'] == betid), None)
    return bt['values'] if bt else None
def af_vals(bms, betid, prefer=PIN):
    """优先取 Pinnacle 的该盘口,缺则取第一家有此盘口的书商。"""
    v = af_bet(af_book(bms, prefer), betid)
    if v: return v
    for b in (bms or []):
        v = af_bet(b, betid)
        if v: return v
    return None
def af_h2h(vals):
    o = {}
    for v in (vals or []):
        k = v['value'].lower()
        if k in ('home', 'draw', 'away'):
            try: o[k] = float(v['odd'])
            except Exception: pass
    return o if len(o) == 3 else None
def af_tot(vals):  # 大小球 2.5
    if not vals: return None
    o = {}
    for v in vals:
        s = v['value'].lower()
        if '2.5' in s:
            if s.startswith('over'):
                try: o['over'] = float(v['odd'])
                except Exception: pass
            elif s.startswith('under'):
                try: o['under'] = float(v['odd'])
                except Exception: pass
    return o or None
def af_spread(bms):  # 亚盘:取主客赔率最接近(主盘口)的让球线
    vals = af_vals(bms, 4)
    if not vals: return None
    g = {}
    for v in vals:
        p = v['value'].rsplit(' ', 1)
        if len(p) != 2: continue
        side, num = p[0].strip(), p[1].strip()
        try: g.setdefault(num, {})[side] = float(v['odd'])
        except Exception: pass
    cand = [(n, d) for n, d in g.items() if 'Home' in d and 'Away' in d]
    if not cand: return None
    n, d = min(cand, key=lambda x: abs(x[1]['Home'] - x[1]['Away']))
    try: pt = float(n)
    except Exception: pt = None
    return {'pt': pt, 'home': d['Home'], 'away': d['Away']}
def af_pair(vals, keys):  # 双方进球/双重机会:取指定取值
    if not vals: return None
    o = {}
    for v in vals:
        if v['value'] in keys:
            try: o[v['value']] = float(v['odd'])
            except Exception: pass
    return o or None
def af_score(bms):  # 逐比分:取盘口条目最多的书商(通常 Pinnacle 121 条)
    cands = []
    for b in (bms or []):
        vals = af_bet(b, 10)
        if not vals: continue
        parsed = {}
        for v in vals:
            try: parsed[v['value'].replace(':', '-').strip()] = float(v['odd'])
            except Exception: pass
        if parsed: cands.append((len(parsed), b['name'], parsed))
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
    rich = {}; hrs = round((cfg['ko']-now).total_seconds()/3600, 1)
    bms = fetch_af_odds(AFID.get(cfg['slug'])) if hrs > 0 else None  # 仅赛前采样,每场 1 个请求
    if bms:
        pinb = af_book(bms, PIN)
        ph = af_h2h(af_bet(pinb, 1))                       # 锐庄胜平负
        allh = [h for h in (af_h2h(af_bet(b, 1)) for b in bms) if h]
        soft = {k: round(sum(x[k] for x in allh)/len(allh), 3) for k in ('home','draw','away')} if allh else None
        src = ph or soft
        tot = af_tot(af_bet(pinb, 5)) or af_tot(af_vals(bms, 5))  # 锐庄大小球,缺则软庄
        if src:
            dv = {k: round(v, 4) for k, v in devig(src).items()}
            rec = {'ts': now.isoformat(timespec='minutes'), 'hrs_to_ko': hrs, 'pin_h2h': ph,
                   'soft_h2h': soft, 'pin_tot25': tot, 'devig': dv, 'n_books': len(allh)}
            with open(os.path.join(DATA_DIR, cfg['slug']+'.jsonl'), 'a') as f:
                f.write(json.dumps(rec, ensure_ascii=False)+'\n')
            print('sampled', cfg['slug'], hrs, 'h', '| books', len(allh))
        rich['spread'] = af_spread(bms)
        rich['tot'] = tot
        rich['btts'] = af_pair(af_vals(bms, 8), ('Yes', 'No'))
        rich['dc'] = af_pair(af_vals(bms, 12), ('Home/Draw', 'Home/Away', 'Draw/Away'))
        rich['score_odds'] = af_score(bms)
        rich['pred'] = fetch_predictions(AFID.get(cfg['slug']))
    return rich

# ---------- 过去赛果对账(价值模型回测,纯赛前去水位赔率驱动,绝不看赛果)----------
def value_call(d):
    """输入赛前去水位概率 d{home/draw/away},输出 (分档, 热门方, 价值方向, 判定类型)。"""
    fav = max(d, key=d.get); f = d[fav]
    tier = '①悬殊' if f >= 0.65 else ('②中热门' if f >= 0.45 else '③势均')
    if tier == '①悬殊':
        return tier, fav, '砍屠杀 / 小球 / 弱队受让', 'anti_blowout'
    return tier, fav, '平 / 弱队 / 小球', 'anti_fav'
def call_hit(kind, fav, gh, ga):
    """方向验证口径:②③档=热门没赢则中;①档(悬殊)=热门净胜≤1球(没被血洗)则中。"""
    res = 'home' if gh > ga else ('away' if ga > gh else 'draw')
    if kind == 'anti_fav': return res != fav
    return abs(gh - ga) <= 1
def _res(gh, ga): return 'home' if gh > ga else ('away' if ga > gh else 'draw')
def value_picks(d, kind, fav):
    """顺价值方向,从赛前去水位泊松网格里筛 2 个推荐比分 + 胜负倾向。"""
    lh, la, grid = poisson_calc(d['home'], d['away'], None)
    def r(s): i, j = map(int, s.split('-')); return 'home' if i > j else ('away' if j > i else 'draw')
    if kind == 'anti_blowout':              # 押热门小胜(砍屠杀):候选=热门赢
        cand = [s for s in grid if r(s) == fav]; wdl = ('win', fav)
    else:                                   # 押平/非热门不败:候选=平 或 非热门赢
        cand = [s for s in grid if r(s) != fav]; wdl = ('safe', fav)
    cand.sort(key=lambda s: -grid[s])
    picks = (cand or [max(grid, key=grid.get)])[:2]
    return [s.replace('-', ':') for s in picks], wdl
def wdl_text(wdl, cnh, cna):
    mode, fav = wdl; favcn = cnh if fav == 'home' else cna; oppcn = cna if fav == 'home' else cnh
    return f'{favcn} 胜(让球)' if mode == 'win' else f'平 或 {oppcn}(双重机会)'
def wdl_hit(wdl, gh, ga):
    mode, fav = wdl; res = _res(gh, ga)
    return (res == fav) if mode == 'win' else (res != fav)
def settle100(v):
    """模拟每场 ¥100(主注50 + 2比分注30/20),用真实赔率按实际结果结算,返回 (赢回, 盈亏)。"""
    d = v['devig']; kind = v['kind']; fav = v['fav']; gh, ga = v['gh'], v['ga']; res = _res(gh, ga); won = 0.0
    if kind == 'anti_blowout':                       # 主注押小球
        hit = (gh + ga) <= 2; odd = v.get('tot_u')
    else:                                            # 主注押"非热门不败"双重机会
        dc = v.get('dc') or {}
        if fav == 'home': hit, odd = res != 'home', dc.get('Draw/Away')
        else: hit, odd = res != 'away', dc.get('Home/Draw')
    if hit and odd: won += 50 * odd
    po = v.get('po') or {}; picks, _ = value_picks(d, kind, fav)
    for i, sc in enumerate(picks):
        key = sc.replace(':', '-')
        if f'{gh}-{ga}' == key and po.get(key): won += [30, 20][i] * po[key]
    return round(won), round(won) - 100
def fetch_fixtures():
    if not AFKEY: return []
    d = af_get("https://v3.football.api-sports.io/fixtures?league=1&season=2026")
    return d.get('response', []) if d else []
PAST_CACHE = os.path.join(DATA_DIR, 'past.json')
def build_past():
    """拉已结束比赛(赛果固定→缓存,只对新结束场次请求赔率),返回按时间倒序的对账列表。"""
    cache = {}
    if os.path.exists(PAST_CACHE):
        try: cache = json.load(open(PAST_CACHE))
        except Exception: cache = {}
    fx = fetch_fixtures()
    ft = [f for f in fx if f['fixture']['status']['short'] in ('FT', 'AET', 'PEN')]
    for f in ft:
        fid = str(f['fixture']['id'])
        gh, ga = f['goals']['home'], f['goals']['away']
        if gh is None or ga is None: continue
        h, a = f['teams']['home']['name'], f['teams']['away']['name']
        rec = cache.get(fid)
        if rec and rec.get('gh') == gh and rec.get('ga') == ga and rec.get('devig') and rec.get('dc') is not None:
            continue  # 已缓存且比分一致、含下注赔率,跳过请求
        bms = fetch_af_odds(int(fid))
        mw = af_h2h(af_bet(af_book(bms, PIN), 1)) if bms else None
        if not mw: mw = af_h2h(af_vals(bms, 1)) if bms else None
        if not mw:  # 无赛前赔率,仅记赛果
            cache[fid] = {'date': f['fixture']['date'], 'h': h, 'a': a, 'gh': gh, 'ga': ga, 'devig': None}
            continue
        d = {k: round(v, 4) for k, v in devig(mw).items()}
        tier, fav, dirn, kind = value_call(d)
        dcd = af_pair(af_vals(bms, 12), ('Home/Draw', 'Home/Away', 'Draw/Away')) or {}
        totd = af_tot(af_bet(af_book(bms, PIN), 5)) or af_tot(af_vals(bms, 5)) or {}
        scd = (af_score(bms) or {}).get('odds', {})
        pk, _w = value_picks(d, kind, fav)
        po = {sc.replace(':', '-'): scd.get(sc.replace(':', '-')) for sc in pk}
        cache[fid] = {'date': f['fixture']['date'], 'h': h, 'a': a, 'gh': gh, 'ga': ga,
                      'devig': d, 'tier': tier, 'fav': fav, 'dir': dirn, 'kind': kind,
                      'hit': bool(call_hit(kind, fav, gh, ga)),
                      'dc': dcd, 'tot_u': totd.get('under'), 'po': po}
    with open(PAST_CACHE, 'w') as fp: json.dump(cache, fp, ensure_ascii=False, indent=0)
    out = []
    for fid, v in cache.items():
        v = dict(v); v['fid'] = fid
        if v.get('devig'):  # 纯计算:顺价值方向产出 2 推荐比分 + 胜负倾向,并模拟 ¥100 下注结算
            picks, wdl = value_picks(v['devig'], v['kind'], v['fav'])
            v['picks'] = picks; v['wdl_txt'] = wdl_text(wdl, cn_of(v['h']), cn_of(v['a']))
            v['wdl_hit'] = bool(wdl_hit(wdl, v['gh'], v['ga']))
            v['score2_hit'] = (f"{v['gh']}:{v['ga']}" in picks)
            v['won'], v['pl'] = settle100(v)
        out.append(v)
    out.sort(key=lambda x: x['date'], reverse=True)
    return out

def L(cfg): return {'home': cfg['cn_h'], 'draw': '平局', 'away': cfg['cn_a']}

# ---------- UI 组件 ----------
def head(title):
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title} · 世界杯推演分析</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">'
            '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style>')
APPBAR = ('<header class="appbar"><div class="brand"><span class="material-symbols-outlined">analytics</span>世界杯推演分析</div>'
          '<div class="barIcons"><span class="material-symbols-outlined">search</span>'
          '<span class="material-symbols-outlined">notifications</span></div></header>')
def nav(active='value'):
    items = [('matches','sports_soccer','Matches'),('value','trending_up','Value'),('signals','sensors','Signals'),('account','person','Account')]
    a = ''.join(f'<a class="{"on" if k==active else ""}"><span class="material-symbols-outlined">{ic}</span>{lb}</a>' for k, ic, lb in items)
    return f'<nav class="nav">{a}</nav>'
def bj_time(cfg):  # 北京时间(UTC+8)比赛日期
    bj = cfg['ko'] + datetime.timedelta(hours=8)
    return f'{bj.month}/{bj.day} 周{"一二三四五六日"[bj.weekday()]} {bj.hour:02d}:{bj.minute:02d}'
def tier_chips(cfg, hrs):
    out = ''
    for p in [x.strip() for x in cfg['tier'].split('·')]:
        cls = 'chip val' if '价值' in p else ('chip warn' if ('冷门' in p or '警报' in p) else 'chip')
        out += f'<span class="{cls}">{p}</span>'
    rel = f' · 距开赛 {hrs}h' if hrs > 0 else ' · 已开赛'
    out += f'<span class="chip dim">🕐 {bj_time(cfg)}（北京）{rel}</span>'
    return f'<div class="chips">{out}</div>'
def probrow(d, cfg):
    l = L(cfg); mx = max(d, key=d.get); al = {'home':'left','draw':'center','away':'right'}
    cells = ''.join(f'<div class="{"fav" if k==mx else "dimv"}" style="text-align:{al[k]}">'
                    f'<span class="pn">{l[k]}</span><b class="pv">{d[k]*100:.0f}%</b></div>' for k in ('home','draw','away'))
    return f'<div class="probrow">{cells}</div>'
def minibar(d):  # 主/平/客比例条(主青柠·平灰·客猩红)
    col = {'home':'#CCFF00','draw':'#3f465c','away':'#FF0055'}
    segs = ''.join(f'<i style="flex:{max(d[k]*100,4):.1f};background:{col[k]}"></i>' for k in ('home','draw','away'))
    return f'<div class="minibar">{segs}</div>'
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
    odds = so['odds']; top = sorted(odds.items(), key=lambda x: x[1])
    h = (f'<div class="note" style="margin-bottom:10px">共 {len(odds)} 个比分 · 期望值=模型推测×盘口,&gt;1 即有价值</div>'
         f'<table class="so"><thead><tr><th>比分</th><th>盘口</th><th>模型推测</th><th>期望值</th></tr></thead><tbody>')
    for s, o in top:
        pp = grid.get(s, 0); ev = pp*o
        h += (f'<tr class="{"val" if ev>1.05 else ""}"><td class="num s">{s}</td><td class="num">{o}</td>'
              f'<td class="num">{pp*100:.0f}%</td><td class="num e">{ev:.2f}</td></tr>')
    return h + '</tbody></table>'

CDSCRIPT = ('<script>(function(){var ko=new Date("__KO__").getTime();var e=document.getElementById("cd");'
            'function t(){if(!e)return;var d=ko-Date.now();if(d<0){e.textContent="已开赛";return;}'
            'var h=Math.floor(d/3.6e6),m=Math.floor(d%3.6e6/6e4);'
            'e.innerHTML=("0"+h).slice(-2)+"<small>H</small> "+("0"+m).slice(-2)+"<small>M</small>";}'
            't();setInterval(t,30000);})();</script>')
# 比分概率付费遮挡:输入验证码 666888 解锁(前端简单门槛,localStorage 记忆)
UNLOCK_JS = ('<script>(function(){var b=document.getElementById("lock-scores");if(!b)return;'
             'if(localStorage.getItem("wc_paid")==="1"){b.classList.add("open");return;}'
             'var k=b.querySelector(".lockbtn"),i=b.querySelector(".lockinput"),h=b.querySelector(".lockhint");'
             'function go(){if(i.value.trim()==="666888"){b.classList.add("open");try{localStorage.setItem("wc_paid","1")}catch(e){}}'
             'else{h.textContent="验证码错误,请重试";i.value="";}}'
             'k.addEventListener("click",go);i.addEventListener("keyup",function(e){if(e.key==="Enter")go();});})();</script>')

def sec_head(icon, title, sub=''):
    s = f'<span class="sech-sub">{sub}</span>' if sub else ''
    return f'<div class="sech"><span class="sech-ic"><span class="material-symbols-outlined">{icon}</span></span><span class="sech-t">{title}</span>{s}</div>'

def match_header(rows, cfg):
    l = L(cfg); last = rows[-1]; first = rows[0]; d = last['devig']; mx = max(d, key=d.get)
    hot = ('<div class="hotpick"><span class="material-symbols-outlined" style="font-size:14px">local_fire_department</span>HOT PICK</div>'
           if '价值' in cfg['tier'] else '')
    mins = max(0, (cfg['ko']-now).total_seconds()/60); ch = int(mins//60); cm = int(mins % 60)
    tier = ' '.join(p.strip() for p in cfg['tier'].split('·')[:2])
    def cell(k):
        cur = d[k]*100; dv = (d[k]-first['devig'][k])*100
        arr, ac = ('↑','#CCFF00') if dv >= .05 else (('↓','#FF0055') if dv <= -.05 else ('→','#8e9379'))
        return (f'<div class="ph"><div class="ph-lbl">{l[k]}</div>'
                f'<div class="ph-big" style="color:{"#CCFF00" if k==mx else "#d4e4fa"}">{cur:.1f}%</div>'
                f'<div class="ph-chg mono" style="color:{ac}">{arr} {abs(dv):.1f}%</div></div>')
    segs = ''.join(f'<div style="flex:{max(d[k]*100,3):.1f};background:{"#CCFF00" if k==mx else "#3f465c"}"></div>' for k in ('home','draw','away'))
    return (f'<div class="glass vshead">{hot}<div class="vsrow">'
            f'<div class="vsteam">{team_badge(cfg["home"], l["home"])}<div class="tn">{l["home"]}</div></div>'
            f'<div class="vsmid"><div class="kol">距离开赛</div><div class="kot" id="cd">{ch:02d}<small>H</small> {cm:02d}<small>M</small></div></div>'
            f'<div class="vsteam">{team_badge(cfg["away"], l["away"])}<div class="tn">{l["away"]}</div></div>'
            f'</div><div class="prob3">{cell("home")}{cell("draw")}{cell("away")}</div>'
            f'<div class="pbar">{segs}</div></div>')

def ev_cards(rows, cfg):
    l = L(cfg); p = rows[-1].get('pin_h2h')
    if not p: return ''
    out = ''
    for k in ('home','draw','away'):
        ev = cfg['my'][k]*p[k]
        if ev > 1.03: cls, tag, ic = 'val', '有价值', 'check_circle'
        elif ev > .99: cls, tag, ic = 'mid', '临界', 'remove'
        else: cls, tag, ic = 'bad', '别碰', 'block'
        out += (f'<div class="evc {cls}"><div class="evbar"></div>'
                f'<div class="evmain"><div class="evteam">{l[k]}</div>'
                f'<div class="evstat">我估: {cfg["my"][k]:.0%}　赔率: {p[k]}</div></div>'
                f'<div class="evright"><div class="evev">期望值 {ev:.2f}</div>'
                f'<div class="evtag"><span class="material-symbols-outlined" style="font-size:15px">{ic}</span>{tag}</div></div></div>')
    return out

def reasoning_timeline(cfg):
    steps = REASON.get(cfg['slug'], [])
    if not steps: return '<p class="note">暂无推理</p>'
    ic = ['bar_chart','trending_up','new_releases','groups','tune']; out = ''; n = len(steps)
    for i, (t, dsc) in enumerate(steps):
        final = (i == n-1); icon = 'priority_high' if final else ic[min(i, len(ic)-1)]
        out += (f'<div class="tl-item{" final" if final else ""}"><div class="tl-icon"><span class="material-symbols-outlined">{icon}</span></div>'
                f'<div class="tl-body"><div class="tl-t">{t}</div><div class="tl-d">{dsc}</div></div></div>')
    return out

def scores_grid(lh, la, grid):
    top = sorted(grid.items(), key=lambda x: -x[1])[:6]; cells = ''
    for i, (s, p) in enumerate(top):
        a, b = s.split('-')
        cells += f'<div class="scg-cell{" hot" if i==0 else ""}"><div class="scg-s">{a} - {b}</div><div class="scg-p">{p*100:.1f}%</div></div>'
    return (f'<div class="scg">{cells}</div><div class="xg"><span class="xg-badge">xG</span><span class="xg-l">预期进球</span>'
            f'<span class="xg-v">主 <b style="color:#CCFF00">{lh:.2f}</b> / 客 <b style="color:#FF0055">{la:.2f}</b></span></div>')

def markets_html(cfg, rows, rich):
    l = L(cfg); p = rows[-1].get('pin_h2h'); t = rich.get('tot') or rows[-1].get('pin_tot25'); r = ''
    if p: r += f'<tr><td>胜平负</td><td class="num">{l["home"]} {p["home"]} · 平 {p["draw"]} · {l["away"]} {p["away"]}</td></tr>'
    if t: r += f'<tr><td>大小球 2.5</td><td class="num">大 {t.get("over","-")} · 小 {t.get("under","-")}</td></tr>'
    sp = rich.get('spread')
    if sp and sp.get('pt') is not None:
        r += f'<tr><td>让球(亚盘)</td><td class="num">{l["home"]} {sp["pt"]:+g} @{sp["home"]} · {l["away"]} {-sp["pt"]:+g} @{sp.get("away","-")}</td></tr>'
    if rich.get('btts'): r += f'<tr><td>双方进球</td><td class="num">是 {rich["btts"].get("Yes","-")} · 否 {rich["btts"].get("No","-")}</td></tr>'
    if rich.get('dc'):
        dcn = {'Home/Draw': f'{l["home"]}或平', 'Home/Away': f'{l["home"]}或{l["away"]}', 'Draw/Away': f'平或{l["away"]}'}
        r += f'<tr><td>双重机会</td><td class="num">{" · ".join(f"{dcn.get(k,k)} {v}" for k,v in rich["dc"].items())}</td></tr>'
    return f'<table>{r}</table>' if r else '<p class="note">暂无盘口数据</p>'

def matchup_analysis(cfg):
    s = cfg['st']; ch = cfg['cn_h']; ca = cfg['cn_a']
    lis = ''
    for x in s['mu']:
        x = x.replace(' vs ', ' <b class="muvs">vs</b> ')
        lis += f'<li><span class="mudot"></span><span>{x}</span></li>'
    oh = s['oh']; oa = s['oa']; tot = (oh + oa) or 1
    hw = oh / tot * 100  # 主队胜率在条形中所占宽度
    head = (f'<b style="color:var(--lime)">{oh}%</b> vs '
            f'<b style="color:var(--crim)">{oa}%</b>'
            f'<span class="opta-tag">({s["otag"]})</span>')
    return (
        f'<div class="mua-h2h"><div class="muah">'
        f'<span class="material-symbols-outlined">history</span><span class="muah-t">历史交锋</span></div>'
        f'<p>{s["h2h"]}</p></div>'
        f'<div class="mua-forms">'
        f'<div class="mua-fc home"><h4>{ch} {s["fh"]}</h4><p>{s["xh"]}</p></div>'
        f'<div class="mua-fc away"><h4>{ca} {s["fa"]}</h4><p>{s["xa"]}</p></div></div>'
        f'<div class="glass mua-key"><div class="muah">'
        f'<span class="material-symbols-outlined">gps_fixed</span><span class="muah-t">关键对位</span></div>'
        f'<div class="mua-div"></div><ul class="mua-mu">{lis}</ul><div class="mua-div"></div>'
        f'<div class="opta-row"><span class="opta-pill">{s.get("osrc","OPTA")}</span>'
        f'<span class="opta-txt">{head}</span></div>'
        f'<div class="opta-bar"><i style="width:{hw:.1f}%;background:var(--lime)"></i>'
        f'<i style="flex:1;background:var(--crim)"></i></div>'
        f'<div class="opta-val"><i>价值结论:{s["val"]}</i></div></div>')

def reasoning_html(cfg):
    steps = REASON.get(cfg['slug'], [])
    if not steps: return '<p class="note">暂无推理</p>'
    return ''.join(f'<div class="mtag"><b>{i+1}.</b> {s}</div>' for i, s in enumerate(steps))

def fetch_last5(tid):  # 该队最近 5 场(API,含热身赛),返回 W/D/L 列表(旧→新)
    if not tid: return []
    d = af_get(f"https://v3.football.api-sports.io/fixtures?team={tid}&last=5")
    out = []
    for f in (d.get('response', []) if d else []):
        gh, ga = f['goals']['home'], f['goals']['away']
        if gh is None or ga is None: continue
        ih = f['teams']['home']['id'] == tid
        gf, gc = (gh, ga) if ih else (ga, gh)
        out.append('W' if gf > gc else ('L' if gf < gc else 'D'))
    return list(reversed(out))
def form_dots(form):
    col = {'W':'#CCFF00','D':'#8e9379','L':'#FF0055'}
    if not form: return '<span class="form-dots"><span class="fdmin">暂无</span></span>'
    return '<span class="form-dots">' + ''.join(f'<span class="fdot" style="background:{col.get(r,"#888")}">{r}</span>' for r in form) + '</span>'
def form_block(cfg):
    th = TID.get(cfg['home']); ta = TID.get(cfg['away'])
    if not th or not ta: return ''
    fh = fetch_last5(th); fa = fetch_last5(ta)
    if not fh and not fa: return ''
    return (f'{sec_head("trending_up","近 5 场状态")}'
            f'<div class="form-blk">'
            f'<div class="form-row"><span class="form-team">{cfg["cn_h"]}</span>{form_dots(fh)}</div>'
            f'<div class="form-row"><span class="form-team">{cfg["cn_a"]}</span>{form_dots(fa)}</div></div>'
            f'<div class="vs-note">近 5 场含热身赛 · 左旧 → 右新 · W 胜 / D 平 / L 负</div>')

def fetch_predictions(afid):
    if not afid: return None
    d = af_get(f"https://v3.football.api-sports.io/predictions?fixture={afid}")
    r = d.get('response') if d else None
    return r[0] if r else None
def _pnum(s):
    try: return float(str(s).replace('%', ''))
    except Exception: return 0.0
def cn_advice(adv, cfg):
    adv = (adv or '')
    for en, cn in [('Combo Double chance :', '组合双重机会:'), ('Double chance :', '双重机会:'),
                   ('Winner :', '胜者:'), (' or ', ' 或 '), (' and ', ' 且 '), ('draw', '平局')]:
        adv = adv.replace(en, cn)
    return adv.replace(cfg['home'], cfg['cn_h']).replace(cfg['away'], cfg['cn_a'])
def third_party_block(cfg, pred):
    if not pred: return ''
    pr = pred.get('predictions', {}); pct = pr.get('percent', {})
    h, d, a = _pnum(pct.get('home')), _pnum(pct.get('draw')), _pnum(pct.get('away'))
    if 'No prediction' in (pr.get('advice') or '') or (h == d == a): return ''  # API 无有效预测,隐藏
    adv = cn_advice(pr.get('advice', ''), cfg)
    row = (f'<div class="tp-pct"><span style="color:#CCFF00">{cfg["cn_h"]} {h:.0f}%</span>'
           f'<span style="color:#8e9379">平 {d:.0f}%</span>'
           f'<span style="color:#FF0055">{cfg["cn_a"]} {a:.0f}%</span></div>'
           f'<div class="tp-bar"><i style="flex:{max(h,3):.0f};background:#CCFF00"></i>'
           f'<i style="flex:{max(d,3):.0f};background:#3f465c"></i><i style="flex:{max(a,3):.0f};background:#FF0055"></i></div>')
    cmap = {'total':'综合实力','goals':'进球预期','h2h':'交锋历史','form':'近期状态','att':'进攻','def':'防守','poisson_distribution':'泊松模型'}
    cp = pred.get('comparison', {}); rows = ''
    for k, label in cmap.items():
        v = cp.get(k)
        if not v: continue
        hh, aa = _pnum(v.get('home')), _pnum(v.get('away'))
        if hh == 0 and aa == 0: continue
        w = hh/(hh+aa)*100 if (hh+aa) else 50
        rows += (f'<div class="cmp-row"><span class="cmp-l">{hh:.0f}</span>'
                 f'<div class="cmp-bar"><i style="width:{w:.0f}%"></i></div>'
                 f'<span class="cmp-r">{aa:.0f}</span><span class="cmp-c">{label}</span></div>')
    adv_html = f'<div class="tp-adv"><span class="material-symbols-outlined">tips_and_updates</span>算法建议:{adv}</div>' if adv else ''
    cmp_html = f'<div class="cmp-blk">{rows}</div>' if rows else ''
    return (f'{sec_head("hub","第三方参照 · API 官方预测")}{row}{adv_html}{cmp_html}'
            f'<div class="vs-note">API-Football 机器学习预测,与本页「市场去水位 / 价值模型」相互参照(部分维度国家队数据缺省已隐藏)</div>')

def bet_plan(rich, my, kind, fav, cnh, cna):
    """模拟拿 100 元的价值投注:用我的概率 × 真实赔率,给出主注(胜负方向)+ 2 个比分注。"""
    g = poisson_calc(my['home'], my['away'], None)[2]  # 我的判断对应的比分分布
    bets = []
    if kind == 'anti_blowout':  # 砍屠杀:核心价值在小球
        prob = sum(p for s, p in g.items() if sum(map(int, s.split('-'))) <= 2)
        odd = (rich.get('tot') or {}).get('under')
        bets.append(['主注', '小球(总进球 ≤ 2)', prob, odd, 50])
    else:                       # 逆向:押"平 或 非热门"双重机会
        dc = rich.get('dc') or {}
        if fav == 'home': key, lbl, prob = 'Draw/Away', f'平 或 {cna}', my['draw'] + my['away']
        else: key, lbl, prob = 'Home/Draw', f'平 或 {cnh}', my['draw'] + my['home']
        bets.append(['主注', f'{lbl}(双重机会)', prob, dc.get(key), 50])
    picks, _ = value_picks(my, kind, fav)
    so = (rich.get('score_odds') or {}).get('odds', {})
    for i, sc in enumerate(picks):
        key = sc.replace(':', '-')
        bets.append(['比分', sc, g.get(key, 0), so.get(key), [30, 20][i] if i < 2 else 10])
    out = []
    for tag, lbl, prob, odd, stake in bets:
        if not odd: odd = round(1/prob, 2) if prob > 0 else 0  # 赔率暂缺→用我的概率反推兜底
        out.append({'tag': tag, 'lbl': lbl, 'prob': prob, 'odd': round(odd, 2), 'stake': stake, 'ret': round(stake*odd)})
    return out
def crowd_block(slug, grid):
    """万人竞猜：抖音评论众选比分 vs 我的 Poisson 模型。"""
    cd = CROWD_DATA.get(slug)
    if not cd: return ''
    total_votes = sum(v for _, v in cd['top'])
    if total_votes == 0: return ''
    scored_n = cd.get('scored', total_votes)  # 有效含比分评论总数
    # 计算众选 WDL 分布
    wdl = {'home': 0, 'draw': 0, 'away': 0}
    for s, v in cd['top']:
        h, a = map(int, s.split('-'))
        if h > a: wdl['home'] += v
        elif h == a: wdl['draw'] += v
        else: wdl['away'] += v
    rows = ''
    top3 = cd['top'][:3]
    so_model = sorted(grid.items(), key=lambda x: -x[1])[:1]
    model_top = so_model[0][0] if so_model else ''
    slug_odds = CROWD_SCORE_ODDS.get(slug, {})
    for i, (s, votes) in enumerate(top3):
        sc = s.replace('-', ':')
        pct = votes / total_votes * 100
        bar_w = int(pct / max(cd['top'][0][1] / total_votes * 100, 1) * 100)
        match_model = s == model_top
        fw = '800' if i == 0 else '500'
        fg = 'var(--fg)' if i == 0 else 'var(--sec)'
        bar_bg = 'var(--lime)' if i == 0 else 'var(--sec)'
        bar_op = '1' if i == 0 else '0.5'
        model_tag = ' <span style="color:var(--lime);font-size:12px">⚡模型一致</span>' if match_model else ''
        # 价差比：大众隐含概率 / 庄家隐含概率
        od = slug_odds.get(s)
        vr_tag = ''
        if od:
            ratio = (votes / scored_n) / (1 / od)
            if ratio >= 2.0:
                vr_tag = f' <span style="color:var(--lime);font-size:11px">价差{ratio:.1f}x @{od}</span>'
            elif ratio >= 1.5:
                vr_tag = f' <span style="color:#BA7517;font-size:11px">{ratio:.1f}x @{od}</span>'
            else:
                vr_tag = f' <span style="color:rgba(255,255,255,.3);font-size:11px">@{od}</span>'
        rows += (f'<div style="margin:6px 0">'
                 f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">'
                 f'<span style="font-size:15px;font-weight:{fw};color:{fg}">#{i+1} <b>{sc}</b>{model_tag}</span>'
                 f'<span style="font-size:13px;color:var(--sec)">{votes} 票 · {pct:.0f}%{vr_tag}</span></div>'
                 f'<div style="height:4px;border-radius:2px;background:rgba(255,255,255,.08);overflow:hidden">'
                 f'<div style="height:100%;width:{bar_w}%;background:{bar_bg};border-radius:2px;opacity:{bar_op}"></div></div></div>')
    # WDL 小结
    wdl_total = sum(wdl.values()) or 1
    wdl_row = (f'<div style="display:flex;gap:8px;margin-top:10px;font-size:11px;color:var(--sec)">'
               f'<span>主胜 {wdl["home"]/wdl_total*100:.0f}%</span>'
               f'<span>平局 {wdl["draw"]/wdl_total*100:.0f}%</span>'
               f'<span>客胜 {wdl["away"]/wdl_total*100:.0f}%</span>'
               f'<span style="margin-left:auto">共 {cd["n"]} 条评论 · {scored_n} 票含比分</span></div>')
    return f'<div class="glass">{sec_head("groups","万人竞猜")}{rows}{wdl_row}</div>'

def crowd_backtest_block():
    inv = len(BACKTEST) * 100
    ret1 = ret2 = h1 = h2 = 0
    rows_html = ''
    for b in BACKTEST:
        actual = b['actual']
        s1, o1 = b['p1']; s2, o2 = b['p2']
        hit1 = s1 == actual; hit2 = s2 == actual
        if hit1: h1 += 1; ret1 += o1 * 100
        if hit2: h2 += 1; ret2 += o2 * 100
        t1 = '<span style="color:var(--lime)">命中</span>' if hit1 else '<span style="color:var(--sec)">✗</span>'
        t2 = '<span style="color:var(--lime)">命中</span>' if hit2 else '<span style="color:var(--sec)">✗</span>'
        vr = f'<span style="color:var(--lime);font-size:10px"> {b["vr"]}x↑</span>' if b.get('vr') else ''
        wn = '<span style="font-size:10px;color:#BA7517"> ⚠</span>' if b.get('warn') else ''
        rows_html += (
            f'<div style="padding:8px 0;border-bottom:.5px solid rgba(255,255,255,.07);font-size:12px">'
            f'<div style="display:flex;justify-content:space-between;color:var(--sec);font-size:11px;margin-bottom:4px">'
            f'<span>{b["cn"]}{wn}</span>'
            f'<span>实际 <b style="color:var(--fg)">{actual.replace("-",":")}</b></span></div>'
            f'<div style="display:flex;gap:14px">'
            f'<span>众#1 <b>{s1.replace("-",":")}</b> @{o1} {t1}</span>'
            f'<span>众#2 <b>{s2.replace("-",":")}</b> @{o2} {t2}{vr}</span>'
            f'</div></div>')
    roi1 = round((ret1 - inv) / inv * 100)
    roi2 = round((ret2 - inv) / inv * 100)
    n = len(BACKTEST)
    def sc(label, roi, hits, note=''):
        col = 'var(--lime)' if roi >= 0 else '#FF0055'
        sg = '+' if roi >= 0 else ''
        return (f'<div style="background:rgba(255,255,255,.05);border-radius:8px;padding:10px;text-align:center">'
                f'<div style="font-size:10px;color:var(--sec);margin-bottom:3px">{label}</div>'
                f'<div style="font-size:20px;font-weight:700;color:{col}">{sg}{roi}%</div>'
                f'<div style="font-size:10px;color:var(--sec);margin-top:2px">{hits}/{n} 命中{note}</div></div>')
    strats = (f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px">'
              f'{sc("买众#1",roi1,h1)}{sc("买众#2",roi2,h2," · @29大冷")}{sc("买最少票",-100,0)}</div>')
    insight = (f'<div style="margin-top:10px;padding:8px 10px;border-left:2px solid rgba(204,255,0,.35);'
               f'background:rgba(204,255,0,.04);font-size:11px;color:var(--sec);line-height:1.6">'
               f'价值信号：大众票占比 ÷ 庄家隐含概率 ≥ 2 才有正期望。'
               f'西班牙 0:0 大众 10.8% / 庄家 3.4% = 3.2x，唯一明确价差盘，@29 命中。</div>')
    dnote = (f'<div style="font-size:10px;color:#BA7517;margin-top:8px;line-height:1.5">'
             f'⚠ 荷兰/巴西评论可能含赛后数据；西班牙/伊朗已做赛前时间戳过滤。{n} 场样本极小，勿过度推断。</div>')
    hd = sec_head('query_stats', f'众选回测 · {n} 场')
    return f'<div class="glass">{hd}{rows_html}{strats}{insight}{dnote}</div>'

def score_top3_block(rich, my, grid):
    """比分推荐 TOP3：Poisson 模型概率最高的3个比分 + 真实赔率。"""
    top3 = sorted(grid.items(), key=lambda x: -x[1])[:3]
    so = (rich.get('score_odds') or {}).get('odds', {})
    rows = ''
    for i, (s, prob) in enumerate(top3):
        sc_disp = s.replace('-', ':')
        od = so.get(s)
        od_txt = f'@{od}' if od else ''
        rows += (f'<div class="bet{" main" if i==0 else ""}"><span class="bet-tag">TOP{i+1}</span>'
                 f'<div class="bet-mid"><b>{sc_disp}</b>'
                 f'<span class="bet-od">我估 {prob*100:.1f}%{" · " + od_txt if od_txt else ""}</span></div></div>')
    return f'<div class="glass">{sec_head("scoreboard","比分推荐 TOP3")}{rows}</div>'

def wdl_rec_block(rows, cfg):
    """胜平负推荐：基于去水位赔率 × 我的概率，给出价值方向。"""
    p = rows[-1].get('pin_h2h')
    if not p: return ''
    l = L(cfg); out = ''
    for k in ('home', 'draw', 'away'):
        ev = cfg['my'][k] * p[k]
        if ev > 1.03: cls, tag, ic = 'val', '✅ 推荐', 'check_circle'
        elif ev > .99: cls, tag, ic = 'mid', '⚪ 临界', 'remove'
        else: cls, tag, ic = 'bad', '❌ 不推荐', 'block'
        out += (f'<div class="evc {cls}"><div class="evbar"></div>'
                f'<div class="evmain"><div class="evteam">{l[k]}</div>'
                f'<div class="evstat">我估: {cfg["my"][k]:.0%}　赔率: {p[k]}</div></div>'
                f'<div class="evright"><div class="evev">EV {ev:.2f}</div>'
                f'<div class="evtag"><span class="material-symbols-outlined" style="font-size:15px">{ic}</span>{tag}</div></div></div>')
    return f'<div class="glass">{sec_head("how_to_vote","胜平负推荐")}{out}</div>'

def goals_block(rich, my, grid):
    """进球推荐：大小球 2.5 + BTTS + xG 预期。"""
    t25 = rich.get('tot') or {}
    btts = rich.get('btts') or {}
    lh = sum(i * sum(grid.get(f'{i}-{jj}', 0) for jj in range(8)) for i in range(8))
    la = sum(jj * sum(grid.get(f'{ii}-{jj}', 0) for ii in range(8)) for jj in range(8))
    ov_prob = sum(p for s, p in grid.items() if sum(map(int, s.split('-'))) > 2)
    un_prob = 1 - ov_prob
    btts_prob = sum(p for s, p in grid.items() if int(s.split('-')[0]) > 0 and int(s.split('-')[1]) > 0)
    rows = ''
    # 大球
    over_od = t25.get('over'); over_txt = f'@{over_od}' if over_od else ''
    rows += (f'<div class="bet{"" if ov_prob < un_prob else " main"}"><span class="bet-tag">大球</span>'
             f'<div class="bet-mid"><b>总进球 ≥ 3</b>'
             f'<span class="bet-od">我估 {ov_prob*100:.0f}%{" · "+over_txt if over_txt else ""}</span></div></div>')
    # 小球
    under_od = t25.get('under'); under_txt = f'@{under_od}' if under_od else ''
    rows += (f'<div class="bet{"" if ov_prob >= un_prob else " main"}"><span class="bet-tag">小球</span>'
             f'<div class="bet-mid"><b>总进球 ≤ 2</b>'
             f'<span class="bet-od">我估 {un_prob*100:.0f}%{" · "+under_txt if under_txt else ""}</span></div></div>')
    # BTTS
    if btts:
        by = btts.get('Yes'); bn = btts.get('No')
        rows += (f'<div class="bet"><span class="bet-tag">双进</span>'
                 f'<div class="bet-mid"><b>双方均进球</b>'
                 f'<span class="bet-od">我估 {btts_prob*100:.0f}%'
                 f'{" · 是@"+str(by) if by else ""}{" · 否@"+str(bn) if bn else ""}</span></div></div>')
    rows += (f'<div style="margin-top:10px;font-family:JetBrains Mono,monospace;font-size:12px;color:var(--sec)">'
             f'xG 预期：主 <b style="color:#CCFF00">{lh:.2f}</b> / 客 <b style="color:#FF0055">{la:.2f}</b>（泊松模型）</div>')
    return f'<div class="glass">{sec_head("sports_score","进球推荐")}{rows}</div>'

def build_detail(cfg, rows, rich):
    l = L(cfg); title = f'{cfg["cn_h"]} vs {cfg["cn_a"]}'; script = ''
    if not rows:
        inner = '<div class="glass"><p class="note">暂无数据(比赛可能已开赛或尚未采样)</p></div>'; sub = cfg['tier']
    else:
        last = rows[-1]; n = len(rows); updated = last['ts']; sub = f'更新 {updated}'
        d = last['devig']; t25 = last.get('pin_tot25') or {}
        up = devig({'over': t25['over'], 'under': t25['under']})['under'] if (t25.get('over') and t25.get('under')) else None
        lh, la, grid = poisson_calc(d['home'], d['away'], up)
        script = CDSCRIPT.replace('__KO__', cfg['ko'].isoformat())
        tp = third_party_block(cfg, rich.get('pred'))
        tp_html = f'<div class="glass">{tp}</div>' if tp else ''
        fb = form_block(cfg)
        fb_html = f'<div class="glass">{fb}</div>' if fb else ''
        inner = (f'{match_header(rows, cfg)}'
                 f'{crowd_block(cfg["slug"], grid)}'
                 f'{score_top3_block(rich, cfg["my"], grid)}'
                 f'{wdl_rec_block(rows, cfg)}'
                 f'{goals_block(rich, cfg["my"], grid)}'
                 f'{tp_html}'
                 f'<div class="glass">{sec_head("account_tree","推理逻辑链")}{reasoning_timeline(cfg)}</div>'
                 f'<div class="glass">{sec_head("view_list","比分赔率")}{score_odds_html(rich, grid)}</div>'
                 f'<div class="glass">{sec_head("dashboard","全盘口快照")}{markets_html(cfg, rows, rich)}</div>'
                 f'{fb_html}'
                 f'{sec_head("analytics","对阵分析")}{matchup_analysis(cfg)}')
    body = (f'<main>'
            f'<a class="back" href="index.html"><span class="material-symbols-outlined">chevron_left</span>返回目录</a>'
            f'<div style="height:12px"></div>{inner}'
            f'<div class="foot">自动每 1h 更新 · 仅供研究,非投注建议</div></main>{script}')
    open(os.path.join(DOCS, cfg['slug']+'.html'), 'w').write(f'<!DOCTYPE html><html lang="zh" class="dark"><head>{head(title)}</head><body>{body}</body></html>')

def sec_h(t, c=''):
    return f'<div class="sec-h"><span class="t">{t}</span><span class="c">{c}</span></div>'
BJ = datetime.timezone(datetime.timedelta(hours=8))
def past_card(p):
    cnh = cn_of(p['h']); cna = cn_of(p['a']); fh = flag_of(p['h']); fa = flag_of(p['a'])
    try:
        bj = datetime.datetime.fromisoformat(p['date']).astimezone(BJ); ds = f'{bj.month}/{bj.day} {bj.hour:02d}:{bj.minute:02d}'
    except Exception: ds = p['date'][:10]
    teams = f'<span class="pteams">{fh} {cnh} <b class="psc">{p["gh"]}-{p["ga"]}</b> {cna} {fa}</span>'
    if not p.get('devig'):
        return (f'<div class="pcard"><div class="ptop">{teams}<span class="pres no">赛果</span></div>'
                f'<div class="pmeta"><span class="pchip">{ds}</span><span class="pval">（无赛前赔率,仅记录比分）</span></div></div>')
    pl = p.get('pl', 0); pos = pl >= 0; accent = '#CCFF00' if pos else 'rgba(255,255,255,.14)'
    badge = f'<span class="pres {"ok" if pos else "no"}">{"+" if pos else "−"}¥{abs(pl)}</span>'
    sc_tag = '<span class="pchip" style="border-color:rgba(204,255,0,.4);color:var(--lime)">比分也中</span>' if p.get('score2_hit') else ''
    return (f'<a class="pcard" style="border-left-color:{accent}" href="past_{p["fid"]}.html"><div class="ptop">{teams}{badge}</div>'
            f'<div class="pmeta"><span class="pchip">{ds}</span>{sc_tag}'
            f'<span class="pval">荐:<b>{p.get("wdl_txt","")}</b></span><span class="pmore">推演 ›</span></div></a>')

def build_past_detail(p):
    if not p.get('devig'): return
    fid = p['fid']; cnh = cn_of(p['h']); cna = cn_of(p['a']); fh = flag_of(p['h']); fa = flag_of(p['a'])
    gh, ga = p['gh'], p['ga']; d = p['devig']
    try:
        bj = datetime.datetime.fromisoformat(p['date']).astimezone(BJ); ds = f'{bj.month}/{bj.day} {bj.hour:02d}:{bj.minute:02d}'
    except Exception: ds = p['date'][:10]
    lh, la, grid = poisson_calc(d['home'], d['away'], None)
    okw = p.get('wdl_hit'); sc_ok = p.get('score2_hit')
    badge = '<span class="pres ok">✓ 胜负命中</span>' if okw else '<span class="pres no">✗ 胜负未中</span>'
    title = f'{cnh} vs {cna}'
    dv = lambda k: f'{d[k]*100:.0f}%'
    picks = p.get('picks', []); pk = ' / '.join(s.replace(':', ' : ') for s in picks)
    rescn = f'{cnh} 胜' if gh > ga else (f'{cna} 胜' if ga > gh else '平局')
    head_card = (f'<div class="glass" style="text-align:center">'
                 f'<div class="pd-flags">{fh} <span class="pd-sc">{gh} - {ga}</span> {fa}</div>'
                 f'<div class="pd-tn">{cnh} vs {cna}</div>'
                 f'<div style="margin:8px 0">{badge}</div>'
                 f'<div class="pd-meta">{ds}(北京) · 已结束 FT · {p["tier"]}</div></div>')
    pva = (f'<div class="glass">{sec_head("emoji_events","竞猜推荐 vs 实际")}'
           f'<table class="rectab">'
           f'<tr><td class="rt-l">胜负倾向</td><td class="rt-m">{p.get("wdl_txt","")}</td><td class="rt-r {"ok" if okw else "no"}">{"✓" if okw else "✗"}</td></tr>'
           f'<tr><td class="rt-l">推荐比分</td><td class="rt-m">{pk}</td><td class="rt-r {"ok" if sc_ok else "no"}">{"✓" if sc_ok else "✗"}</td></tr>'
           f'<tr><td class="rt-l">实际结果</td><td class="rt-m"><b>{rescn} · {gh} : {ga}</b></td><td class="rt-r"></td></tr>'
           f'</table>'
           f'<div class="vs-note">价值逻辑:{p["dir"]}(顺此产出推荐);胜负为主、2 个比分供参考。</div></div>')
    grid_card = f'<div class="glass">{sec_head("grid_view","模型推测比分分布 Top 6")}{scores_grid(lh, la, grid)}</div>'
    devig_card = (f'<div class="glass">{sec_head("balance","赛前市场预期(锐庄去水位)")}'
                  f'<div class="tp-pct"><span style="color:#CCFF00">{cnh} {dv("home")}</span>'
                  f'<span style="color:#8e9379">平 {dv("draw")}</span>'
                  f'<span style="color:#FF0055">{cna} {dv("away")}</span></div>'
                  f'<div class="tp-bar"><i style="flex:{max(d["home"]*100,3):.0f};background:#CCFF00"></i>'
                  f'<i style="flex:{max(d["draw"]*100,3):.0f};background:#3f465c"></i>'
                  f'<i style="flex:{max(d["away"]*100,3):.0f};background:#FF0055"></i></div>'
                  f'<div class="vs-note">这是赛前市场对该场的真实定价(去水位);模型据此反推价值方向,再与实际赛果对账。</div></div>')
    body = (f'<main>'
            f'<a class="back" href="index.html"><span class="material-symbols-outlined">chevron_left</span>返回目录</a>'
            f'<div style="height:12px"></div>'
            f'{head_card}{pva}{grid_card}{devig_card}'
            f'<div class="foot">价值≠会赢、看长期;赛前去水位自动判定方向,逐场仅供参考</div></main>')
    open(os.path.join(DOCS, f'past_{fid}.html'), 'w').write(
        f'<!DOCTYPE html><html lang="zh" class="dark"><head>{head(title)}</head><body>{body}</body></html>')

FID2SLUG = {v: k for k, v in AFID.items()}
def fetch_upcoming(hours=72, limit=6):
    """拉接下来 hours 小时内最近的 limit 场(未开赛),带赔率 + 自动价值方向,供「购彩参考」组票。"""
    fx = sorted(fetch_fixtures(), key=lambda f: f['fixture']['date']); out = []
    for f in fx:
        if f['fixture']['status']['short'] != 'NS': continue
        try: dt = datetime.datetime.fromisoformat(f['fixture']['date'])
        except Exception: continue
        hrs = (dt - now).total_seconds() / 3600
        if hrs <= 0 or hrs > hours: continue
        fid = f['fixture']['id']; bms = fetch_af_odds(fid)
        mw = af_h2h(af_bet(af_book(bms, PIN), 1)) if bms else None
        if not mw: mw = af_h2h(af_vals(bms, 1)) if bms else None
        if not mw: continue
        d = {k: round(v, 4) for k, v in devig(mw).items()}
        tier, fav, dirn, kind = value_call(d)
        h = f['teams']['home']['name']; a = f['teams']['away']['name']
        out.append({'fid': fid, 'cnh': cn_of(h), 'cna': cn_of(a), 'fh': flag_of(h), 'fa': flag_of(a),
                    'd': d, 'fav': fav, 'kind': kind,
                    'dc': af_pair(af_vals(bms, 12), ('Home/Draw', 'Home/Away', 'Draw/Away')) or {},
                    'tot': af_tot(af_bet(af_book(bms, PIN), 5)) or af_tot(af_vals(bms, 5)) or {},
                    'score': (af_score(bms) or {}).get('odds', {})})
        if len(out) >= limit: break
    return out
def _od(o, k, prob): v = o.get(k); return round(v, 2) if v else (round(1/prob, 2) if prob > 0 else 0.0)
def dc_pick(m):
    """按价值方向给出该场要买的双重机会(玩法标签, 赔率, 命中概率)。"""
    af = m['fav']; opp = 'away' if af == 'home' else 'home'
    if m['kind'] == 'anti_fav':   # 押"平 或 非热门不败"
        key = 'Draw/Away' if af == 'home' else 'Home/Draw'
        lbl = f'平或{m["cna"]}' if af == 'home' else f'{m["cnh"]}或平'; prob = m['d']['draw'] + m['d'][opp]
    else:                          # 押"热门 不败"(让球思路,稳)
        key = 'Home/Draw' if af == 'home' else 'Draw/Away'
        lbl = f'{m["cnh"]}或平' if af == 'home' else f'平或{m["cna"]}'; prob = m['d']['draw'] + m['d'][af]
    return lbl, _od(m['dc'], key, prob), prob
def leg_pick(m):
    """价值方向的可串玩法:逆向场=双重机会(平或非热门,有赔率);砍屠杀场=小球(符合价值且赔率合理)。"""
    af = m['fav']; opp = 'away' if af == 'home' else 'home'
    if m['kind'] == 'anti_blowout':
        g = poisson_calc(m['d']['home'], m['d']['away'], None)[2]
        prob = sum(p for s, p in g.items() if sum(map(int, s.split('-'))) <= 2)
        return '小球 ≤2 球', _od(m['tot'], 'under', prob), prob
    key = 'Draw/Away' if af == 'home' else 'Home/Draw'
    lbl = f'平或{m["cna"]}' if af == 'home' else f'{m["cnh"]}或平'; prob = m['d']['draw'] + m['d'][opp]
    return lbl, _od(m['dc'], key, prob), prob
def build_tickets(up):
    if not up: return ''
    def card(cls, tag, stake, legs, ret, prob, note):
        body = ''.join(f'<div class="tk-leg"><span class="tk-vs">{m["fh"]} {m["cnh"]} vs {m["cna"]} {m["fa"]}</span>'
                       f'<span class="tk-bet">{bet} <b>@{od}</b></span></div>' for m, bet, od in legs)
        ph = f'命中约 {prob*100:.0f}%' if prob >= 0.01 else f'命中约 {prob*100:.1f}%'
        mult_x = f'{ret/stake:.1f}x' if stake else '—'
        return (f'<div class="tk {cls}"><div class="tk-top"><span class="tk-tag">{tag}</span>'
                f'<span class="tk-stake">全中倍数 <b>{mult_x}</b></span></div>{body}'
                f'<div class="tk-foot">{ph} · {note}</div></div>')
    # 🟡 平衡:3 串 1(价值方向双重机会)
    three = up[:3]; legs = []; mult = 1.0; cp = 1.0
    for m in three:
        lb, od, pr = leg_pick(m); legs.append((m, lb, od)); mult *= od; cp *= pr
    g_bal = card('amber', '🟡 平衡 · 3 串 1', 10, legs, round(10*mult), cp, '三场价值方向串关,博中等回报') if len(three) >= 2 else ''
    # 🔴 博胆:2 场比分串
    two = up[:2]; slegs = []; smult = 1.0; sprob = 1.0
    for m in two:
        picks, _ = value_picks(m['d'], m['kind'], m['fav']); sc = picks[0]
        g = poisson_calc(m['d']['home'], m['d']['away'], None)[2]; pr = g.get(sc.replace(':', '-'), 0.05)
        od = _od(m['score'], sc.replace(':', '-'), pr); slegs.append((m, f'比分 {sc}', od)); smult *= od; sprob *= pr
    g_bold = card('red', '🔴 博胆 · 比分串', 5, slegs, round(5*smult), sprob, '押被低估的平局/砍屠杀,小钱搏大') if len(two) >= 2 else ''
    warn = '<div class="tk-warn">⚠️ 仅供参考娱乐 · 理性购彩 · 量力而行 · 未成年人禁止购彩。竞彩返还率低,长期期望为负,切勿当作赚钱工具。</div>'
    return f'<div class="tkwrap">{g_bal}{g_bold}{warn}</div>'
def line_row(f, pmap, cur_fid, prob_map):
    """时间线单行:已结束=比分+盈亏(可点复盘);精选未来=⭐可点详情;其余=赛程行。"""
    fid = f['fixture']['id']; st = f['fixture']['status']['short']
    h = f['teams']['home']['name']; a = f['teams']['away']['name']
    try: dt = datetime.datetime.fromisoformat(f['fixture']['date']); bj = dt.astimezone(BJ)
    except Exception: return ''
    tm = f'{bj.hour:02d}:{bj.minute:02d}'
    cc = ' cur' if fid == cur_fid else ''; ida = ' id="cur"' if fid == cur_fid else ''
    th = f'{flag_of(h)} {cn_of(h)}'; ta = f'{cn_of(a)} {flag_of(a)}'
    # 已结束:保持紧凑行(比分 + 盈亏,可点复盘)
    if st in ('FT', 'AET', 'PEN'):
        gh, ga = f['goals']['home'], f['goals']['away']
        teams = f'<span class="tl-tt">{th} <span class="tl-sc">{gh}-{ga}</span> {ta}</span>'
        p = pmap.get(str(fid))
        if p and p.get('wdl_hit') is not None:
            hit = p['wdl_hit']
            lbl = '中' if hit else '未中'
            lbl_style = 'color:var(--lime);font-weight:800' if hit else 'color:var(--sec);opacity:.6'
            return (f'<a class="tl-row done{cc}"{ida} href="past_{fid}.html"><span class="tl-tm">{tm}</span>'
                    f'{teams}<span class="tl-pl" style="{lbl_style}">{lbl}</span></a>')
        return f'<div class="tl-row done{cc}"{ida}><span class="tl-tm">{tm}</span>{teams}<span class="tl-pl" style="color:var(--sec)">完场</span></div>'
    # 未进行 / 进行中:大气卡(增加高度,留分析占位)
    live = st not in ('NS',)
    hrs = (dt - now).total_seconds() / 3600
    when = f'{tm} 北京 · 进行中' if live else f'{tm} 北京 · 距开赛 {hrs:.0f}h'
    slug = FID2SLUG.get(fid)
    tag = ''
    if slug and prob_map.get(fid):           # 精选场:展示去水位概率行 + 比例条
        pcfg, pd = prob_map[fid]; bottom = f'{probrow(pd, pcfg)}{minibar(pd)}'
    elif slug:                               # 精选场但暂无采样数据
        bottom = '<div class="fxbig-cta">⭐ 查看竞猜方案<span class="material-symbols-outlined">arrow_forward</span></div>'
    else:                                    # 无分析场:占位待补
        bottom = '<div class="fxbig-ph"><span class="material-symbols-outlined">hourglass_empty</span>竞猜分析筹备中,赛前补充</div>'
    inner = (f'<div class="fxbig-top"><span class="fxbig-tm"><span class="material-symbols-outlined">schedule</span>{when}</span>{tag}</div>'
             f'<div class="fxbig-vs"><span class="fxbig-team">{th}</span><span class="fxbig-mid">VS</span><span class="fxbig-team">{ta}</span></div>'
             f'{bottom}')
    if slug: return f'<a class="fxbig star{cc}"{ida} href="{slug}.html">{inner}</a>'
    return f'<div class="fxbig{cc}"{ida}>{inner}</div>'

def build_index(items):
    past = build_past()
    for p in past: build_past_detail(p)
    pmap = {str(p['fid']): p for p in past}
    scored = [p for p in past if p.get('devig')]
    ntot = len(scored); nwin = sum(1 for p in scored if p.get('wdl_hit'))
    invest = ntot * 100; won = sum(p.get('won', 0) for p in scored); pl = won - invest
    roi = round(pl/invest*100) if invest else 0
    pcls = 'pos' if pl >= 0 else 'neg'; sign = '+' if pl >= 0 else '−'
    track = (f'<div class="track">'
             f'<div class="pnl {pcls}">ROI {sign}{abs(roi)}%<small></small></div>'
             f'<div class="pnl-row"><span>本金 ¥{invest}</span><span>收回 ¥{won}</span>'
             f'<span>净盈亏 {sign}¥{abs(pl)}</span><span>胜负中 {nwin}/{ntot}</span></div></div>')
    # ---------- 本期购彩参考(嵌入时间线过去/未来分界处)----------
    up = fetch_upcoming(hours=48, limit=3)
    tickets = build_tickets(up)
    ticket_sec = f'<div id="tickets">{sec_h("今日串关推荐", "最近 3 场 · 2 注串关")}{tickets}</div>' if tickets else ''
    # ---------- 统一时间线(全部小组赛按时间从上到下)----------
    prob_map = {}  # 精选场 fid → (cfg, 最新去水位),供大气卡底部展示概率条
    for cfg, rows, rich in items:
        afid = AFID.get(cfg['slug'])
        if afid and rows: prob_map[afid] = (cfg, rows[-1]['devig'])
    fx = sorted(fetch_fixtures(), key=lambda f: f['fixture']['date'])
    cur_fid = next((f['fixture']['id'] for f in fx if f['fixture']['status']['short'] not in ('FT', 'AET', 'PEN')), None)
    RMAP = {'Group Stage - 1': ('r1', '小组赛 · 第 1 轮'), 'Group Stage - 2': ('r2', '小组赛 · 第 2 轮'), 'Group Stage - 3': ('r3', '小组赛 · 第 3 轮')}
    tl = ''; cur_round = None; cur_day = None; crossed = False
    for f in fx:
        st = f['fixture']['status']['short']
        # 在"最后一场已结束"→"第一场未开赛"边界插入串关推荐
        if not crossed and st not in ('FT', 'AET', 'PEN'):
            tl += ticket_sec; crossed = True
        rd = f['league']['round']; rid, rname = RMAP.get(rd, ('rx', rd))
        if rd != cur_round:
            tl += f'<div class="round-head" id="{rid}"><span class="material-symbols-outlined">sports_soccer</span>{rname}</div>'; cur_round = rd; cur_day = None
        try: bj = datetime.datetime.fromisoformat(f['fixture']['date']).astimezone(BJ)
        except Exception: continue
        wd = '一二三四五六日'[bj.weekday()]; day = f'{bj.month}/{bj.day} 周{wd}'
        if day != cur_day: tl += f'<div class="tl-day">{day}</div>'; cur_day = day
        tl += line_row(f, pmap, cur_fid, prob_map)
    if not crossed: tl += ticket_sec  # 全部比赛已结束时追加到末尾
    filt = '<div class="filt"><a href="#r1">第 1 轮</a><a href="#r2">第 2 轮</a><a href="#r3">第 3 轮</a></div>'
    js = ('<script>(function(){if(location.hash)return;'
          'var t=document.getElementById("tickets");'
          'if(t)setTimeout(function(){t.scrollIntoView({block:"start"});},80);})();</script>')
    bt = crowd_backtest_block()
    body = (f'<main>'
            f'<div style="height:12px"></div>{track}{filt}{tl}{bt}'
            f'<div class="foot">API-Football Pro · GitHub Actions</div></main>{js}')
    open(os.path.join(DOCS, 'index.html'), 'w').write(f'<!DOCTYPE html><html lang="zh" class="dark"><head>{head("世界杯赔率追踪")}</head><body>{body}</body></html>')

items = []
for cfg in MATCHES:
    rich = process(cfg); rows = load_rows(cfg['slug'])
    build_detail(cfg, rows, rich); items.append((cfg, rows, rich))
build_index(items)
print('完成', len(items), '场')
