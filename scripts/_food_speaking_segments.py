"""Transcript ↔ grammar-note segments for Section 3 (Food review).

All dialogue text is extracted verbatim from Oxford Online English YouTube
captions in IELTS/SPEAKING/spoken-english-lessons/_raw/*.txt
"""

from __future__ import annotations

import re
from pathlib import Path

RAW_DIR = (
    Path(__file__).resolve().parents[3]
    / "IELTS"
    / "SPEAKING"
    / "spoken-english-lessons"
    / "_raw"
)

TRANSCRIPT_FILES: dict[str, str] = {
    "lesson-34-how-to-talk-about-the-past-in-english": "34-how-to-talk-about-the-past-in-english.txt",
    "lesson-57-how-to-use-the-past-perfect-tense-in-english-english-grammar": (
        "57-how-to-use-the-past-perfect-tense-in-english-english-grammar.txt"
    ),
    "lesson-15-how-to-tell-a-story-in-english-using-past-tense": (
        "15-how-to-tell-a-story-in-english-using-past-tense.txt"
    ),
    "lesson-23-future-in-english-how-to-talk-about-the-future": (
        "23-future-in-english-how-to-talk-about-the-future.txt"
    ),
    "lesson-61-how-to-add-emphasis-in-english-improve-your-spoken-english": (
        "61-how-to-add-emphasis-in-english-improve-your-spoken-english.txt"
    ),
}

_cache: dict[str, str] = {}


def load_transcript(slug: str) -> str:
    if slug not in _cache:
        fname = TRANSCRIPT_FILES[slug]
        raw = (RAW_DIR / fname).read_text(encoding="utf-8")
        _cache[slug] = re.sub(r"\s+", " ", raw).strip()
    return _cache[slug]


def _chk(full: str, text: str, label: str = "") -> str:
    if text not in full:
        raise ValueError(f"Transcript mismatch{f' ({label})' if label else ''}: {text[:72]!r}…")
    return text


def _dlg(full: str, pairs: list[tuple[str, str]], label: str = "") -> list[dict]:
    lines = []
    for speaker, text in pairs:
        _chk(full, text, label)
        lines.append({"speaker": speaker, "text": text})
    return lines


def _note(title: str, **kwargs) -> dict:
    return {"type": "note", "title": title, **kwargs}


def _tx(title: str, lines: list[dict]) -> dict:
    return {"type": "transcript", "title": title, "lines": lines}


def _fw(word: str) -> str:
    return f'<em class="lr-food-word">{word}</em>'


def _food_tx(title: str, pairs: list[tuple[str, str]]) -> dict:
    """Practice dialogue — same grammar as the video, food topic. Not from the clip."""
    return {
        "type": "transcript",
        "food": True,
        "title": title,
        "lines": [{"speaker": s, "text": t} for s, t in pairs],
    }


def _food_note(title: str, **kwargs) -> dict:
    return {"type": "note", "food": True, "title": title, **kwargs}


def _viz(title: str, html: str, **kwargs) -> dict:
    """Grammar slide — visual timeline / compare (Lesson 57 Past Perfect)."""
    return {"type": "note", "title": title, "visual_html": html, **kwargs}


def _m(text: str) -> str:
    return f'<mark class="lr-pp-hl">{text}</mark>'


