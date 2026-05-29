"""
monument_db.py — Monument Information Database
Contains detailed information for all 24 Indian monuments in the dataset.
"""

MONUMENT_DATABASE = {
    "Taj Mahal": {
        "name": "Taj Mahal",
        "location": "Agra, Uttar Pradesh, India",
        "built_by": "Mughal Emperor Shah Jahan",
        "year_built": "1632–1653",
        "architecture_style": "Mughal Architecture (Indo-Islamic composite)",
        "short_description": (
            "The Taj Mahal is an ivory-white marble mausoleum on the right bank of the Yamuna river "
            "in Agra. Built by Mughal Emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal, "
            "it is considered the finest example of Mughal architecture—a blend of Indian, Persian, "
            "and Islamic styles. It was designated a UNESCO World Heritage Site in 1983."
        ),
        "fun_fact": "Over 20,000 artisans worked for 22 years to complete the Taj Mahal.",
        "unesco": True,
        "entry_fee": "₹50 (Indian), ₹1100 (Foreign)",
        "timings": "Sunrise to Sunset (closed on Fridays)",
    },
    "India Gate": {
        "name": "India Gate",
        "location": "New Delhi, India",
        "built_by": "British India (designed by Sir Edwin Lutyens)",
        "year_built": "1921–1931",
        "architecture_style": "Triumphal Arch / Classical European",
        "short_description": (
            "India Gate is a war memorial located astride the Rajpath in New Delhi. "
            "It commemorates the 70,000 soldiers of the British Indian Army who died in "
            "World War I and the Third Anglo-Afghan War. The eternal flame 'Amar Jawan Jyoti' "
            "burns beneath it in memory of the Unknown Soldier. It is one of India's most iconic landmarks."
        ),
        "fun_fact": "India Gate is 42 meters tall and modelled after the Arc de Triomphe in Paris.",
        "unesco": False,
        "entry_fee": "Free",
        "timings": "Open 24 hours",
    },
    "Qutub Minar": {
        "name": "Qutub Minar",
        "location": "Mehrauli, New Delhi, India",
        "built_by": "Qutb ud-Din Aibak (completed by Iltutmish)",
        "year_built": "1193–1220 AD",
        "architecture_style": "Indo-Islamic Afghan Architecture",
        "short_description": (
            "Qutub Minar is a soaring 73-metre minaret and UNESCO World Heritage Site in New Delhi. "
            "It is the tallest minaret in India and was built in the early 13th century as a symbol "
            "of Islamic rule. The tower has five distinct storeys, each marked by a projecting balcony, "
            "and is surrounded by several other medieval ruins and monuments."
        ),
        "fun_fact": "Qutub Minar's base diameter is 14.3 m and it tapers to 2.7 m at the top.",
        "unesco": True,
        "entry_fee": "₹35 (Indian), ₹550 (Foreign)",
        "timings": "Sunrise to Sunset",
    },
    "Gateway of India": {
        "name": "Gateway of India",
        "location": "Mumbai, Maharashtra, India",
        "built_by": "British India (architect George Wittet)",
        "year_built": "1911–1924",
        "architecture_style": "Indo-Saracenic (Mughal and Hindu styles fused with Gothic)",
        "short_description": (
            "The Gateway of India is an arch monument built during the 20th century in Mumbai. "
            "It was constructed to commemorate the visit of King George V and Queen Mary to Bombay. "
            "The gateway is built from yellow Kharodi basalt and reinforced concrete, standing 26 metres "
            "high. It overlooks the Arabian Sea and is a major tourist landmark."
        ),
        "fun_fact": "The last British troops left India through the Gateway of India in February 1948.",
        "unesco": False,
        "entry_fee": "Free",
        "timings": "Open 24 hours",
    },
    "Hawa Mahal": {
        "name": "Hawa Mahal",
        "location": "Jaipur, Rajasthan, India",
        "built_by": "Maharaja Sawai Pratap Singh",
        "year_built": "1799",
        "architecture_style": "Rajput Architecture (blend of Mughal and Rajput)",
        "short_description": (
            "Hawa Mahal, meaning 'Palace of Winds', is a palace in Jaipur, Rajasthan. "
            "Its unique five-storey exterior is akin to a honeycomb with its 953 small windows "
            "called 'Jharokhas' decorated with intricate latticework. It was built so that the "
            "women of the royal household could observe street festivals without being seen. "
            "The palace is made of red and pink sandstone."
        ),
        "fun_fact": "Hawa Mahal has 953 small windows (Jharokhas) to allow cool air to flow through.",
        "unesco": False,
        "entry_fee": "₹50 (Indian), ₹200 (Foreign)",
        "timings": "9:00 AM – 5:00 PM",
    },
    "Golden Temple": {
        "name": "Harmandir Sahib (Golden Temple)",
        "location": "Amritsar, Punjab, India",
        "built_by": "Guru Arjan Dev Ji (completed the present structure)",
        "year_built": "1577–1604 (gold plating added 1830)",
        "architecture_style": "Sikh Architecture (blend of Mughal and Rajput styles)",
        "short_description": (
            "The Harmandir Sahib, commonly known as the Golden Temple, is the holiest Gurdwara "
            "and the most important pilgrimage site of Sikhism. Located in Amritsar, Punjab, it "
            "was built in the 16th century and its upper floors are plated with 750 kg of pure gold. "
            "The temple is surrounded by the Amrit Sarovar (Pool of Nectar), from which the city "
            "of Amritsar gets its name."
        ),
        "fun_fact": "The Golden Temple serves free meals (langar) to over 100,000 people every day.",
        "unesco": False,
        "entry_fee": "Free",
        "timings": "Open 24 hours",
    },
    "Charminar": {
        "name": "Charminar",
        "location": "Hyderabad, Telangana, India",
        "built_by": "Muhammad Quli Qutb Shah",
        "year_built": "1591",
        "architecture_style": "Indo-Islamic Architecture",
        "short_description": (
            "The Charminar is a monument and mosque located in Hyderabad, Telangana. "
            "Built in 1591 by Muhammad Quli Qutb Shah, the founder of Hyderabad, it is "
            "the city's most recognizable landmark. The structure has four grand arches facing "
            "four directions, each containing a mosque, and is surrounded by bustling bazaars. "
            "'Char' means four and 'minar' means minaret."
        ),
        "fun_fact": "Charminar was built to commemorate the end of a deadly plague that ravaged the city.",
        "unesco": False,
        "entry_fee": "₹25 (Indian), ₹300 (Foreign)",
        "timings": "9:30 AM – 5:30 PM",
    },
    "Humayun's Tomb": {
        "name": "Humayun's Tomb",
        "location": "New Delhi, India",
        "built_by": "Bega Begum (wife of Humayun), architect Mirak Mirza Ghiyas",
        "year_built": "1570",
        "architecture_style": "Mughal Architecture",
        "short_description": (
            "Humayun's Tomb is the tomb of the Mughal Emperor Humayun in Delhi. "
            "Built in 1570, it was the first garden-tomb on the Indian subcontinent and "
            "inspired several major architectural innovations, culminating in the construction "
            "of the Taj Mahal. It is a UNESCO World Heritage Site and the first example of "
            "Mughal architecture in India, combining Persian, Timurid and Indian elements."
        ),
        "fun_fact": "Humayun's Tomb served as a model for the Taj Mahal built 80 years later.",
        "unesco": True,
        "entry_fee": "₹35 (Indian), ₹550 (Foreign)",
        "timings": "Sunrise to Sunset",
    },
    "Lotus Temple": {
        "name": "Lotus Temple (Bahá'í House of Worship)",
        "location": "New Delhi, India",
        "built_by": "Bahá'í Faith (architect Fariborz Sahba)",
        "year_built": "1986",
        "architecture_style": "Expressionist / Modern Architecture",
        "short_description": (
            "The Lotus Temple is a Bahá'í House of Worship notable for its flowerlike shape. "
            "Located in New Delhi, it serves as the Mother Temple of the Indian subcontinent. "
            "The building is composed of 27 free-standing marble-clad 'petals' arranged in clusters "
            "of three. It has won numerous architectural awards and is one of the most visited "
            "buildings in the world, welcoming all religions."
        ),
        "fun_fact": "The Lotus Temple has won seven major architectural awards including the Globe Award.",
        "unesco": False,
        "entry_fee": "Free",
        "timings": "9:00 AM – 5:30 PM (closed Mondays)",
    },
    "Mysore Palace": {
        "name": "Mysore Palace (Amba Vilas Palace)",
        "location": "Mysore (Mysuru), Karnataka, India",
        "built_by": "Maharaja Krishnaraja Wadiyar IV (architect Henry Irwin)",
        "year_built": "1912",
        "architecture_style": "Indo-Saracenic (Rajput, Mughal, Hindu & Gothic)",
        "short_description": (
            "Mysore Palace, officially known as Amba Vilas Palace, is a historical palace and "
            "royal residence in Mysore, Karnataka. It is the official residence of the Wadiyar "
            "dynasty and the seat of the Kingdom of Mysore. The palace is among the largest palaces "
            "in India and is one of the most visited monuments in India after the Taj Mahal. "
            "During Dasara festival, the palace is illuminated with 100,000 light bulbs."
        ),
        "fun_fact": "Mysore Palace is illuminated with nearly 100,000 light bulbs during the Dasara festival.",
        "unesco": False,
        "entry_fee": "₹70 (Indian), ₹200 (Foreign)",
        "timings": "10:00 AM – 5:30 PM",
    },
    "Victoria Memorial": {
        "name": "Victoria Memorial",
        "location": "Kolkata, West Bengal, India",
        "built_by": "British India (architect William Emerson)",
        "year_built": "1906–1921",
        "architecture_style": "Indo-Saracenic Revivalist (Marble, British Raj era)",
        "short_description": (
            "The Victoria Memorial is a large marble building in Kolkata, built between 1906 and 1921. "
            "It is dedicated to the memory of Queen Victoria and now serves as a museum under the "
            "Archaeological Survey of India. The 338-acre complex is surrounded by a beautiful garden "
            "and has a collection of 25 galleries with paintings, sculptures, and artifacts "
            "from the British Raj era."
        ),
        "fun_fact": "The Victoria Memorial used 28,000 tonnes of Makrana white marble—the same marble as the Taj Mahal.",
        "unesco": False,
        "entry_fee": "₹30 (Indian), ₹500 (Foreign)",
        "timings": "10:00 AM – 5:00 PM (closed Mondays)",
    },
    "Ajanta Caves": {
        "name": "Ajanta Caves",
        "location": "Aurangabad, Maharashtra, India",
        "built_by": "Buddhist monks (various dynasties)",
        "year_built": "2nd century BCE – 480 CE",
        "architecture_style": "Rock-cut Buddhist Architecture",
        "short_description": (
            "The Ajanta Caves are approximately 30 rock-cut Buddhist cave monuments dating from "
            "the 2nd century BCE to 480 CE in the Aurangabad district of Maharashtra. The caves "
            "include paintings and rock-cut sculptures described as among the finest surviving examples "
            "of ancient Indian art. They are a UNESCO World Heritage Site and are considered "
            "masterpieces of Buddhist religious art."
        ),
        "fun_fact": "The Ajanta Caves were rediscovered in 1819 by a British officer while on a tiger hunt.",
        "unesco": True,
        "entry_fee": "₹40 (Indian), ₹600 (Foreign)",
        "timings": "9:00 AM – 5:30 PM (closed Mondays)",
    },
    "Ellora Caves": {
        "name": "Ellora Caves",
        "location": "Aurangabad, Maharashtra, India",
        "built_by": "Various dynasties (Rashtrakutas, Yadavas, Chalukyas)",
        "year_built": "600–1000 CE",
        "architecture_style": "Rock-cut Architecture (Hindu, Buddhist, Jain)",
        "short_description": (
            "The Ellora Caves are an archaeological site comprising 100 rock-cut cave temples, "
            "monasteries and chapels built between the 6th and 11th centuries CE. Representing "
            "Buddhist, Hindu and Jain rock-cut architecture, the 34 caves open to the public "
            "showcase an artistic synthesis of three religions. Cave 16 (Kailasa Temple) is a "
            "remarkable achievement carved out of a single basalt rock. UNESCO World Heritage Site."
        ),
        "fun_fact": "The Kailasa Temple at Ellora is the world's largest monolithic rock excavation.",
        "unesco": True,
        "entry_fee": "₹40 (Indian), ₹600 (Foreign)",
        "timings": "6:00 AM – 6:00 PM (closed Tuesdays)",
    },
    "Fatehpur Sikri": {
        "name": "Fatehpur Sikri",
        "location": "Agra District, Uttar Pradesh, India",
        "built_by": "Mughal Emperor Akbar",
        "year_built": "1569–1585",
        "architecture_style": "Mughal Architecture (blend of Persian, Indian and Islamic)",
        "short_description": (
            "Fatehpur Sikri is a city and a municipal board in the Agra District of Uttar Pradesh. "
            "The city was founded as the capital of the Mughal Empire by Emperor Akbar in 1569 "
            "and served as the imperial capital for 10 years before being abandoned due to water shortage. "
            "It is a UNESCO World Heritage Site containing the Buland Darwaza—the largest gateway in the world."
        ),
        "fun_fact": "Fatehpur Sikri was abandoned just 14 years after being built, due to a water shortage.",
        "unesco": True,
        "entry_fee": "₹50 (Indian), ₹610 (Foreign)",
        "timings": "Sunrise to Sunset",
    },
    "Khajuraho": {
        "name": "Khajuraho Group of Monuments",
        "location": "Chhatarpur, Madhya Pradesh, India",
        "built_by": "Chandela dynasty",
        "year_built": "950–1050 CE",
        "architecture_style": "Nagara-style North Indian Temple Architecture",
        "short_description": (
            "The Khajuraho Group of Monuments is a group of Hindu temples and Jain temples in "
            "Madhya Pradesh, built by the Chandela dynasty. Famous for their Nagara-style architectural "
            "symbolism and erotic sculptures, the temples represent a fusion of religion and art. "
            "Originally 85 temples were built, of which only 25 survive today. It is a UNESCO "
            "World Heritage Site."
        ),
        "fun_fact": "Only about 10% of the Khajuraho sculptures are erotic — the rest depict everyday life and gods.",
        "unesco": True,
        "entry_fee": "₹40 (Indian), ₹600 (Foreign)",
        "timings": "Sunrise to Sunset",
    },
    "Sun Temple Konark": {
        "name": "Sun Temple, Konark",
        "location": "Puri district, Odisha, India",
        "built_by": "King Narasimhadeva I of the Eastern Ganga dynasty",
        "year_built": "1250 CE",
        "architecture_style": "Kalinga Architecture (Odishan style)",
        "short_description": (
            "The Konark Sun Temple is a 13th-century CE sun temple at Konark, about 35 km northeast "
            "of Puri in Odisha. The temple is attributed to King Narasimhadeva I. "
            "It is designed as a massive chariot of the sun god Surya, with 12 pairs of stone-carved "
            "wheels pulled by 7 horses. It is a UNESCO World Heritage Site and is also known as "
            "'the Black Pagoda'."
        ),
        "fun_fact": "The 12 pairs of wheels at Konark act as sundials — you can tell time from their shadows.",
        "unesco": True,
        "entry_fee": "₹40 (Indian), ₹600 (Foreign)",
        "timings": "6:00 AM – 8:00 PM",
    },
    "Charar-E-Sharif": {
        "name": "Charar-E-Sharif (Shrine of Sheikh Nooruddin)",
        "location": "Charar-E-Sharif, Budgam, Jammu & Kashmir, India",
        "built_by": "Sheikh Nooruddin Noorani (Nund Rishi)",
        "year_built": "15th century CE",
        "architecture_style": "Kashmiri Wooden Architecture",
        "short_description": (
            "Charar-E-Sharif is a shrine (dargah) of Sheikh Nooruddin Wali, popularly known as "
            "Nund Rishi, the patron saint of Kashmir. The shrine is an important Muslim pilgrimage "
            "site and is known for its distinctive Kashmiri wooden architecture with a carved timber "
            "roof. It is located in a scenic valley and attracts thousands of devotees every year."
        ),
        "fun_fact": "Charar-E-Sharif was badly damaged in a fire in 1995 and has been rebuilt since.",
        "unesco": False,
        "entry_fee": "Free",
        "timings": "Open all day",
    },
    "Chhota Imambara": {
        "name": "Chhota Imambara (Husainabad Imambara)",
        "location": "Lucknow, Uttar Pradesh, India",
        "built_by": "Muhammad Ali Shah",
        "year_built": "1838",
        "architecture_style": "Mughal and Indo-Saracenic Architecture",
        "short_description": (
            "Chhota Imambara, also known as Husainabad Imambara or the Palace of Lights, is "
            "a congregation hall for Shia Muslims in Lucknow. Built by Muhammad Ali Shah in 1838, "
            "it contains the tombs of the builder and his mother. The building is ornately decorated "
            "with numerous chandeliers, gold and silver utensils, and is brilliantly illuminated "
            "with thousands of lights during the festival of Muharram."
        ),
        "fun_fact": "Chhota Imambara is called the 'Palace of Lights' for its dazzling illumination during Muharram.",
        "unesco": False,
        "entry_fee": "₹25 (Indian), ₹500 (Foreign)",
        "timings": "9:00 AM – 5:00 PM",
    },
    "Alai Darwaza": {
        "name": "Alai Darwaza",
        "location": "Qutub Minar Complex, New Delhi, India",
        "built_by": "Alauddin Khalji",
        "year_built": "1311",
        "architecture_style": "Khalji Architecture (early Indo-Islamic)",
        "short_description": (
            "Alai Darwaza is the main gateway to the Quwwat-ul-Islam mosque, built by Sultan "
            "Alauddin Khalji in 1311 CE. It is considered one of the finest examples of early "
            "Mughal (Khalji) architecture and the first building in India to use Islamic principles "
            "of construction including true arch and true dome. It is made of red sandstone with "
            "white marble decorations."
        ),
        "fun_fact": "Alai Darwaza is the only completed part of Alauddin Khalji's ambitious plan to build a tower four times larger than the Qutub Minar.",
        "unesco": True,
        "entry_fee": "Included in Qutub Minar complex ticket",
        "timings": "Sunrise to Sunset",
    },
    "Alai Minar": {
        "name": "Alai Minar (Unfinished)",
        "location": "Qutub Minar Complex, New Delhi, India",
        "built_by": "Alauddin Khalji",
        "year_built": "Started c. 1311 (never completed)",
        "architecture_style": "Khalji Architecture (early Indo-Islamic)",
        "short_description": (
            "The Alai Minar is an incomplete tower in the Qutub Minar complex in Delhi. "
            "Alauddin Khalji began its construction with the intent to build a minaret twice "
            "the height of the Qutub Minar. However, after his death in 1316, construction was "
            "abandoned and only the first storey of the rubble core reaching 24.5 meters was completed. "
            "It stands as a reminder of Alauddin's grand ambitions."
        ),
        "fun_fact": "Alai Minar would have been 150 metres tall — more than double the Qutub Minar's 73 metres.",
        "unesco": True,
        "entry_fee": "Included in Qutub Minar complex ticket",
        "timings": "Sunrise to Sunset",
    },
    "Basilica of Bom Jesus": {
        "name": "Basilica of Bom Jesus",
        "location": "Old Goa, Goa, India",
        "built_by": "Portuguese (Jesuits)",
        "year_built": "1594–1605",
        "architecture_style": "Baroque Architecture",
        "short_description": (
            "The Basilica of Bom Jesus is a UNESCO World Heritage Site located in Old Goa. "
            "It holds the mortal remains of St. Francis Xavier, the patron saint of Goa. "
            "Built by the Jesuits, it is one of the best examples of Baroque architecture in India "
            "and the oldest church in Goa. 'Bom Jesus' means 'Good Jesus' or 'Infant Jesus' in Portuguese."
        ),
        "fun_fact": "The body of St. Francis Xavier, preserved in the basilica, has not decayed for over 400 years.",
        "unesco": True,
        "entry_fee": "Free",
        "timings": "9:00 AM – 6:30 PM",
    },
    "Iron Pillar": {
        "name": "Iron Pillar of Delhi",
        "location": "Qutub Minar Complex, New Delhi, India",
        "built_by": "Gupta Empire (attributed to Chandragupta II)",
        "year_built": "c. 402 CE",
        "architecture_style": "Ancient Indian Metallurgy / Gupta Period",
        "short_description": (
            "The Iron Pillar of Delhi is a 7-metre column in the Qutub Minar complex. "
            "It is a renowned example of ancient Indian metallurgical skill — having stood in the "
            "open for over 1,600 years without significant rusting or corrosion. The pillar is made "
            "of 98% wrought iron and carries inscriptions that indicate it was created during the "
            "rule of the Gupta Emperor Chandragupta II."
        ),
        "fun_fact": "The Iron Pillar is 99.72% rust-free despite being 1600+ years old — a mystery modern science is still studying.",
        "unesco": True,
        "entry_fee": "Included in Qutub Minar complex ticket",
        "timings": "Sunrise to Sunset",
    },
    "Jamali Kamali Tomb": {
        "name": "Jamali Kamali Mosque and Tomb",
        "location": "Mehrauli, New Delhi, India",
        "built_by": "Built for Shaikh Fazlullah (Jamali), a Sufi poet",
        "year_built": "1528–1536",
        "architecture_style": "Late Lodi / Early Mughal Architecture",
        "short_description": (
            "Jamali Kamali is a mosque and tomb complex in the Archaeological Village complex of "
            "Mehrauli in Delhi. It is dedicated to the Sufi saint and poet Shaikh Fazlullah, known "
            "as Jamali, who was associated with the courts of the Lodi and Mughal emperors. "
            "The tomb is notable for its intricate painted plaster decorations—some of the finest "
            "Mughal-era decorative work to survive."
        ),
        "fun_fact": "Jamali Kamali tomb is considered one of Delhi's most haunted places, with many paranormal reports.",
        "unesco": False,
        "entry_fee": "Free",
        "timings": "Sunrise to Sunset",
    },
    "Tanjavur Temple": {
        "name": "Brihadeeswara Temple (Tanjavur / Tanjore Temple)",
        "location": "Thanjavur, Tamil Nadu, India",
        "built_by": "Raja Raja Chola I",
        "year_built": "1003–1010 CE",
        "architecture_style": "Dravidian Architecture (Chola style)",
        "short_description": (
            "The Brihadeeswara Temple, also called Peruvudaiyar Kovil, is a Hindu temple dedicated "
            "to Shiva located in Thanjavur, Tamil Nadu. Built by Raja Raja Chola I, it is a UNESCO "
            "World Heritage Site. The temple is one of the largest temples in India and is an example "
            "of Dravidian architecture at its zenith. The vimana (tower above the sanctuary) is "
            "66 metres tall and is one of the tallest in the world."
        ),
        "fun_fact": "The shadow of the Brihadeeswara Temple's gopura never falls on the ground at noon — by architectural design.",
        "unesco": True,
        "entry_fee": "Free",
        "timings": "6:00 AM – 8:30 PM",
    },
}


