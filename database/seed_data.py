"""
Run this after init_db.py to insert sample doctor and patient records.
Usage: python3 seed_data.py
"""
from database import connect
from utils.hashing import hash_password
from database.init_db import init


def add_doctor(tc, name, surname, email, password, birth_date, gender, specialty, photo_path=None):
    try:
        conn = connect()
        if conn is None:
            print("❌ Could not connect to the database.")
            return

        profile_photo = None
        if photo_path:
            try:
                with open(photo_path, "rb") as f:
                    profile_photo = f.read()
            except FileNotFoundError:
                print(f"⚠️  Photo not found: {photo_path}, skipping.")

        hashed_password = hash_password(password)

        conn.execute("""
            INSERT OR IGNORE INTO doktorlar
                (tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, profil_resmi, uzmanlik_alani)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tc, name, surname, email, hashed_password, birth_date, gender, profile_photo, specialty))

        conn.commit()
        conn.close()
        print(f"✔ Doctor added: Dr. {name} {surname}")

    except Exception as e:
        print("❌ An error occurred:", e)


def add_patient(tc, name, surname, email, password, birth_date, gender, doctor_id, photo_path=None):
    try:
        conn = connect()
        if conn is None:
            print("❌ Could not connect to the database.")
            return

        profile_photo = None
        if photo_path:
            try:
                with open(photo_path, "rb") as f:
                    profile_photo = f.read()
            except FileNotFoundError:
                print(f"⚠️  Photo not found: {photo_path}, skipping.")

        hashed_password = hash_password(password)

        conn.execute("""
            INSERT OR IGNORE INTO hastalar
                (tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, profil_resmi, doktor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tc, name, surname, email, hashed_password, birth_date, gender, profile_photo, doctor_id))

        conn.commit()
        conn.close()
        print(f"✔ Patient added: {name} {surname}")

    except Exception as e:
        print("❌ An error occurred:", e)


if __name__ == "__main__":
    # Ensure tables exist first
    init()

    add_doctor(
        tc="12345678901",
        name="Belinay",
        surname="Karatepe",
        email="belinay.karatepe@example.com",
        password="12345",
        birth_date="1985-06-15",
        gender="Kadın",
        specialty="Kardiyoloji",
        photo_path="assets/belinay_karatepe.jpg"
    )
    add_doctor(
        tc="11111111111",
        name="Mehmet",
        surname="Akıncı",
        email="mehmet.ali.akinci@gmail.com",
        password="12345",
        birth_date="1974-11-30",
        gender="Erkek",
        specialty="Dahiliye",
        photo_path="assets/mehmet_ali_akinci.jpeg"
    )

    # Get doctor id for Belinay (id=1 after first insert)
    add_patient(
        tc="10178688290",
        name="Dilay",
        surname="Dikbıyık",
        email="dilaydikbiyik@gmail.com",
        password="12345",
        birth_date="2004-03-17",
        gender="Kadın",
        doctor_id=1,
        photo_path="assets/dilay_dikbiyik.jpg"
    )

    # Demo / test patient — easy credentials for quick testing
    add_patient(
        tc="22222222222",
        name="Test",
        surname="Hasta",
        email="test.hasta@example.com",
        password="12345",
        birth_date="1990-01-01",
        gender="Erkek",
        doctor_id=1,
    )
