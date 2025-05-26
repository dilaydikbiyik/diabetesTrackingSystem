# ekranlar/moduller/oneri_motoru.py

ONERI_KURALLARI = [
    {
        "min": 0, "max": 70,
        "belirtiler": {"Nöropati", "Polifaji", "Yorgunluk"},
        "diyet": "Dengeli Beslenme",
        "egzersiz": "Yok"
    },
    {
        "min": 70, "max": 111,
        "belirtiler": {"Yorgunluk", "Kilo Kaybı"},
        "diyet": "Az Şekerli Diyet",
        "egzersiz": "Yürüyüş"
    },
    {
        "min": 70, "max": 111,
        "belirtiler": {"Polifaji", "Polidipsi"},
        "diyet": "Dengeli Beslenme",
        "egzersiz": "Yürüyüş"
    },
    {
        "min": 111, "max": 181,
        "belirtiler": {"Bulanık Görme", "Nöropati"},
        "diyet": "Az Şekerli Diyet",
        "egzersiz": "Klinik Egzersiz"
    },
    {
        "min": 111, "max": 181,
        "belirtiler": {"Poliüri", "Polidipsi"},
        "diyet": "Şekersiz Diyet",
        "egzersiz": "Klinik Egzersiz"
    },
    {
        "min": 111, "max": 181,
        "belirtiler": {"Yorgunluk", "Nöropati", "Bulanık Görme"},
        "diyet": "Az Şekerli Diyet",
        "egzersiz": "Yürüyüş"
    },
    {
        "min": 181, "max": 999,
        "belirtiler": {"Yaraların Yavaş İyileşmesi", "Polifaji", "Polidipsi"},
        "diyet": "Şekersiz Diyet",
        "egzersiz": "Klinik Egzersiz"
    },
    {
        "min": 181, "max": 999,
        "belirtiler": {"Yaraların Yavaş İyileşmesi", "Kilo Kaybı"},
        "diyet": "Şekersiz Diyet",
        "egzersiz": "Yürüyüş"
    }
]

def oneri_getir(seviye, belirtiler_kumesi):
    for kural in ONERI_KURALLARI:
        if kural["min"] <= seviye < kural["max"]:
            if kural["belirtiler"].issubset(belirtiler_kumesi):
                return {
                    "diyet": kural["diyet"],
                    "egzersiz": kural["egzersiz"],
                    "aralik": f"{kural['min']}–{kural['max']} mg/dL",
                    "belirtiler": ", ".join(kural["belirtiler"])
                }
    return None