def build_lesson_34(full: str) -> list[dict]:
    return [
        _tx(
            "Extreme sports — experiences",
            _dlg(
                full,
                [
                    ("A", "Have you ever been bungee jumping?"),
                    ("B", "No, I haven’t. I’ve been skydiving, though."),
                    (
                        "A",
                        "What about you? Have you ever done any extreme sports like that?",
                    ),
                    (
                        "B",
                        "Does windsurfing count? I’ve tried windsurfing, although that was a long time ago.",
                    ),
                    (
                        "A",
                        "I think windsurfing definitely counts! I’ve seen people doing it and they were going at crazy speeds. I’ve never done anything like that myself. Skydiving sounds very extreme to me.",
                    ),
                    ("B", "Where did you do it?"),
                    (
                        "A",
                        "It was in Spain. I did a tandem jump. It was fun, but I’m not sure I’d do it again.",
                    ),
                ],
                "extreme sports",
            ),
        ),
        _note(
            "Talking about past experiences — present perfect",
            intro="Use the <strong>present perfect</strong> to talk or ask about experiences — only when you <strong>don’t say a time</strong>.",
            items=[
                _chk(full, "I’ve tried windsurfing."),
                _chk(full, "I’ve never been bungee jumping."),
                _chk(full, "Have you ever been skydiving?"),
            ],
        ),
        _note(
            "Talking about past experiences — more examples",
            items=[
                _chk(full, "I’ve read ‘The Idiot’."),
                _chk(full, "I’ve never drunk whisky."),
                _chk(full, "Have you ever grown your own vegetables?"),
            ],
        ),
        _food_tx(
            "Unusual food — present perfect",
            [
                ("A", f"Have you ever tried {_fw('oysters')}?"),
                ("B", f"No, I haven’t. I’ve tried {_fw('lobster')}, though."),
                ("A", "What about you? Have you ever eaten any unusual food like that?"),
                (
                    "B",
                    f"Does {_fw('durian')} count? I’ve tried {_fw('durian')}, although that was a long time ago.",
                ),
                (
                    "A",
                    f"I think {_fw('durian')} definitely counts! I’ve never eaten anything like that myself. {_fw('Blue cheese')} sounds pretty extreme to me.",
                ),
                ("B", "Have you ever cooked something totally new?"),
                (
                    "A",
                    f"I’ve made homemade {_fw('pasta')} a few times. It’s harder than it looks!",
                ),
            ],
        ),
        _food_note(
            "Talking about past experiences — present perfect · food",
            intro="Same grammar — life experiences, <strong>no specific time</strong>. Swap in food vocab.",
            items=[
                f"I’ve tried {_fw('sushi')}.",
                f"I’ve never been to a {_fw('barbecue')}.",
                f"Have you ever grown your own {_fw('herbs')}?",
                f"I’ve never tried {_fw('sake')}.",
            ],
        ),
        _note(
            "Talking about past experiences — past simple + time",
            intro="As soon as you mention a <strong>time</strong>, switch to the <strong>past simple</strong>.",
            items=[
                'I <mark class="lr-hl">went</mark> windsurfing <mark class="lr-hl">three years ago</mark>.',
                'I <mark class="lr-hl">didn’t drink</mark> a lot <mark class="lr-hl">last year</mark>.',
                '<mark class="lr-hl">Did</mark> you <mark class="lr-hl">eat</mark> a lot of sushi <mark class="lr-hl">when you were</mark> in Japan?',
            ],
            items_verbatim=[
                _chk(full, "I went windsurfing three years ago."),
                _chk(full, "I didn’t drink a lot last year."),
                _chk(full, "Did you eat a lot of sushi when you were in Japan?"),
            ],
        ),
        _note(
            "Present perfect → past simple",
            exchange=[
                {
                    "q": '"Have you ever been to Australia?"',
                    "q_hl": ["Have", "been"],
                    "a": '"Yes, I went there two years ago, for my friend\'s wedding."',
                    "a_hl": ["went", "two years ago,"],
                },
            ],
            tip=_chk(
                full,
                "The question is present perfect, because it’s asking about experiences without mentioning a time. The answer mentions a time—two years ago—and so you need the past simple.",
            ),
        ),
        _food_tx(
            "Food trip — present perfect → past simple",
            [
                ("A", "Have you ever been to Japan?"),
                (
                    "B",
                    f"Yes — I went there two years ago. I ate {_fw('sushi')} almost every day when I was there.",
                ),
                ("A", f"Nice! Did you try {_fw('sake')}?"),
                (
                    "B",
                    f"I didn’t drink a lot last year — but I did try {_fw('ramen')} in Osaka last summer.",
                ),
            ],
        ),
        _food_note(
            "Talking about past experiences — past simple + time · food",
            intro="Mention a time → switch to <strong>past simple</strong>.",
            items=[
                f'I <mark class="lr-hl">tried</mark> {_fw("Korean BBQ")} <mark class="lr-hl">last month</mark>.',
                f'I <mark class="lr-hl">didn’t eat</mark> much {_fw("fast food")} <mark class="lr-hl">last year</mark>.',
                f'<mark class="lr-hl">Did</mark> you <mark class="lr-hl">eat</mark> a lot of {_fw("sushi")} <mark class="lr-hl">when you were</mark> in Japan?',
            ],
            exchange=[
                {
                    "q": '"Have you ever tried pho?"',
                    "q_hl": ["Have", "tried"],
                    "a": '"Yes, I had it three years ago in Hanoi — it melted in my mouth."',
                    "a_hl": ["had", "three years ago"],
                },
            ],
        ),
        _tx(
            "Comparing past and present — used to dialogue",
            _dlg(
                full,
                [
                    ("A", "Wow! You used to have a beard? You look so different!"),
                    ("B", "Yeah! That was during my punk rock phase."),
                    ("A", "Really? Did you use to be in a band or something?"),
                    ("B", "Yes, but it wasn’t anything big."),
                    (
                        "B",
                        "There were a few of us who were all mates, and we would play in pubs or small clubs.",
                    ),
                    ("A", "So, what were you? Singer? Guitar?"),
                    ("B", "Drummer! I used to play the drums."),
                    ("A", "And now? You don’t play any more?"),
                    ("B", "No, I gave up."),
                ],
                "used to",
            ),
        ),
        _note(
            "Comparing past and present — used to",
            intro="Something was true in the <strong>past</strong>, but isn’t true <strong>now</strong>.",
            items=[
                _chk(full, "He used to have a beard."),
                _chk(full, "I used to live in Berlin."),
            ],
        ),
        _note(
            "Comparing past and present — didn’t use to",
            intro="Things that <strong>weren’t true</strong> in the past, but <strong>are true now</strong>.",
            items=[
                'They <mark class="lr-hl">didn’t use to</mark> get on so well.',
                'I <mark class="lr-hl">didn’t use to</mark> wear glasses.',
            ],
            items_verbatim=[
                _chk(full, "They didn’t use to get on so well."),
                _chk(full, "I didn’t use to wear glasses."),
            ],
        ),
        _note(
            "Comparing past and present — questions",
            items=[
                _chk(full, "Did you use to play a musical instrument?"),
                _chk(full, "Didn’t he use to work here?"),
            ],
        ),
        _note(
            "would — past habits",
            intro="Actions or habits you did in the past, but don’t do now.",
            items=[
                _chk(
                    full,
                    "When we got home, Mum would make us beans on toast and then we’d watch cartoons.",
                ),
                _chk(
                    full,
                    "There was this bakery near the office where I would go every lunchtime to get a sandwich and chat to the other regulars.",
                ),
            ],
        ),
        _note(
            "any more",
            intro="Present verb + <strong>any more</strong> — similar meaning to <em>used to</em>.",
            items=[
                _chk(full, "She doesn’t live here any more."),
                _chk(full, "I don’t have time to listen to music any more."),
            ],
        ),
        _food_tx(
            "Childhood food — used to / would / any more",
            [
                ("A", f"Wow! You used to hate {_fw('vegetables')}? You look so health-conscious now!"),
                ("B", f"Yeah! That was during my {_fw('fast food')} phase."),
                ("A", f"Really? Did you use to eat {_fw('junk food')} every day?"),
                (
                    "B",
                    f"When I was a child, Mum would make us {_fw('pho')}, and we would eat {_fw('ice cream')} after school.",
                ),
                ("A", f"And now? You don’t eat {_fw('fast food')} any more?"),
                (
                    "B",
                    f"I don’t have {_fw('junk food')} any more. I’d rather have a {_fw('vegetable salad')} or {_fw('fruit salad')}.",
                ),
            ],
        ),
        _food_note(
            "Comparing past and present · food",
            intro="Same structures — childhood eating habits vs now.",
            items=[
                f"I <mark class='lr-hl'>used to</mark> hate {_fw('vegetables')} — now I love a good {_fw('vegetable salad')}.",
                f"They <mark class='lr-hl'>didn’t use to</mark> get on with {_fw('spicy food')} — now they order {_fw('curry')} every week.",
                f"When we got home, Mum <mark class='lr-hl'>would</mark> make us {_fw('pho')} and then we’d watch cartoons.",
                f"I don’t eat {_fw('processed food')} <mark class='lr-hl'>any more</mark>.",
            ],
        ),
        _tx(
            "Telling a story — setting the scene",
            _dlg(
                full,
                [
                    ("A", "Oh! Have I told you what happened to us on our trip?"),
                    ("B", "No! What happened?"),
                    ("A", "It’s a really crazy story."),
                    ("A", "So, we were sitting on the bus, ready to leave…"),
                    ("B", "Where were you going?"),
                    ("A", "Sofia."),
                    (
                        "A",
                        "Anyway, the weather was awful. It was raining so hard you couldn’t even see out of the window, and…",
                    ),
                    ("B", "Who were you travelling with?"),
                    (
                        "A",
                        "With my wife. We were planning to visit some old friends who…",
                    ),
                    ("B", "Where was the bus leaving from?"),
                    ("A", "From Athens."),
                    ("A", "Look, can I tell my story, or not?"),
                    ("B", "Oh, sorry…"),
                ],
                "bus story",
            ),
        ),
        _note(
            "Past continuous — set the scene",
            intro="Describe the background at the start — who was there and what was happening.",
            items=[
                _chk(full, "We were sitting on the bus, ready to leave."),
                _chk(
                    full,
                    "It was raining so hard you couldn’t even see out of the window.",
                ),
                _chk(full, "I was living in a small apartment at the time."),
                _chk(full, "I was driving home after work."),
            ],
            tip="Useful for longer answers in a job interview or IELTS — not only long stories.",
        ),
        _food_tx(
            "Kitchen story — past continuous",
            [
                ("A", "Have I told you what happened at the dinner party?"),
                ("B", "No! What happened?"),
                (
                    "A",
                    f"So, we were sitting in the kitchen, ready to {_fw('grill')} the {_fw('ribs')}…",
                ),
                ("B", "Who were you cooking with?"),
                (
                    "A",
                    f"With my sister. I was {_fw('chopping')} {_fw('garlic')} and {_fw('ginger')}, and she was {_fw('marinating')} the meat, and…",
                ),
                ("B", "And then?"),
                (
                    "A",
                    f"The weather was awful. It was raining so hard we couldn’t even use the {_fw('barbecue')} outside.",
                ),
            ],
        ),
        _food_note(
            "Past continuous — set the scene · food",
            items=[
                f"I was {_fw('chopping')} vegetables when the guests arrived.",
                f"We were {_fw('grilling')} {_fw('kebab')} in the garden.",
                f"I was living on {_fw('instant noodles')} at the time.",
            ],
        ),
        _tx(
            "Driving test story",
            _dlg(
                full,
                [
                    ("A", "Did I tell you about my driving test?"),
                    ("B", "No, what happened?"),
                    ("A", "I passed!"),
                    (
                        "A",
                        "You know, I took it last week, and I hadn’t taken any lessons. Not one!",
                    ),
                    ("B", "No way! But, you must have practiced at least?"),
                    ("A", "No! I had only driven a car twice in my life"),
                    ("B", "How on earth did you pass?"),
                    (
                        "A",
                        "It was rush hour. We drove out of the test centre, and then we sat in a traffic jam. All of the streets were totally stuck. I made three left turns, and finally we arrived back at the test centre. I just drove around the block once!",
                    ),
                    ("B", "And that counts as a pass?"),
                    ("A", "Hey, I didn’t make any mistakes."),
                    ("B", "So what happened next? Did you drive home?"),
                    ("A", "Well…"),
                    ("B", "What happened?"),
                    (
                        "A",
                        "I tried, and I had a very small accident. I mean, I don’t think it even counts as an accident.",
                    ),
                    ("B", "Maybe you should take some driving lessons."),
                    ("A", "Very funny."),
                ],
                "driving test",
            ),
        ),
        _note(
            "Time reference — fix when the story starts",
            items=[
                _chk(full, "Last week…"),
                _chk(full, "This happened two years ago, in summer."),
                _chk(full, "So, yesterday, I was walking down the street…"),
            ],
            tip="A time reference ‘fixes’ when your story starts — then you can talk about events before and after that point.",
        ),
        _note(
            "Past perfect — before the story starts",
            intro="Use <strong>had + past participle</strong> for things that happened <em>before</em> the story’s starting point.",
            items=[
                _chk(full, "I hadn’t taken any driving lessons."),
                _chk(full, "I had only driven a car twice in my life."),
                _chk(
                    full,
                    "When I was 25, I quit my job and decided to train as a pilot. I had always wanted to learn to fly.",
                ),
            ],
        ),
        _note(
            "Past simple — events in the story",
            intro="For what happens <em>during</em> the story (after the starting point), use the past simple.",
            items=[
                _chk(full, "We drove out of the test centre."),
                _chk(full, "We sat in a traffic jam for ages."),
                _chk(full, "I had a small accident on the way home."),
            ],
        ),
        _food_tx(
            "Dinner disaster — past perfect vs past simple",
            [
                ("A", "Did I tell you about last week’s dinner?"),
                ("B", "No, what happened?"),
                (
                    "A",
                    f"I invited friends last Saturday, and I hadn’t {_fw('marinated')} the {_fw('ribs')} the night before. Not once!",
                ),
                ("B", "No way! But you must have cooked something?"),
                (
                    "A",
                    f"I’d never {_fw('roasted')} a whole chicken before that night. We sat in the kitchen for ages. I made three side dishes, and finally we {_fw('grilled')} everything outside instead.",
                ),
                ("B", "And that counted as a dinner party?"),
                (
                    "A",
                    f"Hey, I didn’t burn anything. Well… I had a very small accident with the {_fw('frying pan')}.",
                ),
            ],
        ),
        _food_note(
            "Past perfect vs past simple · food",
            intro="Time reference fixes the story start. <strong>had + PP</strong> = before that; past simple = events in the story.",
            items=[
                f"I <mark class='lr-pp-hl'>had never tasted</mark> {_fw('blue cheese')} before that trip.",
                f"I <mark class='lr-hl'>hadn’t marinated</mark> the meat the night before.",
                f"We <mark class='lr-hl'>grilled</mark> the {_fw('ribs')} outside instead.",
            ],
        ),
        _tx(
            "Regrets — languages",
            _dlg(
                full,
                [
                    ("A", "Do you speak any other languages?"),
                    ("B", "Not really. I used to speak Spanish, but I haven’t used it for years."),
                    (
                        "B",
                        "I wish I’d started learning other languages when I was younger. It’s so much easier if you start earlier.",
                    ),
                    ("A", "Yeah, I know what you mean. If only I’d kept my Spanish going…"),
                    ("A", "Why don’t you pick it up again? It’d come back."),
                    ("B", "Maybe…"),
                    (
                        "B",
                        "You know what, though? I wish I’d spent some time in Latin America when I had the chance.",
                    ),
                    (
                        "B",
                        "I could have lived there for a year or two, and my Spanish would have got really good.",
                    ),
                    ("A", "Well, you could still do it, right?"),
                ],
                "languages",
            ),
        ),
        _note(
            "wish + past perfect",
            intro="Talk about something you <strong>regret</strong> — often the opposite of what really happened.",
            items=[
                _chk(full, "I wish I’d learned other languages when I was younger."),
                _chk(full, "I wish I hadn’t said that."),
            ],
        ),
        _note(
            "if only + past perfect",
            items=[
                _chk(full, "If only I’d kept my Spanish going."),
                _chk(full, "If only I hadn’t wasted so much time."),
            ],
        ),
        _note(
            "could have — regrets",
            items=[
                _chk(full, "I could have tried harder."),
                _chk(
                    full,
                    "If I hadn’t left things to the last minute, I could have passed easily.",
                ),
            ],
        ),
        _food_tx(
            "Food regrets — wish / if only / could have",
            [
                ("A", "Do you cook much at home?"),
                (
                    "B",
                    f"Not really. I used to cook {_fw('pasta')} every night, but I haven’t used the {_fw('wok')} for years.",
                ),
                (
                    "B",
                    f"I wish I’d started eating {_fw('plant-based')} meals when I was younger. It’s so much easier if you start earlier.",
                ),
                ("A", f"Yeah. If only I’d kept my {_fw('low-carb diet')} going…"),
                (
                    "B",
                    f"I could have learned to make {_fw('sushi')} when I had the chance. My {_fw('nutrition')} would have got really good.",
                ),
            ],
        ),
        _food_note(
            "wish · if only · could have · food",
            items=[
                f"I wish I’d learned to cook {_fw('curry')} when I was younger.",
                f"If only I hadn’t wasted so much money on {_fw('takeout')}.",
                f"I could have tried harder with the {_fw('gluten-free diet')}.",
            ],
        ),
    ]


