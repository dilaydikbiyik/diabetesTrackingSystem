"""
Run this script once to initialize the SQLite database and seed reference data.
Usage: python3 init_db.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diabetes.db")


def init():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS doktorlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tc TEXT UNIQUE NOT NULL,
            ad TEXT NOT NULL,
            soyad TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            sifre BLOB NOT NULL,
            dogum_tarihi TEXT NOT NULL,
            cinsiyet TEXT NOT NULL,
            profil_resmi BLOB,
            uzmanlik_alani TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS hastalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tc TEXT NOT NULL UNIQUE,
            ad TEXT NOT NULL,
            soyad TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            sifre BLOB NOT NULL,
            dogum_tarihi TEXT NOT NULL,
            cinsiyet TEXT NOT NULL,
            profil_resmi BLOB,
            doktor_id INTEGER NOT NULL,
            FOREIGN KEY (doktor_id) REFERENCES doktorlar(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS belirti_tanimlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS belirtiler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hasta_id INTEGER NOT NULL,
            tarih_zaman TEXT NOT NULL DEFAULT (datetime('now')),
            belirti_id INTEGER NOT NULL,
            FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
            FOREIGN KEY (belirti_id) REFERENCES belirti_tanimlari(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS diyet_tanimlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS diyetler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hasta_id INTEGER NOT NULL,
            tarih_zaman TEXT NOT NULL DEFAULT (datetime('now')),
            diyet_id INTEGER NOT NULL,
            durum TEXT NOT NULL,
            FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
            FOREIGN KEY (diyet_id) REFERENCES diyet_tanimlari(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS egzersiz_turleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tur_adi TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS egzersiz_durumlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            durum_adi TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS egzersizler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hasta_id INTEGER NOT NULL,
            tarih_zaman TEXT NOT NULL DEFAULT (datetime('now')),
            tur_id INTEGER NOT NULL,
            durum_id INTEGER NOT NULL,
            FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
            FOREIGN KEY (tur_id) REFERENCES egzersiz_turleri(id),
            FOREIGN KEY (durum_id) REFERENCES egzersiz_durumlari(id)
        );

        CREATE TABLE IF NOT EXISTS kan_sekeri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hasta_id INTEGER NOT NULL,
            tarih_zaman TEXT NOT NULL DEFAULT (datetime('now')),
            kan_sekeri INTEGER NOT NULL,
            olcum_grubu TEXT,
            FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS uyari_turleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS uyarilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hasta_id INTEGER NOT NULL,
            zaman TEXT NOT NULL DEFAULT (datetime('now')),
            tip_id INTEGER NOT NULL,
            mesaj TEXT NOT NULL,
            FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
            FOREIGN KEY (tip_id) REFERENCES uyari_turleri(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS notlar_ve_oneriler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hasta_id INTEGER NOT NULL,
            doktor_id INTEGER NOT NULL,
            tarih TEXT DEFAULT (datetime('now')),
            baslik TEXT,
            aciklama TEXT,
            FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
            FOREIGN KEY (doktor_id) REFERENCES doktorlar(id) ON DELETE CASCADE
        );
    """)

    # Seed reference data (INSERT OR IGNORE to avoid duplicates)
    cur.executemany(
        "INSERT OR IGNORE INTO egzersiz_turleri (tur_adi) VALUES (?)",
        [("Yürüyüş",), ("Bisiklet",), ("Klinik Egzersiz",)]
    )
    cur.executemany(
        "INSERT OR IGNORE INTO egzersiz_durumlari (durum_adi) VALUES (?)",
        [("yapıldı",), ("yapılmadı",)]
    )
    cur.executemany(
        "INSERT OR IGNORE INTO diyet_tanimlari (ad) VALUES (?)",
        [("Az Şekerli Diyet",), ("Şekersiz Diyet",), ("Dengeli Beslenme",)]
    )
    cur.executemany(
        "INSERT OR IGNORE INTO belirti_tanimlari (ad) VALUES (?)",
        [
            ("Poliüri",), ("Polifaji",), ("Polidipsi",), ("Nöropati",),
            ("Kilo kaybı",), ("Yorgunluk",), ("Yaraların yavaş iyileşmesi",), ("Bulanık görme",)
        ]
    )
    cur.executemany(
        "INSERT OR IGNORE INTO uyari_turleri (tip) VALUES (?)",
        [("kritik",), ("normal",), ("bilgilendirme",), ("takip",), ("acil",), ("izleme",)]
    )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully:", DB_PATH)


if __name__ == "__main__":
    init()
