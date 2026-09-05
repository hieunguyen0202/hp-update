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

PARAS = [
    (
        "大家好！今天我给大家拍一个小视频。你们知道吗？我的好朋友下个月结婚！她跟她的男朋友结婚。我很高兴，也有点儿忙。",
        "Dàjiā hǎo! Jīntiān wǒ gěi dàjiā pāi yí ge xiǎo shìpín. Nǐmen zhīdào ma? Wǒ de hǎo péngyou xià ge yuè jiéhūn! Tā gēn tā de nánpéngyou jiéhūn. Wǒ hěn gāoxìng, yě yǒudiǎnr máng.",
        "Hello everyone! Today I'm filming a short vlog. Do you know? My good friend is getting married next month! She is marrying her boyfriend. I'm very happy, and also a bit busy.",
    ),
    (
        "你知道他们什么时候结婚吗？他们打算今年十二月结婚。十二月是今年最后一个月。下个月就是十二月。一个月以后，他们就结婚了。",
        "Nǐ zhīdào tāmen shénme shíhou jiéhūn ma? Tāmen dǎsuàn jīnnián shí'èr yuè jiéhūn. Shí'èr yuè shì jīnnián zuìhòu yí ge yuè. Xià ge yuè jiù shì shí'èr yuè. Yí ge yuè yǐhòu, tāmen jiù jiéhūn le.",
        "Do you know when they are getting married? They plan to get married this December. December is the last month of this year. Next month is December. In one month, they will be married.",
    ),
    (
        "她问我：“你能来参加我们的婚礼吗？”我说：“我一定去参加你们的婚礼！”祝福你们！她很高兴。她说：“太好了，你一定要来。”",
        "Tā wèn wǒ: “Nǐ néng lái cānjiā wǒmen de hūnlǐ ma?” Wǒ shuō: “Wǒ yídìng qù cānjiā nǐmen de hūnlǐ!” Zhùfú nǐmen! Tā hěn gāoxìng. Tā shuō: “Tài hǎo le, nǐ yídìng yào lái.”",
        "She asked me: “Can you come to our wedding?” I said: “I will definitely attend your wedding!” Best wishes! She was very happy. She said: “Great — you must come.”",
    ),
    (
        "有的同学不能来参加，因为他们很忙。她问：“你为什么不来参加我们的婚礼？”同学说：“因为我下个月去中国。我不能来。”她说：“知道了，没关系。”",
        "Yǒude tóngxué bù néng lái cānjiā, yīnwèi tāmen hěn máng. Tā wèn: “Nǐ wèishénme bù lái cānjiā wǒmen de hūnlǐ?” Tóngxué shuō: “Yīnwèi wǒ xià ge yuè qù Zhōngguó. Wǒ bù néng lái.” Tā shuō: “Zhīdào le, méi guānxi.”",
        "Some classmates cannot come, because they are busy. She asked: “Why aren't you coming to our wedding?” A classmate said: “Because I'm going to China next month. I can't come.” She said: “I see — that's okay.”",
    ),
    (
        "他们打算去北京拍婚纱照。她问我：“你打算去哪儿拍婚纱照？”我说：“我还没结婚。你呢？你想怎么拍？”她说：“我想用手机拍，也想请人拍。”",
        "Tāmen dǎsuàn qù Běijīng pāi hūnshāzhào. Tā wèn wǒ: “Nǐ dǎsuàn qù nǎr pāi hūnshāzhào?” Wǒ shuō: “Wǒ hái méi jiéhūn. Nǐ ne? Nǐ xiǎng zěnme pāi?” Tā shuō: “Wǒ xiǎng yòng shǒujī pāi, yě xiǎng qǐng rén pāi.”",
        "They plan to go to Beijing to take wedding photos. She asked me: “Where do you plan to take wedding photos?” I said: “I'm not married yet. What about you? How do you want to shoot?” She said: “I want to shoot with a phone, and also hire someone.”",
    ),
    (
        "为什么去北京拍？因为那个地方很好。那是他们第一次见面的地方。她说：“我觉得这个地方很好。我要去那个地方拍照。”第一次见面的地方，一定很好。",
        "Wèishénme qù Běijīng pāi? Yīnwèi nàge dìfang hěn hǎo. Nà shì tāmen dì yí cì jiànmiàn de dìfang. Tā shuō: “Wǒ juéde zhège dìfang hěn hǎo. Wǒ yào qù nàge dìfang pāizhào.” Dì yí cì jiànmiàn de dìfang, yídìng hěn hǎo.",
        "Why Beijing? Because that place is beautiful. That is where they first met. She said: “I think this place is really nice. I want to go there to take photos.” The place of a first meeting is certainly special.",
    ),
    (
        "这里有的地方不能拍照。她问：“我能在这儿拍照吗？”有人说：“这里不能拍照。”她说：“知道了。那我们去别的地方拍婚纱照吧。”",
        "Zhèlǐ yǒude dìfang bù néng pāizhào. Tā wèn: “Wǒ néng zài zhèr pāizhào ma?” Yǒu rén shuō: “Zhèlǐ bù néng pāizhào.” Tā shuō: “Zhīdào le. Nà wǒmen qù biéde dìfang pāi hūnshāzhào ba.”",
        "In some places here you cannot take photos. She asked: “Can I take photos here?” Someone said: “No photos here.” She said: “Got it. Then let's take the wedding photos somewhere else.”",
    ),
    (
        "你们打算在哪儿举行婚礼？他们打算在教堂举行婚礼。英国人常常在教堂举行婚礼。她问：“请问大教堂在哪儿？”我说：“我知道，我能带你去。”",
        "Nǐmen dǎsuàn zài nǎr jǔxíng hūnlǐ? Tāmen dǎsuàn zài jiàotáng jǔxíng hūnlǐ. Yīngguó rén chángcháng zài jiàotáng jǔxíng hūnlǐ. Tā wèn: “Qǐngwèn dà jiàotáng zài nǎr?” Wǒ shuō: “Wǒ zhīdào, wǒ néng dài nǐ qù.”",
        "Where do you plan to hold the wedding? They plan to hold it in a church. British people often hold weddings in a church. She asked: “Where is the big church?” I said: “I know — I can take you there.”",
    ),
    (
        "结婚以后，他们打算去买一些家具。下个星期一她打算跟他一起去买家具。新家要有桌子、椅子，也要有新家具。家具有点儿贵，可是应该买。",
        "Jiéhūn yǐhòu, tāmen dǎsuàn qù mǎi yìxiē jiājù. Xià ge xīngqīyī tā dǎsuàn gēn tā yìqǐ qù mǎi jiājù. Xīn jiā yào yǒu zhuōzi, yǐzi, yě yào yǒu xīn jiājù. Jiājù yǒudiǎnr guì, kěshì yīnggāi mǎi.",
        "After they get married, they plan to buy some furniture. Next Monday she plans to go buy furniture with him. A new home needs desks and chairs, and also new furniture. Furniture is a bit expensive, but they should buy it.",
    ),
    (
        "我应该送什么礼物？你打算买什么礼物？参加婚礼的时候，越南人常送红包。我说：“我打算送红包。”她笑了：“红包很好。谢谢你的礼物，也谢谢你来参加。”",
        "Wǒ yīnggāi sòng shénme lǐwù? Nǐ dǎsuàn mǎi shénme lǐwù? Cānjiā hūnlǐ de shíhou, Yuènán rén cháng sòng hóngbāo. Wǒ shuō: “Wǒ dǎsuàn sòng hóngbāo.” Tā xiào le: “Hóngbāo hěn hǎo. Xièxie nǐ de lǐwù, yě xièxie nǐ lái cānjiā.”",
        "What gift should I give? What gift do you plan to buy? When attending a wedding, Vietnamese people often give a red envelope. I said: “I plan to give a red envelope.” She smiled: “A red envelope is great. Thanks for the gift, and thanks for coming.”",
    ),
    (
        "这是我第一次参加婚礼。第一个月我认识她，现在她要结婚了。第一次见面的地方，我还记得。第一次喝咖啡的地方，也在那个城市。时间过得真快。",
        "Zhè shì wǒ dì yí cì cānjiā hūnlǐ. Dì yí ge yuè wǒ rènshi tā, xiànzài tā yào jiéhūn le. Dì yí cì jiànmiàn de dìfang, wǒ hái jìde. Dì yí cì hē kāfēi de dìfang, yě zài nàge chéngshì. Shíjiān guò de zhēn kuài.",
        "This is my first time attending a wedding. The first month I met her — and now she is getting married. I still remember the place where we first met. The place where I first drank coffee is in that city too. Time goes so fast.",
    ),
    (
        "婚礼那天，我一定来。我能说汉语，能帮他们拍。她说：“你能帮我们拍婚纱照吗？你能给我们拍吗？”我说：“我能。我一定帮你拍。你跟我一起拍吧！”",
        "Hūnlǐ nà tiān, wǒ yídìng lái. Wǒ néng shuō Hànyǔ, néng bāng tāmen pāi. Tā shuō: “Nǐ néng bāng wǒmen pāi hūnshāzhào ma? Nǐ néng gěi wǒmen pāi ma?” Wǒ shuō: “Wǒ néng. Wǒ yídìng bāng nǐ pāi. Nǐ gēn wǒ yìqǐ pāi ba!”",
        "On the wedding day I will definitely come. I can speak Chinese, and I can help them shoot. She said: “Can you help us take the wedding photos? Can you shoot for us?” I said: “I can. I will definitely help you shoot. Take one with me!”",
    ),
    (
        "我还应该做什么？我应该早一点儿来教堂。我不应该迟到。我不应该开车去，因为我不能喝酒以后开车。我打算坐公共汽车去那个地方。",
        "Wǒ hái yīnggāi zuò shénme? Wǒ yīnggāi zǎo yìdiǎnr lái jiàotáng. Wǒ bù yīnggāi chídào. Wǒ bù yīnggāi kāichē qù, yīnwèi wǒ bù néng hējiǔ yǐhòu kāichē. Wǒ dǎsuàn zuò gōnggòng qìchē qù nàge dìfang.",
        "What else should I do? I should come to the church a bit early. I shouldn't be late. I shouldn't drive, because I can't drive after drinking. I plan to take the bus to that place.",
    ),
    (
        "你们呢？你们结婚了吗？你打算什么时候结婚？你跟谁结婚？你们打算在哪儿举行婚礼？在教堂，还是在别的地方？你为什么选那个地方？因为那儿很好吗？",
        "Nǐmen ne? Nǐmen jiéhūn le ma? Nǐ dǎsuàn shénme shíhou jiéhūn? Nǐ gēn shéi jiéhūn? Nǐmen dǎsuàn zài nǎr jǔxíng hūnlǐ? Zài jiàotáng, háishì zài biéde dìfang? Nǐ wèishénme xuǎn nàge dìfang? Yīnwèi nàr hěn hǎo ma?",
        "What about you? Are you married? When do you plan to get married? Who are you marrying? Where do you plan to hold the wedding? In a church, or somewhere else? Why that place? Because it's nice?",
    ),
    (
        "参加别人的婚礼的时候，你常送什么礼物？你常送红包吗？你知道应该送什么吗？第一次参加婚礼，我不知道。现在我知道了：祝福他们，来参加，送红包，就很好。",
        "Cānjiā biérén de hūnlǐ de shíhou, nǐ cháng sòng shénme lǐwù? Nǐ cháng sòng hóngbāo ma? Nǐ zhīdào yīnggāi sòng shénme ma? Dì yí cì cānjiā hūnlǐ, wǒ bù zhīdào. Xiànzài wǒ zhīdào le: zhùfú tāmen, lái cānjiā, sòng hóngbāo, jiù hěn hǎo.",
        "When you attend someone else's wedding, what gift do you often give? Do you often give a red envelope? Do you know what you should give? The first time, I didn't know. Now I know: bless them, come, and give a red envelope — that's already good.",
    ),
    (
        "十二月结婚以前，他们还要见面很多次。第一次见面的地方，他们还想再去拍。我能来，就来。我不能来的时候，我会送礼物，也会祝福他们。",
        "Shí'èr yuè jiéhūn yǐqián, tāmen hái yào jiànmiàn hěn duō cì. Dì yí cì jiànmiàn de dìfang, tāmen hái xiǎng zài qù pāi. Wǒ néng lái, jiù lái. Wǒ bù néng lái de shíhou, wǒ huì sòng lǐwù, yě huì zhùfú tāmen.",
        "Before the December wedding they will still meet many times. They still want to go back to the first-meeting place to shoot. If I can come, I will come. When I cannot come, I will send a gift and still bless them.",
    ),
    (
        "我常在那个教堂附近走路。我知道大教堂在哪儿。举行婚礼的时候，很多人来。你应该早来。你不应该在教堂里乱拍照。有的地方能拍，有的地方不能拍。你知道了吗？",
        "Wǒ cháng zài nàge jiàotáng fùjìn zǒulù. Wǒ zhīdào dà jiàotáng zài nǎr. Jǔxíng hūnlǐ de shíhou, hěn duō rén lái. Nǐ yīnggāi zǎo lái. Nǐ bù yīnggāi zài jiàotáng lǐ luàn pāizhào. Yǒude dìfang néng pāi, yǒude dìfang bù néng pāi. Nǐ zhīdào le ma?",
        "I often walk near that church. I know where the big church is. When they hold the wedding, many people come. You should come early. You shouldn't take photos everywhere in the church. Some places allow shooting, some don't. Got it?",
    ),
    (
        "好，今天的视频就到这儿。下个月见！我一定来参加他们的婚礼，也一定给大家拍。祝福我的朋友！谢谢大家。再见！",
        "Hǎo, jīntiān de shìpín jiù dào zhèr. Xià ge yuè jiàn! Wǒ yídìng lái cānjiā tāmen de hūnlǐ, yě yídìng gěi dàjiā pāi. Zhùfú wǒ de péngyou! Xièxie dàjiā. Zàijiàn!",
        "Okay, that's all for today's video. See you next month! I will definitely attend their wedding, and I will definitely shoot for everyone. Blessings to my friend! Thanks everyone. Bye!",
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
    )
