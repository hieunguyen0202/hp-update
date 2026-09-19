#!/usr/bin/env python3
"""Generate People & Family · Review Exercise 2 (Lesson 2, 3, 5–16; skip 4).

Same Linear Thinking format as Food Review Exercise 2. Food leaves that do not
travel (keep fit, burn calories, culinary tradition…) are replaced with
relationship / family phrases from DOL, ECE, TAK12, ZIM, WESET, Mc IELTS, IDP.
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT2 = ROOT / "public" / "blog" / "english" / "people-family" / "review-exercise-2"

_food_spec = importlib.util.spec_from_file_location(
    "food_rev", Path(__file__).with_name("_gen_food_review_exercise.py")
)
_food = importlib.util.module_from_spec(_food_spec)
assert _food_spec and _food_spec.loader
_food_spec.loader.exec_module(_food)

_maps_spec = importlib.util.spec_from_file_location(
    "pf_maps", Path(__file__).with_name("_people_family_review2_maps.py")
)
_maps = importlib.util.module_from_spec(_maps_spec)
assert _maps_spec and _maps_spec.loader
_maps_spec.loader.exec_module(_maps)

_memos_spec = importlib.util.spec_from_file_location(
    "pf_memos", Path(__file__).with_name("_people_family_review2_memos.py")
)
_memos = importlib.util.module_from_spec(_memos_spec)
assert _memos_spec and _memos_spec.loader
_memos_spec.loader.exec_module(_memos)

WORD_SLOTS = _maps.WORD_SLOTS
esc = _food.esc
mind_map_html = _food.mind_map_html
_ex_card_q_html = _food._ex_card_q_html
_pair_answer_html = _food._pair_answer_html
_ex_chip_notes_html = _food._ex_chip_notes_html
lesson_grammar_tree_html = _food.lesson_grammar_tree_html
lesson_scroll_read_html = _food.lesson_scroll_read_html
lesson_grammar_notes_html = _food.lesson_grammar_notes_html
_g_mark = _food._g_mark
_p2_sec = _food._p2_sec


def slot_select(slot_id: str, default_idx: int = 0, *, kind: str = "vocab") -> str:
    opts = WORD_SLOTS[slot_id]
    idx = min(default_idx, len(opts) - 1)
    extra_cls = " lr-idiom-pick" if kind == "idiom" else ""
    options = "\n".join(
        f'<option value="{esc(o["form"])}" title="{esc(o["vi"])}" data-vi="{esc(o["vi"])}"'
        f'{" selected" if i == idx else ""}>{esc(o["form"])}</option>'
        for i, o in enumerate(opts)
    )
    return (
        f'<select class="lr-word-pick{extra_cls}" data-slot="{esc(slot_id)}" '
        f'data-kind="{esc(kind)}" title="Hover option · nghĩa VI" '
        f'aria-label="Choose vocabulary">{options}</select>'
    )


def phrase_pick(slot_id: str, default_idx: int = 0) -> str:
    return slot_select(slot_id, default_idx, kind="phrase")


def vocab_notes_html(items: list[tuple[str, str, str]]) -> str:
    """Vocab notes after Grammar notes — term (VI): explanation."""
    if not items:
        return ""
    rows = []
    for en, vi, meaning in items:
        rows.append(
            f'<p class="lr-vocab-note"><strong>{esc(en)}</strong> '
            f'<em>({esc(vi)})</em>: {esc(meaning)}</p>'
        )
    return f"""
          <div class="lr-grammar-notes lr-vocab-notes">
            <h4 class="lr-grammar-notes-title">Vocab notes</h4>
            <p class="lr-vocab-notes-hint">Từ / cụm mới dùng trong lesson này — đọc nghĩa rồi lắp vào dropdown.</p>
            <div class="lr-vocab-notes-list">
{chr(10).join("              " + r for r in rows)}
            </div>
          </div>"""


def _vocab_gloss(en: str, vi: str, meaning: str) -> str:
    """Same gloss as other lessons: term (VI): explanation — bold purple, no box."""
    return (
        f'<strong>{esc(en)}</strong> '
        f'<em>({esc(vi)})</em>: {esc(meaning)}'
    )


def vocab_think_notes_html(rows: list[dict]) -> str:
    """Lesson 5 vocab: same gloss as other lessons, laid out in 2 columns."""
    body_rows = []
    for row in rows:
        body_rows.append(
            f"""                <tr>
                  <td>{_vocab_gloss(row["en"], row["vi"], row["meaning"])}</td>
                  <td>{_vocab_gloss(row["why_en"], row["why_vi"], row["why_meaning"])}</td>
                </tr>"""
        )
    return f"""
          <div class="lr-grammar-notes lr-vocab-notes lr-vocab-think">
            <h4 class="lr-grammar-notes-title">Vocab notes</h4>
            <p class="lr-vocab-notes-hint">Từ / cụm mới dùng trong lesson này — đọc nghĩa rồi lắp vào <em>because</em>. Trái = <strong>phẩm chất</strong> · Phải = <strong>lý do</strong>.</p>
            <div class="lr-vocab-think-wrap">
              <table class="lr-vocab-think-table">
                <thead>
                  <tr>
                    <th scope="col">Phẩm chất</th>
                    <th scope="col">Lý do</th>
                  </tr>
                </thead>
                <tbody>
{chr(10).join(body_rows)}
                </tbody>
              </table>
            </div>
          </div>"""


def _vmark(text: str) -> str:
    return f"<strong>{esc(text)}</strong>"


def _think_steps_html(steps: list[dict]) -> str:
    """3-step idea notes above a Lesson 5 sample — chunks only, no coaching."""
    if not steps:
        return ""
    lis = []
    for i, st in enumerate(steps, 1):
        title = st.get("title") or f"Bước {i}"
        en = st.get("en") or ""
        lis.append(
            f"""            <li class="lr-think-step">
              <span class="lr-think-step-n">{i}. {esc(title)}</span>
              <span class="lr-think-step-en">{en}</span>
            </li>"""
        )
    return f"""            <ol class="lr-think-steps" aria-label="Tư duy phát triển ý">
{chr(10).join(lis)}
            </ol>"""


VOCAB_L2 = [
    ("unwind / recharge my batteries", "thư giãn / nạp lại năng lượng", "Nghỉ ngơi sau ngày dài để đầu óc nhẹ lại, như sạc pin cho bản thân."),
    ("widen my social circles", "mở rộng vòng tròn xã hội", "Kết thêm bạn, đồng nghiệp, người quen — không chỉ ở trong nhóm cũ."),
    ("like-minded individuals", "những người cùng chí hướng", "Người có cùng sở thích, giá trị hoặc cách nghĩ, nên dễ nói chuyện và kết bạn."),
    ("emotional support", "hỗ trợ về cảm xúc", "Có người lắng nghe, an ủi khi bạn stress hoặc buồn — không chỉ giúp việc thực tế."),
    ("a sense of belonging", "cảm giác thuộc về", "Cảm giác mình là một phần của gia đình / nhóm, được chấp nhận chứ không đứng ngoài."),
    ("strained relationship", "mối quan hệ căng thẳng", "Quan hệ còn đó nhưng gượng, dễ cãi, thiếu thoải mái."),
    ("drift apart", "dần xa nhau", "Không cãi lớn nhưng ít nói, ít gặp, tình cảm tự mỏng đi theo thời gian."),
    ("fall out with someone", "cãi nhau / cắt đứt với ai", "Mất hòa khí sau một chuyện; nặng hơn drift apart vì thường có cãi vã."),
    ("have a strong bond with someone", "có sự gắn kết mạnh mẽ với ai", "Gắn bó sâu: tin tưởng, hiểu nhau, không chỉ là người quen."),
    ("through thick and thin", "trong mọi hoàn cảnh", "Ở bên nhau lúc vui lẫn lúc khó — cụm hay dùng khi nói family / close friends."),
    ("work through disagreements", "giải quyết bất đồng", "Nói chuyện để hết mâu thuẫn, không để chuyện nhỏ thành cãi lớn."),
    ("prevent loneliness", "ngăn cảm giác cô đơn", "Gia đình / bạn bè giúp mình không bị cô lập khi stress hoặc sống xa nhà."),
    ("build / maintain / strengthen a relationship", "xây / duy trì / củng cố mối quan hệ", "Ba động từ ECE: bắt đầu → giữ cho không đứt → làm cho chặt hơn."),
]

VOCAB_L3 = [
    ("close-knit family", "gia đình gắn bó", "Gia đình thường nói chuyện, hỗ trợ nhau, ít xa cách dù bận."),
    ("quality time", "thời gian chất lượng", "Thời gian thật sự dành cho nhau (ăn tối, nói chuyện) — không phải ngồi cùng phòng mà ai cũng dán điện thoại."),
    ("keep in touch", "giữ liên lạc", "Vẫn nhắn / gọi / gặp dù không sống chung."),
    ("confide in", "tâm sự với", "Kể chuyện riêng, chuyện buồn cho người mình tin — không kể với người ngoài."),
    ("hold immense importance", "có ý nghĩa to lớn", "Cụm paraphrase của “very important” — nghe band cao hơn khi nói về gia đình."),
    ("hold a special place in my heart", "giữ một vị trí đặc biệt trong tim", "Vẫn quý / nhớ người đó dù họ đã xa hoặc đã mất."),
    ("passed away", "qua đời", "Cách nói lịch sự hơn “died” — hay dùng khi kể về ông bà."),
    ("get along with", "hòa thuận với", "Sống / chơi với ai mà ít cãi, dễ chịu."),
    ("lend a listening ear", "sẵn sàng lắng nghe", "Sẵn sàng nghe người khác kể chuyện, không vội khuyên hay phán."),
    ("hardly ever + V", "hiếm khi làm gì", "Cách nói NO mềm: không phải “never”, mà gần như không bao giờ — vd. hardly ever feel lonely."),
]

VOCAB_L5 = [
    {
        "en": "emotionally supportive",
        "vi": "hỗ trợ về mặt cảm xúc",
        "meaning": "Bạn / người thân biết lắng nghe và đứng về phía bạn khi bạn gặp chuyện khó.",
        "why_en": "build a relationship",
        "why_vi": "xây dựng mối quan hệ",
        "why_meaning": "Bắt đầu và gây dựng tình bạn / tình cảm từ từ, không phải quen một lần là xong.",
    },
    {
        "en": "like-minded individuals",
        "vi": "những người cùng chí hướng",
        "meaning": "Người cùng gu, cùng giá trị — dễ bond vì có shared interests.",
        "why_en": "strengthen our bond",
        "why_vi": "củng cố sự gắn kết",
        "why_meaning": "Làm cho tình bạn / gia đình chặt hơn nhờ trải nghiệm chung, không chỉ vui lúc gặp.",
    },
    {
        "en": "compatibility",
        "vi": "sự hòa hợp",
        "meaning": "Hợp nhau về tính cách, giá trị, nhịp sống — quan trọng hơn “thích lúc mới gặp”.",
        "why_en": "build a relationship",
        "why_vi": "xây dựng mối quan hệ",
        "why_meaning": "Bắt đầu và gây dựng tình bạn / tình cảm từ từ, không phải quen một lần là xong.",
    },
    {
        "en": "shared interests",
        "vi": "sở thích chung",
        "meaning": "Điểm chung (phim, thể thao, nấu ăn…) giúp hai người nhanh thân.",
        "why_en": "build a relationship",
        "why_vi": "xây dựng mối quan hệ",
        "why_meaning": "Bắt đầu và gây dựng tình bạn / tình cảm từ từ, không phải quen một lần là xong.",
    },
    {
        "en": "loyalty",
        "vi": "lòng trung thành",
        "meaning": "Đứng về phía bạn khi có chuyện, không “đâm sau lưng” hay bỏ rơi.",
        "why_en": "live in harmony with somebody",
        "why_vi": "chung sống hòa hợp với ai",
        "why_meaning": "Ở cùng / chơi cùng mà ít va chạm, biết nhường và tôn trọng nhau.",
    },
    {
        "en": "mutual respect",
        "vi": "sự tôn trọng lẫn nhau",
        "meaning": "Hai bên coi trọng ý kiến và ranh giới của nhau — không áp đặt.",
        "why_en": "live in harmony with somebody",
        "why_vi": "chung sống hòa hợp với ai",
        "why_meaning": "Ở cùng / chơi cùng mà ít va chạm, biết nhường và tôn trọng nhau.",
    },
    {
        "en": "mutual trust",
        "vi": "sự tin tưởng lẫn nhau",
        "meaning": "Hai bên đều tin nhau; thiếu cái này thì dễ sinh nghi.",
        "why_en": "long-lasting / meaningful",
        "why_vi": "bền vững / ý nghĩa",
        "why_meaning": "Quan hệ kéo dài và có chiều sâu, không chỉ vui tạm thời.",
    },
    {
        "en": "honesty",
        "vi": "sự trung thực",
        "meaning": "Nói thật, không giấu chuyện lớn — phẩm chất TAK12 hay gắn với attracted to.",
        "why_en": "attracted to",
        "why_vi": "bị thu hút",
        "why_meaning": "Thấy mình thích / muốn gần ai đó vì tính cách hoặc cách họ cư xử (TAK12).",
    },
    {
        "en": "kindness",
        "vi": "sự tử tế",
        "meaning": "Đối xử nhẹ nhàng, không làm người khác tổn thương — hay đi cặp honesty and kindness.",
        "why_en": "live in harmony with somebody",
        "why_vi": "chung sống hòa hợp với ai",
        "why_meaning": "Ở cùng / chơi cùng mà ít va chạm, biết nhường và tôn trọng nhau.",
    },
    {
        "en": "empathy",
        "vi": "sự đồng cảm",
        "meaning": "Hiểu cảm xúc của người khác — phẩm chất đi cùng emotionally supportive.",
        "why_en": "strengthen our bond",
        "why_vi": "củng cố sự gắn kết",
        "why_meaning": "Làm cho tình bạn / gia đình chặt hơn nhờ trải nghiệm chung, không chỉ vui lúc gặp.",
    },
    {
        "en": "childhood friend",
        "vi": "bạn thời thơ ấu",
        "meaning": "Bạn quen từ nhỏ; thường có kỷ niệm chung nên dễ lifelong friendship.",
        "why_en": "mutual trust",
        "why_vi": "sự tin tưởng lẫn nhau",
        "why_meaning": "Hai bên đều tin nhau; thiếu cái này thì dễ sinh nghi.",
    },
    {
        "en": "attracted to",
        "vi": "bị thu hút",
        "meaning": "Thấy mình thích / muốn gần ai đó vì tính cách hoặc cách họ cư xử (TAK12).",
        "why_en": "loyalty",
        "why_vi": "lòng trung thành",
        "why_meaning": "Đứng về phía bạn khi có chuyện, không “đâm sau lưng” hay bỏ rơi.",
    },
]

VOCAB_L6 = [
    ("lean towards", "nghiêng về (một lựa chọn)", "Thích cả hai nhưng hơi nghiêng về một bên — mềm hơn “I prefer only X” (ZIM)."),
    ("acquaintance", "người quen", "Biết mặt, nói chuyện xã giao, nhưng chưa đủ thân để tâm sự."),
    ("roommate", "bạn cùng phòng", "Người ở chung phòng / nhà; có thể thành companion nếu sống hòa hợp."),
    ("classmate", "bạn cùng lớp", "Học cùng lớp; dễ gặp nhưng chưa chắc là close friend."),
    ("colleague", "đồng nghiệp", "Người làm cùng chỗ — quan hệ công việc, đôi khi thành bạn."),
    ("companion", "người đồng hành", "Người đi cùng mình trong việc / chuyến đi / một giai đoạn đời — gần hơn acquaintance."),
    ("comfort and security", "sự an ủi và an toàn", "Cảm giác được che chở, được hiểu — thường gắn với gia đình hơn đám đông."),
    ("live in harmony with somebody", "chung sống hòa hợp", "Ở chung hoặc chơi thường xuyên mà vẫn êm, ít xung đột."),
]

VOCAB_L7 = [
    ("Collectivist families", "Gia đình theo chủ nghĩa tập thể", "Kiểu gia đình đề cao sự gắn kết cộng đồng, lợi ích và sự hòa hợp của cả gia đình/dòng họ lên trên cái tôi cá nhân."),
    ("Individualist", "theo chủ nghĩa cá nhân", "Đề cao tự do, lựa chọn và thành tựu của từng người hơn là “gia đình bảo sao nghe vậy”."),
    ("Extended kinship", "Họ hàng thân thuộc / đại gia đình", "Gia đình gồm nhiều thế hệ sống chung hoặc giữ mối liên hệ rất chặt (ông bà, cô chú, bác, họ hàng…)."),
    ("Nuclear households", "Gia đình hạt nhân", "Gia đình cơ bản chỉ gồm 2 thế hệ (bố mẹ và con cái chưa kết hôn) sống độc lập, riêng biệt."),
    ("Patriarchal", "có tính chất gia trưởng", "Đàn ông (thường là bố/ông) nắm quyền quyết định chính trong nhà."),
    ("Matriarchal", "có tính chất gia mẫu", "Phụ nữ (mẹ/bà) là người chủ trì, quyết định việc lớn trong gia đình."),
    ("Kinship", "mối quan hệ họ hàng", "Cảm giác “cùng máu mủ” với họ hàng, kể cả khi sống xa."),
    ("Lineage", "dòng họ, dòng dõi", "Dòng họ kéo dài nhiều đời; hay dùng khi nói gia đình có truyền thống nghề / gốc gác."),
    ("Descendant", "con cháu, hậu duệ", "Người thuộc đời sau của một tổ tiên hoặc dòng họ nổi tiếng."),
    ("Disown", "từ bỏ, không nhận là người trong gia đình", "Cắt đứt quan hệ, không còn xem ai đó là thành viên gia đình (thường sau scandal)."),
    ("fast-paced lifestyle", "lối sống vội vã", "Sống ở thành phố lớn: bận, nhanh, ít thời gian gặp người thân — dễ cô đơn dù đông người."),
]

VOCAB_L8 = [
    ("catch up on each other's day", "kể / cập nhật ngày của nhau", "Hỏi nhau hôm nay làm gì, mệt không — cách giữ quality time dù chỉ 15 phút."),
    ("celebrate milestones", "kỷ niệm các mốc quan trọng", "Sinh nhật, tốt nghiệp, nhận việc… — dịp gia đình/bạn bè tụ họp có ý nghĩa."),
    ("live under the same roof", "sống chung một mái nhà", "Ở cùng nhà (thường với bố mẹ / ông bà), nên gặp nhau hàng ngày."),
    ("as long as", "miễn là", "Đặt điều kiện mềm: “Tối nào cũng được, miễn là nói chuyện trực tiếp”."),
]

VOCAB_L9 = [
    ("get in contact / lose contact", "liên lạc lại / mất liên lạc", "Mất số, mất tin tức một thời gian rồi tìm lại (Facebook, bạn chung) hoặc đứt hẳn."),
    ("reconcile", "giải hòa, hàn gắn", "Nói chuyện lại sau khi giận / không nói với nhau nhiều năm."),
    ("a friend request", "lời mời kết bạn (mạng)", "Nút kết bạn trên Facebook / mạng xã hội — hay dùng khi kể gặp lại bạn cũ."),
    ("hold a special place", "giữ vị trí đặc biệt", "Vẫn nhớ / quý người đó dù đã lâu không gặp."),
]

VOCAB_L10 = [
    ("instilled (in me)", "được thấm nhuần", "Bố mẹ / ông bà truyền giá trị từ nhỏ đến mức nó thành thói quen suy nghĩ."),
    ("take after", "giống (người thân)", "Giống bố/mẹ về tính hoặc ngoại hình — “I take after my dad”."),
    ("look up to", "ngưỡng mộ", "Coi ai đó là tấm gương, muốn học theo (thường anh/chị/bố mẹ)."),
    ("upbringing", "sự nuôi dưỡng, cách dạy dỗ", "Cách mình được lớn lên trong gia đình — ảnh hưởng cách cư xử sau này."),
    ("pass down traditional values", "truyền giá trị truyền thống", "Thế hệ trước dạy thế hệ sau về lễ nghĩa, gia đình, cách đối nhân xử thế."),
    ("immediate family", "gia đình gần", "Bố mẹ và anh chị em ruột — khác extended family (họ hàng rộng)."),
    ("like father, like son", "cha nào con nấy", "Idiom: con thường giống bố về tính nết hoặc thói quen."),
]

VOCAB_L11 = [
    ("long-distance relationship", "mối quan hệ yêu xa", "Hai người yêu nhau nhưng ở khác thành phố / khác nước; sống được nhờ tin tưởng và gọi điện thường xuyên."),
    ("love at first sight", "tình yêu sét đánh", "Thích ngay từ lần gặp đầu; nhiều thí sinh nói đây nghiêng về physical attraction hơn meaningful bond."),
    ("deal-breaker", "điều chấm dứt mối quan hệ", "Một thứ không chấp nhận được (nói dối, mượn tiền…) khiến quan hệ dừng lại."),
    ("tell the full story", "cho thấy tất cả / kể hết câu chuyện", "Không nhìn bề ngoài là đủ — quần áo hay số liệu không nói hết con người thật."),
    ("chemistry", "phản ứng hóa học tình cảm", "Cảm giác “hợp sóng”, nói chuyện dễ, bị kéo về phía nhau."),
    ("affection", "tình cảm, lòng yêu mến", "Sự quan tâm thể hiện bằng lời nói, cử chỉ — sâu hơn attraction thoáng qua."),
    ("attraction", "sự thu hút", "Bị lôi cuốn (thường lúc mới gặp); cần commitment mới thành long-term."),
    ("commitment", "sự cam kết", "Hai bên chịu trách nhiệm với nhau, không chỉ “thích thì yêu”."),
    ("harmonious", "hòa hợp", "Quan hệ êm, ít căng, hai bên tôn trọng nhịp của nhau."),
]

VOCAB_L12 = [
    ("common ground", "điểm chung", "Chủ đề / giá trị hai người cùng có — nền để kết bạn hoặc giải quyết bất đồng."),
    ("like-minded individuals", "người cùng chí hướng", "Người cùng gu; hay gặp ở club, lớp học, nhóm sở thích."),
    ("build a relationship", "xây dựng mối quan hệ", "Gây dựng từ đầu: làm quen, tạo tin tưởng."),
    ("maintain a relationship", "duy trì mối quan hệ", "Giữ cho khỏi nguội sau khi đã quen (nhắn, gặp, không “mất hút”)."),
    ("strengthen a relationship", "củng cố mối quan hệ", "Làm cho chặt hơn — trải nghiệm chung, vượt chuyện khó cùng nhau."),
    ("… is not an exception", "… cũng không phải ngoại lệ", "Cái này cũng khó lúc đầu như mọi thứ mới khác."),
]

VOCAB_L13 = [
    ("overprotective (parents)", "bảo bọc quá mức", "Bố mẹ lo đến mức hạn chế tự do của con — hay dùng khi nói dislike về family."),
    ("sibling rivalry", "sự ganh đua giữa anh chị em", "Anh chị em so sánh, giành sự chú ý của bố mẹ."),
    ("stab someone in the back", "đâm sau lưng", "Lừa / nói xấu người đang tin mình — yếu tố làm đổ tình bạn."),
    ("miscommunication", "sự hiểu lầm (do nói không rõ)", "Không hiểu ý nhau, hay xảy ra trên chat / mạng xã hội."),
    ("family bond", "sự gắn bó gia đình", "Sợi dây tình cảm trong nhà; có thể chặt hoặc complicated."),
    ("complicated", "phức tạp", "Quan hệ rối: yêu nhưng hay cãi, hoặc họ hàng nhiều tầng mâu thuẫn."),
    ("fall out with someone", "cãi nhau / cắt đứt với ai", "Mất hòa khí, có thể ngừng nói chuyện một thời gian."),
    ("distant", "xa cách", "Còn quan hệ trên giấy nhưng tình cảm lạnh, ít chia sẻ."),
]

VOCAB_L14 = [
    ("keep in touch", "giữ liên lạc", "Vẫn nhắn/gọi dù không gặp thường xuyên."),
    ("once in a blue moon", "năm thì mười họa", "Rất hiếm — mạnh hơn “sometimes”, gần “almost never”."),
    ("every now and then", "thỉnh thoảng", "Thỉnh thoảng có làm, không đều."),
    ("make efforts to stay connected", "nỗ lực giữ liên lạc", "Chủ động sắp xếp thời gian, không để quan hệ tự chết."),
    ("keep each other updated", "cập nhật cho nhau", "Kể nhau nghe chuyện đời — TAK12 hay dùng với “meet once a month”."),
]

VOCAB_L15 = [
    ("nuclear households", "gia đình hạt nhân", "Chỉ bố mẹ và con, sống riêng — phổ biến hơn ở thành phố lớn ngày nay."),
    ("extended families (under one roof)", "đại gia đình sống chung", "Nhiều thế hệ ở cùng nhà — kiểu phổ biến hơn trong quá khứ / ở quê."),
    ("fast-paced lifestyle", "lối sống vội vã", "Nhịp sống thành phố khiến người ta ít gặp mặt, dù công nghệ kết nối được."),
    ("virtual interaction / face-to-face", "giao tiếp ảo / gặp trực tiếp", "Chat, video call khác gặp thật — ảo tiện nhưng dễ nông hơn."),
    ("a shift towards…", "sự chuyển dịch hướng tới…", "Xã hội nghiêng sang hướng mới (ví dụ individualist values, hộ hạt nhân)."),
    ("individualist values", "giá trị cá nhân", "Coi trọng lựa chọn và sự độc lập của từng người hơn bổn phận dòng họ."),
    ("through thick and thin", "trong mọi hoàn cảnh", "Ở bên nhau lúc vui lẫn lúc khó — cụm hay dùng khi nói family values không đổi."),
    ("family ties", "mối quan hệ gia đình", "Sợi dây họ hàng; có thể mỏng đi nhưng ít khi mất hết."),
]

VOCAB_L16 = [
    ("look up to", "ngưỡng mộ", "Coi người trong gia đình là tấm gương — mở bài Part 2 “admire a person”."),
    ("emulate", "noi gương", "Cố sống / làm việc giống người mình ngưỡng mộ."),
    ("selflessness", "sự vị tha", "Biết giúp người khác, không chỉ nghĩ mình."),
    ("perseverance", "sự bền bỉ", "Không bỏ cuộc khi việc khó — hay kể về anh/chị học hành."),
    ("broke the ice", "phá băng", "Mở lời đầu tiên cho bớt ngại khi mới quen (ECE)."),
    ("take (care) for granted", "xem là đương nhiên", "Không trân trọng sự quan tâm; câu ECE: never take this care for granted."),
    ("through thick and thin", "trong mọi hoàn cảnh", "Bạn/gia đình không bỏ nhau lúc khó."),
    ("sentimental value", "giá trị tình cảm", "Chỗ / món đồ quý vì kỷ niệm, không phải vì đắt (WESET rooftop café)."),
    ("celebrate milestones", "kỷ niệm các mốc", "Sinh nhật 30, tốt nghiệp… — cốt lõi Part 2 “memorable moment”."),
    ("enduring friendship", "tình bạn bền vững", "Tình bạn kéo dài nhiều năm, không chỉ lúc học cùng."),
    ("lose contact / get in contact", "mất liên lạc / liên lạc lại", "Khung kể bạn cũ tìm lại trên Facebook (TAK12)."),
]


def _yes_no_cards(items: list[dict], *, box_id: str, subtitle: str, hint: str) -> str:
    cards = []
    for it in items:
        cards.append(
            f"""          <article class="lr-food-ex-card">
{_ex_card_q_html(it["q"])}
            <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=it["yes_html"], vi=it["yes_vi"], plain=it["yes_plain"], ipa=it.get("yes_ipa", ""), q=it["q"], ex_en=it.get("yes_ex", ""))}
{_pair_answer_html(kind="no", en_html=it["no_html"], vi=it["no_vi"], plain=it["no_plain"], ipa=it.get("no_ipa", ""), q=it["q"], ex_en=it.get("no_ex", ""))}
            </div>
{_ex_chip_notes_html(it.get("notes"))}
          </article>"""
        )
    return f"""
        <div class="lr-food-examples" id="{esc(box_id)}">
          <h3 class="lr-core-subtitle">{esc(subtitle)}</h3>
          <p class="lr-mm-hint">{hint}</p>
{chr(10).join(cards)}
        </div>"""


def _sample_cards(items: list[dict], *, box_id: str, subtitle: str, hint: str) -> str:
    cards = []
    for it in items:
        alts = ""
        if it.get("alt_html"):
            alts = _pair_answer_html(
                kind=it.get("alt_kind", "alt"),
                en_html=it["alt_html"],
                vi=it["alt_vi"],
                plain=it["alt_plain"],
                ipa=it.get("alt_ipa", ""),
                q=it["q"],
                ex_en=it.get("alt_ex", ""),
            )
        think_html = _think_steps_html(it.get("think") or [])
        cards.append(
            f"""          <article class="lr-food-ex-card">
{_ex_card_q_html(it["q"])}
{think_html}
            <div class="lr-food-ex-pair lr-food-ex-pair--kind">
{_pair_answer_html(kind=it.get("kind", "sample"), en_html=it["html"], vi=it["vi"], plain=it["plain"], ipa=it.get("ipa", ""), q=it["q"], ex_en=it.get("ex", ""))}
{alts}
            </div>
{_ex_chip_notes_html(it.get("notes"))}
          </article>"""
        )
    return f"""
        <div class="lr-food-examples" id="{esc(box_id)}">
          <h3 class="lr-core-subtitle">{esc(subtitle)}</h3>
          <p class="lr-mm-hint">{hint}</p>
{chr(10).join(cards)}
        </div>"""


def _memo_v(text: str, vi: str = "") -> str:
    extra = f' data-vi="{esc(vi)}"' if vi else ""
    return f'<mark class="vocab"{extra}>{esc(text)}</mark>'


def _memo_s(text: str, vi: str = "") -> str:
    extra = f' data-vi="{esc(vi)}"' if vi else ""
    return f'<mark class="lr-memo-struct"{extra}>{esc(text)}</mark>'


def _memo_key_stem(en: str) -> str:
    s = re.sub(r"\s*\+\s*(NP|V-ing|V)\b", "", en, flags=re.I)
    s = s.replace("…", " ").replace("...", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def _memo_find_vi(keys: list[tuple[str, str, str]], mark_en: str) -> str:
    m = re.sub(r"\s+", " ", mark_en).strip().lower()
    if not m:
        return ""
    stop = {"to", "a", "an", "the", "of", "for", "in", "on", "or", "and", "with", "is", "it"}
    best, best_n = "", 0
    for k, vi, _kind in keys:
        stem = _memo_key_stem(k)
        if not stem:
            continue
        if m == stem or m.startswith(stem + " ") or stem.startswith(m):
            return vi
        words = [w for w in re.findall(r"[a-z']+", stem) if len(w) > 1 and w not in stop]
        if words and all(w in m for w in words) and len(words) > best_n:
            best, best_n = vi, len(words)
    return best


def _inject_mark_vi(html_src: str, keys: list[tuple[str, str, str]]) -> str:
    """Attach data-vi on memo highlights so Scroll read can blank them with Vietnamese."""

    def repl(match: re.Match) -> str:
        full, cls, inner = match.group(0), match.group(1), match.group(2)
        if "data-vi=" in full:
            return full
        en = html.unescape(re.sub(r"<[^>]+>", "", inner))
        vi = _memo_find_vi(keys, en)
        if not vi:
            return full
        return f'<mark class="{cls}" data-vi="{esc(vi)}">{inner}</mark>'

    return re.sub(r'<mark class="(vocab|lr-memo-struct)">(.*?)</mark>', repl, html_src)


def _memo_sent(en_html: str, vi: str) -> str:
    plain = re.sub(r"<[^>]+>", "", en_html)
    return (
        f'<p class="lr-memo-sent lr-tip lr-answer-text" data-tip="{esc(vi)}" '
        f'data-plain="{esc(plain)}">{en_html}</p>'
    )


def lesson_memo_html(
    *,
    lesson: str,
    sentences: list[tuple[str, str]],
    keys: list[tuple[str, str, str]],
    question: str = "",
) -> str:
    sent_html = _inject_mark_vi(
        "\n              ".join(_memo_sent(en, vi) for en, vi in sentences),
        keys,
    )
    key_lis = []
    for en, vi, kind in keys:
        mark = _memo_s(en) if kind == "s" else _memo_v(en)
        key_lis.append(f"<li>{mark} <em>({esc(vi)})</em></li>")
    q_html = (
        f'<p class="lr-memo-q">{esc(question)}</p>\n            '
        if question
        else ""
    )
    return f"""
          <aside class="lr-memo" id="lesson{esc(lesson)}-memo">
            <div class="lr-memo-head">
              <h4 class="lr-memo-title">Đoạn văn nhớ · Lesson {esc(lesson)}</h4>
              <label class="ex-toggle"><input type="checkbox" class="js-memo-hl" checked> Hiện highlight</label>
            </div>
            <p class="lr-memo-hint">Thuộc đoạn này để nhớ cụm Lesson {esc(lesson)}. <strong>Tím</strong> = cụm từ mới · <strong>Vàng</strong> = cấu trúc. Hover <em>từng câu</em> để xem bản dịch riêng câu đó. Scroll read → nguồn <strong>Đoạn văn nhớ</strong>: Hint <strong>Blank từ mới (VI)</strong> / <strong>Cả đoạn tiếng Việt</strong>.</p>
            {q_html}<div class="lr-memo-body">
              {sent_html}
            </div>
            <ul class="lr-memo-legend" aria-hidden="true">
              <li>{_memo_v("cụm từ mới")}</li>
              <li>{_memo_s("cấu trúc")}</li>
            </ul>
            <ul class="lr-memo-key">
              {chr(10).join("              " + x for x in key_lis)}
            </ul>
          </aside>"""


MEMO_BANK = _memos.lesson_memos(_memo_v, _memo_s)


def memo_html_for(n: str) -> str:
    spec = MEMO_BANK[n]
    return lesson_memo_html(
        lesson=n,
        question=spec["question"],
        sentences=spec["sentences"],
        keys=spec["keys"],
    )


def lesson2_memo_html() -> str:
    return lesson_memo_html(
        lesson="2",
        question="How do you usually relax or unwind after a hard-working day?",
        sentences=[
            (
                f'In my daily life, I always try to {_memo_v("unwind and recharge my batteries")} after a hard-working day.',
                "Trong cuộc sống hàng ngày, tôi luôn cố thư giãn và nạp lại năng lượng sau một ngày làm việc vất vả.",
            ),
            (
                f'Spending time with my family or close friends {_memo_s("helps me feel relaxed")} because we {_memo_v("have a strong bond with each other")}, and they always offer me great {_memo_v("emotional support")}.',
                "Dành thời gian với gia đình hoặc bạn thân giúp tôi cảm thấy thư giãn vì chúng tôi có sự gắn kết mạnh mẽ với nhau, và họ luôn cho tôi sự hỗ trợ cảm xúc lớn.",
            ),
            (
                f'{_memo_s("It\'s also a great way to")} {_memo_v("prevent loneliness")} and {_memo_v("widen my social circles")} to meet {_memo_v("like-minded individuals")}.',
                "Đó cũng là một cách tuyệt vời để ngăn cảm giác cô đơn và mở rộng vòng tròn xã hội để gặp những người cùng chí hướng.",
            ),
            (
                f'However, I believe that ignoring small issues {_memo_s("doesn\'t solve anything")} and {_memo_s("can lead to")} {_memo_v("a strained relationship")}, or even make people {_memo_v("drift apart")}.',
                "Tuy nhiên, tôi tin rằng bỏ qua chuyện nhỏ không giải quyết được gì và có thể dẫn đến một mối quan hệ căng thẳng, thậm chí khiến mọi người dần xa nhau.",
            ),
            (
                f'That\'s why whenever a problem happens, it is important to {_memo_v("work through disagreements")} instead of letting things go too far.',
                "Vì vậy mỗi khi có vấn đề, điều quan trọng là giải quyết bất đồng thay vì để mọi thứ đi quá xa.",
            ),
            (
                f'On the other hand, some people might {_memo_v("fall out with someone")} over trivial things, which is really unfortunate.',
                "Mặt khác, một số người có thể cãi nhau / cắt đứt với ai đó vì chuyện vặt, điều đó thật đáng tiếc.",
            ),
        ],
        keys=[
            ("unwind / recharge my batteries", "thư giãn / nạp lại năng lượng", "v"),
            ("helps me + V", "giúp tôi làm gì — giúp tôi cảm thấy thư giãn", "s"),
            ("have a strong bond with each other", "có sự gắn kết mạnh mẽ với nhau", "v"),
            ("emotional support", "hỗ trợ về cảm xúc", "v"),
            ("It's a great way to + V", "Đó là một cách tuyệt vời để… — ngăn cô đơn / mở rộng vòng tròn xã hội", "s"),
            ("prevent loneliness", "ngăn cảm giác cô đơn", "v"),
            ("widen my social circles", "mở rộng vòng tròn xã hội", "v"),
            ("like-minded individuals", "những người cùng chí hướng", "v"),
            ("doesn't + V", "doesn't solve anything", "s"),
            ("can lead to + NP", "can lead to a strained relationship / drift apart", "s"),
            ("strained relationship", "mối quan hệ căng thẳng", "v"),
            ("drift apart", "dần xa nhau", "v"),
            ("work through disagreements", "giải quyết bất đồng", "v"),
            ("fall out with someone", "cãi nhau / cắt đứt với ai", "v"),
        ],
    )


def lesson3_memo_html() -> str:
    return lesson_memo_html(
        lesson="3",
        question="Do you like spending time with your family?",
        sentences=[
            (
                f'Yes, I\'m a big fan of spending {_memo_v("quality time")} with my family because we are a really {_memo_v("close-knit family")}.',
                "Vâng, tôi rất thích dành thời gian chất lượng với gia đình vì chúng tôi là một gia đình gắn bó.",
            ),
            (
                f'Family {_memo_v("holds immense importance")} to me.',
                "Gia đình có ý nghĩa to lớn với tôi.",
            ),
            (
                f'Whenever I go through a tough time, I can easily {_memo_v("confide in")} my parents, and they always {_memo_v("lend a listening ear")} without judging.',
                "Mỗi khi gặp chuyện khó, tôi có thể dễ dàng tâm sự với bố mẹ, và họ luôn sẵn sàng lắng nghe mà không phán xét.",
            ),
            (
                f'We {_memo_v("get along with")} each other very well.',
                "Chúng tôi hòa thuận với nhau rất tốt.",
            ),
            (
                f'Even though my grandfather has {_memo_v("passed away")}, he still {_memo_v("holds a special place in my heart")}.',
                "Dù ông tôi đã qua đời, ông vẫn giữ một vị trí đặc biệt trong tim tôi.",
            ),
            (
                f'We always make an effort to {_memo_v("keep in touch")} no matter how busy we get, so I {_memo_s("hardly ever feel lonely")}.',
                "Chúng tôi luôn nỗ lực giữ liên lạc dù bận đến mấy, nên tôi hiếm khi cảm thấy cô đơn.",
            ),
        ],
        keys=[
            ("quality time", "thời gian chất lượng", "v"),
            ("close-knit family", "gia đình gắn bó", "v"),
            ("hold immense importance", "có ý nghĩa to lớn", "v"),
            ("confide in", "tâm sự với", "v"),
            ("lend a listening ear", "sẵn sàng lắng nghe", "v"),
            ("get along with", "hòa thuận với", "v"),
            ("passed away", "qua đời", "v"),
            ("hold a special place in my heart", "giữ một vị trí đặc biệt trong tim", "v"),
            ("keep in touch", "giữ liên lạc", "v"),
            ("hardly ever + V", "hardly ever feel lonely — hiếm khi cảm thấy cô đơn", "s"),
        ],
    )


def lesson2_practice_html(*, open_attr: str = " open") -> str:
    home_yes_tpl = (
        "I think because it's a great way to {relax_phrase} after a hard-working day. "
        "Spending time together helps us {bond_phrase}, and they {support_phrase}."
    )
    home_no_tpl = (
        "Well, some people don't enjoy big family gatherings because arguing can lead to "
        "{toxic_outcome} instead of helping anyone unwind."
    )
    edu_yes_tpl = (
        "Yes, because it helps me {edu_phrase}. "
        "I also get the opportunity to {meet_phrase}."
    )
    edu_no_tpl = (
        "No, not really — large networking events aren't my cup of tea. {no_benefit}."
    )
    bond_yes_tpl = (
        "Yes, because it's a great way to {belong_phrase} and {lonely_phrase}. "
        "They also {thick_thin}."
    )
    bond_no_tpl = (
        "No, definitely not because arguing all the time can lead to {toxic_outcome}."
    )
    talk_yes_tpl = (
        "Yes, because if we want to {rel_verb}, we have to {edu_phrase}."
    )
    talk_no_tpl = (
        "If you ignore small issues, it can lead to {toxic_outcome} "
        "rather than helping you {rel_verb}."
    )
    q1 = "Why do people like spending time with family?"
    q2 = "Do you like joining clubs to meet new people?"
    q3 = "Do you like staying close to your relatives?"
    q4 = "Is it important to talk things through with family?"
    cards = f"""
            <div class="lr-practice-source" id="lesson2-practice">
              <article class="lr-food-ex-card">
{_ex_card_q_html(q1)}
                <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=home_yes_tpl.format(relax_phrase=phrase_pick("relax_phrase", 5), bond_phrase=phrase_pick("bond_phrase", 6), support_phrase=phrase_pick("bond_phrase", 0)), vi="Tôi nghĩ vì đó là cách tuyệt để thư giãn và nạp lại năng lượng sau ngày làm việc vất vả. Dành thời gian cùng nhau giúp chúng tôi có sự gắn kết mạnh, và họ mang lại hỗ trợ cảm xúc.", plain="I think because it's a great way to unwind and recharge my batteries after a hard-working day. Spending time together helps us have a strong bond with each other, and they provide emotional support.", ipa="", q=q1, ex_en=home_yes_tpl)}
{_pair_answer_html(kind="no", en_html=home_no_tpl.format(toxic_outcome=phrase_pick("toxic_outcome", 2)), vi="Một số người không thích họp mặt lớn vì cãi nhau có thể dẫn đến mối quan hệ căng thẳng, thay vì giúp ai thư giãn.", plain="Well, some people don't enjoy big family gatherings because arguing can lead to a strained relationship instead of helping anyone unwind.", ipa="", q=q1, ex_en=home_no_tpl)}
                </div>
{_ex_chip_notes_html([{"en": "unwind / recharge my batteries", "vi": "thư giãn / nạp lại năng lượng"}, {"en": "have a strong bond with each other", "vi": "có sự gắn kết mạnh mẽ với nhau"}, {"en": "emotional support", "vi": "hỗ trợ về cảm xúc"}, {"en": "can lead to a strained relationship", "vi": "có thể dẫn đến mối quan hệ căng thẳng"}])}
              </article>
              <article class="lr-food-ex-card">
{_ex_card_q_html(q2)}
                <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=edu_yes_tpl.format(edu_phrase=phrase_pick("edu_phrase", 0), meet_phrase=phrase_pick("edu_phrase", 1)), vi="Có, vì nó giúp tôi mở rộng vòng tròn xã hội. Tôi cũng có cơ hội gặp những người cùng chí hướng.", plain="Yes, because it helps me widen my social circles. I also get the opportunity to meet like-minded individuals.", ipa="", q=q2, ex_en=edu_yes_tpl)}
{_pair_answer_html(kind="no", en_html=edu_no_tpl.format(no_benefit=phrase_pick("no_benefit", 1)), vi="Không thực sự — sự kiện networking lớn không phải sở thích của tôi. Nó không giúp tôi thư giãn.", plain="No, not really — large networking events aren't my cup of tea. It doesn't help me unwind.", ipa="", q=q2, ex_en=edu_no_tpl)}
                </div>
{_ex_chip_notes_html([{"en": "helps me + V", "vi": "giúp tôi làm gì"}, {"en": "widen my social circles", "vi": "mở rộng vòng tròn xã hội"}, {"en": "like-minded individuals", "vi": "người cùng chí hướng"}, {"en": "doesn't + V", "vi": "It doesn't help me unwind"}])}
              </article>
              <article class="lr-food-ex-card">
{_ex_card_q_html(q3)}
                <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=bond_yes_tpl.format(belong_phrase=phrase_pick("bond_phrase", 1), lonely_phrase=phrase_pick("bond_phrase", 4), thick_thin=phrase_pick("thick_thin", 0)), vi="Có, vì đó là cách tuyệt để nuôi dưỡng cảm giác thuộc về và ngăn cô đơn. Họ cũng đứng bên tôi trong mọi hoàn cảnh.", plain="Yes, because it's a great way to foster a sense of belonging and prevent loneliness. They also stand by me through thick and thin.", ipa="", q=q3, ex_en=bond_yes_tpl)}
{_pair_answer_html(kind="no", en_html=bond_no_tpl.format(toxic_outcome=phrase_pick("toxic_outcome", 4)), vi="Không, chắc chắn không — cãi nhau suốt có thể dẫn đến cắt đứt với người mình quý.", plain="No, definitely not because arguing all the time can lead to falling out with someone you care about.", ipa="", q=q3, ex_en=bond_no_tpl)}
                </div>
{_ex_chip_notes_html([{"en": "It's a great way to + V", "vi": "Đó là cách tuyệt để…"}, {"en": "a sense of belonging", "vi": "cảm giác thuộc về"}, {"en": "prevent loneliness", "vi": "ngăn cảm giác cô đơn"}, {"en": "through thick and thin", "vi": "trong mọi hoàn cảnh"}, {"en": "fall out with someone", "vi": "cãi nhau / cắt đứt với ai"}])}
              </article>
              <article class="lr-food-ex-card">
{_ex_card_q_html(q4)}
                <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=talk_yes_tpl.format(rel_verb=phrase_pick("rel_verb", 2), edu_phrase=phrase_pick("edu_phrase", 2)), vi="Có, vì nếu muốn củng cố mối quan hệ, chúng ta phải học cách giải quyết bất đồng.", plain="Yes, because if we want to strengthen a relationship, we have to learn how to work through disagreements.", ipa="", q=q4, ex_en=talk_yes_tpl)}
{_pair_answer_html(kind="no", en_html=talk_no_tpl.format(toxic_outcome=phrase_pick("toxic_outcome", 3), rel_verb=phrase_pick("rel_verb", 0)), vi="Nếu bỏ qua chuyện nhỏ, điều đó có thể khiến mọi người dần xa nhau thay vì giúp bạn xây dựng mối quan hệ.", plain="If you ignore small issues, it can lead to people drifting apart rather than helping you build a relationship.", ipa="", q=q4, ex_en=talk_no_tpl)}
                </div>
{_ex_chip_notes_html([{"en": "build / maintain / strengthen a relationship", "vi": "xây / duy trì / củng cố mối quan hệ"}, {"en": "work through disagreements", "vi": "giải quyết bất đồng"}, {"en": "drift apart", "vi": "dần xa nhau"}, {"en": "can lead to + NP", "vi": "có thể dẫn đến…"}])}
              </article>
            </div>"""
    return f"""
          <details class="lr-formula-details"{open_attr}>
            <summary>Thực hành · Giải trí / Giáo dục / Sức khỏe tinh thần</summary>
            <p class="lr-mm-hint">Mỗi câu <strong>Thích / Không thích</strong> dùng đúng cụm trong Vocab notes (dropdown đổi được cụm cùng nhóm). Sau các câu hỏi: đoạn văn nhớ + highlight.</p>
{cards}
          </details>
{lesson2_memo_html()}
{lesson_scroll_read_html("lesson2", title="Lesson 2", source_sel="#lesson2-practice", memo_sel="#lesson2-memo")}"""


def lesson3_examples_html() -> str:
    items = []
    t1y = (
        "Yes, I'm a big fan of spending {quality_time} with my family because we are "
        "a really {family_type}."
    )
    t1n = (
        "Well, not really. I hardly ever {hardly_ever_action} because big gatherings "
        "{soft_dislike}. I prefer {prefer_rather_than}."
    )
    items.append({
        "q": "Do you have a close-knit family? (WESET)",
        "yes_html": t1y.format(quality_time=phrase_pick("quality_time", 0), family_type=phrase_pick("family_type", 0)),
        "yes_vi": "Vâng. Tôi rất thích dành thời gian chất lượng với gia đình vì chúng tôi là một gia đình gắn bó.",
        "yes_plain": "Yes, I'm a big fan of spending quality time with my family because we are a really close-knit family.",
        "yes_ex": t1y,
        "no_html": t1n.format(hardly_ever_action=phrase_pick("hardly_ever_action", 1), soft_dislike=phrase_pick("soft_dislike", 2), prefer_rather_than=phrase_pick("prefer_rather_than", 1)),
        "no_vi": "Không thực sự. Tôi hiếm khi đi tiệc lớn vì khá căng thẳng. Tôi thích buổi họp mặt nhỏ hơn.",
        "no_plain": "Well, not really. I hardly ever go to large family parties because big gatherings can feel quite stressful. I prefer small gatherings rather than big parties.",
        "no_ex": t1n,
        "notes": [{"en": "quality time", "vi": "thời gian chất lượng"}, {"en": "close-knit family", "vi": "gia đình gắn bó"}, {"en": "I hardly ever + V", "vi": "hiếm khi + V"}],
    })
    t2y = (
        "Yes, absolutely. Family {importance_phrase}. We {get_along} very well."
    )
    t2n = (
        "I'm a bit more independent these days. I hardly ever {hardly_ever_action} "
        "because of my busy schedule."
    )
    items.append({
        "q": "Is family very important to you? (ZIM / Mc / ECE)",
        "yes_html": t2y.format(importance_phrase=phrase_pick("importance_phrase", 0), get_along=phrase_pick("get_along", 0)),
        "yes_vi": "Vâng. Gia đình có ý nghĩa to lớn với tôi. Chúng tôi hòa thuận với nhau rất tốt.",
        "yes_plain": "Yes, absolutely. Family holds immense importance to me. We get along with each other very well.",
        "yes_ex": t2y,
        "no_html": t2n.format(hardly_ever_action=phrase_pick("hardly_ever_action", 0)),
        "no_vi": "Tôi độc lập hơn. Hiếm khi thăm đại gia đình vì lịch bận.",
        "no_plain": "I'm a bit more independent these days. I hardly ever visit my extended family because of my busy schedule.",
        "no_ex": t2n,
        "notes": [{"en": "hold immense importance", "vi": "có ý nghĩa to lớn"}, {"en": "get along with", "vi": "hòa thuận với"}],
    })
    t3y = (
        "Yes, I do. Whenever I go through a tough time, I can easily {relationship_v} "
        "my parents, and they always {listen_phrase}."
    )
    t3n = (
        "No, not really. I'm pretty picky. I hardly ever open up because I have "
        "an irrational fear that people barely tolerate me."
    )
    items.append({
        "q": "Do you confide in your family when you have problems? (TAK12 / ECE)",
        "yes_html": t3y.format(relationship_v=phrase_pick("relationship_v", 4), listen_phrase=phrase_pick("listen_phrase", 1)),
        "yes_vi": "Có. Mỗi khi gặp chuyện khó, tôi có thể dễ dàng tâm sự với bố mẹ, và họ luôn lắng nghe mà không phán xét.",
        "yes_plain": "Yes, I do. Whenever I go through a tough time, I can easily confide in my parents, and they always lend a listening ear without judging.",
        "yes_ex": t3y,
        "no_html": t3n,
        "no_vi": "Không thực sự. Tôi khá kén. Hiếm khi mở lòng vì sợ người khác chỉ chịu đựng mình (TAK12).",
        "no_plain": "No, not really. I'm pretty picky. I hardly ever open up because I have an irrational fear that people barely tolerate me.",
        "no_ex": t3n,
        "notes": [{"en": "confide in", "vi": "tâm sự với"}, {"en": "lend a listening ear", "vi": "sẵn sàng lắng nghe"}],
    })
    t4y = (
        "Yes, definitely. We always make an effort to {keep_touch} no matter how busy "
        "we get, so I hardly ever {hardly_ever_action}."
    )
    t4n = (
        "No, not really. I prefer {prefer_rather_than} because big groups {soft_dislike}."
    )
    items.append({
        "q": "Do you like spending time with your family? (ZIM / WESET)",
        "yes_html": t4y.format(keep_touch=phrase_pick("keep_touch", 0), hardly_ever_action=phrase_pick("hardly_ever_action", 4)),
        "yes_vi": "Vâng. Chúng tôi luôn nỗ lực giữ liên lạc dù bận đến mấy, nên tôi hiếm khi cảm thấy cô đơn.",
        "yes_plain": "Yes, definitely. We always make an effort to keep in touch no matter how busy we get, so I hardly ever feel lonely.",
        "yes_ex": t4y,
        "no_html": t4n.format(prefer_rather_than=phrase_pick("prefer_rather_than", 1), soft_dislike=phrase_pick("soft_dislike", 2)),
        "no_vi": "Không thực sự. Tôi thích họp mặt nhỏ hơn tiệc lớn vì đám đông khá căng.",
        "no_plain": "No, not really. I prefer small gatherings rather than big parties because big groups can feel quite stressful.",
        "no_ex": t4n,
        "notes": [{"en": "keep in touch", "vi": "giữ liên lạc"}, {"en": "hardly ever + V", "vi": "hardly ever feel lonely"}],
    })
    t5y = (
        "Yes, I still do. We {keep_touch} and visiting them is always a special occasion."
    )
    t5n = (
        "Unfortunately my grandfather has passed away, but he still "
        "holds a special place in my heart. My maternal grandfather used to tell army stories."
    )
    items.append({
        "q": "Do you still have your grandparents? (ZIM / Mc)",
        "yes_html": t5y.format(keep_touch=phrase_pick("keep_touch", 1)),
        "yes_vi": "Vẫn còn. Chúng tôi giữ liên lạc với nhau và thăm họ luôn là dịp đặc biệt.",
        "yes_plain": "Yes, I still do. We keep in touch with each other and visiting them is always a special occasion.",
        "yes_ex": t5y,
        "no_html": t5n,
        "no_vi": "Rất tiếc ông tôi đã mất, nhưng ông vẫn giữ một vị trí đặc biệt trong tim. Ông ngoại từng kể chuyện quân ngũ (ZIM).",
        "no_plain": "Unfortunately my grandfather has passed away, but he still holds a special place in my heart. My maternal grandfather used to tell army stories.",
        "no_ex": t5n,
        "notes": [{"en": "passed away", "vi": "qua đời"}, {"en": "hold a special place in my heart", "vi": "giữ một vị trí đặc biệt trong tim"}],
    })
    t6n = (
        "No, not really. I hardly ever {hardly_ever_action} because I prefer "
        "{prefer_rather_than}."
    )
    t6y = (
        "Yes, occasionally — as long as we still {keep_touch} afterwards."
    )
    items.append({
        "q": "Do you like large family parties?",
        "yes_html": t6y.format(keep_touch=phrase_pick("keep_touch", 0)),
        "yes_vi": "Có, thỉnh thoảng — miễn là sau đó chúng tôi vẫn giữ liên lạc.",
        "yes_plain": "Yes, occasionally — as long as we still keep in touch afterwards.",
        "yes_ex": t6y,
        "no_html": t6n.format(hardly_ever_action=phrase_pick("hardly_ever_action", 1), prefer_rather_than=phrase_pick("prefer_rather_than", 1)),
        "no_vi": "Không thực sự. Tôi hiếm khi đi tiệc lớn vì thích họp mặt nhỏ hơn.",
        "no_plain": "No, not really. I hardly ever go to large family parties because I prefer small gatherings rather than big parties.",
        "no_ex": t6n,
        "notes": [{"en": "I hardly ever + V", "vi": "Hiếm khi + V"}, {"en": "keep in touch", "vi": "giữ liên lạc"}],
    })
    return _yes_no_cards(
        items,
        box_id="pf-examples-l3",
        subtitle="Ví dụ People & Family · Do you like X?",
        hint="Mỗi câu <strong>Thích / Không thích</strong> dùng đúng cụm Vocab notes Lesson 3. Sau các câu hỏi: đoạn văn nhớ + highlight.",
    )


def lesson5_examples_html() -> str:
    items = []
    t1 = (
        "Well, I love all kinds of friends, but if I had to choose one, it would have to be "
        "{kind_friend}. This is because I think {kind_why}. For example, my childhood friend "
        "is still close to me today because mutual trust is essential if you want to develop "
        "a long-lasting and meaningful connection."
    )
    items.append({
        "q": "What kind of people do you like to have as friends? (TAK12)",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất",
                "en": f'{_vmark("emotionally supportive")} và {_vmark("like-minded individuals")}',
            },
            {
                "title": "Lý do",
                "en": f'{_vmark("strengthen our bond")} và are the foundation to {_vmark("build a relationship")}',
            },
            {
                "title": "Ví dụ",
                "en": f'{_vmark("childhood friend")} is still close to me today. This is because '
                      f'{_vmark("mutual trust")} is essential if you want to develop a '
                      f'{_vmark("long-lasting / meaningful")} connection.',
            },
        ],
        "html": t1.format(kind_friend=phrase_pick("kind_friend", 0), kind_why=phrase_pick("kind_why", 0)),
        "vi": "Tôi thích mọi kiểu bạn, nhưng nếu phải chọn thì người hỗ trợ cảm xúc và cùng chí hướng. Vì sự hòa hợp và sở thích chung là nền tảng để xây mối quan hệ. Ví dụ, bạn thời thơ ấu đến nay vẫn thân vì tin tưởng lẫn nhau then chốt cho mối liên kết bền.",
        "plain": "Well, I love all kinds of friends, but if I had to choose one, it would have to be emotionally supportive and like-minded individuals. This is because I think compatibility and shared interests are the foundation whenever you want to build a relationship. For example, my childhood friend is still close to me today because mutual trust is essential if you want to develop a long-lasting and meaningful connection.",
        "ex": t1,
        "notes": [
            {"en": "if I had to choose… it would have to be", "vi": "nếu phải chọn… thì sẽ là"},
            {"en": "emotionally supportive", "vi": "hỗ trợ về cảm xúc"},
            {"en": "like-minded individuals", "vi": "người cùng chí hướng"},
            {"en": "build a relationship", "vi": "xây dựng mối quan hệ"},
        ],
    })
    t2 = (
        "Well, I look for all kinds of qualities, but if I had to choose, I would go for "
        "{kind_quality}. This is because mutual respect makes it much easier to live in "
        "harmony with somebody. For example, without mutual trust, suspicion develops."
    )
    items.append({
        "q": "What qualities do you look for in a romantic partner? (ZIM / Mc / ECE)",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất",
                "en": f'{_vmark("honesty")} và {_vmark("kindness")}',
            },
            {
                "title": "Lý do",
                "en": f'{_vmark("mutual respect")} · {_vmark("live in harmony with somebody")}',
            },
            {
                "title": "Ví dụ",
                "en": f'without {_vmark("mutual trust")}, suspicion develops',
            },
        ],
        "html": t2.format(kind_quality=phrase_pick("kind_quality", 0)),
        "vi": "Tôi tìm nhiều phẩm chất, nhưng nếu phải chọn thì trung thực và tử tế. Vì tôn trọng lẫn nhau giúp sống hòa hợp. Ví dụ, không có tin tưởng thì sinh nghi.",
        "plain": "Well, I look for all kinds of qualities, but if I had to choose, I would go for honesty and kindness. This is because mutual respect makes it much easier to live in harmony with somebody. For example, without mutual trust, suspicion develops.",
        "ex": t2,
        "notes": [
            {"en": "honesty · kindness", "vi": "trung thực · tử tế"},
            {"en": "live in harmony with somebody", "vi": "chung sống hòa hợp"},
            {"en": "mutual trust", "vi": "sự tin tưởng lẫn nhau"},
        ],
    })
    t3 = (
        "Well, I love all kinds of family activities, but if I had to choose one, "
        "it would have to be {kind_family_act}. This is because it {kind_reason}. "
        "For example, we catch up on each other's lives and it helps us strengthen our bond."
    )
    items.append({
        "q": "What kind of family activities do you like most?",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất / loại",
                "en": f'{_vmark("having dinner together")}',
            },
            {
                "title": "Lý do",
                "en": f'{_vmark("sense of belonging")} và {_vmark("strengthen our bond")}',
            },
            {
                "title": "Ví dụ",
                "en": "we catch up on each other's lives",
            },
        ],
        "html": t3.format(kind_family_act=phrase_pick("kind_family_act", 0), kind_reason=phrase_pick("kind_reason", 1)),
        "vi": "Tôi thích mọi hoạt động gia đình, nhưng nếu phải chọn thì ăn tối cùng nhau vì mang lại cảm giác thuộc về. Ví dụ, chúng tôi kể cho nhau nghe ngày hôm đó và gắn kết hơn.",
        "plain": "Well, I love all kinds of family activities, but if I had to choose one, it would have to be having dinner together. This is because it gives me a real sense of belonging. For example, we catch up on each other's lives and it helps us strengthen our bond.",
        "ex": t3,
        "notes": [
            {"en": "it would have to be", "vi": "thì sẽ phải là"},
            {"en": "sense of belonging", "vi": "cảm giác thuộc về"},
            {"en": "strengthen our bond", "vi": "gắn kết hơn"},
        ],
    })
    t4 = (
        "Well, I love all kinds of friends, but if I had to choose one, it would have to be "
        "{kind_friend}. This is because I think {kind_why}. For example, my childhood friend "
        "is still close to me today because mutual trust is essential if you want to develop "
        "a long-lasting and meaningful connection."
    )
    items.append({
        "q": "What kind of friends do you like most?",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất",
                "en": f'{_vmark("emotionally supportive")} và {_vmark("like-minded individuals")}',
            },
            {
                "title": "Lý do",
                "en": f'{_vmark("compatibility")} và {_vmark("shared interests")} are the foundation to {_vmark("build a relationship")}',
            },
            {
                "title": "Ví dụ",
                "en": f'{_vmark("childhood friend")} is still close to me today because {_vmark("mutual trust")} is essential for a {_vmark("long-lasting / meaningful")} connection.',
            },
        ],
        "html": t4.format(kind_friend=phrase_pick("kind_friend", 0), kind_why=phrase_pick("kind_why", 0)),
        "vi": "Tôi thích mọi kiểu bạn, nhưng nếu phải chọn thì người hỗ trợ cảm xúc và cùng chí hướng. Vì sự hòa hợp và sở thích chung là nền tảng để xây mối quan hệ. Ví dụ, bạn thời thơ ấu đến nay vẫn thân vì tin tưởng lẫn nhau.",
        "plain": "Well, I love all kinds of friends, but if I had to choose one, it would have to be emotionally supportive and like-minded individuals. This is because I think compatibility and shared interests are the foundation whenever you want to build a relationship. For example, my childhood friend is still close to me today because mutual trust is essential if you want to develop a long-lasting and meaningful connection.",
        "ex": t4,
        "notes": [
            {"en": "emotionally supportive", "vi": "hỗ trợ về cảm xúc"},
            {"en": "like-minded individuals", "vi": "người cùng chí hướng"},
            {"en": "childhood friend", "vi": "bạn thời thơ ấu"},
        ],
    })
    t5 = (
        "If I had to choose, I would go for {kind_quality}. This is because that lays "
        "the groundwork whenever you want to build a relationship. For example, without "
        "mutual trust, suspicion develops, so a long-lasting and meaningful connection is hard to keep."
    )
    items.append({
        "q": "What qualities are important in a good relationship? (ECE / TAK12)",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất",
                "en": f'{_vmark("mutual trust")} và {_vmark("mutual respect")}',
            },
            {
                "title": "Lý do",
                "en": f'lay the groundwork to {_vmark("build a relationship")} · {_vmark("long-lasting / meaningful")}',
            },
            {
                "title": "Ví dụ",
                "en": f'without {_vmark("mutual trust")}, suspicion develops',
            },
        ],
        "html": t5.format(kind_quality=phrase_pick("kind_quality", 1)),
        "vi": "Nếu phải chọn, tôi chọn tin tưởng và tôn trọng lẫn nhau. Vì đó đặt nền để xây mối quan hệ. Ví dụ, không tin tưởng thì sinh nghi, khó giữ mối liên kết bền.",
        "plain": "If I had to choose, I would go for mutual trust and respect. This is because that lays the groundwork whenever you want to build a relationship. For example, without mutual trust, suspicion develops, so a long-lasting and meaningful connection is hard to keep.",
        "ex": t5,
        "notes": [
            {"en": "lay the groundwork for", "vi": "đặt nền tảng cho"},
            {"en": "build a relationship", "vi": "xây dựng mối quan hệ"},
            {"en": "long-lasting / meaningful", "vi": "bền vững / ý nghĩa"},
        ],
    })
    t6 = (
        "Well, I get on with all kinds of relatives, but if I had to choose one, "
        "I would opt for my {family_type}. This is because we live in harmony with each other "
        "and it gives me a real sense of belonging. For example, we still have dinner together "
        "most evenings — people even say we are {family_idiom}."
    )
    items.append({
        "q": "What kind of family do you come from?",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất / loại",
                "en": f'{_vmark("close-knit family")}',
            },
            {
                "title": "Lý do",
                "en": f'{_vmark("live in harmony with somebody")} và {_vmark("sense of belonging")}',
            },
            {
                "title": "Ví dụ",
                "en": f'we still have dinner together · {_vmark("like two peas in a pod")}',
            },
        ],
        "html": t6.format(family_type=phrase_pick("family_type", 0), family_idiom=phrase_pick("family_idiom", 1)),
        "vi": "Tôi hòa hợp với mọi họ hàng, nhưng nếu phải chọn thì gia đình gắn bó. Vì chúng tôi sống hòa hợp và có cảm giác thuộc về. Ví dụ, tối nào cũng ăn cùng nhau — người ta còn nói giống nhau như đúc.",
        "plain": "Well, I get on with all kinds of relatives, but if I had to choose one, I would opt for my close-knit family. This is because we live in harmony with each other and it gives me a real sense of belonging. For example, we still have dinner together most evenings — people even say we are like two peas in a pod.",
        "ex": t6,
        "notes": [
            {"en": "close-knit family", "vi": "gia đình gắn bó"},
            {"en": "live in harmony with somebody", "vi": "chung sống hòa hợp"},
            {"en": "like two peas in a pod", "vi": "giống nhau như đúc"},
        ],
    })
    t7 = (
        "I find myself attracted to {attracted_to}. This is because it makes it much easier "
        "to live in harmony with somebody. For example, my childhood friend is still close "
        "to me today because mutual trust is essential if you want to develop a long-lasting "
        "and meaningful connection."
    )
    items.append({
        "q": "What kind of people do you like to have as friends? (TAK12 · attracted to)",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất",
                "en": f'{_vmark("honesty")} · {_vmark("loyalty")} và {_vmark("mutual respect")}',
            },
            {
                "title": "Lý do",
                "en": f'{_vmark("attracted to")} · {_vmark("live in harmony with somebody")}',
            },
            {
                "title": "Ví dụ",
                "en": f'{_vmark("childhood friend")} is still close to me today because {_vmark("mutual trust")} is essential for a {_vmark("long-lasting / meaningful")} connection.',
            },
        ],
        "html": t7.format(attracted_to=phrase_pick("attracted_to", 0)),
        "vi": "Tôi bị thu hút bởi người thành thật và biết cư xử. Vì như thế dễ sống hòa hợp. Ví dụ, bạn thời thơ ấu đến nay vẫn thân vì tin tưởng lẫn nhau then chốt cho mối liên kết bền.",
        "plain": "I find myself attracted to people who are honest and who know how to behave with others. This is because it makes it much easier to live in harmony with somebody. For example, my childhood friend is still close to me today because mutual trust is essential if you want to develop a long-lasting and meaningful connection.",
        "ex": t7,
        "notes": [
            {"en": "attracted to", "vi": "bị thu hút (TAK12)"},
            {"en": "loyalty · mutual respect", "vi": "trung thành · tôn trọng lẫn nhau"},
            {"en": "childhood friend", "vi": "bạn thời thơ ấu"},
        ],
    })
    t8 = (
        "If I had to choose, I would go for {kind_quality}. This is because that helps me "
        "build a relationship that feels {relation_adj}. For example, my childhood friend "
        "is still close to me today because mutual trust is essential for a long-lasting "
        "and meaningful connection."
    )
    items.append({
        "q": "What kind of relationship do you value most?",
        "think": [
            {
                "title": "Chọn 1–2 phẩm chất",
                "en": f'{_vmark("loyalty")} và {_vmark("mutual respect")}',
            },
            {
                "title": "Lý do",
                "en": f'{_vmark("build a relationship")} that feels {_vmark("long-lasting / meaningful")}',
            },
            {
                "title": "Ví dụ",
                "en": f'{_vmark("childhood friend")} is still close to me today because {_vmark("mutual trust")} is essential.',
            },
        ],
        "html": t8.format(kind_quality=phrase_pick("kind_quality", 4), relation_adj=phrase_pick("relation_adj", 1)),
        "vi": "Nếu phải chọn, tôi chọn lòng trung thành và tôn trọng lẫn nhau. Vì điều đó giúp xây mối quan hệ bền vững, ý nghĩa. Ví dụ, bạn thời thơ ấu đến nay vẫn thân vì tin tưởng lẫn nhau.",
        "plain": "If I had to choose, I would go for loyalty and mutual respect. This is because that helps me build a relationship that feels meaningful and long-lasting. For example, my childhood friend is still close to me today because mutual trust is essential for a long-lasting and meaningful connection.",
        "ex": t8,
        "notes": [
            {"en": "build a relationship", "vi": "xây dựng mối quan hệ"},
            {"en": "long-lasting · meaningful", "vi": "bền vững · ý nghĩa"},
            {"en": "mutual trust", "vi": "sự tin tưởng lẫn nhau"},
        ],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l5",
        subtitle="Ví dụ People & Family · What kind of X?",
        hint="3 bước từ đoạn văn nhớ: <strong>1</strong> chọn 1–2 phẩm chất · "
             "<strong>2</strong> lý do · <strong>3</strong> ví dụ. "
             "Cùng kho cụm, đổi X = friends / partner / family / activities.",
    )


def lesson6_examples_html() -> str:
    items = []
    t1 = (
        "Well, I love both, but I {prefer_x} to {prefer_y}. This is because family "
        "gives me comfort and security, while a big crowd can feel superficial."
    )
    # prefer_x/y are V-ing/NP already in slots - "I prefer X to Y"
    t1 = (
        "Well, I love both, but I prefer {prefer_x} to {prefer_y}. This is because family "
        "gives me comfort and security, while a big crowd can feel superficial."
    )
    items.append({
        "q": "Do you prefer spending time with family or with friends? (ZIM / ECE / Mc)",
        "html": t1.format(prefer_x=phrase_pick("prefer_x", 0), prefer_y=phrase_pick("prefer_y", 0)),
        "vi": "Tôi thích cả hai, nhưng thích ở với gia đình hơn đi chơi với đám đông vì gia đình cho sự an ủi, còn đám đông đôi khi hời hợt.",
        "plain": "Well, I love both, but I prefer spending time with my family to going out with a big crowd. This is because family gives me comfort and security, while a big crowd can feel superficial.",
        "ex": t1,
        "alt_html": (
            "As a young adult I lean more towards my friends when I want to explore. "
            "However, I always make sure to spend quality time with my family."
        ),
        "alt_vi": "Khi còn trẻ tôi hơi nghiêng về bạn khi muốn khám phá. Nhưng tôi vẫn dành thời gian chất lượng cho gia đình (ZIM).",
        "alt_plain": "As a young adult I lean more towards my friends when I want to explore. However, I always make sure to spend quality time with my family.",
        "alt_kind": "depends",
        "notes": [{"en": "prefer X to Y", "vi": "thích X hơn Y"}, {"en": "lean towards", "vi": "nghiêng về (ZIM)"}],
    })
    t2 = (
        "I prefer {prefer_x} rather than {prefer_y}. I love the feeling of having "
        "someone to confide in, whereas staying alone too long can lead to loneliness."
    )
    items.append({
        "q": "Which do you prefer — spending time with a friend or alone? (TAK12)",
        "html": t2.format(prefer_x=phrase_pick("prefer_x", 1), prefer_y=phrase_pick("prefer_y", 1)),
        "vi": "Tôi thích đi chơi với bạn thân hơn ở một mình cả cuối tuần. Tôi thích có người tâm sự, còn ở một mình lâu dễ cô đơn.",
        "plain": "I prefer hanging out with close friends rather than staying alone all weekend. I love the feeling of having someone to confide in, whereas staying alone too long can lead to loneliness.",
        "ex": t2,
        "notes": [{"en": "prefer X rather than Y", "vi": "thích X hơn là Y"}, {"en": "confide in", "vi": "tâm sự"}],
    })
    t3 = (
        "I prefer {prefer_x} to {prefer_y}. Face-to-face talks hold a special place "
        "in my heart, while endless texting can feel distant."
    )
    items.append({
        "q": "Do you prefer talking face to face or chatting online? (WESET)",
        "html": t3.format(prefer_x=phrase_pick("prefer_x", 3), prefer_y=phrase_pick("prefer_y", 2)),
        "vi": "Tôi thích nói chuyện trực tiếp hơn giữ mọi thứ trên mạng. Gặp mặt giữ chỗ đặc biệt, còn nhắn tin mãi thì xa cách.",
        "plain": "I prefer talking face to face to keeping everything online. Face-to-face talks hold a special place in my heart, while endless texting can feel distant.",
        "ex": t3,
        "notes": [{"en": "hold a special place", "vi": "giữ vị trí đặc biệt"}, {"en": "face-to-face", "vi": "trực tiếp"}],
    })
    t4 = (
        "It depends on the situation. If I want to chill, I prefer {prefer_x}. "
        "But if I need comfort, I prefer my family because they understand me better."
    )
    items.append({
        "q": "Who are you closest to — family or friends?",
        "html": t4.format(prefer_x=phrase_pick("prefer_x", 1)),
        "vi": "Tùy tình huống. Muốn thư giãn thì bạn; cần an ủi thì gia đình vì họ hiểu tôi hơn (ECE).",
        "plain": "It depends on the situation. If I want to chill, I prefer hanging out with close friends. But if I need comfort, I prefer my family because they understand me better.",
        "ex": t4,
        "kind": "depends",
        "notes": [{"en": "It depends on the situation", "vi": "còn tùy tình huống"}],
    })
    t5 = (
        "Most of my friends are around my age. I prefer {prefer_x} to making small talk "
        "with acquaintances, although I do {relationship_v} a few older colleagues."
    )
    items.append({
        "q": "Are your friends mostly your age or different ages? (TAK12)",
        "html": t5.format(prefer_x=phrase_pick("prefer_x", 2), relationship_v=phrase_pick("relationship_v", 0)),
        "vi": "Hầu hết bạn tôi cùng tuổi. Tôi thích nhóm nhỏ hơn chuyện xã giao, dù vẫn hòa thuận với vài đồng nghiệp lớn tuổi.",
        "plain": "Most of my friends are around my age. I prefer being with a small group to making small talk with acquaintances, although I do get on well with a few older colleagues.",
        "ex": t5,
        "notes": [{"en": "acquaintance", "vi": "người quen (ECE)"}],
    })
    t6 = (
        "I prefer hanging out with {relation_type} to making small talk with an acquaintance. "
        "A roommate or classmate can become a companion if we live in harmony with each other."
    )
    items.append({
        "q": "Do you prefer close friends or acquaintances? (ECE relation types)",
        "html": t6.format(relation_type=phrase_pick("relation_type", 0)),
        "vi": "Tôi thích đi với bạn thân hơn chuyện xã giao với người quen. Bạn cùng phòng hoặc bạn cùng lớp có thể thành người đồng hành nếu sống hòa hợp.",
        "plain": "I prefer hanging out with a close friend to making small talk with an acquaintance. A roommate or classmate can become a companion if we live in harmony with each other.",
        "ex": t6,
        "notes": [
            {"en": "roommate · classmate · companion", "vi": "bạn cùng phòng · bạn cùng lớp · người đồng hành (ECE)"},
            {"en": "live in harmony with somebody", "vi": "chung sống hòa hợp (TAK12)"},
        ],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l6",
        subtitle="Ví dụ People & Family · Prefer X or Y?",
        hint="prefer X to Y / rather than / lean towards. ECE types: roommate, classmate, companion.",
    )


def lesson7_examples_html() -> str:
    items = []
    t1 = (
        "Yes, it's very popular. The majority of families still {pop_custom}. "
        "You can see three generations living under the same roof, especially in the countryside."
    )
    items.append({
        "q": "Is family very important in your country?",
        "html": t1.format(pop_custom=phrase_pick("pop_custom", 0)),
        "vi": "Có, rất phổ biến. Đa số gia đình vẫn tôn trọng người lớn và xin lời khuyên. Ở quê vẫn thấy ba thế hệ chung một mái nhà.",
        "plain": "Yes, it's very popular. The majority of families still honouring elders and seeking their advice. You can see three generations living under the same roof, especially in the countryside.",
        "ex": t1,
        "kind": "pop_yes",
        "notes": [{"en": "live under the same roof", "vi": "sống chung một mái nhà"}, {"en": "the majority of", "vi": "đa số"}],
    })
    t2 = (
        "It depends. In collectivist families, {pop_group} still value extended kinship. "
        "But in major cities, an increasing number of people live in nuclear households."
    )
    items.append({
        "q": "Are there traditional customs related to relationships in your culture? (WESET)",
        "html": t2.format(pop_group=phrase_pick("pop_group", 1)),
        "vi": "Còn tùy. Gia đình theo chủ nghĩa tập thể, người lớn tuổi vẫn coi trọng họ hàng rộng. Nhưng ở thành phố ngày càng nhiều hộ hạt nhân.",
        "plain": "It depends. In collectivist families, older people still value extended kinship. But in major cities, an increasing number of people live in nuclear households.",
        "ex": t2,
        "kind": "depends",
        "notes": [{"en": "collectivist", "vi": "theo chủ nghĩa tập thể (DOL)"}, {"en": "nuclear households", "vi": "hộ gia đình hạt nhân"}],
    })
    t3 = (
        "Yes, especially in crowded cities. A fast-paced lifestyle can lead to loneliness "
        "even when {pop_group} are surrounded by people."
    )
    items.append({
        "q": "Do people feel lonely in crowded cities? (DOL Part 3)",
        "html": t3.format(pop_group=phrase_pick("pop_group", 2)),
        "vi": "Có, nhất là thành phố đông. Lối sống vội vã có thể dẫn đến cô đơn dù người thành thị bị bao quanh bởi mọi người.",
        "plain": "Yes, especially in crowded cities. A fast-paced lifestyle can lead to loneliness even when urban dwellers are surrounded by people.",
        "ex": t3,
        "kind": "pop_yes",
        "notes": [{"en": "fast-paced lifestyle", "vi": "lối sống vội vã (DOL)"}, {"en": "can lead to …", "vi": "có thể dẫn đến"}],
    })
    t4 = (
        "No, not really — at least not every day. Very few young couples still "
        "{pop_custom}. It used to account for a large percentage, but rarely now."
    )
    items.append({
        "q": "Is arranged marriage still popular in your country?",
        "html": t4.format(pop_custom=phrase_pick("pop_custom", 2)),
        "vi": "Không thực sự — ít nhất không phải mỗi ngày. Rất ít cặp trẻ vẫn hôn nhân sắp đặt. Trước chiếm tỷ lệ lớn, nay hiếm.",
        "plain": "No, not really — at least not every day. Very few young couples still arranging marriages based on family values. It used to account for a large percentage, but rarely now.",
        "ex": t4,
        "kind": "pop_no",
        "notes": [{"en": "account for + %", "vi": "chiếm bao nhiêu %"}, {"en": "hardly ever / rarely", "vi": "hiếm khi"}],
    })
    t5 = (
        "It depends on the generation. {pop_group} are more individualist, "
        "whereas older people still prefer patriarchal or at least family-led decisions."
    )
    items.append({
        "q": "How does society influence a person's personality? (DOL)",
        "html": t5.format(pop_group=phrase_pick("pop_group", 0)),
        "vi": "Còn tùy thế hệ. Thế hệ trẻ cá nhân hơn, còn người lớn tuổi vẫn thích quyết định theo gia đình / gia trưởng.",
        "plain": "It depends on the generation. the younger generation are more individualist, whereas older people still prefer patriarchal or at least family-led decisions.",
        "ex": t5,
        "kind": "depends",
        "notes": [{"en": "individualist", "vi": "theo chủ nghĩa cá nhân (DOL)"}, {"en": "patriarchal", "vi": "gia trưởng (ZIM)"}],
    })
    t6 = (
        "Generally speaking, yes. Most people still {pop_custom}. "
        "However, urban dwellers can hardly ever visit every relative."
    )
    items.append({
        "q": "Do people in your country still live with their grandparents?",
        "html": t6.format(pop_custom=phrase_pick("pop_custom", 1)),
        "vi": "Nói chung có. Hầu hết vẫn sống chung đại gia đình. Nhưng người thành thị hiếm khi thăm hết họ hàng.",
        "plain": "Generally speaking, yes. Most people still living with extended family under one roof. However, urban dwellers can hardly ever visit every relative.",
        "ex": t6,
        "kind": "pop_yes",
        "notes": [{"en": "generally speaking", "vi": "nói chung"}],
    })
    t7 = (
        "It depends on the family. Some people still feel {fighter_family} even from abroad. "
        "A few households are matriarchal, while others stay patriarchal. Disowning a child is rare, but it does happen after a serious scandal."
    )
    items.append({
        "q": "Do family lineage and kinship still matter in your country? (IELTS-Fighter)",
        "html": t7.format(fighter_family=phrase_pick("fighter_family", 0)),
        "vi": "Còn tùy gia đình. Có người vẫn cảm thấy mối họ hàng sâu dù ở nước ngoài. Một số hộ gia mẫu, số khác vẫn gia trưởng. Từ bỏ con cái hiếm, nhưng vẫn xảy ra sau scandal.",
        "plain": "It depends on the family. Some people still feel a deep sense of kinship even from abroad. A few households are matriarchal, while others stay patriarchal. Disowning a child is rare, but it does happen after a serious scandal.",
        "ex": t7,
        "kind": "depends",
        "notes": [
            {"en": "kinship · lineage · descendant", "vi": "họ hàng · dòng dõi · hậu duệ"},
            {"en": "matriarchal · patriarchal · disown", "vi": "gia mẫu · gia trưởng · từ bỏ (IELTS-Fighter)"},
        ],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l7",
        subtitle="Ví dụ People & Family · Is X popular?",
        hint="Có / Không / Còn tùy. DOL lonely cities + IELTS-Fighter kinship / lineage / disown.",
    )


def lesson8_examples_html() -> str:
    items = []
    t1 = (
        "{best_time} is the best time to spend with family. This is because nobody "
        "is rushing, so we can catch up on each other's day."
    )
    items.append({
        "q": "What is the best time to spend with your family?",
        "html": t1.format(best_time=phrase_pick("best_time", 0)),
        "vi": "Bữa trưa Chủ nhật là lúc tốt nhất. Không ai vội nên chúng tôi kể cho nhau nghe ngày hôm đó.",
        "plain": "Sunday lunch is the best time to spend with family. This is because nobody is rushing, so we can catch up on each other's day.",
        "ex": t1,
        "notes": [{"en": "catch up on each other's day", "vi": "cập nhật ngày của nhau (ZIM)"}],
    })
    t2 = (
        "{best_time} is my favourite time to meet friends. I find myself most relaxed "
        "then. However, generally speaking, any evening is fine as long as we talk face to face."
    )
    items.append({
        "q": "What is the best time to meet your friends?",
        "html": t2.format(best_time=phrase_pick("best_time", 4)),
        "vi": "Sáng cuối tuần là lúc tôi thích gặp bạn nhất — lúc đó tôi thấy thư thái. Nói chung tối nào cũng được miễn là nói chuyện trực tiếp.",
        "plain": "weekend mornings is my favourite time to meet friends. I find myself most relaxed then. However, generally speaking, any evening is fine as long as we talk face to face.",
        "ex": t2,
        "notes": [{"en": "find + myself + adj", "vi": "thấy bản thân như thế nào"}, {"en": "as long as", "vi": "miễn là"}],
    })
    t3 = (
        "It depends. For me, {best_time} is ideal because it lasts several days "
        "and relatives come from everywhere. However, some people prefer a quiet Sunday."
    )
    items.append({
        "q": "When is the best time for a family reunion?",
        "html": t3.format(best_time=phrase_pick("best_time", 2)),
        "vi": "Còn tùy. Với tôi Tết lý tưởng vì kéo dài vài ngày và họ hàng về từ khắp nơi. Nhưng có người thích Chủ nhật yên.",
        "plain": "It depends. For me, the Tet holiday is ideal because it lasts several days and relatives come from everywhere. However, some people prefer a quiet Sunday.",
        "ex": t3,
        "kind": "depends",
        "notes": [{"en": "last (v) + thời gian", "vi": "kéo dài bao lâu"}, {"en": "celebrate milestones", "vi": "kỷ niệm các mốc (WESET)"}],
    })
    t4 = (
        "{best_time} is the perfect time to call my parents. After work I am tired, "
        "but a short call still makes it easier to stay connected."
    )
    items.append({
        "q": "What is the best time to call your parents?",
        "html": t4.format(best_time=phrase_pick("best_time", 3)),
        "vi": "Tối sau giờ làm là lúc hoàn hảo để gọi bố mẹ. Dù mệt, một cuộc gọi ngắn vẫn giúp giữ liên lạc.",
        "plain": "quiet evenings after work is the perfect time to call my parents. After work I am tired, but a short call still makes it easier to stay connected.",
        "ex": t4,
        "notes": [{"en": "make it + adj + to V", "vi": "khiến việc … trở nên adj"}],
    })
    t5 = (
        "Weekday dinners are the best time if everyone lives under the same roof. "
        "On weekends I lean more towards friends, as long as Sunday lunch stays family time."
    )
    items.append({
        "q": "Is evening the best time for family meals?",
        "html": t5,
        "vi": "Bữa tối ngày thường tốt nhất nếu sống chung. Cuối tuần tôi nghiêng về bạn, miễn là trưa Chủ nhật vẫn là giờ gia đình.",
        "plain": "Weekday dinners are the best time if everyone lives under the same roof. On weekends I lean more towards friends, as long as Sunday lunch stays family time.",
        "ex": t5,
        "notes": [{"en": "live under the same roof", "vi": "sống chung một mái nhà"}],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l8",
        subtitle="Ví dụ People & Family · Best time?",
        hint="Thời điểm tốt nhất / Còn tùy. catch up on · Tet · quality time.",
    )


def lesson9_examples_html() -> str:
    items = []
    t1 = (
        "As far as I can remember, the last time I saw my extended family was {time_anchor}. "
        "We spent a whole afternoon catching up on old memories."
    )
    items.append({
        "q": "When was the last time you saw your extended family?",
        "html": t1.format(time_anchor=phrase_pick("time_anchor", 1)),
        "vi": "Theo tôi nhớ, lần gần nhất gặp đại gia đình là Tết vừa rồi. Chúng tôi dành cả buổi chiều ôn kỷ niệm.",
        "plain": "As far as I can remember, the last time I saw my extended family was just last Tet. We spent a whole afternoon catching up on old memories.",
        "ex": t1,
        "kind": "clear",
        "notes": [{"en": "As far as I can remember", "vi": "theo như tôi còn nhớ"}, {"en": "it's been … since", "vi": "đã … kể từ"}],
    })
    t2 = (
        "I can't remember exactly, but I guess I last got in contact with an old friend "
        "{time_anchor}. I sent a friend request and we started calling again."
    )
    items.append({
        "q": "When was the last time you got in contact with an old friend? (TAK12)",
        "html": t2.format(time_anchor=phrase_pick("time_anchor", 3)),
        "vi": "Không nhớ chính xác, nhưng đoán là trong đại dịch. Tôi gửi lời mời kết bạn rồi chúng tôi gọi lại.",
        "plain": "I can't remember exactly, but I guess I last got in contact with an old friend during the pandemic. I sent a friend request and we started calling again.",
        "ex": t2,
        "kind": "guess",
        "notes": [{"en": "get in contact / lose contact", "vi": "liên lạc lại / mất liên lạc"}, {"en": "a friend request", "vi": "lời mời kết bạn"}],
    })
    t3 = (
        "It's been years since we last spoke, but we reconciled {time_anchor}. "
        "I felt thrilled because I had missed her a lot."
    )
    items.append({
        "q": "When was the first time you reconciled with someone? (ZIM vocab)",
        "html": t3.format(time_anchor=phrase_pick("time_anchor", 0)),
        "vi": "Đã nhiều năm không nói chuyện, nhưng chúng tôi hàn gắn khoảng hai năm trước. Tôi vui sướng vì nhớ cô ấy nhiều.",
        "plain": "It's been years since we last spoke, but we reconciled about two years ago. I felt thrilled because I had missed her a lot.",
        "ex": t3,
        "kind": "clear",
        "notes": [{"en": "reconcile", "vi": "hàn gắn, giải hòa (ZIM)"}, {"en": "it's been … since", "vi": "đã … kể từ"}],
    })
    t4 = (
        "I'm not really sure but I guess the first time I lived away from my parents "
        "was {time_anchor}. Coming home still holds a special place in my heart."
    )
    items.append({
        "q": "When was the first time you lived away from your family?",
        "html": t4.format(time_anchor=phrase_pick("time_anchor", 2)),
        "vi": "Không chắc lắm nhưng đoán là khi học cấp 3. Về nhà vẫn giữ chỗ đặc biệt trong tim.",
        "plain": "I'm not really sure but I guess the first time I lived away from my parents was when I was in high school. Coming home still holds a special place in my heart.",
        "ex": t4,
        "kind": "guess",
        "notes": [{"en": "hold a special place", "vi": "giữ vị trí đặc biệt"}],
    })
    t5 = (
        "Just last month. A cousin came over to celebrate a milestone, and we had "
        "a great time together."
    )
    items.append({
        "q": "When was the last time you had a family gathering?",
        "html": t5,
        "vi": "Tháng trước thôi. Một người anh em họ đến nhà kỷ niệm một mốc, chúng tôi vui vẻ.",
        "plain": "Just last month. A cousin came over to celebrate a milestone, and we had a great time together.",
        "ex": t5,
        "kind": "clear",
        "notes": [{"en": "come over to + V", "vi": "đến nhà để làm gì"}, {"en": "celebrate milestones", "vi": "kỷ niệm các mốc"}],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l9",
        subtitle="Ví dụ People & Family · First / last time?",
        hint="Nhớ rõ / Đoán. TAK12 get in contact · ZIM reconcile.",
    )


def lesson10_examples_html() -> str:
    items = []
    t1 = (
        "Yes, I did. When I was a kid I used to {child_detail}. "
        "Those family ties were instilled in me from a young age."
    )
    items.append({
        "q": "Did you spend a lot of time with your family when you were a child? (WESET)",
        "html": t1.format(child_detail=phrase_pick("child_detail", 3)),
        "vi": "Có. Khi còn nhỏ tôi thường tối nào cũng ở chung một mái nhà. Những mối quan hệ đó được thấm nhuần từ nhỏ.",
        "plain": "Yes, I did. When I was a kid I used to spend most evenings under the same roof. Those family ties were instilled in me from a young age.",
        "ex": t1,
        "kind": "yes",
        "alt_html": (
            "No, not really. I spent most of my time studying. I did see my cousins "
            "sometimes but not too often."
        ),
        "alt_vi": "Không thật sự. Tôi dành phần lớn thời gian học. Tôi có gặp anh em họ nhưng không thường.",
        "alt_plain": "No, not really. I spent most of my time studying. I did see my cousins sometimes but not too often.",
        "alt_kind": "no",
        "notes": [{"en": "instilled", "vi": "được thấm nhuần (ZIM)"}, {"en": "did + V (emphasis)", "vi": "nhấn mạnh quá khứ"}],
    })
    t2 = (
        "Yes. When I was in primary school I used to {child_detail}. "
        "People still say {family_idiom}."
    )
    items.append({
        "q": "Did you take after anyone in your family as a child?",
        "html": t2.format(child_detail=phrase_pick("child_detail", 2), family_idiom=phrase_pick("family_idiom", 3)),
        "vi": "Có. Khi học tiểu học tôi đã giống bố. Người ta vẫn nói cha nào con nấy.",
        "plain": "Yes. When I was in primary school I used to take after my dad. People still say like father, like son.",
        "ex": t2,
        "kind": "yes",
        "notes": [{"en": "take after", "vi": "giống người thân"}, {"en": "like father, like son", "vi": "cha nào con nấy"}],
    })
    t3 = (
        "Yes, I did. My mum encouraged me to {child_detail}. "
        "She also used to help me with homework after dinner."
    )
    items.append({
        "q": "Did your parents encourage you when you were a child?",
        "html": t3.format(child_detail=phrase_pick("child_detail", 1)),
        "vi": "Có. Mẹ khuyến khích tôi ngưỡng mộ anh trai. Bà cũng giúp tôi bài tập sau bữa tối.",
        "plain": "Yes, I did. My mum encouraged me to look up to my older brother. She also used to help me with homework after dinner.",
        "ex": t3,
        "kind": "yes",
        "notes": [{"en": "encourage sb to + V", "vi": "khuyến khích ai làm gì"}, {"en": "look up to", "vi": "ngưỡng mộ"}],
    })
    t4 = (
        "No, not really. I was not really interested in big reunions. "
        "I found them quite noisy, so I stayed with my immediate family."
    )
    items.append({
        "q": "Did you enjoy family reunions when you were a child?",
        "html": t4,
        "vi": "Không thật sự. Tôi không thích họp mặt lớn — thấy ồn — nên chỉ ở với gia đình gần.",
        "plain": "No, not really. I was not really interested in big reunions. I found them quite noisy, so I stayed with my immediate family.",
        "ex": t4,
        "kind": "no",
        "notes": [{"en": "find + sth + adj", "vi": "thấy cái gì như thế nào"}, {"en": "immediate family", "vi": "gia đình gần"}],
    })
    t5 = (
        "Yes. When I was little my parents passed down traditional values. "
        "My upbringing still shapes how I treat people with respect."
    )
    items.append({
        "q": "Did your family teach you traditional values as a child?",
        "html": t5,
        "vi": "Có. Khi còn nhỏ bố mẹ truyền giá trị truyền thống. Cách nuôi dưỡng vẫn định hình cách tôi tôn trọng người khác.",
        "plain": "Yes. When I was little my parents passed down traditional values. My upbringing still shapes how I treat people with respect.",
        "ex": t5,
        "kind": "yes",
        "notes": [{"en": "pass down traditional values", "vi": "truyền giá trị truyền thống"}, {"en": "upbringing", "vi": "sự nuôi dưỡng"}],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l10",
        subtitle="Ví dụ People & Family · When you were a child?",
        hint="Yes, I did / No, not really + childhood time. take after · instilled · upbringing.",
    )


def lesson11_examples_html() -> str:
    items = []
    t1 = (
        "Yes, I think so — as long as {suit_case}. Physical distance is hard, "
        "but emotional closeness can still be maintained through video calls."
    )
    items.append({
        "q": "Do you think long-distance relationships can be successful? (WESET / Mc)",
        "html": t1.format(suit_case=phrase_pick("suit_case", 0)),
        "vi": "Tôi nghĩ có — miễn là cả hai giao tiếp cởi mở. Xa về địa lý khó, nhưng gần về cảm xúc vẫn giữ được nhờ video call.",
        "plain": "Yes, I think so — as long as both people communicate openly. Physical distance is hard, but emotional closeness can still be maintained through video calls.",
        "ex": t1,
        "kind": "yes",
        "notes": [{"en": "long-distance relationship", "vi": "mối quan hệ yêu xa"}, {"en": "as long as", "vi": "miễn là"}],
    })
    t2 = (
        "I'm a bit skeptical. Instant attraction can happen, but true love needs "
        "commitment. Love at first sight is more physical attraction than a meaningful bond."
    )
    items.append({
        "q": "Do you believe in love at first sight? (ZIM / Mc)",
        "html": t2,
        "vi": "Tôi hơi hoài nghi. Có thể bị thu hút ngay, nhưng tình yêu thật cần cam kết. Tình yêu sét đánh nghiêng về hấp dẫn thể xác hơn gắn kết cảm xúc.",
        "plain": "I'm a bit skeptical. Instant attraction can happen, but true love needs commitment. Love at first sight is more physical attraction than a meaningful bond.",
        "ex": t2,
        "kind": "no",
        "notes": [{"en": "skeptical", "vi": "hoài nghi"}, {"en": "deal-breaker", "vi": "điều chấm dứt quan hệ"}],
    })
    t3 = (
        "No, I don't think it's a good idea. Money can become a deal-breaker; "
        "that's the reason why I try not to mix friendship with loans."
    )
    items.append({
        "q": "Is it a good idea to borrow money from a friend? (TAK12)",
        "html": t3,
        "vi": "Tôi không nghĩ vậy. Tiền có thể thành điều chấm dứt quan hệ; vì thế tôi cố không trộn tình bạn với nợ.",
        "plain": "No, I don't think it's a good idea. Money can become a deal-breaker; that's the reason why I try not to mix friendship with loans.",
        "ex": t3,
        "kind": "no",
        "notes": [{"en": "that's the reason why", "vi": "đó là lý do tại sao"}, {"en": "deal-breaker", "vi": "điều chấm dứt quan hệ (ZIM)"}],
    })
    t4 = (
        "It depends. If {suit_case}, then I would say yes. "
        "But if it is mainly for showing off online, then it is not really suitable."
    )
    items.append({
        "q": "Is social media suitable for romantic relationships? (WESET / Mc)",
        "html": t4.format(suit_case=phrase_pick("suit_case", 1)),
        "vi": "Còn tùy. Nếu có tin tưởng lẫn nhau thì được. Nhưng nếu chủ yếu để khoe trên mạng thì không phù hợp.",
        "plain": "It depends. If there is mutual trust, then I would say yes. But if it is mainly for showing off online, then it is not really suitable.",
        "ex": t4,
        "kind": "depends",
        "notes": [{"en": "If … then … / But if …", "vi": "Nếu … thì … / Nhưng nếu …"}],
    })
    t5 = (
        "Not really. Clothing can hint at style, but it doesn't tell the full story "
        "of a person's personality. Plus, people dress for work, not for who they are."
    )
    items.append({
        "q": "Can clothing tell and reveal a person's personality? (DOL)",
        "html": t5,
        "vi": "Không thật sự. Quần áo gợi ý phong cách nhưng không cho thấy tất cả tính cách. Hơn nữa người ta mặc vì việc, không phải vì con người thật.",
        "plain": "Not really. Clothing can hint at style, but it doesn't tell the full story of a person's personality. Plus, people dress for work, not for who they are.",
        "ex": t5,
        "kind": "no",
        "notes": [{"en": "tell the full story", "vi": "cho thấy tất cả (DOL)"}, {"en": "Plus / Moreover", "vi": "thêm vào đó"}],
    })
    t6 = (
        "Yes, it would be a great idea if both partners are mature enough to "
        "adapt and compromise. Shared interests help, but they are not a deal-breaker."
    )
    items.append({
        "q": "Is it important to have similar interests with your partner? (ZIM / Mc)",
        "html": t6,
        "vi": "Đó sẽ là ý hay nếu cả hai đủ trưởng thành để thích nghi và thỏa hiệp. Sở thích chung hữu ích nhưng không phải điều chấm dứt quan hệ.",
        "plain": "Yes, it would be a great idea if both partners are mature enough to adapt and compromise. Shared interests help, but they are not a deal-breaker.",
        "ex": t6,
        "kind": "yes",
        "notes": [{"en": "adj + enough + to V", "vi": "đủ … để …"}, {"en": "adapt and compromise", "vi": "thích nghi và thỏa hiệp (WESET)"}],
    })
    t7 = (
        "It depends. {romance_lex} can start a relationship, but without commitment "
        "and compatibility it will not stay harmonious. Affection matters more than a brief attraction."
    )
    items.append({
        "q": "Is chemistry enough for a long-term relationship? (IELTS-Fighter romance)",
        "html": t7.format(romance_lex=phrase_pick("romance_lex", 1)),
        "vi": "Còn tùy. Chemistry có thể khởi đầu, nhưng thiếu cam kết và sự hòa hợp thì không giữ được hòa hợp. Tình cảm quan trọng hơn sự thu hút thoáng qua.",
        "plain": "It depends. chemistry can start a relationship, but without commitment and compatibility it will not stay harmonious. Affection matters more than a brief attraction.",
        "ex": t7,
        "kind": "depends",
        "notes": [
            {"en": "chemistry · affection · attraction", "vi": "hóa học tình cảm · tình cảm · sự thu hút (Fighter)"},
            {"en": "harmonious", "vi": "hòa hợp (ECE adj)"},
        ],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l11",
        subtitle="Ví dụ People & Family · Is X suitable?",
        hint="Có / Không / Còn tùy. Fighter romance: chemistry, affection, attraction.",
    )


def lesson12_examples_html() -> str:
    items = []
    t1 = (
        "It's not really easy to {easy_hard_x}. I think the hardest part is finding "
        "common ground. It takes time for busy people to trust someone new."
    )
    items.append({
        "q": "Is it easy to make friends as an adult? (TAK12)",
        "html": t1.format(easy_hard_x=phrase_pick("easy_hard_x", 0)),
        "vi": "Không thật sự dễ kết bạn khi đã lớn. Phần khó nhất là tìm điểm chung. Người bận cần thời gian mới tin ai đó.",
        "plain": "It's not really easy to make new friends as an adult. I think the hardest part is finding common ground. It takes time for busy people to trust someone new.",
        "ex": t1,
        "kind": "hard",
        "notes": [{"en": "the hardest part is…", "vi": "phần khó nhất là"}, {"en": "common ground", "vi": "điểm chung"}],
    })
    t2 = (
        "It's quite challenging to {easy_hard_x}. Online chats are easy, but becoming "
        "real friends takes shared experiences. Take my classmate as an example."
    )
    items.append({
        "q": "Is it possible to become real friends with people you meet on the internet? (TAK12)",
        "html": t2.format(easy_hard_x=phrase_pick("easy_hard_x", 1)),
        "vi": "Khá thách thức. Chat thì dễ, nhưng thành bạn thật cần trải nghiệm chung. Lấy bạn cùng lớp làm ví dụ.",
        "plain": "It's quite challenging to become real friends with people you meet online. Online chats are easy, but becoming real friends takes shared experiences. Take my classmate as an example.",
        "ex": t2,
        "kind": "hard",
        "notes": [{"en": "Take … as an example", "vi": "lấy … làm ví dụ"}],
    })
    t3 = (
        "It's always quite difficult at the beginning when you try something new, "
        "and {easy_hard_x} is not an exception. At first you feel awkward, "
        "but after a while things begin to get a bit easier."
    )
    items.append({
        "q": "Is it difficult to maintain a long-distance relationship?",
        "html": t3.format(easy_hard_x=phrase_pick("easy_hard_x", 2)),
        "vi": "Lúc đầu cái gì mới cũng khó, và yêu xa cũng không ngoại lệ. Ban đầu ngượng, sau một thời gian dễ hơn.",
        "plain": "It's always quite difficult at the beginning when you try something new, and maintain a long-distance relationship is not an exception. At first you feel awkward, but after a while things begin to get a bit easier.",
        "ex": t3,
        "kind": "then",
        "notes": [{"en": "… is not an exception", "vi": "cũng không phải ngoại lệ"}, {"en": "At first… / after a while…", "vi": "lúc đầu… / sau một thời gian…"}],
    })
    t4 = (
        "It's quite simple to meet people if you join a club. You can meet "
        "like-minded individuals nearby. However, staying close is another story."
    )
    items.append({
        "q": "Where and how can people get to know new people? (DOL)",
        "html": t4,
        "vi": "Khá đơn giản nếu tham gia câu lạc bộ — gặp người cùng chí hướng. Nhưng giữ quan hệ lại là chuyện khác.",
        "plain": "It's quite simple to meet people if you join a club. You can meet like-minded individuals nearby. However, staying close is another story.",
        "ex": t4,
        "kind": "easy",
        "notes": [{"en": "like-minded individuals", "vi": "người cùng chí hướng (DOL)"}],
    })
    t5 = (
        "Adults and children do not make friends in the same way. For kids it is "
        "really easy — they just play. For adults it takes time to {easy_hard_x}."
    )
    items.append({
        "q": "Do adults and children make friends in the same way? (TAK12)",
        "html": t5.format(easy_hard_x=phrase_pick("easy_hard_x", 3)),
        "vi": "Người lớn và trẻ con không kết bạn giống nhau. Trẻ thì dễ — chỉ cần chơi. Người lớn mất thời gian để giải quyết bất đồng bình tĩnh.",
        "plain": "Adults and children do not make friends in the same way. For kids it is really easy — they just play. For adults it takes time to work through disagreements calmly.",
        "ex": t5,
        "kind": "hard",
        "notes": [{"en": "take + time + to V", "vi": "mất thời gian để…"}],
    })
    t6 = (
        "It's quite easy to meet {relation_type}, but it's harder to {rel_verb}. "
        "The hardest part is to maintain a relationship after you leave school."
    )
    items.append({
        "q": "Is it easy to build and maintain a relationship? (ECE phrasal verbs)",
        "html": t6.format(relation_type=phrase_pick("relation_type", 2), rel_verb=phrase_pick("rel_verb", 2)),
        "vi": "Gặp bạn cùng lớp thì dễ, nhưng củng cố mối quan hệ thì khó hơn. Phần khó nhất là duy trì sau khi rời trường.",
        "plain": "It's quite easy to meet a classmate, but it's harder to strengthen a relationship. The hardest part is to maintain a relationship after you leave school.",
        "ex": t6,
        "kind": "hard",
        "notes": [
            {"en": "build / maintain / strengthen a relationship", "vi": "xây / duy trì / củng cố mối quan hệ (ECE)"},
            {"en": "have a strong bond with someone", "vi": "có sự gắn kết mạnh mẽ"},
        ],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l12",
        subtitle="Ví dụ People & Family · Easy / Difficult?",
        hint="Dễ / Khó / Ban đầu khó. ECE build–maintain–strengthen a relationship.",
    )


def lesson13_examples_html() -> str:
    items = []
    t1 = (
        "I don't really like {dislike_point}. It makes it hard for me to become independent."
    )
    items.append({
        "q": "What do you dislike about family life?",
        "html": t1.format(dislike_point=phrase_pick("dislike_point", 0)),
        "vi": "Tôi không thật sự thích bố mẹ bảo bọc quá mức. Nó khiến tôi khó độc lập.",
        "plain": "I don't really like overprotective parents. It makes it hard for me to become independent.",
        "ex": t1,
        "kind": "direct",
        "notes": [{"en": "overprotective parents", "vi": "bố mẹ bảo bọc quá mức (IDP)"}],
    })
    t2 = (
        "Well, generally speaking I love my family, but the only thing I don't really like "
        "is {dislike_point}. Apart from that, I'm fine."
    )
    items.append({
        "q": "Is there anything you dislike about your relatives?",
        "html": t2.format(dislike_point=phrase_pick("dislike_point", 2)),
        "vi": "Nói chung tôi yêu gia đình, nhưng điều duy nhất tôi không thích là áp lực hôn nhân. Ngoài ra thì ổn.",
        "plain": "Well, generally speaking I love my family, but the only thing I don't really like is family pressure about marriage. Apart from that, I'm fine.",
        "ex": t2,
        "kind": "soft",
        "notes": [{"en": "the only thing I don't really like about X is…", "vi": "điều duy nhất tôi không thích là…"}],
    })
    t3 = (
        "There are a few things that can break a friendship. First, {dislike_point}. "
        "Second, people simply grow apart. Finally, some friends might stab you in the back."
    )
    items.append({
        "q": "What factors may result in the breakdown of a good friendship? (TAK12)",
        "html": t3.format(dislike_point=phrase_pick("dislike_point", 3)),
        "vi": "Có vài thứ làm tình bạn vỡ. Thứ nhất hiểu lầm trên mạng. Thứ hai mọi người lớn theo hướng khác. Cuối cùng có người đâm sau lưng.",
        "plain": "There are a few things that can break a friendship. First, miscommunication on social media. Second, people simply grow apart. Finally, some friends might stab you in the back.",
        "ex": t3,
        "kind": "list",
        "notes": [{"en": "stab someone in the back", "vi": "đâm sau lưng (TAK12)"}, {"en": "First / Second / Finally", "vi": "liệt kê"}],
    })
    t4 = (
        "Undoubtedly one common issue is {dislike_point}. Financial stress is another "
        "contributing factor, and in Vietnam family pressure can place a real strain on couples."
    )
    items.append({
        "q": "What are some common problems that couples face? (Mc Part 3)",
        "html": t4.format(dislike_point=phrase_pick("dislike_point", 3)),
        "vi": "Chắc chắn một vấn đề phổ biến là hiểu lầm. Áp lực tài chính cũng góp phần, và ở Việt Nam áp lực gia đình đè nặng cặp đôi.",
        "plain": "Undoubtedly one common issue is miscommunication on social media. Financial stress is another contributing factor, and in Vietnam family pressure can place a real strain on couples.",
        "ex": t4,
        "kind": "list",
        "notes": [{"en": "contributing factor", "vi": "yếu tố góp phần (Mc)"}, {"en": "miscommunication", "vi": "sự hiểu lầm"}],
    })
    t5 = (
        "Well, I don't really like {dislike_point}. It's hard for quieter kids "
        "to feel seen, but apart from that we still get along."
    )
    items.append({
        "q": "What do you dislike about having siblings?",
        "html": t5.format(dislike_point=phrase_pick("dislike_point", 1)),
        "vi": "Tôi không thật sự thích sự ganh đua anh chị em. Trẻ trầm hơn khó được để ý, nhưng ngoài ra chúng tôi vẫn hòa thuận.",
        "plain": "Well, I don't really like sibling rivalry. It's hard for quieter kids to feel seen, but apart from that we still get along.",
        "ex": t5,
        "kind": "soft",
        "notes": [{"en": "sibling rivalry", "vi": "ganh đua anh chị em (IDP)"}, {"en": "apart from that", "vi": "ngoài điều đó ra"}],
    })
    t6 = (
        "Well, generally speaking I love my family, but some family bonds feel {relation_adj}. "
        "If we fall out with someone and never reconcile, the relationship stays distant."
    )
    items.append({
        "q": "What do you dislike about complicated family bonds? (ECE adj)",
        "html": t6.format(relation_adj=phrase_pick("relation_adj", 3)),
        "vi": "Nói chung tôi yêu gia đình, nhưng một số sự gắn bó cảm thấy phức tạp. Nếu cãi nhau rồi không hàn gắn thì quan hệ mãi xa cách.",
        "plain": "Well, generally speaking I love my family, but some family bonds feel complicated. If we fall out with someone and never reconcile, the relationship stays distant.",
        "ex": t6,
        "kind": "soft",
        "notes": [
            {"en": "family bond · complicated · distant", "vi": "sự gắn bó gia đình · phức tạp · xa cách (ECE)"},
            {"en": "fall out with someone", "vi": "cãi nhau với ai đó"},
        ],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l13",
        subtitle="Ví dụ People & Family · Dislike about X?",
        hint="Nói thẳng / Nói vòng / Liệt kê. ECE complicated / family bond / fall out.",
    )


def lesson14_examples_html() -> str:
    items = []
    t1 = (
        "I try to meet my friends {freq}, which may not seem much, but it is enough "
        "to keep each other updated about our lives."
    )
    items.append({
        "q": "How often do you meet with your friends? (TAK12)",
        "html": t1.format(freq=phrase_pick("freq", 2)),
        "vi": "Tôi cố gặp bạn mỗi tháng một lần — nghe không nhiều nhưng đủ để cập nhật cuộc sống cho nhau.",
        "plain": "I try to meet my friends once a month, which may not seem much, but it is enough to keep each other updated about our lives.",
        "ex": t1,
        "kind": "freq",
        "notes": [{"en": "keep each other updated", "vi": "cập nhật cho nhau (TAK12)"}, {"en": "once a month", "vi": "mỗi tháng một lần"}],
    })
    t2 = (
        "I see my parents {freq} because we still live under the same roof. "
        "I also keep in touch with cousins every now and then."
    )
    items.append({
        "q": "How much time do you manage to spend with your family? (TAK12 / ZIM)",
        "html": t2.format(freq=phrase_pick("freq", 0)),
        "vi": "Tôi gặp bố mẹ hầu như mỗi ngày vì vẫn ở chung. Tôi cũng thỉnh thoảng giữ liên lạc với anh em họ.",
        "plain": "I see my parents almost every day because we still live under the same roof. I also keep in touch with cousins every now and then.",
        "ex": t2,
        "kind": "freq",
        "notes": [{"en": "I also + freq", "vi": "đối chiếu tần suất"}, {"en": "keep in touch", "vi": "giữ liên lạc"}],
    })
    t3 = (
        "I call my grandparents {freq}. I'm too busy to visit every weekend, "
        "but none of us want to lose contact."
    )
    items.append({
        "q": "How often do you visit your grandparents?",
        "html": t3.format(freq=phrase_pick("freq", 1)),
        "vi": "Tôi gọi ông bà mỗi tuần một lần. Tôi quá bận để về mỗi cuối tuần, nhưng không ai muốn mất liên lạc.",
        "plain": "I call my grandparents once a week. I'm too busy to visit every weekend, but none of us want to lose contact.",
        "ex": t3,
        "kind": "rare",
        "notes": [{"en": "too + adj + to V", "vi": "quá … nên không …"}, {"en": "none of + group", "vi": "không một ai trong nhóm"}],
    })
    t4 = (
        "Honestly, I check social media {freq}, but I meet people face to face "
        "once in a blue moon. I make efforts to stay connected, though."
    )
    items.append({
        "q": "How often do you keep in touch with distant relatives?",
        "html": t4.format(freq=phrase_pick("freq", 0)),
        "vi": "Thành thật thì tôi xem mạng hầu như mỗi ngày, nhưng gặp trực tiếp thì năm thì mười họa. Tôi vẫn nỗ lực giữ liên lạc.",
        "plain": "Honestly, I check social media almost every day, but I meet people face to face once in a blue moon. I make efforts to stay connected, though.",
        "ex": t4,
        "kind": "rare",
        "notes": [{"en": "once in a blue moon", "vi": "năm thì mười họa"}, {"en": "make efforts to stay connected", "vi": "nỗ lực giữ liên lạc"}],
    })
    t5 = (
        "At the weekend when none of us have to work, we have dinner together. "
        "On weekdays I hardly ever stay up chatting — I'm too tired to talk for long."
    )
    items.append({
        "q": "How often do you have dinner with your family?",
        "html": t5,
        "vi": "Cuối tuần khi không ai phải làm, chúng tôi ăn tối cùng. Ngày thường tôi hiếm khi thức trò chuyện — quá mệt để nói lâu.",
        "plain": "At the weekend when none of us have to work, we have dinner together. On weekdays I hardly ever stay up chatting — I'm too tired to talk for long.",
        "ex": t5,
        "kind": "freq",
        "notes": [{"en": "none of us have to work", "vi": "không ai phải đi làm"}],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l14",
        subtitle="Ví dụ People & Family · How often?",
        hint="5 bậc tần suất + lý do. TAK12 once a month · keep in touch.",
    )


def lesson15_examples_html() -> str:
    items = []
    t1 = (
        "It has changed a great deal in recent years. In the past, {change_old}. "
        "But recently {change_new} have become much more common."
    )
    items.append({
        "q": "How has the concept of family changed over the years? (WESET / TAK12)",
        "html": t1.format(change_old=phrase_pick("change_old", 0), change_new=phrase_pick("change_new", 0)),
        "vi": "Đã thay đổi rất nhiều. Trước đây đại gia đình sống chung một mái nhà. Gần đây hộ hạt nhân ở thành phố lớn phổ biến hơn.",
        "plain": "It has changed a great deal in recent years. In the past, extended families living under one roof. But recently nuclear households in big cities have become much more common.",
        "ex": t1,
        "kind": "alot",
        "notes": [{"en": "It has changed a great deal", "vi": "đã thay đổi rất lớn"}, {"en": "nuclear households", "vi": "hộ hạt nhân"}],
    })
    t2 = (
        "Technology has had a profound impact. In the past {change_old}. "
        "These days {change_new} help us stay in touch, but they can reduce face-to-face depth."
    )
    items.append({
        "q": "How has technology affected relationships? (WESET / Mc / DOL)",
        "html": t2.format(change_old=phrase_pick("change_old", 2), change_new=phrase_pick("change_new", 1)),
        "vi": "Công nghệ ảnh hưởng sâu. Trước là thư mất cả tuần. Nay video call giúp giữ liên lạc nhưng có thể làm giảm chiều sâu gặp mặt.",
        "plain": "Technology has had a profound impact. In the past letters that took weeks to arrive. These days virtual interaction and video calls help us stay in touch, but they can reduce face-to-face depth.",
        "ex": t2,
        "kind": "alot",
        "notes": [{"en": "profound impact", "vi": "ảnh hưởng sâu (Mc)"}, {"en": "face-to-face vs virtual", "vi": "trực tiếp vs ảo"}],
    })
    t3 = (
        "Yes, at least to some extent. People used to become friends through direct "
        "interaction. Nowadays a fast-paced lifestyle and social media have started "
        "to replace some of that, so some friendships feel less strong."
    )
    items.append({
        "q": "Do you think friendships are different now compared to the past? (ECE)",
        "html": t3,
        "vi": "Có, ít nhất một phần. Trước kết bạn qua gặp mặt. Nay lối sống vội và mạng xã hội thay một phần, nên tình bạn đôi khi mỏng hơn.",
        "plain": "Yes, at least to some extent. People used to become friends through direct interaction. Nowadays a fast-paced lifestyle and social media have started to replace some of that, so some friendships feel less strong.",
        "ex": t3,
        "kind": "alot",
        "notes": [{"en": "used to", "vi": "đã từng"}, {"en": "fast-paced lifestyle", "vi": "lối sống vội vã"}],
    })
    t4 = (
        "It hasn't changed much at the core. The only change is that {change_new}. "
        "Family values like standing by each other through thick and thin are still the same."
    )
    items.append({
        "q": "Have things changed since your parents' time? (TAK12)",
        "html": t4.format(change_new=phrase_pick("change_new", 3)),
        "vi": "Cốt lõi không đổi nhiều. Thay đổi duy nhất là cả hai cùng chia sẻ việc nhà. Giá trị đứng bên nhau trong mọi hoàn cảnh vẫn vậy.",
        "plain": "It hasn't changed much at the core. The only change is that both partners sharing household responsibilities. Family values like standing by each other through thick and thin are still the same.",
        "ex": t4,
        "kind": "little",
        "notes": [{"en": "The only change is that…", "vi": "thay đổi duy nhất là…"}, {"en": "through thick and thin", "vi": "trong mọi hoàn cảnh"}],
    })
    t5 = (
        "As I've grown older, the relationship has evolved from dependency to a more "
        "equal, friendship-like dynamic. We have transitioned, but the deep bonds are still there."
    )
    items.append({
        "q": "How has your relationship with your family changed as you've grown older? (WESET)",
        "html": t5,
        "vi": "Khi lớn hơn, quan hệ chuyển từ phụ thuộc sang bình đẳng, hơi giống bạn bè. Chúng tôi đã chuyển, nhưng mối liên kết sâu vẫn còn.",
        "plain": "As I've grown older, the relationship has evolved from dependency to a more equal, friendship-like dynamic. We have transitioned, but the deep bonds are still there.",
        "ex": t5,
        "kind": "alot",
        "notes": [{"en": "have/has + V3", "vi": "Hiện tại hoàn thành"}, {"en": "since I was a child", "vi": "kể từ khi còn nhỏ"}],
    })
    t6 = (
        "There has been a shift towards individualist values. An increasing number of "
        "young people leave home early. Still, family ties have not been replaced completely."
    )
    items.append({
        "q": "In what ways have families in your country changed recently? (TAK12)",
        "html": t6,
        "vi": "Có sự chuyển dịch sang giá trị cá nhân. Ngày càng nhiều người trẻ ra ở riêng sớm. Nhưng mối quan hệ gia đình chưa bị thay hết.",
        "plain": "There has been a shift towards individualist values. An increasing number of young people leave home early. Still, family ties have not been replaced completely.",
        "ex": t6,
        "kind": "alot",
        "notes": [{"en": "a shift towards…", "vi": "sự chuyển dịch hướng tới…"}, {"en": "an increasing number of", "vi": "ngày càng nhiều"}],
    })
    return _sample_cards(
        items,
        box_id="pf-examples-l15",
        subtitle="Ví dụ People & Family · How has X changed?",
        hint="Đổi nhiều / đổi ít. WESET concept of family · ECE friendships · TAK12 parents' time.",
    )


def lesson16_frame_html() -> str:
    parts = [
        ("1", "Mở đầu", "I'm going to talk about [X] which [paraphrase cue card].",
         "Paraphrase từ khóa trên đề (admire → look up to / good relationship → lifelong bond)."),
        ("2", "Thông tin cơ bản", "Who + How you met + How long + 1 câu đánh giá",
         "Although we don't live under the same roof now, which makes every visit…"),
        ("3", "Cốt lõi ★", "Chiếm phần lớn thời gian (~1–1.5 phút)",
         "Người: tính cách + việc họ làm · Bạn: gặp thế nào + trust · Kỷ niệm: occasion + why memorable"),
        ("4", "Cảm nhận", "Kỷ niệm gần đây · ý nghĩa · emulate / recommend",
         "This is the person I think of… / I try to emulate…"),
        ("5", "Kết", "So, if I had to talk about [topic], it would have to be [X].",
         "Nhắc lại đề (paraphrase) + tên cụ thể đã chọn."),
    ]
    part_cards = "".join(
        f"""              <div class="lr-p2-part" data-p2-step="{n}">
                <span class="lr-p2-num">{n}</span>
                <div class="lr-p2-part-body">
                  <h5 class="lr-p2-part-title">{esc(title)}</h5>
                  <p class="lr-p2-tpl"><code>{esc(tpl)}</code></p>
                  <p class="lr-p2-hint">{esc(hint)}</p>
                </div>
              </div>"""
        for n, title, tpl, hint in parts
    )
    cues = [
        (
            "Family member",
            [
                ("Describe a person you admire in your family (Mc)", "Person"),
                ("Describe a family member you get on well with (TAK12)", "Person"),
                ("Describe something useful you learned from a family member", "Person"),
            ],
        ),
        (
            "Friend / relationship",
            [
                ("Describe a person you have a very good relationship with (ECE)", "Friend"),
                ("Describe a friend you really like to spend time with (TAK12)", "Friend"),
                ("Describe an old friend you got in contact with again (TAK12)", "Friend"),
            ],
        ),
        (
            "Memory / moment",
            [
                ("Describe a memorable moment in a close relationship (WESET)", "Event"),
                ("Describe a person you only met once and want to know more (TAK12)", "Person"),
            ],
        ),
    ]
    cue_cols = []
    for title, items in cues:
        lis = "".join(
            f'<li><span class="lr-p2-cue-q">{esc(q)}</span> '
            f'<span class="lr-p2-cue-tag" data-tag="{esc(tag.lower())}">{esc(tag)}</span></li>'
            for q, tag in items
        )
        cue_cols.append(
            f"""              <div class="lr-lex-col">
                <h5 class="lr-lex-col-title">{esc(title)}</h5>
                <ul class="lr-lex-list lr-p2-cue-list">{lis}</ul>
              </div>"""
        )
    return f"""
          <div class="lr-grammar-notes lr-p2-frame-wrap" id="lesson16-part2-frame">
            <h4 class="lr-grammar-notes-title">Part 2 · Khung 5 phần (cố định mọi đề)</h4>
            <p class="lr-freq-hint">Giống Food: <strong>mở đầu &amp; kết = công thức cố định</strong> · <strong>cốt lõi = dài nhất</strong>. People &amp; Family chỉ đổi nội dung nhánh 2–4.</p>
            <div class="lr-p2-parts">
{part_cards}
            </div>
            <h4 class="lr-grammar-notes-title" style="margin-top:1rem">Cue card People &amp; Family · nguồn bạn gửi</h4>
            <p class="lr-freq-hint">Mc admire · ECE good relationship · TAK12 old friend / spend time with · WESET memorable moment.</p>
            <div class="lr-lex-grid">
{chr(10).join(cue_cols)}
            </div>
          </div>"""


def lesson16_examples_html() -> str:
    cards_data = [
        {
            "cue": "Describe a person you admire in your family",
            "bullets": ["who the person is", "what he or she does", "what he or she is like", "and explain why you admire him or her"],
            "source": "Mc IELTS · TAK12 · family member",
            "choice": "Anh trai Minh · mentor / role model",
            "fw": "Person",
            "secs": [
                ("Mở đầu",
                 f'{phrase_pick("p2_open", 0)} my older brother Minh, who I really look up to — not just as a sibling but as a mentor.',
                 "Tôi sẽ nói về anh trai Minh, người tôi thực sự ngưỡng mộ — không chỉ là anh em mà còn là người dẫn dắt."),
                ("Thông tin cơ bản",
                 "He studied engineering and used to stay up late, never giving up. Although he is busy now, he still makes time, which makes every conversation meaningful.",
                 "Anh học kỹ thuật, từng thức khuya không bỏ cuộc. Dù bận, anh vẫn sắp xếp thời gian, khiến mỗi cuộc nói chuyện đều ý nghĩa."),
                ("Cốt lõi",
                 "What I admire most is his kindness and selflessness. He never hesitates to lend a hand — helping a neighbour or volunteering. I also remember our weekend fishing trips, when he taught me perseverance and patience. People say we are like two peas in a pod, but he is the one I try to emulate.",
                 "Điều tôi ngưỡng mộ nhất là sự tử tế và vị tha. Anh không ngần ngại giúp hàng xóm hay tình nguyện. Tôi nhớ những buổi câu cuối tuần, khi anh dạy tôi sự bền bỉ. Người ta nói chúng tôi giống như đúc, nhưng anh là người tôi muốn noi theo."),
                ("Cảm nhận",
                 "His influence still shapes my values. I would recommend having a role model like him to anyone who needs unwavering support.",
                 "Ảnh hưởng của anh vẫn định hình giá trị của tôi. Tôi khuyên ai cần sự hỗ trợ kiên định hãy có một tấm gương như anh."),
                ("Kết",
                 f'{phrase_pick("p2_close", 0)}, {phrase_pick("p2_close_tail", 2)}',
                 "Vậy nếu tôi phải nói về người tôi ngưỡng mộ, thì đó sẽ phải là anh Minh."),
            ],
            "notes": [
                {"en": "look up to / emulate", "vi": "ngưỡng mộ / noi gương (Mc)"},
                {"en": "selflessness · perseverance", "vi": "vị tha · sự bền bỉ"},
            ],
        },
        {
            "cue": "Describe a person you have a very good relationship with",
            "bullets": ["who the person is", "how you met", "what you usually do together", "and explain why the relationship is good"],
            "source": "ECE English · best friend",
            "choice": "Bạn thân Lam · 10+ năm",
            "fw": "Friend",
            "secs": [
                ("Mở đầu",
                 f'{phrase_pick("p2_open", 1)} my best friend Lam, who I have known for over ten years.',
                 "Tôi muốn nói về bạn thân Lam, người tôi quen hơn mười năm."),
                ("Thông tin cơ bản",
                 "We met in secondary school and were assigned to sit next to each other. She broke the ice by asking about a school club. Although we no longer live in the same city, which makes meeting harder, we still keep in touch.",
                 "Chúng tôi gặp ở cấp 2, được xếp ngồi cạnh. Cô ấy phá băng bằng câu hỏi về CLB. Dù không còn cùng thành phố, chúng tôi vẫn giữ liên lạc."),
                ("Cốt lõi",
                 "We have so many shared interests and similar personalities. We used to ride to school and have lunch together. What makes the friendship special is the trust — we never take this care for granted, and we stand by each other through thick and thin.",
                 "Chúng tôi có nhiều sở thích chung và tính cách giống. Ngày xưa đi học chung, ăn trưa chung. Điều đặc biệt là sự tin tưởng — không xem sự quan tâm là đương nhiên, và đứng bên nhau trong mọi hoàn cảnh."),
                ("Cảm nhận",
                 "I know I will always receive willing support from her, and I would definitely do the same. That is why I believe our friendship is going to last.",
                 "Tôi biết mình luôn nhận được sự hỗ trợ sẵn lòng, và tôi cũng sẽ làm vậy. Vì thế tôi tin tình bạn này sẽ bền."),
                ("Kết",
                 f'{phrase_pick("p2_close", 1)}, {phrase_pick("p2_close_tail", 1)}',
                 "Vậy nếu tôi phải nói về một mối quan hệ thân, thì đó sẽ phải là bạn thân Lan."),
            ],
            "notes": [
                {"en": "broke the ice", "vi": "phá băng (ECE)"},
                {"en": "never take … for granted", "vi": "không xem là đương nhiên"},
                {"en": "through thick and thin", "vi": "trong mọi hoàn cảnh"},
            ],
        },
        {
            "cue": "Describe an old friend that you got in contact with again",
            "bullets": ["who he or she is", "what he or she is like", "how you got in contact", "and explain how you felt"],
            "source": "TAK12 · old friend / Facebook",
            "choice": "Bạn học Preet · mất liên lạc rồi gặp lại",
            "fw": "Friend",
            "secs": [
                ("Mở đầu",
                 f'{phrase_pick("p2_open", 0)} a school friend I lost contact with and found again on Facebook.',
                 "Tôi sẽ nói về một bạn học tôi mất liên lạc rồi tìm lại trên Facebook."),
                ("Thông tin cơ bản",
                 "Her name is Preet. We studied together for ten years before her family shifted to another city. Unfortunately I lost her number. Although years passed, she still holds a special place in my memory.",
                 "Tên cô ấy là Preet. Chúng tôi học cùng mười năm trước khi gia đình chuyển đi. Không may tôi mất số. Dù nhiều năm, cô ấy vẫn giữ chỗ đặc biệt trong trí nhớ."),
                ("Cốt lõi",
                 "She was a brilliant student, good at maths and sports, and she liked to live simply. Last month I typed her name in the search box, sent a friend request, and she accepted the next day. After that we started calling and recalling our old days.",
                 "Cô ấy học giỏi, giỏi toán và thể thao, sống giản dị. Tháng trước tôi gõ tên trên thanh tìm, gửi lời mời, hôm sau cô ấy nhận. Sau đó chúng tôi gọi và ôn ngày cũ."),
                ("Cảm nhận",
                 "I felt thrilled because I had been trying to find her for years. Whenever we call, we keep each other updated and laugh about school memories.",
                 "Tôi thấy vui sướng vì đã cố tìm cô ấy nhiều năm. Mỗi lần gọi, chúng tôi cập nhật cho nhau và cười về kỷ niệm trường."),
                ("Kết",
                 f'{phrase_pick("p2_close", 2)}, {phrase_pick("p2_close_tail", 3)}',
                 "Vậy nếu tôi phải nói về một người bạn cũ, thì đó sẽ phải là bạn học Preet."),
            ],
            "notes": [
                {"en": "lose contact / get in contact", "vi": "mất liên lạc / liên lạc lại (TAK12)"},
                {"en": "a friend request", "vi": "lời mời kết bạn"},
            ],
        },
        {
            "cue": "Describe a memorable moment in a close relationship",
            "bullets": ["who the person is", "what the occasion was", "where it happened", "and why it was memorable"],
            "source": "WESET · surprise birthday",
            "choice": "Tiệc sinh nhật bất ngờ · bạn Lan 30 tuổi",
            "fw": "Event",
            "secs": [
                ("Mở đầu",
                 f'{phrase_pick("p2_open", 1)} a surprise birthday I organised for my best friend Lan when she turned 30.',
                 "Tôi muốn nói về tiệc sinh nhật bất ngờ tôi tổ chức cho bạn thân Lan khi cô ấy 30 tuổi."),
                ("Thông tin cơ bản",
                 "It took place at a rooftop café that held sentimental value — we had spent countless evenings there in college. Although I was nervous about the surprise, the location made it a perfect place for those who wanted a warm celebration.",
                 "Ở quán cà phê sân thượng có giá trị tình cảm — chúng tôi từng ngồi đó vô số tối đại học. Dù tôi hồi hộp vì bất ngờ, địa điểm rất hợp cho buổi kỷ niệm ấm."),
                ("Cốt lõi",
                 "Lan had no idea. Seeing her reaction — joy, disbelief, then tears — is etched in my memory. The speeches and heartfelt conversations reaffirmed our enduring friendship. It was not only a birthday; it was a reminder to celebrate milestones with those who matter most.",
                 "Lan không hề biết. Nhìn phản ứng — vui, không tin, rồi nước mắt — khắc trong trí nhớ. Những lời phát biểu khẳng định tình bạn bền. Không chỉ sinh nhật; còn là nhắc nhở kỷ niệm các mốc với người quan trọng."),
                ("Cảm nhận",
                 "That night highlighted the power of genuine connections. It is a memory both of us hold dear to our hearts.",
                 "Đêm đó làm nổi bật sức mạnh của kết nối thật. Đó là kỷ niệm cả hai đều trân trọng."),
                ("Kết",
                 f'{phrase_pick("p2_close", 1)}, that rooftop surprise for Lan.',
                 "Vậy nếu tôi phải nói về một mối quan hệ thân, thì đó sẽ phải là đêm bất ngờ trên sân thượng cho Lan."),
            ],
            "notes": [
                {"en": "sentimental value", "vi": "giá trị tình cảm (WESET)"},
                {"en": "celebrate milestones", "vi": "kỷ niệm các mốc quan trọng"},
                {"en": "enduring friendship", "vi": "tình bạn bền vững"},
            ],
        },
    ]
    cards_html = []
    for it in cards_data:
        bullets = "".join(f"<li>{esc(b)}</li>" for b in it["bullets"])
        secs = "\n".join(_p2_sec(lab, en, vi) for lab, en, vi in it["secs"])
        fw = it.get("fw") or ""
        fw_html = (
            f'<p class="lr-p2-fw"><span class="lr-p2-cue-tag" data-tag="{esc(fw.lower())}">{esc(fw)}</span></p>'
            if fw else ""
        )
        cards_html.append(f"""          <article class="lr-food-ex-card lr-p2-card">
            <div class="lr-cue-box">
              <p class="lr-cue-title">{esc(it["cue"])}</p>
{fw_html}              <p class="lr-cue-should">You should say:</p>
              <ul class="lr-cue-bullets">{bullets}</ul>
            </div>
            <p class="lr-food-ex-source">{esc(it["source"])} · chọn: <strong>{esc(it["choice"])}</strong></p>
            <div class="lr-p2-answer">
{secs}
            </div>
{_ex_chip_notes_html(it.get("notes"))}
          </article>""")
    return f"""
        <div class="lr-food-examples" id="pf-examples-l16">
          <h3 class="lr-core-subtitle">Ví dụ People &amp; Family · Part 2 (5 phần)</h3>
          <p class="lr-mm-hint">Cue từ Mc / ECE / TAK12 / WESET. Hover đoạn → tooltip VI. Dropdown ở mở/kết để đổi khung.</p>
{chr(10).join(cards_html)}
        </div>"""


def lesson_highlights_html() -> str:
    g2 = lesson_grammar_notes_html(
        "Lesson 2",
        [
            "It's + adj · It makes me + adj · It helps me + V · It's a great way to + V",
            "doesn't + V · can lead to + NP (loneliness / mistrust / drifting apart)",
            "Nhánh Sức khỏe tinh thần = Cụm V Family — không dùng keep fit / burn calories",
        ],
    )
    g3 = lesson_grammar_tree_html(
        "Lesson 3 · Do you like X?",
        "Yes / No + Reasons",
        [
            {
                "label_html": f'{_g_mark("YES")}',
                "openers": ["Yes, definitely / absolutely", "I like/love/enjoy + V-ing · I'm keen on · I'm a big fan of"],
                "details_label": "Family",
                "details": ["close-knit · quality time · keep in touch · confide in"],
            },
            {
                "label_html": f'{_g_mark("NO")}',
                "openers": ["No, not really · I hardly ever + V", "prefer to V rather than V"],
                "details_label": "Family",
                "details": ["large parties · lose contact · posting private life"],
            },
        ],
        footer=["because / This is because + S + V", "because of + NP"],
    )
    g5 = lesson_grammar_tree_html(
        "Lesson 5 · What kind?",
        "Loại gì? + Lý do",
        [
            {
                "label_html": f'{_g_mark("Soft choose")}',
                "openers": ["I love all kinds of …, but if I had to choose one,", "it would have to be / I would go for / opt for"],
            },
            {
                "label_html": f'{_g_mark("Lý do")}',
                "openers": ["This is because + S + V", "try to / try not to / try + V-ing"],
                "details_label": "Lexical Family",
                "details": ["emotionally supportive · like-minded · mutual trust · compatibility"],
            },
        ],
    )
    g6 = lesson_grammar_tree_html(
        "Lesson 6 · Prefer X or Y?",
        "Chọn + Lý do",
        [
            {
                "label_html": f'{_g_mark("prefer")}',
                "openers": ["I prefer X", "I prefer X to Y", "I prefer X rather than Y · lean towards"],
            },
            {
                "label_html": f'{_g_mark("Contrast")}',
                "openers": ["while / whereas", "comfort and security ↔ superficial crowd"],
            },
        ],
    )
    g7 = lesson_grammar_tree_html(
        "Lesson 7 · Is X popular?",
        "Có / Không / Còn tùy",
        [
            {
                "label_html": f'{_g_mark("Có / Không")}',
                "openers": ["the majority / a large proportion / account for %", "not many / very few / rarely"],
            },
            {
                "label_html": f'{_g_mark("Còn tùy")}',
                "openers": ["collectivist ↔ individualist", "urban ↔ rural · nuclear ↔ extended"],
            },
        ],
    )
    g8 = lesson_grammar_tree_html(
        "Lesson 8 · Best time?",
        "Thời điểm / Còn tùy",
        [
            {
                "label_html": f'{_g_mark("Thời điểm")}',
                "openers": ["… is the best / ideal time to …", "catch up on each other's day · Tet"],
            },
            {
                "label_html": f'{_g_mark("Còn tùy")}',
                "openers": ["It depends on mood / schedule", "as long as · generally speaking"],
            },
        ],
    )
    g9 = lesson_grammar_tree_html(
        "Lesson 9 · First / last time?",
        "Nhớ rõ / Đoán",
        [
            {
                "label_html": f'{_g_mark("Nhớ rõ")}',
                "openers": ["As far as I can remember", "it's been … since · get in contact / reconcile"],
            },
            {
                "label_html": f'{_g_mark("Đoán")}',
                "openers": ["I can't remember exactly, but I guess", "About … ago / when I was in…"],
            },
        ],
    )
    g10 = lesson_grammar_tree_html(
        "Lesson 10 · Childhood?",
        "Có / Không",
        [
            {
                "label_html": f'{_g_mark("Có")}',
                "openers": ["Yes, I did · When I was a kid", "instilled · take after · look up to"],
            },
            {
                "label_html": f'{_g_mark("Không")}',
                "openers": ["No, not really", "find + sth + adj · did + V (emphasis)"],
            },
        ],
    )
    g11 = lesson_grammar_tree_html(
        "Lesson 11 · Suitable?",
        "Có / Không / Còn tùy",
        [
            {
                "label_html": f'{_g_mark("Có")}',
                "openers": ["Yes, I think so · as long as there is mutual trust", "long-distance + video calls"],
            },
            {
                "label_html": f'{_g_mark("Không / Còn tùy")}',
                "openers": ["deal-breaker · love at first sight", "If … then … / But if …"],
            },
        ],
    )
    g12 = lesson_grammar_tree_html(
        "Lesson 12 · Easy / Difficult?",
        "Dễ / Khó / Ban đầu khó",
        [
            {
                "label_html": f'{_g_mark("Dễ / Khó")}',
                "openers": ["It's quite easy / not really difficult", "the hardest part is · take + time"],
            },
            {
                "label_html": f'{_g_mark("Tiến trình")}',
                "openers": ["… is not an exception", "At first… / after a while…"],
            },
        ],
    )
    g13 = lesson_grammar_tree_html(
        "Lesson 13 · Dislike?",
        "Nói thẳng / Nói vòng",
        [
            {
                "label_html": f'{_g_mark("Thẳng")}',
                "openers": ["I don't really like…", "overprotective · sibling rivalry"],
            },
            {
                "label_html": f'{_g_mark("Vòng")}',
                "openers": ["generally speaking · the only thing", "First / Second / Finally · stab in the back"],
            },
        ],
    )
    g14 = lesson_grammar_tree_html(
        "Lesson 14 · How often?",
        "Tần suất + lý do",
        [
            {
                "label_html": f'{_g_mark("5 bậc")}',
                "openers": ["almost every day · once a week · once a month", "every now and then · once in a blue moon"],
            },
            {
                "label_html": f'{_g_mark("Grammar")}',
                "openers": ["none of + group", "too + adj + to V · keep in touch"],
            },
        ],
    )
    g15 = lesson_grammar_tree_html(
        "Lesson 15 · How changed?",
        "Đổi nhiều / Đổi ít",
        [
            {
                "label_html": f'{_g_mark("Đổi nhiều")}',
                "openers": ["It has changed a great deal", "Past Simple → Present Perfect · nuclear / virtual"],
            },
            {
                "label_html": f'{_g_mark("Đổi ít")}',
                "openers": ["It hasn't changed much · The only change is…", "family values · through thick and thin"],
            },
        ],
    )
    g16 = lesson_grammar_tree_html(
        "Lesson 16 · Part 2",
        "Describe a People / Family cue card",
        [
            {
                "label_html": f'{_g_mark("Mở + Kết")} cố định',
                "openers": ["I'm going to talk about [X] which [paraphrase]", "So, if I had to talk about [topic], it would have to be [X]"],
            },
            {
                "label_html": f'{_g_mark("Cốt lõi")} ★',
                "openers": ["Người: look up to + selflessness", "Bạn: broke the ice + keep in touch", "Kỷ niệm: celebrate milestones"],
            },
        ],
        footer=["Reuse Family lexical từ L2–L15", "Cốt lõi ~60%"],
    )

    def _lesson(num: str, title: str, mmap_id: str, center: str, sides: str, left, right, note: str, extra: str, gmin: str, grammar: str, vocab: str, examples: str, scroll_id: str, memo: str = "") -> str:
        memo_sel = f"#lesson{num}-memo" if memo else ""
        return f"""
        <article class="lr-core-lesson" id="lesson{num}-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson {num} · {esc(title)}</h3>
          </header>
{mind_map_html(mmap_id, f"Lesson {num} · {title}", center, sides, left, right, note=note, extra_class=extra, min_width=gmin)}
{grammar}
{vocab}
          <div id="lesson{scroll_id}-scroll-source">
{examples}
          </div>
{memo}
{lesson_scroll_read_html(f"lesson{scroll_id}", title=f"Lesson {num}", source_sel=f"#lesson{scroll_id}-scroll-source", memo_sel=memo_sel)}
        </article>"""

    return f"""
      <div class="lr-core-lessons">
        <article class="lr-core-lesson" id="lesson2-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 2 · Reasons like / dislike</h3>
          </header>
{mind_map_html("lesson2MindmapPF", "Lesson 2 · Reasons like / dislike", "Reasons", "Dislike ↔ Like", _maps.LESSON2_MINDMAP_LEFT, _maps.LESSON2_MINDMAP_RIGHT, note="Trái = <strong>KHÔNG THÍCH</strong> · Phải = <strong>THÍCH</strong>. Nhánh sức khỏe Food → <strong>tinh thần / gắn kết</strong>.", extra_class=" lr-mmap--lesson2", min_width="1280px")}
{g2}
{vocab_notes_html(VOCAB_L2)}
{lesson2_practice_html()}
        </article>
{_lesson("3", "Do you like X?", "lesson3MindmapPF", "Do you like X?", "No ↔ Yes + Reasons", _maps.LESSON3_MINDMAP_LEFT, _maps.LESSON3_MINDMAP_RIGHT, "Trái = <strong>NO</strong> · Phải = <strong>YES</strong> + Reasons.", " lr-mmap--lesson3", "1200px", g3, vocab_notes_html(VOCAB_L3), lesson3_examples_html(), "3", lesson3_memo_html())}
{_lesson("5", "What kind of X do you like most?", "lesson5MindmapPF", "What kind of X?", "Loại gì? ↔ Lý do", _maps.LESSON5_MINDMAP_LEFT, _maps.LESSON5_MINDMAP_RIGHT, "Trái = <strong>Loại gì?</strong> · Phải = <strong>Lý do</strong> + Lexical Family.", " lr-mmap--lesson5", "1200px", g5, vocab_think_notes_html(VOCAB_L5), lesson5_examples_html(), "5", memo_html_for("5"))}
{_lesson("6", "Do you prefer X or Y?", "lesson6MindmapPF", "Do you prefer X or Y?", "Chọn ↔ Lý do", _maps.LESSON6_MINDMAP_LEFT, _maps.LESSON6_MINDMAP_RIGHT, "Trái = <strong>prefer X / X to Y / rather than</strong> · Phải = lý do Family.", " lr-mmap--lesson6", "1200px", g6, vocab_notes_html(VOCAB_L6), lesson6_examples_html(), "6", memo_html_for("6"))}
{_lesson("7", "Is X popular in your country?", "lesson7MindmapPF", "Is X popular?", "Có/Không ↔ Còn tùy", _maps.LESSON7_MINDMAP_LEFT, _maps.LESSON7_MINDMAP_RIGHT, "Trái = <strong>Có / Không</strong> · Phải = <strong>Còn tùy</strong> (collectivist · đô thị · cấu trúc gia đình).", " lr-mmap--lesson7", "1280px", g7, vocab_notes_html(VOCAB_L7), lesson7_examples_html(), "7", memo_html_for("7"))}
{_lesson("8", "What is the best time to do X?", "lesson8MindmapPF", "Best time to do X?", "Thời điểm ↔ Còn tùy", _maps.LESSON8_MINDMAP_LEFT, _maps.LESSON8_MINDMAP_RIGHT, "Trái = <strong>Thời điểm tốt nhất</strong> · Phải = <strong>Còn tùy</strong> + Lexical Family.", " lr-mmap--lesson8", "1280px", g8, vocab_notes_html(VOCAB_L8), lesson8_examples_html(), "8", memo_html_for("8"))}
{_lesson("9", "When was the first/last time you did X?", "lesson9MindmapPF", "First / last time?", "Nhớ rõ ↔ Đoán", _maps.LESSON9_MINDMAP_LEFT, _maps.LESSON9_MINDMAP_RIGHT, "Trái = <strong>Nói rõ thời gian</strong> · Phải = <strong>Đoán</strong> + get in contact / reconcile.", " lr-mmap--lesson9", "1280px", g9, vocab_notes_html(VOCAB_L9), lesson9_examples_html(), "9", memo_html_for("9"))}
{_lesson("10", "Did you do X when you were a child?", "lesson10MindmapPF", "When you were a child?", "Có ↔ Không", _maps.LESSON10_MINDMAP_LEFT, _maps.LESSON10_MINDMAP_RIGHT, "Trái = <strong>Có</strong> + childhood time · Phải = <strong>Không</strong> + take after / instilled.", " lr-mmap--lesson10", "1280px", g10, vocab_notes_html(VOCAB_L10), lesson10_examples_html(), "10", memo_html_for("10"))}
{_lesson("11", "Is X suitable for…?", "lesson11MindmapPF", "Is X suitable for…?", "Có / Không ↔ Còn tùy", _maps.LESSON11_MINDMAP_LEFT, _maps.LESSON11_MINDMAP_RIGHT, "Trái = <strong>Có</strong> · Phải = <strong>Không</strong> + <strong>Còn tùy</strong> (long-distance · love at first sight).", " lr-mmap--lesson11", "1320px", g11, vocab_notes_html(VOCAB_L11), lesson11_examples_html(), "11", memo_html_for("11"))}
{_lesson("12", "Is it easy/difficult to do X?", "lesson12MindmapPF", "Easy / Difficult?", "Dễ / Khó ↔ Ban đầu khó", _maps.LESSON12_MINDMAP_LEFT, _maps.LESSON12_MINDMAP_RIGHT, "Trái = <strong>Dễ</strong> · Phải = <strong>Khó</strong> + tiến trình. Câu TAK12 / DOL.", " lr-mmap--lesson12", "1320px", g12, vocab_notes_html(VOCAB_L12), lesson12_examples_html(), "12", memo_html_for("12"))}
{_lesson("13", "What do you dislike about X?", "lesson13MindmapPF", "Dislike about X?", "Nói thẳng ↔ Nói vòng", _maps.LESSON13_MINDMAP_LEFT, _maps.LESSON13_MINDMAP_RIGHT, "Trái = <strong>Nói thẳng</strong> · Phải = <strong>Nói vòng</strong> / liệt kê.", " lr-mmap--lesson13", "1320px", g13, vocab_notes_html(VOCAB_L13), lesson13_examples_html(), "13", memo_html_for("13"))}
{_lesson("14", "How often do you do X?", "lesson14MindmapPF", "How often?", "Tần suất ↔ Lý do", _maps.LESSON14_MINDMAP_LEFT, _maps.LESSON14_MINDMAP_RIGHT, "Trái = <strong>5 bậc</strong> · Phải = lý do + none of / too…to.", " lr-mmap--lesson14", "1320px", g14, vocab_notes_html(VOCAB_L14), lesson14_examples_html(), "14", memo_html_for("14"))}
{_lesson("15", "How has X changed?", "lesson15MindmapPF", "How has X changed?", "Đổi nhiều ↔ Đổi ít", _maps.LESSON15_MINDMAP_LEFT, _maps.LESSON15_MINDMAP_RIGHT, "Trái = <strong>đổi nhiều</strong> · Phải = <strong>đổi ít</strong> + lexical nâng điểm Family.", " lr-mmap--lesson15", "1320px", g15, vocab_notes_html(VOCAB_L15), lesson15_examples_html(), "15", memo_html_for("15"))}
        <article class="lr-core-lesson" id="lesson16-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 16 · Part 2 People &amp; Family (5 phần)</h3>
          </header>
{mind_map_html("lesson16MindmapPF", "Lesson 16 · Part 2 Family", "Describe a People cue card", "5 phần cố định", _maps.LESSON16_MINDMAP_LEFT, _maps.LESSON16_MINDMAP_RIGHT, note="Trái = <strong>mở · cơ bản · kết</strong> · Phải = <strong>cốt lõi + cảm nhận</strong> theo loại đề Family.", extra_class=" lr-mmap--lesson16", min_width="1360px")}
{lesson16_frame_html()}
{g16}
{vocab_notes_html(VOCAB_L16)}
          <div id="lesson16-scroll-source">
{lesson16_examples_html()}
          </div>
{lesson_scroll_read_html("lesson16", title="Lesson 16 · Part 2", source_sel="#lesson16-scroll-source")}
        </article>
      </div>"""


def build_page_review2() -> str:
    home = "../../../../"
    slots_json = json.dumps(WORD_SLOTS, ensure_ascii=False)
    body = f"""    <aside class="docs-sidebar" id="docsSidebar" data-nav="english" data-docs-root="../../" data-active="people-family">
      <div class="docs-nav-label">English</div>
      <ul class="docs-nav" id="docsNav">
        <li><a href="../../">All topics</a></li>
        <li><a href="../">People &amp; Family</a></li>
        <li><a href="../review-exercise/">Review Exercise 1</a></li>
        <li><a class="active" href="./">Review Exercise 2</a></li>
      </ul>
      <div class="docs-nav-label">Lessons</div>
      <ul class="docs-nav docs-nav--page" aria-label="Lessons on this page">
        <li><a href="#lesson2-formulas">Lesson 2 · Reasons</a></li>
        <li><a href="#lesson3-formulas">Lesson 3 · Do you like X?</a></li>
        <li><a href="#lesson5-formulas">Lesson 5 · What kind?</a></li>
        <li><a href="#lesson6-formulas">Lesson 6 · Prefer X or Y?</a></li>
        <li><a href="#lesson7-formulas">Lesson 7 · Is X popular?</a></li>
        <li><a href="#lesson8-formulas">Lesson 8 · Best time?</a></li>
        <li><a href="#lesson9-formulas">Lesson 9 · First/last time?</a></li>
        <li><a href="#lesson10-formulas">Lesson 10 · Childhood?</a></li>
        <li><a href="#lesson11-formulas">Lesson 11 · Suitable?</a></li>
        <li><a href="#lesson12-formulas">Lesson 12 · Easy/Difficult?</a></li>
        <li><a href="#lesson13-formulas">Lesson 13 · Dislike about X?</a></li>
        <li><a href="#lesson14-formulas">Lesson 14 · How often?</a></li>
        <li><a href="#lesson15-formulas">Lesson 15 · How changed?</a></li>
        <li><a href="#lesson16-formulas">Lesson 16 · Part 2</a></li>
      </ul>
    </aside>
    <article class="docs-main lr-page">
      <div class="docs-breadcrumb">
        <a href="{home}">Home</a><span>›</span>
        <a href="{home}#blogs">Blogs</a><span>›</span>
        <a href="../../">English</a><span>›</span>
        <a href="../">People &amp; Family</a><span>›</span>
        <span>Review Exercise 2</span>
      </div>
      <header class="lr-hero">
        <p class="lr-hero-badge">Linear Thinking · Lesson 2–16</p>
        <h1>People &amp; Family — Review Exercise 2</h1>
        <p class="lede">Cùng khung Food (skip Lesson 4): mind map + ví dụ Relationships &amp; Family + dropdown. Cụm từ / idiom lấy từ <a href="https://tuhoc.dolenglish.vn/blog/relationships-and-personalities-bai-mau-sample-ielts-speaking-part-3" target="_blank" rel="noopener">DOL</a>, <a href="https://ece.edu.vn/ielts-speaking-topic-relationships/" target="_blank" rel="noopener">ECE</a>, <a href="https://tak12.com/news/n/1601/on-thi-ielts-tong-hop-de-thi-ielts-speaking-topic-people-and-relationships" target="_blank" rel="noopener">TAK12</a>, <a href="https://zim.vn/ielts-speaking-part-1-topic-relationship" target="_blank" rel="noopener">ZIM</a>, <a href="https://weset.edu.vn/blog/bai-hoc-moi-ngay/ielts-speaking-topic-relationship/" target="_blank" rel="noopener">WESET</a>, <a href="https://mcielts.com/topic-relationship-ielts-speaking/" target="_blank" rel="noopener">Mc IELTS</a>, IDP.</p>
      </header>
      <section class="lr-section" id="lessons">
        <h2>Lessons</h2>
{lesson_highlights_html()}
      </section>
      <script type="application/json" id="lrWordSlots">{slots_json}</script>
    </article>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Review Exercise 2 · People &amp; Family — The Quiet Corner</title>
  <meta name="description" content="Lesson 2, 3, 5–16: Reasons through Part 2 People &amp; Family — mind maps and cue-card talks.">
  <link rel="icon" href="{home}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{home}css/docs.css?v=lr73">