def _pp_viz_form() -> str:
    return f"""<div class="lr-pp-viz">
  <p class="lr-pp-rule"><strong>Form:</strong> {_m("had")} / {_m("hadn't")} + past participle</p>
  <p class="lr-pp-examples">e.g. {_m("had gone")} · {_m("hadn't prepared")} · {_m("had booked")}</p>
  <p class="lr-pp-note-sm"><code>'d</code> = had (don't confuse with <code>would</code>)</p>
</div>"""


def _pp_viz_wedding_list() -> str:
    items = [
        f"They {_m('had booked')} a hall for the ceremony.",
        f"Surely they knew how many people they {_m('had invited')}?",
        f"They{_m("'d booked")} a restaurant for the reception.",
        f'They {_m("hadn\'t told")} them how many people were coming.',
        f"No one {_m('had prepared')} their speeches.",
    ]
    lis = "\n".join(f"  <li>{x}</li>" for x in items)
    return f"""<div class="lr-pp-viz">
  <p class="lr-pp-axis-label lr-pp-axis-label--pp">past perfect = <strong>before</strong> the wedding</p>
  <ul class="lr-pp-list">{lis}
  </ul>
</div>"""


def _pp_viz_wedding_compare() -> str:
    return f"""<div class="lr-pp-viz lr-pp-viz--split">
  <p class="lr-pp-sentence">They {_m('had booked')} a hall for the ceremony... but it {_m('was')} much too small.</p>
  <div class="lr-pp-split">
    <div class="lr-pp-split-col lr-pp-split-col--pp">
      <span class="lr-pp-tag">→ past perfect</span>
      <p>= <strong>before</strong> the wedding</p>
    </div>
    <div class="lr-pp-split-col lr-pp-split-col--ps">
      <span class="lr-pp-tag">→ past simple</span>
      <p>= <strong>during</strong> the wedding</p>
    </div>
  </div>
</div>"""


