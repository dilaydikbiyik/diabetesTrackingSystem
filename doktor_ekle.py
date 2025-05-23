import psycopg2
from veritabani import baglanti_kur
from hashleme import hashle

def doktor_ekle(
    tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, uzmanlik_alani, resim_yolu=None
):
    try:
        conn = baglanti_kur()
        if conn is None:
            print("❌ Veritabanı bağlantısı kurulamadı.")
            return

        cursor = conn.cursor()

        profil_resmi = None
        if resim_yolu:
            with open(resim_yolu, "rb") as file:
                profil_resmi = file.read()

        hashed_sifre = hashle(sifre)

        cursor.execute("""
            INSERT INTO doktorlar (
                tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, profil_resmi, uzmanlik_alani
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            tc, ad, soyad, email, hashed_sifre, dogum_tarihi, cinsiyet,
            psycopg2.Binary(profil_resmi) if profil_resmi else None,
            uzmanlik_alani
        ))

        conn.commit()
        print(f"✔ Doktor başarıyla eklendi: Dr. {ad} {soyad}")

    except Exception as e:
        print("❌ Hata oluştu:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    doktor_ekle(
        tc="12345678901",
        ad="Ayşe",
        soyad="Demir",
        email="ayse.demir@example.com",
        sifre="12345",
        dogum_tarihi="1985-06-15",
        cinsiyet="Kadın",
        uzmanlik_alani="Dahiliye",
        resim_yolu="assets/ayşe_demir.png"
    )
    doktor_ekle(
        tc="11111111111",
        ad="Mehmet",
        soyad="Akıncı",
        email="mehmet.ali.akinci@gmail.com",
        sifre="12345",
        dogum_tarihi="1974-11-30",
        cinsiyet="Erkek",
        uzmanlik_alani="Kardiyoloji",
        resim_yolu="assets/mehmet_ali_akinci.jpeg"
    )