def get_monument_info(monument_name: str) -> dict:
    """
    Retrieves monument information by name.
    Performs fuzzy key matching to handle minor label variations.
    """
    # Direct match
    if monument_name in MONUMENT_DATABASE:
        return MONUMENT_DATABASE[monument_name]

    # Case-insensitive and partial match
    name_lower = monument_name.lower().replace("_", " ").replace("-", " ").strip()
    for key, value in MONUMENT_DATABASE.items():
        if (
            key.lower() == name_lower
            or name_lower in key.lower()
            or key.lower() in name_lower
        ):
            return value

    # Alias mapping for dataset folder names → DB keys
    ALIASES = {
        "tajmahal": "Taj Mahal",
        "taj mahal": "Taj Mahal",
        "india gate pics": "India Gate",
        "india_gate": "India Gate",
        "india gate": "India Gate",
        "qutub_minar": "Qutub Minar",
        "qutub minar": "Qutub Minar",
        "gateway of india": "Gateway of India",
        "hawa mahal pics": "Hawa Mahal",
        "hawa mahal": "Hawa Mahal",
        "golden temple": "Golden Temple",
        "charminar": "Charminar",
        "humayun_s tomb": "Humayun's Tomb",
        "humayuns tomb": "Humayun's Tomb",
        "lotus_temple": "Lotus Temple",
        "lotus temple": "Lotus Temple",
        "mysore_palace": "Mysore Palace",
        "mysore palace": "Mysore Palace",
        "victoria memorial": "Victoria Memorial",
        "ajanta caves": "Ajanta Caves",
        "ellora caves": "Ellora Caves",
        "fatehpur sikri": "Fatehpur Sikri",
        "khajuraho": "Khajuraho",
        "sun temple konark": "Sun Temple Konark",
        "charar-e- sharif": "Charar-E-Sharif",
        "charar e sharif": "Charar-E-Sharif",
        "chhota_imambara": "Chhota Imambara",
        "chhota imambara": "Chhota Imambara",
        "alai_darwaza": "Alai Darwaza",
        "alai darwaza": "Alai Darwaza",
        "alai_minar": "Alai Minar",
        "alai minar": "Alai Minar",
        "basilica_of_bom_jesus": "Basilica of Bom Jesus",
        "basilica of bom jesus": "Basilica of Bom Jesus",
        "iron_pillar": "Iron Pillar",
        "iron pillar": "Iron Pillar",
        "jamali_kamali_tomb": "Jamali Kamali Tomb",
        "jamali kamali tomb": "Jamali Kamali Tomb",
        "tanjavur temple": "Tanjavur Temple",
    }
    alias_key = name_lower
    if alias_key in ALIASES:
        return MONUMENT_DATABASE.get(ALIASES[alias_key], _unknown_monument(monument_name))

    return _unknown_monument(monument_name)


def _unknown_monument(name: str) -> dict:
    return {
        "name": name,
        "location": "Unknown",
        "built_by": "Unknown",
        "year_built": "Unknown",
        "architecture_style": "Unknown",
        "short_description": f"No detailed information found for '{name}' in the database.",
        "fun_fact": "N/A",
        "unesco": False,
        "entry_fee": "N/A",
        "timings": "N/A",
    }