def _pp_viz_during_wedding() -> str:
    return f"""<div class="lr-pp-viz">
  <p class="lr-pp-axis-label lr-pp-axis-label--ps">past simple = <strong>during</strong> the wedding</p>
  <p class="lr-pp-q"><strong>What happened?</strong></p>
  <ul class="lr-pp-list">
    <li>Everyone else {_m('had to')} wait outside. <span class="lr-pp-gloss">(modal — not past perfect)</span></li>
    <li>There {_m("wasn't")} enough food.</li>
  </ul>
</div>"""


def _pp_viz_story_timeline() -> str:
    return f"""<div class="lr-pp-viz lr-pp-viz--timeline">
  <div class="lr-pp-tl" aria-hidden="true">
    <div class="lr-pp-tl-line"></div>
    <div class="lr-pp-tl-further">
      <span class="lr-pp-dot lr-pp-dot--pp">4</span>
      <span class="lr-pp-tl-cap">further in past<br><strong>= past perfect</strong></span>
    </div>
    <div class="lr-pp-tl-story">
      <span class="lr-pp-tl-arc">Your story</span>
      <div class="lr-pp-tl-dots">
        <span class="lr-pp-dot">1</span>
        <span class="lr-pp-dot">2</span>
        <span class="lr-pp-dot">3</span>
      </div>
      <span class="lr-pp-tl-cap">past</span>
    </div>
    <span class="lr-pp-tl-now">now</span>
  </div>
  <div class="lr-pp-tl-examples">
    <p class="lr-pp-tl-hint"><strong>Past simple</strong> — one thing after another:</p>
    <ol>
      <li>I {_m('bought')} a new car.</li>
      <li>I {_m('took')} it for a drive.</li>
      <li>I {_m('crashed')} it into a tree.</li>
    </ol>
    <p class="lr-pp-tl-hint"><strong>Past perfect</strong> — before your story starts (point 4).</p>
  </div>
</div>"""


def _pp_viz_bear_story() -> str:
    return f"""<div class="lr-pp-viz lr-pp-viz--story">
  <p class="lr-pp-story">I'm going to tell you a story. This happened to me when I was twelve years old. I was on holiday with my family, and we were walking in a forest. My Dad {_m('had told')} me that there were bears in the forest, but I didn't really take him seriously. I was walking in front; I turned a corner, and… there was a bear! I {_m('had never seen')} such a big animal in the wild before. I remembered something I {_m('had read')} about bears: you should stay calm and try to move away slowly. So, I walked backwards, very slowly.</p>
  <p class="lr-pp-note-sm">3 past perfect verbs — all <strong>before</strong> the time of the story.</p>
</div>"""


def _pp_viz_teaching_timeline() -> str:
    return f"""<div class="lr-pp-viz lr-pp-viz--timeline lr-pp-viz--teach">
  <div class="lr-pp-tl" aria-hidden="true">
    <div class="lr-pp-tl-line"></div>
    <div class="lr-pp-tl-further">
      <span class="lr-pp-dot lr-pp-dot--pp">2</span>
      <span class="lr-pp-tl-cap">further in past<br>(before I started teaching)</span>
    </div>
    <div class="lr-pp-tl-story">
      <span class="lr-pp-dot lr-pp-dot--ps">1</span>
      <span class="lr-pp-tl-cap">past<br>(2005, when I started teaching)</span>
    </div>
    <span class="lr-pp-tl-now">now</span>
  </div>
  <div class="lr-pp-tl-examples">
    <p><strong>1.</strong> When {_m('did')} you start teaching?</p>
    <ul class="lr-pp-list lr-pp-list--inline">
      <li>I {_m('wanted')} to live abroad.</li>
      <li>I {_m("wasn't")} sure what I {_m('wanted')} to do.</li>
    </ul>
    <p><strong>2.</strong> (before 2005)</p>
    <ul class="lr-pp-list lr-pp-list--inline">
      <li>I {_m('had just graduated')}.</li>
      <li>I{_m("'d spent")} some time in Canada.</li>
    </ul>
    <p class="lr-pp-note-sm">Past perfect = the <strong>past in the past</strong> — further back than the time you're talking about.</p>
  </div>
</div>"""


def _pp_viz_not_needed() -> str:
    return f"""<div class="lr-pp-viz">
  <p class="lr-pp-axis-label lr-pp-axis-label--ps">past simple = <strong>during</strong> the morning / evening</p>
  <p class="lr-pp-q"><strong>What happened?</strong></p>
  <ul class="lr-pp-list">
    <li>My alarm clock {_m("didn't")} go off this morning.</li>
    <li>Why {_m('did')} you wake up so late?</li>
    <li>I probably {_m('got')} four hours of sleep.</li>
  </ul>
  <p class="lr-pp-note-sm">No past perfect in this dialogue — the order of events is already <strong>clear</strong>. Using <em>had woken up</em> sounds unnatural here.</p>
</div>"""


def _pp_viz_when_compare() -> str:
    return f"""<div class="lr-pp-viz lr-pp-viz--when">
  <div class="lr-pp-when-row">
    <p>When I moved to the USA, I {_m('found')} a job.</p>
    <p class="lr-pp-eq">= I found a job <strong>{_m('after')}</strong> I moved to the USA.</p>
  </div>
  <div class="lr-pp-when-row">
    <p>When I moved to the USA, I {_m('had found')} a job.</p>
    <p class="lr-pp-eq">= I found a job <strong>{_m('before')}</strong> I moved to the USA.</p>
  </div>
  <p class="lr-pp-note-sm">When sequence matters, past perfect is <strong>necessary</strong> — past simple changes the meaning.</p>
</div>"""


