#!/usr/bin/env python3
"""Rewrite Body & Appearance, Home & Living, Clothes & Fashion exercises
as daily blog / speaking-style English (same approach as Food & People).
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "public" / "blog" / "english"

_spec = importlib.util.spec_from_file_location(
    "gen_ex", Path(__file__).with_name("_gen_english_exercises.py")
)
_gen = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_gen)

TOPICS = _gen.TOPICS
collect_words = _gen.collect_words
mark_sentence = _gen.mark_sentence
wrap_exercise = _gen.wrap_exercise


def verify_coverage(words: list[dict], sentences: list[dict]) -> list[str]:
    """Like generator verify, but decode HTML entities from mark_sentence()."""
    blob = " ".join(s["en_html"] for s in sentences).lower()
    blob = (
        blob.replace("&#x27;", "'")
        .replace("&#39;", "'")
        .replace("&apos;", "'")
        .replace("&amp;", "&")
    )
    missing = []
    for w in words:
        form = w["form"].lower()
        lemma = w["word"].lower()
        if form not in blob and lemma not in blob:
            missing.append(w["word"])
    return missing

# PASSAGES[slug][level] = list[(en, vi)]
PASSAGES: dict[str, dict[str, list[tuple[str, str]]]] = {
    "body-appearance": {
        "A1": [
            (
                "Yes, absolutely — my favourite way to warm up speaking is naming body words. "
                "My body has a head, a face, a neck, and hair that I brush every morning. "
                "I look in the mirror and see my eye, nose, ear, cheek, chin, mouth, tooth, and lip. "
                "Honestly, describing my face helps me sound more natural in English.",
                "Chắc chắn rồi — cách khởi động speaking yêu thích của tôi là gọi tên từ về body. "
                "Body tôi có head, face, neck, và hair tôi chải mỗi sáng. "
                "Tôi nhìn gương thấy eye, nose, ear, cheek, chin, mouth, tooth, và lip. "
                "Mô tả face giúp tôi nói tự nhiên hơn.",
            ),
            (
                "What kind of body words do I still need? The rest of my body. "
                "I raise my hand and stretch my arm on each side, then feel my back, stomach, and a strong leg. "
                "My foot and knee help me walk; when I sit too long my back feels tired. "
                "So that’s my simple A1 blog about the head and the body.",
                "Loại từ body nào tôi còn cần? Phần còn lại của body. "
                "Tôi có hand và arm mỗi bên, rồi back, stomach, và leg khỏe. "
                "Foot và knee giúp đi; ngồi lâu thì back mệt. "
                "Đó là blog A1 đơn giản về head và body.",
            ),
        ],
        "A2": [
            (
                "I prefer kind descriptions of appearance and personality to rude jokes. "
                "Some people look attractive, good-looking, handsome, pretty, or just cute. "
                "Hair can be curly, wavy, or straight; someone blond or bald may also wear a beard or a mustache. "
                "A male or female friend can look slim, skinny, fit, or tiny — I try to describe with kind words, not rude ones.",
                "Tôi thích mô tả appearance và personality tử tế hơn đùa thô. "
                "Có người attractive, good-looking, handsome, pretty, hoặc cute. "
                "Hair có thể curly, wavy, hoặc straight; người blond hoặc bald cũng có thể có beard hay mustache. "
                "Friend male hoặc female có thể slim, skinny, fit, hoặc tiny — tôi cố describe tử tế, không rude.",
            ),
            (
                "To be honest, behavior and character are harder to describe than looks. "
                "My personality can feel shy or talkative, serious or funny, interesting or boring. "
                "An exciting day feels wonderful, amazing, excellent, and awesome; a kind person is nice and great. "
                "Sometimes life feels weird, strange, or tough; a unique, creative, brilliant idea can still look crazy. "
                "I want to stay confident, helpful, fair, and quiet when I’m unsure — not jealous, foolish, or unhappy.",
                "Thành thật mà nói, behavior và character khó mô tả hơn vẻ ngoài. "
                "Personality tôi có lúc shy hoặc talkative, serious hoặc funny, interesting hoặc boring. "
                "Ngày exciting thì wonderful, amazing, excellent, awesome; người kind thì nice và great. "
                "Đôi khi weird, strange, hoặc tough; ý tưởng unique, creative, brilliant vẫn có thể crazy. "
                "Tôi muốn confident, helpful, fair, và quiet khi unsure — không jealous, foolish, hay unhappy.",
            ),
            (
                "About the human body: under the skin there is blood, bone, and muscle. "
                "My chest rises with every breath and breathing feels easy when I’m active and strong, not weak. "
                "I can show my palm, forearm, wrist, elbow, and finger; my thigh, heel, and throat work hard when I run. "
                "The skull protects the brain; gum and eyelash are small but useful. "
                "Physically I’m fine — I brush my hair, smile, look friendly, and hide stress when I appear calm. "
                "Other people may look similar; each individual still has their own mild or scary mood. "
                "A perfect day is when I feel normal, certain, and ready to describe how I appear.",
                "Về human body: dưới skin có blood, bone, và muscle. "
                "Chest nhịp theo breath và breathing dễ khi active và strong, không weak. "
                "Tôi show palm, forearm, wrist, elbow, finger; thigh, heel, throat làm việc khi chạy. "
                "Skull bảo vệ brain; gum và eyelash nhỏ nhưng hữu ích. "
                "Physically tôi ổn — brush hair, smile, look thân thiện, hide stress khi appear bình tĩnh. "
                "Other người có thể similar; mỗi individual vẫn own mild hoặc scary. "
                "Ngày perfect là khi normal, certain, và sẵn sàng describe cách mình appear. "
                "Còn fat trên body thì tôi nói nhẹ nhàng thôi.",
            ),
        ],
        "B1": [
            (
                "Generally speaking, I talk about figure and beauty without being cruel. "
                "Attractiveness can look stunning or gorgeous; ugliness talk feels unattractive and mean. "
                "Someone chubby, overweight, or obese needs respect; someone underweight does too. "
                "A hairstyle can be thick, shiny, ginger, red, gray-haired, or fair after a haircut. "
                "I comb carefully, sometimes shave, and ignore hairy jokes. "
                "A pale expression, a frown, a grin, a spot, or a freckle still belongs to a well-dressed person of any race — even a little curious child.",
                "Nhìn chung, tôi nói về figure và beauty mà không cruel. "
                "Attractiveness có thể stunning hoặc gorgeous; nói ugliness thì unattractive và mean. "
                "Người chubby, overweight, hoặc obese cần tôn trọng; underweight cũng vậy. "
                "Hairstyle có thể thick, shiny, ginger, red, gray-haired, hoặc fair sau haircut. "
                "Tôi comb cẩn thận, đôi khi shave, bỏ qua joke hairy. "
                "Expression pale, frown, grin, spot, freckle vẫn thuộc người well-dressed mọi race — kể cả child little curious.",
            ),
            (
                "If I had to describe personal characteristics, it would have to start with friends. "
                "A brave and honest friend feels loyal, responsible, and reliable; a stubborn bully can feel annoying or evil. "
                "I admire people who are patient, keen, generous, gentle, understanding, skillful, and peaceful. "
                "Ambitious, independent, outgoing, organized, and sociable energy feels warm and welcoming. "
                "I try not to be selfish, miserable, needy, childish, or doubtful; I appreciate wise, slow, cool, and mysterious calm. "
                "Talent is a quality and a characteristic; nature can look positive or negative. "
                "When I’m relaxed and easy, I don’t pretend or play a trick — I stay open, determined, and proud of small progress. "
                "Horrible days happen; I stay experienced enough not to turn cruel or weak.",
                "Nếu phải mô tả personal characteristics, chắc chắn bắt đầu từ bạn bè. "
                "Friend brave và honest thì loyal, responsible, reliable; bully stubborn có thể annoying hoặc evil. "
                "Tôi admire người patient, keen, generous, gentle, understanding, skillful, peaceful. "
                "Năng lượng ambitious, independent, outgoing, organized, sociable thì warm và welcoming. "
                "Tôi tránh selfish, miserable, needy, childish, doubtful; appreciate sự wise, slow, cool, mysterious. "
                "Talent là quality và characteristic; nature có thể positive hoặc negative. "
                "Khi relaxed và easy, tôi không pretend hay trick — open, determined, proud với tiến bộ nhỏ. "
                "Ngày horrible vẫn tới; tôi đủ experienced để không cruel hay weak. "
                "Concern về hình ảnh thì có, nhưng tôi muốn individual dependent vào giá trị thật.",
            ),
            (
                "About the body in B1: armpit, hip, temple, thumb, toenail, fingernail, joint, rib, and sole are useful words. "
                "An eyeball helps sight; I breathe for circulation while hearing, touch, smell, and taste work as a sense. "
                "My waist moves when I dance; a tear can fall; blood sugar, a kidney, a lung, a hormone, tissue, and a nerve keep me alive. "
                "A small gesture says a lot — that’s my speaking blog for human characteristics.",
                "Về body B1: armpit, hip, temple, thumb, toenail, fingernail, joint, rib, và sole rất hữu ích. "
                "Eyeball giúp sight; tôi breathe cho circulation trong khi hearing, touch, smell, taste là sense. "
                "Waist chuyển động khi nhảy; tear có thể rơi; blood sugar, kidney, lung, hormone, tissue, nerve giữ tôi sống. "
                "Gesture nhỏ nói nhiều — đó là blog speaking về human characteristics. "
                "Talent và silly moments vẫn thuộc về tôi; talented friends inspire me.",
            ),
        ],
        "B2": [
            (
                "Looking back, the last time I described bodily actions was in a real story. "
                "I can beat a drum, clap, drag a bag, grab a bottle, or punch a pillow for fun — carefully. "
                "I bend, bow, lean, or slouch when I’m tired; I kneel, leap, tiptoe, crawl, or lie down at home. "
                "Eyes blink, gaze, squint, stare, or wink; I chuckle, giggle, or smirk with friends. "
                "Sometimes I march, nod, pace, or trip; kids give bunny ears in photos — books write [give] {sb} bunny ears. "
                "I crouch to tie shoes and wake early for work.",
                "Nhìn lại, lần gần nhất tôi mô tả bodily actions là trong chuyện thật. "
                "Tôi beat trống, clap, drag túi, grab chai, hoặc punch gối vui — cẩn thận. "
                "Tôi bend, bow, lean, hoặc slouch khi mệt; kneel, leap, tiptoe, crawl, hoặc lie down ở nhà. "
                "Mắt blink, gaze, squint, stare, hoặc wink; tôi chuckle, giggle, hoặc smirk với bạn. "
                "Đôi khi march, nod, pace, hoặc trip; trẻ give bunny ears — sách ghi [give] {sb} bunny ears. "
                "Tôi crouch buộc giày và wake sớm đi làm.",
            ),
            (
                "Personality words matter too. I try to stay caring, decent, easy-going, energetic, enthusiastic, and dynamic. "
                "I dislike arrogant, dishonest, greedy, icy, impatient, nosy, violent, or tight-fisted behavior. "
                "A bold, lively, logical, modest, moral, optimistic, passionate, practical, reasonable, and respectable attitude feels sincere. "
                "Self-confident people can still be sensitive and sympathetic; moody, pessimistic, unreliable, unstable, or unsure days happen. "
                "Strict or lenient teachers both shape us; tough weeks need a strong-willed plan, not forgetful chaos.",
                "Từ personality cũng quan trọng. Tôi cố caring, decent, easy-going, energetic, enthusiastic, dynamic. "
                "Không thích arrogant, dishonest, greedy, icy, impatient, nosy, violent, tight-fisted. "
                "Thái độ bold, lively, logical, modest, moral, optimistic, passionate, practical, reasonable, respectable thì sincere. "
                "Người self-confident vẫn có thể sensitive và sympathetic; ngày moody, pessimistic, unreliable, unstable, unsure vẫn tới. "
                "Thầy strict hoặc lenient đều ảnh hưởng; tuần tough cần kế hoạch strong-willed, không forgetful.",
            ),
            (
                "Self-care is part of my routine: electric razor or shaver, sunscreen, shampoo, conditioner, balm, lotion, and cosmetics. "
                "Gel, hairspray, eyeliner, eyeshadow, blush, concealer, face powder, foundation, lip gloss, lipstick, mascara, and nail polish sit on the shelf. "
                "A face mask, dye, tweezers, cologne, deodorant, mouthwash, dental floss, nail file, cotton swab, makeup, and nail clippers finish the kit. "
                "I won’t detail every private item, but a tampon belongs to real adult talk too.",
                "Self-care là routine: electric razor hoặc shaver, sunscreen, shampoo, conditioner, balm, lotion, cosmetics. "
                "Gel, hairspray, eyeliner, eyeshadow, blush, concealer, face powder, foundation, lip gloss, lipstick, mascara, nail polish trên kệ. "
                "Face mask, dye, tweezers, cologne, deodorant, mouthwash, dental floss, nail file, cotton swab, makeup, nail clippers hoàn thiện. "
                "Tôi không đi sâu đồ riêng tư, nhưng tampon cũng thuộc nói chuyện người lớn.",
            ),
            (
                "Anatomy helps advanced speaking: an organ, Adam's apple, artery, blood vessel, cell, heartbeat, and scalp. "
                "Collarbone, breast, abdomen, digestive system, immune system, belly, belly button, intestine, gallbladder, bladder, and buttock are clinical but useful. "
                "Spine, calf, shin, big toe, pinky, eyelid, jaw, vein, nostril, eyebrow — and a painful kidney stone — complete the picture. "
                "That’s my B2 body-and-appearance blog for the exam room.",
                "Anatomy giúp speaking nâng cao: organ, Adam's apple, artery, blood vessel, cell, heartbeat, scalp. "
                "Collarbone, breast, abdomen, digestive system, immune system, belly, belly button, intestine, gallbladder, bladder, buttock hữu ích. "
                "Spine, calf, shin, big toe, pinky, eyelid, jaw, vein, nostril, eyebrow — và kidney stone đau — hoàn thiện. "
                "Đó là blog B2 body & appearance cho phòng thi.",
            ),
        ],
    },
    "home-living": {
        "A1": [
            (
                "Yes, definitely — my favourite place to relax is my home. "
                "I live in an apartment inside a building, but my dream is a quiet house with a garden. "
                "Every room has a door, a window, a wall, a floor, a roof above, and a ceiling. "
                "Upstairs and downstairs feel different; the living room, dining room, kitchen, bedroom, and bathroom make daily life easy.",
                "Chắc chắn rồi — nơi yêu thích để thư giãn là home của tôi. "
                "Tôi sống trong apartment trong building, nhưng mơ house yên với garden. "
                "Mỗi room có door, window, wall, floor, roof và ceiling. "
                "Upstairs và downstairs khác nhau; living room, dining room, kitchen, bedroom, bathroom làm đời dễ.",
            ),
            (
                "What kind of furniture do I use every day? "
                "I have a desk, a chair, a table, a sofa, a bed, and a cabinet near the refrigerator, television, and stove. "
                "In the closet I keep a box; in the yard there is no elevator, just open space. "
                "On the table I put a dish, spoon, fork, knife, plate, glass, bottle, and cup. "
                "Soap, a brush, and a toothbrush stay in the bathroom; a pillow is on the bed; a trash can holds trash. "
                "A ball and a doll are little thing for fun — that’s part of my home story.",
                "Loại furniture nào tôi dùng mỗi ngày? "
                "Tôi có desk, chair, table, sofa, bed, cabinet gần refrigerator, television, stove. "
                "Trong closet có box; yard không có elevator, chỉ khoảng trống. "
                "Trên table có dish, spoon, fork, knife, plate, glass, bottle, cup. "
                "Soap, brush, toothbrush trong bathroom; pillow trên bed; trash can đựng rác. "
                "Ball và doll là thing vui — đó là part câu chuyện home.",
            ),
        ],
        "A2": [
            (
                "I’m going to describe my cozy neighborhood apartment. "
                "The entrance has a gate, a fence, a mailbox, and sometimes an emergency exit sign. "
                "Inside the hall, a stair takes you to each level; a light and a light bulb need a switch and an outlet. "
                "The landlord and tenant signed a lease for rent; utilities like electricity, gas, heat, and cable matter every month. "
                "I live here now; I will move in with more furniture and maybe move out later.",
                "Tôi sẽ mô tả apartment cozy trong neighborhood. "
                "Entrance có gate, fence, mailbox, đôi khi biển emergency exit. "
                "Trong hall, stair đưa lên từng level; light và light bulb cần switch và outlet. "
                "Landlord và tenant ký lease cho rent; utility như electricity, gas, heat, cable quan trọng mỗi tháng. "
                "Tôi live ở đây; sẽ move in với furniture rồi có thể move out sau.",
            ),
            (
                "Home appliances make life easier: dishwasher, washing machine, oven, coffee maker, toaster oven, "
                "air conditioner, heater, radio, telephone line, hair dryer, fan, vacuum cleaner, and iron. "
                "I use a remote control and check the smoke detector; if something is broken I repair it or call for help. "
                "In the bathroom: shower, toilet, sink, bathtub, towel, mirror, toothpaste, razor, scissors, tissue, and napkin. "
                "A key and a lock keep us safe; a gutter sits outside; a cushion softens the sofa; a bookshelf and a curtain finish the room. "
                "An alarm clock wakes me; a camera and a loudspeaker are useful device and equipment. "
                "I turn on the light, turn off the fan, and hope every system will work — even a flashlight and carpet on busy days.",
                "Home appliances giúp đời dễ: dishwasher, washing machine, oven, coffee maker, toaster oven, "
                "air conditioner, heater, radio, telephone line, hair dryer, fan, vacuum cleaner, iron. "
                "Tôi dùng remote control và kiểm tra smoke detector; nếu broken thì repair hoặc gọi giúp. "
                "Phòng tắm: shower, toilet, sink, bathtub, towel, mirror, toothpaste, razor, scissors, tissue, napkin. "
                "Key và lock giữ an toàn; gutter bên ngoài; cushion làm êm sofa; bookshelf và curtain hoàn thiện room. "
                "Alarm clock đánh thức; camera và loudspeaker là device và equipment hữu ích. "
                "Tôi turn on đèn, turn off quạt, mong mọi system work — kể cả flashlight và carpet ngày bận.",
            ),
        ],
        "B1": [
            (
                "These days houses and buildings have changed a lot where I live. "
                "Some people dream of a palace; I prefer a cabin, a studio, a guest house, a country house, or a simple apartment building. "
                "A resident needs good accommodations; rent is paid every month — yes, rent again if you share. "
                "Inside: floor, step, fireplace, chimney, driveway, corridor, drain, walkway, back door, front door, "
                "family room, guest room, storeroom, study, shelf, porch, and maybe a swimming pool.",
                "Dạo này houses và buildings nơi tôi ở đã đổi nhiều. "
                "Có người mơ palace; tôi thích cabin, studio, guest house, country house, hoặc apartment building đơn giản. "
                "Resident cần accommodations tốt; rent trả mỗi tháng — đúng, rent lần nữa nếu share. "
                "Bên trong: floor, step, fireplace, chimney, driveway, corridor, drain, walkway, back door, front door, "
                "family room, guest room, storeroom, study, shelf, porch, và có thể swimming pool.",
            ),
            (
                "Appliances and furniture in B1: bed sheet, mattress, radiator, freezer, kitchen hood, garbage disposal, "
                "pressure cooker, food processor, juicer, flatware, chopstick, ladle, spatula, mower, and faucet. "
                "A vase, a blind, a couch, a sofa bed, hair straighteners, a thermostat, a pillow, a brush, a microwave, and a rug "
                "make the place feel finished. That’s my home-living speaking blog.",
                "Appliances và furniture B1: bed sheet, mattress, radiator, freezer, kitchen hood, garbage disposal, "
                "pressure cooker, food processor, juicer, flatware, chopstick, ladle, spatula, mower, faucet. "
                "Vase, blind, couch, sofa bed, hair straighteners, thermostat, pillow, brush, microwave, rug "
                "làm nơi ở trọn vẹn. Đó là blog speaking home & living.",
            ),
        ],
        "B2": [
            (
                "One thing I dislike about some city property is how crowded it feels — still, structures fascinate me. "
                "A mortgage on a skyscraper condo sounds heavy; a mansion, condominium, penthouse, duplex, complex, "
                "housing development, row house, or houseboat each has a different vibe. "
                "An attic, basement, cellar, nursery, patio, and rooftop change how a household uses space. "
                "Doorbell, doorstep, doorway, air conditioning, central heating, and a smoke alarm matter for safety. "
                "A bureau with a drawer, a garbage can, and daily chore like mop, scrub, sweep, vacuum, and wipe keep things clean. "
                "We furnish with care, follow a blueprint, and avoid an abandoned ruin.",
                "Một điều tôi không thích ở một số property thành phố là đông — nhưng city structures vẫn cuốn. "
                "Mortgage cho skyscraper nặng; mansion, condominium, penthouse, duplex, complex, "
                "housing development, row house, hoặc houseboat mỗi kiểu một vibe. "
                "Attic, basement, cellar, nursery, patio, rooftop đổi cách dùng không gian. "
                "Doorbell, doorstep, doorway, air conditioning, central heating, smoke alarm quan trọng. "
                "Bureau với drawer, garbage can, và chore như mop, scrub, sweep, vacuum, wipe giữ sạch. "
                "Chúng tôi furnish cẩn thận, theo blueprint, tránh ruin abandoned.",
            ),
            (
                "Buildings can look classical, external, industrial, open-plan, or spacious. "
                "Workers construct with brick, column, concrete, and a digger; a passage leads to an exit or a hut on another level. "
                "Cities rebuild after damage; a curb, landfill, and sewer sit under a landmark or monument. "
                "A facility may be a casino, courthouse, disco, nursing home, schoolhouse, town hall, funeral home, graveyard, or tomb — "
                "each structure tells a social story.",
                "Building có thể classical, external, industrial, open-plan, hoặc spacious. "
                "Công nhân construct bằng brick, column, concrete, digger; passage dẫn tới exit hoặc hut ở level khác. "
                "Thành phố rebuild sau hỏng; curb, landfill, sewer dưới landmark hoặc monument. "
                "Facility có thể casino, courthouse, disco, nursing home, schoolhouse, town hall, funeral home, graveyard, tomb — "
                "mỗi structure kể chuyện xã hội. Development cũng là từ hay dùng.",
            ),
            (
                "Tools finish this B2 blog: hammer, mallet, saw, chainsaw, drill, wrench, screw, screwdriver, nail, glue, "
                "file, chisel, bolt, nut, washer, fork, shovel, wheelbarrow, toolbox, pliers, wire cutter, duct tape, "
                "plunger, crowbar, staple gun, box cutter, adjustable wrench, tape measure, sledgehammer, and ax. "
                "Every tool has a function — even a simple coat by the door after work. "
                "That’s how I talk about home, living, and building sites in English.",
                "Tools kết thúc blog B2: hammer, mallet, saw, chainsaw, drill, wrench, screw, screwdriver, nail, glue, "
                "file, chisel, bolt, nut, washer, fork, shovel, wheelbarrow, toolbox, pliers, wire cutter, duct tape, "
                "plunger, crowbar, staple gun, box cutter, adjustable wrench, tape measure, sledgehammer, ax. "
                "Mỗi tool có function — kể cả coat đơn giản cạnh cửa sau giờ làm. "
                "Đó là cách tôi nói về home, living, và công trường bằng tiếng Anh.",
            ),
        ],
    },
    "clothes-fashion": {
        "A1": [
            (
                "Yes, absolutely. My favourite clothes are simple ones. "
                "Most days I wear a shirt or a T-shirt, pants or jeans, and a comfortable shoe or sock. "
                "In cold weather I add a coat, jacket, or sweater; for work I may choose a suit and a tie. "
                "A dress or a skirt feels nice for events; a hat and a purse finish the look. "
                "At home I change into pajamas; underwear and a swimsuit stay for private or beach days. "
                "A boot is for rain — that’s my A1 fashion speaking blog.",
                "Chắc chắn rồi. Clothes yêu thích của tôi là kiểu đơn giản. "
                "Hầu hết ngày tôi mặc shirt hoặc T-shirt, pants hoặc jeans, và shoe hoặc sock. "
                "Trời lạnh thêm coat, jacket, hoặc sweater; đi làm có thể suit và tie. "
                "Dress hoặc skirt hợp sự kiện; hat và purse hoàn thiện. "
                "Ở nhà tôi mặc pajamas; underwear và swimsuit cho riêng tư hoặc biển. "
                "Boot cho mưa — đó là blog speaking A1 về thời trang.",
            ),
        ],
        "A2": [
            (
                "How often do I think about fashion and clothing? Almost every morning. "
                "A blouse, shorts, a uniform, or a belt can change a look; a pocket and a button are small but useful. "
                "Accessories matter: a watch, glasses, sunglasses, briefcase, cap, bracelet, wallet, chain, "
                "earring, ring, necklace, jewelry, perfume, and an umbrella. "
                "Clothes may feel loose or tight; I try on items, put on what fits, take off what feels worn-out, and change if needed. "
                "That’s how I speak about style at A2.",
                "Tôi nghĩ về fashion và clothing bao lâu một lần? Hầu như mỗi sáng. "
                "Blouse, shorts, uniform, hoặc belt đổi diện mạo; pocket và button nhỏ nhưng hữu ích. "
                "Accessory quan trọng: watch, glasses, sunglasses, briefcase, cap, bracelet, wallet, chain, "
                "earring, ring, necklace, jewelry, perfume, umbrella. "
                "Clothes có thể loose hoặc tight; tôi try on, put on đồ fit, take off đồ worn-out, và change nếu cần. "
                "Đó là cách tôi nói về style ở A2.",
            ),
        ],
        "B1": [
            (
                "Yes, definitely. Fashion at B1 feels more detailed. "
                "A costume, top, hoodie, sweatshirt, overcoat, or bathing suit can look trendy and fashionable. "
                "Underpants, panties, and a bra are private words but real; a baggy hoodie with a collar and sleeve feels casual. "
                "I fasten a button on denim, cotton, wool, linen, leather, or fur cloth with a stripe pattern. "
                "A backpack finishes school days; a suit still works for meetings. "
                "Good design keeps me in style — even a simple dress with the right cloth.",
                "Chắc chắn rồi. Fashion B1 chi tiết hơn. "
                "Costume, top, hoodie, sweatshirt, overcoat, hoặc bathing suit có thể trendy và fashionable. "
                "Underpants, panties, bra là từ riêng tư nhưng thật; hoodie baggy với collar và sleeve thì casual. "
                "Tôi fasten button trên denim, cotton, wool, linen, leather, hoặc fur cloth với pattern stripe. "
                "Backpack cho ngày học; suit vẫn hợp họp. "
                "Design tốt giữ style — kể cả dress đơn giản với cloth đúng. "
                "Từ in cũng hay gặp khi nói 'in fashion'.",
            ),
        ],
        "B2": [
            (
                "The best time to talk about advanced clothes and fashion is before a night out. "
                "An apron, badge, bathrobe, bikini, cardigan, helmet, mask, or miniskirt changes the outfit mood. "
                "A jersey, sandal, vest, hood, and zipper sit next to fabric like denim, lace, lining, silk, or wooly knit. "
                "A designer collection for modeling can look glamorous, stylish, sporty, striped, plain, casual, or matching. "
                "My wardrobe helps me dress up for a masquerade or stay undressed comfort at home after work. "
                "When colors match, the whole look feels complete — that’s my B2 speaking blog on clothes.",
                "Thời điểm tốt nhất để nói về clothes và fashion nâng cao là trước khi đi chơi tối. "
                "Apron, badge, bathrobe, bikini, cardigan, helmet, mask, hoặc miniskirt đổi mood outfit. "
                "Jersey, sandal, vest, hood, zipper cạnh fabric như denim, lace, lining, silk, hoặc wooly. "
                "Collection của designer cho modeling có thể glamorous, stylish, sporty, striped, plain, casual, hoặc matching. "
                "Wardrobe giúp dress up cho masquerade hoặc undressed thoải mái ở nhà. "
                "Khi màu match, tổng thể trọn — đó là blog speaking B2 về clothes. "
                "Costume cũng vẫn là từ hay dùng.",
            ),
        ],
    },
}

LEDE = {
    "body-appearance": "Daily body & appearance blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
    "home-living": "Daily home & living blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
    "clothes-fashion": "Daily clothes & fashion blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
}

TOPIC_LABEL = {
    "body-appearance": "body and appearance",
    "home-living": "home and living",
    "clothes-fashion": "clothes and fashion",
}


def build_from_passages(slug: str, level: str, words: list[dict]) -> list[dict]:
    paras = PASSAGES[slug][level]
    sentences = []
    for en, vi in paras:
        sentences.append({"en_html": mark_sentence(en, words), "vi": vi, "words": []})

    missing = verify_coverage(words, sentences)
    if missing:
        label = TOPIC_LABEL[slug]
        miss_items = [w for w in words if w["word"] in missing]
        for i in range(0, len(miss_items), 5):
            chunk = miss_items[i : i + 5]
            forms = [w["form"] for w in chunk]
            if len(forms) == 1:
                en = f"And one more word I keep using when I talk about {label} is {forms[0]}."
                vi = f"Và thêm một từ tôi hay dùng khi nói về {label} là {forms[0]}."
            elif len(forms) == 2:
                en = f"When I wrap up this topic, I also mention {forms[0]} and {forms[1]}."
                vi = f"Khi kết thúc chủ đề này, tôi cũng nhắc {forms[0]} và {forms[1]}."
            else:
                mid = ", ".join(forms[:-1])
                en = (
                    f"To finish this {label} blog the way I’d speak in an exam, "
                    f"I also bring in {mid}, and finally {forms[-1]}."
                )
                vi = (
                    f"Để kết thúc blog {label} theo cách nói trong phòng thi, "
                    f"tôi cũng nhắc {mid}, và cuối cùng {forms[-1]}."
                )
            for w in chunk:
                if not re.search(rf"(?i)(?<![A-Za-z\[]){re.escape(w['form'])}(?![A-Za-z\]])", en):
                    en += f" ({w['form']})"
            sentences.append(
                {
                    "en_html": mark_sentence(en, chunk),
                    "vi": vi,
                    "words": [w["word"] for w in chunk],
                }
            )
    return sentences


def patch_lede(page: str, slug: str) -> str:
    lede = LEDE[slug]
    olds = [
        "Reading passage with every new word from this level’s LanGeek lessons — IPA, highlights, sentence translation, and free TTS.",
        "Daily food blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
        "Daily people & family blog / speaking-style passage — every new word from this level’s LanGeek lessons, with IPA, highlights, VI toggle, and TTS (IPA is display-only).",
    ]
    for old in olds:
        page = page.replace(old, lede)
    # If already a speaking lede from another topic, force ours
    if "speaking-style passage" in page and lede not in page:
        page = re.sub(
            r"<p class=\"lede\">Daily .*?speaking-style passage.*?</p>",
            f'<p class="lede">{lede}</p>',
            page,
            count=1,
        )
    return page


def main() -> None:
    for slug in ["body-appearance", "home-living", "clothes-fashion"]:
        topic = next(t for t in TOPICS["topics"] if t["slug"] == slug)
        print(f"\n== {slug} ==")
        for level in ["A1", "A2", "B1", "B2"]:
            lessons = [l for l in topic["lessons"] if l["level"] == level]
            if not lessons:
                continue
            words = collect_words([l["id"] for l in lessons])
            sentences = build_from_passages(slug, level, words)
            missing = verify_coverage(words, sentences)
            page = wrap_exercise(
                topic,
                level,
                words,
                sentences,
                [l["title"] for l in lessons],
            )
            page = patch_lede(page, slug)
            out_dir = OUT_ROOT / slug / f"{level.lower()}-exercise"
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(page, encoding="utf-8")
            print(f"  {level}: {len(words)} words, {len(sentences)} paras, missing={len(missing)}")
            if missing:
                print("   still:", missing[:12])


if __name__ == "__main__":
    main()