</head>
<body class="docs lr-body">
  <div class="cursor" id="cursor"></div>
  <div class="cursor-ring" id="cursorRing"></div>
  <canvas id="matrix-canvas"></canvas>
  <div class="grid-bg"></div>
  <header class="docs-topbar">
    <button class="docs-menu-btn" id="docsMenuBtn" type="button">menu</button>
    <button class="docs-sidebar-toggle" id="docsSidebarToggle" type="button" aria-expanded="true" aria-label="Toggle navigation" title="Thu thanh điều hướng"><svg class="docs-nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    <a class="docs-brand" href="{home}"><span>✦</span> The Quiet Corner <span>✦</span></a>
    <nav class="docs-series">
      <a href="{home}blog/web-security/">DevSecOps</a>
      <a href="{home}blog/kubestronaut/">Kubestronaut</a>
      <a class="active" href="../../">English</a>
      <a href="{home}blog/tech-hub/">Tech Hub</a>
    </nav>
    <span class="docs-topbar-spacer"></span>
    <a class="docs-top-link" href="{home}#blogs">blogs</a>
  </header>
  <div class="docs-shell docs-shell--wide">
{body}
  </div>
  <script src="{home}js/docs.js?v=lr23"></script>
  <script src="{home}js/linear-review.js?v=lr47"></script>
