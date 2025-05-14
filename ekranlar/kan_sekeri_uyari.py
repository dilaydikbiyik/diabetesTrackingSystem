from datetime import datetime, timedelta
import psycopg2

def gun_sonu_analiz_ve_uyari(hasta_id):
    conn = psycopg2.connect(
        dbname="diabetes_tracking",
        user="postgres",
        password="veritabani13",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    bugun = datetime.now().date()
    baslangic = datetime.combine(bugun, datetime.min.time())
    bitis = datetime.combine(bugun, datetime.max.time())

    cur.execute("""
        SELECT kan_sekeri, tarih_zaman
        FROM olcumler
        WHERE hasta_id = %s AND tarih_zaman BETWEEN %s AND %s
        ORDER BY tarih_zaman
    """, (hasta_id, baslangic, bitis))

    olcumler = cur.fetchall()
    adet = len(olcumler)
    toplam = 0
    bugun_zaman = datetime.now()

    if adet == 0:
        cur.execute("""
            INSERT INTO uyarilar (hasta_id, zaman, tip, mesaj)
            VALUES (%s, %s, %s, %s)
        """, (
            hasta_id,
            bugun_zaman,
            "kritik",
            "⚠️ Ölçüm Eksik Uyarısı: Bugün hiç kan şekeri ölçümü yapılmamış."
        ))

    else:
        # Kritik seviye kontrolü
        for seviye, zaman in olcumler:
            toplam += seviye
            if seviye < 70:
                cur.execute("""
                    INSERT INTO uyarilar (hasta_id, zaman, tip, mesaj)
                    VALUES (%s, %s, %s, %s)
                """, (
                    hasta_id,
                    bugun_zaman,
                    "kritik",
                    f"🚨 Hipoglisemi Uyarısı: {zaman.strftime('%Y-%m-%d %H:%M')} - Seviye: {seviye} mg/dL"
                ))
            elif seviye > 200:
                cur.execute("""
                    INSERT INTO uyarilar (hasta_id, zaman, tip, mesaj)
                    VALUES (%s, %s, %s, %s)
                """, (
                    hasta_id,
                    bugun_zaman,
                    "kritik",
                    f"🚨 Hiperglisemi Uyarısı: {zaman.strftime('%Y-%m-%d %H:%M')} - Seviye: {seviye} mg/dL"
                ))

        # 3'ten az ölçüm varsa uyarı
        if adet < 3:
            cur.execute("""
                INSERT INTO uyarilar (hasta_id, zaman, tip, mesaj)
                VALUES (%s, %s, %s, %s)
            """, (
                hasta_id,
                bugun_zaman,
                "kritik",
                f"⚠️ Ölçüm Yetersiz Uyarısı: Bugün yalnızca {adet} ölçüm yapılmış."
            ))

        # Ortalama ve insülin dozu
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
            INSERT INTO uyarilar (hasta_id, zaman, tip, mesaj)
            VALUES (%s, %s, %s, %s)
        """, (
            hasta_id,
            bugun_zaman,
            "bilgilendirme",
            f"📊 Günlük Ortalama: {ortalama:.2f} mg/dL — 💉 İnsülin Önerisi: {doz}"
        ))

    conn.commit()
    cur.close()
    conn.close()
