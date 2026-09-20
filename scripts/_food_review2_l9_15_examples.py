"""Expand/collapse vocab examples for Food & Drink Review Exercise 2 · Lessons 9–15.

Keys must match VOCABS terms in _food_review2_notes.py exactly.
"""
from __future__ import annotations

VOCAB_EXAMPLES: dict[str, dict[str, list[tuple[str, str]]]] = {
    "9": {
        "As far as I can remember, …": [
            (
                "As far as I can remember, the most memorable meal I ever had was a homemade bowl of soup when I was sick.",
                "Theo như tôi còn nhớ, bữa ăn đáng nhớ nhất mà tôi từng có là một bát súp nhà nấu lúc tôi bị ốm.",
            ),
            (
                "As far as I can remember, we used to gather for family dinners every single Sunday.",
                "Theo như tôi còn nhớ, chúng tôi từng quây quần cho các bữa cơm gia đình vào mọi Chủ nhật.",
            ),
            (
                "As far as I can remember, that Italian restaurant has always been famous for its authentic local specialities.",
                "Theo như tôi còn nhớ, nhà hàng Ý đó luôn nổi tiếng với các món đặc sản địa phương chính gốc.",
            ),
            (
                "As far as I can remember, I have always had a sweet tooth for chocolate cheesecakes.",
                "Theo như tôi còn nhớ, tôi vẫn luôn hảo ngọt các loại bánh cheesecake sô-cô-la.",
            ),
            (
                "As far as I can remember, my mother always made our meals from scratch using seasonal produce.",
                "Theo như tôi còn nhớ, mẹ tôi luôn tự tay chuẩn bị các bữa ăn từ nguyên liệu tươi theo mùa.",
            ),
        ],
        "left a mark on me": [
            (
                "That heartwarming homemade meal left a mark on me because it reminded me of my grandmother.",
                "Bữa cơm nhà ấm áp đó đã để lại dấu ấn sâu sắc trong tôi vì nó gợi cho tôi nhớ về bà của mình.",
            ),
            (
                "The unforgettable culinary experience during my trip to Hanoi truly left a mark on me.",
                "Trải nghiệm ẩm thực khó quên trong chuyến đi Hà Nội thực sự đã để lại dấu ấn sâu sắc trong tôi.",
            ),
            (
                "A simple yet wholesome bowl of soup can sometimes leave a mark on me more than luxury food.",
                "Một tô canh giản dị nhưng lành mạnh đôi khi để lại dấu ấn trong tôi nhiều hơn cả đồ ăn sang trọng.",
            ),
            (
                "The bold flavors and aromatic spices of that street dish left a mark on me.",
                "Hương vị đậm đà và các loại gia vị thơm nồng của món ăn đường phố đó đã để lại dấu ấn trong tôi.",
            ),
            (
                "Sharing a meal and catching up with old friends left a mark on me for a long time.",
                "Việc chia sẻ bữa ăn và trò chuyện cùng những người bạn cũ đã để lại dấu ấn trong tôi trong một thời gian dài.",
            ),
        ],
        "homemade meal": [
            (
                "Nothing can beat a warm homemade meal prepared by your mother when you are feeling sick.",
                "Không gì có thể đánh bại được một bữa ăn do nhà tự nấu ấm áp do mẹ chuẩn bị khi bạn cảm thấy ốm.",
            ),
            (
                "Eating a homemade meal allows me to stay in control of what I consume.",
                "Việc ăn một bữa ăn do nhà tự nấu cho phép tôi kiểm soát những gì mình tiêu thụ.",
            ),
            (
                "A homemade meal is usually much more wholesome and nutritious than dining out.",
                "Một bữa cơm nhà thường lành mạnh và giàu dinh dưỡng hơn nhiều so với việc đi ăn ngoài.",
            ),
            (
                "She loves preparing homemade meals from scratch using fresh ingredients.",
                "Cô ấy thích chuẩn bị các bữa ăn nhà làm hoàn toàn từ nguyên liệu tươi.",
            ),
            (
                "Whenever I travel far away, I always miss the comfort of a traditional homemade meal.",
                "Bất cứ khi nào đi du lịch xa, tôi luôn nhớ cảm giác thoải mái của một bữa cơm nhà truyền thống.",
            ),
        ],
        "bland porridge": [
            (
                "When I recovered from my fever, my mother fed me bland porridge before letting me eat solid food.",
                "Khi tôi khỏi sốt, mẹ tôi cho tôi ăn cháo nhạt trước khi để tôi ăn đồ ăn đặc.",
            ),
            (
                "Eating bland porridge for days while being sick made me crave some bold flavors.",
                "Việc ăn cháo nhạt trong nhiều ngày khi bị ốm khiến tôi khao khát một chút hương vị đậm đà.",
            ),
            (
                "Bland porridge is easy to digest, making it the perfect meal for patients.",
                "Cháo nhạt rất dễ tiêu hóa, biến nó thành bữa ăn hoàn hảo cho bệnh nhân.",
            ),
            (
                "Unlike mouth-watering dishes, bland porridge lacks seasoning and heavy spices.",
                "Không giống như các món ăn ngon kích thích vị giác, cháo nhạt thiếu đi sự nêm nếm và các loại gia vị đậm.",
            ),
            (
                "After eating bland porridge for a week, a hearty bowl of phở felt like heaven.",
                "Sau khi ăn cháo nhạt suốt một tuần, một tô phở thịnh soạn có cảm giác tuyệt vời như ở thiên đường.",
            ),
        ],
        "topped with": [
            (
                "The delicious bowl of noodles was topped with fresh herbs, beef slices, and spring onions.",
                "Tô mì thơm ngon được phủ lên trên bằng rau thơm tươi, các lát thịt bò và hành lá.",
            ),
            (
                "A warm slice of cheesecake can be topped with sweet berry sauce.",
                "Một miếng bánh cheesecake ấm áp có thể được phủ lên trên bằng sốt quả mọng ngọt ngào.",
            ),
            (
                "The pizza was generously topped with melted cheese and mushrooms.",
                "Chiếc bánh pizza được phủ đầy phô mai tan chảy và nấm lên trên.",
            ),
            (
                "This traditional dessert is usually topped with roasted peanuts and coconut milk.",
                "Món tráng miệng truyền thống này thường được phủ đậu phộng rang và nước cốt dừa lên trên.",
            ),
            (
                "A wholesome bowl of soup topped with crispy garlic adds a wonderful layer of flavor.",
                "Một tô canh lành mạnh được phủ tỏi phi giòn lên trên mang lại một tầng hương vị tuyệt vời.",
            ),
        ],
        "delicacies": [
            (
                "The high-end restaurant is famous for serving Italian delicacies like handmade pasta and risotto.",
                "Nhà hàng cao cấp nổi tiếng với việc phục vụ các món ngon ẩm thực Ý như mì làm thủ công và cơm Ý risotto.",
            ),
            (
                "Foreign foodies love exploring local delicacies when visiting different regions in Asia.",
                "Những người mê ẩm thực nước ngoài rất thích khám phá các món ngon địa phương khi ghé thăm các vùng miền khác nhau ở châu Á.",
            ),
            (
                "We decided to treat ourselves to some seafood delicacies on our wedding anniversary.",
                "Chúng tôi quyết định tự thưởng cho mình một vài món ngon hải sản vào dịp kỷ niệm ngày cưới.",
            ),
            (
                "Preparing these culinary delicacies requires great cooking skills and fresh seasonal produce.",
                "Việc chuẩn bị những món ngon ẩm thực này đòi hỏi kỹ năng nấu nướng tuyệt vời và nông sản tươi theo mùa.",
            ),
            (
                "Tasting regional delicacies is an essential part of any meaningful culinary experience.",
                "Thưởng thức các món ngon vùng miền là một phần thiết yếu của bất kỳ trải nghiệm ẩm thực ý nghĩa nào.",
            ),
        ],
        "make my mouth water": [
            (
                "Just the smell of garlic and butter cooking in the pan can make my mouth water.",
                "Chỉ cần ngửi mùi tỏi và bơ đang nấu trong chảo cũng đủ khiến tôi thèm thuồng chảy nước miếng.",
            ),
            (
                "Looking at those mouth-watering pictures of chocolate cheesecake always makes my mouth water.",
                "Nhìn vào những bức ảnh bánh cheesecake sô-cô-la hấp dẫn đó lúc nào cũng khiến tôi thèm thuồng.",
            ),
            (
                "The aromatic scent of grilled street food was enough to make my mouth water.",
                "Mùi hương thơm nồng của đồ ăn đường phố nướng đủ sức khiến tôi thèm thuồng.",
            ),
            (
                "Thinking about a hot, well-seasoned bowl of phở instantly makes my mouth water.",
                "Nghĩ đến một tô phở nóng hổi, nêm nếm đậm đà ngay lập tức khiến tôi thèm thuồng.",
            ),
            (
                "Watching cooking shows late at night never fails to make my mouth water.",
                "Xem các chương trình nấu ăn vào đêm muộn chưa bao giờ thất bại trong việc khiến tôi thèm ăn.",
            ),
        ],
        "slap-up meal": [
            (
                "We decided to celebrate our graduation by having a slap-up meal at a luxury restaurant downtown.",
                "Chúng tôi quyết định ăn mừng lễ tốt nghiệp bằng cách có một bữa ăn thịnh soạn tại một nhà hàng sang trọng ở trung tâm thành phố.",
            ),
            (
                "After finishing the project, the team was treated to a slap-up meal with wine and dine.",
                "Sau khi hoàn thành dự án, cả đội được chiêu đãi một bữa ăn thịnh soạn đi kèm rượu và các món sang trọng.",
            ),
            (
                "Birthdays are great occasions to enjoy a slap-up meal with your loved ones.",
                "Sinh nhật là những dịp tuyệt vời để tận hưởng một bữa ăn thịnh soạn cùng những người thân yêu.",
            ),
            (
                "Instead of cooking at home, they opted for a slap-up meal to spice things up.",
                "Thay vì nấu ăn ở nhà, họ đã chọn một bữa ăn thịnh soạn để đổi gió.",
            ),
            (
                "Quality justifies the bill when you are paying for such a slap-up meal.",
                "Chất lượng hoàn toàn xứng đáng với hóa đơn khi bạn đang trả tiền cho một bữa ăn thịnh soạn như vậy.",
            ),
        ],
        "recount": [
            (
                "I would like to recount a memorable meal I had at a small family restaurant in Hanoi.",
                "Tôi muốn kể lại một bữa ăn đáng nhớ mà tôi từng có tại một nhà hàng gia đình nhỏ ở Hà Nội.",
            ),
            (
                "My grandfather loves to recount stories about traditional cuisine from his childhood.",
                "Ông tôi rất thích kể lại những câu chuyện về ẩm thực truyền thống từ thời thơ ấu của ông.",
            ),
            (
                "During dinner, we gathered around to recount funny moments from our trip.",
                "Trong bữa tối, chúng tôi quây quần bên nhau để kể lại những khoảnh khắc hài hước từ chuyến đi của mình.",
            ),
            (
                "The food blogger used his vlog to recount his culinary experiences across Asia.",
                "Blogger ẩm thực đã dùng vlog của mình để thuật lại những trải nghiệm ẩm thực khắp châu Á.",
            ),
            (
                "She began to recount how she learned to cook wholesome meals from scratch.",
                "Cô ấy bắt đầu kể lại cách cô học nấu những bữa ăn lành mạnh từ nguyên liệu tươi từ đầu.",
            ),
        ],
    },
    "10": {
        "fussy eater / picky eater": [
            (
                "As a child, I used to be a very fussy eater who always complained about eating vegetables.",
                "Khi còn nhỏ, tôi từng là một người rất kén ăn, người luôn phàn nàn về việc ăn rau củ.",
            ),
            (
                "Being a picky eater, he would only eat chicken nuggets and turn his nose up at healthy food.",
                "Là một kẻ kén ăn, cậu ấy chỉ chịu ăn bánh gà viên và chê bai đồ ăn lành mạnh.",
            ),
            (
                "Parents often struggle to prepare meals when their children are fussy eaters.",
                "Cha mẹ thường gặp khó khăn trong việc chuẩn bị bữa ăn khi con cái họ là những đứa trẻ kén ăn.",
            ),
            (
                "Overcoming being a picky eater takes time as your palate gradually matures.",
                "Việc vượt qua tính kén ăn cần có thời gian khi khẩu vị của bạn dần trưởng thành hơn.",
            ),
            (
                "Unlike my brother who is a fussy eater, I love trying out authentic local specialities.",
                "Không giống như anh trai tôi, người vốn kén ăn, tôi rất thích thử các món đặc sản địa phương chính gốc.",
            ),
        ],
        "turn my nose up at": [
            (
                "When I was little, I used to turn my nose up at green vegetables like broccoli and spinach.",
                "Khi còn nhỏ, tôi từng tỏ thái độ chê bai các loại rau xanh như bông cải xanh và rau bina.",
            ),
            (
                "You shouldn't turn your nose up at a wholesome home-cooked meal just because it looks simple.",
                "Bạn không nên chê bai một bữa cơm nhà lành mạnh chỉ vì trông nó có vẻ giản dị.",
            ),
            (
                "He would always turn his nose up at bland porridge when he wanted something sweet.",
                "Cậu ấy thường hay chê bai món cháo nhạt khi bản thân lại muốn ăn một thứ gì đó ngọt ngào.",
            ),
            (
                "As my palate matured, I stopped turning my nose up at traditional cuisine containing herbs.",
                "Khi khẩu vị trưởng thành hơn, tôi đã ngừng chê bai các món ăn truyền thống chứa rau thơm.",
            ),
            (
                "Don't turn your nose up at foreign cuisine before you even give it a try.",
                "Đừng vội chê bai ẩm thực nước ngoài trước khi bạn thậm chí còn chưa cho nó một cơ hội.",
            ),
        ],
        "wolf down": [
            (
                "Whenever my mother baked sweet cheesecakes, I would wolf them down in seconds.",
                "Bất cứ khi nào mẹ tôi nướng bánh cheesecake ngọt ngào, tôi đều ăn ngấu nghiến chúng trong vài giây.",
            ),
            (
                "After playing football all afternoon, the kids wolfed down their meals hungrily.",
                "Sau khi đá bóng suốt cả buổi chiều, lũ trẻ đã ăn ngấu nghiến bữa ăn của chúng một cách đói khát.",
            ),
            (
                "Instead of bolting your food down or wolfing down snacks, try to eat mindfully.",
                "Thay vì nuốt chửng đồ ăn hay ăn ngấu nghiến đồ ăn vặt, hãy cố gắng ăn uống có ý thức.",
            ),
            (
                "He was so starving that he wolfed down a hearty plate of pasta right away.",
                "Cậu ấy đói đến mức đã ăn ngấu nghiến một đĩa mì Ý thịnh soạn ngay lập tức.",
            ),
            (
                "Children often wolf down fast food because of its heavy seasoning and bold flavors.",
                "Trẻ em thường ăn ngấu nghiến đồ ăn nhanh vì lớp gia vị đậm và hương vị đậm đà của nó.",
            ),
        ],
        "pester": [
            (
                "When I was a kid, I used to pester my parents to buy me candies and sugary drinks at the supermarket.",
                "Khi còn là một đứa trẻ, tôi thường nài nỉ bố mẹ mua cho mình kẹo và đồ uống có đường ở siêu thị.",
            ),
            (
                "Children frequently pester adults for junk food instead of eating wholesome meals.",
                "Trẻ em thường xuyên vòi vĩnh người lớn đòi đồ ăn vặt thay vì ăn các bữa ăn lành mạnh.",
            ),
            (
                "Instead of pestering for processed snacks, she learned to enjoy seasonal fruits.",
                "Thay vì nài nỉ đòi đồ ăn vặt chế biến sẵn, cô ấy đã học cách thưởng thức trái cây theo mùa.",
            ),
            (
                "Parents shouldn't give in when their children pester them for unhealthy treats.",
                "Cha mẹ không nên nhượng bộ khi con cái họ nài nỉ đòi những món quà vặt không lành mạnh.",
            ),
            (
                "I used to pester my grandmother to bake my favorite chocolate cake from scratch.",
                "Tôi từng nài nỉ bà mình tự tay nướng chiếc bánh sô-cô-la yêu thích từ đầu.",
            ),
        ],
        "palate (has matured)": [
            (
                "As I grew older, my palate has matured, and I now enjoy the bitter taste of fresh vegetables.",
                "Khi tôi lớn hơn, khẩu vị đã trưởng thành hơn, và giờ đây tôi thích vị đắng của rau tươi.",
            ),
            (
                "My palate has matured significantly, allowing me to appreciate bold flavors and aromatic spices.",
                "Khẩu vị của tôi đã trưởng thành đáng kể, cho phép tôi cảm nhận được hương vị đậm đà và các loại gia vị thơm nồng.",
            ),
            (
                "Once your palate has matured, you will stop turning your nose up at traditional cuisine.",
                "Một khi khẩu vị đã trưởng thành, bạn sẽ ngừng việc chê bai ẩm thực truyền thống.",
            ),
            (
                "A mature palate helps foodies explore exotic local specialities without hesitation.",
                "Một khẩu vị trưởng thành giúp những người mê ẩm thực khám phá các đặc sản địa phương lạ miệng mà không do dự.",
            ),
            (
                "Her palate has matured over the years, shifting from sweet snacks to balanced, nutritious diets.",
                "Khẩu vị của cô ấy đã trưởng thành qua nhiều năm, chuyển dịch từ các món ăn vặt ngọt sang chế độ ăn uống cân bằng, giàu dinh dưỡng.",
            ),
        ],
        "acquired taste": [
            (
                "Eating bitter greens like spinach is often an acquired taste that you learn to love over time.",
                "Ăn các loại rau đắng như rau bina thường là một sở thích hình thành theo thời gian mà bạn học cách yêu thích qua năm tháng.",
            ),
            (
                "Strong-flavored cheese and black coffee are classic examples of an acquired taste.",
                "Phô mai vị nồng và cà phê đen là những ví dụ kinh điển về một khẩu vị cần thời gian để làm quen.",
            ),
            (
                "At first, I hated spicy food, but it became an acquired taste as I broadened my palate.",
                "Ban đầu, tôi ghét đồ ăn cay, nhưng nó dần trở thành món tôi thích theo thời gian khi tôi mở rộng khẩu vị.",
            ),
            (
                "Appreciating traditional fermented dishes is often an acquired taste for foreign visitors.",
                "Việc thưởng thức các món lên men truyền thống thường là một sở thích cần thời gian làm quen đối với du khách nước ngoài.",
            ),
            (
                "Bitter melon soup may seem unappealing initially, but it is an acquired taste with great health benefits.",
                "Canh khổ qua có vẻ kém hấp dẫn lúc ban đầu, nhưng đó là món ăn có khẩu vị tích lũy mang lại lợi ích sức khỏe tuyệt vời.",
            ),
        ],
        "snack on junk food": [
            (
                "Before deciding to eat clean, I used to snack on junk food while watching television late at night.",
                "Trước khi quyết định ăn sạch, tôi từng có thói quen ăn vặt đồ junk food trong lúc xem TV vào đêm khuya.",
            ),
            (
                "Snacking on junk food can easily lead to feeling sluggish and pose serious health risks.",
                "Việc ăn vặt đồ ăn nhanh có thể dễ dàng dẫn đến cảm giác mệt mỏi và gây ra rủi ro sức khỏe nghiêm trọng.",
            ),
            (
                "To stay in control of what I consume, I stopped snacking on junk food between meals.",
                "Để kiểm soát những gì mình tiêu thụ, tôi đã ngưng thói quen ăn vặt đồ không lành mạnh giữa các bữa ăn.",
            ),
            (
                "Children who frequently snack on junk food often lose their appetite for wholesome home-cooked dinners.",
                "Những đứa trẻ thường xuyên ăn vặt đồ không lành mạnh thường mất cảm giác thèm ăn cho bữa tối gia đình lành mạnh.",
            ),
            (
                "Replacing the habit of snacking on junk food with seasonal fruits is a great step toward a balanced diet.",
                "Thay thế thói quen ăn vặt đồ junk food bằng trái cây theo mùa là một bước tiến tuyệt vời hướng tới chế độ ăn cân bằng.",
            ),
        ],
        "eat clean / stick to a balanced diet": [
            (
                "As I entered adulthood, I decided to eat clean and stick to a balanced diet to protect my health.",
                "Khi bước vào tuổi trưởng thành, tôi quyết định ăn sạch và duy trì chế độ ăn uống cân bằng để bảo vệ sức khỏe của mình.",
            ),
            (
                "Choosing to eat clean means cutting down on processed foods and reducing sugar intake.",
                "Việc lựa chọn ăn sạch đồng nghĩa với việc cắt giảm thực phẩm chế biến sẵn và giảm lượng đường nạp vào.",
            ),
            (
                "People who stick to a balanced diet usually feel more energetic throughout the working day.",
                "Những người duy trì chế độ ăn uống cân bằng thường cảm thấy tràn đầy năng lượng hơn suốt cả ngày làm việc.",
            ),
            (
                "It is much easier to eat clean when you prepare your wholesome meals from scratch at home.",
                "Việc ăn sạch sẽ dễ dàng hơn rất nhiều khi bạn tự tay chuẩn bị các bữa ăn lành mạnh từ đầu tại nhà.",
            ),
            (
                "To avoid health risks, she tries to eat clean and stick to a balanced diet despite having a sweet tooth.",
                "Để tránh rủi ro sức khỏe, cô ấy cố gắng ăn sạch và duy trì chế độ ăn cân bằng dù bản thân là người hảo ngọt.",
            ),
        ],
        "cut down on processed foods": [
            (
                "I started to cut down on processed foods when I noticed packaged snacks made me feel sluggish.",
                "Tôi bắt đầu cắt giảm thực phẩm chế biến sẵn khi nhận ra đồ ăn đóng gói khiến tôi uể oải.",
            ),
            (
                "Being health-conscious as I grow older, I actively cut down on processed foods and sugary drinks.",
                "Trở nên ý thức hơn về sức khỏe khi lớn lên, tôi chủ động cắt giảm thực phẩm chế biến sẵn và đồ uống có đường.",
            ),
            (
                "Cutting down on processed foods is essential if you want to avoid long-term chronic health issues.",
                "Việc cắt giảm thực phẩm chế biến sẵn là điều thiết yếu nếu bạn muốn tránh các vấn đề sức khỏe mãn tính lâu dài.",
            ),
            (
                "Instead of buying packaged meals, she cuts down on processed foods by cooking fresh ingredients.",
                "Thay vì mua các bữa ăn đóng gói sẵn, cô ấy cắt giảm đồ chế biến sẵn bằng cách nấu các nguyên liệu tươi.",
            ),
            (
                "Doctors always advise patients to cut down on processed foods to maintain a wholesome lifestyle.",
                "Các bác sĩ luôn khuyên bệnh nhân nên cắt giảm thực phẩm chế biến sẵn để duy trì lối sống lành mạnh.",
            ),
        ],
    },
    "11": {
        "balanced diet / well-balanced meal": [
            (
                "Maintaining a balanced diet consisting of protein, fiber, and vitamins is essential for everyone's well-being.",
                "Duy trì một chế độ ăn cân bằng gồm protein, chất xơ và vitamin là điều thiết yếu cho sức khỏe của mọi người.",
            ),
            (
                "Instead of eating less to lose weight, you should focus on eating a well-balanced meal every day.",
                "Thay vì ăn ít đi để giảm cân, bạn nên tập trung vào việc ăn một bữa ăn cân bằng đầy đủ dưỡng chất mỗi ngày.",
            ),
            (
                "A balanced diet helps you stay energized and prevents you from feeling sluggish after meals.",
                "Một chế độ ăn cân bằng giúp bạn luôn tràn đầy năng lượng và tránh cảm giác uể oải sau các bữa ăn.",
            ),
            (
                "People who stick to a balanced diet rarely suffer from chronic diseases as they grow older.",
                "Những người duy trì chế độ ăn cân bằng hiếm khi mắc các bệnh mãn tính khi họ lớn tuổi hơn.",
            ),
            (
                "Cooking at home makes it much easier to prepare a well-balanced meal tailored to your personal needs.",
                "Nấu ăn tại nhà giúp bạn dễ dàng chuẩn bị một bữa ăn cân bằng được điều chỉnh theo nhu cầu cá nhân.",
            ),
        ],
        "health-conscious": [
            (
                "Being health-conscious, I always check the ingredient labels before purchasing packaged food at the supermarket.",
                "Là một người có ý thức về sức khỏe, tôi luôn kiểm tra nhãn thành phần trước khi mua thực phẩm đóng gói trong siêu thị.",
            ),
            (
                "Health-conscious individuals usually prefer steering clear of deep-fried dishes and sugary beverages.",
                "Những cá nhân có ý thức sức khỏe thường thích tránh xa các món chiên ngập dầu và đồ uống có đường.",
            ),
            (
                "As I became more health-conscious, I started cutting down on processed foods and snacking on fruits.",
                "Khi tôi trở nên quan tâm đến sức khỏe hơn, tôi bắt đầu cắt giảm thực phẩm chế biến sẵn và ăn vặt bằng trái cây.",
            ),
            (
                "Restaurants are now offering more organic options to cater to health-conscious customers.",
                "Các nhà hàng hiện đang cung cấp nhiều lựa chọn hữu cơ hơn để phục vụ khách hàng có ý thức về sức khỏe.",
            ),
            (
                "A health-conscious lifestyle requires you to stay in control of what you consume daily.",
                "Lối sống có ý thức về sức khỏe đòi hỏi bạn phải kiểm soát những gì mình tiêu thụ hàng ngày.",
            ),
        ],
        "nutritious foods": [
            (
                "Eating nutritious foods like fresh vegetables, fish, and whole grains provides fuel for both body and mind.",
                "Việc ăn các thực phẩm bổ dưỡng như rau tươi, cá và ngũ cốc nguyên hạt cung cấp năng lượng cho cả thể chất lẫn tinh thần.",
            ),
            (
                "Parents should encourage their children to consume nutritious foods instead of craving fast food.",
                "Cha mẹ nên khuyến khích con cái tiêu thụ thực phẩm bổ dưỡng thay vì thèm thuồng đồ ăn nhanh.",
            ),
            (
                "Nutritious foods play a crucial role in strengthening your immune system against illnesses.",
                "Thực phẩm bổ dưỡng đóng vai trò cốt lõi trong việc tăng cường hệ miễn dịch chống lại bệnh tật.",
            ),
            (
                "Cooking wholesome meals from scratch is the best way to enjoy nutritious foods at home.",
                "Nấu các bữa ăn lành mạnh từ đầu là cách tốt nhất để thưởng thức thực phẩm bổ dưỡng tại nhà.",
            ),
            (
                "Buying seasonal produce is an affordable way to add nutritious foods to your daily diet.",
                "Mua nông sản theo mùa là một cách tiết kiệm để bổ sung thực phẩm bổ dưỡng vào chế độ ăn hàng ngày.",
            ),
        ],
        "pose a health risk": [
            (
                "Consuming fast food on a regular basis can pose a health risk and lead to severe medical issues.",
                "Việc tiêu thụ đồ ăn nhanh thường xuyên có thể gây ra rủi ro sức khỏe và dẫn đến các vấn đề y tế nghiêm trọng.",
            ),
            (
                "Unchecked lifestyles and lack of exercise together pose a serious health risk for office workers.",
                "Lối sống thiếu kiểm soát và lười vận động kết hợp lại gây ra rủi ro sức khỏe nghiêm trọng cho nhân viên văn phòng.",
            ),
            (
                "Habits like snacking on junk food late at night definitely pose a health risk in the long run.",
                "Những thói quen như ăn vặt đồ không lành mạnh vào đêm khuya chắc chắn sẽ gây rủi ro sức khỏe về lâu dài.",
            ),
            (
                "Ignorance regarding food safety can pose a health risk to consumers everywhere.",
                "Sự thiếu hiểu biết về an toàn thực phẩm có thể gây rủi ro sức khỏe cho người tiêu dùng ở mọi nơi.",
            ),
            (
                "To avoid actions that pose a health risk, we should stick to a clean, balanced diet.",
                "Để tránh những hành động gây rủi ro cho sức khỏe, chúng ta nên tuân thủ chế độ ăn sạch và cân bằng.",
            ),
        ],
        "sluggish": [
            (
                "Eating too much heavy junk food often makes me feel sluggish and unproductive in the afternoon.",
                "Ăn quá nhiều đồ ăn vặt nặng bụng thường khiến tôi cảm thấy uể oải và kém năng suất vào buổi chiều.",
            ),
            (
                "After a sleepless night and a poor breakfast, I felt completely sluggish during the meeting.",
                "Sau một đêm mất ngủ và bữa sáng kém chất lượng, tôi cảm thấy hoàn toàn uể oải trong suốt cuộc họp.",
            ),
            (
                "Drinking enough water and eating nutritious foods help you avoid feeling sluggish throughout the day.",
                "Uống đủ nước và ăn thực phẩm bổ dưỡng giúp bạn tránh cảm giác mệt mỏi, uể oải suốt cả ngày.",
            ),
            (
                "Instead of feeling sluggish, a wholesome breakfast gave him plenty of energy to work out.",
                "Thay vì cảm thấy uể oải, một bữa sáng lành mạnh đã mang lại cho anh ấy tràn ngập năng lượng để tập luyện.",
            ),
            (
                "Overeating during festive holidays can easily leave you feeling sluggish and tired.",
                "Việc ăn quá độ trong các dịp lễ hội có thể dễ dàng khiến bạn cảm thấy nặng nề và mệt mỏi.",
            ),
        ],
        "immune system / chronic diseases": [
            (
                "Eating a balanced diet rich in vitamins helps strengthen your immune system naturally.",
                "Việc ăn chế độ ăn cân bằng giàu vitamin giúp tăng cường hệ miễn dịch của bạn một cách tự nhiên.",
            ),
            (
                "Poor eating habits and heavy fast food consumption can increase the risk of developing chronic diseases later in life.",
                "Thói quen ăn uống kém và tiêu thụ nhiều đồ ăn nhanh có thể làm tăng nguy cơ phát triển các bệnh mãn tính sau này trong đời.",
            ),
            (
                "A strong immune system is your best defense against seasonal flu and infections.",
                "Hệ miễn dịch mạnh mẽ là sự bảo vệ tốt nhất của bạn chống lại cúm mùa và các bệnh nhiễm trùng.",
            ),
            (
                "Cutting down on processed foods is a proven way to prevent lifestyle-related chronic diseases.",
                "Cắt giảm thực phẩm chế biến sẵn là một cách đã được chứng minh để phòng ngừa các bệnh mãn tính liên quan đến lối sống.",
            ),
            (
                "Nourishing your body with wholesome meals protects both your immune system and long-term health.",
                "Nuôi dưỡng cơ thể bằng các bữa ăn lành mạnh giúp bảo vệ cả hệ miễn dịch lẫn sức khỏe lâu dài của bạn.",
            ),
        ],
        "steer clear of": [
            (
                "To maintain a healthy weight, I try to steer clear of sugary drinks and midnight snacks.",
                "Để duy trì cân nặng lành mạnh, tôi cố gắng tránh xa các loại đồ uống có đường và món ăn vặt đêm khuya.",
            ),
            (
                "Health-conscious people usually steer clear of processed foods that pose health risks.",
                "Những người có ý thức về sức khỏe thường tránh xa các thực phẩm chế biến sẵn gây rủi ro sức khỏe.",
            ),
            (
                "The doctor advised him to steer clear of oily dishes to lower his cholesterol levels.",
                "Bác sĩ khuyên anh ấy nên tránh xa các món ăn nhiều dầu mỡ để hạ mức cholesterol.",
            ),
            (
                "If you want to eat clean, you must learn to steer clear of junk food sections in supermarkets.",
                "Nếu bạn muốn ăn sạch, bạn phải học cách tránh xa các khu vực đồ ăn vặt trong siêu thị.",
            ),
            (
                "She steers clear of dairy products because of her sensitive stomach.",
                "Cô ấy tránh xa các sản phẩm từ sữa vì dạ dày của cô ấy khá nhạy cảm.",
            ),
        ],
        "that said": [
            (
                "Fast food is undeniably cheap and convenient; that said, it lacks essential nutrients for the body.",
                "Đồ ăn nhanh không thể phủ nhận là rẻ và tiện lợi; tuy nhiên, nó lại thiếu các chất dinh dưỡng thiết yếu cho cơ thể.",
            ),
            (
                "Cooking at home takes time and effort; that said, the health benefits are totally worth it.",
                "Nấu ăn ở nhà tốn thời gian và công sức; tuy nhiên, những lợi ích sức khỏe hoàn toàn rất đáng giá.",
            ),
            (
                "I prefer eating clean on weekdays; that said, I occasionally treat myself on weekends.",
                "Tôi thích ăn sạch vào các ngày trong tuần; tuy nhiên, thỉnh thoảng tôi vẫn tự thưởng cho bản thân vào cuối tuần.",
            ),
            (
                "Vegan diets can be very wholesome; that said, planning them properly requires patience.",
                "Chế độ ăn thuần chay có thể rất lành mạnh; tuy nhiên, việc lên kế hoạch cho chúng một cách đúng đắn đòi hỏi sự kiên nhẫn.",
            ),
            (
                "The restaurant was crowded and noisy; that said, the food quality justified the bill.",
                "Nhà hàng rất đông đúc và ồn ào; tuy nhiên, chất lượng món ăn hoàn toàn tương xứng với giá tiền.",
            ),
        ],
        "a piece of cake": [
            (
                "Learning how to cook a basic bowl of rice is a piece of cake for most adults.",
                "Học cách nấu một nồi cơm cơ bản là chuyện dễ như ăn kẹo đối với hầu hết người lớn.",
            ),
            (
                "Sticking to a strict diet and avoiding all sweets is definitely not a piece of cake.",
                "Việc tuân thủ chế độ ăn kiêng nghiêm ngặt và tránh mọi món ngọt chắc chắn không hề dễ dàng chút nào.",
            ),
            (
                "Transitioning to a vegan lifestyle sounds simple, but trust me, it is not a piece of cake.",
                "Chuyển sang lối sống thuần chay nghe có vẻ đơn giản, nhưng hãy tin tôi, nó không hề dễ dàng đâu.",
            ),
            (
                "Passing the basic cooking test turned out to be a piece of cake thanks to my mother's guidance.",
                "Việc vượt qua bài kiểm tra nấu ăn cơ bản hóa ra lại dễ như ăn kẹo nhờ sự hướng dẫn của mẹ tôi.",
            ),
            (
                "Making meals from scratch isn't always a piece of cake, but the wholesome taste makes it worthwhile.",
                "Làm món ăn từ đầu không phải lúc nào cũng dễ dàng, nhưng hương vị lành mạnh khiến nó trở nên rất đáng giá.",
            ),
        ],
        "take my health for granted": [
            (
                "When I was younger, I used to take my health for granted and ate whatever junk food I liked.",
                "Khi còn trẻ, tôi từng xem nhẹ sức khỏe của mình và ăn bất kỳ món đồ ăn vặt nào tôi thích.",
            ),
            (
                "You shouldn't take your health for granted by staying up late and skipping wholesome meals.",
                "Bạn không nên xem nhẹ sức khỏe bằng cách thức khuya và bỏ bê các bữa ăn lành mạnh.",
            ),
            (
                "Many young people take their health for granted until they experience chronic health issues.",
                "Nhiều người trẻ tuổi thường xem nhẹ sức khỏe cho đến khi họ gặp phải các vấn đề sức khỏe mãn tính.",
            ),
            (
                "Facing a minor illness made me realize I shouldn't have taken my health for granted.",
                "Đối mặt với một cơn bệnh nhẹ đã khiến tôi nhận ra mình không nên xem nhẹ sức khỏe.",
            ),
            (
                "Now that I am more health-conscious, I no longer take my physical well-being for granted.",
                "Giờ đây khi đã có ý thức hơn về sức khỏe, tôi không còn xem nhẹ thể trạng của mình nữa.",
            ),
        ],
    },
    "12": {
        "it's always quite difficult at the beginning when you try something new": [
            (
                "It's always quite difficult at the beginning when you try something new, especially when you step into the kitchen for the first time.",
                "Lúc đầu luôn khá khó khăn khi bạn thử một điều gì đó mới, đặc biệt là khi bạn bước vào bếp lần đầu tiên.",
            ),
            (
                "Learning to cook wholesome meals from scratch can feel overwhelming because it's always quite difficult at the beginning when you try something new.",
                "Học nấu những bữa ăn lành mạnh từ đầu có thể gây choáng ngợp vì lúc đầu luôn khá khó khi thử điều mới.",
            ),
            (
                "It's always quite difficult at the beginning when you try something new, but practice makes perfect.",
                "Lúc đầu luôn khá khó khăn khi bạn thử một điều mới, nhưng có công mài sắt có ngày nên kim.",
            ),
            (
                "Switching to a balanced diet is tough since it's always quite difficult at the beginning when you try something new.",
                "Chuyển sang chế độ ăn cân bằng rất chông gai vì lúc đầu luôn khá khó khăn khi thử điều mới.",
            ),
            (
                "Don't give up on baking; remember that it's always quite difficult at the beginning when you try something new.",
                "Đừng từ bỏ việc làm bánh; hãy nhớ rằng lúc đầu luôn khá khó khi bạn thử thứ gì đó mới mẻ.",
            ),
        ],
        "… is not an exception": [
            (
                "Cooking well is not an exception; it requires a great deal of patience and regular practice.",
                "Nấu ăn ngon cũng không phải là ngoại lệ; nó đòi hỏi rất nhiều sự kiên nhẫn và luyện tập thường xuyên.",
            ),
            (
                "Mastering traditional culinary delicacies is not an exception to the rule of hard work.",
                "Làm chủ các món ngon ẩm thực truyền thống cũng không phải là ngoại lệ đối với quy luật chăm chỉ.",
            ),
            (
                "Learning to prep vegetables quickly is not an exception when you want to become an efficient cook.",
                "Học cách sơ chế rau củ nhanh chóng cũng không phải ngoại lệ khi bạn muốn trở thành một đầu bếp thành thạo.",
            ),
            (
                "Transitioning to a health-conscious lifestyle is not an exception; everyone faces struggles at first.",
                "Chuyển sang lối sống có ý thức về sức khỏe cũng không phải ngoại lệ; ai cũng gặp khó khăn lúc đầu.",
            ),
            (
                "Even professional chefs make mistakes, and my recent cooking failure is not an exception.",
                "Ngay cả các đầu bếp chuyên nghiệp cũng mắc sai lầm, và thất bại nấu nướng gần đây của tôi cũng không phải là ngoại lệ.",
            ),
        ],
        "follow a recipe": [
            (
                "When trying a new dish for the first time, I always follow a recipe carefully from a cooking blog.",
                "Khi thử một món ăn mới lần đầu tiên, tôi luôn làm theo công thức một cách cẩn thận từ một blog nấu ăn.",
            ),
            (
                "You don't necessarily have to follow a recipe strictly; sometimes improvisation makes the dish better.",
                "Bạn không nhất thiết phải làm theo công thức một cách cứng nhắc; đôi khi sự ứng biến giúp món ăn ngon hơn.",
            ),
            (
                "Beginners should follow a recipe step-by-step to avoid ruining expensive seasonal produce.",
                "Người mới bắt đầu nên làm theo công thức từng bước một để tránh làm hỏng nông sản theo mùa đắt tiền.",
            ),
            (
                "She learned how to bake delicious cheesecakes just by reading and following a recipe online.",
                "Cô ấy học cách nướng bánh cheesecake ngon chỉ bằng cách đọc và làm theo công thức trên mạng.",
            ),
            (
                "It's hard to replicate my grandmother's homemade meal because she never uses or follows a recipe.",
                "Thật khó để tái tạo bữa cơm nhà của bà tôi vì bà không bao giờ dùng hay làm theo công thức nào cả.",
            ),
        ],
        "cook from scratch": [
            (
                "Preparing a meal from scratch takes more time than using canned food, but it lets you stay in control of what you consume.",
                "Chuẩn bị một bữa ăn nấu từ nguyên liệu tươi tốn nhiều thời gian hơn dùng đồ hộp, nhưng nó giúp bạn kiểm soát được những gì mình tiêu thụ.",
            ),
            (
                "Health-conscious people prefer to cook from scratch to avoid hidden processed ingredients.",
                "Những người có ý thức về sức khỏe thích nấu ăn từ nguyên liệu tươi từ đầu để tránh các thành phần chế biến ẩn giấu.",
            ),
            (
                "Learning how to cook from scratch is a rewarding skill for anyone who loves wholesome food.",
                "Học cách nấu ăn từ nguyên liệu tươi là một kỹ năng đáng giá cho bất kỳ ai yêu thích thực phẩm lành mạnh.",
            ),
            (
                "Instead of ordering takeout, she decided to cook from scratch using fresh market produce.",
                "Thay vì gọi đồ mang đi, cô ấy quyết định tự nấu từ nguyên liệu tươi sử dụng nông sản ngoài chợ.",
            ),
            (
                "Making pasta sauce from scratch makes the dish taste infinitely better than store-bought ones.",
                "Làm sốt mì Ý từ đầu khiến món ăn có hương vị ngon hơn vô hạn so với loại mua sẵn trong cửa hàng.",
            ),
        ],
        "prepping (vegetables)": [
            (
                "Prepping vegetables like washing, peeling, and chopping is often the most time-consuming part of cooking.",
                "Việc sơ chế rau củ như rửa, gọt vỏ và cắt thái thường là phần tốn thời gian nhất khi nấu nướng.",
            ),
            (
                "To save time on busy weekdays, I prefer prepping my vegetables over the weekend.",
                "Để tiết kiệm thời gian vào các ngày trong tuần bận rộn, tôi thích sơ chế rau củ sẵn vào dịp cuối tuần.",
            ),
            (
                "Proper prepping of ingredients ensures that everything cooks evenly in the pan.",
                "Việc sơ chế nguyên liệu đúng cách đảm bảo mọi thứ chín đều trong chảo.",
            ),
            (
                "While prepping ingredients for the soup, she made sure to steer clear of bruised vegetables.",
                "Trong lúc sơ chế nguyên liệu cho món súp, cô ấy đảm bảo tránh xa những củ quả bị dập nát.",
            ),
            (
                "Prepping seafood and meats requires extra cleanliness to avoid posing any health risks.",
                "Sơ chế hải sản và thịt đòi hỏi sự sạch sẽ kỹ lưỡng để tránh gây ra bất kỳ rủi ro sức khỏe nào.",
            ),
        ],
        "simmer": [
            (
                "Let the curry simmer on low heat for twenty minutes so the aromatic spices can fully blend.",
                "Hãy để món cà ri ninh trên lửa nhỏ trong hai mươi phút để các loại gia vị thơm nồng có thể hòa quyện hoàn toàn.",
            ),
            (
                "Traditional beef stews taste best when you simmer them slowly for hours.",
                "Các món thịt bò hầm truyền thống ngon nhất khi bạn ninh chúng từ từ trong nhiều giờ.",
            ),
            (
                "Turn down the stove and let the bone broth simmer gently to bring out its wholesome flavor.",
                "Vặn nhỏ bếp và để nước dùng xương hầm từ từ để làm nổi bật hương vị lành mạnh của nó.",
            ),
            (
                "While the soup is simmering, you can focus on prepping the side dishes.",
                "Trong lúc canh đang sôi liu riu trên lửa nhỏ, bạn có thể tập trung sơ chế các món phụ.",
            ),
            (
                "Simmering the sauce helps reduce excess liquid and concentrates the rich flavors.",
                "Việc ninh nước sốt giúp làm giảm bớt lượng chất lỏng dư thừa và cô đặc hương vị đậm đà.",
            ),
        ],
        "seasoning / blending": [
            (
                "Proper seasoning can transform a bland bowl of porridge into a mouth-watering masterpiece.",
                "Việc nêm nếm gia vị đúng cách có thể biến một bát cháo nhạt nhẽo thành một kiệt tác ngon ngất ngây.",
            ),
            (
                "Blending fresh herbs and spices together creates an authentic curry paste from scratch.",
                "Việc xay trộn các loại rau thơm và gia vị tươi với nhau tạo ra một hỗn hợp sốt cà ri chính gốc từ đầu.",
            ),
            (
                "Pay close attention to your seasoning so the dish doesn't end up too salty.",
                "Hãy chú ý kỹ đến việc nêm nếm gia vị để món ăn không bị quá mặn.",
            ),
            (
                "The chef spent years perfecting the art of flavor blending for Italian delicacies.",
                "Đầu bếp đã mất nhiều năm để hoàn thiện nghệ thuật pha trộn hương vị cho các món ngon Ý.",
            ),
            (
                "Adjusting the seasoning at the end of cooking ensures the dish is cooked to perfection.",
                "Việc điều chỉnh gia vị vào cuối quá trình nấu đảm bảo món ăn được nấu chín hoàn hảo.",
            ),
        ],
        "cooked to perfection": [
            (
                "The juicy steak was cooked to perfection, remaining tender on the inside and crispy outside.",
                "Miếng bít tết mọng nước được nấu chín tới độ hoàn hảo, giữ được độ mềm bên trong và giòn bên ngoài.",
            ),
            (
                "Making sure the pasta is cooked to perfection is the secret to a great Italian meal.",
                "Đảm bảo mì Ý được nấu chín tới độ hoàn hảo là bí quyết của một bữa ăn Ý tuyệt vời.",
            ),
            (
                "Unlike overcooked vegetables, these beans were cooked to perfection, retaining their bright green color.",
                "Không giống như rau củ bị nấu quá lửa, những hạt đậu này được nấu chín hoàn hảo, giữ nguyên màu xanh tươi sáng.",
            ),
            (
                "The homemade meal felt extra special because every single dish was cooked to perfection.",
                "Bữa cơm nhà mang cảm giác đặc biệt hơn hẳn vì mọi món ăn đều được nấu chín hoàn hảo.",
            ),
            (
                "It takes practice to ensure that fish is cooked to perfection without drying it out.",
                "Cần phải luyện tập để đảm bảo cá được nấu chín vừa tới mà không bị khô.",
            ),
        ],
        "common ground": [
            (
                "When cooking for a large family with picky eaters, finding a common ground on the menu is crucial.",
                "Khi nấu ăn cho một gia đình lớn có những người kén ăn, việc tìm ra điểm chung về thực đơn là vô cùng quan trọng.",
            ),
            (
                "My friends and I finally found some common ground regarding our favorite local eateries.",
                "Tôi và các bạn cuối cùng cũng tìm được một vài điểm chung về những quán ăn địa phương yêu thích.",
            ),
            (
                "Despite having different tastes in food, they managed to establish a common ground for dinner.",
                "Dù có khẩu vị ăn uống khác nhau, họ vẫn xoay sở tìm được điểm chung cho bữa tối.",
            ),
            (
                "Finding common ground in dietary habits makes meal planning much easier for couples.",
                "Việc tìm thấy điểm chung trong thói quen ăn uống giúp việc lên thực đơn trở nên dễ dàng hơn nhiều cho các cặp đôi.",
            ),
            (
                "The food discussion reached a common ground when everyone agreed on ordering wholesome soups.",
                "Cuộc thảo luận về ẩm thực đã đạt được tiếng nói chung khi mọi người đồng ý gọi các món canh lành mạnh.",
            ),
        ],
    },
    "13": {
        "generally speaking, I love …, but the only thing I don't really like about … is …": [
            (
                "Generally speaking, I love dining out with my friends, but the only thing I don't really like about it is the noisy atmosphere.",
                "Nói chung là tôi thích đi ăn ngoài với bạn bè, nhưng điều duy nhất tôi không thực sự thích ở đó là không khí ồn ào.",
            ),
            (
                "Generally speaking, I love traditional street food, but the only thing I don't really like about it is the high amount of oil.",
                "Nói chung là tôi thích đồ ăn đường phố truyền thống, nhưng điều duy nhất tôi không thực sự thích ở nó là lượng dầu mỡ khá cao.",
            ),
            (
                "Generally speaking, I love cooking wholesome meals at home, but the only thing I don't really like about it is the tedious prepping process.",
                "Nói chung là tôi thích nấu các bữa ăn lành mạnh tại nhà, nhưng điều duy nhất tôi không thực sự thích ở việc này là công đoạn sơ chế tẻ nhạt.",
            ),
            (
                "Generally speaking, I love trying new culinary delicacies, but the only thing I don't really like about them is the expensive price tag.",
                "Nói chung là tôi thích thử các món ngon ẩm thực mới, nhưng điều duy nhất tôi không thực sự thích ở chúng là mức giá đắt đỏ.",
            ),
            (
                "Generally speaking, I love family dinners, but the only thing I don't really like about them is dealing with heavy seasoning.",
                "Nói chung là tôi thích các bữa cơm gia đình, nhưng điều duy nhất tôi không thực sự thích ở đó là phải đối mặt với gia vị đậm.",
            ),
        ],
        "Apart from that, I'm fine": [
            (
                "The restaurant service was a bit slow, but apart from that, I'm fine with the overall dining experience.",
                "Dịch vụ của nhà hàng hơi chậm một chút, nhưng ngoài điều đó ra thì tôi hoàn toàn ổn với trải nghiệm ăn uống tổng thể.",
            ),
            (
                "The soup lacked a bit of salt, but apart from that, I'm fine eating it.",
                "Món canh thiếu chút muối, nhưng ngoài điều đó ra thì tôi ăn vẫn thấy ổn.",
            ),
            (
                "Sometimes prepping vegetables takes too long, but apart from that, I'm fine with cooking from scratch.",
                "Đôi khi việc sơ chế rau củ mất quá nhiều thời gian, nhưng ngoài điều đó ra thì tôi vẫn ổn với việc nấu ăn từ đầu.",
            ),
            (
                "The dish was slightly greasy, but apart from that, I'm fine since the ingredients were fresh.",
                "Món ăn hơi nhiều dầu mỡ một chút, nhưng ngoài điều đó ra thì tôi thấy ổn vì các nguyên liệu đều tươi.",
            ),
            (
                "We had a minor disagreement on the menu, but apart from that, I'm fine with our dinner plans.",
                "Chúng tôi có một chút bất đồng nhỏ về thực đơn, nhưng ngoài điều đó ra thì tôi hoàn toàn ổn với kế hoạch ăn tối của chúng ta.",
            ),
        ],
        "picky eater": [
            (
                "My friends always call me a picky eater because I refuse to eat dishes containing onions or garlic.",
                "Bạn bè thường gọi tôi là một đứa kén ăn vì tôi từ chối ăn các món có chứa hành hoặc tỏi.",
            ),
            (
                "Being a picky eater can make it quite challenging to enjoy a shared meal with others.",
                "Trở thành một người kén ăn có thể khiến việc tận hưởng bữa ăn chung với người khác trở nên khá thử thách.",
            ),
            (
                "Parents often worry when their children turn out to be picky eaters who hate green vegetables.",
                "Cha mẹ thường lo lắng khi con cái họ hóa ra lại là những đứa trẻ kén ăn, những kẻ ghét rau xanh.",
            ),
            (
                "As my palate matured, I stopped acting like a picky eater and started trying bitter greens.",
                "Khi khẩu vị trưởng thành hơn, tôi đã ngừng cư xử như một kẻ kén ăn và bắt đầu thử các loại rau đắng.",
            ),
            (
                "Even though he is a picky eater, he still loves tasting sweet cheesecakes and desserts.",
                "Dù là một người kén ăn, anh ấy vẫn rất thích thưởng thức bánh cheesecake ngọt và các món tráng miệng.",
            ),
        ],
        "strong tastes overpower other ingredients": [
            (
                "I dislike garlic and onions because their strong tastes overpower other ingredients in the dish.",
                "Tôi không thích tỏi và hành vì hương vị nồng của chúng lấn át các nguyên liệu khác trong món ăn.",
            ),
            (
                "Be careful with the seasoning; strong tastes overpower other ingredients and ruin the delicate flavors.",
                "Hãy cẩn thận với việc nêm nếm gia vị; vị nồng sẽ át đi các nguyên liệu khác và làm hỏng hương vị tinh tế.",
            ),
            (
                "In this soup, the heavy spices have strong tastes that overpower other ingredients like fresh vegetables.",
                "Trong món canh này, các loại gia vị nặng có vị nồng át đi các nguyên liệu khác như rau tươi.",
            ),
            (
                "A good chef knows how to balance flavors so that strong tastes do not overpower other ingredients.",
                "Một đầu bếp giỏi biết cách cân bằng hương vị để vị nồng không lấn át các thành phần khác.",
            ),
            (
                "I prefer subtle seasoning because strong tastes overpower other ingredients and make everything taste the same.",
                "Tôi thích gia vị nhẹ nhàng vì vị nồng sẽ lấn át các nguyên liệu khác và khiến mọi thứ có vị giống nhau.",
            ),
        ],
        "overwhelming": [
            (
                "The spicy chili flavor in the curry was completely overwhelming, making it hard for me to finish my meal.",
                "Vị ớt cay trong món cà ri thực sự quá mạnh và choáng ngợp, khiến tôi khó lòng ăn hết bữa.",
            ),
            (
                "Sometimes the strong smell of garlic in a restaurant can feel overwhelming for a sensitive palate.",
                "Đôi khi mùi tỏi nồng trong nhà hàng có thể mang lại cảm giác quá mạnh đối với một vòm miệng nhạy cảm.",
            ),
            (
                "Avoid using too much fish sauce, or the pungent smell will become overwhelming.",
                "Tránh dùng quá nhiều nước mắm, nếu không mùi hăng sẽ trở nên nồng nặc không chịu nổi.",
            ),
            (
                "The rich and heavy cheese topping had an overwhelming taste that ruined the balance of the pizza.",
                "Lớp phủ phô mai béo ngậy có hương vị quá nồng làm hỏng sự cân bằng của chiếc bánh pizza.",
            ),
            (
                "Walking past a fast-food joint with greasy take-away can sometimes feel overwhelmingly unappealing.",
                "Đi ngang qua một quán đồ ăn nhanh với đồ mang đi nhiều dầu mỡ đôi khi có thể mang lại cảm giác khó chịu đến ngộp thở.",
            ),
        ],
        "monotonous": [
            (
                "Eating bland porridge for days while recovering from an illness felt extremely monotonous.",
                "Việc ăn cháo nhạt trong nhiều ngày khi đang hồi phục sau bệnh tật mang lại cảm giác vô cùng nhàm chán.",
            ),
            (
                "To avoid having a monotonous diet, I try to switch between various seasonal vegetables.",
                "Để tránh một chế độ ăn uống đơn điệu, tôi cố gắng xoay vòng giữa các loại rau theo mùa khác nhau.",
            ),
            (
                "Eating the exact same meal every single day quickly becomes boring and monotonous.",
                "Việc ăn chính xác một món ăn y hệt mỗi ngày nhanh chóng trở nên nhàm chán và đơn điệu.",
            ),
            (
                "The culinary options at the cafeteria were so monotonous that we decided to dine out.",
                "Các lựa chọn ẩm thực ở quán ăn tự phục vụ quá đơn điệu đến mức chúng tôi quyết định đi ăn ngoài.",
            ),
            (
                "Cooking from scratch breaks the monotonous cycle of relying on pre-packaged frozen foods.",
                "Nấu ăn từ đầu giúp phá vỡ vòng lặp nhàm chán đơn điệu của việc phụ thuộc vào thực phẩm đông lạnh đóng gói sẵn.",
            ),
        ],
        "greasy take-away": [
            (
                "I usually steer clear of greasy take-away because it poses a serious health risk in the long run.",
                "Tôi thường tránh xa đồ ăn mang đi nhiều dầu mỡ vì nó gây ra rủi ro sức khỏe nghiêm trọng về lâu dài.",
            ),
            (
                "After a long tiring day at work, it's tempting to order greasy take-away, but I prefer wholesome meals.",
                "Sau một ngày làm việc mệt mỏi dài đằng đẵng, việc gọi đồ ăn mang đi nhiều dầu mỡ rất hấp dẫn, nhưng tôi thích các bữa ăn lành mạnh hơn.",
            ),
            (
                "Eating greasy take-away frequently leaves my body feeling sluggish and heavy.",
                "Việc thường xuyên ăn đồ mang đi nhiều dầu mỡ khiến cơ thể tôi cảm thấy uể oải và nặng nề.",
            ),
            (
                "Greasy take-away items like deep-fried chicken are major contributors to poor health habits.",
                "Các món ăn mang đi nhiều dầu mỡ như gà rán ngập dầu là nguyên nhân chính dẫn đến thói quen sức khỏe kém.",
            ),
            (
                "Instead of indulging in greasy take-away, she decided to prepare a clean salad at home.",
                "Thay vì nuông chiều bản thân với đồ mang đi nhiều dầu mỡ, cô ấy quyết định chuẩn bị một đĩa salad sạch tại nhà.",
            ),
        ],
        "malodorous": [
            (
                "Some traditional cheeses can be quite malodorous, turning off people who prefer subtle aromas.",
                "Một số loại phô mai truyền thống có thể khá nặng mùi, làm nản lòng những người thích hương thơm dịu nhẹ.",
            ),
            (
                "The garbage bin outside the kitchen became malodorous, so we had to clean it immediately.",
                "Thùng rác bên ngoài nhà bếp đã trở nên nặng mùi, vì vậy chúng tôi phải dọn dẹp ngay lập tức.",
            ),
            (
                "Unlike aromatic herbs that enhance a dish, certain ingredients can smell malodorous if left unwashed.",
                "Không giống như các loại rau thơm làm tăng hương vị món ăn, một số nguyên liệu có thể mang mùi khó chịu nếu để không rửa sạch.",
            ),
            (
                "The malodorous smell of stale fast food made me lose my appetite instantly.",
                "Mùi khó chịu của đồ ăn nhanh ôi thiu lập tức khiến tôi mất cảm giác thèm ăn.",
            ),
            (
                "Proper food storage prevents ingredients from becoming spoiled and malodorous.",
                "Việc bảo quản thực phẩm đúng cách giúp ngăn chặn các nguyên liệu bị hỏng và nặng mùi.",
            ),
        ],
        "restrain one's hunger": [
            (
                "Even though the food smelled amazing, I tried to restrain my hunger and wait until everyone arrived.",
                "Mặc dù thức ăn có mùi rất tuyệt, tôi vẫn cố gắng kiềm chế cơn đói của mình và đợi cho đến khi mọi người đến đủ.",
            ),
            (
                "It is hard to restrain your hunger when you see a table full of delicious delicacies.",
                "Thật khó để kiềm chế cơn đói khi bạn nhìn thấy một bàn đầy những món ngon hấp dẫn.",
            ),
            (
                "Instead of wolfing down snacks blindly, he learned to restrain his hunger until dinnertime.",
                "Thay vì ăn ngấu nghiến đồ ăn vặt một cách bất chấp, cậu ấy đã học cách kiềm chế cơn đói cho đến giờ ăn tối.",
            ),
            (
                "Restraining your hunger helps you eat mindfully and prevents overeating heavy meals.",
                "Việc kiềm chế cơn đói giúp bạn ăn uống có ý thức và ngăn ngừa việc ăn quá nhiều các món nặng bụng.",
            ),
            (
                "She couldn't restrain her hunger any longer and grabbed a piece of fruit before the meal.",
                "Cô ấy không thể kiềm chế cơn đói được nữa và vội vớ lấy một miếng trái cây trước bữa ăn.",
            ),
        ],
    },
    "14": {
        "at the weekend when none of us have to work": [
            (
                "At the weekend when none of us have to work, we usually gather together to prepare a hearty homemade meal.",
                "Vào cuối tuần khi không ai phải làm việc, chúng tôi thường quây quần lại để chuẩn bị một bữa cơm nhà thịnh soạn.",
            ),
            (
                "At the weekend when none of us have to work, we love to take our time cooking from scratch rather than grabbing a bite.",
                "Vào cuối tuần khi không ai phải làm việc, chúng tôi thích dành thời gian nấu ăn từ đầu hơn là ăn vội.",
            ),
            (
                "At the weekend when none of us have to work, we make efforts to eat together and catch up over a meal.",
                "Vào cuối tuần khi không ai phải làm việc, chúng tôi nỗ lực ngồi ăn cùng nhau và trò chuyện cập nhật chuyện của nhau.",
            ),
            (
                "At the weekend when none of us have to work, we might visit a luxury restaurant for a slap-up meal.",
                "Vào cuối tuần khi không ai phải làm việc, chúng tôi có thể ghé thăm một nhà hàng sang trọng để thưởng thức bữa ăn thịnh soạn.",
            ),
            (
                "At the weekend when none of us have to work, we escape from our hectic world and relax at home.",
                "Vào cuối tuần khi không ai phải làm việc, chúng tôi thoát khỏi thế giới bận rộn và thư giãn tại nhà.",
            ),
        ],
        "every now and then": [
            (
                "We cook wholesome meals at home on weekdays, but we like to eat out every now and then.",
                "Chúng tôi nấu các bữa ăn lành mạnh ở nhà vào các ngày trong tuần, nhưng thỉnh thoảng chúng tôi thích đi ăn ngoài.",
            ),
            (
                "Every now and then, it's nice to treat yourself to a delicious slice of chocolate cheesecake.",
                "Thỉnh thoảng, thật tuyệt khi tự thưởng cho bản thân một miếng bánh cheesecake sô-cô-la ngon lành.",
            ),
            (
                "Every now and then, even health-conscious people can indulge in some greasy take-away.",
                "Thỉnh thoảng, ngay cả những người có ý thức về sức khỏe cũng có thể nuông chiều bản thân với chút đồ mang đi nhiều dầu mỡ.",
            ),
            (
                "Every now and then, we invite our old friends over to catch up over a meal.",
                "Thỉnh thoảng, chúng tôi mời những người bạn cũ đến nhà để vừa ăn vừa trò chuyện.",
            ),
            (
                "Every now and then, trying a new recipe breaks the monotonous routine of daily cooking.",
                "Thỉnh thoảng, việc thử một công thức mới giúp phá vỡ thói quen nấu nướng đơn điệu hằng ngày.",
            ),
        ],
        "once in a blue moon": [
            (
                "We only go to high-end restaurants for a wine and dine experience once in a blue moon.",
                "Chúng tôi chỉ đến các nhà hàng cao cấp để trải nghiệm rượu vang và ẩm thực sang trọng năm thì mười họa một lần.",
            ),
            (
                "Being up to our ears in work, we manage to have a slap-up meal once in a blue moon.",
                "Vì bận ngập đầu trong công việc, chúng tôi chỉ có được một bữa ăn thịnh soạn hiếm hoi năm thì mười họa.",
            ),
            (
                "Once in a blue moon, I might snack on junk food when I crave something sweet.",
                "Năm thì mười họa, tôi có thể ăn vặt đồ không lành mạnh khi thèm một thứ gì đó ngọt.",
            ),
            (
                "Because of our busy schedules, the whole family gathers for a grand dinner once in a blue moon.",
                "Do lịch trình bận rộn, cả gia đình mới quây quần cho một bữa tối hoành tráng hiếm hoi.",
            ),
            (
                "Ordering greasy take-away is something I do once in a blue moon to protect my health.",
                "Việc gọi đồ ăn mang đi nhiều dầu mỡ là điều tôi làm rất hiếm hoi để bảo vệ sức khỏe.",
            ),
        ],
        "grab a bite": [
            (
                "On busy weekdays, I usually just grab a bite at a local café before rushing to work.",
                "Vào những ngày trong tuần bận rộn, tôi thường chỉ ăn vội một chút ở quán cà phê địa phương trước khi vội vã đi làm.",
            ),
            (
                "Instead of cooking from scratch, we had to grab a bite of fast food because we were up to our ears in tasks.",
                "Thay vì nấu ăn từ đầu, chúng tôi đành phải ăn vội đồ ăn nhanh vì bận ngập đầu với các nhiệm vụ.",
            ),
            (
                "There's no time for a sit-down meal today, so let's just grab a bite on the go.",
                "Hôm nay không có thời gian cho một bữa ăn đàng hoàng, nên chúng ta hãy ăn vội trên đường đi nhé.",
            ),
            (
                "Grabbing a quick bite is convenient, but it can never replace a wholesome home-cooked meal.",
                "Việc ăn vội thì tiện lợi, nhưng nó không bao giờ thay thế được một bữa cơm nhà lành mạnh.",
            ),
            (
                "We decided to sit down and enjoy our dinner leisurely instead of just grabbing a bite.",
                "Chúng tôi quyết định ngồi xuống và thong thả thưởng thức bữa tối thay vì chỉ ăn vội.",
            ),
        ],
        "make efforts to eat together": [
            (
                "Even though parents are busy with work, they always make efforts to eat together with their children.",
                "Mặc dù cha mẹ bận rộn với công việc, họ vẫn luôn nỗ lực để cùng ngồi ăn với con cái.",
            ),
            (
                "In this hectic world, families must make efforts to eat together to maintain strong bonds.",
                "Trong thế giới bận rộn này, các gia đình phải nỗ lực ngồi ăn cùng nhau để duy trì sự gắn kết khăng khít.",
            ),
            (
                "We made efforts to eat together at the weekend when none of us had to work.",
                "Chúng tôi đã nỗ lực cùng ngồi ăn với nhau vào cuối tuần khi không ai phải làm việc.",
            ),
            (
                "Making efforts to eat together helps family members touch base and share their daily stories.",
                "Việc nỗ lực ăn cùng nhau giúp các thành viên trong gia đình kết nối và chia sẻ câu chuyện hằng ngày.",
            ),
            (
                "Despite our tight schedules, we make efforts to eat together at least once a day.",
                "Dù lịch trình dày đặc, chúng tôi vẫn nỗ lực ăn cùng nhau ít nhất một lần mỗi ngày.",
            ),
        ],
        "touch base / catch up": [
            (
                "Family dinner is the ideal time to touch base and catch up after a long hectic week.",
                "Bữa tối gia đình là thời điểm lý tưởng để kết nối và trò chuyện sau một tuần dài bận rộn.",
            ),
            (
                "I met my old friend at a restaurant to touch base and talk about our recent lives.",
                "Tôi gặp người bạn cũ ở nhà hàng để kết nối và trò chuyện về cuộc sống gần đây của chúng tôi.",
            ),
            (
                "Catching up over a meal allows us to touch base and chew the fat comfortably.",
                "Việc vừa ăn vừa trò chuyện giúp chúng tôi kết nối và tâm sự thoải mái.",
            ),
            (
                "Even a quick phone call helps busy colleagues touch base during the workday.",
                "Ngay cả một cuộc điện thoại nhanh cũng giúp các đồng nghiệp bận rộn kết nối với nhau trong giờ làm việc.",
            ),
            (
                "We used the weekend gathering to catch up on all the news we missed.",
                "Chúng tôi tận dụng buổi tụ họp cuối tuần để cập nhật tất cả những tin tức đã bỏ lỡ.",
            ),
        ],
        "up to their ears": [
            (
                "My parents are up to their ears in work on weekdays, so family dinners are often short.",
                "Bố mẹ tôi bận ngập đầu công việc vào các ngày trong tuần, nên bữa cơm gia đình thường khá ngắn.",
            ),
            (
                "Parents are often up to their ears in work, leaving little time to cook elaborate meals.",
                "Cha mẹ thường bận ngập đầu trong công việc, để lại rất ít thời gian nấu các món ăn kỳ công.",
            ),
            (
                "When students are up to their ears in exams, they tend to rely on fast food and quick snacks.",
                "Khi học sinh bận ngập đầu với các kỳ thi, các em có xu hướng dựa vào đồ ăn nhanh và đồ ăn vặt nhanh.",
            ),
            (
                "I was up to my ears in reports, so I had to grab a bite.",
                "Tôi bận ngập đầu trong các báo cáo, vì vậy tôi buộc phải ăn vội một chút.",
            ),
            (
                "Even though we were up to our ears, we still made efforts to eat together on Sunday.",
                "Mặc dù chúng tôi bận ngập đầu, chúng tôi vẫn nỗ lực ngồi ăn cùng nhau vào ngày Chủ nhật.",
            ),
        ],
        "hectic world": [
            (
                "In today's hectic world, dinner is often the only time for families to catch up.",
                "Trong thế giới bận rộn ngày nay, bữa tối thường là khoảng thời gian duy nhất để các gia đình trò chuyện cùng nhau.",
            ),
            (
                "People living in the modern hectic world frequently suffer from stress and poor eating habits.",
                "Những người sống trong thế giới bận rộn hiện đại thường xuyên chịu đựng căng thẳng và thói quen ăn uống kém.",
            ),
            (
                "Cooking wholesome meals from scratch helps us slow down in this hectic world.",
                "Việc nấu các bữa ăn lành mạnh từ đầu giúp chúng ta sống chậm lại trong thế giới hối hả này.",
            ),
            (
                "Taking a break from our hectic world at the weekend is essential for mental well-being.",
                "Việc nghỉ ngơi khỏi thế giới bận rộn vào cuối tuần là điều thiết yếu cho sức khỏe tinh thần.",
            ),
            (
                "Finding common ground in a hectic world requires patience and mutual understanding.",
                "Việc tìm kiếm tiếng nói chung trong một thế giới hối hả đòi hỏi sự kiên nhẫn và thấu hiểu lẫn nhau.",
            ),
        ],
    },
    "15": {
        "has changed a great deal in recent years": [
            (
                "Our eating habits have changed a great deal in recent years due to fast-paced modern lifestyles.",
                "Thói quen ăn uống của chúng ta đã thay đổi rất nhiều trong những năm gần đây do lối sống hiện đại nhịp độ nhanh.",
            ),
            (
                "The culinary scene in big cities has changed a great deal in recent years with the rise of healthy eateries.",
                "Bối cảnh ẩm thực ở các thành phố lớn đã thay đổi rất nhiều trong những năm gần đây với sự gia tăng của các quán ăn lành mạnh.",
            ),
            (
                "Traditional food culture has changed a great deal in recent years as younger generations embrace convenient options.",
                "Văn hóa ẩm thực truyền thống đã thay đổi rất nhiều trong những năm gần đây khi thế hệ trẻ đón nhận các lựa chọn tiện lợi.",
            ),
            (
                "People's awareness of nutrition has changed a great deal in recent years, leading to a healthier society.",
                "Nhận thức của mọi người về dinh dưỡng đã thay đổi rất nhiều trong những năm gần đây, dẫn đến một xã hội lành mạnh hơn.",
            ),
            (
                "The way we source our food has changed a great deal in recent years, shifting toward organic and local markets.",
                "Cách chúng ta tìm nguồn thực phẩm đã thay đổi rất nhiều trong những năm gần đây, chuyển dịch sang các chợ hữu cơ và địa phương.",
            ),
        ],
        "a shift towards…": [
            (
                "There is a shift towards plant-based diets and health-conscious eating among young adults today.",
                "Có một sự chuyển dịch hướng tới chế độ ăn thực vật và ăn uống có ý thức về sức khỏe trong giới trẻ ngày nay.",
            ),
            (
                "A shift towards sustainable food sources has forced supermarkets to offer more organic produce.",
                "Sự chuyển dịch hướng tới các nguồn thực phẩm bền vững đã buộc các siêu thị cung cấp nhiều nông sản hữu cơ hơn.",
            ),
            (
                "We are witnessing a shift towards cooking wholesome meals at home rather than ordering fast food.",
                "Chúng ta đang chứng kiến sự chuyển dịch hướng tới việc nấu các bữa ăn lành mạnh tại nhà thay vì gọi đồ ăn nhanh.",
            ),
            (
                "A shift towards digital food delivery services has made greasy take-away more popular than ever.",
                "Sự chuyển dịch hướng tới các dịch vụ giao đồ ăn trực tuyến đã khiến đồ mang đi nhiều dầu mỡ trở nên phổ biến hơn bao giờ hết.",
            ),
            (
                "A shift towards mindful eating helps consumers steer clear of processed foods and hidden risks.",
                "Sự chuyển dịch hướng tới việc ăn uống có ý thức giúp người tiêu dùng tránh xa thực phẩm chế biến sẵn và các rủi ro ẩn giấu.",
            ),
        ],
        "cook everything from scratch": [
            (
                "In the past, our grandparents used to cook everything from scratch because ready meals were not available.",
                "Trong quá khứ, ông bà chúng ta thường nấu toàn bộ từ nguyên liệu tươi vì các bữa ăn làm sẵn chưa xuất hiện.",
            ),
            (
                "Although it takes time, learning to cook everything from scratch guarantees nutritious and wholesome meals.",
                "Mặc dù tốn thời gian, việc học cách nấu toàn bộ từ nguyên liệu tươi đảm bảo những bữa ăn bổ dưỡng và lành mạnh.",
            ),
            (
                "Being caught up in the rat race makes it almost impossible to cook everything from scratch on weekdays.",
                "Việc bị cuốn vào vòng xoáy bận rộn khiến việc nấu toàn bộ từ nguyên liệu tươi vào các ngày trong tuần gần như là bất khả thi.",
            ),
            (
                "Health-conscious consumers prefer to cook everything from scratch to avoid processed additives.",
                "Những người có ý thức về sức khỏe thích nấu toàn bộ từ nguyên liệu tươi từ đầu để tránh các chất phụ gia chế biến.",
            ),
            (
                "She loves spending her weekends trying new recipes and cooking everything from scratch for her family.",
                "Cô ấy thích dành những ngày cuối tuần để thử các công thức mới và nấu ăn từ đầu cho gia đình mình.",
            ),
        ],
        "caught up in the rat race": [
            (
                "Office workers who are caught up in the rat race often rely heavily on greasy take-away.",
                "Nhân viên văn phòng bị cuốn vào vòng xoáy bận rộn thường phụ thuộc rất nhiều vào đồ ăn mang đi nhiều dầu mỡ.",
            ),
            (
                "When you are caught up in the rat race, it is easy to fall into the trap of grabbing quick snacks.",
                "Khi bạn bị cuốn vào vòng xoáy bận rộn, rất dễ rơi vào cạm bẫy ăn vội những món ăn nhanh.",
            ),
            (
                "Living in a hectic world means many people get caught up in the rat race and neglect their diets.",
                "Sống trong một thế giới hối hả có nghĩa là nhiều người bị cuốn vào vòng xoáy bận rộn và bỏ bê chế độ ăn uống của họ.",
            ),
            (
                "She managed to escape being caught up in the rat race by moving to the countryside to grow organic produce.",
                "Cô ấy đã xoay sở thoát khỏi việc bị cuốn vào vòng xoáy bận rộn bằng cách chuyển về vùng quê để trồng nông sản hữu cơ.",
            ),
            (
                "Being caught up in the rat race pushed home-cooked meals to the back burner for most urban residents.",
                "Việc bị cuốn vào vòng xoáy bận rộn đã đẩy những bữa cơm nhà ra sau cho phần lớn cư dân thành thị.",
            ),
        ],
        "fallen into the trap of grabbing takeaway": [
            (
                "Busy professionals often have fallen into the trap of grabbing takeaway instead of preparing wholesome meals.",
                "Những chuyên gia bận rộn thường đã sa vào cạm bẫy mua đồ mang đi thay vì chuẩn bị các bữa ăn lành mạnh.",
            ),
            (
                "Avoid falling into the trap of grabbing takeaway late at night by planning your weekly menu.",
                "Hãy tránh việc sa vào cạm bẫy mua đồ mang đi vào đêm khuya bằng cách lên kế hoạch thực đơn hàng tuần.",
            ),
            (
                "When we are up to our ears in work, we easily fall into the trap of grabbing takeaway.",
                "Khi chúng ta bận ngập đầu trong công việc, chúng ta dễ dàng sa vào cạm bẫy mua đồ ăn nhanh.",
            ),
            (
                "Falling into the trap of grabbing takeaway frequently can pose serious health risks over time.",
                "Việc thường xuyên sa vào cạm bẫy mua đồ mang đi có thể gây ra rủi ro sức khỏe nghiêm trọng theo thời gian.",
            ),
            (
                "She realized she had fallen into the trap of grabbing takeaway and decided to return to cooking from scratch.",
                "Cô ấy nhận ra mình đã sa vào cạm bẫy mua đồ mang đi và quyết định quay lại việc tự nấu ăn từ đầu.",
            ),
        ],
        "pushed home-cooked meals to the back burner": [
            (
                "Modern work pressures have pushed home-cooked meals to the back burner for many young families.",
                "Áp lực công việc hiện đại đã gác lại việc nấu cơm nhà sang một bên đối với nhiều gia đình trẻ.",
            ),
            (
                "Don't let your busy schedule push home-cooked meals to the back burner; your health should come first.",
                "Đừng để lịch trình bận rộn gác lại những bữa cơm nhà; sức khỏe của bạn phải được đặt lên hàng đầu.",
            ),
            (
                "Convenience culture has pushed home-cooked meals to the back burner, favoring fast-food deliveries.",
                "Văn hóa tiện lợi đã đẩy các bữa cơm nhà sang một bên, ưu tiên các dịch vụ giao đồ ăn nhanh.",
            ),
            (
                "We need to revive our culinary traditions instead of keeping home-cooked meals on the back burner.",
                "Chúng ta cần hồi sinh các truyền thống ẩm thực thay vì cứ để việc nấu cơm nhà ở vị trí ưu tiên thấp.",
            ),
            (
                "After moving to the city, studying and working pushed home-cooked meals to the back burner of her life.",
                "Sau khi chuyển lên thành phố, việc học và làm việc đã đẩy những bữa cơm nhà lùi về phía sau trong cuộc sống của cô ấy.",
            ),
        ],
        "health-conscious consumers": [
            (
                "Health-conscious consumers always check food labels for artificial ingredients and high sugar content.",
                "Những người tiêu dùng có ý thức sức khỏe luôn kiểm tra nhãn thực phẩm để tìm các thành phần nhân tạo và hàm lượng đường cao.",
            ),
            (
                "Supermarkets are stocking more organic items to attract health-conscious consumers.",
                "Các siêu thị đang dự trữ nhiều mặt hàng hữu cơ hơn để thu hút người tiêu dùng có ý thức về sức khỏe.",
            ),
            (
                "Health-conscious consumers prefer purchasing fresh seasonal produce directly from local farmers' markets.",
                "Người tiêu dùng có ý thức sức khỏe thích mua nông sản theo mùa tươi trực tiếp từ các chợ nông sản địa phương.",
            ),
            (
                "The rising number of health-conscious consumers has transformed the restaurant industry significantly.",
                "Số lượng người tiêu dùng có ý thức sức khỏe ngày càng tăng đã làm biến đổi ngành công nghiệp nhà hàng đáng kể.",
            ),
            (
                "To satisfy health-conscious consumers, brands are cutting down on processed components in their products.",
                "Để làm hài lòng người tiêu dùng có ý thức sức khỏe, các thương hiệu đang cắt giảm các thành phần chế biến trong sản phẩm của họ.",
            ),
        ],
        "processed foods / ready meals": [
            (
                "Processed foods and ready meals are convenient, but they often lack the essential nutrients of home-cooked dishes.",
                "Thực phẩm chế biến sẵn và bữa ăn làm sẵn rất tiện lợi, nhưng chúng thường thiếu các chất dinh dưỡng thiết yếu của các món ăn nhà nấu.",
            ),
            (
                "Eating too many processed foods and ready meals can increase the risk of chronic health issues.",
                "Ăn quá nhiều thực phẩm chế biến sẵn và đồ ăn làm sẵn có thể làm tăng nguy cơ gặp các vấn đề sức khỏe mãn tính.",
            ),
            (
                "Health-conscious people actively cut down on processed foods and ready meals to protect their immune systems.",
                "Những người quan tâm đến sức khỏe chủ động cắt giảm thực phẩm chế biến sẵn và đồ ăn làm sẵn để bảo vệ hệ miễn dịch.",
            ),
            (
                "Supermarket aisles are filled with cheap processed foods and ready meals targeting busy workers.",
                "Các lối đi trong siêu thị ngập tràn thực phẩm chế biến sẵn và đồ ăn làm sẵn giá rẻ nhắm vào những công nhân bận rộn.",
            ),
            (
                "Replacing processed foods and ready meals with fresh fruits and vegetables is a great step toward clean eating.",
                "Việc thay thế thực phẩm chế biến sẵn và đồ ăn làm sẵn bằng trái cây và rau củ tươi là bước tiến tuyệt vời hướng tới ăn sạch.",
            ),
        ],
        "culinary traditions / food culture": [
            (
                "Rich culinary traditions and unique food culture are vital parts of a country's national identity.",
                "Truyền thống ẩm thực phong phú và văn hóa ẩm thực độc đáo là những phần quan trọng của bản sắc quốc gia.",
            ),
            (
                "Despite rapid modernization, local food culture remains deeply woven into everyday life.",
                "Bất chấp sự hiện đại hóa nhanh chóng, văn hóa ẩm thực địa phương vẫn đan cài sâu sắc vào đời sống hàng ngày.",
            ),
            (
                "Foreign tourists love exploring Vietnam's rich culinary traditions through street food tours.",
                "Du khách nước ngoài rất thích khám phá truyền thống ẩm thực phong phú của Việt Nam thông qua các chuyến tham quan đồ ăn đường phố.",
            ),
            (
                "Preserving our traditional food culture helps future generations connect with their roots.",
                "Việc bảo tồn văn hóa ẩm thực truyền thống giúp các thế hệ tương lai kết nối với cội nguồn của họ.",
            ),
            (
                "Globalization has introduced international elements into our local culinary traditions.",
                "Toàn cầu hóa đã mang các yếu tố quốc tế hòa nhập vào truyền thống ẩm thực địa phương của chúng ta.",
            ),
        ],
        "sustainable food sources": [
            (
                "Modern foodies care deeply about supporting sustainable food sources like organic farms and local fisheries.",
                "Những người mê ẩm thực hiện đại rất quan tâm đến việc hỗ trợ các nguồn thực phẩm bền vững như nông trại hữu cơ và nghề cá địa phương.",
            ),
            (
                "Investing in sustainable food sources ensures that future generations will have access to clean produce.",
                "Việc đầu tư vào các nguồn thực phẩm bền vững đảm bảo rằng các thế hệ tương lai sẽ tiếp cận được với nông sản sạch.",
            ),
            (
                "Restaurants that use sustainable food sources often attract eco-friendly, health-conscious consumers.",
                "Các nhà hàng sử dụng nguồn thực phẩm bền vững thường thu hút những thực khách thân thiện với môi trường và có ý thức sức khỏe.",
            ),
            (
                "Finding sustainable food sources can be challenging, but it is necessary for environmental protection.",
                "Tìm kiếm các nguồn thực phẩm bền vững có thể gặp nhiều thử thách, nhưng nó rất cần thiết cho việc bảo vệ môi trường.",
            ),
            (
                "A shift towards sustainable food sources is changing how global supermarkets operate today.",
                "Sự chuyển dịch hướng tới các nguồn thực phẩm bền vững đang thay đổi cách các siêu thị toàn cầu vận hành ngày nay.",
            ),
        ],
    },
}