def build_lesson_57(full: str) -> list[dict]:
    return [
        _tx(
            "The wedding — what went wrong",
            _dlg(
                full,
                [
                    ("A", "How was the wedding?"),
                    ("B", "A disaster! I’ve never seen anything go so wrong."),
                    ("A", "Why? What happened?"),
                    (
                        "B",
                        "First, they had booked a hall for the ceremony, but it was much too small. Only 30 people could go in, and everyone else had to wait outside.",
                    ),
                    ("A", "Really? That’s weird."),
                    ("A", "I know! Surely they knew how many people they had invited?"),
                    ("B", "I guess not. Sounds bad."),
                    ("B", "Yes, but that’s not all."),
                    (
                        "B",
                        "They’d booked a restaurant for the reception, but they hadn’t told them how many people were coming. So, there wasn’t enough food, either!",
                    ),
                    ("A", "That’s not good."),
                    (
                        "B",
                        "And then, as if that wasn’t enough, there were so many long, boring speeches! You could tell that no one had prepared their speeches, and they were just trying to improvise. It just went on and on.",
                    ),
                    ("A", "So, you’re hungry and listening to boring speeches for hours? Doesn’t sound like much fun."),
                    ("B", "It wasn’t."),
                ],
                "wedding",
            ),
        ),
        _viz("Form — had / hadn't + past participle", _pp_viz_form()),
        _viz("Past perfect = before the wedding", _pp_viz_wedding_list()),
        _viz("One sentence — two tenses", _pp_viz_wedding_compare()),
        _viz("Past simple = during the wedding", _pp_viz_during_wedding()),
        _viz("Timeline — your story vs further in the past", _pp_viz_story_timeline()),
        _viz("Bear story — past perfect in narrative", _pp_viz_bear_story()),
        _food_tx(
            "Wedding buffet — past perfect",
            [
                ("A", "How was the wedding dinner?"),
                ("B", "A disaster! I’ve never seen a buffet go so wrong."),
                ("A", "Why? What happened?"),
                (
                    "B",
                    f"First, they had booked a tiny hall, but they’d ordered {_fw('lobster')} and {_fw('oysters')} for 200 people. Only 30 could sit inside.",
                ),
                (
                    "B",
                    f"They’d booked a restaurant for the reception, but they hadn’t told them how many people were coming. So there wasn’t enough {_fw('seafood')} either!",
                ),
                (
                    "A",
                    f"And the {_fw('cheesecake')}? Had anyone even {_fw('marinated')} the meat?",
                ),
                (
                    "B",
                    f"You could tell that no one had prepared the {_fw('speeches')} — or the {_fw('mustard')} and {_fw('soy sauce')} for the table.",
                ),
            ],
        ),
        _food_note(
            "Past perfect — form & meaning · food",
            intro="had / hadn’t + past participle — food events <em>before</em> the meal.",
            items=[
                f"They <mark class='lr-pp-hl'>had booked</mark> a restaurant, but it was much too small.",
                f"They <mark class='lr-pp-hl'>hadn't told</mark> the chef how many guests were coming.",
                f"I <mark class='lr-pp-hl'>had never tasted</mark> {_fw('blue cheese')} before that dinner.",
            ],
        ),
        _tx(
            "When did you start teaching?",
            _dlg(
                full,
                [
                    ("A", "When did you start teaching?"),
                    (
                        "B",
                        "Actually, it was kind of an accident. It was 2005. I had just graduated, and I wasn’t sure what I wanted to do. So, I took a six-month teaching job, mostly because I wanted to live abroad and travel a bit.",
                    ),
                    ("A", "So, you didn’t want to teach?"),
                    ("B", "Not really! I had never considered it as a career."),
                    ("A", "Where did you move to?"),
                    (
                        "B",
                        "Russia. I had studied a little bit of Russian at university, but not enough to really be able to do anything. So, I wanted to learn more, and also just experience living in Russia.",
                    ),
                    ("A", "Had you ever lived abroad before?"),
                    (
                        "B",
                        "Briefly. I’d spent some time in Canada, but this was more challenging.",
                    ),
                ],
                "teaching",
            ),
        ),
        _viz("Timeline — teaching (2005)", _pp_viz_teaching_timeline()),
        _note(
            "Past perfect in conversation",
            tip=_chk(
                full,
                "You use it when you’re already talking about the past, and you want to refer to something which is *further* in the past.",
            ),
            items=[
                _chk(full, "I had just graduated, and I wasn’t sure what I wanted to do."),
                _chk(full, "I had never considered it as a career."),
                _chk(full, "I had studied a little bit of Russian at university, but not enough to really be able to do anything."),
            ],
        ),
        _food_tx(
            "First cooking job — past in the past",
            [
                ("A", "When did you start cooking professionally?"),
                (
                    "B",
                    f"It was 2018. I had just graduated, and I wasn’t sure what I wanted to do. So I took a six-month job in a {_fw('kebab')} shop.",
                ),
                ("A", "So you didn’t want to be a chef?"),
                (
                    "B",
                    f"Not really! I had never considered it as a career. I had studied a little {_fw('nutrition')} at university, but not enough to run a kitchen.",
                ),
                ("A", "Had you ever lived abroad before?"),
                (
                    "B",
                    f"Briefly. I’d spent some time in Thailand — that’s where I first tried {_fw('curry')} and {_fw('shellfish')}.",
                ),
            ],
        ),
        _food_note(
            "Past perfect in conversation · food",
            items=[
                f"I had just graduated, so I took a job making {_fw('baguettes')}.",
                f"I had never considered {_fw('plant-based')} cooking as a career.",
                f"I had studied a little {_fw('nutrition')}, but not enough to be a chef.",
            ],
        ),
        _tx(
            "Late for work — when NOT to use past perfect",
            _dlg(
                full,
                [
                    ("A", "Were you late for work *again*?"),
                    ("B", "Yeah… What happened?"),
                    ("A", "My alarm clock didn’t go off this morning."),
                    ("A", "So what time did you get there?"),
                    ("B", "Around eleven."),
                    ("A", "Eleven?! Why did you wake up so late?"),
                    ("B", "I couldn’t fall asleep last night. I probably got four hours of sleep."),
                    ("A", "Did you go to bed late?"),
                    ("B", "Not really. I think it was around twelve."),
                ],
                "late for work",
            ),
        ),
        _viz("Past simple only — late for work", _pp_viz_not_needed()),
        _viz("When + past perfect changes the meaning", _pp_viz_when_compare()),
        _food_note(
            "Past perfect vs past simple · food meaning",
            intro="Sequence changes the meaning:",
            items=[
                f"When I moved to Italy, I found a job in a {_fw('pasta')} kitchen. → moved first, then the job.",
                f"When I moved to Italy, I <mark class='lr-hl'>had found</mark> a job. → job first, then the move.",
            ],
        ),
    ]


