"""Build IELTS Speaking-style practice passages (Part 1 / 2 / 3) for exercise pages.

Uses Q&A blocks with natural collocations — vocabulary is grouped by meaning,
not stuffed into one short paragraph. Structures echo IELTS Speaking lessons
(Yes/No + reasons, Part 2 cue card, Part 3 discussion).
"""
from __future__ import annotations

import re
from typing import Callable

# Type: (words: list[dict], topic: str, level: str) -> tuple[str, str]
AnswerFn = Callable[[list[dict], str, str], tuple[str, str]]


def _w(words: list[dict], n: int) -> list[dict]:
    return words[:n]


def _forms(words: list[dict]) -> list[str]:
    return [x["form"] for x in words]


def _glosses(words: list[dict]) -> list[str]:
    return [x.get("vi") or x["form"] for x in words]


def _join_en(items: list[str], conj: str = "and") -> str:
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} {conj} {items[1]}"
    return ", ".join(items[:-1]) + f", {conj} {items[-1]}"


def _join_vi(items: list[str]) -> str:
    return _join_en(items, "và")


def _norm_key(w: str) -> str:
    return re.sub(r"\s+", " ", (w or "").strip().lower())


# Explicit consumption order for Body & Appearance B1 (115 words → 13 Q&A blocks).
BODY_APPEARANCE_WORD_ORDER: list[str] = [
    # Part 1
    "figure", "beauty", "attractiveness", "stunning", "gorgeous", "unattractive",
    "hairstyle", "thick", "shiny", "haircut", "to comb", "to shave",
    "pale", "expression", "spot", "freckle", "frown", "grin",
    "ugliness", "chubby", "overweight", "obese", "underweight", "mean", "hairy",
    "fair", "ginger", "red", "gray-haired", "well-dressed",
    # Part 2
    "race", "little", "curious", "brave",
    "silly", "proud", "experienced", "positive", "negative", "selfish",
    "miserable", "talented", "patient", "keen", "honest", "cruel",
    "warm", "welcoming", "sociable", "generous", "independent", "ambitious", "cool", "annoying", "needy", "stubborn",
    "gentle", "understanding", "skillful", "peaceful", "nature", "individual",
    "doubtful", "bully",
    # Part 3
    "personal", "characteristic", "quality", "horrible", "dependent", "organized",
    "outgoing", "to pretend", "evil", "responsible", "relaxed", "easy", "reliable", "wise",
    "armpit", "hip", "temple", "thumb", "toenail", "fingernail", "joint", "rib", "sole", "eyeball",
    "to breathe", "circulation", "sense", "sight", "hearing", "touch", "smell",
    "waist", "taste", "hormone", "tissue", "nerve", "gesture", "tear", "blood sugar", "kidney", "lung",
    "slow", "to trick", "weak", "childish", "loyal", "open", "mysterious", "determined", "concern", "to appreciate",
]


def reorder_body_appearance_words(words: list[dict]) -> list[dict]:
    """Place vocabulary in semantic order for IELTS Q&A blocks (not raw lesson order)."""
    by_key = {_norm_key(w["word"]): w for w in words}
    ordered: list[dict] = []
    seen: set[str] = set()
    for key in BODY_APPEARANCE_WORD_ORDER:
        item = by_key.get(key)
        if item:
            ordered.append(item)
            seen.add(key)
    for w in words:
        key = _norm_key(w["word"])
        if key not in seen:
            ordered.append(w)
    return ordered


# ── Body & Appearance — curated Q&A (natural IELTS speaking) ───────────────

def _ba_p1_q1(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"Yes, definitely. I care about my {f[0]} and natural {f[1]}. "
        f"I think {f[2]} is subjective — some people look {f[3]} or even {f[4]} without heavy makeup. "
        f"We should never fixate on {f[5]} in others."
    )
    vi = (
        f"Vâng, chắc chắn. Mình quan tâm đến {g[0]} và {g[1]} tự nhiên. "
        f"Mình nghĩ {g[2]} mang tính chủ quan — có người trông {g[3]} hay thậm chí {g[4]} mà không cần trang điểm nặng. "
        f"Không nên chỉ nhìn {g[5]} ở người khác."
    )
    return en, vi