VOCAB_EXAMPLE_HIGHLIGHTS: dict[str, list[str]] = {
    "9": [
        r"As far as I can remember",
        r"left a mark on me",
        r"leave a mark on me",
        r"homemade meals?",
        r"bland porridge",
        r"topped with",
        r"culinary delicacies",
        r"local delicacies",
        r"seafood delicacies",
        r"regional delicacies",
        r"Italian delicacies",
        r"\bdelicacies\b",
        r"makes? my mouth water",
        r"slap-up meal",
        r"recount(?:s|ed|ing)?",
    ],
    "10": [
        r"fussy eaters?",
        r"picky eaters?",
        r"turn(?:ing)? (?:my|your|his|her|their) nose up at",
        r"wolf(?:ed|ing)? (?:them |their meals |a hearty plate of pasta |fast food |snacks )?down",
        r"wolf them down",
        r"pester(?:ing)?",
        r"palate has matured",
        r"palate matured",
        r"mature palate",
        r"acquired taste",
        r"snack(?:ing)? on junk food",
        r"eat clean",
        r"stick to a balanced diet",
        r"cut(?:s|ting)? down on processed foods",
    ],
    "11": [
        r"well-balanced meal",
        r"balanced diet",
        r"health-conscious",
        r"nutritious foods",
        r"pose(?:s)? a(?: serious)? health risk",
        r"feeling sluggish",
        r"\bsluggish\b",
        r"immune system",
        r"chronic diseases",
        r"steer(?:s|ing)? clear of",
        r"that said",
        r"a piece of cake",
        r"take(?:n)? (?:my|your|their) (?:health|physical well-being) for granted",
        r"taken my health for granted",
        r"for granted",
    ],
    "12": [
        r"it's always quite difficult at the beginning when you try something new",
        r"is not an exception",
        r"follow(?:s|ing)? a recipe",
        r"cook(?:ing)? from scratch",
        r"from scratch",
        r"Prepping vegetables",
        r"prepping (?:my )?vegetables",
        r"prepping (?:ingredients|seafood and meats)",
        r"\bprepping\b",
        r"simmer(?:ing)?",
        r"\bseasoning\b",
        r"flavor blending",
        r"\b[Bb]lending\b",
        r"cooked to perfection",
        r"common ground",
    ],
    "13": [
        r"Generally speaking, I love",
        r"but the only thing I don't really like about",
        r"apart from that, I'm fine",
        r"picky eaters?",
        r"strong tastes (?:that )?overpower other ingredients",
        r"do not overpower other ingredients",
        r"overpower other ingredients",
        r"overwhelmingly",
        r"\boverwhelming\b",
        r"\bmonotonous\b",
        r"greasy take-away",
        r"\bmalodorous\b",
        r"restrain(?:ing)? (?:my|your|his|her|one's) hunger",
    ],
    "14": [
        r"at the weekend when none of us have to work",
        r"At the weekend when none of us have to work",
        r"every now and then",
        r"once in a blue moon",
        r"grab(?:bing)? a(?: quick)? bite",
        r"make(?:s)? efforts to eat together",
        r"made efforts to eat together",
        r"Making efforts to eat together",
        r"touch base",
        r"catch(?:ing)? up",
        r"up to (?:their|our|my) ears",
        r"hectic world",
    ],
    "15": [
        r"ha(?:ve|s) changed a great deal in recent years",
        r"a shift towards",
        r"cook(?:ing)? everything from scratch",
        r"caught up in the rat race",
        r"fall(?:en|ing)? into the trap of grabbing takeaway",
        r"fall into the trap of grabbing (?:takeaway|quick snacks)",
        r"push(?:ed)? home-cooked meals to the back burner",
        r"keeping home-cooked meals on the back burner",
        r"health-conscious consumers",
        r"processed foods",
        r"ready meals",
        r"culinary traditions",
        r"food culture",
        r"sustainable food sources",
    ],
}