def build_lesson_15(full: str) -> list[dict]:
    return [
        _tx(
            "Intro — why stories matter",
            _dlg(
                full,
                [
                    (
                        "Gina",
                        "Hi, I’m Gina. Welcome to Oxford Online English! In this lesson, you can learn how to tell a story in English.",
                    ),
                    (
                        "Gina",
                        "Stories are powerful. When you meet someone new, go to a job interview or take a speaking exam like IELTS, you need to tell stories, whether you realise that’s what you’re doing or not.",
                    ),
                ],
                "intro",
            ),
        ),
        _note(
            "Step 1 · Background",
            intro="Start with <strong>who · when · where · what</strong>. Add 1–2 detail sentences — don’t drag.",
            items=[
                _chk(full, "It was summer, and I went with some friends to a beach in Crimea which you could only get to by boat."),
                _chk(full, "At university, I shared a flat with three other guys."),
            ],
        ),
        _food_tx(
            "Meal story — step 1 background",
            [
                (
                    "A",
                    f"It was last month, and I invited some friends over for {_fw('ribs')} and a {_fw('vegetable salad')}.",
                ),
                (
                    "B",
                    f"At university, I shared a flat with three other guys who lived on {_fw('instant noodles')} and {_fw('donuts')}.",
                ),
            ],
        ),
        _food_note(
            "Step 1 · Background · food",
            intro="who · when · where · what — for a meal story.",
            items=[
                f"It was last Sunday, and I {_fw('grilled')} {_fw('kebab')} in the garden with my cousins.",
                f"At university, I shared a kitchen with three other guys.",
            ],
        ),
        _tx(
            "Story 1 — opening & background",
            _dlg(
                full,
                [
                    (
                        "Gina",
                        "It was summer, and I went with some friends to a beach in Crimea which you could only get to by boat.",
                    ),
                    (
                        "Gina",
                        "People had been going there for years, and there were benches and tables, places to camp, fire places and so on. It was kind of a hippy place, with everyone walking around naked and doing whatever they felt like.",
                    ),
                ],
                "crimea",
            ),
        ),
        _note(
            "Step 2 · Goal",
            intro="What did the people in the story <strong>want</strong>?",
            items=[
                _chk(full, "On the last day, we had to catch a train in the evening."),
                _chk(
                    full,
                    "To reach Issyk-Kul lake, which was the end of my journey, I had to cross a mountain pass, almost 4,000m high.",
                ),
            ],
        ),
        _food_note(
            "Step 2 · Goal · food",
            items=[
                f"We had to finish {_fw('roasting')} the chicken before the guests arrived.",
                f"I had to cross the market to buy {_fw('oysters')} before the stall closed.",
            ],
        ),
        _tx(
            "Story 2 — tension (mountain pass)",
            _dlg(
                full,
                [
                    (
                        "Gina",
                        "On the third day, I had to cross a mountain pass, almost 4,000m high. It was so hard, because the air is thin up there and I was carrying a very heavy pack.",
                    ),
                    (
                        "Gina",
                        "It seemed to take forever, but finally I got close to the top… and then a storm boiled over the ridge and landed right on my head. There was lightning all around me, even below me! The noise was unbelievable.",
                    ),
                ],
                "mountain",
            ),
        ),
        _note(
            "Step 3 · Tension",
            intro="The goal must not be too easy. Listeners should wonder: <em>what’s going to happen?</em>",
            items=[
                "Problems or difficulties before the climax",
                "Foreshadowing — e.g. I told them not to do anything to my room. I knew they were going to do something.",
            ],
        ),
        _food_tx(
            "Meal story — tension",
            [
                (
                    "A",
                    f"The oven broke. The {_fw('ribs')} weren’t ready, the guests were at the door, and we still had to {_fw('chop')} the {_fw('herbs')}.",
                ),
                (
                    "B",
                    f"I knew something would go wrong — I told them not to touch my {_fw('cheesecake')}. I knew they were going to do something…",
                ),
            ],
        ),
        _food_note(
            "Step 3 · Tension · food",
            items=[
                "Broken oven / missing ingredient / rain on the barbecue",
                f"Foreshadowing: I told them not to touch my {_fw('cheesecake')}. I knew they were going to do something.",
            ],
        ),
        _tx(
            "Story 3 — flatmates prank (tension)",
            _dlg(
                full,
                [
                    (
                        "Gina",
                        "One weekend, I was going home to visit my parents. I said bye to my flatmates, and told them not to do anything to my room.",
                    ),
                    ("Gina", "“Don’t worry, we won’t. Have a good weekend,” they said."),
                    (
                        "Gina",
                        "I knew they were going to do something, but I couldn’t believe what they actually did:",
                    ),
                ],
                "flatmates",
            ),
        ),
        _tx(
            "Endings — resolve tension",
            _dlg(
                full,
                [
                    (
                        "Gina",
                        "We loaded our stuff onto a kayak and swam almost a kilometre around the cliffs. A naked hippy paddled the kayak, which was piled high with our things and looked like it could sink at any minute. We made it to land, and after several hours of hitchhiking and walking, we caught our train.",
                    ),
                    (
                        "Gina",
                        "It was stressful at the time, but looking back now it makes a good story!",
                    ),
                    (
                        "Gina",
                        "They made my room into a jungle! I’m not kidding: there were flowers, plants, three whole trees, jungle animals made from paper, and a ‘sounds of the forest’ mix playing on my stereo.",
                    ),
                ],
                "endings",
            ),
        ),
        _note(
            "Step 4 · Ending + retrospective comment",
            items=[
                "Resolve the tension — answer what happened",
                _chk(full, "It was stressful at the time, but looking back now it makes a good story!"),
                _chk(full, "It was a very frightening experience."),
            ],
        ),
        _food_tx(
            "Meal story — ending",
            [
                (
                    "A",
                    f"We {_fw('grilled')} everything outside instead. Looking back, it was stressful at the time, but it makes a good story!",
                ),
                (
                    "B",
                    f"They made my fridge into a {_fw('dessert')} shop — {_fw('cupcakes')}, {_fw('pudding')}, even a {_fw('popsicle')} tower. It took me three hours to clean up.",
                ),
            ],
        ),
        _food_note(
            "Step 4 · Ending · food",
            items=[
                f"Looking back, it was one of the best {_fw('barbecues')} I’d ever shared with friends.",
                f"In the end, we {_fw('grilled')} outside — and it tasted even better.",
            ],
        ),
    ]


