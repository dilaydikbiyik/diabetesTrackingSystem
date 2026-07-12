from datetime import datetime, date
from database import connect


def tip_id_al(cur, tip_adi):
    cur.execute("SELECT id FROM uyari_turleri WHERE tip = ?", (tip_adi,))
    sonuc = cur.fetchone()
    return sonuc[0] if sonuc else None


def gun_sonu_analiz_ve_uyari(hasta_id):
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    simdi = datetime.now()
    bugun = simdi.date().isoformat()  # "YYYY-MM-DD"
    simdi_str = simdi.strftime("%Y-%m-%d %H:%M:%S")

    kritik_id = tip_id_al(cur, "kritik")
    bilgi_id = tip_id_al(cur, "bilgilendirme")

    cur.execute("""
        SELECT kan_sekeri, tarih_zaman, olcum_grubu
        FROM kan_sekeri
        WHERE hasta_id = ? AND date(tarih_zaman) = ? AND olcum_grubu IS NOT NULL
        ORDER BY tarih_zaman
    """, (hasta_id, bugun))

    olcumler = cur.fetchall()
    if not olcumler:
        cur.execute("""
            INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
            VALUES (?, ?, ?, ?)
        """, (hasta_id, simdi_str, kritik_id,
              "⚠️ Ölçüm Eksik Uyarısı: Bugün hiç geçerli saat aralığında ölçüm yapılmamış."))
        conn.commit()
        cur.close()
        conn.close()
        return

    for seviye, zaman_str, grup in olcumler:
        try:
            zaman = datetime.fromisoformat(str(zaman_str))
            zaman_label = zaman.strftime('%H:%M')
        except Exception:
            zaman_label = str(zaman_str)

        if seviye < 70:
            cur.execute("""
                INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
                VALUES (?, ?, ?, ?)
            """, (hasta_id, simdi_str, kritik_id,
                  f"🚨 Hipoglisemi Uyarısı: {zaman_label} - Seviye: {seviye} mg/dL"))
        elif seviye > 200:
            cur.execute("""
                INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
                VALUES (?, ?, ?, ?)
            """, (hasta_id, simdi_str, kritik_id,
                  f"🚨 Hiperglisemi Uyarısı: {zaman_label} - Seviye: {seviye} mg/dL"))

    grup_sirasi = ["sabah", "öğle", "ikindi", "akşam", "gece"]
    grup_verileri = {g: [] for g in grup_sirasi}
    for seviye, _, grup in olcumler:
        if grup in grup_verileri:
            grup_verileri[grup].append(seviye)

    biriken = []
    for grup in grup_sirasi:
        if grup_verileri[grup]:
            biriken.extend(grup_verileri[grup])
            ort = sum(biriken) / len(biriken)
            if ort < 70:
                doz = "Yok (Hipoglisemi)"
            elif 70 <= ort <= 110:
                doz = "Yok (Normal)"
            elif 111 <= ort <= 150:
                doz = "1 ml"
            elif 151 <= ort <= 200:
                doz = "2 ml"
            else:
                doz = "3 ml"

            cur.execute("""
                INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
                VALUES (?, ?, ?, ?)
            """, (hasta_id, simdi_str, bilgi_id,
                  f"💉 {grup.title()} İnsülin Önerisi: Ortalama {ort:.2f} mg/dL → {doz}"))

    toplam_olcum = sum(len(v) for v in grup_verileri.values())
    if toplam_olcum < 3:
        cur.execute("""
            INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
            VALUES (?, ?, ?, ?)
        """, (hasta_id, simdi_str, kritik_id,
              f"⚠️ Ölçüm Yetersiz Uyarısı: Bugün yalnızca {toplam_olcum} geçerli ölçüm yapılmış."))

    conn.commit()
    cur.close()
    conn.close()
