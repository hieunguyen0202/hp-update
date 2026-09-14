"""Memorization paragraphs for People & Family Review Exercise 2 (Lessons 5–15)."""
from __future__ import annotations


def lesson_memos(v, s) -> dict[str, dict]:
    """Return memo specs keyed by lesson number. v/s = highlight helpers."""
    return {
        "5": {
            "question": "What kind of friends do you like most?",
            "sentences": [
                (
                    f'Well, I love all kinds of friends, but if I had to choose one, it would have to be {_memo_join(v, "emotionally supportive")} and {_memo_join(v, "like-minded individuals")}.',
                    "Tôi thích mọi kiểu bạn, nhưng nếu phải chọn một thì sẽ là những người hỗ trợ về cảm xúc và cùng chí hướng.",
                ),
                (
                    f'For me, {_memo_join(v, "compatibility")} and {_memo_join(v, "shared interests")} are the foundation whenever you want to {_memo_join(v, "build a relationship")}.',
                    "Với tôi, sự hòa hợp và sở thích chung là nền tảng mỗi khi bạn muốn xây dựng một mối quan hệ.",
                ),
                (
                    f'I am usually {_memo_join(v, "attracted to")} people who demonstrate true {_memo_join(v, "loyalty")} and {_memo_join(v, "mutual respect")}, as it makes it much easier to {_memo_join(v, "live in harmony with somebody")}.',
                    "Tôi thường bị thu hút bởi những người thể hiện lòng trung thành và sự tôn trọng lẫn nhau thật sự, vì như thế dễ chung sống / chơi hòa hợp hơn.",
                ),
                (
                    f'Even my {_memo_join(v, "childhood friend")} is still close to me today.',
                    "Ngay cả bạn thời thơ ấu của tôi đến nay vẫn còn thân.",
                ),
                (
                    f'This is because {_memo_join(v, "mutual trust")} is essential if you want to develop a {_memo_join(v, "long-lasting / meaningful")} connection.',
                    "Vì sự tin tưởng lẫn nhau là then chốt nếu bạn muốn phát triển một mối liên kết bền vững / ý nghĩa.",
                ),
            ],
            "keys": [
                ("emotionally supportive", "hỗ trợ về mặt cảm xúc", "v"),
                ("like-minded individuals", "những người cùng chí hướng", "v"),
                ("compatibility", "sự hòa hợp", "v"),
                ("shared interests", "sở thích chung", "v"),
                ("build a relationship", "xây dựng mối quan hệ", "v"),
                ("attracted to", "bị thu hút", "v"),
                ("loyalty", "lòng trung thành", "v"),
                ("mutual respect", "sự tôn trọng lẫn nhau", "v"),
                ("live in harmony with somebody", "chung sống/chơi hòa hợp với ai", "v"),
                ("childhood friend", "bạn thời thơ ấu", "v"),
                ("mutual trust", "sự tin tưởng lẫn nhau", "v"),
                ("long-lasting / meaningful", "bền vững / ý nghĩa", "v"),
            ],
        },
        "6": {
            "question": "Do you prefer spending time with a few close friends or a large group of people?",
            "sentences": [
                (
                    f'Well, honestly, I {_memo_join(s, "lean towards")} spending time with a small circle of close friends rather than hanging out with a large crowd or just casual {_memo_join(v, "acquaintances")}.',
                    "Thật ra, tôi nghiêng về việc dành thời gian với một vòng tròn bạn thân nhỏ hơn là đi chơi với đám đông hay chỉ những người quen xã giao.",
                ),
                (
                    f'While a {_memo_join(v, "classmate")}, {_memo_join(v, "roommate")}, or {_memo_join(v, "colleague")} is nice to talk to day-to-day, I truly {_memo_join(s, "love the feeling of")} having a trusted {_memo_join(v, "companion")} by my side.',
                    "Bạn cùng lớp, bạn cùng phòng hay đồng nghiệp thì nói chuyện hàng ngày cũng vui, nhưng tôi thật sự thích cảm giác có một người đồng hành tin cậy bên cạnh.",
                ),
                (
                    f'For me, staying home with someone close brings a real sense of {_memo_join(v, "comfort and security")}, and it makes it much easier to {_memo_join(v, "live in harmony with somebody")} compared to dealing with noisy social gatherings.',
                    "Với tôi, ở nhà với người thân mang lại cảm giác an ủi và an toàn thật sự, và dễ sống hòa hợp hơn so với những buổi tụ tập ồn ào.",
                ),
            ],
            "keys": [
                ("lean towards + NP", "nghiêng về…", "s"),
                ("acquaintance", "người quen", "v"),
                ("classmate / roommate / colleague", "bạn cùng lớp / bạn cùng phòng / đồng nghiệp", "v"),
                ("love the feeling of + V-ing", "thích cảm giác làm gì", "s"),
                ("companion", "người đồng hành", "v"),
                ("comfort and security", "sự an ủi và an toàn", "v"),
                ("live in harmony with somebody", "chung sống hòa hợp với ai", "v"),
            ],
        },
        "7": {
            "question": "What kind of family structure is common in your country?",
            "sentences": [
                (
                    f'Actually, it {_memo_join(s, "depends on")} the generation and where people live.',
                    "Thực ra còn tùy thuộc vào thế hệ và nơi người ta sống.",
                ),
                (
                    f'While older generations often grew up in {_memo_join(v, "collectivist families")} with a strong sense of {_memo_join(v, "kinship")} and respect for a traditional {_memo_join(v, "patriarchal")} or {_memo_join(v, "matriarchal")} structure, many young people today tend to be much more {_memo_join(v, "individualist")}.',
                    "Thế hệ trước thường lớn lên trong gia đình tập thể, coi trọng họ hàng và tôn trọng cấu trúc gia trưởng hoặc gia mẫu; nhiều bạn trẻ ngày nay thì mang tính cá nhân hơn hẳn.",
                ),
                (
                    f'Because of the {_memo_join(v, "fast-paced lifestyle")} in big cities, {_memo_join(v, "nuclear households")} have become far more common than large {_memo_join(v, "extended kinship")} networks.',
                    "Vì lối sống vội vã ở thành phố lớn, hộ gia đình hạt nhân phổ biến hơn nhiều so với mạng lưới họ hàng / đại gia đình rộng.",
                ),
                (
                    f'However, most people still care deeply about their {_memo_join(v, "lineage")} and would never {_memo_join(v, "disown")} their background, even when living independently.',
                    "Tuy nhiên, hầu hết mọi người vẫn coi trọng dòng họ và không bao giờ từ bỏ gốc gác, dù sống độc lập.",
                ),
            ],
            "keys": [
                ("depends on", "tùy thuộc vào…", "s"),
                ("collectivist families", "gia đình theo chủ nghĩa tập thể", "v"),
                ("kinship", "mối quan hệ họ hàng", "v"),
                ("patriarchal / matriarchal", "có tính chất gia trưởng / gia mẫu", "v"),
                ("individualist", "theo chủ nghĩa cá nhân", "v"),
                ("fast-paced lifestyle", "lối sống vội vã", "v"),
                ("nuclear households", "gia đình hạt nhân", "v"),
                ("extended kinship", "họ hàng thân thuộc / đại gia đình", "v"),
                ("lineage", "dòng họ, dòng dõi", "v"),
                ("disown", "từ bỏ, không nhận là người trong gia đình", "v"),
            ],
        },
        "8": {
            "question": "When is the best time for you to spend time with your family?",
            "sentences": [
                (
                    f'Well, evening time {_memo_join(s, "is the best time for")} me to spend quality moments with my family, especially since we {_memo_join(v, "live under the same roof")}.',
                    "Buổi tối là thời gian tốt nhất để tôi dành những phút chất lượng với gia đình, nhất là vì chúng tôi sống chung một mái nhà.",
                ),
                (
                    f'This is because the end of the day allows us to sit down together for a family dinner and {_memo_join(v, "catch up on each other\'s day")}.',
                    "Vì cuối ngày chúng tôi có thể ngồi ăn tối cùng nhau và kể / cập nhật ngày của nhau.",
                ),
                (
                    f'It doesn\'t matter how busy we get, {_memo_join(s, "as long as")} we have a chance to {_memo_join(v, "celebrate milestones")} or simply talk things through, it really helps us {_memo_join(v, "make it special")} and strengthens our bond.',
                    "Dù bận đến mấy, miễn là còn dịp kỷ niệm các mốc hoặc nói chuyện cho ra chuyện, điều đó làm buổi gặp trở nên đặc biệt và gắn kết hơn.",
                ),
            ],
            "keys": [
                ("… is the best time for …", "là thời gian tốt nhất cho…", "s"),
                ("live under the same roof", "sống chung một mái nhà", "v"),
                ("catch up on each other's day", "kể / cập nhật ngày của nhau", "v"),
                ("as long as …", "miễn là…", "s"),
                ("celebrate milestones", "kỷ niệm các mốc quan trọng", "v"),
                ("make it special", "làm cho nó trở nên đặc biệt", "v"),
            ],
        },
        "9": {
            "question": "Describe a time when you got in contact with someone you hadn’t seen for a long time.",
            "sentences": [
                (
                    f'{_memo_join(s, "As far as I can remember")}, the last time I saw my old high school friend was about 5 years ago, and after that, we slowly {_memo_join(v, "lost contact")}.',
                    "Theo như tôi còn nhớ, lần cuối gặp bạn cấp 3 là khoảng 5 năm trước, rồi chúng tôi dần mất liên lạc.",
                ),
                (
                    f'However, out of the blue, I received {_memo_join(v, "a friend request")} from him on Facebook last month.',
                    "Nhưng đột nhiên tháng trước tôi nhận được lời mời kết bạn của cậu ấy trên Facebook.",
                ),
                (
                    f'When we finally started chatting and decided to {_memo_join(v, "reconcile after years of not speaking")}, I felt thrilled.',
                    "Khi chúng tôi bắt đầu trò chuyện và quyết định giải hòa sau nhiều năm không nói chuyện, tôi thấy vui sướng.",
                ),
                (
                    f'Even though we had drifted apart for a long time, he still {_memo_join(v, "holds a special place")} in my heart, and we managed to {_memo_join(v, "catch up on old memories")} and had a great time together.',
                    "Dù đã xa cách lâu, cậu ấy vẫn giữ một vị trí đặc biệt trong tim tôi, và chúng tôi ôn lại kỷ niệm cũ, vui vẻ bên nhau.",
                ),
            ],
            "keys": [
                ("As far as I can remember, …", "Theo như tôi có thể nhớ…", "s"),
                ("lose contact", "mất liên lạc", "v"),
                ("a friend request", "lời mời kết bạn", "v"),
                ("reconcile after years of not speaking", "giải hòa sau nhiều năm không nói chuyện", "v"),
                ("hold a special place", "giữ một vị trí đặc biệt", "v"),
                ("catch up on old memories", "ôn lại những kỷ niệm cũ", "v"),
            ],
        },
        "10": {
            "question": "Did you learn a lot of important values from your family when you were a child?",
            "sentences": [
                (
                    f'Yes, when I was a child, my {_memo_join(v, "immediate family")} played a huge role in my {_memo_join(v, "upbringing")}.',
                    "Có, hồi nhỏ gia đình gần của tôi đóng vai trò rất lớn trong cách tôi được dạy dỗ.",
                ),
                (
                    f'My parents always tried to {_memo_join(v, "pass down traditional values")} and good morals, so these principles were deeply {_memo_join(v, "instilled in me")} from a very young age.',
                    "Bố mẹ luôn cố truyền các giá trị truyền thống và đạo đức tốt, nên những nguyên tắc đó được thấm nhuần trong tôi từ rất nhỏ.",
                ),
                (
                    f'Growing up, I really {_memo_join(v, "look up to")} my dad because I {_memo_join(v, "take after")} him a lot in terms of personality and mindset—people often look at us and say \'{_memo_join(v, "like father, like son")}\' since we share so many similar habits.',
                    "Lớn lên, tôi rất ngưỡng mộ bố vì tôi giống ông ấy nhiều về tính cách và tư duy — người ta thường nói “cha nào con nấy” vì chúng tôi có nhiều thói quen giống nhau.",
                ),
            ],
            "keys": [
                ("immediate family", "gia đình gần / gia đình ruột thịt", "v"),
                ("upbringing", "sự nuôi dưỡng, cách dạy dỗ", "v"),
                ("pass down traditional values", "truyền lại các giá trị truyền thống", "v"),
                ("instilled in me", "được thấm nhuần / truyền vào trong tôi từ nhỏ", "v"),
                ("look up to", "ngưỡng mộ, coi ai là tấm gương", "v"),
                ("take after", "giống người thân về tính cách hoặc ngoại hình", "v"),
                ("like father, like son", "cha nào con nấy", "v"),
            ],
        },
        "11": {
            "question": "Do you think a long-distance relationship is a good idea?",
            "sentences": [
                (
                    "Yes, I think so, though it really depends on the couple.",
                    "Tôi nghĩ vậy, dù còn tùy cặp đôi.",
                ),
                (
                    f'While some people believe strongly in {_memo_join(v, "love at first sight")}, I feel that initial {_memo_join(v, "attraction")} is often just physical and doesn\'t {_memo_join(v, "tell the full story")}.',
                    "Một số người tin mạnh vào tình yêu sét đánh, nhưng tôi thấy sự thu hút ban đầu thường chỉ là thể xác và không nói lên tất cả.",
                ),
                (
                    f'To build a truly {_memo_join(v, "harmonious")} connection, you need much more than that—it requires genuine {_memo_join(v, "chemistry")}, deep {_memo_join(v, "affection")}, and a solid {_memo_join(v, "commitment")}.',
                    "Để xây một mối liên kết thật sự hòa hợp, cần nhiều hơn thế — phải có chemistry, tình cảm sâu và sự cam kết vững.",
                ),
                (
                    f'For instance, a {_memo_join(v, "long-distance relationship")} can definitely succeed if both people trust each other, whereas hidden lies or a lack of effort can easily become a major {_memo_join(v, "deal-breaker")}.',
                    "Ví dụ, mối quan hệ yêu xa hoàn toàn có thể thành công nếu hai người tin nhau; còn giấu giếm hay thiếu nỗ lực dễ trở thành deal-breaker.",
                ),
            ],
            "keys": [
                ("love at first sight", "tình yêu sét đánh", "v"),
                ("attraction", "sự thu hút", "v"),
                ("tell the full story", "nói lên tất cả / phản ánh toàn bộ sự thật", "v"),
                ("harmonious", "hòa hợp", "v"),
                ("chemistry", "phản ứng hóa học / sự ăn ý", "v"),
                ("affection", "tình cảm, sự quý mến", "v"),
                ("commitment", "sự cam kết", "v"),
                ("long-distance relationship", "mối quan hệ yêu xa", "v"),
                ("deal-breaker", "điều khiến mối quan hệ đổ vỡ / không thể chấp nhận được", "v"),
            ],
        },
        "12": {
            "question": "Is it easy or difficult to make new friends nowadays?",
            "sentences": [
                (
                    f'Well, I think {_memo_join(s, "it\'s always quite difficult at the beginning when you try something new")}, and making new friends {_memo_join(s, "is not an exception")}.',
                    "Tôi nghĩ lúc đầu luôn khá khó khi thử điều gì mới, và kết bạn mới cũng không phải ngoại lệ.",
                ),
                (
                    f'At first, it takes a lot of time to find {_memo_join(v, "common ground")} with {_memo_join(v, "like-minded individuals")} and {_memo_join(v, "build a relationship")} from scratch.',
                    "Lúc đầu phải mất nhiều thời gian để tìm điểm chung với người cùng chí hướng và xây dựng mối quan hệ từ đầu.",
                ),
                (
                    f'However, after a while, things begin to get a bit easier once you connect over {_memo_join(v, "shared interests")}.',
                    "Sau một thời gian, mọi thứ dễ hơn khi các bạn kết nối nhờ sở thích chung.",
                ),
                (
                    f'It certainly takes effort to {_memo_join(v, "maintain a relationship")} and {_memo_join(v, "strengthen a relationship")}, but it is definitely worth it in the end.',
                    "Duy trì và củng cố mối quan hệ chắc chắn tốn công, nhưng cuối cùng rất đáng.",
                ),
            ],
            "keys": [
                ("it's always quite difficult at the beginning when you try something new", "Lúc đầu luôn khá khó khăn khi bạn thử làm điều gì mới", "s"),
                ("… is not an exception", "… cũng không phải ngoại lệ", "s"),
                ("common ground", "điểm chung", "v"),
                ("like-minded individuals", "những người cùng chí hướng", "v"),
                ("build a relationship", "xây dựng mối quan hệ", "v"),
                ("shared interests", "sở thích chung", "v"),
                ("maintain a relationship", "duy trì mối quan hệ", "v"),
                ("strengthen a relationship", "củng cố mối quan hệ", "v"),
            ],
        },
        "13": {
            "question": "Is there anything you don't really like about family gatherings or close relationships?",
            "sentences": [
                (
                    f'Well, {_memo_join(s, "generally speaking, I love")} spending time with my family, {_memo_join(s, "but the only thing I don\'t really like about it is")} when things get a bit {_memo_join(v, "complicated")}.',
                    "Nói chung tôi thích dành thời gian với gia đình, nhưng điều duy nhất tôi không thực sự thích là khi mọi thứ trở nên phức tạp.",
                ),
                (
                    f'Sometimes, having {_memo_join(v, "overprotective")} parents or dealing with unnecessary {_memo_join(v, "sibling rivalry")} can make the {_memo_join(v, "family bond")} feel a bit tense.',
                    "Đôi khi bố mẹ bảo bọc quá mức hoặc ganh đua anh chị em không cần thiết làm sợi dây gia đình căng hơn.",
                ),
                (
                    f'On top of that, {_memo_join(v, "miscommunication")} can easily happen, causing people to drift apart or even {_memo_join(v, "fall out with someone")}, leaving the relationship feeling quite {_memo_join(v, "distant")}.',
                    "Thêm nữa, hiểu lầm dễ xảy ra, khiến người ta dần xa hoặc thậm chí cắt đứt, để mối quan hệ trở nên xa cách.",
                ),
                (
                    f'{_memo_join(s, "Apart from that, I\'m fine")} with how things are.',
                    "Ngoài điều đó ra thì tôi thấy ổn.",
                ),
            ],
            "keys": [
                ("generally speaking, I love …, but the only thing I don't really like about … is …", "Nói chung là tôi thích…, nhưng điều duy nhất tôi không thực sự thích là…", "s"),
                ("complicated", "phức tạp", "v"),
                ("overprotective", "bảo bọc quá mức", "v"),
                ("sibling rivalry", "sự ganh đua giữa anh chị em", "v"),
                ("family bond", "sự gắn bó gia đình", "v"),
                ("miscommunication", "sự hiểu lầm do nói không rõ", "v"),
                ("fall out with someone", "cãi nhau / cắt đứt với ai", "v"),
                ("distant", "xa cách", "v"),
                ("Apart from that, I'm fine", "Ngoài điều đó ra thì tôi thấy ổn", "s"),
            ],
        },
        "14": {
            "question": "How often do you meet or catch up with your close friends?",
            "sentences": [
                (
                    f'Well, I usually catch up with my close friends {_memo_join(s, "at the weekend when none of us have to work")}.',
                    "Tôi thường gặp bạn thân vào cuối tuần khi không ai phải đi làm.",
                ),
                (
                    f'Even though we get quite busy with our own lives, we always {_memo_join(v, "make efforts to stay connected")} and {_memo_join(v, "keep in touch")} regularly.',
                    "Dù ai cũng bận việc riêng, chúng tôi luôn nỗ lực giữ liên lạc thường xuyên.",
                ),
                (
                    f'We try to meet {_memo_join(v, "every now and then")}—or at least once a month—just to {_memo_join(v, "keep each other updated")} on what\'s going on.',
                    "Chúng tôi cố gặp thỉnh thoảng — hoặc ít nhất mỗi tháng một lần — để cập nhật tình hình cho nhau.",
                ),
                (
                    f'Meeting them {_memo_join(v, "once in a blue moon")} is definitely not enough, because I really believe it is way too boring to stay isolated than to share real-life stories together.',
                    "Gặp năm thì mười họa là không đủ, vì tôi thấy ở một mình nhàm hơn nhiều so với việc kể chuyện đời thật cho nhau nghe.",
                ),
            ],
            "keys": [
                ("at the weekend when none of us have to work", "vào cuối tuần khi không ai trong chúng tôi phải đi làm", "s"),
                ("make efforts to stay connected", "nỗ lực giữ liên lạc", "v"),
                ("keep in touch", "giữ liên lạc", "v"),
                ("every now and then", "thỉnh thoảng", "v"),
                ("keep each other updated", "cập nhật tình hình cho nhau", "v"),
                ("once in a blue moon", "năm thì mười họa / rất hiếm khi", "v"),
            ],
        },
        "15": {
            "question": "How has family life changed in your country in recent years?",
            "sentences": [
                (
                    f'Well, I think family life {_memo_join(s, "has changed a great deal in recent years")}.',
                    "Tôi nghĩ đời sống gia đình đã thay đổi rất nhiều trong những năm gần đây.",
                ),
                (
                    f'In the past, people mostly lived in {_memo_join(v, "extended families under one roof")}, whereas nowadays there is {_memo_join(v, "a shift towards…")} {_memo_join(v, "nuclear households")}.',
                    "Trước đây người ta chủ yếu sống đại gia đình chung một mái nhà, còn nay có sự chuyển dịch hướng tới hộ hạt nhân.",
                ),
                (
                    f'Due to a {_memo_join(v, "fast-paced lifestyle")}, we tend to rely more on {_memo_join(v, "virtual interaction")} rather than regular {_memo_join(v, "face-to-face")} meetings.',
                    "Vì lối sống vội vã, chúng ta dựa nhiều hơn vào giao tiếp ảo thay vì gặp trực tiếp thường xuyên.",
                ),
                (
                    f'However, despite the rise of {_memo_join(v, "individualist values")}, strong {_memo_join(v, "family ties")} remain unchanged as members still support each other {_memo_join(v, "through thick and thin")}.',
                    "Dù giá trị cá nhân lên ngôi, mối quan hệ gia đình vẫn không đổi vì các thành viên vẫn đỡ nhau trong mọi hoàn cảnh.",
                ),
            ],
            "keys": [
                ("has changed a great deal in recent years", "đã thay đổi rất nhiều trong những năm gần đây", "s"),
                ("extended families under one roof", "đại gia đình sống chung dưới một mái nhà", "v"),
                ("a shift towards…", "sự chuyển dịch hướng tới…", "v"),
                ("nuclear households", "gia đình hạt nhân", "v"),
                ("fast-paced lifestyle", "lối sống vội vã", "v"),
                ("virtual interaction", "giao tiếp ảo", "v"),
                ("face-to-face", "gặp trực tiếp", "v"),
                ("individualist values", "giá trị cá nhân", "v"),
                ("family ties", "mối quan hệ gia đình", "v"),
                ("through thick and thin", "trong mọi hoàn cảnh / qua bao thăng trầm", "v"),
            ],
        },
    }


def _memo_join(fn, text: str) -> str:
    return fn(text)