def build_lesson_23(full: str) -> list[dict]:
    return [
        _tx(
            "This weekend — present continuous plans",
            _dlg(
                full,
                [
                    ("Martin", "What are you doing this weekend?"),
                    (
                        "B",
                        "I’m meeting some friends for lunch on Saturday, and then we’re going to the theatre.",
                    ),
                    ("Martin", "Sounds good! What about Sunday?"),
                    ("B", "Not sure. I don’t have plans yet."),
                    ("Martin", "What about you—doing anything fun?"),
                    ("A", "I’m going away for the weekend."),
                    ("Martin", "Really? Nice! Where are you going?"),
                    ("A", "Berlin! I found some cheap flights."),
                ],
                "weekend",
            ),
        ),
        _note(
            "Present continuous — fixed plans",
            intro="Use present continuous for the future when you know <strong>when / where</strong>.",
            items=[
                _chk(full, "What are you doing tomorrow?"),
                _chk(
                    full,
                    "I’m working in the morning, then I’m playing football in the park with some friends.",
                ),
            ],
        ),
        _food_tx(
            "Weekend food plans — present continuous",
            [
                ("A", "What are you doing this weekend?"),
                (
                    "B",
                    f"I’m meeting some friends for {_fw('brunch')} on Saturday — {_fw('croissants')} and {_fw('latte')} — and then we’re going to a {_fw('barbecue')}.",
                ),
                ("A", "Sounds good! What about Sunday?"),
                (
                    "B",
                    f"I’m cooking {_fw('pasta')} in the evening. What about you?",
                ),
                (
                    "A",
                    f"I’m going to a {_fw('cooking class')} on Sunday morning.",
                ),
            ],
        ),
        _food_note(
            "Present continuous — food plans",
            items=[
                f"I’m meeting friends for {_fw('lunch')} on Saturday.",
                f"I’m trying a {_fw('low-carb diet')} this month.",
            ],
        ),
        _tx(
            "Holiday plans — Egypt",
            _dlg(
                full,
                [
                    ("A", "Are you going anywhere next summer?"),
                    ("B", "We’re going to Cornwall. It’s the same place we go every year."),
                    ("A", "I’ve heard it’s beautiful there! How long are you staying there?"),
                    ("B", "Just a week."),
                    ("A", "Are you going in July?"),
                    ("B", "No, we’re going in August."),
                    ("A", "Who are you going with?"),
                    ("B", "I’m going with two old college friends."),
                ],
                "cornwall",
            ),
        ),
        _note(
            "Planning to · going to · I'd like to",
            items=[
                _chk(full, "I’m going to Egypt for 10 days with a group of friends."),
                _chk(
                    full,
                    "We’re planning to do some sightseeing around Cairo, then we’re going to do a boat trip on the Nile.",
                ),
                _chk(full, "I’d like to start my own business."),
                _chk(full, "My dream is to have my own small marketing firm."),
            ],
        ),
        _food_tx(
            "Food dreams — going to / I'd like to",
            [
                ("A", "What are you going to do after you graduate?"),
                (
                    "B",
                    f"I’m planning to take a {_fw('nutrition')} course. I’d like to start my own small {_fw('café')} one day.",
                ),
                (
                    "B",
                    f"My dream is to live near the sea and cook {_fw('seafood')} every day. I’m hoping to start with {_fw('freelancing')} as a food writer.",
                ),
            ],
        ),
        _food_note(
            "going to / planning to / I'd like to · food",
            items=[
                f"I’m planning to try a {_fw('gluten-free diet')} next month.",
                f"I’d like to learn to cook {_fw('Thai curry')} one day.",
                f"My dream is to open a small {_fw('café')} near the sea.",
            ],
        ),
        _tx(
            "Quitting work — dreams & plans",
            _dlg(
                full,
                [
                    ("A", "Is it true? You quit?"),
                    ("B", "Yes! I’m done with this place, and it feels great!"),
                    ("A", "What are you going to do now?"),
                    (
                        "B",
                        "You know, first of all I’m planning to take some time to rest and recover my energy. I’ve been so stressed the last few months.",
                    ),
                    ("A", "Sure, but then how are you going to find a new job?"),
                    ("B", "Actually, I’d like to start my own business. I’m tired of working for other people."),
                    ("A", "Really? What kind of thing are you thinking of doing?"),
                    (
                        "B",
                        "My dream is to have my own small marketing firm. I’m hoping to start with freelancing, and then build up from there.",
                    ),
                    ("A", "Wow—good luck!"),
                ],
                "quit",
            ),
        ),
        _tx(
            "Concert & bus timetable",
            _dlg(
                full,
                [
                    ("A", "What time does the concert start?"),
                    ("B", "8.00, so we need to leave at 6.30."),
                    ("A", "Is there a bus?"),
                    (
                        "B",
                        "Yeah, I think it leaves at 6.45, and it gets there around 7.30.",
                    ),
                    ("A", "What time does it finish?"),
                    ("B", "It’s supposed to end at ten."),
                    (
                        "B",
                        "The last bus back leaves at 10.15, so we’ll have to hurry.",
                    ),
                ],
                "concert",
            ),
        ),
        _note(
            "Present simple — timetables",
            items=[
                _chk(full, "What time does the concert start?"),
                _chk(full, "The bus gets there around 7.30."),
                _chk(full, "Our class starts at eleven thirty."),
            ],
        ),
        _food_note(
            "Present simple — food timetables",
            items=[
                f"The {_fw('cooking class')} starts at eleven thirty.",
                f"The last {_fw('food delivery')} leaves at ten fifteen.",
                f"The wedding lunch is at three.",
            ],
        ),
        _tx(
            "World Cup predictions",
            _dlg(
                full,
                [
                    ("Martin", "At the beginning: who’s going to win the next World Cup?"),
                    ("A", "Italy will win."),
                    ("B", "I hope Russia will win, but I don’t think they actually will."),
                    ("A", "England definitely won’t win it."),
                ],
                "world cup",
            ),
        ),
        _note(
            "will / going to — predictions",
            items=[
                _chk(full, "It’s going to rain—look at those clouds."),
                "will and going to are often interchangeable for predictions",
            ],
        ),
        _food_tx(
            "Food trends — predictions",
            [
                ("A", "Who’s going to win the next food awards?"),
                (
                    "B",
                    f"People will eat more {_fw('plant-based')} food. {_fw('Fast food')} definitely won’t win.",
                ),
                (
                    "A",
                    f"Look at those clouds — it’s going to rain before the {_fw('barbecue')}.",
                ),
            ],
        ),
        _food_note(
            "will / going to — food predictions",
            items=[
                f"People will eat more {_fw('plant-based')} food.",
                f"It’s going to rain — look at those clouds. We’ll have to cancel the {_fw('barbecue')}.",
            ],
        ),
        _tx(
            "Marathon predictions",
            _dlg(
                full,
                [
                    ("A", "So, do you think they’ll do it?"),
                    ("B", "Michelle will definitely do it."),
                    ("A", "There’s no chance Andy is going to finish."),
                    (
                        "A",
                        "He doesn’t look like he can run to the bus stop, so I can’t believe he’ll run 26 miles.",
                    ),
                    (
                        "B",
                        "He’s unlikely to get a fast time, but I’m pretty sure he’ll do it.",
                    ),
                    ("A", "Well, anyway, we can agree that Michelle is sure to be much faster!"),
                    ("B", "Yeah, of course."),
                    ("A", "Do you think she’ll do it in under three hours?"),
                    ("B", "It’s not likely that she’ll do it that fast."),
                    ("B", "But, she’s bound to get under four hours. That’s still a good time."),
                ],
                "marathon",
            ),
        ),
        _note(
            "How certain? — adverbs & phrases",
            items=[
                _chk(full, "She’ll definitely do it."),
                _chk(full, "He’s unlikely to get a fast time."),
                _chk(full, "She’s sure to be much faster."),
                _chk(full, "It’s not likely that she’ll do it that fast."),
                _chk(full, "she’s bound to get under four hours"),
            ],
        ),
        _tx(
            "Uncertainty at work",
            _dlg(
                full,
                [
                    ("A", "So, do you have any idea when you’ll have finished everything?"),
                    ("B", "It really depends. It may be ready next week if everything goes well."),
                    (
                        "B",
                        "The thing is, it’s possible that we’ll have to replace some of the artwork. That could take a few days.",
                    ),
                    ("B", "Perhaps we won’t need to change anything."),
                    ("B", "Maybe I’ll work overtime this weekend. That might help."),
                ],
                "uncertainty",
            ),
        ),
        _note(
            "may / might / could",
            items=[
                _chk(full, "It may be ready next week."),
                _chk(full, "That could take a few days."),
                _chk(full, "That might help."),
            ],
        ),
        _note(
            "perhaps / maybe · it's possible that",
            items=[
                _chk(full, "Perhaps we won’t need to change anything."),
                _chk(full, "Maybe I’ll work overtime this weekend."),
                _chk(full, "It’s possible that we’ll have to replace some of the artwork."),
            ],
        ),
        _food_tx(
            "Dinner plans — uncertainty",
            [
                ("A", "Will the new menu be ready next week?"),
                (
                    "B",
                    f"It may be ready — or it could take a few more days. I might order {_fw('takeout')} tonight.",
                ),
                (
                    "A",
                    f"Perhaps we won’t need to change the {_fw('dessert')}. It’s possible that we’ll have to replace some recipes.",
                ),
            ],
        ),
        _food_note(
            "may / might / could · food",
            items=[
                f"I might order {_fw('takeout')} tonight.",
                f"Perhaps we won’t need to change the {_fw('menu')}.",
                f"It’s possible that we’ll have to replace the {_fw('cheesecake')} recipe.",
            ],
        ),
    ]


