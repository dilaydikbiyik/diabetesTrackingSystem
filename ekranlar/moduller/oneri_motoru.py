ONERI_KURALLARI = [
    {
        "min": 0, "max": 70,
        "belirtiler": {"nöropati", "polifaji", "yorgunluk"},
        "diyet": "Dengeli Beslenme",
        "egzersiz": "Yok"
    },
    {
        "min": 70, "max": 111,
        "belirtiler": {"yorgunluk", "kilo kaybı"},
        "diyet": "Az Şekerli Diyet",
        "egzersiz": "Yürüyüş"
    },
    {
        "min": 70, "max": 111,
        "belirtiler": {"polifaji", "polidipsi"},
        "diyet": "Dengeli Beslenme",
        "egzersiz": "Yürüyüş"
    },
    {
        "min": 111, "max": 181,
        "belirtiler": {"bulanık görme", "nöropati"},
        "diyet": "Az Şekerli Diyet",
        "egzersiz": "Klinik Egzersiz"
    },
    {
        "min": 111, "max": 181,
        "belirtiler": {"poliüri", "polidipsi"},
        "diyet": "Şekersiz Diyet",
        "egzersiz": "Klinik Egzersiz"
    },
    {
        "min": 111, "max": 181,
        "belirtiler": {"yorgunluk", "nöropati", "bulanık görme"},
        "diyet": "Az Şekerli Diyet",
        "egzersiz": "Yürüyüş"
    },
    {
        "min": 181, "max": 999,
        "belirtiler": {"yaraların yavaş iyileşmesi", "polifaji", "polidipsi"},
        "diyet": "Şekersiz Diyet",
        "egzersiz": "Klinik Egzersiz"
    },
    {
        "min": 181, "max": 999,
        "belirtiler": {"yaraların yavaş iyileşmesi", "kilo kaybı"},
        "diyet": "Şekersiz Diyet",
        "egzersiz": "Yürüyüş"
    }
]


def temizle_belirtiler(belirtiler):
    return set(b.strip().lower() for b in belirtiler)

def oneri_getir(seviye, belirtiler_kumesi):
    temiz_belirtiler = temizle_belirtiler(belirtiler_kumesi)

    for kural in ONERI_KURALLARI:
        if kural["min"] <= seviye < kural["max"]:
            if kural["belirtiler"].issubset(temiz_belirtiler):
                return {
                    "diyet": kural["diyet"],
                    "egzersiz": kural["egzersiz"],
                    "aralik": f"{kural['min']}–{kural['max']} mg/dL",
                    "belirtiler": ", ".join(kural["belirtiler"])
                }
    return None