</body>
</html>"""


def patch_topic_index() -> None:
    path = ROOT / "public" / "blog" / "english" / "people-family" / "index.html"
    text = path.read_text(encoding="utf-8")
    review_icon = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72' fill='none'%3E"
        "%3Crect width='72' height='72' rx='14' fill='%231a1033'/%3E"
        "%3Ccircle cx='36' cy='36' r='22' stroke='%23a78bfa' stroke-width='2.5'/%3E"
        "%3Cpath d='M36 20v16l10 8' stroke='%2322d3ee' stroke-width='2.5' stroke-linecap='round'/%3E"
        "%3Cpath d='M22 48h28' stroke='%23e4e4e7' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E"
    )
    review2_icon = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72' fill='none'%3E"
        "%3Crect width='72' height='72' rx='14' fill='%23101828'/%3E"
        "%3Ccircle cx='36' cy='36' r='18' stroke='%2334d399' stroke-width='2.5'/%3E"
        "%3Cpath d='M24 36h24M36 24v24' stroke='%2367e8f9' stroke-width='2.5' stroke-linecap='round'/%3E"
        "%3C/svg%3E"
    )
    review_section = f"""
      <section class="vocab-level vocab-level--review" id="review">
        <div class="vocab-level__head">
          <span class="vocab-level__badge vocab-level__badge--review">Review</span>
          <h2>Linear Thinking · Capstone exercise</h2>
        </div>
        <p class="vocab-level__desc"><strong>Review 1</strong> — full capstone: ngữ pháp (gerunds, because/conditional 2), mental model, cấu trúc Speaking, mock IELTS Part 1/2/3. <strong>Review 2</strong> — Lesson 2, 3, 5–16 (mind map + ví dụ People &amp; Family + dropdown; skip Lesson 4). Trước khi học: Pareto 80/20 → neo ngữ cảnh → khung câu an toàn.</p>
        <div class="vocab-lesson-grid">
          <a class="vocab-lesson-card vocab-lesson-card--review" href="review-exercise/">
            <img src="{review_icon}" alt="" width="72" height="72" loading="lazy">
            <span>Review Exercise 1</span>
          </a>
          <a class="vocab-lesson-card vocab-lesson-card--review" href="review-exercise-2/">
            <img src="{review2_icon}" alt="" width="72" height="72" loading="lazy">
            <span>Review Exercise 2</span>
          </a>
        </div>
        <div class="vocab-core-steps">
          <h3 class="vocab-core-steps-title">Core steps · trước khi học &amp; ôn</h3>
          <p class="vocab-core-steps-lead">Đừng ôm 100 từ. Làm 3 bước này trước Flashcards / Review Exercise:</p>
          <ol class="vocab-core-steps-list">
            <li><strong>Pareto 80/20</strong> — chia 3 nhóm: Không thông dụng · Phải học · Đã biết. Chỉ giữ ~20–30 từ vàng.</li>
            <li><strong>Neo ngữ cảnh</strong> — gắn mỗi từ vào 1 câu mẫu duy nhất (vd. “We're a <em>close-knit</em> family, so we talk almost every day.”).</li>
            <li><strong>Khung câu an toàn</strong> — lắp từ vào: <em>I'm a big fan of…</em> · <em>Whenever I have free time, I really love to…</em> · <em>What I like most about…</em></li>
          </ol>
          <p class="vocab-core-steps-more"><a href="review-exercise/#core-steps">Xem hướng dẫn đầy đủ trong Review Exercise 1 →</a></p>
        </div>
      </section>
"""
    if 'id="review"' in text:
        text, n = re.subn(
            r'\s*<section class="vocab-level vocab-level--review" id="review">.*?</section>',
            "\n" + review_section.rstrip() + "\n",
            text,
            count=1,
            flags=re.S,
        )
        if n:
            path.write_text(text, encoding="utf-8")
        return
    marker = '      <div class="docs-pager">'
    if marker in text:
        text = text.replace(marker, review_section + "\n" + marker)
        path.write_text(text, encoding="utf-8")


def patch_review1_nav() -> None:
    path = ROOT / "public" / "blog" / "english" / "people-family" / "review-exercise" / "index.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    old = """        <li><a class="active" href="./">Review Exercise</a></li>
      </ul>"""
    new = """        <li><a class="active" href="./">Review Exercise 1</a></li>
        <li><a href="../review-exercise-2/">Review Exercise 2</a></li>
      </ul>"""
    if old in text and "review-exercise-2" not in text:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    OUT2.mkdir(parents=True, exist_ok=True)
    (OUT2 / "index.html").write_text(build_page_review2(), encoding="utf-8")
    patch_topic_index()
    patch_review1_nav()
    print("Wrote", OUT2 / "index.html")
    print("Patched people-family/index.html with Review 1 + Review 2")


if __name__ == "__main__":
    main()
