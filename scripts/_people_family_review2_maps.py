"""Mind maps + dropdown slots for People & Family · Review Exercise 2.

Same Linear Thinking skeleton as Food (Lesson 2, 3, 5–16; skip 4).
Nhánh 2 leaves that were Food-only (keep fit, burn calories…) are replaced
with relationship / family phrases from DOL, ECE, TAK12, ZIM, WESET, Mc IELTS, IDP.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_food_spec = importlib.util.spec_from_file_location(
    "food_rev", Path(__file__).with_name("_gen_food_review_exercise.py")
)
_food = importlib.util.module_from_spec(_food_spec)
assert _food_spec and _food_spec.loader
_food_spec.loader.exec_module(_food)

tip = _food.tip
tip_html = _food.tip_html


def _opt(form: str, vi: str) -> dict:
    return {"form": form, "vi": vi}


WORD_SLOTS: dict[str, list[dict]] = {
    # Lesson 2 · Reasons
    "relax_phrase": [
        _opt("unwind after a long day", "thư giãn sau ngày dài"),
        _opt("recharge my batteries", "nạp lại năng lượng"),
        _opt("clear my head", "giải tỏa đầu óc"),
        _opt("escape from the hustle and bustle of the city", "thoát khỏi sự hối hả của thành phố"),
        _opt("temporarily forget all the pressures from my work", "tạm quên áp lực công việc"),
        _opt("unwind and recharge my batteries", "thư giãn và nạp lại năng lượng"),
    ],
    "edu_phrase": [
        _opt("widen my social circles", "mở rộng vòng tròn xã hội"),
        _opt("meet like-minded individuals", "gặp người cùng chí hướng"),
        _opt("learn how to work through disagreements", "học cách giải quyết bất đồng"),
        _opt("become a more well-rounded person", "trở nên toàn diện hơn"),
        _opt("pass down traditional values", "truyền giá trị truyền thống"),
    ],
    "bond_phrase": [
        _opt("provide emotional support", "mang lại hỗ trợ cảm xúc"),
        _opt("foster a sense of belonging", "nuôi dưỡng cảm giác thuộc về"),
        _opt("strengthen family ties", "củng cố mối quan hệ gia đình"),
        _opt("maintain strong bonds", "duy trì mối liên kết bền"),
        _opt("prevent loneliness", "ngăn cảm giác cô đơn"),
        _opt("work through disagreements in a respectful way", "giải quyết bất đồng một cách tôn trọng"),
        _opt("have a strong bond with each other", "có sự gắn kết mạnh mẽ với nhau"),
    ],
    "bond_followup": [
        _opt("It also helps me stay emotionally healthy.", "Nó cũng giúp tôi khỏe về mặt tinh thần."),
        _opt("Spending time together can also prevent us from drifting apart.", "Dành thời gian cùng nhau cũng giúp không xa cách."),
        _opt("It also helps me feel truly at home.", "Nó cũng giúp tôi cảm thấy thật sự thuộc về."),
    ],
    "thick_thin": [
        _opt("stand by me through thick and thin", "đứng bên tôi trong mọi hoàn cảnh"),
        _opt("stand by each other through thick and thin", "đứng bên nhau trong mọi hoàn cảnh"),
        _opt("stay with me through thick and thin", "ở bên tôi trong mọi hoàn cảnh"),
    ],
    "soft_dislike": [
        _opt("isn't my cup of tea", "không phải sở thích của tôi"),
        _opt("is not really entertaining", "không thật sự giải trí"),
        _opt("can feel quite stressful", "có thể khá căng thẳng"),
    ],
    "no_benefit": [
        _opt("It doesn't give me the chance to connect on a deep level", "Không cho tôi cơ hội kết nối sâu"),
        _opt("It doesn't help me unwind", "Không giúp tôi thư giãn"),
        _opt("It doesn't help me enrich my social life", "Không giúp làm giàu đời sống xã hội"),
    ],
    "toxic_outcome": [
        _opt("loneliness and a sense of isolation", "cô đơn và cảm giác bị cô lập"),
        _opt("mistrust and miscommunication", "sự nghi ngờ và hiểu lầm"),
        _opt("a strained relationship", "một mối quan hệ căng thẳng"),
        _opt("people drifting apart", "mọi người dần xa nhau"),
        _opt("falling out with someone you care about", "cãi nhau / cắt đứt với người mình quý"),
    ],
    # Lesson 3
    "family_type": [
        _opt("close-knit family", "gia đình gắn bó"),
        _opt("nuclear family", "gia đình hạt nhân"),
        _opt("extended family", "đại gia đình"),
        _opt("blended family", "gia đình tái hợp"),
    ],
    "activity": [
        _opt("having dinner together", "ăn tối cùng nhau"),
        _opt("catching up on each other's day", "kể cho nhau nghe ngày hôm đó"),
        _opt("going on weekend trips", "đi chơi cuối tuần"),
        _opt("spending quality time at home", "dành thời gian chất lượng ở nhà"),
        _opt("celebrating milestones together", "kỷ niệm các mốc quan trọng cùng nhau"),
    ],
    "prefer_rather_than": [
        _opt("spending time with family rather than going out", "dành thời gian với gia đình hơn là đi chơi"),
        _opt("small gatherings rather than big parties", "buổi họp mặt nhỏ hơn tiệc lớn"),
        _opt("face-to-face talks rather than texting", "nói chuyện trực tiếp hơn nhắn tin"),
        _opt("keeping in touch rather than losing contact", "giữ liên lạc hơn là mất liên lạc"),
    ],
    "hardly_ever_action": [
        _opt("visit my extended family", "thăm đại gia đình"),
        _opt("go to large family parties", "đi tiệc gia đình lớn"),
        _opt("call distant relatives", "gọi họ hàng xa"),
        _opt("post about my private life", "đăng chuyện riêng tư"),
        _opt("feel lonely", "cảm thấy cô đơn"),
    ],
    "quality_time": [
        _opt("quality time", "thời gian chất lượng"),
        _opt("quality time at home", "thời gian chất lượng ở nhà"),
        _opt("quality time together", "thời gian chất lượng cùng nhau"),
    ],
    "listen_phrase": [
        _opt("lend a listening ear", "sẵn sàng lắng nghe"),
        _opt("lend a listening ear without judging", "lắng nghe mà không phán xét"),
        _opt("lend a sympathetic ear", "lắng nghe đồng cảm"),
    ],
    "keep_touch": [
        _opt("keep in touch", "giữ liên lạc"),
        _opt("keep in touch with each other", "giữ liên lạc với nhau"),
        _opt("make an effort to keep in touch", "nỗ lực giữ liên lạc"),
    ],
    "get_along": [
        _opt("get along with each other", "hòa thuận với nhau"),
        _opt("get on well with each other", "hòa thuận với nhau"),
        _opt("get along with my parents", "hòa thuận với bố mẹ"),
    ],
    "importance_phrase": [
        _opt("holds immense importance to me", "có ý nghĩa to lớn với tôi"),
        _opt("is my pillar of strength", "là trụ cột tinh thần của tôi"),
        _opt("gives me unwavering support", "mang lại sự hỗ trợ kiên định"),
    ],
    # Lesson 5
    "kind_friend": [
        _opt("emotionally supportive friends", "bạn hỗ trợ về cảm xúc"),
        _opt("like-minded individuals", "người cùng chí hướng"),
        _opt("childhood friends", "bạn thời thơ ấu"),
        _opt("people I can confide in", "người tôi có thể tâm sự"),
    ],
    "kind_quality": [
        _opt("honesty and kindness", "sự trung thực và tử tế"),
        _opt("mutual trust and respect", "tin tưởng và tôn trọng lẫn nhau"),
        _opt("compatibility and shared interests", "sự hòa hợp và sở thích chung"),
        _opt("empathy and open communication", "đồng cảm và giao tiếp cởi mở"),
        _opt("loyalty and mutual respect", "lòng trung thành và tôn trọng lẫn nhau"),
        _opt("understanding and affection", "sự thấu hiểu và tình cảm"),
    ],
    "attracted_to": [
        _opt("people who are honest and who know how to behave with others", "người thành thật và biết cư xử (TAK12)"),
        _opt("like-minded individuals I can live in harmony with", "người cùng chí hướng, sống hòa hợp được"),
        _opt("a partner I have chemistry and compatibility with", "bạn đời hợp nhau về chemistry và compatibility"),
        _opt("companions who show loyalty, not just acquaintances", "người đồng hành có lòng trung thành, không chỉ người quen"),
    ],
    "relation_type": [
        _opt("a close friend", "bạn thân"),
        _opt("a childhood friend", "bạn thời thơ ấu"),
        _opt("a classmate", "bạn cùng lớp"),
        _opt("a roommate", "bạn cùng phòng"),
        _opt("a colleague", "đồng nghiệp"),
        _opt("a companion", "người đồng hành"),
        _opt("an acquaintance", "người quen"),
        _opt("a partner", "bạn đời / người yêu"),
    ],
    "relation_adj": [
        _opt("close-knit and supportive", "gắn bó và luôn ủng hộ"),
        _opt("meaningful and long-lasting", "ý nghĩa và bền vững"),
        _opt("harmonious", "hòa hợp"),
        _opt("complicated", "phức tạp"),
        _opt("distant or strained", "xa cách hoặc căng thẳng"),
    ],
    "rel_verb": [
        _opt("build a relationship", "xây dựng mối quan hệ"),
        _opt("maintain a relationship", "duy trì mối quan hệ"),
        _opt("strengthen a relationship", "củng cố mối quan hệ"),
        _opt("have a strong bond with someone", "có sự gắn kết mạnh mẽ với ai"),
        _opt("fall out with someone", "cãi nhau / cắt đứt với ai"),
        _opt("get along with someone", "hòa hợp với ai"),
    ],
    "fighter_family": [
        _opt("a deep sense of kinship", "mối quan hệ họ hàng sâu (IELTS-Fighter)"),
        _opt("a long family lineage", "dòng họ / dòng dõi dài"),
        _opt("a descendant of a well-known family", "hậu duệ của một dòng họ nổi tiếng"),
        _opt("a matriarchal household", "hộ gia đình theo gia mẫu"),
        _opt("a patriarchal system", "hệ thống gia trưởng"),
        _opt("disown a family member and cut all ties", "từ bỏ người trong gia đình, cắt hết quan hệ"),
    ],
    "romance_lex": [
        _opt("affection", "tình cảm, lòng yêu mến"),
        _opt("chemistry", "hóa học tình cảm"),
        _opt("attraction", "sự thu hút"),
        _opt("commitment", "sự cam kết"),
        _opt("compatibility", "sự hòa hợp"),
        _opt("empathy", "sự đồng cảm"),
    ],
    "kind_family_act": [
        _opt("having dinner together", "ăn tối cùng nhau"),
        _opt("family gatherings at Tet", "họp mặt gia đình dịp Tết"),
        _opt("quiet weekends at home", "cuối tuần yên ở nhà"),
        _opt("short trips with my parents", "chuyến đi ngắn với bố mẹ"),
    ],
    "kind_reason": [
        _opt("helps us strengthen our bond", "giúp chúng tôi gắn kết hơn"),
        _opt("gives me a real sense of belonging", "mang lại cảm giác thuộc về"),
        _opt("lets us catch up on each other's lives", "để chúng tôi cập nhật cuộc sống của nhau"),
        _opt("lays the groundwork for a lifelong friendship", "đặt nền cho tình bạn bền lâu"),
    ],
    # Lesson 6
    "prefer_x": [
        _opt("spending time with my family", "dành thời gian với gia đình"),
        _opt("hanging out with close friends", "đi chơi với bạn thân"),
        _opt("being with a small group", "ở với nhóm nhỏ"),
        _opt("talking face to face", "nói chuyện trực tiếp"),
    ],
    "prefer_y": [
        _opt("going out with a big crowd", "đi chơi với đám đông"),
        _opt("staying alone all weekend", "ở một mình cả cuối tuần"),
        _opt("keeping everything online", "giữ mọi thứ trên mạng"),
        _opt("making small talk with acquaintances", "nói chuyện xã giao với người quen"),
    ],
    # Lesson 7
    "pop_group": [
        _opt("the younger generation", "thế hệ trẻ"),
        _opt("older people", "người lớn tuổi"),
        _opt("urban dwellers", "người thành thị"),
        _opt("people in rural areas", "người nông thôn"),
    ],
    "pop_custom": [
        _opt("honouring elders and seeking their advice", "tôn trọng người lớn và xin lời khuyên"),
        _opt("living with extended family under one roof", "sống chung đại gia đình một mái nhà"),
        _opt("arranging marriages based on family values", "hôn nhân sắp đặt dựa trên giá trị gia đình"),
        _opt("gathering for Tet and family reunions", "sum họp Tết và họp mặt gia đình"),
    ],
    # Lesson 8
    "best_time": [
        _opt("Sunday lunch", "bữa trưa Chủ nhật"),
        _opt("weekday family dinners", "bữa tối ngày thường"),
        _opt("the Tet holiday", "dịp Tết"),
        _opt("quiet evenings after work", "buổi tối yên sau giờ làm"),
        _opt("weekend mornings", "sáng cuối tuần"),
    ],
    # Lesson 9
    "time_anchor": [
        _opt("about two years ago", "khoảng hai năm trước"),
        _opt("just last Tet", "đúng Tết vừa rồi"),
        _opt("when I was in high school", "khi tôi học cấp 3"),
        _opt("during the pandemic", "trong thời kỳ đại dịch"),
    ],
    # Lesson 10
    "child_detail": [
        _opt("help my mum with household chores", "giúp mẹ việc nhà"),
        _opt("look up to my older brother", "ngưỡng mộ anh trai"),
        _opt("take after my dad", "giống bố"),
        _opt("spend most evenings under the same roof", "hầu hết tối sống chung một mái nhà"),
    ],
    # Lesson 11
    "suit_case": [
        _opt("both people communicate openly", "cả hai giao tiếp cởi mở"),
        _opt("there is mutual trust", "có sự tin tưởng lẫn nhau"),
        _opt("they share similar values", "họ có giá trị giống nhau"),
        _opt("they still make time for quality time", "họ vẫn dành thời gian chất lượng"),
    ],
    # Lesson 12
    "easy_hard_x": [
        _opt("make new friends as an adult", "kết bạn mới khi đã trưởng thành"),
        _opt("become real friends with people you meet online", "trở thành bạn thật với người quen trên mạng"),
        _opt("maintain a long-distance relationship", "duy trì mối quan hệ yêu xa"),
        _opt("work through disagreements calmly", "giải quyết bất đồng một cách bình tĩnh"),
    ],
    # Lesson 13
    "dislike_point": [
        _opt("overprotective parents", "bố mẹ bảo bọc quá mức"),
        _opt("sibling rivalry", "sự ganh đua giữa anh chị em"),
        _opt("family pressure about marriage", "áp lực gia đình về hôn nhân"),
        _opt("miscommunication on social media", "hiểu lầm trên mạng xã hội"),
        _opt("friends who might stab you in the back", "bạn có thể đâm sau lưng"),
    ],
    # Lesson 14
    "freq": [
        _opt("almost every day", "hầu như mỗi ngày"),
        _opt("once a week", "mỗi tuần một lần"),
        _opt("once a month", "mỗi tháng một lần"),
        _opt("every now and then", "thỉnh thoảng"),
        _opt("once in a blue moon", "năm thì mười họa"),
    ],
    # Lesson 15
    "change_old": [
        _opt("extended families living under one roof", "đại gia đình sống chung một mái nhà"),
        _opt("face-to-face conversations every evening", "nói chuyện trực tiếp mỗi tối"),
        _opt("letters that took weeks to arrive", "những lá thư mất cả tuần mới tới"),
        _opt("men being the sole breadwinners", "đàn ông là trụ cột kinh tế duy nhất"),
    ],
    "change_new": [
        _opt("nuclear households in big cities", "hộ gia đình hạt nhân ở thành phố lớn"),
        _opt("virtual interaction and video calls", "giao tiếp ảo và gọi video"),
        _opt("a much faster-paced lifestyle", "lối sống vội vã hơn nhiều"),
        _opt("both partners sharing household responsibilities", "cả hai cùng chia sẻ việc nhà"),
    ],
    # Lesson 16
    "p2_open": [
        _opt("I'm going to talk about", "Tôi sẽ nói về"),
        _opt("I'd like to talk about", "Tôi muốn nói về"),
        _opt("So, if I had to talk about this topic, it would have to be", "Nếu phải nói về chủ đề này thì sẽ là"),
    ],
    "p2_close": [
        _opt("So, if I had to talk about a person I admire", "Vậy nếu tôi phải nói về người tôi ngưỡng mộ"),
        _opt("So, if I had to talk about a close relationship", "Vậy nếu tôi phải nói về một mối quan hệ thân"),
        _opt("So, if I had to talk about an old friend", "Vậy nếu tôi phải nói về một người bạn cũ"),
    ],
    "p2_close_tail": [
        _opt("it would have to be my mum.", "thì đó sẽ phải là mẹ tôi."),
        _opt("it would have to be my best friend Lan.", "thì đó sẽ phải là bạn thân Lan."),
        _opt("it would have to be my brother Minh.", "thì đó sẽ phải là anh Minh."),
        _opt("it would have to be my school friend Preet.", "thì đó sẽ phải là bạn học Preet."),
    ],
    "score_phrase": [
        _opt("hold immense importance", "có ý nghĩa to lớn"),
        _opt("are my pillars of strength", "là những trụ cột của tôi"),
        _opt("give me unwavering support", "mang lại sự hỗ trợ kiên định"),
        _opt("give me a sense of belonging", "mang lại cảm giác thuộc về"),
        _opt("stand by me through thick and thin", "đứng bên tôi trong mọi hoàn cảnh"),
    ],
    "family_idiom": [
        _opt("blood is thicker than water", "máu mủ ruột thịt"),
        _opt("like two peas in a pod", "giống nhau như đúc"),
        _opt("the apple never falls far from the tree", "con nhà tông không giống lông cũng giống cánh"),
        _opt("like father, like son", "cha nào con nấy"),
        _opt("the black sheep of the family", "thành viên cá biệt"),
    ],
    "relationship_v": [
        _opt("get on well with", "hòa thuận với"),
        _opt("look up to", "ngưỡng mộ"),
        _opt("take after", "giống (người thân)"),
        _opt("keep in touch with", "giữ liên lạc với"),
        _opt("confide in", "tâm sự với"),
    ],
}


# ── Lesson 2 · Reasons (same skeleton; Health → emotional wellbeing) ──

LESSON2_MINDMAP_LEFT = [
    {
        "id": "dis-fun",
        "color": "#fca5a5",
        "name": "Không giải trí",
        "name_vi": "not entertaining",
        "flow": True,
        "opener": "I don't like this · I can't stand … · It's not my cup of tea",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj",
                "leaves": [
                    tip(
                        "It's + not + interesting / entertaining / exciting / relaxing",
                        "Không thú vị / giải trí / hấp dẫn / thư giãn",
                    ),
                    tip(
                        "It's + boring / stressful / noisy / awkward",
                        "Nhàm chán / căng thẳng / ồn ào / ngượng",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · It makes me + adj",
                "patterns": (
                    "It makes me + bored / tired / stressed / exhausted · "
                    "I have to + deal with the same… every day"
                ),
                "leaves": [
                    tip("not my cup of tea", "không phải sở thích của tôi"),
                    tip("can't stand large family parties", "không chịu nổi tiệc gia đình lớn"),
                    tip("I can't bear small talk with distant relatives", "tôi không chịu nổi chuyện xã giao với họ hàng xa"),
                    tip(
                        "I have to deal with the same family questions every gathering",
                        "tôi phải nghe cùng câu hỏi gia đình mỗi lần họp mặt",
                    ),
                    tip(
                        "overprotective parents make me feel trapped",
                        "bố mẹ bảo bọc quá mức khiến tôi cảm thấy bị gò bó",
                    ),
                ],
            },
        ],
    },
    {
        "id": "dis-edu",
        "color": "#f87171",
        "name": "Không giáo dục",
        "name_vi": "not educational",
        "flow": True,
        "opener": "I don't think … · To be honest, I don't enjoy …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + not + adj",
                "leaves": [
                    tip(
                        "It's + not + educational / useful / practical",
                        "Không mang tính giáo dục / hữu ích / thực tế",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · doesn't + V",
                "patterns": (
                    "<code>doesn't</code> + V nguyên mẫu · "
                    "It doesn't give me the chance to … · "
                    "It doesn't help me …"
                ),
                "leaves": [
                    tip("It doesn't help me unwind", "Nó không giúp tôi thư giãn"),
                    tip(
                        "It doesn't give me the chance to connect on a deep level",
                        "Nó không cho tôi cơ hội kết nối sâu",
                    ),
                    tip(
                        "It doesn't help me widen my social circles",
                        "Nó không giúp tôi mở rộng vòng tròn xã hội",
                    ),
                    tip(
                        "It doesn't give me the opportunity to meet like-minded individuals",
                        "Nó không cho tôi cơ hội gặp người cùng chí hướng",
                    ),
                    tip(
                        "It doesn't help me work through disagreements",
                        "Nó không giúp tôi giải quyết bất đồng",
                    ),
                ],
            },
        ],
    },
    {
        "id": "dis-health",
        "color": "#ef4444",
        "name": "Hại tinh thần",
        "name_vi": "toxic / lonely — thay nhánh sức khỏe Food",
        "flow": True,
        "opener": "No, definitely not because … · I avoid …",
        "branches": [
            {
                "label": "Nhánh 1 · not good / harmful",
                "leaves": [
                    tip_html(
                        "not good <strong>for</strong> my mental health",
                        "không tốt cho sức khỏe tinh thần",
                    ),
                    tip_html(
                        "harmful / detrimental <strong>to</strong> a relationship",
                        "có hại / bất lợi cho mối quan hệ",
                    ),
                    tip("It's + toxic / strained / distant", "Nó độc hại / căng thẳng / xa cách"),
                ],
            },
            {
                "label": "Nhánh 2 · can lead to …",
                "patterns": "Spending too little time with loved ones / arguing all the time can lead to …",
                "leaves": [
                    tip("loneliness and a sense of isolation", "cô đơn và cảm giác bị cô lập"),
                    tip("mistrust and miscommunication", "sự nghi ngờ và hiểu lầm"),
                    tip("a strained relationship", "một mối quan hệ căng thẳng"),
                    tip("drifting apart", "dần xa nhau"),
                    tip("falling out with someone", "cãi nhau / cắt đứt quan hệ"),
                    tip("sibling rivalry", "sự ganh đua giữa anh chị em"),
                ],
            },
        ],
    },
]

LESSON2_MINDMAP_RIGHT = [
    {
        "id": "like-fun",
        "color": "#67e8f9",
        "name": "Giải trí",
        "name_vi": "entertainment",
        "flow": True,
        "opener": "I love this · I think … · I'm keen on …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj",
                "leaves": [
                    tip(
                        "It's + relaxing / exciting / entertaining / interesting …",
                        "Thư giãn / thú vị / giải trí / hấp dẫn…",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Starter + V",
                "patterns": (
                    "It helps me + V · It's a great way to + V · "
                    "It gives me the chance to + V · "
                    "I also get the opportunity to + V"
                ),
                "leaves": [
                    tip("reduce stress", "giảm căng thẳng"),
                    tip("relax / unwind", "thư giãn"),
                    tip("clear my head", "giải tỏa đầu óc"),
                    tip("recharge my batteries", "nạp lại năng lượng"),
                    tip("catch up on each other's day", "cập nhật ngày của nhau"),
                    tip("spend quality time together", "dành thời gian chất lượng"),
                    tip(
                        "temporarily forget all the pressures from my work",
                        "tạm thời quên áp lực công việc",
                    ),
                    tip(
                        "escape from the hustle and bustle of the city",
                        "thoát khỏi sự hối hả của thành phố",
                    ),
                ],
            },
        ],
    },
    {
        "id": "like-edu",
        "color": "#5eead4",
        "name": "Giáo dục",
        "name_vi": "educational",
        "flow": True,
        "opener": "I love this · I think it's useful · Yes, because …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj",
                "leaves": [
                    tip(
                        "It's + educational / useful / practical",
                        "Mang tính giáo dục / hữu ích / thực tế",
                    ),
                    tip(
                        "learn skills such as … ↔ learn how to + V",
                        "học kỹ năng như … ↔ học cách + V",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Starter + V",
                "patterns": (
                    "It helps me + V · It gives me the chance to + V · "
                    "I also get the opportunity to + V"
                ),
                "leaves": [
                    tip("meet like-minded individuals", "gặp người cùng chí hướng"),
                    tip("widen my social circles", "mở rộng vòng tròn xã hội"),
                    tip("pass down traditional values", "truyền giá trị truyền thống"),
                    tip("learn how to practise empathy", "học cách đồng cảm"),
                    tip("learn how to work through disagreements", "học cách giải quyết bất đồng"),
                    tip(
                        "become more confident and independent",
                        "trở nên tự tin và độc lập hơn",
                    ),
                    tip(
                        "become a more well-rounded person",
                        "trở thành một con người toàn diện hơn",
                    ),
                    tip(
                        "learn how to treat people with respect",
                        "học cách đối xử với người khác bằng sự tôn trọng",
                    ),
                ],
            },
        ],
    },
    {
        "id": "like-health",
        "color": "#34d399",
        "name": "Sức khỏe tinh thần",
        "name_vi": "emotional wellbeing — thay Cụm V Food",
        "flow": True,
        "opener": "I love this · Yes, because it's a great way to …",
        "branches": [
            {
                "label": "Nhánh 1 · It's a great way to",
                "leaves": [
                    tip(
                        "It's a great way to + stay emotionally healthy / feel a sense of belonging",
                        "Cách tuyệt để khỏe tinh thần / cảm giác thuộc về",
                    ),
                    tip("It's + good for your mental health", "Tốt cho sức khỏe tinh thần"),
                ],
            },
            {
                "label": "Nhánh 2 · Cụm V",
                "patterns": (
                    "It helps me + V · It also helps me + V · "
                    "Spending time with … can also prevent …"
                ),
                "leaves": [
                    tip(
                        "provide emotional support / lend a listening ear",
                        "mang hỗ trợ cảm xúc / lắng nghe đồng hành",
                    ),
                    tip("foster a sense of security", "nuôi dưỡng cảm giác an toàn"),
                    tip("strengthen family ties / have a strong bond with someone", "củng cố / có sự gắn kết mạnh (ECE)"),
                    tip("build / maintain / strengthen a relationship", "xây · duy trì · củng cố mối quan hệ"),
                    tip("prevent loneliness / a sense of isolation", "ngăn cô đơn / cảm giác bị cô lập"),
                    tip("maintain a healthy relationship", "duy trì mối quan hệ lành mạnh"),
                    tip(
                        "work through disagreements in a respectful way",
                        "giải quyết bất đồng một cách tôn trọng",
                    ),
                    tip(
                        "stand by each other through thick and thin",
                        "đứng bên nhau trong mọi hoàn cảnh",
                    ),
                ],
            },
        ],
    },
]

LESSON3_MINDMAP_LEFT = [
    {
        "id": "no-flow",
        "color": "#fca5a5",
        "name": "NO",
        "name_vi": "phủ định",
        "flow": True,
        "opener": "No, definitely not · No, absolutely not · No, not really · Well, not really",
        "branches": [
            {
                "label": "Nhánh 1 · Verb",
                "leaves": [
                    tip("I don't like / love / enjoy + V-ing", "Tôi không thích / yêu / tận hưởng + V-ing"),
                    tip(
                        "Family: I don't enjoy large family parties / posting my private life",
                        "Family: Tôi không thích tiệc lớn / khoe đời tư",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Adj / NP",
                "leaves": [
                    tip("I'm not keen on …", "Tôi không hứng thú với …"),
                    tip("I'm not interested in …", "Tôi không quan tâm đến …"),
                    tip("I'm not a big fan of …", "Tôi không phải fan của …"),
                ],
            },
            {
                "label": "Nhánh 3 · hardly ever (chiến thuật Favourite)",
                "patterns": "<code>I hardly ever</code> + V nguyên mẫu",
                "leaves": [
                    tip("I hardly ever + V", "Tôi hiếm khi / hầu như không bao giờ + V"),
                    tip(
                        "I hardly ever visit my extended family / go to big parties / lose contact",
                        "Hiếm khi thăm đại gia đình / đi tiệc lớn / mất liên lạc",
                    ),
                ],
            },
        ],
    },
]

LESSON3_MINDMAP_RIGHT = [
    {
        "id": "yes-flow",
        "color": "#67e8f9",
        "name": "YES + Reasons",
        "name_vi": "khẳng định + lý do",
        "flow": True,
        "opener": "Yes, definitely · Yes, absolutely · Yes, I do",
        "branches": [
            {
                "label": "Nhánh 1 · Verb / Adj / NP",
                "leaves": [
                    tip("I like / love / enjoy + V-ing", "Tôi thích / yêu / tận hưởng + V-ing"),
                    tip("I'm keen on / interested in + N", "Tôi hứng thú / quan tâm đến + N"),
                    tip("I'm a big fan of + N", "Tôi là fan lớn của + N"),
                    tip(
                        "Family: I'm a big fan of family gatherings / quality time",
                        "Family: Tôi rất thích họp mặt / thời gian chất lượng",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · prefer (so sánh)",
                "leaves": [
                    tip("prefer to V rather than V", "thích V hơn là V"),
                    tip("prefer V-ing to V-ing", "thích V-ing hơn V-ing"),
                    tip(
                        "I prefer spending time with family rather than going out",
                        "Tôi thích ở với gia đình hơn đi chơi",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Danh từ / mở rộng",
                "leaves": [
                    tip("because / This is because + S + V", "because + mệnh đề"),
                    tip("because of + noun / NP", "because of + danh từ"),
                    tip("close-knit family · quality time · keep in touch", "gia đình gắn bó · thời gian chất lượng · giữ liên lạc"),
                    tip("get along with · confide in · lend a listening ear", "hòa thuận · tâm sự · lắng nghe"),
                ],
            },
        ],
    },
]

LESSON5_MINDMAP_LEFT = [
    {
        "id": "kind-flow",
        "color": "#93c5fd",
        "name": "Loại gì?",
        "name_vi": "What kind?",
        "flow": True,
        "opener": "Well, … · Honestly, …",
        "branches": [
            {
                "label": "Nhánh 1 · Direct",
                "leaves": [
                    tip("I like … most.", "Tôi thích … nhất."),
                    tip(
                        "Family: I like emotionally supportive friends most.",
                        "Family: Tôi thích bạn hỗ trợ cảm xúc nhất.",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Soft choose (hay dùng nhất)",
                "patterns": (
                    "<code>I love all kinds of …, but if I had to choose one, "
                    "it would have to be…</code>"
                ),
                "leaves": [
                    tip(
                        "I love all kinds of friends, but if I had to choose one, it would have to be…",
                        "Tôi thích mọi kiểu bạn, nhưng nếu phải chọn một thì sẽ là…",
                    ),
                    tip("… I would go for …", "… tôi sẽ chọn … (go for)"),
                    tip("… I would opt for …", "… tôi sẽ chọn … (opt for — formal hơn)"),
                ],
            },
            {
                "label": "Nhánh 3 · People kinds (gợi ý chọn)",
                "leaves": [
                    tip(
                        "emotionally supportive · like-minded · childhood friends",
                        "hỗ trợ cảm xúc · cùng chí hướng · bạn thời thơ ấu",
                    ),
                    tip(
                        "nuclear / extended / blended / close-knit family",
                        "hạt nhân / đại gia đình / tái hợp / gắn bó",
                    ),
                    tip(
                        "honesty · mutual trust · compatibility · empathy · loyalty",
                        "trung thực · tin tưởng lẫn nhau · hòa hợp · đồng cảm · trung thành",
                    ),
                    tip(
                        "attracted to honest people · live in harmony with somebody",
                        "bị thu hút bởi người thành thật · chung sống hòa hợp (TAK12)",
                    ),
                ],
            },
        ],
        "link": "→ <strong>because / This is because</strong> + Lý do (phải)",
    },
]

LESSON5_MINDMAP_RIGHT = [
    {
        "id": "kind-reason-flow",
        "color": "#fcd34d",
        "name": "Lý do",
        "name_vi": "Reason",
        "flow": True,
        "opener": "because · This is because · because of",
        "branches": [
            {
                "label": "Nhánh 1 · Mệnh đề / NP",
                "leaves": [
                    tip("because / This is because + S + V", "because + mệnh đề"),
                    tip("because of + noun / NP", "because of + danh từ / cụm DT"),
                    tip(
                        "This is because mutual trust is essential for building strong relationships",
                        "Vì sự tin tưởng lẫn nhau là then chốt để xây mối quan hệ bền",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Mở rộng (try / compare)",
                "patterns": (
                    "<code>try not to + V</code> · <code>try to + V</code> · "
                    "<code>try + V-ing</code>"
                ),
                "leaves": [
                    tip(
                        "I try not to judge people too quickly",
                        "Tôi cố không phán xét người khác quá nhanh",
                    ),
                    tip(
                        "I try to stay connected with like-minded friends",
                        "Tôi cố giữ liên lạc với bạn cùng chí hướng",
                    ),
                    tip(
                        "You should try sharing your thoughts more openly",
                        "Bạn nên thử chia sẻ suy nghĩ cởi mở hơn (try + V-ing)",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Family (collocation hay)",
                "patterns": "Cụm band 7+ từ DOL / ECE / IDP / ZIM — thay Lexical Food",
                "leaves": [
                    tip(
                        "emotionally supportive · like-minded individuals",
                        "hỗ trợ cảm xúc · người cùng chí hướng",
                    ),
                    tip(
                        "shared interests · mutual trust · common ground",
                        "sở thích chung · tin tưởng lẫn nhau · điểm chung",
                    ),
                    tip(
                        "close-knit · quality time · sense of belonging",
                        "gắn bó · thời gian chất lượng · cảm giác thuộc về",
                    ),
                    tip(
                        "compatibility · chemistry · affection · attraction",
                        "hòa hợp · hóa học tình cảm · tình cảm · sự thu hút (Fighter)",
                    ),
                    tip(
                        "build / maintain / strengthen a relationship",
                        "xây · duy trì · củng cố mối quan hệ (ECE)",
                    ),
                    tip(
                        "have a strong bond · family bond · lifelong friendship",
                        "gắn kết mạnh · sự gắn bó gia đình · tình bạn lâu dài",
                    ),
                    tip(
                        "unwavering support · pillars of strength",
                        "hỗ trợ kiên định · trụ cột tinh thần",
                    ),
                ],
            },
        ],
        "link": "→ ghép Lesson 2 reasons nếu cần dài thêm 1 câu",
    },
]

LESSON6_MINDMAP_LEFT = [
    {
        "id": "prefer-xy-flow",
        "color": "#c4b5fd",
        "name": "Chọn X / Y",
        "name_vi": "Prefer",
        "flow": True,
        "opener": "Well, … · Honestly, …",
        "branches": [
            {
                "label": "Nhánh 1 · I prefer X",
                "patterns": "X thường là <strong>V-ing</strong> / NP",
                "leaves": [
                    tip("I prefer + V-ing / NP", "Tôi thích hơn + V-ing / danh từ"),
                    tip(
                        "Family: I prefer spending time with my family",
                        "Family: Tôi thích dành thời gian với gia đình hơn",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · I prefer X to Y",
                "patterns": "<code>prefer + V-ing + to + V-ing</code> (cùng form)",
                "leaves": [
                    tip(
                        "I prefer spending time with family to hanging out with a crowd",
                        "Tôi thích ở với gia đình hơn đi chơi với đám đông",
                    ),
                    tip(
                        "I prefer talking face to face to texting all day",
                        "Tôi thích nói chuyện trực tiếp hơn nhắn tin cả ngày",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · I prefer X rather than Y",
                "patterns": "<code>prefer to V rather than V</code>",
                "leaves": [
                    tip(
                        "I prefer to stay with close friends rather than go to big parties",
                        "Tôi thích ở với bạn thân hơn đi tiệc lớn",
                    ),
                    tip(
                        "I lean more towards my friends as a young adult",
                        "Tôi hơi nghiêng về bạn bè khi còn trẻ (ZIM)",
                    ),
                ],
            },
        ],
        "link": "→ <strong>because</strong> + Lý do (ưu điểm X · while · nhược điểm Y)",
    },
]

LESSON6_MINDMAP_RIGHT = [
    {
        "id": "prefer-reason-flow",
        "color": "#fcd34d",
        "name": "Lý do",
        "name_vi": "Reason",
        "flow": True,
        "opener": "because · This is because · while / whereas",
        "branches": [
            {
                "label": "Nhánh 1 · Ưu điểm X / Nhược điểm Y",
                "leaves": [
                    tip(
                        "Ưu điểm của X → more comforting / more meaningful / safer",
                        "Nêu điểm mạnh của lựa chọn X",
                    ),
                    tip(
                        "Nhược điểm của Y → time-consuming / superficial / lonely",
                        "Nêu điểm yếu của Y",
                    ),
                    tip("X …, while / whereas Y …", "Đối chiếu trực tiếp X và Y"),
                ],
            },
            {
                "label": "Nhánh 2 · Cấu trúc slide (Family)",
                "patterns": "Áp dụng đúng ngữ cảnh People & Family — không copy ví dụ Food",
                "leaves": [
                    tip("It takes + time (+ for sb) + to V", "Tốn bao nhiêu thời gian (cho ai) để làm gì"),
                    tip("love the feeling of + V-ing", "Thích cảm giác làm gì"),
                    tip("have someone to + V / confide in", "Có ai đó để làm gì / tâm sự"),
                    tip("lean towards + NP", "Có xu hướng nghiêng về… (ZIM)"),
                    tip("hold a special place in my heart", "Giữ một vị trí đặc biệt trong tim"),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Family (trong contrast)",
                "leaves": [
                    tip(
                        "quality time · comfort and security",
                        "thời gian chất lượng · sự an ủi và an toàn",
                    ),
                    tip(
                        "face-to-face · virtual interaction",
                        "gặp trực tiếp · giao tiếp ảo",
                    ),
                    tip(
                        "close friend · classmate · roommate · colleague",
                        "bạn thân · bạn cùng lớp · bạn cùng phòng · đồng nghiệp",
                    ),
                    tip(
                        "companion · acquaintance · partner",
                        "người đồng hành · người quen · bạn đời",
                    ),
                    tip(
                        "meaningful · long-lasting · harmonious · complicated",
                        "ý nghĩa · bền vững · hòa hợp · phức tạp (ECE adj)",
                    ),
                    tip(
                        "blood is thicker than water",
                        "máu mủ ruột thịt (dùng 1 lần, đúng chỗ)",
                    ),
                ],
            },
        ],
        "link": "→ thêm 1 ví dụ cụ thể để chốt đoạn",
    },
]

LESSON7_MINDMAP_LEFT = [
    {
        "id": "popular-yes-no",
        "color": "#86efac",
        "name": "Có / Không",
        "name_vi": "Yes / No + detail",
        "flow": True,
        "opener": "Yes, it's very popular · No, not really",
        "branches": [
            {
                "label": "Nhánh 1 · Có + số lượng lớn",
                "patterns": "The majority · most · many · a large number / proportion · 60–70%",
                "leaves": [
                    tip("Yes, it's very popular.", "Có, rất phổ biến."),
                    tip("the majority of… / most / many / a lot of", "đa số / hầu hết / nhiều"),
                    tip(
                        "a large proportion of families still live with grandparents",
                        "một tỷ lệ lớn gia đình vẫn sống với ông bà",
                    ),
                    tip("account for + %", "chiếm bao nhiêu %"),
                ],
            },
            {
                "label": "Nhánh 2 · Không + số lượng nhỏ",
                "patterns": "not many · very few · 20–30% · hardly ever / rarely",
                "leaves": [
                    tip("No, it's not really popular. / No, not really.", "Không thực sự phổ biến."),
                    tip("not many · very few · a small proportion", "không nhiều · rất ít"),
                    tip(
                        "Family: arranged marriage every day — rarely mainstream now",
                        "Hôn nhân sắp đặt mỗi ngày — nay ít còn phổ biến",
                    ),
                ],
            },
        ],
        "link": "→ hoặc chuyển sang nhánh <strong>Còn tùy</strong>",
    },
]

LESSON7_MINDMAP_RIGHT = [
    {
        "id": "popular-depends",
        "color": "#fcd34d",
        "name": "Còn tùy",
        "name_vi": "It depends + case",
        "flow": True,
        "opener": "It depends. · It depends on…",
        "branches": [
            {
                "label": "Nhánh 1 · Chia theo người (Family)",
                "leaves": [
                    tip(
                        "Age: young people ↔ older people / elderly",
                        "Tuổi: giới trẻ ↔ người lớn tuổi",
                    ),
                    tip(
                        "Culture: collectivist ↔ individualist",
                        "Văn hóa: tập thể ↔ cá nhân (DOL Part 3)",
                    ),
                    tip(
                        "Place: urban dwellers ↔ rural dwellers",
                        "Nơi sống: thành thị ↔ nông thôn",
                    ),
                    tip(
                        "Income / lifestyle: nuclear households ↔ extended families",
                        "Lối sống: hộ hạt nhân ↔ đại gia đình",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Chia theo thể loại / khu vực (Family)",
                "leaves": [
                    tip(
                        "Relationship types: family / friends / romantic / online",
                        "Loại quan hệ: gia đình · bạn · tình cảm · online",
                    ),
                    tip(
                        "Family structure: patriarchal ↔ matriarchal / egalitarian",
                        "Cấu trúc: gia trưởng ↔ gia mẫu / bình đẳng (Fighter)",
                    ),
                    tip(
                        "kinship · lineage · descendant · disown / cut all ties",
                        "họ hàng · dòng dõi · hậu duệ · từ bỏ / cắt quan hệ (Fighter)",
                    ),
                    tip(
                        "Major cities ↔ countryside (lonely in crowded cities)",
                        "Thành phố lớn ↔ nông thôn (DOL: lonely in crowded cities)",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Cấu trúc slide (Family)",
                "leaves": [
                    tip("account for + %", "Chiếm bao nhiêu phần trăm"),
                    tip("can see sb/sth + V-ing", "Có thể thấy ai/cái gì đang làm gì"),
                    tip("can't stand sth", "Không chịu nổi cái gì"),
                    tip("hardly ever / rarely + V", "Hiếm khi / ít khi + V"),
                    tip("popular with + group", "Phổ biến với nhóm nào"),
                ],
            },
        ],
        "link": "→ chọn 1 trục chia + 1 ví dụ văn hóa Việt",
    },
]

LESSON8_MINDMAP_LEFT = [
    {
        "id": "best-time-direct",
        "color": "#fca5a5",
        "name": "Thời điểm tốt nhất",
        "name_vi": "Best time + reason",
        "flow": True,
        "opener": "… is the best / ideal / perfect time to …",
        "branches": [
            {
                "label": "Nhánh 1 · Khung câu (chọn 1)",
                "leaves": [
                    tip("… is the best time for/to …", "… là thời điểm tốt nhất để …"),
                    tip("… is the greatest / perfect / ideal time to …", "greatest / perfect / ideal"),
                    tip("… is my favourite time to …", "… là thời điểm yêu thích để …"),
                    tip("We should/can do X + thời điểm", "Nên/có thể làm X vào lúc …"),
                ],
            },
            {
                "label": "Nhánh 2 · Lý do / chi tiết (Family)",
                "leaves": [
                    tip("This is because + S + V", "Vì + mệnh đề (lịch / tâm trạng / dịp lễ)"),
                    tip("last (v) + thời gian", "kéo dài bao lâu — Tet lasts about a week"),
                    tip("make it + adj (+ for sb) + to V", "khiến việc … trở nên adj"),
                    tip("So sánh thời điểm khác để kéo dài câu", "vd. On weekdays… / During exam season…"),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Family",
                "leaves": [
                    tip("catch up on each other's day", "cập nhật ngày của nhau (ZIM)"),
                    tip("family dinner · quality time · weekend gathering", "bữa tối gia đình · thời gian chất lượng"),
                    tip("celebrate milestones · Tet reunion", "kỷ niệm mốc · sum họp Tết"),
                    tip("by my side · hold a special place", "ở bên tôi · giữ chỗ đặc biệt trong tim"),
                ],
            },
        ],
        "link": "→ nêu <strong>1 thời điểm</strong> + <strong>1 lý do Family</strong>",
    },
]

LESSON8_MINDMAP_RIGHT = [
    {
        "id": "best-time-depends",
        "color": "#86efac",
        "name": "Còn tùy",
        "name_vi": "It depends + case",
        "flow": True,
        "opener": "It depends. · It depends on…",
        "branches": [
            {
                "label": "Nhánh 1 · Cách chia (phụ thuộc câu hỏi)",
                "leaves": [
                    tip("Sở thích: For me … However, some people…", "Tôi … / Một số người …"),
                    tip("Lịch trình: busy weekdays ↔ free weekends", "Ngày thường bận ↔ cuối tuần rảnh"),
                    tip("Loại quan hệ: family / friends / partner", "Chia theo đối tượng"),
                    tip("Mood: chill with friends ↔ comfort from family", "Tâm trạng (ECE)"),
                ],
            },
            {
                "label": "Nhánh 2 · Cấu trúc slide (Family)",
                "leaves": [
                    tip("find + myself / themselves + adj", "thấy bản thân như thế nào"),
                    tip("during this time ≈ after 7 pm / Sunday lunch", "paraphrase khung giờ"),
                    tip("However, generally speaking… / as long as…", "nói chung · miễn là…"),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Family (thêm)",
                "leaves": [
                    tip("make an effort to stay connected", "nỗ lực giữ liên lạc"),
                    tip("open and honest communication", "giao tiếp cởi mở, trung thực"),
                    tip("sentimental value", "giá trị tình cảm (WESET)"),
                ],
            },
        ],
        "link": "→ chọn <strong>1 trục chia</strong> + linker hay",
    },
]

LESSON9_MINDMAP_LEFT = [
    {
        "id": "first-last-clear",
        "color": "#fca5a5",
        "name": "Nói rõ thời gian",
        "name_vi": "As far as I can remember + time",
        "flow": True,
        "opener": "As far as I can remember, …",
        "branches": [
            {
                "label": "Nhánh 1 · Khung câu (chọn 1)",
                "leaves": [
                    tip("the first/last time I did X was … + thời gian", "Lần đầu/gần nhất tôi làm X là …"),
                    tip("I first/last did X when …", "Tôi lần đầu/gần nhất làm X khi …"),
                    tip("it's been … since I first/last did X", "Đã … kể từ lần đầu/gần nhất"),
                    tip("Just a month ago. / About 10 years ago. / Last Tet, …", "Mốc thời gian ngắn gọn"),
                ],
            },
            {
                "label": "Nhánh 2 · Kéo dài câu (slide → Family)",
                "leaves": [
                    tip("get in contact / lose contact", "liên lạc lại / mất liên lạc (TAK12)"),
                    tip("spend + time + V-ing", "Dành bao lâu làm gì"),
                    tip("come over to + V", "Đến nhà để làm gì"),
                    tip("reconcile after years of not speaking", "hàn gắn sau nhiều năm (ZIM)"),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Family (tái dùng L3–L8)",
                "leaves": [
                    tip("keep in touch · send a friend request", "giữ liên lạc · gửi lời mời kết bạn"),
                    tip("hold a special place · we had a great time", "giữ chỗ đặc biệt · chúng tôi vui vẻ"),
                    tip("reunite · catch up on old memories", "gặp lại · ôn kỷ niệm cũ"),
                ],
            },
        ],
        "link": "→ nêu <strong>1 mốc thời gian</strong> + <strong>1–2 chi tiết Family</strong>",
    },
]

LESSON9_MINDMAP_RIGHT = [
    {
        "id": "first-last-guess",
        "color": "#86efac",
        "name": "Không nhớ rõ, đoán",
        "name_vi": "I guess + approximate time",
        "flow": True,
        "opener": "I can't remember exactly, but I guess…",
        "branches": [
            {
                "label": "Nhánh 1 · Cụm mở (chọn 1)",
                "leaves": [
                    tip("I'm not really sure but I guess…", "Không chắc lắm nhưng đoán là…"),
                    tip("I can't remember exactly, but I guess…", "Không nhớ chính xác, nhưng đoán là…"),
                ],
            },
            {
                "label": "Nhánh 2 · Khung sau guess",
                "leaves": [
                    tip("the first/last time … was when …", "sau guess → gắn mốc gần đúng"),
                    tip("I first/last … when I was in …", "gắn với giai đoạn đời (high school / uni)"),
                    tip("About … ago / in my second year of…", "ước lượng thời gian"),
                ],
            },
            {
                "label": "Nhánh 3 · Chi tiết + cảm xúc (Family)",
                "leaves": [
                    tip("I felt thrilled · I missed her a lot", "tôi thấy vui sướng · tôi nhớ cô ấy nhiều"),
                    tip("What a shame! / We recalled our old days", "tiếc quá / chúng tôi ôn ngày cũ"),
                    tip("We had a great time together", "kết bài ấm"),
                ],
            },
        ],
        "link": "→ <strong>1 cụm đoán</strong> + mốc gần đúng + 1 chi tiết Family",
    },
]

LESSON10_MINDMAP_LEFT = [
    {
        "id": "child-yes",
        "color": "#fca5a5",
        "name": "Có + lý do",
        "name_vi": "Yes, I did + detail",
        "flow": True,
        "opener": "Yes, I did. / Yes, … when I was a child …",
        "branches": [
            {
                "label": "Nhánh 1 · Mở (chọn 1)",
                "leaves": [
                    tip("Yes, I did.", "Vâng, tôi có"),
                    tip("Yes, … when I was a child …", "Vâng, … khi tôi còn nhỏ …"),
                ],
            },
            {
                "label": "Nhánh 2 · Cụm thời gian childhood",
                "leaves": [
                    tip("When I was a kid / very small / little", "Khi còn nhỏ / rất nhỏ"),
                    tip("When I was … (years old)", "Khi tôi … tuổi"),
                    tip("When I was in primary school", "Khi học tiểu học"),
                    tip(
                        "I can't remember exactly how old I was, but I was probably about …",
                        "Không nhớ chính xác tuổi, nhưng chắc khoảng …",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Kéo dài (slide → Family)",
                "leaves": [
                    tip("My mom told me that …", "Mẹ bảo rằng …"),
                    tip("help sb with sth · help sb (to) V", "giúp mẹ việc nhà / chăm em"),
                    tip("encourage sb to + V", "khuyến khích tâm sự / giữ liên lạc"),
                    tip("values were instilled in me", "giá trị được thấm nhuần (ZIM)"),
                    tip("I take after / look up to …", "tôi giống / ngưỡng mộ …"),
                ],
            },
        ],
        "link": "→ <strong>Yes</strong> + 1 cụm thời gian + 1–2 chi tiết Family",
    },
]

LESSON10_MINDMAP_RIGHT = [
    {
        "id": "child-no",
        "color": "#86efac",
        "name": "Không + lý do",
        "name_vi": "No, not really + detail",
        "flow": True,
        "opener": "No, I didn't. / No, not really.",
        "branches": [
            {
                "label": "Nhánh 1 · Mở (chọn 1)",
                "leaves": [
                    tip("No, I didn't.", "Không"),
                    tip("No, not really.", "Không thật sự"),
                    tip("No, … when I was a child …", "Không, … khi còn nhỏ …"),
                ],
            },
            {
                "label": "Nhánh 2 · Lý do / chi tiết",
                "leaves": [
                    tip("not really interested in + N", "không thật sự thích …"),
                    tip("find + sth + adj", "thấy cái gì như thế nào"),
                    tip("did + V (nhấn mạnh)", "I did see my cousins sometimes but not too often"),
                    tip("spent most of my time + V-ing", "dành phần lớn thời gian …"),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Family (tái dùng)",
                "leaves": [
                    tip("upbringing · family ties · only child", "sự nuôi dưỡng · mối quan hệ gia đình · con một"),
                    tip("immediate family · live under the same roof", "gia đình gần · sống chung mái nhà"),
                    tip("like father, like son · a chip off the old block", "cha nào con nấy · giống bố như đúc"),
                ],
            },
        ],
        "link": "→ <strong>No</strong> + childhood time + find/did-emphasize + 1 collocation cũ",
    },
]

LESSON11_MINDMAP_LEFT = [
    {
        "id": "suit-yes",
        "color": "#fca5a5",
        "name": "Có + lý do",
        "name_vi": "Yes / suitable / great idea",
        "flow": True,
        "opener": "Yes, I think so. · Yes, it would be a great idea…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở (chọn 1)",
                "leaves": [
                    tip("Yes, I think so.", "Vâng, tôi nghĩ vậy"),
                    tip("Yes, it's very suitable…", "Vâng, rất phù hợp…"),
                    tip("Yes, it would be a great idea…", "Vâng, ý tưởng tuyệt vời…"),
                    tip("appropriate ≈ suitable", "appropriate = phù hợp"),
                ],
            },
            {
                "label": "Nhánh 2 · Kéo dài (slide → Family)",
                "leaves": [
                    tip("need + time / trust for …", "cần thời gian/niềm tin cho …"),
                    tip("Plus / Moreover / In addition", "nối lý do 2"),
                    tip("Anyone from A to B can… · It's also a great way to…", "kids → elderly"),
                    tip("long-distance can succeed with strong communication", "yêu xa thành công nếu giao tiếp tốt (WESET)"),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Family (tái dùng)",
                "leaves": [
                    tip("mutual trust · compatibility · commitment", "tin tưởng lẫn nhau · hòa hợp · cam kết"),
                    tip("open and honest communication", "giao tiếp cởi mở, trung thực"),
                    tip("quality time · emotional closeness", "thời gian chất lượng · sự gần gũi cảm xúc"),
                ],
            },
        ],
        "link": "→ <strong>Yes</strong> + because + (Plus) + 1 collocation Family",
    },
]

LESSON11_MINDMAP_RIGHT = [
    {
        "id": "suit-no",
        "color": "#fcd34d",
        "name": "Không + lý do",
        "name_vi": "No / not suitable / not a good idea",
        "flow": True,
        "opener": "No, I don't think so. · No, it's not really suitable…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở (chọn 1)",
                "leaves": [
                    tip("No, I don't think so.", "Không, tôi không nghĩ vậy"),
                    tip("No, not really.", "Không thật sự"),
                    tip("No, I don't think it's a good idea…", "Không phải ý hay…"),
                ],
            },
            {
                "label": "Nhánh 2 · Cấu trúc slide",
                "leaves": [
                    tip("… ; that's the reason why …", "nối nguyên nhân → kết quả"),
                    tip("in search of …", "tìm kiếm … — a healthier relationship"),
                    tip("adj + enough + to V", "đủ … để … — mature enough to…"),
                    tip(
                        "love at first sight is more physical attraction than a meaningful bond",
                        "tình yêu sét đánh nghiêng về hấp dẫn thể xác (ZIM / Mc)",
                    ),
                    tip(
                        "borrowing money from a friend can be a deal-breaker",
                        "mượn tiền bạn có thể là điều chấm dứt quan hệ (TAK12)",
                    ),
                ],
            },
        ],
        "link": "→ <strong>No</strong> + because + that's the reason why",
    },
    {
        "id": "suit-depends",
        "color": "#86efac",
        "name": "Còn tùy",
        "name_vi": "It depends + case (good ↔ bad)",
        "flow": True,
        "opener": "It depends. · It depends on…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở",
                "leaves": [
                    tip("It depends.", "Còn tùy"),
                    tip("It depends on…", "Còn tùy vào… (niềm tin / khoảng cách / tuổi)"),
                ],
            },
            {
                "label": "Nhánh 2 · If … then … / But if …",
                "leaves": [
                    tip("If …, then I would say yes", "trường hợp tốt (trust / communication)"),
                    tip("But if … mainly for …, then not really suitable", "trường hợp xấu (jealousy / no effort)"),
                    tip("mainly for + N / V-ing", "chủ yếu cho / để …"),
                ],
            },
        ],
        "link": "→ <strong>It depends</strong> + 1 case tốt + 1 case xấu",
    },
]

LESSON12_MINDMAP_LEFT = [
    {
        "id": "easy-yes",
        "color": "#86efac",
        "name": "Dễ + lý do",
        "name_vi": "easy / simple · not really difficult",
        "flow": True,
        "opener": "It's very/quite/really easy/simple to… · It's not really difficult…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở (chọn 1)",
                "leaves": [
                    tip("It's very / quite / really easy / simple to…", "Rất / khá / thật sự dễ / đơn giản để…"),
                    tip("It's not really difficult / hard / challenging to…", "Không thật sự khó / thách thức để…"),
                ],
            },
            {
                "label": "Nhánh 2 · Kéo dài (slide → Family)",
                "leaves": [
                    tip("You can + V / There are… nearby", "join a club · meet like-minded people"),
                    tip("However, …", "đối chiếu nhẹ — adults vs children (TAK12)"),
                    tip("shared interests · common ground", "sở thích chung · điểm chung"),
                ],
            },
        ],
        "link": "→ <strong>Dễ</strong> + lý do + 1 collocation Family",
    },
]

LESSON12_MINDMAP_RIGHT = [
    {
        "id": "easy-hard",
        "color": "#fca5a5",
        "name": "Khó + lý do",
        "name_vi": "difficult / hard / challenging · hardest part",
        "flow": True,
        "opener": "It's quite/very/really difficult… · the hardest part is…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở (chọn 1)",
                "leaves": [
                    tip("It's quite / very / really difficult / hard / challenging…", "Khá / rất / thật sự khó…"),
                    tip("It's not really easy / simple to…", "Không thật sự dễ…"),
                    tip("I think the hardest part is…", "Phần khó nhất là…"),
                ],
            },
            {
                "label": "Nhánh 2 · Thời gian (slide)",
                "leaves": [
                    tip("take + sb + time + to V", "It took me years to rebuild trust…"),
                    tip("take + time + for sb/sth + to V", "It takes time for adults to…"),
                    tip("especially for…", "đặc biệt với busy people / introverts"),
                ],
            },
        ],
        "link": "→ <strong>Khó</strong> + especially / hardest part + take + time",
    },
    {
        "id": "easy-then",
        "color": "#fcd34d",
        "name": "Ban đầu khó → dễ hơn",
        "name_vi": "at first · after a while · not an exception",
        "flow": True,
        "opener": "At first… but after a while, things begin to get a bit easier.",
        "branches": [
            {
                "label": "Nhánh 1 · Khung slide",
                "leaves": [
                    tip(
                        "It's always quite difficult at the beginning when you try something new",
                        "Lúc đầu luôn khá khó khi thử cái mới",
                    ),
                    tip("… is not an exception", "… cũng không phải ngoại lệ"),
                    tip("Take … as an example", "Lấy … làm ví dụ (Take making friends at work…)"),
                ],
            },
            {
                "label": "Nhánh 2 · Tiến trình",
                "leaves": [
                    tip("At first, …", "Lúc đầu, …"),
                    tip(
                        "But after a while, things begin to get a bit easier",
                        "Nhưng sau một thời gian mọi thứ dễ hơn một chút",
                    ),
                ],
            },
        ],
        "link": "→ khung mở + not an exception + Take… + At first / after a while",
    },
]

LESSON13_MINDMAP_LEFT = [
    {
        "id": "dislike-direct",
        "color": "#fca5a5",
        "name": "Nói thẳng + lý do",
        "name_vi": "I don't really like / love…",
        "flow": True,
        "opener": "I don't really like/love… + detail",
        "branches": [
            {
                "label": "Nhánh 1 · Mở",
                "leaves": [
                    tip("I don't really like / love…", "Không thật sự thích / yêu…"),
                    tip("Well, I don't really like…", "Ừ, tôi không thật sự thích…"),
                ],
            },
            {
                "label": "Nhánh 2 · Family detail (tái dùng)",
                "leaves": [
                    tip(
                        "overprotective parents · family pressure · sibling rivalry",
                        "bố mẹ bảo bọc · áp lực gia đình · ganh đua anh chị em",
                    ),
                    tip("can't really enjoy the gathering", "không thật sự tận hưởng buổi họp mặt"),
                ],
            },
        ],
        "link": "→ <strong>Nói thẳng</strong> dislike + 1–2 chi tiết Family",
    },
]

LESSON13_MINDMAP_RIGHT = [
    {
        "id": "dislike-soft",
        "color": "#86efac",
        "name": "Nói vòng · soften",
        "name_vi": "generally speaking · the only thing · apart from that",
        "flow": True,
        "opener": "Generally speaking, I love X, but…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở (chọn 1)",
                "leaves": [
                    tip(
                        "Well, generally speaking, I love X, but sometimes…",
                        "Nói chung tôi thích X, nhưng đôi khi…",
                    ),
                    tip(
                        "… but the only thing I don't really like about X is…",
                        "… nhưng điều duy nhất tôi không thích về X là…",
                    ),
                    tip("but apart from that, I'm fine", "nhưng ngoài điều đó ra thì tôi ổn"),
                ],
            },
            {
                "label": "Nhánh 2 · Grammar slide",
                "leaves": [
                    tip(
                        "it's hard / difficult / easy (for sb) to V",
                        "khó / dễ (cho ai) để làm gì — set boundaries / say no",
                    ),
                    tip(
                        "stab someone in the back · fall out with",
                        "đâm sau lưng · cãi nhau / cắt đứt (TAK12)",
                    ),
                ],
            },
        ],
        "link": "→ love X trước → 1 điểm dislike → consequence / apart from that",
    },
    {
        "id": "dislike-list",
        "color": "#fcd34d",
        "name": "Nói vòng · liệt kê",
        "name_vi": "a few things · First / Second / Finally",
        "flow": True,
        "opener": "There are a few things that I don't really love about X.",
        "branches": [
            {
                "label": "Nhánh 1 · Mở + sequence",
                "leaves": [
                    tip(
                        "Well, there are a few things that I don't really love about X",
                        "Có vài điều tôi không thật sự thích về X",
                    ),
                    tip("First / Firstly / The first thing is…", "Đầu tiên"),
                    tip("Second / Secondly / The second thing is…", "Thứ hai"),
                    tip("Finally, …", "Cuối cùng"),
                ],
            },
            {
                "label": "Nhánh 2 · Lexical Family",
                "leaves": [
                    tip(
                        "miscommunication · financial stress · family pressure",
                        "hiểu lầm · áp lực tài chính · áp lực gia đình (Mc Part 3)",
                    ),
                    tip(
                        "overdependence on digital communication · mistrust",
                        "lạm dụng chat · sự nghi ngờ",
                    ),
                ],
            },
        ],
        "link": "→ liệt kê 2–3 điểm + First / Second / Finally",
    },
]

LESSON14_MINDMAP_LEFT = [
    {
        "id": "freq-level",
        "color": "#86efac",
        "name": "Mức độ thường xuyên",
        "name_vi": "always → never (5 bậc)",
        "flow": True,
        "opener": "once a week · usually · hardly ever · once in a blue moon…",
        "branches": [
            {
                "label": "Rất thường xuyên",
                "leaves": [
                    tip("always · all the time · every day / almost every day", "luôn · mọi lúc · mỗi ngày"),
                    tip("five days a week · very often · a lot", "5 ngày/tuần · rất thường"),
                ],
            },
            {
                "label": "Thường / khá thường",
                "leaves": [
                    tip("usually · often · regularly · frequently", "thường · thường xuyên"),
                    tip("quite often · 2 or 3 times a week · once a week", "khá thường · 2–3 lần/tuần"),
                ],
            },
            {
                "label": "Thỉnh thoảng → không bao giờ",
                "leaves": [
                    tip("sometimes · occasionally · every now and then", "thỉnh thoảng"),
                    tip("hardly ever · once in a blue moon · never", "hiếm · năm thì mười họa"),
                    tip("at least once a month (TAK12)", "ít nhất mỗi tháng một lần"),
                ],
            },
        ],
        "link": "→ chọn <strong>1–2</strong> cụm tần suất",
    },
]

LESSON14_MINDMAP_RIGHT = [
    {
        "id": "freq-detail",
        "color": "#fcd34d",
        "name": "Lý do / chi tiết",
        "name_vi": "when · why · with whom · example",
        "flow": True,
        "opener": "at the weekend · because · I also…",
        "branches": [
            {
                "label": "Nhánh 1 · Kéo dài",
                "leaves": [
                    tip(
                        "at the weekend when none of us have to work",
                        "cuối tuần khi không ai phải đi làm → họp mặt",
                    ),
                    tip("I also + freq2 (đối chiếu)", "I also keep in touch by message / I hardly ever…"),
                    tip(
                        "make efforts to stay connected · keep each other updated",
                        "nỗ lực giữ liên lạc · cập nhật cho nhau (TAK12)",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Grammar slide → Family",
                "leaves": [
                    tip("none of + group (+ plural V spoken)", "none of us have to rush"),
                    tip("too + adj + to V", "too busy to visit my hometown"),
                    tip(
                        "interesting to V … than to V",
                        "interesting to talk face to face than to scroll alone",
                    ),
                ],
            },
        ],
        "link": "→ tần suất + when/why + (I also…) + 1 grammar nếu khớp",
    },
]

LESSON15_MINDMAP_LEFT = [
    {
        "id": "change-alot",
        "color": "#86efac",
        "name": "Thay đổi nhiều",
        "name_vi": "a lot / a great deal / significantly",
        "flow": True,
        "opener": "It has changed a great deal in recent years…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở mức độ",
                "leaves": [
                    tip("It has changed a lot / a great deal", "đã thay đổi rất nhiều / rất lớn"),
                    tip("It has changed quite a bit / significantly", "khá nhiều / đáng kể"),
                    tip(
                        "in recent years · over the past few decades · since I was a child",
                        "khung thời gian Present Perfect",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Past → Recently (Family)",
                "leaves": [
                    tip(
                        "Past Simple: In the past / A decade ago…",
                        "extended families · letters · sole breadwinners",
                    ),
                    tip(
                        "Present Perfect: But recently… have become / have started",
                        "nuclear households · video calls · dual-income couples",
                    ),
                    tip(
                        "have/has been + V3 (bị động)",
                        "have been replaced by virtual interaction",
                    ),
                ],
            },
        ],
        "link": "→ mức độ + past (QKĐ) + recently (HTHT) + 1 lexical nâng điểm",
    },
]

LESSON15_MINDMAP_RIGHT = [
    {
        "id": "change-little",
        "color": "#fca5a5",
        "name": "Thay đổi ít",
        "name_vi": "hasn't changed much · the only change",
        "flow": True,
        "opener": "It hasn't changed much. The only change is that…",
        "branches": [
            {
                "label": "Nhánh 1 · Mở",
                "leaves": [
                    tip("It hasn't changed much", "không thay đổi nhiều"),
                    tip("It has changed very slightly", "chỉ thay đổi rất nhẹ"),
                    tip("The only change is that…", "Thay đổi duy nhất là…"),
                ],
            },
            {
                "label": "Nhánh 2 · Lexical nâng điểm (Family)",
                "leaves": [
                    tip(
                        "family values · family ties · filial piety",
                        "giá trị gia đình · mối quan hệ · chữ hiếu",
                    ),
                    tip(
                        "a shift towards… · individualist values",
                        "chuyển dịch sang… · giá trị cá nhân (WESET)",
                    ),
                    tip(
                        "an increasing number of · have become more popular",
                        "ngày càng nhiều · trở nên phổ biến hơn",
                    ),
                    tip(
                        "fast-paced lifestyle · face-to-face vs virtual",
                        "lối sống vội vã · trực tiếp vs ảo (DOL)",
                    ),
                    tip(
                        "generation gap · urbanization · nuclear households",
                        "khoảng cách thế hệ · đô thị hóa · hộ hạt nhân",
                    ),
                ],
            },
        ],
        "link": "→ ít đổi + 1 điểm only change + lexical cụm",
    },
]

LESSON16_MINDMAP_LEFT = [
    {
        "id": "p2-frame",
        "color": "#86efac",
        "name": "Khung 5 phần",
        "name_vi": "mở đầu → cơ bản → cốt lõi → cảm nhận → kết",
        "flow": True,
        "opener": "I'm going to talk about… → So, if I had to talk about…, it would have to be…",
        "branches": [
            {
                "label": "1 · Mở đầu",
                "leaves": [
                    tip("I'm going to talk about + X", "mở bài cố định"),
                    tip("which + paraphrase cue card", "đổi từ khóa trên đề → lexical range"),
                ],
            },
            {
                "label": "2 · Thông tin cơ bản",
                "leaves": [
                    tip("Who · How you met · How long", "ai · gặp thế nào · bao lâu"),
                    tip("1 câu đánh giá: Although…, which makes it…", "1 câu dài kết thúc phần cơ bản"),
                ],
            },
            {
                "label": "5 · Kết",
                "leaves": [
                    tip(
                        "So, if I had to talk about [topic], it would have to be [X].",
                        "nhắc lại đề + tên cụ thể",
                    ),
                ],
            },
        ],
        "link": "→ khung xương cố định · cốt lõi chiếm ~60% thời gian",
    },
]

LESSON16_MINDMAP_RIGHT = [
    {
        "id": "p2-core-feel",
        "color": "#fde68a",
        "name": "Cốt lõi + Cảm nhận (Family)",
        "name_vi": "phần dài nhất · biến theo loại cue card",
        "flow": True,
        "opener": "Person · Friendship · Memory",
        "branches": [
            {
                "label": "3 · Cốt lõi (chiếm phần lớn)",
                "leaves": [
                    tip(
                        "Người: appearance + personality + what they do",
                        "caring · supportive · dedicated · selflessness (Mc / ECE)",
                    ),
                    tip(
                        "Tình bạn: how you met + shared interests + trust",
                        "broke the ice · keep in touch · never take for granted (ECE)",
                    ),
                    tip(
                        "Kỷ niệm: occasion + surprise + why memorable",
                        "celebrate milestones · etched in my memory (WESET)",
                    ),
                ],
            },
            {
                "label": "4 · Cảm nhận",
                "leaves": [
                    tip("Lần gần nhất / vì sao ý nghĩa", "personal story ngắn"),
                    tip("I would recommend… / I try to emulate…", "recommendation · noi gương"),
                ],
            },
            {
                "label": "Cue card Family (lọc exam / nguồn)",
                "leaves": [
                    tip(
                        "Admire a family member · good relationship · old friend again",
                        "Mc / ECE / TAK12 Part 2",
                    ),
                ],
            },
        ],
        "link": "→ chọn 1 loại cue · nhồi cốt lõi · cảm nhận ngắn · kết công thức",
    },
]
