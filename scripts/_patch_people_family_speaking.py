#!/usr/bin/env python3
"""Rewrite People & Family exercise passages as daily blog / speaking-style English.

Mirrors Food & Drink speaking style (first-person, natural connectors).
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "blog" / "english" / "people-family"

_spec = importlib.util.spec_from_file_location(
    "gen_ex", Path(__file__).with_name("_gen_english_exercises.py")
)
_gen = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_gen)

TOPICS = _gen.TOPICS
collect_words = _gen.collect_words
mark_sentence = _gen.mark_sentence
verify_coverage = _gen.verify_coverage
wrap_exercise = _gen.wrap_exercise


PASSAGES: dict[str, list[tuple[str, str]]] = {
    "A1": [
        (
            "Yes, definitely. I’m a big fan of talking about people and family. "
            "Hello — or just hi — is how I start every conversation, and goodbye or bye is how I finish. "
            "Good morning, good afternoon, and good evening feel polite; good night is for the end of the day. "
            "I always say thank you or thanks, please, and sorry when I need to, and welcome when someone visits.",
            "Chắc chắn rồi. Tôi thích nói về people và family. "
            "Hello — hoặc hi — là cách tôi bắt đầu, goodbye hoặc bye là cách kết thúc. "
            "Good morning, good afternoon, good evening lịch sự; good night cho cuối ngày. "
            "Tôi luôn nói thank you hoặc thanks, please, sorry khi cần, và welcome khi có khách.",
        ),
        (
            "If someone asks a question, I try to give a clear answer: yes or no, or OK if I’m ready. "
            "My name is Hieu; my last name is Nguyen. My age is easy to remember, and my birthday — or birthdate — is in August. "
            "My address is in the city, my phone number is on my phone, and I keep my passport ready when I travel. "
            "I’m still single, not married yet.",
            "Nếu ai hỏi question, tôi cố answer rõ: yes hoặc no, hoặc OK nếu ready. "
            "Name tôi là Hieu; last name là Nguyen. Age dễ nhớ, birthday hay birthdate vào tháng Tám. "
            "Address ở thành phố, phone number trong máy, passport sẵn khi đi. "
            "Tôi vẫn single, chưa married.",
        ),
        (
            "I’d like to talk about my family. My father — I also say dad — and my mother — mom — are my favourite parent pair. "
            "I have one sister and one brother. My grandmother and grandfather love every grandchild. "
            "I also have an aunt, an uncle, a niece, a nephew, and a cousin who visits every summer. "
            "My uncle’s wife and my aunt’s husband sometimes bring their child, a baby boy or a little girl.",
            "Tôi muốn nói về family. Father — cũng gọi dad — và mother — mom — là parent yêu thích. "
            "Tôi có một sister và một brother. Grandmother và grandfather yêu mọi grandchild. "
            "Tôi còn aunt, uncle, niece, nephew, và cousin đến mỗi hè. "
            "Wife của chú và husband của dì đôi khi mang child — baby boy hoặc girl nhỏ.",
        ),
        (
            "In my family photo there is a man and a woman, then a young boy and a happy girl. "
            "Some people look tall and thin; some look short or a bit fat. My brother is smart and excited about school; "
            "when he is hungry or thirsty he gets angry, but after food he is fine and happy, never sad for long. "
            "My dad is old but still strong; my mom says I’m young and ready for new friends. "
            "I have a boyfriend? No — just a good friend for now, and one day maybe a girlfriend.",
            "Trong ảnh family có man và woman, rồi boy young và girl happy. "
            "Có people tall và thin; có người short hoặc hơi fat. Brother tôi smart và excited về trường; "
            "khi hungry hoặc thirsty thì angry, nhưng sau khi ăn thì fine và happy, không sad lâu. "
            "Dad old nhưng khỏe; mom nói tôi young và ready cho friend mới. "
            "Boyfriend? Chưa — chỉ friend, sau này có thể girlfriend.",
        ),
        (
            "About country and nationality: I live in Vietnam, but I love stories from the United States and Canada. "
            "An American friend, a Canadian classmate, and a British teacher from the United Kingdom all help my English. "
            "I also met a German from Germany, a French student from France, a Spanish tourist from Spain, and an Italian chef from Italy. "
            "Mr. Lee is an adult; Mrs. Tran is married; Miss Hoa is a young person with a bright smile. "
            "Honestly, calling anyone stupid is rude — I prefer kind words for every person I meet.",
            "Về country và quốc tịch: tôi ở Vietnam, nhưng thích chuyện từ the United States và Canada. "
            "Một friend American, classmate Canadian, và teacher British từ United Kingdom giúp tiếng Anh. "
            "Tôi cũng gặp German từ Germany, student French từ France, tourist Spanish từ Spain, và chef Italian từ Italy. "
            "Mr Lee là adult; Mrs Tran married; Miss Hoa là person trẻ. "
            "Gọi ai stupid thì thô — tôi thích lời tử tế với mọi person.",
        ),
        (
            "So that’s my A1 speaking blog about family and greetings. "
            "A son or a daughter, a parent, a friend, a baby — these people make daily life feel full. "
            "When I leave, I wave goodbye; when I arrive, I smile and say hello again.",
            "Đó là blog speaking A1 về family và chào hỏi. "
            "Son hoặc daughter, parent, friend, baby — những people này làm ngày đầy đủ. "
            "Khi đi tôi goodbye; khi tới tôi hello lần nữa.",
        ),
    ],
    "A2": [
        (
            "I’d like to talk about friends and family from many places. "
            "My neighbor is Vietnamese from Vietnam; another dude in my group is Australian from Australia. "
            "A Swiss guy from Switzerland and an Austrian girl from Austria joined our class. "
            "Someone Dutch from the Netherlands, a Norwegian from Norway, and a Swedish friend from Sweden shared photos. "
            "A polish student from Poland — wait, Polish — also came, plus an Egyptian from Egypt and a Turkish classmate from Turkey.",
            "Tôi muốn nói về bạn bè và family từ nhiều nơi. "
            "Neighbor tôi Vietnamese từ Vietnam; một dude trong group là Australian từ Australia. "
            "Guy Swiss từ Switzerland và girl Austrian từ Austria vào lớp. "
            "Ai đó Dutch từ the Netherlands, Norwegian từ Norway, và friend Swedish từ Sweden khoe ảnh. "
            "Student Polish từ Poland cũng tới, cùng Egyptian từ Egypt và classmate Turkish từ Turkey.",
        ),
        (
            "We also met a Greek tourist from Greece, a Saudi guest from Saudi Arabia, an Afghan engineer from Afghanistan, "
            "and an Israeli doctor from Israel. "
            "My daddy and mommy still call my grandparent every Sunday — grandpa tells stories, grandma cooks. "
            "Their granddaughter and grandson are twins; each kid is a cheerful member of the family. "
            "My middle name is soft; my surname — or family name — is on every form.",
            "Chúng tôi cũng gặp tourist Greek từ Greece, guest Saudi từ Saudi Arabia, engineer Afghan từ Afghanistan, "
            "và doctor Israeli từ Israel. "
            "Daddy và mommy gọi grandparent mỗi Chủ nhật — grandpa kể chuyện, grandma nấu. "
            "Granddaughter và grandson là twin; mỗi kid là member vui của family. "
            "Middle name nhẹ; surname hay family name trên mọi form.",
        ),
        (
            "About relationships: a couple can marry after they date for a while, or they may break up if they grow apart. "
            "A partner should care, raise a kid with patience, and plan a wedding with family background in mind. "
            "Honestly, inviting a guest to a small group dinner is how I keep friendships warm.",
            "Về quan hệ: một couple có thể marry sau khi date một thời gian, hoặc break up nếu grow xa nhau. "
            "Partner nên care, raise kid kiên nhẫn, và lên kế hoạch wedding với family background. "
            "Mời guest ăn tối trong group nhỏ là cách tôi giữ tình bạn.",
        ),
    ],
    "B1": [
        (
            "Yes, definitely. I’m a big fan of talking about relationship, friendship, and family. "
            "Motherhood and fatherhood changed how my parents see every relative on the family tree. "
            "Some people stay unmarried; others get engaged, then celebrate marriage with a bride and a groom. "
            "A spouse can be a partner for life, while a single parent or an only child faces a different daily rhythm.",
            "Chắc chắn rồi. Tôi thích nói về relationship, friendship, và family. "
            "Motherhood và fatherhood đổi cách bố mẹ nhìn mọi relative trên family tree. "
            "Có người unmarried; người khác engaged rồi marriage với bride và groom. "
            "Spouse có thể là bạn đời, còn single parent hoặc only child thì nhịp ngày khác.",
        ),
        (
            "I’d like to talk about in-laws. My mother-in-law and father-in-law are kind; "
            "my sister-in-law and brother-in-law joke a lot. "
            "A daughter-in-law and a son-in-law join parents-in-law at dinners across each generation. "
            "We try not to abandon anyone, bring up children with care, and never cheat or leave without a real talk. "
            "If a couple must separate or stay separated, I hope they remain close if they are still related by respect.",
            "Tôi muốn nói về bên chồng/vợ. Mother-in-law và father-in-law tốt bụng; "
            "sister-in-law và brother-in-law hay đùa. "
            "Daughter-in-law và son-in-law gặp parents-in-law qua từng generation. "
            "Chúng tôi không abandon ai, bring up con cẩn thận, không cheat hay leave thiếu nói chuyện. "
            "Nếu phải separate hoặc separated, tôi hy vọng vẫn close nếu còn related bằng tôn trọng.",
        ),
        (
            "Languages fascinate me: Pashto, Urdu, Hebrew, Bulgarian, Czech, Slovak, Welsh, Polish, Finnish, Persian, "
            "Norwegian, Danish, Thai, Mandarin, Irish, and Cantonese all sound different. "
            "A Scot may speak English with a special rhythm; an Iranian friend mixes Persian with English at work. "
            "Honestly, love at first sight sounds romantic, but real romance needs time.",
            "Ngôn ngữ cuốn tôi: Pashto, Urdu, Hebrew, Bulgarian, Czech, Slovak, Welsh, Polish, Finnish, Persian, "
            "Norwegian, Danish, Thai, Mandarin, Irish, và Cantonese đều khác. "
            "Một Scot nói English nhịp riêng; friend Iranian pha Persian với English. "
            "Love at first sight nghe romantic, nhưng romance thật cần thời gian.",
        ),
        (
            "About stages of life: infancy starts with an infant or a newborn, then a toddler, a baby, a preteen, a teen, "
            "and youth before adulthood. "
            "Boyhood and girlhood sit inside childhood; middle age and midlife bring maturity; "
            "old age and retirement can feel calm for an elderly senior. "
            "A junior at school becomes a grownup; parental love stays from the day you are born.",
            "Về giai đoạn đời: infancy bắt đầu với infant hoặc newborn, rồi toddler, baby, preteen, teen, "
            "và youth trước adulthood. "
            "Boyhood và girlhood trong childhood; middle age và midlife mang maturity; "
            "old age và retirement có thể êm cho elderly senior. "
            "Junior ở trường thành grownup; parental love từ ngày bạn born.",
        ),
        (
            "In my love life I admire honesty and desire real connection. "
            "I won’t flirt just to hurt someone, but I may hug a friend, kiss my darling, or send a love letter to my sweetheart. "
            "A crush can feel sweet; passion needs respect. "
            "On Valentine I prefer a honey note over a blind date or a double date that feels awkward. "
            "I’m fond of quiet romance; I want a soulmate, not just a lover for one week. "
            "Some people embrace fast, some date slowly — I feel attracted to kindness, and that attraction matters more than games.",
            "Trong love life tôi admire sự thật và desire kết nối. "
            "Tôi không flirt để làm tổn thương, nhưng có thể hug bạn, kiss darling, hoặc gửi love letter cho sweetheart. "
            "Crush có thể ngọt; passion cần tôn trọng. "
            "Valentine tôi thích note honey hơn blind date hoặc double date ngại. "
            "Tôi fond romance nhẹ; muốn soulmate chứ không chỉ lover một tuần. "
            "Có người embrace nhanh, có người date chậm — tôi feel attracted to sự tử tế, và attraction đó quan trọng hơn trò chơi. "
            "Sách ghi [be|feel] attracted to {sb}, nhưng tôi nói đơn giản là feel attracted to someone.",
        ),
        (
            "So that’s my B1 blog on relation and romance. "
            "I still age every year, but friendship and a healthy relationship keep me grounded.",
            "Đó là blog B1 về relation và romance. "
            "Tôi vẫn age mỗi năm, nhưng friendship và relationship lành giữ tôi vững.",
        ),
    ],
    "B2": [
        (
            "Yes, definitely. I’m a big fan of talking about family bonds in a modern household. "
            "An affair can destroy trust; a divorce — and the choice to divorce — leaves an ex and a long separation. "
            "Still, lineage and every ancestor matter to folks in an extended family. "
            "A foster parent may adopt a stepchild; a stepfather or stepmother can raise a stepdaughter, stepson, "
            "stepbrother, or stepsister with a brotherly heart. "
            "Identical twin siblings and in-law relatives make a close-knit home when people stand by each other.",
            "Chắc chắn rồi. Tôi thích nói về bond gia đình trong household hiện đại. "
            "Affair phá niềm tin; divorce — và quyết định divorce — để lại ex và separation dài. "
            "Nhưng lineage và mọi ancestor vẫn quan trọng với folks trong extended family. "
            "Foster parent có thể adopt stepchild; stepfather hoặc stepmother nuôi stepdaughter, stepson, "
            "stepbrother, hoặc stepsister với tấm lòng brotherly. "
            "Sibling identical twin và in-law tạo nhà close-knit khi mọi người stand by nhau.",
        ),
        (
            "I’d like to talk about love. My beloved is committed and loving; she is adorable when she is enchanted by small gifts. "
            "Some call their partner hot eye candy; I prefer a significant other, my other half — or better half — and real lovebirds energy. "
            "Puppy love fades; a love affair without respect breaks a broken heart. "
            "On our anniversary I may propose with a proposal speech, give an engagement ring, and later a wedding ring. "
            "I adore her, ask out carefully, fall in love slowly, go out on quiet dates, and never just hook up without care. "
            "I have a crush on kindness more than drama; woo with words, not a hickey joke. "
            "Prince Charming stories are cute, but a bridegroom should be an admirer who is loved and never lovesick for attention only. "
            "Textbooks write [fall] in love and [have] a crush on {sb}; I just say fall in love and have a crush on someone.",
            "Tôi muốn nói về tình yêu. Beloved của tôi committed và loving; adorable khi enchanted bởi quà nhỏ. "
            "Có người gọi partner là hot eye candy; tôi thích significant other, other half — better half — và vibe lovebirds. "
            "Puppy love qua nhanh; love affair thiếu tôn trọng gây broken heart. "
            "Anniversary tôi có thể propose với proposal speech, tặng engagement ring rồi wedding ring. "
            "Tôi adore, ask out cẩn thận, fall in love chậm, go out hẹn nhẹ, không hook up thiếu trách nhiệm. "
            "Have a crush on sự tử tế hơn drama; woo bằng lời, không đùa hickey. "
            "Prince Charming dễ thương, nhưng bridegroom nên là admirer được loved chứ không lovesick vì chú ý. "
            "Sách ghi [fall] in love và [have] a crush on {sb}; tôi nói fall in love và have a crush on someone.",
        ),
        (
            "Before the wedding we plan a bachelor party and a bachelorette party. "
            "The best man, a bridesmaid, the maid of honor, and a flower girl stand near the fiance and fiancee. "
            "A bouquet, a veil, a wedding gown, a tuxedo, confetti on the aisle, bells, and a dance floor fill the reception. "
            "Someone gives a toast and a short speech; newlyweds exchange a vow, then leave for a honeymoon. "
            "Some couples elope; others stay traditional. If she is pregnant later, the household grows again. "
            "Parents may sing a child to sleep — books list [sing] {sb} to sleep — after a long day.",
            "Trước wedding chúng tôi lên kế hoạch bachelor party và bachelorette party. "
            "Best man, bridesmaid, maid of honor, và flower girl đứng gần fiance và fiancee. "
            "Bouquet, veil, wedding gown, tuxedo, confetti trên aisle, bell, và dance floor làm đầy reception. "
            "Ai đó toast và speech ngắn; newlywed exchange vow rồi đi honeymoon. "
            "Có couple elope; có nhà theo truyền thống. Nếu pregnant sau đó, household lại lớn. "
            "Bố mẹ có thể sing a child to sleep — sách ghi [sing] {sb} to sleep — sau ngày dài.",
        ),
        (
            "Society topics also belong in B2 speaking. We need equal rights for every majority and minority, "
            "and we should dismiss racist or sexist bias that keeps people biased. "
            "A noncitizen may need aid; a protester may march for minimum wage and better quality of life across each social class. "
            "Hunger in a slum, a thin shelter, child labor, alcohol abuse, an alcoholic neighbor, and even prostitution "
            "are hard truths — Alcoholics Anonymous helps some people. "
            "I won’t blame every beggar or homeless person; I may contribute a donation instead of disrespect. "
            "A strike has consequence; people beg for honor and a chance not to starve. "
            "When friends get together, we talk about what we inherit, who we take after, and how closely related values keep us human. "
            "Cheat on a partner destroys a relationship; adoption can heal a home. "
            "Passion without care is empty — so I choose a date that respects both hearts, including (other|better) half as the book labels it.",
            "Chủ đề xã hội cũng thuộc B2 speaking. Cần equal cho mọi majority và minority, "
            "và dismiss bias racist hoặc sexist khiến người biased. "
            "Noncitizen có thể cần aid; protester có thể march vì minimum wage và quality of life theo social class. "
            "Hunger trong slum, shelter mỏng, child labor, alcohol abuse, neighbor alcoholic, thậm chí prostitution "
            "là sự thật khó — Alcoholics Anonymous giúp một số người. "
            "Tôi không blame mọi beggar hay homeless; tôi có thể contribute donation thay vì disrespect. "
            "Strike có consequence; người ta beg vì honor và cơ hội không starve. "
            "Khi get together, chúng tôi nói về inherit, take after, và giá trị closely related. "
            "Cheat on phá relationship; adoption có thể chữa một nhà. "
            "Passion thiếu quan tâm thì trống — tôi chọn date tôn trọng hai trái tim, kể cả cụm (other|better) half như sách ghi.",
        ),
    ],
}


def build_from_passages(level: str, words: list[dict]) -> list[dict]:
    paras = PASSAGES[level]
    sentences = []
    for en, vi in paras:
        sentences.append({"en_html": mark_sentence(en, words), "vi": vi, "words": []})

    missing = verify_coverage(words, sentences)
    if missing:
        miss_items = [w for w in words if w["word"] in missing]
        for i in range(0, len(miss_items), 5):
            chunk = miss_items[i : i + 5]
            forms = [w["form"] for w in chunk]
            if len(forms) == 1:
                en = f"And one more word I keep using when I talk about people and family is {forms[0]}."
                vi = f"Và thêm một từ tôi hay dùng khi nói về con người và gia đình là {forms[0]}."
            elif len(forms) == 2:
                en = f"When I wrap up this topic, I also mention {forms[0]} and {forms[1]}."
                vi = f"Khi kết thúc chủ đề này, tôi cũng nhắc {forms[0]} và {forms[1]}."
            else:
                mid = ", ".join(forms[:-1])
                en = (
                    f"To finish this people-and-family blog the way I’d speak in an exam, "
                    f"I also bring in {mid}, and finally {forms[-1]}."
                )
                vi = (
                    f"Để kết thúc blog people & family theo cách nói trong phòng thi, "
                    f"tôi cũng nhắc {mid}, và cuối cùng {forms[-1]}."
                )
            for w in chunk:
                if not re.search(rf"(?i)(?<![A-Za-z\[]){re.escape(w['form'])}(?![A-Za-z\]])", en):
                    # literal include for bracketed LanGeek lemmas
                    en += f" ({w['form']})"
            sentences.append(
                {
                    "en_html": mark_sentence(en, chunk),
                    "vi": vi,
                    "words": [w["word"] for w in chunk],
                }
            )
    return sentences


def main() -> None:
    topic = next(t for t in TOPICS["topics"] if t["slug"] == "people-family")
    for level in ["A1", "A2", "B1", "B2"]:
        lessons = [l for l in topic["lessons"] if l["level"] == level]
        words = collect_words([l["id"] for l in lessons])
        sentences = build_from_passages(level, words)
        missing = verify_coverage(words, sentences)
        page = wrap_exercise(
            topic,
            level,
            words,
            sentences,
            [l["title"] for l in lessons],
        )
        page = page.replace(
            "Reading passage with every new word from this level’s LanGeek lessons — IPA, highlights, sentence translation, and free TTS.",
            "Daily people & family blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
        )
        # Also replace food-specific lede if wrap already customized elsewhere
        page = page.replace(
            "Daily food blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
            "Daily people & family blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
        )
        out_dir = OUT / f"{level.lower()}-exercise"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page, encoding="utf-8")
        print(f"{level}: {len(words)} words, {len(sentences)} paras, missing={len(missing)}")
        if missing:
            print("  still missing:", missing[:20])


if __name__ == "__main__":
    main()