def _ba_p1_q2(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"Not very often. I like a simple {f[0]} — {f[1]}, {f[2]} hair after a good {f[3]}. "
        f"I usually {f[4]} it in the morning, and sometimes I {f[5]} before an interview."
    )
    vi = (
        f"Không thường xuyên lắm. Mình thích {g[0]} đơn giản — tóc {g[1]}, {g[2]} sau khi {g[3]} ưng ý. "
        f"Sáng nào mình cũng {g[4]} tóc, đôi khi {g[5]} trước buổi phỏng vấn."
    )
    return en, vi


def _ba_p1_q3(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    w = _w(words, 6)
    f, g = _forms(w), _glosses(w)
    en = (
        f"Sometimes my face looks a bit {f[0] if len(f)>0 else 'pale'}, especially with a tired {f[1] if len(f)>1 else 'expression'}. "
        f"A small {f[2] if len(f)>2 else 'spot'} before a date is annoying, but a {f[3] if len(f)>3 else 'freckle'} across the nose can look cute. "
        f"I might {f[4] if len(f)>4 else 'frown'} in traffic, then suddenly {f[5] if len(f)>5 else 'grin'} when a friend calls."
    )
    vi = (
        f"Đôi khi mặt mình hơi {g[0] if len(g)>0 else 'nhợt'}, nhất là khi {g[1] if len(g)>1 else 'biểu cảm'} mệt mỏi. "
        f"Một {g[2] if len(g)>2 else 'mụn'} nhỏ trước hẹn hò thì phiền, nhưng {g[3] if len(g)>3 else 'tàn nhang'} trên mũi đôi khi trông dễ thương. "
        f"Kẹt xe thì mình {g[4] if len(g)>4 else 'nhăn mặt'}, rồi bỗng {g[5] if len(g)>5 else 'cười'} khi bạn gọi."
    )
    return en, vi


def _ba_p1_q4(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"Honestly, jokes about someone's {f[0]} feel wrong. "
        f"Calling them {f[1]}, {f[2]}, {f[3]}, or {f[4]} in public is never okay — that humour sounds {f[5]} and {f[6]}. "
        f"Weight and body hair are private topics."
    )
    vi = (
        f"Thật ra, trò đùa về {g[0]} là sai. "
        f"Gọi ai đó {g[1]}, {g[2]}, {g[3]} hay {g[4]} trước đám đông không bao giờ ổn — kiểu đùa đó nghe {g[5]} và {g[6]}. "
        f"Cân nặng và lông trên cơ thể là chuyện riêng."
    )
    return en, vi


def _ba_p1_q5(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"My cousin has {f[0]}, slightly {f[1]} hair — some people say {f[2]}, and my grandpa is proudly {f[3]}. "
        f"In my family, being {f[4]} matters more than hair colour."
    )
    vi = (
        f"Em họ mình có tóc {g[0]}, hơi {g[1]} — có người bảo {g[2]}, còn ông ngoại thì tự hào vì {g[3]}. "
        f"Trong gia đình mình, {g[4]} quan trọng hơn màu tóc."
    )
    return en, vi


def _ba_p2_open(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"I'm going to talk about my close friend Linh, who I've known since university. "
        f"She is {f[3]} but also {f[1]} in spirit — never afraid to try new things. "
        f"Some people wrongly bring up {f[0]} in conversation, but I notice her {f[2]} mind and how she stays calm under pressure."
    )
    vi = (
        f"Mình sẽ nói về bạn thân Linh, quen từ thời đại học. "
        f"Bạn ấy {g[3]} nhưng tinh thần {g[1]} — không ngại thử điều mới. "
        f"Có người nhắc {g[0]} một cách không công bằng, nhưng mình để ý đầu óc {g[2]} của bạn và cách bạn bình tĩnh khi áp lực."
    )
    return en, vi


def _ba_p2_personality(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    traits = _join_en(f[:6])
    traits_vi = _join_vi(g[:6])
    en = (
        f"About her personality, she can be {traits} — it depends on the situation. "
        f"She is {f[6]} and {f[7]}, and I really admire how {f[8]} she is at work. "
        f"She stays {f[9]} even when people are {f[10]}, and she is never {f[11]} when we disagree."
    )
    vi = (
        f"Về tính cách, bạn ấy có thể {traits_vi} — tùy hoàn cảnh. "
        f"Bạn {g[6]} và {g[7]}, mình rất ngưỡng mộ sự {g[8]} khi làm việc. "
        f"Bạn vẫn {g[9]} dù người khác {g[10]}, và không bao giờ {g[11]} khi bất đồng."
    )
    return en, vi


def _ba_p2_more_traits(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"She is also {f[0]}, {f[1]}, and {f[2]} with new colleagues. "
        f"Her {f[4]}, {f[5]} side is {f[6]} and {f[3]}; she stays {f[2]} at work. "
        f"Even when people act {f[7]} or {f[8]}, she keeps her patience — though she hates feeling {f[9]}."
    )
    vi = (
        f"Bạn còn {g[0]}, {g[1]} và {g[2]} với đồng nghiệp mới. "
        f"Phần {g[4]}, {g[5]} của bạn {g[6]} và {g[3]}; làm việc rất {g[2]}. "
        f"Dù người khác {g[7]} hay {g[8]}, bạn vẫn giữ bình tĩnh — dù ghét cảm giác {g[9]}."
    )
    return en, vi


def _ba_p2_close(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"So if I had to describe one {f[5]} I admire, it would be her. "
        f"Her {f[4]} is {f[0]} and {f[1]}, and she stays {f[2]} yet {f[3]} under pressure. "
        f"She is never a {f[7]} — even when others feel {f[6]} about the future."
    )
    vi = (
        f"Vậy nếu phải mô tả một {g[5]} mình ngưỡng mộ, đó là bạn ấy. "
        f"{g[4]} bạn {g[0]} và {g[1]}, vẫn {g[2]} mà {g[3]} khi áp lực. "
        f"Bạn không bao giờ là {g[7]} — dù người khác {g[6]} về tương lai."
    )
    return en, vi


def _ba_p3_q1(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"I think it has changed quite a bit. In the past, people judged others by fixed standards and ignored {f[0]} {f[1]}. "
        f"Nowadays we value inner {f[2]} more — though being {f[3]} or overly {f[4]} should not define anyone. "
        f"Staying {f[5]} still helps at school and work."
    )
    vi = (
        f"Mình nghĩ đã thay đổi khá nhiều. Ngày xưa người ta phán xét theo chuẩn mắc cố định, bỏ qua {g[0]} {g[1]}. "
        f"Nay ta coi trọng {g[2]} bên trong hơn — dù {g[3]} hay quá {g[4]} không nên định nghĩa ai. "
        f"Giữ {g[5]} vẫn hữu ích ở trường và công việc."
    )
    return en, vi


def _ba_p3_q2(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"Sadly, an {f[0]} influencer may {f[1]} to be perfect online — that is {f[2]} messaging for teenagers. "
        f"We need {f[3]}, {f[4]} role models, not people who only seem {f[5]} or {f[6]}. "
        f"A {f[7]} leader sets a better example."
    )
    vi = (
        f"Đáng buồn là người {g[0]} có thể {g[1]} hoàn hảo trên mạng — thông điệp {g[2]} với tuổi teen. "
        f"Cần hình mẫu {g[3]}, {g[4]} chứ không phải người chỉ trông {g[5]} hay {g[6]}. "
        f"Một nhà lãnh đạo {g[7]} là gương tốt hơn."
    )
    return en, vi


def _ba_p3_q3(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"Body language matters too. After exercise I notice my {f[0]} sweating, my {f[1]} moving when I dance, "
        f"and how my {f[3]} holds a pen while my {f[2]} aches in the sun. "
        f"A broken {f[5]} or {f[4]} is painful; every {f[6]} and {f[7]} reminds me to stretch. "
        f"The {f[8]} of my foot feels the ground, and my {f[9]} needs rest after screens."
    )
    vi = (
        f"Ngôn ngữ cơ thể cũng quan trọng. Sau tập mình thấy {g[0]} đổ mồ hôi, {g[1]} chuyển động khi nhảy, "
        f"và cách {g[3]} cầm bút trong khi {g[2]} nhức dưới nắng. "
        f"{g[5]} hay {g[4]} gãy rất đau; mỗi {g[6]} và {g[7]} nhắc mình duỗi người. "
        f"{g[8]} cảm nhận mặt đất, còn {g[9]} cần nghỉ sau màn hình."
    )
    return en, vi


def _ba_p3_q4(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"I {f[0]} slowly so {f[1]} stays steady. "
        f"{f[3]}, {f[4]}, {f[5]}, {f[6]}, and {f[8]} work with {f[2]} as one way of being alive. "
        f"My {f[7]} moves when I stretch; a {f[13]} may fall after bad news. "
        f"{f[14]}, the {f[15]}, {f[16]}, {f[9]}, {f[10]}, and each {f[11]} keep the body going — a small {f[12]} can say more than a long speech."
    )
    vi = (
        f"Mình {g[0]} chậm để {g[1]} ổn định. "
        f"{g[3]}, {g[4]}, {g[5]}, {g[6]} và {g[8]} cùng {g[2]} như một cách cảm nhận cuộc sống. "
        f"{g[7]} chuyển động khi duỗi; {g[13]} có thể rơi sau tin xấu. "
        f"{g[14]}, {g[15]}, {g[16]}, {g[9]}, {g[10]} và mỗi {g[11]} giữ cơ thể vận hành — một {g[12]} nhỏ đôi khi nói nhiều hơn cả bài dài."
    )
    return en, vi


def _ba_p3_traits(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"I value {f[4]} and {f[5]} friends who are {f[7]} when life gets hard — not {f[3]} or {f[2]}. "
        f"Even a {f[6]} person can be trustworthy if they never {f[1]} you. "
        f"I {f[9]} honesty, and a little {f[8]} shows they truly care — even if they seem {f[0]} to open up at first."
    )
    vi = (
        f"Mình trân trọng bạn {g[4]} và {g[5]} — {g[7]} khi khó khăn, không {g[3]} hay {g[2]}. "
        f"Người {g[6]} vẫn đáng tin nếu không {g[1]} bạn. "
        f"Mình {g[9]} sự trung thực, và chút {g[8]} cho thấy họ thật sự quan tâm — dù ban đầu có vẻ {g[0]}."
    )
    return en, vi


def _ba_p1_extra(words: list[dict], _t: str, _l: str) -> tuple[str, str]:
    """Mop up remaining personality / misc words."""
    w = words
    f, g = _forms(w), _glosses(w)
    chunks_en, chunks_vi = [], []
    for i in range(0, len(f), 3):
        bit = f[i : i + 3]
        bit_vi = g[i : i + 3]
        if bit:
            chunks_en.append(_join_en(bit))
            chunks_vi.append(_join_vi(bit_vi))
    en = (
        "When I describe people, I notice both strengths and weaknesses. "
        + " ".join(
            f"Some friends are {c}, which feels positive; others can be {chunks_en[i+1] if i+1 < len(chunks_en) else 'difficult'}."
            for i, c in enumerate(chunks_en[:1])
        )
        if chunks_en
        else "I try to describe people fairly."
    )
    if len(chunks_en) > 1:
        en += f" I also value people who are {chunks_en[1]}."
    if len(chunks_en) > 2:
        en += f" On bad days someone may seem {chunks_en[2]}, but that does not define them."
    en += f" Overall I stay {f[-2] if len(f)>1 else 'relaxed'} and {f[-1] if len(f)>0 else 'open'} when I speak about appearance and character."
    vi = (
        "Khi mô tả người khác, mình để ý cả điểm mạnh lẫn yếu. "
        + (f"Một số bạn {chunks_vi[0]}, điều đó tích cực." if chunks_vi else "")
        + (f" Mình cũng trân trọng người {chunks_vi[1]}." if len(chunks_vi) > 1 else "")
        + (f" Ngày xấu ai đó có thể {chunks_vi[2]}." if len(chunks_vi) > 2 else "")
        + f" Nhìn chung mình giữ {g[-2] if len(g)>1 else 'thư giãn'} và {g[-1] if len(g)>0 else 'cởi mở'} khi nói về ngoại hình và tính cách."
    )
    return en, vi


BODY_APPEARANCE_SCRIPT: list[dict] = [
    {
        "part": 1,
        "q": "Do you care about your appearance?",
        "q_vi": "Bạn có quan tâm đến ngoại hình của mình không?",
        "fn": _ba_p1_q1,
        "size": 6,
    },
    {
        "part": 1,
        "q": "How often do you change your hairstyle?",
        "q_vi": "Bạn có thường đổi kiểu tóc không?",
        "fn": _ba_p1_q2,
        "size": 6,
    },
    {
        "part": 1,
        "q": "Do you think comments about people's faces can be hurtful?",
        "q_vi": "Bạn có nghĩ nhận xét về mặt mọi người có thể làm tổn thương không?",
        "fn": _ba_p1_q3,
        "size": 6,
    },
    {
        "part": 1,
        "q": "Should people joke about someone's weight?",
        "q_vi": "Mọi người có nên đùa về cân nặng của ai đó không?",
        "fn": _ba_p1_q4,
        "size": 7,
    },
    {
        "part": 1,
        "q": "What hair colours do people in your family have?",
        "q_vi": "Người trong gia đình bạn thường có màu tóc gì?",
        "fn": _ba_p1_q5,
        "size": 5,
    },
    {
        "part": 2,
        "q": "Describe a person you admire.",
        "q_vi": "Hãy mô tả một người bạn ngưỡng mộ.",
        "cue": [
            "who this person is",
            "what he or she looks like",
            "what kind of person he or she is",
            "and explain why you admire him or her",
        ],
        "fn": _ba_p2_open,
        "size": 4,
        "label": "Opening · looks",
    },
    {
        "part": 2,
        "q": None,
        "fn": _ba_p2_personality,
        "size": 12,
        "label": "Core · personality (1)",
    },
    {
        "part": 2,
        "q": None,
        "fn": _ba_p2_more_traits,
        "size": 10,
        "label": "Core · personality (2)",
    },
    {
        "part": 2,
        "q": None,
        "fn": _ba_p2_close,
        "size": 8,
        "label": "Closing",
    },
    {
        "part": 3,
        "q": "How have attitudes towards beauty and character changed in your country?",
        "q_vi": "Thái độ về vẻ đẹp và tính cách ở nước bạn đã thay đổi thế nào?",
        "fn": _ba_p3_q1,
        "size": 6,
    },
    {
        "part": 3,
        "q": "Why do some people admire negative role models online?",
        "q_vi": "Vì sao một số người lại ngưỡng mộ hình mẫu tiêu cực trên mạng?",
        "fn": _ba_p3_q2,
        "size": 8,
    },
    {
        "part": 3,
        "q": "How important is body language in daily communication?",
        "q_vi": "Ngôn ngữ cơ thể quan trọng thế nào trong giao tiếp hàng ngày?",
        "fn": _ba_p3_q3,
        "size": 10,
    },
    {
        "part": 3,
        "q": "Do you think people pay enough attention to their health?",
        "q_vi": "Bạn có nghĩ mọi người đủ chú ý đến sức khỏe không?",
        "fn": _ba_p3_q4,
        "size": 17,
    },
    {
        "part": 3,
        "q": "What personality traits matter most in friendship?",
        "q_vi": "Đặc điểm tính cách nào quan trọng nhất trong tình bạn?",
        "fn": _ba_p3_traits,
        "size": 10,
    },
]


def _run_script(
    script: list[dict], words: list[dict], topic: str, level: str
) -> list[dict]:
    """Execute a topic script, consuming words in order."""
    pool = list(words)
    blocks: list[dict] = []
    sent_id = 0

    for item in script:
        n = item.get("size", 4)
        chunk = pool[:n]
        pool = pool[n:]
        if not chunk and item.get("fn") != _ba_p1_extra:
            continue
        en, vi = item["fn"](chunk, topic, level)
        sent_id += 1
        blocks.append(
            {
                "part": item["part"],
                "q": item.get("q"),
                "q_vi": item.get("q_vi"),
                "cue": item.get("cue"),
                "label": item.get("label"),
                "en": en,
                "vi": vi,
                "words": chunk,
                "sent_id": sent_id,
            }
        )

    if pool:
        en, vi = _ba_p1_extra(pool, topic, level)
        sent_id += 1
        blocks.append(
            {
                "part": 3,
                "q": "Is there anything else you would like to add?",
                "q_vi": "Bạn còn muốn bổ sung gì không?",
                "en": en,
                "vi": vi,
                "words": pool,
                "sent_id": sent_id,
            }
        )
    return blocks


# ── Generic IELTS script (other topics) ────────────────────────────────────

def _generic_part1_yes(words: list[dict], topic: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    topic_l = topic.lower()
    kw = _join_en(f[:4]) if f else topic_l
    kw_vi = _join_vi(g[:4]) if g else topic_l
    en = (
        f"Yes, definitely. I'm quite interested in {topic_l}, especially words like {kw}. "
        f"This is because it gives me the chance to practise natural English in real conversations."
    )
    vi = (
        f"Vâng, chắc chắn. Mình khá quan tâm đến {topic_l}, nhất là các từ như {kw_vi}. "
        f"Vì nó cho mình cơ hội luyện tiếng Anh tự nhiên trong hội thoại thật."
    )
    return en, vi


def _generic_part2(words: list[dict], topic: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    mid = len(f) // 2
    en = (
        f"I'm going to talk about {topic.lower()}, which matters in daily life. "
        f"First, people often mention {_join_en(f[:mid])}. "
        f"Then they also discuss {_join_en(f[mid:])} when the topic comes up in conversation."
    )
    vi = (
        f"Mình sẽ nói về {topic.lower()} — chủ đề quan trọng trong đời sống. "
        f"Trước hết mọi người hay nhắc {_join_vi(g[:mid])}. "
        f"Sau đó còn bàn về {_join_vi(g[mid:])} khi chủ đề xuất hiện trong hội thoại."
    )
    return en, vi


def _generic_part3(words: list[dict], topic: str, _l: str) -> tuple[str, str]:
    f, g = _forms(words), _glosses(words)
    en = (
        f"I think it has changed quite a bit in recent years. "
        f"Nowadays people talk more about {_join_en(f)} when they discuss {topic.lower()}."
    )
    vi = (
        f"Mình nghĩ đã thay đổi khá nhiều trong vài năm gần đây. "
        f"Ngày nay mọi người nói nhiều hơn về {_join_vi(g)} khi bàn về {topic.lower()}."
    )
    return en, vi


def _build_generic_script(words: list[dict], topic: str, level: str) -> list[dict]:
    n = len(words)
    p1_n = max(3, n // 4)
    p2_n = max(4, n // 3)
    p3_n = n - p1_n - p2_n
    pool = list(words)
    blocks = []
    sent_id = 0

    def add(part, q, q_vi, fn, size, **extra):
        nonlocal sent_id, pool
        chunk = pool[:size]
        pool = pool[size:]
        if not chunk:
            return
        en, vi = fn(chunk, topic, level)
        sent_id += 1
        blocks.append(
            {
                "part": part,
                "q": q,
                "q_vi": q_vi,
                "en": en,
                "vi": vi,
                "words": chunk,
                "sent_id": sent_id,
                **extra,
            }
        )

    add(
        1,
        f"Do you like talking about {topic.lower()}?",
        f"Bạn có thích nói về {topic.lower()} không?",
        _generic_part1_yes,
        min(p1_n, len(pool)),
    )
    add(
        1,
        f"How often do you use vocabulary about {topic.lower()}?",
        f"Bạn có thường dùng từ vựng về {topic.lower()} không?",
        _generic_part1_yes,
        min(max(3, p1_n // 2), len(pool)),
    )
    add(
        2,
        f"Describe something important related to {topic.lower()}.",
        f"Hãy mô tả điều gì đó quan trọng liên quan đến {topic.lower()}.",
        _generic_part2,
        min(p2_n, len(pool)),
        cue=["what it is", "when you use it", "why it is important"],
        label="Part 2 cue card",
    )
    add(
        3,
        f"How has {topic.lower()} changed in recent years?",
        f"{topic} đã thay đổi thế nào trong những năm gần đây?",
        _generic_part3,
        len(pool),
    )
    return blocks


TOPIC_SCRIPTS: dict[str, list[dict]] = {
    "body-appearance": BODY_APPEARANCE_SCRIPT,
}


def build_ielts_blocks(words: list[dict], topic_name: str, topic_slug: str, level: str) -> list[dict]:
    script = TOPIC_SCRIPTS.get(topic_slug)
    if script and topic_slug == "body-appearance" and level == "B1":
        words = reorder_body_appearance_words(words)
        return _run_script(script, words, topic_name, level)
    return _build_generic_script(words, topic_name, level)


def blocks_to_sentences(
    blocks: list[dict],
    prepare_pair,
    mark_sentence,
    localize_vi,
    mark_vi_sentence,
    esc,
) -> list[dict]:
    """Convert IELTS blocks to sentence dicts for HTML + coverage check."""
    sentences = []
    for b in blocks:
        chunk = b.get("words") or []
        en_html = mark_sentence(b["en"], chunk)
        vi_local = localize_vi(b["vi"], chunk)
        sentences.append(
            {
                "ielts_part": b["part"],
                "ielts_q": b.get("q"),
                "ielts_q_vi": b.get("q_vi"),
                "ielts_cue": b.get("cue"),
                "ielts_label": b.get("label"),
                "en_html": en_html,
                "vi": vi_local,
                "vi_html": mark_vi_sentence(vi_local, chunk),
                "words": [w["word"] for w in chunk],
                "sent_id": b.get("sent_id"),
            }
        )
    return sentences
