"""Transcript ↔ grammar-note segments for Section 3 speaking videos (Food review).

Each lesson alternates dialogue blocks (teacher / A / B) with slide-style notes
so learners can catch up on the full video without rewatching.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Lesson 34 — Talk about the past (rZS5qlCGCIY)
# ---------------------------------------------------------------------------
LESSON_34 = [
    {
        "type": "transcript",
        "title": "Opening — food experiences",
        "lines": [
            {"speaker": "Teacher", "text": "Today we're talking about the past — experiences, habits, and finished events. Let's start with a simple chat."},
            {"speaker": "A", "text": "So, have you tried many unusual foods?"},
            {"speaker": "B", "text": "Yeah, I've tried sushi, and I've eaten insects once — in Thailand."},
            {"speaker": "A", "text": "Really? I've never tried that. Have you ever cooked something totally new?"},
            {"speaker": "B", "text": "I've made homemade pasta a few times. It's harder than it looks!"},
        ],
    },
    {
        "type": "note",
        "title": "Talking about past experiences",
        "intro": "Use the <strong>present perfect</strong> (have/has + past participle) for life experiences — no specific time.",
        "items": [
            "I've tried windsurfing.",
            "I've never been bungee jumping.",
        ],
    },
    {
        "type": "note",
        "title": "Talking about past experiences",
        "items": [
            "I've read 'The Idiot'.",
            "I've never drunk whisky.",
            "Have you ever grown your own vegetables?",
        ],
    },
    {
        "type": "transcript",
        "title": "Follow-up — more experience questions",
        "lines": [
            {"speaker": "A", "text": "Have you ever been to Italy?"},
            {"speaker": "B", "text": "Yes — I went there two years ago for a friend's wedding."},
            {"speaker": "A", "text": "Nice! Did you eat a lot of pasta?"},
            {"speaker": "B", "text": "I ate pasta almost every day when I was there."},
            {"speaker": "A", "text": "When did you last try a new cuisine?"},
            {"speaker": "B", "text": "I tried Korean BBQ last month — it was amazing."},
        ],
    },
    {
        "type": "note",
        "title": "Talking about past experiences",
        "intro": "Use the <strong>past simple</strong> when you mention a <strong>specific time</strong> in the past.",
        "items": [
            'I <mark class="lr-hl">went</mark> windsurfing <mark class="lr-hl">three years ago</mark>.',
            'I <mark class="lr-hl">didn\'t drink</mark> a lot <mark class="lr-hl">last year</mark>.',
            '<mark class="lr-hl">Did</mark> you <mark class="lr-hl">eat</mark> a lot of sushi <mark class="lr-hl">when you were</mark> in Japan?',
        ],
    },
    {
        "type": "note",
        "title": "Present perfect → past simple",
        "exchange": [
            {
                "q": '"Have you ever been to Australia?"',
                "q_hl": ["Have", "been"],
                "a": '"Yes, I went there two years ago, for my friend\'s wedding."',
                "a_hl": ["went", "two years ago,"],
            },
        ],
        "tip": "Experience question → present perfect. Answer with a specific time → past simple.",
    },
    {
        "type": "transcript",
        "title": "Childhood eating habits",
        "lines": [
            {"speaker": "A", "text": "What did you use to eat when you were a kid?"},
            {"speaker": "B", "text": "When I was a child, I would eat fast food almost every day. My mum used to cook at home, but I hated vegetables."},
            {"speaker": "A", "text": "And now?"},
            {"speaker": "B", "text": "Now I love a good vegetable salad. I was chopping vegetables yesterday when my friend called — we talked about healthy eating for ages."},
        ],
    },
    {
        "type": "note",
        "title": "Past habits & background actions",
        "items": [
            ("Past Simple", "finished events — <em>Last Sunday I grilled kebab.</em>"),
            ("Past Continuous", "background action — <em>I was chopping vegetables when…</em>"),
            ("used to / would", "past habits — <em>When I was a child, I would eat fast food every day.</em>"),
            ("Time anchors", "when I was younger · last year · as a teenager"),
        ],
        "formula": True,
    },
]

# ---------------------------------------------------------------------------
# Lesson 57 — Past Perfect (iKi4Jy6r-0s)
# ---------------------------------------------------------------------------
LESSON_57 = [
    {
        "type": "transcript",
        "title": "Arriving late to dinner",
        "lines": [
            {"speaker": "A", "text": "Sorry I'm late! What did I miss?"},
            {"speaker": "B", "text": "They'd already served dessert by the time you arrived."},
            {"speaker": "A", "text": "No way — I'd been looking forward to the main course all day!"},
            {"speaker": "B", "text": "Well, they'd finished the roast before eight. You should have come earlier."},
        ],
    },
    {
        "type": "note",
        "title": "Past perfect — form & meaning",
        "items": [
            ("Form", "had + past participle — <em>I had tried</em> · <em>they had served</em>"),
            ("Earlier past", "Event A happened <strong>before</strong> event B (both in the past)"),
            ("Timeline", "had tried → then visited → then tasted"),
        ],
        "formula": True,
    },
    {
        "type": "transcript",
        "title": "First-time food experiences",
        "lines": [
            {"speaker": "A", "text": "Had you ever tasted blue cheese before that trip to France?"},
            {"speaker": "B", "text": "No — I'd never tried it before. When I finally ate some, the flavour shocked me."},
            {"speaker": "A", "text": "Had you read anything about French cheese before you went?"},
            {"speaker": "B", "text": "I'd read a few articles, but I hadn't expected it to be so strong."},
        ],
    },
    {
        "type": "note",
        "title": "Past perfect for experiences before another past moment",
        "items": [
            "<em>I had never tried lobster before that trip.</em>",
            "<em>She'd already eaten when we arrived.</em>",
            "<em>Had you ever cooked Thai food before you moved to Bangkok?</em>",
        ],
        "tip": "Use past perfect for the <strong>earlier</strong> of two past events — especially with <em>before</em>, <em>already</em>, <em>never … before</em>.",
    },
    {
        "type": "transcript",
        "title": "Cooking disaster — two past events",
        "lines": [
            {"speaker": "A", "text": "What happened at the barbecue?"},
            {"speaker": "B", "text": "The guests had already left when the meat was ready. I'd burned everything because I'd forgotten to check the grill."},
            {"speaker": "A", "text": "Oh no! Had you marinated it the night before?"},
            {"speaker": "B", "text": "Yes, but I'd left it out too long — it wasn't safe to serve."},
        ],
    },
    {
        "type": "note",
        "title": "Past perfect continuous (bonus)",
        "items": [
            "<em>I'd been cooking for two hours when the oven broke.</em>",
            "<em>She'd been waiting ages before the food finally arrived.</em>",
        ],
        "tip": "Past perfect continuous = had been + -ing — an action continuing up to another past point.",
    },
]

# ---------------------------------------------------------------------------
# Lesson 15 — Tell a story (m04lQ5BUAn0)
# ---------------------------------------------------------------------------
LESSON_15 = [
    {
        "type": "transcript",
        "title": "Intro — why stories matter",
        "lines": [
            {"speaker": "Gina", "text": "Stories are powerful. In IELTS Speaking — especially Part 2 — you need to tell stories whether you realise it or not."},
            {"speaker": "Gina", "text": "In this lesson you'll see three stories. Think of your own meal or kitchen story as we go."},
        ],
    },
    {
        "type": "note",
        "title": "Step 1 · Background",
        "intro": "Start with one sentence: <strong>who · when · where · what</strong>. Add 1–2 detail sentences — don't drag.",
        "items": [
            "<em>It was last month, and I invited some friends over for dinner.</em>",
            "<em>At university, I shared a flat with three other guys who loved cooking pranks.</em>",
        ],
        "tip": "Enough detail to feel real; get to the point quickly.",
    },
    {
        "type": "transcript",
        "title": "Story 1 — beach picnic (background)",
        "lines": [
            {"speaker": "Gina", "text": "It was summer, and I went with some friends to a beach in Crimea which you could only get to by boat."},
            {"speaker": "Gina", "text": "People had been going there for years — benches, fire places, a kind of hippy place."},
        ],
    },
    {
        "type": "note",
        "title": "Step 2 · Goal",
        "intro": "Every story needs a <strong>goal</strong> — what did people want?",
        "items": [
            "<em>On the last day, we had to catch a train in the evening.</em>",
            "<em>We wanted to finish cooking before the guests arrived.</em>",
        ],
    },
    {
        "type": "transcript",
        "title": "Story 1 — tension builds",
        "lines": [
            {"speaker": "Gina", "text": "We'd planned a big barbecue, but the weather turned bad."},
            {"speaker": "Gina", "text": "The meat wasn't ready, the train was at six, and we still had to pack everything."},
            {"speaker": "Gina", "text": "People started to worry we wouldn't make it."},
        ],
    },
    {
        "type": "note",
        "title": "Step 3 · Tension",
        "intro": "The goal must <strong>not</strong> be too easy. Add problems — listeners should think: <em>what's going to happen?</em>",
        "items": [
            "Difficult conditions before the climax",
            "Unexpected problem (storm, broken oven, missing ingredient)",
            "People doubt success or failure",
        ],
    },
    {
        "type": "transcript",
        "title": "Story 1 — ending",
        "lines": [
            {"speaker": "Gina", "text": "We ran to the station with bags of half-eaten food — and we made the train with one minute to spare."},
            {"speaker": "Gina", "text": "Looking back, it was stressful but really fun. We still talk about that trip."},
        ],
    },
    {
        "type": "note",
        "title": "Step 4 · Ending",
        "intro": "Resolve the tension, then add a <strong>retrospective comment</strong>.",
        "items": [
            "<em>Looking back, it was one of the best meals I'd ever shared with friends.</em>",
            "<em>In the end, we grilled outside instead — and it tasted even better.</em>",
        ],
    },
]

# ---------------------------------------------------------------------------
# Lesson 23 — Future (0anZBvnj6LM)
# ---------------------------------------------------------------------------
LESSON_23 = [
    {
        "type": "transcript",
        "title": "Weekend plans",
        "lines": [
            {"speaker": "Martin", "text": "What are you doing this weekend?"},
            {"speaker": "B", "text": "I'm meeting some friends for lunch on Saturday, and then we're going to the theatre."},
            {"speaker": "Martin", "text": "Sounds good! What about Sunday?"},
            {"speaker": "B", "text": "Not sure — I don't have plans yet."},
            {"speaker": "Martin", "text": "I'm going away for the weekend. I found some cheap flights to Berlin!"},
        ],
    },
    {
        "type": "note",
        "title": "Present continuous — fixed plans",
        "intro": "Present continuous for the future when you know <strong>when / where</strong>.",
        "items": [
            "What are you doing tomorrow / tonight / next Wednesday evening?",
            "<em>I'm working in the morning, then I'm playing football in the park.</em>",
            "<em>I'm going for a beer with some people from work.</em>",
        ],
    },
    {
        "type": "transcript",
        "title": "Holiday plans — Egypt",
        "lines": [
            {"speaker": "A", "text": "Are you going anywhere next summer?"},
            {"speaker": "B", "text": "I'm going to Egypt for ten days with a group of friends."},
            {"speaker": "A", "text": "How long are you staying? Who are you going with?"},
            {"speaker": "B", "text": "Just a week in August. We're planning to do sightseeing around Cairo, then we're going to do a boat trip on the Nile."},
        ],
    },
    {
        "type": "note",
        "title": "Plans without full details",
        "items": [
            "<em>What are you going to do after you graduate?</em>",
            "<em>I'm planning to buy an apartment next year.</em>",
            "<em>I'd like to learn to cook Thai food one day.</em>",
            "<em>My dream is to open a small café near the sea.</em>",
        ],
    },
    {
        "type": "transcript",
        "title": "Concert & bus schedule",
        "lines": [
            {"speaker": "A", "text": "What time does the concert start?"},
            {"speaker": "B", "text": "It starts at eight, so we need to leave at half past six."},
            {"speaker": "A", "text": "Is there a bus?"},
            {"speaker": "B", "text": "Yeah — it leaves at quarter to seven and gets there around half past seven. The last bus back leaves at ten fifteen."},
        ],
    },
    {
        "type": "note",
        "title": "Present simple — timetables & schedules",
        "intro": "Use present simple for buses, classes, flights, events on a fixed timetable.",
        "items": [
            "<em>Our cooking class starts at eleven thirty.</em>",
            "<em>What time is your flight?</em>",
            "<em>The wedding is at three.</em>",
        ],
    },
    {
        "type": "transcript",
        "title": "World Cup predictions",
        "lines": [
            {"speaker": "Martin", "text": "Who's going to win the next World Cup?"},
            {"speaker": "A", "text": "Italy will win, I think."},
            {"speaker": "B", "text": "I hope England will win, but I don't think they actually will."},
            {"speaker": "A", "text": "Look at those clouds — it's going to rain before the match."},
        ],
    },
    {
        "type": "note",
        "title": "Predictions — will / going to",
        "items": [
            "<em>People will eat more plant-based food.</em>",
            "<em>It's going to rain — look at those clouds.</em>",
            "will and going to are often interchangeable for predictions",
        ],
    },
    {
        "type": "transcript",
        "title": "Marathon — how sure are you?",
        "lines": [
            {"speaker": "A", "text": "Do you think she'll finish under four hours?"},
            {"speaker": "B", "text": "She'll definitely do it. Michelle is sure to be much faster than Andy."},
            {"speaker": "A", "text": "Andy? There's no chance he's going to finish — he's unlikely to get a fast time."},
            {"speaker": "B", "text": "Michelle's bound to get under four hours. That's still a good time."},
        ],
    },
    {
        "type": "note",
        "title": "How certain? — adverbs & phrases",
        "items": [
            "<em>She'll definitely do it.</em> · <em>I'm pretty sure he'll do it.</em>",
            "<em>He's unlikely to get a fast time.</em>",
            "<em>She's sure to / bound to be much faster.</em>",
            "<em>It's not likely that she'll do it that fast.</em>",
        ],
    },
    {
        "type": "transcript",
        "title": "Uncertainty — dinner plans",
        "lines": [
            {"speaker": "A", "text": "Will the new menu be ready next week?"},
            {"speaker": "B", "text": "It may be ready — or it could take a few more days."},
            {"speaker": "A", "text": "Maybe I'll order takeout tonight. It's possible that we won't need to change anything on the menu."},
        ],
    },
    {
        "type": "note",
        "title": "Uncertainty — may / might / could",
        "items": [
            "<em>I might order takeout tonight.</em>",
            "<em>Perhaps we won't need to change anything.</em>",
            "<em>It's possible that we'll have to replace some recipes.</em>",
        ],
    },
]

# ---------------------------------------------------------------------------
# Lesson 61 — Add emphasis (P-PSlizktNU)
# ---------------------------------------------------------------------------
LESSON_61 = [
    {
        "type": "transcript",
        "title": "What do you enjoy about cooking?",
        "lines": [
            {"speaker": "A", "text": "What do you like about cooking?"},
            {"speaker": "B", "text": "What I enjoy most is experimenting with spices and herbs."},
            {"speaker": "A", "text": "Do you like spicy food?"},
            {"speaker": "B", "text": "I do like spicy food — but not every day. Really spicy dishes are what I crave when it's cold."},
        ],
    },
    {
        "type": "note",
        "title": "What … is / What … do",
        "items": [
            "<em>What I enjoy most is trying new cuisines.</em>",
            "<em>What I don't like is processed food.</em>",
            "Front-load the important idea — sounds natural in IELTS answers.",
        ],
    },
    {
        "type": "transcript",
        "title": "Memorable meal",
        "lines": [
            {"speaker": "A", "text": "Tell me about a meal you remember."},
            {"speaker": "B", "text": "It was the fresh herbs that made the dish special — not the meat, actually."},
            {"speaker": "A", "text": "So the flavour came from the herbs?"},
            {"speaker": "B", "text": "Exactly. It was my grandmother's recipe that started my love of cooking."},
        ],
    },
    {
        "type": "note",
        "title": "It was … that (cleft sentence)",
        "items": [
            "<em>It was the fresh herbs that made the dish special.</em>",
            "<em>It was last summer that I first tried authentic pho.</em>",
            "Highlights one part of the sentence — great for Part 2 & 3.",
        ],
    },
    {
        "type": "transcript",
        "title": "Strong feelings about food",
        "lines": [
            {"speaker": "A", "text": "You don't eat fast food, do you?"},
            {"speaker": "B", "text": "I do eat it sometimes — but I absolutely hate eating it every day."},
            {"speaker": "A", "text": "Homemade pasta?"},
            {"speaker": "B", "text": "I really love homemade pasta. So does my sister — we both make it on Sundays."},
        ],
    },
    {
        "type": "note",
        "title": "do/does · so / really / absolutely",
        "items": [
            "<em>I do like</em> spicy food (affirm emphatic)",
            "<em>I absolutely love</em> homemade pasta.",
            "<em>I really enjoy</em> baking at the weekend.",
            "Also: stress the key word when speaking — <em>I LOVE spicy food</em>.",
        ],
    },
]

SPEAKING_SEGMENTS: dict[str, list[dict]] = {
    "lesson-34-how-to-talk-about-the-past-in-english": LESSON_34,
    "lesson-57-how-to-use-the-past-perfect-tense-in-english-english-grammar": LESSON_57,
    "lesson-15-how-to-tell-a-story-in-english-using-past-tense": LESSON_15,
    "lesson-23-future-in-english-how-to-talk-about-the-future": LESSON_23,
    "lesson-61-how-to-add-emphasis-in-english-improve-your-spoken-english": LESSON_61,
}
