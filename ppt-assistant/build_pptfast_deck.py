#!/usr/bin/env python3
"""用 pptfast 语义 IR 生成《温柔一点，好不好？》情书 deck（加厚内容版）。"""
import json, os, shutil
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, 'output', 'img')

def p(n): return os.path.join(IMG, n)

ASSETS = {
    'envelope': p('rom3_love_letter_envelope.jpg'),
    'pen': p('rom3_fountain_pen_writing.jpg'),
    'heart': p('rom3_heart_shape.jpg'),
    'candle': p('rom3_candle_light.jpg'),
    'roses': p('rom3_pink_roses.jpg'),
    'hands': p('rom3_couple_holding_hands.jpg'),
    'coffee': p('rom3_two_coffee_mugs.jpg'),
    'blanket': p('rom3_cozy_blanket.jpg'),
    'morning': p('rom3_soft_morning_light_window.jpg'),
    'hands2': p('rom4_holding_hands_together.jpg'),
    'beach': p('rom4_sunset_beach_warm.jpg'),
    'fireplace': p('rom4_cozy_fireplace.jpg'),
    'bouquet': p('rom4_flowers_bouquet_soft.jpg'),
    'silhouette': p('rom4_couple_silhouette_sunset.jpg'),
    'sweater': p('rom4_warm_sweater_knit.jpg'),
    'dinner': p('rom4_candle_dinner_table.jpg'),
    'marshmallow': p('rom4_marshmallow_hot_drink.jpg'),
    'lantern': p('rom4_lantern_warm_glow.jpg'),
    'chocolate': p('rom4_chocolate_hearts.jpg'),
    'sunset': p('rom3_warm_sunset_sky.jpg'),
}

def prose(t): return {"type": "paragraph", "text": t}
def bullets(items, style="default"): return {"type": "bullets", "items": items, "style": style}
def banner(text): return {"type": "verdict_banner", "text": text, "tone": "positive"}
def img(aid, caption): return {"type": "image", "asset_id": aid, "fit": "cover", "caption": caption}

