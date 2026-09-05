#!/usr/bin/env python3
"""Generate HSK lesson 16 data (daily routine / work day)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hsk_gen_lib import emit_lesson

VOCAB = [
    {"id": "zhiyuan", "hanzi": "职员", "pinyin": "zhíyuán", "vi": "nhân viên", "en": "employee / staff", "pos": "noun",
     "examples": [{"zh": "你的公司有多少个职员？", "py": "Nǐ de gōngsī yǒu duōshao ge zhíyuán?", "vi": "Công ty bạn có bao nhiêu nhân viên?", "en": "How many employees does your company have?"}]},
    {"id": "dian", "hanzi": "点", "pinyin": "diǎn", "vi": "giờ", "en": "o'clock", "pos": "noun",
     "examples": [{"zh": "现在几点了？", "py": "Xiànzài jǐ diǎn le?", "vi": "Bây giờ mấy giờ rồi?", "en": "What time is it now?"}]},
    {"id": "qichuang", "hanzi": "起床", "pinyin": "qǐchuáng", "vi": "thức dậy", "en": "to get up", "pos": "verb",
     "examples": [{"zh": "你几点起床？", "py": "Nǐ jǐ diǎn qǐchuáng?", "vi": "Mấy giờ bạn thức dậy?", "en": "What time do you get up?"}]},
    {"id": "chuang", "hanzi": "床", "pinyin": "chuáng", "vi": "giường (张)", "en": "bed", "pos": "noun",
     "examples": [{"zh": "我打算给女儿买一张新床。", "py": "Wǒ dǎsuàn gěi nǚ'ér mǎi yì zhāng xīn chuáng.", "vi": "Tôi dự định mua cho con gái một cái giường mới.", "en": "I plan to buy my daughter a new bed."}]},
    {"id": "mei", "hanzi": "每", "pinyin": "měi", "vi": "mỗi", "en": "every", "pos": "prefix",
     "match": ["每天", "每个", "每次", "每年", "每个月"],
     "examples": [{"zh": "每天我六点起床。", "py": "Měi tiān wǒ liù diǎn qǐchuáng.", "vi": "Mỗi ngày tôi thức dậy lúc 6 giờ.", "en": "Every day I get up at six."}]},
    {"id": "ranhou", "hanzi": "然后", "pinyin": "ránhòu", "vi": "sau đó", "en": "then / after that", "pos": "conj",
     "examples": [{"zh": "我六点起床，然后骑车去学校。", "py": "Wǒ liù diǎn qǐchuáng, ránhòu qí chē qù xuéxiào.", "vi": "Sáu giờ tôi thức dậy, sau đó đạp xe đến trường.", "en": "I get up at six, then ride to school."}]},
    {"id": "gongyuan", "hanzi": "公园", "pinyin": "gōngyuán", "vi": "công viên", "en": "park", "pos": "noun",
     "examples": [{"zh": "我打算骑自行车去公园。", "py": "Wǒ dǎsuàn qí zìxíngchē qù gōngyuán.", "vi": "Tôi dự định đạp xe đến công viên.", "en": "I plan to ride a bike to the park."}]},
    {"id": "paobu", "hanzi": "跑步", "pinyin": "pǎobù", "vi": "chạy bộ", "en": "to jog / run", "pos": "verb",
     "examples": [{"zh": "去公园跑步。", "py": "Qù gōngyuán pǎobù.", "vi": "Đi công viên chạy bộ.", "en": "Go to the park to run."}]},
    {"id": "fen", "hanzi": "分", "pinyin": "fēn", "vi": "phút", "en": "minute", "pos": "noun",
     "match": ["分"],
     "examples": [{"zh": "我六点四十五分起床。", "py": "Wǒ liù diǎn sìshíwǔ fēn qǐchuáng.", "vi": "Tôi thức dậy lúc 6 giờ 45.", "en": "I get up at 6:45."}]},
    {"id": "zhong", "hanzi": "钟", "pinyin": "zhōng", "vi": "đồng hồ, phút", "en": "clock / minute (in 分钟)", "pos": "noun",
     "examples": [{"zh": "给你们十五分钟。", "py": "Gěi nǐmen shíwǔ fēnzhōng.", "vi": "Cho các bạn mười lăm phút.", "en": "You have fifteen minutes."}]},
    {"id": "zaofan", "hanzi": "早饭", "pinyin": "zǎofàn", "vi": "bữa sáng", "en": "breakfast", "pos": "noun",
     "examples": [{"zh": "你几点吃早饭？", "py": "Nǐ jǐ diǎn chī zǎofàn?", "vi": "Mấy giờ bạn ăn sáng?", "en": "What time do you eat breakfast?"}]},
    {"id": "wufan", "hanzi": "午饭", "pinyin": "wǔfàn", "vi": "bữa trưa", "en": "lunch", "pos": "noun",
     "examples": [{"zh": "中午我吃午饭。", "py": "Zhōngwǔ wǒ chī wǔfàn.", "vi": "Trưa tôi ăn cơm trưa.", "en": "At noon I eat lunch."}]},
    {"id": "wanfan", "hanzi": "晚饭", "pinyin": "wǎnfàn", "vi": "bữa tối", "en": "dinner", "pos": "noun",
     "examples": [{"zh": "我不想吃晚饭。", "py": "Wǒ bù xiǎng chī wǎnfàn.", "vi": "Tôi không muốn ăn cơm tối.", "en": "I don't want to eat dinner."}]},
    {"id": "buxiang", "hanzi": "不想", "pinyin": "bù xiǎng", "vi": "không muốn", "en": "to not want", "pos": "verb",
     "examples": [{"zh": "我不想吃晚饭。", "py": "Wǒ bù xiǎng chī wǎnfàn.", "vi": "Tôi không muốn ăn cơm tối.", "en": "I don't want dinner."}]},
    {"id": "dao", "hanzi": "到", "pinyin": "dào", "vi": "đến, tới", "en": "to arrive / until", "pos": "verb",
     "examples": [{"zh": "我工作到下午五点。", "py": "Wǒ gōngzuò dào xiàwǔ wǔ diǎn.", "vi": "Tôi làm việc đến 5 giờ chiều.", "en": "I work until 5 p.m."}]},
    {"id": "gen", "hanzi": "跟", "pinyin": "gēn", "vi": "cùng, với", "en": "with", "pos": "prep",
     "examples": [{"zh": "我跟同事一起吃饭。", "py": "Wǒ gēn tóngshì yìqǐ chīfàn.", "vi": "Tôi ăn cơm cùng đồng nghiệp.", "en": "I eat with my colleagues."}]},
    {"id": "yiqi", "hanzi": "一起", "pinyin": "yìqǐ", "vi": "cùng nhau", "en": "together", "pos": "adv",
     "examples": [{"zh": "你跟我一起跑步，好吗？", "py": "Nǐ gēn wǒ yìqǐ pǎobù, hǎo ma?", "vi": "Bạn chạy bộ cùng tôi nhé?", "en": "Run with me, okay?"}]},
    {"id": "zainar", "hanzi": "在哪儿", "pinyin": "zài nǎr", "vi": "ở đâu", "en": "where", "pos": "phrase",
     "examples": [{"zh": "你在哪儿吃晚饭？", "py": "Nǐ zài nǎr chī wǎnfàn?", "vi": "Bạn ăn tối ở đâu?", "en": "Where do you eat dinner?"}]},
    {"id": "zhunshi", "hanzi": "准时", "pinyin": "zhǔnshí", "vi": "đúng giờ", "en": "on time", "pos": "adv",
     "examples": [{"zh": "明天你要准时起床。", "py": "Míngtiān nǐ yào zhǔnshí qǐchuáng.", "vi": "Ngày mai bạn phải thức dậy đúng giờ.", "en": "Tomorrow you must get up on time."}]},
    {"id": "shangban", "hanzi": "上班", "pinyin": "shàngbān", "vi": "vào làm", "en": "to go to work", "pos": "verb",
     "examples": [{"zh": "你要准时上班。", "py": "Nǐ yào zhǔnshí shàngbān.", "vi": "Bạn phải đi làm đúng giờ.", "en": "You must go to work on time."}]},
    {"id": "xiaban", "hanzi": "下班", "pinyin": "xiàbān", "vi": "tan làm", "en": "to get off work", "pos": "verb",
     "examples": [{"zh": "你几点下班？", "py": "Nǐ jǐ diǎn xiàbān?", "vi": "Bạn mấy giờ tan làm?", "en": "What time do you get off work?"}]},
    {"id": "gongsi", "hanzi": "公司", "pinyin": "gōngsī", "vi": "công ty (家)", "en": "company", "pos": "noun",
     "examples": [{"zh": "我八点要去公司上班。", "py": "Wǒ bā diǎn yào qù gōngsī shàngbān.", "vi": "Tôi 8 giờ phải đi công ty làm.", "en": "At eight I have to go to the company for work."}]},
    {"id": "youshihou", "hanzi": "有时候", "pinyin": "yǒushíhou", "vi": "có lúc", "en": "sometimes", "pos": "adv",
     "examples": [{"zh": "我有时候在家吃早饭。", "py": "Wǒ yǒushíhou zài jiā chī zǎofàn.", "vi": "Có lúc tôi ăn sáng ở nhà.", "en": "Sometimes I eat breakfast at home."}]},
    {"id": "tongshi", "hanzi": "同事", "pinyin": "tóngshì", "vi": "đồng nghiệp", "en": "colleague", "pos": "noun",
     "examples": [{"zh": "我跟同事一起吃饭。", "py": "Wǒ gēn tóngshì yìqǐ chīfàn.", "vi": "Tôi ăn cùng đồng nghiệp.", "en": "I eat with colleagues."}]},
    {"id": "chuqu", "hanzi": "出去", "pinyin": "chūqù", "vi": "ra ngoài", "en": "to go out", "pos": "verb",
     "examples": [{"zh": "我想出去跑步。", "py": "Wǒ xiǎng chūqù pǎobù.", "vi": "Tôi muốn ra ngoài chạy bộ.", "en": "I want to go out for a run."}]},
    {"id": "bangongshi", "hanzi": "办公室", "pinyin": "bàngōngshì", "vi": "văn phòng", "en": "office", "pos": "noun",
     "examples": [{"zh": "他在办公室等你。", "py": "Tā zài bàngōngshì děng nǐ.", "vi": "Anh ấy ở văn phòng đợi bạn.", "en": "He is waiting for you in the office."}]},
    {"id": "waimai", "hanzi": "外卖", "pinyin": "wàimài", "vi": "đồ ăn mang về", "en": "takeout", "pos": "noun",
     "examples": [{"zh": "我有时候在办公室叫外卖。", "py": "Wǒ yǒushíhou zài bàngōngshì jiào wàimài.", "vi": "Có lúc tôi gọi đồ ăn ở văn phòng.", "en": "Sometimes I order takeout in the office."}]},
    {"id": "yibian", "hanzi": "一边", "pinyin": "yìbiān", "vi": "vừa… vừa…", "en": "while (doing both)", "pos": "phrase",
     "examples": [{"zh": "我常一边吃饭一边看电视。", "py": "Wǒ cháng yìbiān chīfàn yìbiān kàn diànshì.", "vi": "Tôi thường vừa ăn vừa xem ti vi.", "en": "I often eat while watching TV."}]},
    {"id": "yihou", "hanzi": "以后", "pinyin": "yǐhòu", "vi": "sau khi, sau này", "en": "after / later", "pos": "noun",
     "examples": [{"zh": "下班以后我常去超市。", "py": "Xiàbān yǐhòu wǒ cháng qù chāoshì.", "vi": "Sau khi tan làm tôi thường đi siêu thị.", "en": "After work I often go to the supermarket."}]},
    {"id": "ban", "hanzi": "半", "pinyin": "bàn", "vi": "nửa, rưỡi", "en": "half", "pos": "num",
     "examples": [{"zh": "我十点半睡觉。", "py": "Wǒ shí diǎn bàn shuìjiào.", "vi": "Tôi 10 giờ rưỡi đi ngủ.", "en": "I go to bed at 10:30."}]},
    {"id": "chaoshi", "hanzi": "超市", "pinyin": "chāoshì", "vi": "siêu thị", "en": "supermarket", "pos": "noun",
     "examples": [{"zh": "去超市买菜。", "py": "Qù chāoshì mǎi cài.", "vi": "Đi siêu thị mua đồ ăn.", "en": "Go to the supermarket to buy food."}]},
    {"id": "dianshi", "hanzi": "电视", "pinyin": "diànshì", "vi": "ti vi", "en": "TV", "pos": "noun",
     "examples": [{"zh": "看电视。", "py": "Kàn diànshì.", "vi": "Xem ti vi.", "en": "Watch TV."}]},
    {"id": "liaotianr", "hanzi": "聊天儿", "pinyin": "liáotiānr", "vi": "nói chuyện", "en": "to chat", "pos": "verb",
     "examples": [{"zh": "你跟谁一起聊天儿？", "py": "Nǐ gēn shéi yìqǐ liáotiānr?", "vi": "Bạn nói chuyện cùng ai?", "en": "Who do you chat with?"}]},
    {"id": "cha", "hanzi": "差", "pinyin": "chà", "vi": "thiếu, kém (giờ)", "en": "to lack (time: … to)", "pos": "verb",
     "examples": [{"zh": "差十分六点。", "py": "Chà shí fēn liù diǎn.", "vi": "6 giờ kém 10 phút.", "en": "Ten to six."}]},
    {"id": "ke", "hanzi": "刻", "pinyin": "kè", "vi": "khắc (15 phút)", "en": "quarter-hour", "pos": "noun",
     "examples": [{"zh": "我七点一刻上课。", "py": "Wǒ qī diǎn yí kè shàngkè.", "vi": "Tôi 7 giờ 15 lên lớp.", "en": "I have class at 7:15."}]},
    {"id": "shangke", "hanzi": "上课", "pinyin": "shàngkè", "vi": "lên lớp", "en": "to attend class", "pos": "verb",
     "examples": [{"zh": "每个同学都要准时上课。", "py": "Měi ge tóngxué dōu yào zhǔnshí shàngkè.", "vi": "Mỗi học sinh đều phải đúng giờ vào lớp.", "en": "Every student must go to class on time."}]},
    {"id": "xiake", "hanzi": "下课", "pinyin": "xiàkè", "vi": "tan học", "en": "class is over", "pos": "verb",
     "examples": [{"zh": "下课以后要做练习。", "py": "Xiàkè yǐhòu yào zuò liànxí.", "vi": "Sau khi tan học phải làm bài tập.", "en": "After class you should do exercises."}]},
    {"id": "huozhe", "hanzi": "或者", "pinyin": "huòzhě", "vi": "hoặc là", "en": "or", "pos": "conj",
     "examples": [{"zh": "我常喝茶或者喝咖啡。", "py": "Wǒ cháng hē chá huòzhě hē kāfēi.", "vi": "Tôi thường uống trà hoặc cà phê.", "en": "I often drink tea or coffee."}]},
    {"id": "wanr", "hanzi": "玩儿", "pinyin": "wánr", "vi": "chơi", "en": "to have fun / hang out", "pos": "verb",
     "examples": [{"zh": "星期天我常跟同事一起出去玩儿。", "py": "Xīngqītiān wǒ cháng gēn tóngshì yìqǐ chūqù wánr.", "vi": "Chủ nhật tôi thường ra ngoài chơi cùng đồng nghiệp.", "en": "On Sunday I often go out with colleagues."}]},
    {"id": "shuijiao", "hanzi": "睡觉", "pinyin": "shuìjiào", "vi": "ngủ", "en": "to sleep", "pos": "verb",
     "examples": [{"zh": "我十点半睡觉。", "py": "Wǒ shí diǎn bàn shuìjiào.", "vi": "Tôi 10 giờ rưỡi đi ngủ.", "en": "I go to sleep at 10:30."}]},
    {"id": "fuxi", "hanzi": "复习", "pinyin": "fùxí", "vi": "ôn tập", "en": "to review", "pos": "verb",
     "examples": [{"zh": "现在我要复习课文。", "py": "Xiànzài wǒ yào fùxí kèwén.", "vi": "Bây giờ tôi muốn ôn bài khóa.", "en": "Now I need to review the text."}]},
    {"id": "kewen", "hanzi": "课文", "pinyin": "kèwén", "vi": "bài khóa", "en": "lesson text", "pos": "noun",
     "examples": [{"zh": "现在我要复习复习课文。", "py": "Xiànzài wǒ yào fùxí fùxí kèwén.", "vi": "Bây giờ tôi muốn ôn bài khóa.", "en": "Now I want to review the text."}]},
    {"id": "douyin", "hanzi": "抖音", "pinyin": "Dǒuyīn", "vi": "TikTok", "en": "Douyin / TikTok", "pos": "noun",
     "examples": [{"zh": "看抖音。", "py": "Kàn Dǒuyīn.", "vi": "Xem TikTok.", "en": "Watch Douyin."}]},
]

BLOCKED = {
    "chuang": ("起床",),
    "dian": ("有点儿",),
}

PARAS = [
    (
        "大家好！今天我拍我的一天。我是一家大公司的职员。我们公司有一百个职员。每个职员都要准时上班。现在几点了？现在早上差一刻七点。",
        "Dàjiā hǎo! Jīntiān wǒ pāi wǒ de yì tiān. Wǒ shì yì jiā dà gōngsī de zhíyuán. Wǒmen gōngsī yǒu yìbǎi ge zhíyuán. Měi ge zhíyuán dōu yào zhǔnshí shàngbān. Xiànzài jǐ diǎn le? Xiànzài zǎoshang chà yí kè qī diǎn.",
        "Hello everyone! Today I'm filming my day. I'm an employee at a big company. Our company has a hundred staff. Every employee must go to work on time. What time is it? It's a quarter to seven in the morning.",
    ),
    (
        "每天我六点四十五分起床。床是新的，一张新床。起床以后我常做什么？起床以后，我先去公园跑步，然后回家吃早饭。你跟我一起跑步，好吗？",
        "Měi tiān wǒ liù diǎn sìshíwǔ fēn qǐchuáng. Chuáng shì xīn de, yì zhāng xīn chuáng. Qǐchuáng yǐhòu wǒ cháng zuò shénme? Qǐchuáng yǐhòu, wǒ xiān qù gōngyuán pǎobù, ránhòu huí jiā chī zǎofàn. Nǐ gēn wǒ yìqǐ pǎobù, hǎo ma?",
        "Every day I get up at 6:45. The bed is new — one new bed. After getting up, what do I usually do? I first go to the park to run, then go home for breakfast. Run with me, okay?",
    ),
    (
        "我不常去公园跑步，因为我觉得跑步很累。可是今天我想出去跑步。你怎么去公园？我打算骑自行车去公园。给自己十五分钟，然后回家。",
        "Wǒ bù cháng qù gōngyuán pǎobù, yīnwèi wǒ juéde pǎobù hěn lèi. Kěshì jīntiān wǒ xiǎng chūqù pǎobù. Nǐ zěnme qù gōngyuán? Wǒ dǎsuàn qí zìxíngchē qù gōngyuán. Gěi zìjǐ shíwǔ fēnzhōng, ránhòu huí jiā.",
        "I don't often run in the park, because running feels tiring. But today I want to go out for a run. How do you get to the park? I plan to ride a bike there. Fifteen minutes, then home.",
    ),
    (
        "你几点吃早饭？我七点一刻吃早饭。早上，我常喝茶或者喝咖啡。我有时候在家吃早饭，我有时候在公司吃早饭。今天我在家吃早饭，然后去上班。",
        "Nǐ jǐ diǎn chī zǎofàn? Wǒ qī diǎn yí kè chī zǎofàn. Zǎoshang, wǒ cháng hē chá huòzhě hē kāfēi. Wǒ yǒushíhou zài jiā chī zǎofàn, wǒ yǒushíhou zài gōngsī chī zǎofàn. Jīntiān wǒ zài jiā chī zǎofàn, ránhòu qù shàngbān.",
        "What time do you eat breakfast? I eat breakfast at 7:15. In the morning I often drink tea or coffee. Sometimes I eat breakfast at home, sometimes at the company. Today I eat at home, then go to work.",
    ),
    (
        "每个职员要八点准时上班。我八点要去公司上班。你送我去公司吧！我常坐公共汽车或者骑自行车去公司。今天差十分八点我到公司。不能晚。",
        "Měi ge zhíyuán yào bā diǎn zhǔnshí shàngbān. Wǒ bā diǎn yào qù gōngsī shàngbān. Nǐ sòng wǒ qù gōngsī ba! Wǒ cháng zuò gōnggòng qìchē huòzhě qí zìxíngchē qù gōngsī. Jīntiān chà shí fēn bā diǎn wǒ dào gōngsī. Bù néng wǎn.",
        "Every employee must start work at eight on time. At eight I have to go to the company. Drop me at the company! I often take the bus or ride a bike. Today I arrive at ten to eight. I can't be late.",
    ),
    (
        "我在办公室工作。他在办公室等你。中午我常跟同事一起出去吃饭，或者在办公室叫外卖。今天我不做饭，叫外卖吧。你在哪儿吃午饭？",
        "Wǒ zài bàngōngshì gōngzuò. Tā zài bàngōngshì děng nǐ. Zhōngwǔ wǒ cháng gēn tóngshì yìqǐ chūqù chīfàn, huòzhě zài bàngōngshì jiào wàimài. Jīntiān wǒ bú zuòfàn, jiào wàimài ba. Nǐ zài nǎr chī wǔfàn?",
        "I work in the office. He is waiting for you in the office. At noon I often go out to eat with colleagues, or order takeout in the office. Today I'm not cooking — let's get takeout. Where do you eat lunch?",
    ),
    (
        "我中午十二点吃午饭。有时候我跟同事们一起吃饭，有时候一个人吃饭。她常一边吃饭一边跟同事一起聊天儿。我也常一边吃饭一边看电视。看一会儿就工作。",
        "Wǒ zhōngwǔ shí'èr diǎn chī wǔfàn. Yǒushíhou wǒ gēn tóngshì men yìqǐ chīfàn, yǒushíhou yí ge rén chīfàn. Tā cháng yìbiān chīfàn yìbiān gēn tóngshì yìqǐ liáotiānr. Wǒ yě cháng yìbiān chīfàn yìbiān kàn diànshì. Kàn yíhuìr jiù gōngzuò.",
        "I eat lunch at twelve. Sometimes I eat with colleagues, sometimes alone. She often eats while chatting with colleagues. I often eat while watching TV. Watch a bit, then work again.",
    ),
    (
        "我工作到下午五点就下班。你几点下班？下班以后，我常去超市买菜。你来公司接我吧！下班以后你想做什么？我想出去买，然后回家做晚饭。",
        "Wǒ gōngzuò dào xiàwǔ wǔ diǎn jiù xiàbān. Nǐ jǐ diǎn xiàbān? Xiàbān yǐhòu, wǒ cháng qù chāoshì mǎi cài. Nǐ lái gōngsī jiē wǒ ba! Xiàbān yǐhòu nǐ xiǎng zuò shénme? Wǒ xiǎng chūqù mǎi, ránhòu huí jiā zuò wǎnfàn.",
        "I work until 5 p.m., then I get off work. What time do you finish? After work I often go to the supermarket. Come pick me up at the company! After work, what do you want to do? I want to go out to shop, then go home and cook dinner.",
    ),
    (
        "今天，你跟谁一起吃晚饭？你在哪儿吃晚饭？我不想吃晚饭，因为中午的外卖有点儿多。可是妈妈说：“你应该吃晚饭。”好，我七点吃晚饭。差十五分七点我吃饭。",
        "Jīntiān, nǐ gēn shéi yìqǐ chī wǎnfàn? Nǐ zài nǎr chī wǎnfàn? Wǒ bù xiǎng chī wǎnfàn, yīnwèi zhōngwǔ de wàimài yǒudiǎnr duō. Kěshì māma shuō: “Nǐ yīnggāi chī wǎnfàn.” Hǎo, wǒ qī diǎn chī wǎnfàn. Chà shíwǔ fēn qī diǎn wǒ chīfàn.",
        "Who are you eating dinner with today? Where do you eat dinner? I don't want dinner, because the lunch takeout was a bit much. But mom said: “You should eat dinner.” Okay — I eat at seven. I eat at a quarter to seven.",
    ),
    (
        "晚上我一边看书一边喝茶，或者一边做练习一边用电脑。以后你想做什么工作？以后我想当医生。现在我是职员。每个月都有很多工作。每年都这样。",
        "Wǎnshang wǒ yìbiān kàn shū yìbiān hē chá, huòzhě yìbiān zuò liànxí yìbiān yòng diànnǎo. Yǐhòu nǐ xiǎng zuò shénme gōngzuò? Yǐhòu wǒ xiǎng dāng yīshēng. Xiànzài wǒ shì zhíyuán. Měi ge yuè dōu yǒu hěn duō gōngzuò. Měi nián dōu zhèyàng.",
        "In the evening I read while drinking tea, or do exercises while using the computer. What job do you want later? Later I want to be a doctor. Now I am a staff member. Every month there is a lot of work. Every year is like this.",
    ),
    (
        "我还在学汉语。每天八点上汉语课。每个同学都要准时上课。我七点一刻上课。老师让我们下课以后要做练习。下课以后，我复习课文。你复习吧！现在我要复习复习课文。",
        "Wǒ hái zài xué Hànyǔ. Měi tiān bā diǎn shàng Hànyǔ kè. Měi ge tóngxué dōu yào zhǔnshí shàngkè. Wǒ qī diǎn yí kè shàngkè. Lǎoshī ràng wǒmen xiàkè yǐhòu yào zuò liànxí. Xiàkè yǐhòu, wǒ fùxí kèwén. Nǐ fùxí ba! Xiànzài wǒ yào fùxí fùxí kèwén.",
        "I am still learning Chinese. Every day at eight there is Chinese class. Every classmate must go to class on time. I have class at 7:15. The teacher tells us to do exercises after class. After class I review the text. Review! Now I need to review the lesson text.",
    ),
    (
        "复习以后，我有时候看抖音，有时候看电视。看抖音十五分钟就好，不应该看很长时间。两点半我还在公司的时候，我不能看抖音。上班的时候要工作。",
        "Fùxí yǐhòu, wǒ yǒushíhou kàn Dǒuyīn, yǒushíhou kàn diànshì. Kàn Dǒuyīn shíwǔ fēnzhōng jiù hǎo, bù yīnggāi kàn hěn cháng shíjiān. Liǎng diǎn bàn wǒ hái zài gōngsī de shíhou, wǒ bù néng kàn Dǒuyīn. Shàngbān de shíhou yào gōngzuò.",
        "After reviewing, sometimes I watch Douyin, sometimes TV. Fifteen minutes of Douyin is enough — I shouldn't watch long. At 2:30 when I'm still at the company, I can't watch Douyin. During work time, I should work.",
    ),
    (
        "星期天我常跟同事一起出去玩儿。去公园跑步，或者去超市，或者在家聊天儿。你跟谁一起聊天儿？我跟同事聊天儿，也跟朋友聊天儿。出去玩儿的时候很高兴。",
        "Xīngqītiān wǒ cháng gēn tóngshì yìqǐ chūqù wánr. Qù gōngyuán pǎobù, huòzhě qù chāoshì, huòzhě zài jiā liáotiānr. Nǐ gēn shéi yìqǐ liáotiānr? Wǒ gēn tóngshì liáotiānr, yě gēn péngyou liáotiānr. Chūqù wánr de shíhou hěn gāoxìng.",
        "On Sunday I often go out with colleagues. Run in the park, or go to the supermarket, or chat at home. Who do you chat with? I chat with colleagues and with friends. Going out is fun.",
    ),
    (
        "晚上十点半我睡觉。有时候十点睡觉，有时候十点半。床很大，我很累，睡觉就好。明天你要准时起床。六点准时起床，然后跑步，然后吃早饭，然后上班。",
        "Wǎnshang shí diǎn bàn wǒ shuìjiào. Yǒushíhou shí diǎn shuìjiào, yǒushíhou shí diǎn bàn. Chuáng hěn dà, wǒ hěn lèi, shuìjiào jiù hǎo. Míngtiān nǐ yào zhǔnshí qǐchuáng. Liù diǎn zhǔnshí qǐchuáng, ránhòu pǎobù, ránhòu chī zǎofàn, ránhòu shàngbān.",
        "At 10:30 I go to sleep. Sometimes at ten, sometimes at 10:30. The bed is big, I am tired — sleep is good. Tomorrow you must get up on time. Get up at six on time, then run, then breakfast, then work.",
    ),
    (
        "你们呢？你几点起床？你在哪儿吃早饭、午饭、晚饭？你跟谁一起吃饭？下班以后你常做什么？去超市，还是出去玩儿，还是复习课文？你常看抖音吗？",
        "Nǐmen ne? Nǐ jǐ diǎn qǐchuáng? Nǐ zài nǎr chī zǎofàn, wǔfàn, wǎnfàn? Nǐ gēn shéi yìqǐ chīfàn? Xiàbān yǐhòu nǐ cháng zuò shénme? Qù chāoshì, háishì chūqù wánr, háishì fùxí kèwén? Nǐ cháng kàn Dǒuyīn ma?",
        "What about you? What time do you get up? Where do you eat breakfast, lunch, and dinner? Who do you eat with? After work, what do you often do? Supermarket, go out, or review the text? Do you often watch Douyin?",
    ),
    (
        "我看钟。钟在桌子上。现在两点三十分。两点半我还在办公室。每个职员工作到五点。我工作到下午五点就下班。星期一到星期五都这样。",
        "Wǒ kàn zhōng. Zhōng zài zhuōzi shang. Xiànzài liǎng diǎn sānshí fēn. Liǎng diǎn bàn wǒ hái zài bàngōngshì. Měi ge zhíyuán gōngzuò dào wǔ diǎn. Wǒ gōngzuò dào xiàwǔ wǔ diǎn jiù xiàbān. Xīngqīyī dào xīngqīwǔ dōu zhèyàng.",
        "I look at the clock. The clock is on the desk. It's 2:30 now. At 2:30 I am still in the office. Every employee works until five. I work until 5 p.m. then get off work. Monday to Friday is like this.",
    ),
    (
        "吃饭以后应该休息。下课以后也应该休息。起床以后先跑步，然后吃早饭，然后上课或者上班。一边学习一边工作，有点儿累。累了就睡觉。床在那儿，你去睡觉吧。",
        "Chīfàn yǐhòu yīnggāi xiūxi. Xiàkè yǐhòu yě yīnggāi xiūxi. Qǐchuáng yǐhòu xiān pǎobù, ránhòu chī zǎofàn, ránhòu shàngkè huòzhě shàngbān. Yìbiān xuéxí yìbiān gōngzuò, yǒudiǎnr lèi. Lèi le jiù shuìjiào. Chuáng zài nàr, nǐ qù shuìjiào ba.",
        "After eating you should rest. After class you should rest too. After getting up, first run, then breakfast, then class or work. Studying while working is a bit tiring. If you're tired, sleep. The bed is there — go sleep.",
    ),
    (
        "好，今天的视频就到这儿。从起床到睡觉，这就是我的一天。谢谢大家。差一刻十一点了，我要睡觉了。明天见！",
        "Hǎo, jīntiān de shìpín jiù dào zhèr. Cóng qǐchuáng dào shuìjiào, zhè jiù shì wǒ de yì tiān. Xièxie dàjiā. Chà yí kè shíyī diǎn le, wǒ yào shuìjiào le. Míngtiān jiàn!",
        "Okay, that's all for today's video. From getting up to sleeping — this is my day. Thanks everyone. It's a quarter to eleven — I need to sleep. See you tomorrow!",
    ),
]


if __name__ == "__main__":
    emit_lesson(
        lesson=16,
        title="我的一天",
        title_py="Wǒ de yì tiān",
        title_en="My day",
        vocab=VOCAB,
        paras=PARAS,
        blocked_if_inside=BLOCKED,
    )
