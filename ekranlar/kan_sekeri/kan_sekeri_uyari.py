from datetime import datetime, timedelta
from veritabani import baglanti_kur
from pytz import timezone


def tip_id_al(cur, tip_adi):
    cur.execute("SELECT id FROM uyari_turleri WHERE tip = %s", (tip_adi,))
    sonuc = cur.fetchone()
    return sonuc[0] if sonuc else None


def gun_sonu_analiz_ve_uyari(hasta_id):
    conn = baglanti_kur()
    if conn is None:
        return

    cur = conn.cursor()

    bugun = datetime.now(timezone("Europe/Istanbul")).date()
    baslangic = datetime.combine(bugun, datetime.min.time()).astimezone(timezone("Europe/Istanbul"))
    bitis = datetime.combine(bugun, datetime.max.time()).astimezone(timezone("Europe/Istanbul"))
    simdi = datetime.now(timezone("Europe/Istanbul"))

    cur.execute("""
        SELECT kan_sekeri, tarih_zaman
        FROM kan_sekeri
        WHERE hasta_id = %s AND tarih_zaman BETWEEN %s AND %s
        ORDER BY tarih_zaman
    """, (hasta_id, baslangic, bitis))

    olcumler = cur.fetchall()
    adet = len(olcumler)
    toplam = 0

    kritik_id = tip_id_al(cur, "kritik")
    bilgi_id = tip_id_al(cur, "bilgilendirme")

    if adet == 0:
        cur.execute("""
            INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
            VALUES (%s, %s, %s, %s)
        """, (hasta_id, simdi, kritik_id, "⚠️ Ölçüm Eksik Uyarısı: Bugün hiç kan şekeri ölçümü yapılmamış."))
    else:
        for seviye, zaman in olcumler:
            toplam += seviye
            if seviye < 70:
                cur.execute("""
                    INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
                    VALUES (%s, %s, %s, %s)
                """, (hasta_id, simdi, kritik_id,
                      f"🚨 Hipoglisemi Uyarısı: {zaman.strftime('%d.%m.%Y %H:%M')} - Seviye: {seviye} mg/dL"))
            elif seviye > 200:
                cur.execute("""
                    INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
                    VALUES (%s, %s, %s, %s)
                """, (hasta_id, simdi, kritik_id,
                      f"🚨 Hiperglisemi Uyarısı: {zaman.strftime('%d.%m.%Y %H:%M')} - Seviye: {seviye} mg/dL"))

        if adet < 3:
            cur.execute("""
                INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
                VALUES (%s, %s, %s, %s)
            """, (hasta_id, simdi, kritik_id,
                  f"⚠️ Ölçüm Yetersiz Uyarısı: Bugün yalnızca {adet} ölçüm yapılmış."))

        ortalama = toplam / adet
        if ortalama < 70:
            doz = "Yok (Hipoglisemi)"
        elif 70 <= ortalama <= 110:
            doz = "Yok (Normal)"
        elif 111 <= ortalama <= 150:
            doz = "1 ml"
        elif 151 <= ortalama <= 200:
            doz = "2 ml"
        else:
            doz = "3 ml"

        cur.execute("""
            INSERT INTO uyarilar (hasta_id, zaman, tip_id, mesaj)
            VALUES (%s, %s, %s, %s)
        """, (hasta_id, simdi, bilgi_id,
              f"📊 Günlük Ortalama: {ortalama:.2f} mg/dL — 💉 İnsülin Önerisi: {doz}"))

    conn.commit()
    cur.close()
    conn.close()
