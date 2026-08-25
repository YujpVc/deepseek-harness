#!/usr/bin/env python3
"""用 pptfast 生成《电动车选购指南》deck 项目。"""
import json, os, shutil
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, 'output', 'img')

def p(n): return os.path.join(IMG, n)

ASSETS = {
    'charging': p('ev_electric_car_charging.jpg'),
    'station': p('ev_ev_charging_station.jpg'),
    'battery': p('ev_electric_vehicle_battery.jpg'),
    'dashboard': p('ev_electric_car_interior_dashboard.jpg'),
    'tesla': p('ev_tesla_electric_car.jpg'),
    'roadtrip': p('ev_electric_car_road_trip.jpg'),
    'homecharge': p('ev_ev_home_charging.jpg'),
    'scooter': p('ev_electric_scooter_city.jpg'),
}

def prose(t): return {"type": "paragraph", "text": t}
def bullets(items, style="default"): return {"type": "bullets", "items": items, "style": style}
def banner(text): return {"type": "verdict_banner", "text": text, "tone": "positive"}
def img(aid, caption): return {"type": "image", "asset_id": aid, "fit": "cover", "caption": caption}
def kpi(items): return {"type": "kpi_cards", "items": items}

PAGES = [
    # 1 封面
    {"id":"p01","type":"cover","heading":"电动车选购指南","subheading":"新手买车，一篇讲清续航、充电、预算与试驾"},
    # 2 目录
    {"id":"p02","type":"content","heading":"这份指南会讲什么","components":[
        prose("买电动车和买油车逻辑不同：续航、充电、电池质保、保值率，都是新的决策变量。这份指南按「先想清楚 → 再比参数 → 最后试驾下单」的顺序，把关键点一次讲清。"),
        bullets(["为什么现在买电动车","续航、电池与充电怎么选","预算、车型与品牌怎么比","试驾、保值与避坑清单"], "numbered"),
    ]},
    # 3 为什么现在买（image-split 左图）
    {"id":"p03","type":"content","heading":"为什么现在买电动车","layout":"image-split","image_side":"left","components":[
        img("roadtrip","电车的用车成本，远低于油车"),
        prose("如果你一年开 1.5 万公里，电车每公里电费约 0.1 元，油车约 0.6 元——一年能省下七八千。加上免购置税、不限行（多数城市）和更平顺的驾驶体验，对家用代步来说优势明显。"),
        bullets(["用车成本低：每公里约 0.1 元","免购置税、多数城市不限行","驾驶平顺安静，智能化程度高"]),
        banner("家用代步、通勤为主，现在买电车很划算。"),
    ]},
    # 4 续航与电池（kpi_cards）
    {"id":"p04","type":"content","heading":"续航与电池，重点看这四点","components":[
        prose("不要只看官方续航，真实续航通常打 7–8 折。重点看电池类型、快充速度和是否支持对外放电，这些才决定你日常用起来方不方便。"),
        kpi([
            {"value":"500", "unit":"km", "label":"日常够用续航", "icon":"battery-charging"},
            {"value":"30", "unit":"分", "label":"快充到 80%", "icon":"zap"},
            {"value":"7.5", "unit":"折", "label":"冬季续航", "icon":"snowflake"},
        ]),
        banner("按「实际续航 = 标称 × 0.75」来预估，别被宣传数字误导。"),
    ]},
    # 5 充电方式（image-top + comparison）
    {"id":"p05","type":"content","heading":"三种充电方式，怎么选","layout":"image-top","components":[
        img("homecharge","有家充，是买电车的最大底气"),
        prose("有固定车位和家充，电车的日常体验会好很多——晚上插上，第二天满电出发，成本最低。没有家充，就要依赖公共快充桩。"),
        {"type":"comparison","columns":["家充","公共快充"],"rows":[
            {"label":"速度","cells":["慢，一夜充满","快，30分钟"]},
            {"label":"成本","cells":["约 0.3 元/度","1–1.8 元/度"]},
            {"label":"适合","cells":["有固定车位","赶时间"]}
        ]},
        banner("能装家充优先装，它是电车体验的关键前提。"),
    ]},
    # 6 预算（kpi_cards）
    {"id":"p06","type":"content","heading":"预算：别只看车价","components":[
        prose("裸车价之外，还有保险、充电桩安装、停车和电池租赁（部分品牌）等费用。用「全生命周期成本」来算，才是真实预算。"),
        kpi([
            {"value":"10–15", "unit":"万", "label":"主流价位", "icon":"wallet"},
            {"value":"5000+", "unit":"元", "label":"首年保险", "icon":"shield"},
            {"value":"0", "unit":"元", "label":"购置税", "icon":"badge-check"},
            {"value":"3–8", "unit":"千元", "label":"家充桩安装", "icon":"plug"},
        ]),
        banner("把保险、充电桩、停车都算进去，才不会被「低车价」误导。"),
    ]},
    # 7 车型选择（image-split 左图）
    {"id":"p07","type":"content","heading":"车型：按你的场景选","layout":"image-split","image_side":"left","components":[
        img("tesla","轿车/SUV/微型车，各有各的合适场景"),
        prose("城市通勤、家里第二辆车，微型或紧凑轿车够用又便宜；经常全家出行、要装大件，选 SUV；纯粹一个人上下班，微型车停车方便、成本最低。"),
        bullets(["城市通勤/第二辆车 → 紧凑轿车","全家出行/装大件 → SUV","一个人代步 → 微型车"]),
        banner("先想清楚「平时几个人坐、跑多远」，再决定车型。"),
    ]},
    # 8 品牌对比（comparison）
    {"id":"p08","type":"content","heading":"主流品牌，各有什么特点","components":[
        prose("不推荐具体品牌，只讲各家的鲜明特点，方便你按需求对号入座："),
        {"type":"comparison","columns":["类型","特点","适合谁"],"rows":[
            {"label":"新势力","cells":["智能化/服务好","看重智驾与体验"]},
            {"label":"传统大厂","cells":["渠道广/保值稳","求稳、图省心"]},
            {"label":"性价比","cells":["配置高/价格低","预算有限"]}
        ]},
        banner("没有最好的品牌，只有最匹配你需求的选择。"),
    ]},
    # 9 试驾（image-split 右图）
    {"id":"p09","type":"content","heading":"试驾，重点试这几样","layout":"image-split","image_side":"right","components":[
        img("dashboard","屏幕再炫，不如坐进去开一圈"),
        prose("别只坐展厅看参数，一定要开出去试。重点感受：低速走走停停的平顺度、动能回收的拖拽感、车内静音，以及车机是否顺手。"),
        bullets(["低速走走停停是否平顺","动能回收拖拽感能不能适应","静音与底盘舒适度","车机卡不卡、导航好不好用"]),
        banner("试驾就一句话：当自己每天上下班那样开。"),
    ]},
    # 10 保值与质保（bullets）
    {"id":"p10","type":"content","heading":"保值率与电池质保，别忽略","components":[
        prose("电车保值率整体低于油车，但电池质保是更关键的长期保障。购车前问清三电质保的具体条款：年限、里程、是否限制首任车主、衰减到多少算免费更换。"),
        bullets(["三电质保：主流 8 年或 15 万公里","问清是否限首任车主（过户会失效）","衰减到 70% 以下是否免费换电","电池租赁方案（如换电）要算总账"]),
        banner("质保条款写进合同，口头承诺不算数。"),
    ]},
    # 11 常见误区（bullets）
    {"id":"p11","type":"content","heading":"这些误区，新手最容易踩","components":[
        prose("买电车前，先避开这五个坑："),
        bullets(["只看标称续航，不看真实打折","以为快充免费又随时有（公共桩要排队、收费）","忽略电池衰减和质保条款","跟风买顶配，用不上的配置白花钱","没提前确认小区能不能装家充"], "checklist"),
        banner("多问一句、多查一步，能省下不少冤枉钱。"),
    ]},
    # 12 购买流程（steps）
    {"id":"p12","type":"content","heading":"从决定到提车，五步走","components":[
        prose("把流程理清，买电车不复杂："),
        {"type":"steps","items":[
            {"title":"定预算","text":"算清全生命周期成本"},
            {"title":"定场景","text":"几个人坐、跑多远、装不装家充"},
            {"title":"圈车型","text":"按场景筛 2–3 款"},
            {"title":"去试驾","text":"当日常开，感受平顺与静音"},
            {"title":"比权益","text":"质保、补贴、交付周期再下单"}
        ]},
        banner("一步一步来，别被销售节奏带着走。"),
    ]},
    # 13 总结（bullets）
    {"id":"p13","type":"content","heading":"一句话总结","components":[
        prose("买电动车的核心逻辑：先确认能不能装家充，再按真实续航和用车场景选车型，最后把质保和保险算进总价。适合自己，比参数好看更重要。"),
        bullets(["家充是前提，能装优先装","续航按 7.5 折估，别信宣传","预算算全生命周期，不只车价","质保写进合同，试驾当日常开"]),
        banner("适合自己的车，就是最好的车。"),
    ]},
    # 14 结束
    {"id":"p14","type":"ending","heading":"选到心仪的车","subheading":"愿你的第一台电车，开得省心、用得放心"},
]

OUT = os.path.join(BASE, 'ev_pptfast')
ASSET_DIR = os.path.join(OUT, 'assets')
os.makedirs(os.path.join(OUT, 'pages'), exist_ok=True)
os.makedirs(ASSET_DIR, exist_ok=True)

for aid, src in ASSETS.items():
    if os.path.exists(src):
        im = Image.open(src).convert('RGB')
        im.save(os.path.join(ASSET_DIR, aid + '.jpg'), 'JPEG', quality=92)

spec = {
    "version": "1",
    "filename": "ev.pptx",
    "theme": "consulting",
    "narrative": {"strategy": "instructional", "pacing": "dense", "audience": "public"},
    "seed": 20260821,
    "pages": [{"id": pg["id"], "type": pg["type"], "heading": pg.get("heading","")} for pg in PAGES],
}
json.dump(spec, open(os.path.join(OUT, 'deck.spec.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

for pg in PAGES:
    page = {}
    for k in ('layout', 'image_side', 'subheading', 'components'):
        if pg.get(k) is not None:
            page[k] = pg[k]
    json.dump(page, open(os.path.join(OUT, 'pages', pg['id'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print("已生成 deck 项目:", OUT, "| 页数:", len(PAGES))
