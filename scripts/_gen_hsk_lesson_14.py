#!/usr/bin/env python3
"""Generate HSK lesson 14 data (vocab + vlog script with new-word tokens)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "js" / "hsk-lesson-14-data.js"

VOCAB = [
    {
        "id": "kaixue",
        "hanzi": "开学",
        "pinyin": "kāixué",
        "vi": "khai giảng",
        "en": "school starts / term begins",
        "pos": "verb",
        "examples": [
            {"zh": "你的学校开学了吗？", "py": "Nǐ de xuéxiào kāixué le ma?", "vi": "Trường của bạn khai giảng chưa?", "en": "Has your school started yet?"},
            {"zh": "你学校星期几开学？", "py": "Nǐ xuéxiào xīngqī jǐ kāixué?", "vi": "Trường của bạn thứ mấy khai giảng?", "en": "What day does your school start?"},
        ],
    },
    {
        "id": "xia",
        "hanzi": "下",
        "pinyin": "xià",
        "vi": "tiếp theo, tới + danh từ",
        "en": "next (下个星期一)",
        "pos": "prefix",
        "match": ["下个"],
        "examples": [
            {"zh": "下个星期一，我学校开学。", "py": "Xià ge xīngqīyī, wǒ xuéxiào kāixué.", "vi": "Thứ Hai tuần tới, trường tôi khai giảng.", "en": "Next Monday, my school starts."},
        ],
    },
    {
        "id": "song",
        "hanzi": "送",
        "pinyin": "sòng",
        "vi": "đưa, tiễn",
        "en": "to drop off / see off",
        "pos": "verb",
        "examples": [
            {"zh": "让我送你吧！", "py": "Ràng wǒ sòng nǐ ba!", "vi": "Để tôi tiễn bạn!", "en": "Let me see you off!"},
            {"zh": "我送你去学校吧！", "py": "Wǒ sòng nǐ qù xuéxiào ba!", "vi": "Tôi đưa bạn đến trường nhé!", "en": "Let me take you to school!"},
            {"zh": "我送你去医院吧！", "py": "Wǒ sòng nǐ qù yīyuàn ba!", "vi": "Tôi đưa bạn đến bệnh viện nhé!", "en": "Let me take you to the hospital!"},
            {"zh": "我让爸爸送你去学校吧。", "py": "Wǒ ràng bàba sòng nǐ qù xuéxiào ba.", "vi": "Để bố tiễn bạn đến trường nhé.", "en": "I'll have dad take you to school."},
        ],
    },
    {
        "id": "jie",
        "hanzi": "接",
        "pinyin": "jiē",
        "vi": "đón",
        "en": "to pick up",
        "pos": "verb",
        "examples": [
            {"zh": "一会儿，你接我吧。", "py": "Yíhuìr, nǐ jiē wǒ ba.", "vi": "Lát nữa, bạn đón tôi nhé.", "en": "Pick me up in a bit."},
            {"zh": "爸爸接我回家。", "py": "Bàba jiē wǒ huí jiā.", "vi": "Bố đón tôi về nhà.", "en": "Dad picks me up and takes me home."},
            {"zh": "今天，谁接你回家？", "py": "Jīntiān, shéi jiē nǐ huí jiā?", "vi": "Hôm nay ai đón bạn về nhà?", "en": "Who is picking you up today?"},
        ],
    },
    {
        "id": "ziji",
        "hanzi": "自己",
        "pinyin": "zìjǐ",
        "vi": "tự mình",
        "en": "oneself",
        "pos": "pronoun",
        "examples": [
            {"zh": "我自己学习汉语。", "py": "Wǒ zìjǐ xuéxí Hànyǔ.", "vi": "Tôi tự học tiếng Trung.", "en": "I study Chinese by myself."},
            {"zh": "自己写汉字。", "py": "Zìjǐ xiě Hànzì.", "vi": "Tự viết chữ Hán.", "en": "Write the characters yourself."},
            {"zh": "让我自己去学校。", "py": "Ràng wǒ zìjǐ qù xuéxiào.", "vi": "Để tôi tự đến trường.", "en": "Let me go to school by myself."},
            {"zh": "让我自己回家，不要送了。", "py": "Ràng wǒ zìjǐ huí jiā, bú yào sòng le.", "vi": "Tôi tự về nhà, đừng tiễn nữa.", "en": "Let me go home by myself — don't see me off."},
        ],
    },
    {
        "id": "ziji-de",
        "hanzi": "自己的",
        "pinyin": "zìjǐ de",
        "vi": "cái gì đó của mình",
        "en": "one's own",
        "pos": "pronoun",
        "examples": [
            {"zh": "你检查自己的书包吧！", "py": "Nǐ jiǎnchá zìjǐ de shūbāo ba!", "vi": "Bạn kiểm tra ba lô của mình đi!", "en": "Check your own backpack!"},
            {"zh": "你用自己的钱吧！", "py": "Nǐ yòng zìjǐ de qián ba!", "vi": "Bạn dùng tiền của mình đi!", "en": "Use your own money!"},
        ],
    },
    {
        "id": "kai",
        "hanzi": "开",
        "pinyin": "kāi",
        "vi": "lái (xe 4 bánh)",
        "en": "to drive (a car)",
        "pos": "verb",
        "match": ["开车"],
        "examples": [
            {"zh": "爸爸开车送我去学校。", "py": "Bàba kāichē sòng wǒ qù xuéxiào.", "vi": "Bố lái xe đưa tôi đến trường.", "en": "Dad drives me to school."},
            {"zh": "他自己开车去医院。", "py": "Tā zìjǐ kāichē qù yīyuàn.", "vi": "Anh ấy tự lái xe đến bệnh viện.", "en": "He drives to the hospital himself."},
        ],
    },
    {
        "id": "kaiche",
        "hanzi": "开车",
        "pinyin": "kāichē",
        "vi": "lái xe",
        "en": "to drive a car",
        "pos": "verb",
        "examples": [
            {"zh": "开车的时候别看手机。", "py": "Kāichē de shíhou bié kàn shǒujī.", "vi": "Lúc lái xe đừng xem điện thoại.", "en": "Don't look at your phone while driving."},
        ],
    },
    {
        "id": "che",
        "hanzi": "车",
        "pinyin": "chē",
        "vi": "xe",
        "en": "vehicle / car",
        "pos": "noun",
        "examples": [
            {"zh": "这是谁的车？", "py": "Zhè shì shéi de chē?", "vi": "Đây là xe của ai?", "en": "Whose car is this?"},
        ],
    },
    {
        "id": "qi",
        "hanzi": "骑",
        "pinyin": "qí",
        "vi": "cưỡi, lái (xe 2 bánh)",
        "en": "to ride (a bike / motorcycle)",
        "pos": "verb",
        "examples": [
            {"zh": "现在你骑车去哪儿？", "py": "Xiànzài nǐ qí chē qù nǎr?", "vi": "Bây giờ bạn đi xe đạp đi đâu?", "en": "Where are you riding to now?"},
        ],
    },
    {
        "id": "zixingche",
        "hanzi": "自行车",
        "pinyin": "zìxíngchē",
        "vi": "xe đạp",
        "en": "bicycle",
        "pos": "noun",
        "examples": [
            {"zh": "我想找我的自行车。", "py": "Wǒ xiǎng zhǎo wǒ de zìxíngchē.", "vi": "Tôi muốn tìm xe đạp của tôi.", "en": "I want to find my bicycle."},
            {"zh": "我骑自行车去学校。", "py": "Wǒ qí zìxíngchē qù xuéxiào.", "vi": "Tôi đi xe đạp đến trường.", "en": "I ride a bicycle to school."},
        ],
    },
    {
        "id": "motuoche",
        "hanzi": "摩托车",
        "pinyin": "mótuōchē",
        "vi": "xe máy",
        "en": "motorcycle",
        "pos": "noun",
        "examples": [
            {"zh": "他骑摩托车去工作。", "py": "Tā qí mótuōchē qù gōngzuò.", "vi": "Anh ấy đi xe máy đi làm.", "en": "He rides a motorcycle to work."},
        ],
    },
    {
        "id": "qiche",
        "hanzi": "汽车",
        "pinyin": "qìchē",
        "vi": "xe ô tô",
        "en": "car",
        "pos": "noun",
        "examples": [
            {"zh": "我坐汽车去学校。", "py": "Wǒ zuò qìchē qù xuéxiào.", "vi": "Tôi đi ô tô đến trường.", "en": "I go to school by car."},
        ],
    },
    {
        "id": "gonggongqiche",
        "hanzi": "公共汽车",
        "pinyin": "gōnggòng qìchē",
        "vi": "xe buýt",
        "en": "bus",
        "pos": "noun",
        "examples": [
            {"zh": "我坐公共汽车去学校。", "py": "Wǒ zuò gōnggòng qìchē qù xuéxiào.", "vi": "Tôi đi xe buýt đến trường.", "en": "I take the bus to school."},
        ],
    },
    {
        "id": "diannao",
        "hanzi": "电脑",
        "pinyin": "diànnǎo",
        "vi": "máy tính",
        "en": "computer",
        "pos": "noun",
        "examples": [
            {"zh": "我用自己的电脑工作。", "py": "Wǒ yòng zìjǐ de diànnǎo gōngzuò.", "vi": "Tôi dùng máy tính của mình làm việc.", "en": "I work on my own computer."},
            {"zh": "妈妈刚给我买一台电脑。", "py": "Māma gāng gěi wǒ mǎi yì tái diànnǎo.", "vi": "Mẹ vừa mua cho tôi một cái máy tính.", "en": "Mom just bought me a computer."},
            {"zh": "我跟妈妈一起去买电脑。", "py": "Wǒ gēn māma yìqǐ qù mǎi diànnǎo.", "vi": "Tôi đi mua máy tính cùng mẹ.", "en": "I went with mom to buy a computer."},
        ],
    },
    {
        "id": "zhuozi",
        "hanzi": "桌子",
        "pinyin": "zhuōzi",
        "vi": "bàn (量词 张)",
        "en": "desk / table",
        "pos": "noun",
        "examples": [
            {"zh": "两张桌子。", "py": "Liǎng zhāng zhuōzi.", "vi": "Hai cái bàn.", "en": "Two desks."},
        ],
    },
    {
        "id": "yizi",
        "hanzi": "椅子",
        "pinyin": "yǐzi",
        "vi": "cái ghế",
        "en": "chair",
        "pos": "noun",
        "examples": [
            {"zh": "我觉得这个椅子有点儿小。", "py": "Wǒ juéde zhège yǐzi yǒudiǎnr xiǎo.", "vi": "Tôi cảm thấy cái ghế này hơi nhỏ.", "en": "I think this chair is a bit small."},
        ],
    },
    {
        "id": "youdiar",
        "hanzi": "有点儿",
        "pinyin": "yǒudiǎnr",
        "vi": "hơi + tính từ",
        "en": "a bit / a little",
        "pos": "adverb",
        "examples": [
            {"zh": "这个椅子有点儿小。", "py": "Zhège yǐzi yǒudiǎnr xiǎo.", "vi": "Cái ghế này hơi nhỏ.", "en": "This chair is a bit small."},
        ],
    },
    {
        "id": "jiu-old",
        "hanzi": "旧",
        "pinyin": "jiù",
        "vi": "cũ",
        "en": "old (used)",
        "pos": "adj",
        "examples": [
            {"zh": "有点儿旧。", "py": "Yǒudiǎnr jiù.", "vi": "Hơi cũ.", "en": "A bit old."},
        ],
    },
    {
        "id": "xin",
        "hanzi": "新",
        "pinyin": "xīn",
        "vi": "mới",
        "en": "new",
        "pos": "adj",
        "examples": [
            {"zh": "有点儿新。", "py": "Yǒudiǎnr xīn.", "vi": "Hơi mới.", "en": "Quite new."},
        ],
    },
    {
        "id": "gui",
        "hanzi": "贵",
        "pinyin": "guì",
        "vi": "đắt",
        "en": "expensive",
        "pos": "adj",
        "examples": [
            {"zh": "有点儿贵。", "py": "Yǒudiǎnr guì.", "vi": "Hơi đắt.", "en": "A bit expensive."},
        ],
    },
    {
        "id": "lianxi",
        "hanzi": "练习",
        "pinyin": "liànxí",
        "vi": "luyện tập, bài tập",
        "en": "practice / exercise",
        "pos": "noun/verb",
        "examples": [
            {"zh": "现在我要用电脑做练习。", "py": "Xiànzài wǒ yào yòng diànnǎo zuò liànxí.", "vi": "Bây giờ tôi phải dùng máy tính làm bài tập.", "en": "Now I need to do exercises on the computer."},
            {"zh": "今天的练习有点儿多。", "py": "Jīntiān de liànxí yǒudiǎnr duō.", "vi": "Bài tập hôm nay hơi nhiều.", "en": "Today's exercises are a bit many."},
            {"zh": "你们回家要多练习。", "py": "Nǐmen huí jiā yào duō liànxí.", "vi": "Các bạn về nhà phải luyện tập nhiều.", "en": "Practice more when you go home."},
        ],
    },
    {
        "id": "jiu-then",
        "hanzi": "就",
        "pinyin": "jiù",
        "vi": "thì, liền",
        "en": "then / right away",
        "pos": "adv",
        "examples": [
            {"zh": "你喜欢就好。", "py": "Nǐ xǐhuan jiù hǎo.", "vi": "Bạn thích thì tốt.", "en": "If you like it, that's good."},
            {"zh": "累了就休息吧。", "py": "Lèi le jiù xiūxi ba.", "vi": "Mệt rồi thì nghỉ ngơi đi.", "en": "If you're tired, then rest."},
        ],
    },
    {
        "id": "lei",
        "hanzi": "累",
        "pinyin": "lèi",
        "vi": "mệt",
        "en": "tired",
        "pos": "adj",
        "examples": [
            {"zh": "累了就休息吧，不要做了。", "py": "Lèi le jiù xiūxi ba, bú yào zuò le.", "vi": "Mệt rồi thì nghỉ đi, đừng làm nữa.", "en": "If you're tired, rest — don't keep working."},
        ],
    },
    {
        "id": "shihou",
        "hanzi": "时候",
        "pinyin": "shíhou",
        "vi": "khi, lúc",
        "en": "time / moment",
        "pos": "noun",
        "examples": [
            {"zh": "什么时候你回家？", "py": "Shénme shíhou nǐ huí jiā?", "vi": "Khi nào bạn về nhà?", "en": "When are you going home?"},
            {"zh": "你的学校什么时候开学？", "py": "Nǐ de xuéxiào shénme shíhou kāixué?", "vi": "Khi nào trường bạn khai giảng?", "en": "When does your school start?"},
        ],
    },
    {
        "id": "de-shihou",
        "hanzi": "的时候",
        "pinyin": "de shíhou",
        "vi": "lúc làm gì",
        "en": "when (doing something)",
        "pos": "phrase",
        "examples": [
            {"zh": "做练习的时候。", "py": "Zuò liànxí de shíhou.", "vi": "Lúc làm bài tập.", "en": "When doing exercises."},
            {"zh": "开车的时候不要看手机。", "py": "Kāichē de shíhou bú yào kàn shǒujī.", "vi": "Lúc lái xe đừng xem điện thoại.", "en": "Don't look at your phone while driving."},
        ],
    },
    {
        "id": "ban",
        "hanzi": "班",
        "pinyin": "bān",
        "vi": "lớp (个)",
        "en": "class",
        "pos": "noun",
        "examples": [
            {"zh": "我们班只有十六个学生。", "py": "Wǒmen bān zhǐ yǒu shíliù ge xuéshēng.", "vi": "Lớp chúng tôi chỉ có 16 học sinh.", "en": "Our class has only 16 students."},
            {"zh": "你在哪个班学习？", "py": "Nǐ zài nǎge bān xuéxí?", "vi": "Bạn học ở lớp nào?", "en": "Which class do you study in?"},
        ],
    },
    {
        "id": "nver",
        "hanzi": "女儿",
        "pinyin": "nǚ'ér",
        "vi": "con gái",
        "en": "daughter",
        "pos": "noun",
        "examples": [
            {"zh": "她有一个女儿。", "py": "Tā yǒu yí ge nǚ'ér.", "vi": "Cô ấy có một cô con gái.", "en": "She has a daughter."},
        ],
    },
    {
        "id": "erzi",
        "hanzi": "儿子",
        "pinyin": "érzi",
        "vi": "con trai",
        "en": "son",
        "pos": "noun",
        "examples": [
            {"zh": "她有一个儿子。", "py": "Tā yǒu yí ge érzi.", "vi": "Cô ấy có một cậu con trai.", "en": "She has a son."},
        ],
    },
    {
        "id": "yong",
        "hanzi": "用",
        "pinyin": "yòng",
        "vi": "dùng, bằng",
        "en": "to use",
        "pos": "verb",
        "examples": [
            {"zh": "我用筷子吃饭。", "py": "Wǒ yòng kuàizi chīfàn.", "vi": "Tôi ăn cơm bằng đũa.", "en": "I eat with chopsticks."},
            {"zh": "我用电脑做工作。", "py": "Wǒ yòng diànnǎo zuò gōngzuò.", "vi": "Tôi làm việc bằng máy tính.", "en": "I work with a computer."},
        ],
    },
    {
        "id": "zuo",
        "hanzi": "坐",
        "pinyin": "zuò",
        "vi": "ngồi, đi (phương tiện)",
        "en": "to sit / take (transport)",
        "pos": "verb",
        "examples": [
            {"zh": "我坐公共汽车去学校。", "py": "Wǒ zuò gōnggòng qìchē qù xuéxiào.", "vi": "Tôi đi xe buýt đến trường.", "en": "I take the bus to school."},
        ],
    },
]

# Longest match first. 开 is covered by 开车 so we do not also mark 开 inside 开车.
# 下 only matches 下个 (next), never 下午 / 下课.
MATCHERS: list[tuple[str, str]] = []
for w in VOCAB:
    forms = w.get("match") or [w["hanzi"]]
    for form in forms:
        MATCHERS.append((form, w["id"]))
MATCHERS.sort(key=lambda x: len(x[0]), reverse=True)

# Do not let 车 / 开 / 自己 steal longer compounds.
BLOCKED_IF_INSIDE = {
    "che": ("自行车", "摩托车", "汽车", "公共汽车", "开车"),
    "kai": ("开学", "开车"),
    "ziji": ("自己的", "自行车"),
    "qiche": ("公共汽车",),
    "shihou": ("的时候",),
}


PARAS: list[tuple[str, str, str]] = [
    (
        "大家好！我是小明。今天我给大家拍一个小视频。今天是我们学校开学的日子。你们的学校开学了吗？你学校星期几开学？",
        "Dàjiā hǎo! Wǒ shì Xiǎo Míng. Jīntiān wǒ gěi dàjiā pāi yí ge xiǎo shìpín. Jīntiān shì wǒmen xuéxiào kāixué de rìzi. Nǐmen de xuéxiào kāixué le ma? Nǐ xuéxiào xīngqī jǐ kāixué?",
        "Hello everyone! I'm Xiao Ming. Today I'm filming a short vlog for you. Today is the day our school starts. Has your school started yet? What day does your school start?",
    ),
    (
        "下个星期一，很多学校也要开学。我的学校今天开学。早上七点，爸爸问我：“今天谁送你去学校？”我说：“让我自己去学校吧，不要送了。”",
        "Xià ge xīngqīyī, hěn duō xuéxiào yě yào kāixué. Wǒ de xuéxiào jīntiān kāixué. Zǎoshang qī diǎn, bàba wèn wǒ: “Jīntiān shéi sòng nǐ qù xuéxiào?” Wǒ shuō: “Ràng wǒ zìjǐ qù xuéxiào ba, bú yào sòng le.”",
        "Next Monday, many schools will also start. My school starts today. At seven in the morning, dad asked me: “Who is taking you to school today?” I said: “Let me go by myself — don't drop me off.”",
    ),
    (
        "爸爸说：“学校有点儿远，我开车送你去学校吧。”妈妈也说：“我让爸爸送你去学校吧。”好，今天爸爸送我。他自己开车去医院工作，所以他可以送我。",
        "Bàba shuō: “Xuéxiào yǒudiǎnr yuǎn, wǒ kāichē sòng nǐ qù xuéxiào ba.” Māma yě shuō: “Wǒ ràng bàba sòng nǐ qù xuéxiào ba.” Hǎo, jīntiān bàba sòng wǒ. Tā zìjǐ kāichē qù yīyuàn gōngzuò, suǒyǐ tā kěyǐ sòng wǒ.",
        "Dad said: “School is a bit far. Let me drive you.” Mom also said: “I'll have dad take you to school.” Okay — dad is dropping me off today. He drives to the hospital for work himself, so he can take me.",
    ),
    (
        "车上，爸爸说：“开车的时候不要看手机。”我说：“好，我知道了。”开车的时候，我们看路，不看手机。你喜欢开车吗？我现在不会开车，就坐爸爸的车。",
        "Chē shang, bàba shuō: “Kāichē de shíhou bú yào kàn shǒujī.” Wǒ shuō: “Hǎo, wǒ zhīdào le.” Kāichē de shíhou, wǒmen kàn lù, bú kàn shǒujī. Nǐ xǐhuan kāichē ma? Wǒ xiànzài bú huì kāichē, jiù zuò bàba de chē.",
        "In the car, dad said: “Don't look at your phone while driving.” I said: “Okay, I know.” When driving, we watch the road, not the phone. Do you like driving? I can't drive yet, so I just sit in dad's car.",
    ),
    (
        "我有一辆自行车。我想找我的自行车。自行车有点儿旧，可是我很喜欢。很多时候，我骑自行车去学校。现在你骑车去哪儿？今天我没有骑，因为爸爸送我。",
        "Wǒ yǒu yí liàng zìxíngchē. Wǒ xiǎng zhǎo wǒ de zìxíngchē. Zìxíngchē yǒudiǎnr jiù, kěshì wǒ hěn xǐhuan. Hěn duō shíhou, wǒ qí zìxíngchē qù xuéxiào. Xiànzài nǐ qí chē qù nǎr? Jīntiān wǒ méiyǒu qí, yīnwèi bàba sòng wǒ.",
        "I have a bicycle. I wanted to find my bicycle. The bike is a bit old, but I like it a lot. Often I ride my bicycle to school. Where are you riding now? Today I didn't ride, because dad dropped me off.",
    ),
    (
        "我的同学怎么去学校？有的同学骑自行车，有的同学坐公共汽车。还有同学骑摩托车。公共汽车有点儿慢，汽车快一点儿。今天我坐汽车去学校。这是爸爸的车。",
        "Wǒ de tóngxué zěnme qù xuéxiào? Yǒude tóngxué qí zìxíngchē, yǒude tóngxué zuò gōnggòng qìchē. Hái yǒu tóngxué qí mótuōchē. Gōnggòng qìchē yǒudiǎnr màn, qìchē kuài yìdiǎnr. Jīntiān wǒ zuò qìchē qù xuéxiào. Zhè shì bàba de chē.",
        "How do my classmates go to school? Some ride bicycles, some take the bus. Some ride motorcycles. The bus is a bit slow; a car is a bit faster. Today I go to school by car. This is dad's car.",
    ),
    (
        "我们到学校了。学校的门是新的。教室里有很多桌子和椅子。我们班有两张新桌子。我觉得这个椅子有点儿小。有的椅子有点儿旧。新桌子有点儿贵。老师说：“你们用自己的桌子和椅子。”",
        "Wǒmen dào xuéxiào le. Xuéxiào de mén shì xīn de. Jiàoshì lǐ yǒu hěn duō zhuōzi hé yǐzi. Wǒmen bān yǒu liǎng zhāng xīn zhuōzi. Wǒ juéde zhège yǐzi yǒudiǎnr xiǎo. Yǒude yǐzi yǒudiǎnr jiù. Xīn zhuōzi yǒudiǎnr guì. Lǎoshī shuō: “Nǐmen yòng zìjǐ de zhuōzi hé yǐzi.”",
        "We arrived at school. The school gate is new. There are many desks and chairs in the classroom. Our class has two new desks. I think this chair is a bit small. Some chairs are a bit old. New desks are a bit expensive. The teacher said: “Use your own desk and chair.”",
    ),
    (
        "我检查自己的书包。书包里有我的电脑。妈妈刚给我买一台电脑。电脑是新的，有点儿贵。我跟妈妈一起去买电脑。现在我要用自己的电脑做练习。你用自己的电脑吗？",
        "Wǒ jiǎnchá zìjǐ de shūbāo. Shūbāo lǐ yǒu wǒ de diànnǎo. Māma gāng gěi wǒ mǎi yì tái diànnǎo. Diànnǎo shì xīn de, yǒudiǎnr guì. Wǒ gēn māma yìqǐ qù mǎi diànnǎo. Xiànzài wǒ yào yòng zìjǐ de diànnǎo zuò liànxí. Nǐ yòng zìjǐ de diànnǎo ma?",
        "I check my own backpack. There is my computer inside. Mom just bought me a computer. The computer is new — a bit expensive. I went with mom to buy it. Now I need to do exercises on my own computer. Do you use your own computer?",
    ),
    (
        "今天的练习有点儿多，也有点儿难。做练习的时候，我很认真。我自己写汉字。我自己学习汉语。老师说：“你们回家要多练习。多练习，汉语就好。”你喜欢就好。",
        "Jīntiān de liànxí yǒudiǎnr duō, yě yǒudiǎnr nán. Zuò liànxí de shíhou, wǒ hěn rènzhēn. Wǒ zìjǐ xiě Hànzì. Wǒ zìjǐ xuéxí Hànyǔ. Lǎoshī shuō: “Nǐmen huí jiā yào duō liànxí. Duō liànxí, Hànyǔ jiù hǎo.” Nǐ xǐhuan jiù hǎo.",
        "Today's exercises are a bit many, and a bit hard. When I do exercises, I am very focused. I write characters by myself. I study Chinese by myself. The teacher said: “Practice more at home. Practice more, and your Chinese will get better.” If you like it, that's good.",
    ),
    (
        "我们班只有十六个学生。我在这个班学习汉语。同班同学都很好。老师问：“你在哪个班学习？”我说：“我在这个班。”老师有一个女儿，也有一个儿子。女儿在我们学校。儿子在别的班。",
        "Wǒmen bān zhǐ yǒu shíliù ge xuéshēng. Wǒ zài zhège bān xuéxí Hànyǔ. Tóngbān tóngxué dōu hěn hǎo. Lǎoshī wèn: “Nǐ zài nǎge bān xuéxí?” Wǒ shuō: “Wǒ zài zhège bān.” Lǎoshī yǒu yí ge nǚ'ér, yě yǒu yí ge érzi. Nǚ'ér zài wǒmen xuéxiào. Érzi zài biéde bān.",
        "Our class has only sixteen students. I study Chinese in this class. My classmates are all very nice. The teacher asked: “Which class do you study in?” I said: “This one.” The teacher has a daughter and a son. The daughter is at our school. The son is in another class.",
    ),
    (
        "中午，我用筷子吃饭。吃完饭，我有点儿累。累了就休息吧，不要做了。休息的时候，我给妈妈打电话。妈妈问：“什么时候你回家？”我说：“下午四点。今天谁接我回家？”",
        "Zhōngwǔ, wǒ yòng kuàizi chīfàn. Chī wán fàn, wǒ yǒudiǎnr lèi. Lèi le jiù xiūxi ba, bú yào zuò le. Xiūxi de shíhou, wǒ gěi māma dǎ diànhuà. Māma wèn: “Shénme shíhou nǐ huí jiā?” Wǒ shuō: “Xiàwǔ sì diǎn. Jīntiān shéi jiē wǒ huí jiā?”",
        "At noon I eat with chopsticks. After lunch I am a bit tired. If you're tired, then rest — don't keep working. When I rest, I call mom. Mom asked: “When are you going home?” I said: “Four in the afternoon. Who is picking me up today?”",
    ),
    (
        "妈妈说：“爸爸接你回家。一会儿，你等他。”下午，我又做了很多练习。用电脑做练习的时候，不要看手机。练习多了就累。累了就休息。你累了吗？",
        "Māma shuō: “Bàba jiē nǐ huí jiā. Yíhuìr, nǐ děng tā.” Xiàwǔ, wǒ yòu zuò le hěn duō liànxí. Yòng diànnǎo zuò liànxí de shíhou, bú yào kàn shǒujī. Liànxí duō le jiù lèi. Lèi le jiù xiūxi. Nǐ lèi le ma?",
        "Mom said: “Dad will pick you up. Wait for him in a bit.” In the afternoon I did many more exercises. When you use the computer to practice, don't look at your phone. Too much practice and you get tired. If you're tired, then rest. Are you tired?",
    ),
    (
        "四点，我在学校门口等爸爸。爸爸开车来接我。他说：“让我送你回家吧。”我说：“好。今天谢谢爸爸送我，也谢谢爸爸接我。”回家的时候，我看到很多学生。",
        "Sì diǎn, wǒ zài xuéxiào ménkǒu děng bàba. Bàba kāichē lái jiē wǒ. Tā shuō: “Ràng wǒ sòng nǐ huí jiā ba.” Wǒ shuō: “Hǎo. Jīntiān xièxie bàba sòng wǒ, yě xièxie bàba jiē wǒ.” Huí jiā de shíhou, wǒ kàndào hěn duō xuéshēng.",
        "At four I wait for dad at the school gate. Dad drives over to pick me up. He said: “Let me take you home.” I said: “Okay. Thank you for dropping me off and picking me up today.” On the way home, I see many students.",
    ),
    (
        "有的学生自己回家，有的学生坐公共汽车回家。有一个同学骑自行车回家。他的自行车是新的，我的自行车有点儿旧。还有人骑摩托车。汽车很多。公共汽车上也有很多人。",
        "Yǒude xuéshēng zìjǐ huí jiā, yǒude xuéshēng zuò gōnggòng qìchē huí jiā. Yǒu yí ge tóngxué qí zìxíngchē huí jiā. Tā de zìxíngchē shì xīn de, wǒ de zìxíngchē yǒudiǎnr jiù. Hái yǒu rén qí mótuōchē. Qìchē hěn duō. Gōnggòng qìchē shang yě yǒu hěn duō rén.",
        "Some students go home by themselves, some take the bus. One classmate rides a bicycle home. His bicycle is new; mine is a bit old. Some people ride motorcycles. There are many cars. There are also many people on the bus.",
    ),
    (
        "晚上，我用电脑做练习。桌子上有电脑，椅子有点儿小，我坐着做练习。妈妈问我：“你用自己的钱了吗？”我说：“没有。电脑是妈妈买的。我用自己的电脑学习，用自己的钱买水。”",
        "Wǎnshang, wǒ yòng diànnǎo zuò liànxí. Zhuōzi shang yǒu diànnǎo, yǐzi yǒudiǎnr xiǎo, wǒ zuò zhe zuò liànxí. Māma wèn wǒ: “Nǐ yòng zìjǐ de qián le ma?” Wǒ shuō: “Méiyǒu. Diànnǎo shì māma mǎi de. Wǒ yòng zìjǐ de diànnǎo xuéxí, yòng zìjǐ de qián mǎi shuǐ.”",
        "In the evening I do exercises on the computer. The computer is on the desk. The chair is a bit small. I sit and practice. Mom asked: “Did you use your own money?” I said: “No. Mom bought the computer. I study on my own computer, and I use my own money to buy water.”",
    ),
    (
        "今天是开学的第一天。我坐汽车去学校，爸爸送我，爸爸接我。我有自己的自行车，可是今天没有骑。我在自己的班学习，用新电脑做练习。椅子有点儿旧，桌子是新的。新的东西有点儿贵。我有点儿累，可是我很喜欢今天。",
        "Jīntiān shì kāixué de dì yì tiān. Wǒ zuò qìchē qù xuéxiào, bàba sòng wǒ, bàba jiē wǒ. Wǒ yǒu zìjǐ de zìxíngchē, kěshì jīntiān méiyǒu qí. Wǒ zài zìjǐ de bān xuéxí, yòng xīn diànnǎo zuò liànxí. Yǐzi yǒudiǎnr jiù, zhuōzi shì xīn de. Xīn de dōngxi yǒudiǎnr guì. Wǒ yǒudiǎnr lèi, kěshì wǒ hěn xǐhuan jīntiān.",
        "Today is the first day of school. I went by car. Dad dropped me off and picked me up. I have my own bicycle, but I didn't ride it today. I study in my own class and do exercises on a new computer. The chair is a bit old; the desk is new. New things are a bit expensive. I am a bit tired, but I really liked today.",
    ),
    (
        "你们什么时候开学？你们怎么去学校？坐公共汽车，还是骑自行车，还是爸爸开车送你们？下课的时候，谁接你们回家？你们用电脑做练习吗？今天的练习多不多？累了就休息，好吗？",
        "Nǐmen shénme shíhou kāixué? Nǐmen zěnme qù xuéxiào? Zuò gōnggòng qìchē, háishì qí zìxíngchē, háishì bàba kāichē sòng nǐmen? Xiàkè de shíhou, shéi jiē nǐmen huí jiā? Nǐmen yòng diànnǎo zuò liànxí ma? Jīntiān de liànxí duō bu duō? Lèi le jiù xiūxi, hǎo ma?",
        "When does your school start? How do you go to school? By bus, by bicycle, or does dad drive you? When class ends, who picks you up? Do you do exercises on a computer? Are today's exercises many? If you're tired, then rest, okay?",
    ),
    (
        "好，今天的视频就到这儿。谢谢大家看我的开学小视频！下个星期一见！你们要多练习汉语。自己写汉字，自己学习，就好。再见！",
        "Hǎo, jīntiān de shìpín jiù dào zhèr. Xièxie dàjiā kàn wǒ de kāixué xiǎo shìpín! Xià ge xīngqīyī jiàn! Nǐmen yào duō liànxí Hànyǔ. Zìjǐ xiě Hànzì, zìjǐ xuéxí, jiù hǎo. Zàijiàn!",
        "Okay, that's all for today's video. Thanks for watching my back-to-school vlog! See you next Monday! Practice Chinese more. Write characters yourself, study yourself — then it's good. Bye!",
    ),
]


def tokenize(text: str) -> list[dict]:
    tokens: list[dict] = []
    i = 0
    n = len(text)
    plain = []

    def flush():
        nonlocal plain
        if plain:
            tokens.append({"t": "".join(plain)})
            plain = []

    while i < n:
        matched = False
        for form, vid in MATCHERS:
            if text.startswith(form, i):
                blocked = BLOCKED_IF_INSIDE.get(vid, ())
                if any(text.startswith(b, i) for b in blocked if b != form):
                    continue
                # 下个: highlight only 下, keep 个 as plain after
                flush()
                if vid == "xia" and form == "下个":
                    tokens.append({"t": "下", "new": vid})
                    plain.append("个")
                    i += 2
                elif vid == "kai" and form == "开车":
                    # mark 开 only when we want 开; 开车 is also its own word.
                    # If both 开 and 开车 exist, prefer marking 开车 as kaiche.
                    tokens.append({"t": "开车", "new": "kaiche"})
                    i += 2
                else:
                    tokens.append({"t": form, "new": vid})
                    i += len(form)
                matched = True
                break
        if not matched:
            plain.append(text[i])
            i += 1
    flush()
    return tokens


def hanzi_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def main() -> None:
    paragraphs = []
    used: set[str] = set()
    total_hanzi = 0
    for zh, py, en in PARAS:
        toks = tokenize(zh)
        for t in toks:
            if t.get("new"):
                used.add(t["new"])
        total_hanzi += hanzi_count(zh)
        paragraphs.append({"tokens": toks, "py": py, "en": en, "zh": zh})

    missing = [w["id"] for w in VOCAB if w["id"] not in used and w["id"] != "kai"]
    # 开 is folded into 开车 by design
    payload = {
        "lesson": 14,
        "title": "开学这一天",
        "title_py": "Kāixué zhè yì tiān",
        "title_en": "The day school starts",
        "level": "HSK 1 → Lesson 14",
        "hanzi_count": total_hanzi,
        "vocab": [{k: v for k, v in w.items() if k != "match"} for w in VOCAB],
        "script": paragraphs,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    body = (
        "/* Generated by scripts/_gen_hsk_lesson_14.py — do not edit by hand. */\n"
        "window.HSK_LESSON_14 = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n"
    )
    OUT.write_text(body, encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"hanzi_count={total_hanzi}")
    print(f"paragraphs={len(paragraphs)}")
    print(f"vocab={len(VOCAB)} used={len(used)}")
    if missing:
        print("MISSING highlights:", missing)


if __name__ == "__main__":
    main()