PAGES = [
    # 1 封面
    {"id":"p01","type":"cover","heading":"温柔一点，好不好？","subheading":"写给我最爱的你 · 一些藏在心里很久的话"},
    # 2 目录
    {"id":"p02","type":"content","heading":"把这些话，慢慢讲给你听","components":[
        prose("这是我憋了很久、一直想对你说的话。不是要讲道理，也不是要争对错——只是有些心里话，当面总怕说不好，所以写成了这几页，想请你安安静静地听完。"),
        bullets(["第一章 · 写在前面","第二章 · 男生也需要温柔","第三章 · 你可以这样温柔待我","第四章 · 一起走下去"], "divided"),
        banner("这不是一份控诉书，而是一封情书。"),
    ]},
    # 3 引言
    {"id":"p03","type":"content","heading":"这不是一份控诉书，而是一封情书","layout":"quote-stage","components":[
        {"type":"callout","variant":"tip","text":"做这几十页，不是要责怪你，也不是想翻旧账。只是有些话，当面总怕说不好，也怕一激动就变了味。希望你慢慢读，慢慢听。"},
    ]},
    # 4 为什么这种方式（image-split 左图）
    {"id":"p04","type":"content","heading":"为什么选择这种方式","layout":"image-split","image_side":"left","components":[
        img("pen","把心里话，一笔一画写给你"),
        prose("有些话，当面说不出口——怕一激动语气就变了味，怕你误会我真正想说的。写下来，我能想清楚了再说，你也能安安静静地读，不用急着反驳，也不用急着打断我。"),
        bullets(["写下来，是想让你认真地听一次","先听完，我们再慢慢聊","这不是逃避沟通，而是想让沟通更温柔"]),
        banner("这不是逃避沟通，而是想让沟通更温柔。"),
    ]},
    # 5 男生不是铁打（image-top）
    {"id":"p05","type":"content","heading":"男生，不是铁打的","layout":"image-top","components":[
        img("blanket","我也会累，也会想被抱一抱"),
        prose("从小到大，我们被教着要「扛得住」：男儿有泪不轻弹，男子汉要坚强一点。于是我们习惯了自己咽下，很少在你面前喊累。可真相是，我也会累、会委屈、会想哭——只是怕你担心，也怕你觉得我不够好。"),
        bullets(["「男儿有泪不轻弹」——所以我很少说","我也会累、会委屈、会想哭","只是怕你担心，也怕你觉得我不够好"]),
        banner("坚强是他的盔甲，温柔才是他的软肋。"),
    ]},
    # 6 扛下的事（image-split 左图）
    {"id":"p06","type":"content","heading":"他默默扛下的那些事","layout":"image-split","image_side":"left","components":[
        img("coffee","加班的夜里，也会想家"),
        prose("工作上的项目催得紧、要求也高，加班的夜里还在想怎么做得更好；生活里房子、车子、未来的规划，他总想给你更好的生活。他很少主动说这些，怕你跟着一起焦虑。"),
        bullets(["工作：项目催得紧，加班到深夜","生活：房子车子，想给你安稳","偶尔挫败，也会偷偷怀疑自己"]),
        banner("他的沉默不是冷漠，而是在独自消化。"),
    ]},
    # 7 爱在细节（image-split 右图）
    {"id":"p07","type":"content","heading":"他的爱，藏在细节里","layout":"image-split","image_side":"right","components":[
        img("hands2","爱，都在行动里"),
        prose("他不声张，却记得你随口提过的小事；加班路上给你带一杯热饮，下雨天把伞悄悄倾向你。他很少把「我爱你」挂在嘴边，却会在你冷时把外套披给你，在你累时默默接过家务。"),
        bullets(["记得你随口提过的小事","下雨天把伞悄悄倾向你","把外套披给你、默默接过家务"]),
        banner("他的爱不常挂在嘴边，却都落在行动里。"),
    ]},
    # 8 两种说法（comparison 全宽）
    {"id":"p08","type":"content","heading":"同一句话，两种说法","components":[
        prose("同一件事，换个语气，结果就完全不一样。左边的话会把人推开，右边的话会把人拉近。我知道你没有恶意，只是有时候，话说出口就冷了。"),
        {"type":"comparison","columns":["冷硬的说法","温柔的说法"],"rows":[
            {"label":"问候","cells":["「你又怎么了？」","「今天有点累吧？」"]},
            {"label":"争执","cells":["「随便你」","「我在呢」"]},
            {"label":"事后","cells":["「早说过了」","「一起想办法」"]}
        ]},
        banner("同样的事，换一种语气，结果完全不同。"),
    ]},
    # 9 真正在意（image-split 右图）
    {"id":"p09","type":"content","heading":"他真正在意的","layout":"image-split","image_side":"right","components":[
        img("hands","他缺的不是道理，而是被理解"),
        prose("他不要你事事完美，不需要你永远不发脾气、每句话都对。他真正要的，从来不多：气头上也给他留一点余地，他的付出能被看见，他难过时，你愿意抱抱他。"),
        bullets(["不要你完美，只要被好好对待","气头上给他留一点余地","付出能被看见，难过时有个抱抱"]),
        banner("他缺的不是道理，而是被理解、被在乎。"),
    ]},
    # 10 温柔不是示弱（quote-stage）
    {"id":"p10","type":"content","heading":"温柔，不是示弱","layout":"quote-stage","components":[
        {"type":"callout","variant":"tip","text":"把爱放在情绪之上——这需要很大的内心力量。能温柔的人，从不软弱；温柔让彼此都舒服，是双向的滋养。"},
    ]},
    # 11 你温柔的样子（image-split 左图）
    {"id":"p11","type":"content","heading":"你温柔的样子，真的很好看","layout":"image-split","image_side":"left","components":[
        img("roses","你温柔的样子，是我眼里最美的风景"),
        prose("温柔是一种气质，比外表更长久，让人如沐春风，想靠近、想珍惜。我记忆里最珍贵的画面，是你轻声说话时眼里的光，是你耐心听我说话的样子——都让我越看越喜欢。"),
        bullets(["它比外表更长久","让人如沐春风、想靠近","你眼里的光，我都记着"]),
    ]},
    # 12 情绪四步（steps）
    {"id":"p12","type":"content","heading":"当情绪上来的时候","components":[
        prose("情绪一上来，最容易说出伤人的话。下次可以试试这四步：先停三秒、换种说法、不翻旧账、给个台阶。"),
        {"type":"steps","items":[
            {"title":"先停三秒","text":"话到嘴边，先深呼吸"},
            {"title":"换种说法","text":"把指责换成「我有点难过」"},
            {"title":"不翻旧账","text":"就事论事，只谈眼前"},
            {"title":"给个台阶","text":"吵完别冷战，抱一下就好"}
        ]},
        banner("情绪来的那一刻，温柔就是最好的刹车。"),
    ]},
    # 13 夸奖（image-split 左图）
    {"id":"p13","type":"content","heading":"他也想被你夸一夸","layout":"image-split","image_side":"left","components":[
        img("bouquet","你的一句夸奖，抵得过千军万马"),
        prose("男生，同样需要肯定。一句「你真棒」能让他开心一整天，你的认可，是他最珍贵的勋章。不妨多夸夸他：「谢谢你今天记得帮我带伞」「你今天真帅」「有你在，我安心多了」。"),
        bullets(["一句「你真棒」能让他开心一整天","你的认可，是他最珍贵的勋章","被在乎的人夸，最有力量"]),
        banner("你的一句夸奖，抵得过千军万马。"),
    ]},
    # 14 玻璃心（image-split 右图）
    {"id":"p14","type":"content","heading":"他的「玻璃心」时刻","layout":"image-split","image_side":"right","components":[
        img("lantern","这些时刻，他最需要你的温柔"),
        prose("他也有脆弱的时刻：努力了很久，却被一句「就这」否定；加班攒钱规划未来，却没人问一句「你累不累」；累到说不出话时，只想安安静静地靠一靠。"),
        bullets(["被否定时，他会怀疑自己","努力不被看见，其实很累","累到说不出话，只想靠一靠"]),
        banner("这些时刻，他比任何时候都更需要你的温柔。"),
    ]},
    # 15 互相滋养（image-split 右图）
    {"id":"p15","type":"content","heading":"好的关系，是互相滋养","layout":"image-split","image_side":"right","components":[
        img("hands2","温柔是相互的，爱也是"),
        prose("你温柔待我，我更想加倍对你好，你对我的好，我会记一辈子；我也会温柔待你，更努力、更体贴，更懂得疼你、护着你。温柔从来不是单方面的。"),
        bullets(["你温柔待我，我更想加倍对你好","你对我的好，我会记一辈子","我也会更努力、更体贴"]),
        banner("温柔从来不是单方面的。"),
    ]},
    # 16 守护（image-split 左图）
    {"id":"p16","type":"content","heading":"你，也是我最想守护的人","layout":"image-split","image_side":"left","components":[
        img("silhouette","想和你，走到最后"),
        prose("说这些，不是只要求你付出。我也会改变、会成长，会努力做更好的自己。你永远是我最想守护的人——你的小脾气其实很可爱，我只想和你好好在一起，把日子过成我们想要的样子。"),
        bullets(["我也会改变、会成长","你的小脾气，其实也很可爱","把日子过成我们想要的样子"]),
        banner("我要的，是两个人一起变好。"),
    ]},
    # 17 心愿（image-split 右图）
    {"id":"p17","type":"content","heading":"一个很小的心愿","layout":"image-split","image_side":"right","components":[
        img("sunset","你多温柔一分，我就多爱你十分"),
        prose("在我累的时候，少一点指责，多一点抱抱，不问「怎么又这样」，问一句「你还好吗」；在我失落的时候，少一点比较，多一点鼓励，不和别人比，只和我一起往前走。"),
        bullets(["累的时候：多一点抱抱，问「你还好吗」","失落的时候：多一点鼓励","不和别人比，只和我一起走"]),
        banner("你多温柔一分，我就多爱你十分。"),
    ]},
    # 18 约定（comparison 全宽）
    {"id":"p18","type":"content","heading":"我们的约定","components":[
        prose("我答应你：我会更懂你、更体贴，多表达、多陪伴，把你放在心尖上。也请你答应我：累的时候多给我一点温柔，难过的时候多给我一点安慰。"),
        {"type":"comparison","columns":["我答应你","也请你答应我"],"rows":[
            {"label":"我会","cells":["更懂你","多一点温柔"]},
            {"label":"我会","cells":["多陪伴","多一点安慰"]},
            {"label":"一起","cells":["放在心上","好好走下去"]}
        ]},
        banner("这是我们的约定，拉勾不许变。"),
    ]},
    # 19 感谢（image-split 左图）
    {"id":"p19","type":"content","heading":"谢谢你一直以来的好","layout":"image-split","image_side":"left","components":[
        img("heart","我不是要一个完美的你，只要真实的你"),
        prose("谢谢你，在我最难的时候都在；谢谢你，包容我的粗心和小毛病；谢谢你，让我知道自己被好好爱着，也让我更想好好爱你。我不是要一个完美的你，我只要眼前真实的你。"),
        bullets(["谢谢你的陪伴：我最难的时候，你都在","谢谢你的包容：包容我的小毛病","谢谢你的爱：让我更想好好爱你"]),
        banner("我不是要一个完美的你，我只要眼前真实的你。"),
    ]},
    # 20 结束
    {"id":"p20","type":"ending","heading":"谢谢你，亲爱的","subheading":"我会用一辈子，温柔地爱你 · 也请你，温柔待我"},
]

OUT = os.path.join(BASE, 'gentle_love_pptfast')
ASSET_DIR = os.path.join(OUT, 'assets')
os.makedirs(os.path.join(OUT, 'pages'), exist_ok=True)
os.makedirs(ASSET_DIR, exist_ok=True)

for aid, src in ASSETS.items():
    if os.path.exists(src):
        im = Image.open(src).convert('RGB')
        im.save(os.path.join(ASSET_DIR, aid + '.jpg'), 'JPEG', quality=92)

spec = {
    "version": "1",
    "filename": "gentle_love.pptx",
    "theme": "bloom",
    "narrative": {"strategy": "storytelling", "pacing": "dense", "audience": "public"},
    "seed": 20260818,
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