def build_lesson_61(full: str) -> list[dict]:
    return [
        _tx(
            "Word stress — John & Paris",
            _dlg(
                full,
                [
                    ("A", "What time is John flying to Paris tomorrow?"),
                    ("B", "He isn’t flying to Paris *tomorrow.*"),
                    ("A", "What time is John flying to Paris tomorrow?"),
                    ("B", "He isn’t *flying* to Paris tomorrow."),
                    ("A", "What time is John flying to Paris tomorrow?"),
                    ("B", "*He* isn’t flying to Paris tomorrow."),
                ],
                "paris stress",
            ),
        ),
        _note(
            "Word stress — contrast & correction",
            tip=_chk(
                full,
                "Adding word stress is a simple way to add emphasis to your idea. This is especially useful when you want to correct someone, or disagree with somebody else.",
            ),
        ),
        _note(
            "Word stress — what it means",
            intro="Stressing one word shows contrast or corrects someone. Examples from the video:",
            items=[
                "Stress <strong>tomorrow</strong> → he is flying to Paris, but not tomorrow.",
                "Stress <strong>flying</strong> → he is going to Paris tomorrow, but not by plane.",
                "Stress <strong>he</strong> → other people are flying, but he isn’t.",
            ],
        ),
        _food_tx(
            "Food — word stress",
            [
                ("A", f"Are you cooking {_fw('pasta')} tomorrow?"),
                ("B", f"I’m not cooking {_fw('pasta')} *tomorrow.* Maybe on Sunday."),
                ("A", f"So you’re *eating out* tomorrow?"),
                (
                    "B",
                    f"*He* isn’t cooking — I am. I’m making {_fw('curry')} tonight.",
                ),
            ],
        ),
        _food_note(
            "Word stress · food",
            items=[
                f"Stress <strong>tomorrow</strong> → you’re cooking, but not tomorrow.",
                f"Stress <strong>pasta</strong> → you’re cooking something, but not pasta (maybe {_fw('curry')}).",
            ],
        ),
        _tx(
            "After the movie — inversion",
            _dlg(
                full,
                [
                    ("A", "So, what did you think of the movie?"),
                    ("B", "Amazing! It was so tense!"),
                    ("A", "Yeah, I saw you jump so many times!"),
                    ("B", "I know! *Never* have I been so scared."),
                    (
                        "B",
                        "That basement scene was so frightening, I could hardly watch.",
                    ),
                    ("A", "And the ending! What a twist!"),
                    ("B", "At no point did I see that coming."),
                ],
                "movie",
            ),
        ),
        _note(
            "Inversion — Never / At no point / Not only",
            items=[
                _chk(full, "*Never* have I been so scared."),
                _chk(full, "At no point did I see that coming."),
                _chk(full, "Not only did she direct it, but she also wrote and starred in it too!"),
            ],
        ),
        _food_note(
            "Inversion · food",
            items=[
                f"*Never* have I tasted such good {_fw('pho')}.",
                f"Not only did she {_fw('roast')} the chicken, but she also made the {_fw('cheesecake')}.",
            ],
        ),
        _tx(
            "Party — do / does / did emphasis",
            _dlg(
                full,
                [
                    ("A", "You’re not coming to the party tonight, right?"),
                    ("B", "I *am* coming! Why would you think I wasn’t?"),
                    (
                        "A",
                        "Well, last time we went to their place, you were in a terrible mood. It didn’t look like you were enjoying yourself at all.",
                    ),
                    ("B", "Well, I was quite tired, but I *did* have a good time."),
                    ("A", "OK, well that’s good. I *do* hope you’re bringing Michelle with you, too?"),
                    ("B", "Yes, she’ll be there."),
                    ("A", "Is she going to make her orange cake again? That was the best!"),
                    ("B", "I’ll ask her. She *does* make the best cakes."),
                ],
                "party",
            ),
        ),
        _note(
            "Stress an auxiliary — do / does / did / am",
            items=[
                _chk(full, "I *am* coming!"),
                _chk(full, "I *did* have a good time."),
                _chk(full, "I *do* hope you’re bringing Michelle with you, too?"),
            ],
        ),
        _food_tx(
            "Spicy food — do / does / did",
            [
                ("A", f"You don’t eat {_fw('spicy food')}, do you?"),
                (
                    "B",
                    f"I *do* like {_fw('spicy food')} — but not every day. I *did* have a good time at that {_fw('curry')} place last week.",
                ),
                (
                    "A",
                    f"She *does* make the best {_fw('cheesecake')}. I *am* bringing homemade {_fw('pasta')} tonight.",
                ),
            ],
        ),
        _food_note(
            "do / does / did · food",
            items=[
                f"I <strong>do</strong> like {_fw('spicy food')}, but not every day.",
                f"I <strong>absolutely love</strong> homemade {_fw('pasta')}.",
                f"She <strong>does</strong> make the best {_fw('cakes')}.",
            ],
        ),
        _tx(
            "Broken TV — cleft sentence",
            _dlg(
                full,
                [
                    ("A", "Olivier, can you come downstairs, please?"),
                    ("B", "What’s happened?"),
                    ("A", "Look in the living room. Did you break the TV?"),
                    ("B", "I didn’t break the TV!"),
                    ("A", "Well, what happened then?"),
                    ("B", "It was the dog who did it!"),
                    (
                        "B",
                        "He ran through the living room chasing the cat and got caught on the wires.",
                    ),
                    ("A", "OK, sorry, my mistake."),
                ],
                "tv",
            ),
        ),
        _note(
            "Cleft sentences — It was… who / What… is",
            items=[
                _chk(full, "It was the dog who did it!"),
                _chk(full, "‘what I hate most about living here is the dark winters.’"),
                _chk(full, "‘What I need right now is a good long holiday.’"),
            ],
        ),
        _note(
            "Cleft sentences — all / something",
            items=[
                _chk(full, "‘All I want is to lie down. I feel terrible!’"),
                _chk(
                    full,
                    "‘Something you should think about is choosing the words you use more carefully.’",
                ),
            ],
        ),
        _food_tx(
            "Memorable meal — cleft",
            [
                ("A", "Tell me about a meal you remember."),
                (
                    "B",
                    f"It was the fresh {_fw('herbs')} that made the dish special — not the meat.",
                ),
                (
                    "A",
                    f"What I enjoy most is experimenting with {_fw('spices')} and {_fw('ginger')}.",
                ),
                (
                    "B",
                    f"All I want after work is a bowl of {_fw('pho')}. What I need right now is a good long {_fw('brunch')}.",
                ),
            ],
        ),
        _food_note(
            "Cleft sentences · food",
            items=[
                f"What I enjoy most is trying new {_fw('cuisines')}.",
                f"It was the fresh {_fw('herbs')} that made the dish special.",
                f"What I don’t like is {_fw('processed food')}.",
            ],
        ),
    ]


_BUILDERS = {
    "lesson-34-how-to-talk-about-the-past-in-english": build_lesson_34,
    "lesson-57-how-to-use-the-past-perfect-tense-in-english-english-grammar": build_lesson_57,
    "lesson-15-how-to-tell-a-story-in-english-using-past-tense": build_lesson_15,
    "lesson-23-future-in-english-how-to-talk-about-the-future": build_lesson_23,
    "lesson-61-how-to-add-emphasis-in-english-improve-your-spoken-english": build_lesson_61,
}


def build_all_segments() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for slug, builder in _BUILDERS.items():
        full = load_transcript(slug)
        out[slug] = builder(full)
    return out


# Built at import — raises if any quote is not in the source transcript.
SPEAKING_SEGMENTS: dict[str, list[dict]] = build_all_segments()
