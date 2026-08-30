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
    ]


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
        _note(
            "Past perfect — form",
            items=[
                _chk(
                    full,
                    "You need ‘had’ or ‘hadn’t’ plus a past participle. For example, ‘had gone’, ‘hadn’t prepared’, and so on.",
                ),
            ],
        ),
        _note(
            "Past perfect examples from the wedding dialogue",
            items=[
                _chk(full, "they had booked a hall for the ceremony"),
                _chk(full, "They’d booked a restaurant for the reception"),
                _chk(full, "they hadn’t told them how many people were coming"),
                _chk(full, "no one had prepared their speeches"),
            ],
        ),
        _note(
            "Past perfect — form & meaning",
            intro="Form: <strong>had / hadn’t + past participle</strong>. Use when you need the <em>past in the past</em> — something before another past time.",
            items=[
                ("Form", "had + past participle — <em>had booked</em> · <em>hadn’t prepared</em>"),
                ("Earlier past", _chk(full, "They had booked a hall for the ceremony, but it was much too small.")),
                ("Timeline", "preparations (had…) → wedding day (past simple)"),
            ],
            formula=True,
        ),
        _note(
            "Bear in the forest — story excerpt",
            items_verbatim=[
                _chk(full, "My Dad had told me that there were bears in the forest, but I didn’t really take him seriously."),
                _chk(full, "I had never seen such a big animal in the wild before."),
                _chk(full, "I remembered something I had read about bears: you should stay calm and try to move away slowly."),
            ],
            speaker="Oli",
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
        _note(
            "When past perfect is NOT needed",
            tip=_chk(
                full,
                "When the order that things happened is clear, you don’t need to use the past perfect.",
            ),
            items=[
                _chk(full, "When I moved to the USA, I found a job."),
                _chk(full, "When I moved to the USA, I had found a job."),
            ],
        ),
        _note(
            "Past perfect vs past simple — meaning",
            intro="When the order of events is obvious, past simple is enough. Past perfect changes meaning when sequence matters:",
            items=[
                _chk(full, "When I moved to the USA, I found a job."),
                _chk(full, "When I moved to the USA, I had found a job."),
            ],
            tip="First = moved then found job. Second = found job before moving.",
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
