#!/usr/bin/env python3
"""Generate HSK lesson 15 data (wedding / plans)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hsk_gen_lib import emit_lesson

VOCAB = [
    {
        "id": "yue",
        "hanzi": "月",
        "pinyin": "yuè",
        "vi": "tháng",
        "en": "month",
        "pos": "noun",
        "examples": [
            {"zh": "你几月去中国？", "py": "Nǐ jǐ yuè qù Zhōngguó?", "vi": "Bạn tháng mấy đi Trung Quốc?", "en": "Which month are you going to China?"},
            {"zh": "下个月我回越南。", "py": "Xià ge yuè wǒ huí Yuènán.", "vi": "Tháng sau tôi về Việt Nam.", "en": "Next month I'm going back to Vietnam."},
        ],
    },
    {
        "id": "jiehun",
        "hanzi": "结婚",
        "pinyin": "jiéhūn",
        "vi": "kết hôn",
        "en": "to get married",
        "pos": "verb",
        "examples": [
            {"zh": "你结婚了吗？", "py": "Nǐ jiéhūn le ma?", "vi": "Bạn đã kết hôn chưa?", "en": "Are you married?"},
            {"zh": "你跟谁结婚？", "py": "Nǐ gēn shéi jiéhūn?", "vi": "Bạn kết hôn với ai?", "en": "Who are you marrying?"},
        ],
    },
    {
        "id": "neng",
        "hanzi": "能",
        "pinyin": "néng",
        "vi": "có thể",
        "en": "can / to be able to",
        "pos": "verb",
        "match": ["不能", "能"],
        "examples": [
            {"zh": "你能帮我吗？", "py": "Nǐ néng bāng wǒ ma?", "vi": "Bạn có thể giúp tôi không?", "en": "Can you help me?"},
            {"zh": "我能说汉语。", "py": "Wǒ néng shuō Hànyǔ.", "vi": "Tôi có thể nói tiếng Trung.", "en": "I can speak Chinese."},
        ],
    },
    {
        "id": "lai",
        "hanzi": "来",
        "pinyin": "lái",
        "vi": "đến, tới",
        "en": "to come",
        "pos": "verb",
        "examples": [
            {"zh": "你能来接我吗？", "py": "Nǐ néng lái jiē wǒ ma?", "vi": "Bạn có thể đến đón tôi không?", "en": "Can you come pick me up?"},
            {"zh": "你来我家吃饭吧。", "py": "Nǐ lái wǒ jiā chīfàn ba.", "vi": "Bạn đến nhà tôi ăn cơm đi.", "en": "Come to my place for dinner."},
        ],
    },
    {
        "id": "canjia",
        "hanzi": "参加",
        "pinyin": "cānjiā",
        "vi": "tham gia",
        "en": "to attend / take part in",
        "pos": "verb",
        "examples": [
            {"zh": "你能来参加吗？", "py": "Nǐ néng lái cānjiā ma?", "vi": "Bạn có thể đến tham gia không?", "en": "Can you come and attend?"},
            {"zh": "我有点儿忙，我不能去参加。", "py": "Wǒ yǒudiǎnr máng, wǒ bù néng qù cānjiā.", "vi": "Tôi hơi bận, tôi không thể đi tham gia.", "en": "I'm a bit busy, I can't go."},
        ],
    },
    {
        "id": "hunli",
        "hanzi": "婚礼",
        "pinyin": "hūnlǐ",
        "vi": "hôn lễ, đám cưới",
        "en": "wedding",
        "pos": "noun",
        "examples": [
            {"zh": "你能来参加我们的婚礼吗？", "py": "Nǐ néng lái cānjiā wǒmen de hūnlǐ ma?", "vi": "Bạn có thể đến tham gia hôn lễ của chúng tôi không?", "en": "Can you come to our wedding?"},
        ],
    },
    {
        "id": "zhufu",
        "hanzi": "祝福",
        "pinyin": "zhùfú",
        "vi": "chúc phúc, chúc mừng",
        "en": "to bless / best wishes",
        "pos": "verb/noun",
        "examples": [
            {"zh": "祝福你们！", "py": "Zhùfú nǐmen!", "vi": "Chúc mừng các bạn!", "en": "Best wishes to you both!"},
        ],
    },
    {
        "id": "yiding",
        "hanzi": "一定",
        "pinyin": "yídìng",
        "vi": "nhất định",
        "en": "certainly / must",
        "pos": "adv",
        "examples": [
            {"zh": "我一定去参加你们的婚礼。", "py": "Wǒ yídìng qù cānjiā nǐmen de hūnlǐ.", "vi": "Tôi nhất định đến tham gia đám cưới của các bạn.", "en": "I will definitely attend your wedding."},
            {"zh": "你做的菜一定很好吃。", "py": "Nǐ zuò de cài yídìng hěn hǎochī.", "vi": "Món cậu làm nhất định sẽ rất ngon.", "en": "The dish you make will certainly be delicious."},
        ],
    },
    {
        "id": "pai",
        "hanzi": "拍",
        "pinyin": "pāi",
        "vi": "chụp (ảnh)",
        "en": "to take (a photo)",
        "pos": "verb",
        "examples": [
            {"zh": "你跟我一起拍吧！", "py": "Nǐ gēn wǒ yìqǐ pāi ba!", "vi": "Bạn chụp cùng tôi đi!", "en": "Take a photo with me!"},
            {"zh": "我想用手机拍。", "py": "Wǒ xiǎng yòng shǒujī pāi.", "vi": "Tôi muốn chụp bằng điện thoại.", "en": "I want to shoot with my phone."},
        ],
    },
    {
        "id": "hunshazhao",
        "hanzi": "婚纱照",
        "pinyin": "hūnshāzhào",
        "vi": "ảnh cưới",
        "en": "wedding photos",
        "pos": "noun",
        "examples": [
            {"zh": "我想去北京拍婚纱照。", "py": "Wǒ xiǎng qù Běijīng pāi hūnshāzhào.", "vi": "Tôi muốn đi Bắc Kinh chụp ảnh cưới.", "en": "I want to go to Beijing to take wedding photos."},
        ],
    },
    {
        "id": "paizhao",
        "hanzi": "拍照",
        "pinyin": "pāizhào",
        "vi": "chụp ảnh",
        "en": "to take a photo",
        "pos": "verb",
        "examples": [
            {"zh": "这里不能拍照。", "py": "Zhèlǐ bù néng pāizhào.", "vi": "Ở đây không được chụp ảnh.", "en": "You can't take photos here."},
        ],
    },
    {
        "id": "dasuan",
        "hanzi": "打算",
        "pinyin": "dǎsuàn",
        "vi": "dự định, kế hoạch",
        "en": "to plan / intend",
        "pos": "verb",
        "examples": [
            {"zh": "你打算什么时候结婚？", "py": "Nǐ dǎsuàn shénme shíhou jiéhūn?", "vi": "Bạn dự định bao giờ kết hôn?", "en": "When do you plan to get married?"},
            {"zh": "我们打算今年十二月结婚。", "py": "Wǒmen dǎsuàn jīnnián shí'èr yuè jiéhūn.", "vi": "Chúng tôi dự định tháng 12 năm nay kết hôn.", "en": "We plan to get married this December."},
        ],
    },
    {
        "id": "weishenme",
        "hanzi": "为什么",
        "pinyin": "wèishénme",
        "vi": "tại sao",
        "en": "why",
        "pos": "adv",
        "examples": [
            {"zh": "你为什么不来参加我们的婚礼？", "py": "Nǐ wèishénme bù lái cānjiā wǒmen de hūnlǐ?", "vi": "Tại sao bạn không đến tham gia hôn lễ của chúng tôi?", "en": "Why aren't you coming to our wedding?"},
        ],
    },
    {
        "id": "yinwei",
        "hanzi": "因为",
        "pinyin": "yīnwèi",
        "vi": "bởi vì",
        "en": "because",
        "pos": "conj",
        "examples": [
            {"zh": "因为没有钱。", "py": "Yīnwèi méiyǒu qián.", "vi": "Bởi vì không có tiền.", "en": "Because I don't have money."},
            {"zh": "因为他是好人。", "py": "Yīnwèi tā shì hǎo rén.", "vi": "Bởi vì anh ấy là người tốt.", "en": "Because he is a good person."},
        ],
    },
    {
        "id": "di",
        "hanzi": "第",
        "pinyin": "dì",
        "vi": "thứ (đệ)",
        "en": "ordinal prefix (first, second…)",
        "pos": "prefix",
        "examples": [
            {"zh": "这是我第一次参加婚礼。", "py": "Zhè shì wǒ dì yí cì cānjiā hūnlǐ.", "vi": "Đây là lần đầu tôi tham gia hôn lễ.", "en": "This is my first time attending a wedding."},
        ],
    },
    {
        "id": "jianmian",
        "hanzi": "见面",
        "pinyin": "jiànmiàn",
        "vi": "gặp mặt",
        "en": "to meet",
        "pos": "verb",
        "examples": [
            {"zh": "我很想跟他见面。", "py": "Wǒ hěn xiǎng gēn tā jiànmiàn.", "vi": "Tôi rất muốn gặp anh ấy.", "en": "I really want to meet him."},
            {"zh": "我们见面了。", "py": "Wǒmen jiànmiàn le.", "vi": "Chúng tôi đã gặp mặt rồi.", "en": "We have met."},
        ],
    },
    {
        "id": "difang",
        "hanzi": "地方",
        "pinyin": "dìfang",
        "vi": "nơi (个)",
        "en": "place",
        "pos": "noun",
        "examples": [
            {"zh": "我觉得这个地方很好。", "py": "Wǒ juéde zhège dìfang hěn hǎo.", "vi": "Tôi cảm thấy nơi này rất đẹp.", "en": "I think this place is really nice."},
            {"zh": "那是我们第一次见面的地方。", "py": "Nà shì wǒmen dì yí cì jiànmiàn de dìfang.", "vi": "Đó là nơi lần đầu chúng tôi gặp nhau.", "en": "That is the place where we first met."},
        ],
    },
    {
        "id": "juxing",
        "hanzi": "举行",
        "pinyin": "jǔxíng",
        "vi": "tổ chức",
        "en": "to hold (an event)",
        "pos": "verb",
        "examples": [
            {"zh": "你们打算在哪儿举行婚礼？", "py": "Nǐmen dǎsuàn zài nǎr jǔxíng hūnlǐ?", "vi": "Các bạn dự định tổ chức hôn lễ ở đâu?", "en": "Where do you plan to hold the wedding?"},
        ],
    },
    {
        "id": "jiaotang",
        "hanzi": "教堂",
        "pinyin": "jiàotáng",
        "vi": "nhà thờ",
        "en": "church",
        "pos": "noun",
        "examples": [
            {"zh": "他们打算在教堂举行婚礼。", "py": "Tāmen dǎsuàn zài jiàotáng jǔxíng hūnlǐ.", "vi": "Họ dự định tổ chức hôn lễ ở nhà thờ.", "en": "They plan to hold the wedding in a church."},
        ],
    },
    {
        "id": "jiaju",
        "hanzi": "家具",
        "pinyin": "jiājù",
        "vi": "đồ gia dụng",
        "en": "furniture",
        "pos": "noun",
        "examples": [
            {"zh": "我打算去买一些家具。", "py": "Wǒ dǎsuàn qù mǎi yìxiē jiājù.", "vi": "Tôi dự định đi mua một ít đồ gia dụng.", "en": "I plan to buy some furniture."},
        ],
    },
    {
        "id": "chang",
        "hanzi": "常",
        "pinyin": "cháng",
        "vi": "thường",
        "en": "often",
        "pos": "adv",
        "match": ["常常", "常"],
        "examples": [
            {"zh": "我常常骑自行车去学校。", "py": "Wǒ chángcháng qí zìxíngchē qù xuéxiào.", "vi": "Tôi thường đạp xe đến trường.", "en": "I often ride a bike to school."},
            {"zh": "你常喝咖啡吗？", "py": "Nǐ cháng hē kāfēi ma?", "vi": "Bạn có hay uống cà phê không?", "en": "Do you often drink coffee?"},
        ],
    },
    {
        "id": "liwu",
        "hanzi": "礼物",
        "pinyin": "lǐwù",
        "vi": "quà",
        "en": "gift",
        "pos": "noun",
        "examples": [
            {"zh": "你打算买什么礼物？", "py": "Nǐ dǎsuàn mǎi shénme lǐwù?", "vi": "Bạn định mua quà gì?", "en": "What gift do you plan to buy?"},
            {"zh": "你送她什么礼物？", "py": "Nǐ sòng tā shénme lǐwù?", "vi": "Bạn tặng cô ấy quà gì?", "en": "What gift are you giving her?"},
        ],
    },
    {
        "id": "hongbao",
        "hanzi": "红包",
        "pinyin": "hóngbāo",
        "vi": "tiền mừng, lì xì",
        "en": "red envelope",
        "pos": "noun",
        "examples": [
            {"zh": "参加婚礼的时候越南人常送红包。", "py": "Cānjiā hūnlǐ de shíhou Yuènán rén cháng sòng hóngbāo.", "vi": "Khi tham gia hôn lễ, người Việt thường tặng tiền mừng.", "en": "When attending a wedding, Vietnamese people often give a red envelope."},
        ],
    },
    {
        "id": "zhidao",
        "hanzi": "知道",
        "pinyin": "zhīdào",
        "vi": "biết",
        "en": "to know",
        "pos": "verb",
        "examples": [
            {"zh": "你知道他什么时候结婚吗？", "py": "Nǐ zhīdào tā shénme shíhou jiéhūn ma?", "vi": "Bạn có biết khi nào anh ấy kết hôn không?", "en": "Do you know when he is getting married?"},
            {"zh": "我知道了。", "py": "Wǒ zhīdào le.", "vi": "Tôi biết rồi.", "en": "I got it."},
        ],
    },
    {
        "id": "yinggai",
        "hanzi": "应该",
        "pinyin": "yīnggāi",
        "vi": "nên",
        "en": "should",
        "pos": "verb",
        "match": ["不应该", "应该"],
        "examples": [
            {"zh": "你应该多练习。", "py": "Nǐ yīnggāi duō liànxí.", "vi": "Bạn nên luyện tập nhiều hơn.", "en": "You should practice more."},
            {"zh": "我应该送什么礼物？", "py": "Wǒ yīnggāi sòng shénme lǐwù?", "vi": "Tôi nên tặng quà gì?", "en": "What gift should I give?"},
        ],
    },
]

BLOCKED = {
    "pai": ("拍照", "婚纱照"),
}

# Outside-lesson words worth noting in this dialogue
EXTRAS = [
    {"id": "xiaoxi", "hanzi": "消息", "pinyin": "xiāoxi", "vi": "tin tức, tin", "en": "news / message"},
    {"id": "fengjing", "hanzi": "风景", "pinyin": "fēngjǐng", "vi": "phong cảnh", "en": "scenery"},
    {"id": "kongqi", "hanzi": "空气", "pinyin": "kōngqì", "vi": "không khí", "en": "air"},
    {"id": "duile", "hanzi": "对了", "pinyin": "duìle", "vi": "phải rồi; à đúng rồi", "en": "by the way / oh right"},
    {"id": "xiangshi", "hanzi": "相识", "pinyin": "xiāngshí", "vi": "quen biết", "en": "to get to know each other"},
    {"id": "langman", "hanzi": "浪漫", "pinyin": "làngmàn", "vi": "lãng mạn", "en": "romantic"},
    {"id": "meili", "hanzi": "美丽", "pinyin": "měilì", "vi": "xinh đẹp, đẹp", "en": "beautiful"},
    {"id": "dasao", "hanzi": "打扫", "pinyin": "dǎsǎo", "vi": "dọn dẹp", "en": "to clean"},
    {"id": "bangmang", "hanzi": "帮忙", "pinyin": "bāngmáng", "vi": "giúp đỡ", "en": "to help"},
    {"id": "xingfu", "hanzi": "幸福", "pinyin": "xìngfú", "vi": "hạnh phúc", "en": "happiness / happy"},
    {"id": "tiqian", "hanzi": "提前", "pinyin": "tíqián", "vi": "trước, sớm hơn", "en": "in advance"},
]

# Everyday reaction phrases (not lesson vocab)
EMOTIONS = [
    {"hanzi": "太好了", "pinyin": "tài hǎo le", "vi": "Tuyệt quá!", "en": "Great!"},
    {"hanzi": "太棒了", "pinyin": "tài bàng le", "vi": "Quá đỉnh!", "en": "Awesome!"},
    {"hanzi": "真的吗", "pinyin": "zhēn de ma", "vi": "Thật á?", "en": "Really?"},
    {"hanzi": "没问题", "pinyin": "méi wèntí", "vi": "Không vấn đề gì!", "en": "No problem!"},
    {"hanzi": "噢", "pinyin": "ò", "vi": "Ồ", "en": "Oh"},
]

# A/B wedding invitation dialogue — (speaker, zh, py, en, vi)
PARAS = [
    (
        "A",
        "下个月十二号，我打算同女朋友结婚，举行一场浪漫的婚礼。你能来参加吗？",
        "Xià ge yuè shí'èr hào, wǒ dǎsuàn tóng nǚpéngyou jiéhūn, jǔxíng yì chǎng làngmàn de hūnlǐ. Nǐ néng lái cānjiā ma?",
        "Next month on the 12th, I plan to marry my girlfriend and hold a romantic wedding. Can you come?",
        "Tháng sau ngày 12, tôi dự định kết hôn với bạn gái, tổ chức một hôn lễ lãng mạn. Bạn có thể đến tham gia không?",
    ),
    (
        "B",
        "太好了！一定去！这是我第一次收到你结婚的消息。你们打算在哪儿举行？",
        "Tài hǎo le! Yídìng qù! Zhè shì wǒ dì yí cì shōudào nǐ jiéhūn de xiāoxi. Nǐmen dǎsuàn zài nǎr jǔxíng?",
        "Great! I'll definitely go! This is the first time I've heard you're getting married. Where do you plan to hold it?",
        "Tuyệt quá! Nhất định đi! Đây là lần đầu tiên tôi nhận được tin bạn kết hôn. Các bạn định tổ chức ở đâu?",
    ),
    (
        "A",
        "我们打算在那个美丽的教堂举行，那是我们第一次相识、见面的地方。",
        "Wǒmen dǎsuàn zài nàge měilì de jiàotáng jǔxíng, nà shì wǒmen dì yí cì xiāngshí, jiànmiàn de dìfang.",
        "We plan to hold it at that beautiful church — that's where we first got to know each other and met.",
        "Chúng tôi dự định tổ chức ở nhà thờ đẹp đó, đó là nơi lần đầu tiên chúng tôi quen biết và gặp mặt.",
    ),
    (
        "B",
        "噢，我知道那个地方，风景很美。为什么选在那里呢？",
        "Ò, wǒ zhīdào nàge dìfang, fēngjǐng hěn měi. Wèishénme xuǎn zài nàlǐ ne?",
        "Oh, I know that place — the scenery is beautiful. Why choose there?",
        "Ồ, tôi biết nơi đó, phong cảnh rất đẹp. Tại sao lại chọn ở đó vậy?",
    ),
    (
        "A",
        "因为那里的空气很好，我们很喜欢。对了，我们最近还买了一些新家具，常常去那儿打扫。",
        "Yīnwèi nàlǐ de kōngqì hěn hǎo, wǒmen hěn xǐhuan. Duìle, wǒmen zuìjìn hái mǎi le yìxiē xīn jiājù, chángcháng qù nàr dǎsǎo.",
        "Because the air there is great, and we really like it. Oh right — we recently bought some new furniture and often go there to clean.",
        "Bởi vì không khí ở đó rất tốt, chúng tôi rất thích. Phải rồi, dạo gần đây chúng tôi còn mua một ít đồ gia dụng mới, thường hay đến đó dọn dẹp.",
    ),
    (
        "B",
        "太棒了！拍照的时候能找人帮忙吗？我朋友很会拍，特别是婚纱照。",
        "Tài bàng le! Pāizhào de shíhou néng zhǎo rén bāngmáng ma? Wǒ péngyou hěn huì pāi, tèbié shì hūnshāzhào.",
        "Awesome! When taking photos, can we find someone to help? My friend is great at shooting, especially wedding photos.",
        "Quá đỉnh! Lúc chụp ảnh có thể tìm người giúp không? Bạn tôi chụp rất giỏi, đặc biệt là ảnh cưới.",
    ),
    (
        "A",
        "真的吗？那太好了！我正想找人来拍呢。",
        "Zhēn de ma? Nà tài hǎo le! Wǒ zhèng xiǎng zhǎo rén lái pāi ne.",
        "Really? That's great! I was just looking for someone to shoot.",
        "Thật á? Thế thì tốt quá! Tôi đang muốn tìm người đến chụp đây.",
    ),
    (
        "B",
        "没问题！对了，参加婚礼我应该送什么礼物？送红包行吗？",
        "Méi wèntí! Duìle, cānjiā hūnlǐ wǒ yīnggāi sòng shénme lǐwù? Sòng hóngbāo xíng ma?",
        "No problem! By the way, what gift should I give for the wedding? Is a red envelope okay?",
        "Không vấn đề gì! Đúng rồi, đi dự đám cưới tôi nên tặng quà gì? Tặng phong bì (tiền mừng) có được không?",
    ),
    (
        "A",
        "送红包很好，谢谢你！提前祝福我们吧！",
        "Sòng hóngbāo hěn hǎo, xièxie nǐ! Tíqián zhùfú wǒmen ba!",
        "A red envelope is perfect, thank you! Please give us your blessings in advance!",
        "Tặng phong bì rất tốt, cảm ơn bạn! Hãy chúc phúc cho chúng tôi trước nhé!",
    ),
    (
        "B",
        "祝你们幸福！",
        "Zhù nǐmen xìngfú!",
        "Wish you both happiness!",
        "Chúc các bạn hạnh phúc!",
    ),
]


if __name__ == "__main__":
    emit_lesson(
        lesson=15,
        title="朋友的婚礼",
        title_py="Péngyou de hūnlǐ",
        title_en="A friend's wedding",
        vocab=VOCAB,
        paras=PARAS,
        blocked_if_inside=BLOCKED,
        extras=EXTRAS,
        emotions=EMOTIONS,
    )
