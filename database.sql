-- Doktorlar
CREATE TABLE IF NOT EXISTS doktorlar (
    id SERIAL PRIMARY KEY,
    tc VARCHAR(11) UNIQUE NOT NULL CHECK (tc ~ '^[0-9]{11}$'),
    ad VARCHAR(50) NOT NULL CHECK (ad ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'),
    soyad VARCHAR(50) NOT NULL CHECK (soyad ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'),
    email VARCHAR(100) UNIQUE NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    sifre BYTEA NOT NULL,
    dogum_tarihi DATE NOT NULL,
    cinsiyet VARCHAR(10) NOT NULL CHECK (cinsiyet IN ('Erkek', 'Kadın', 'Diğer')),
    profil_resmi BYTEA,
    uzmanlik_alani VARCHAR(100) NOT NULL CHECK (uzmanlik_alani ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ\s]+$')
);

-- Hastalar
CREATE TABLE IF NOT EXISTS hastalar (
    id SERIAL PRIMARY KEY,
    tc VARCHAR(11) NOT NULL UNIQUE CHECK (tc ~ '^[0-9]{11}$'),
    ad VARCHAR(50) NOT NULL CHECK (ad ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'),
    soyad VARCHAR(50) NOT NULL CHECK (soyad ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'),
    email VARCHAR(100) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    sifre BYTEA NOT NULL,
    dogum_tarihi DATE NOT NULL,
    cinsiyet VARCHAR(10) NOT NULL CHECK (cinsiyet IN ('Erkek', 'Kadın', 'Diğer')),
    profil_resmi BYTEA,
    doktor_id INTEGER NOT NULL,
    FOREIGN KEY (doktor_id) REFERENCES doktorlar(id) ON DELETE CASCADE
);

-- Belirti Tanımları
CREATE TABLE IF NOT EXISTS belirti_tanimlari (
    id SERIAL PRIMARY KEY,
    ad VARCHAR(100) UNIQUE NOT NULL CHECK (
        ad IN (
            'Poliüri (Sık idrara çıkma)',
            'Polifaji (Aşırı açlık hissi)',
            'Polidipsi (Aşırı susama hissi)',
            'Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)',
            'Kilo kaybı',
            'Yorgunluk',
            'Yaraların yavaş iyileşmesi',
            'Bulanık görme'
        )
    )
);

-- Belirtiler
CREATE TABLE IF NOT EXISTS belirtiler (
    id SERIAL PRIMARY KEY,
    hasta_id INTEGER NOT NULL,
    tarih_zaman TIMESTAMPTZ NOT NULL DEFAULT now(),
    belirti_id INTEGER NOT NULL,
    FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
    FOREIGN KEY (belirti_id) REFERENCES belirti_tanimlari(id) ON DELETE CASCADE
);

-- Diyet Tanımları
CREATE TABLE IF NOT EXISTS diyet_tanimlari (
    id SERIAL PRIMARY KEY,
    ad VARCHAR(50) UNIQUE NOT NULL CHECK (
        ad IN (
            'Az Şekerli Diyet',
            'Şekersiz Diyet',
            'Dengeli Beslenme'
        )
    )
);

-- Diyetler
CREATE TABLE IF NOT EXISTS diyetler (
    id SERIAL PRIMARY KEY,
    hasta_id INTEGER NOT NULL,
    tarih_zaman TIMESTAMPTZ NOT NULL DEFAULT now(),
    diyet_id INTEGER NOT NULL,
    durum VARCHAR(20) NOT NULL CHECK (durum IN ('uygulandı', 'uygulanmadı')),
    FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
    FOREIGN KEY (diyet_id) REFERENCES diyet_tanimlari(id) ON DELETE CASCADE
);

-- Egzersiz Türleri
CREATE TABLE IF NOT EXISTS egzersiz_turleri (
    id SERIAL PRIMARY KEY,
    tur_adi VARCHAR(50) UNIQUE NOT NULL CHECK (
        tur_adi IN (
            'Yürüyüş',
            'Klinik Egzersiz',
            'Bisiklet'
        )
    )
);

-- Egzersiz Durumları
CREATE TABLE IF NOT EXISTS egzersiz_durumlari (
    id SERIAL PRIMARY KEY,
    durum_adi VARCHAR(20) NOT NULL UNIQUE CHECK (durum_adi IN ('yapıldı', 'yapılmadı'))
);

-- Egzersizler
CREATE TABLE IF NOT EXISTS egzersizler (
    id SERIAL PRIMARY KEY,
    hasta_id INTEGER NOT NULL,
    tarih_zaman TIMESTAMPTZ NOT NULL DEFAULT now(),
    tur_id INTEGER NOT NULL,
    durum_id INTEGER NOT NULL,
    FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
    FOREIGN KEY (tur_id) REFERENCES egzersiz_turleri(id),
    FOREIGN KEY (durum_id) REFERENCES egzersiz_durumlari(id)
);

-- Kan Şekeri Ölçümleri
CREATE TABLE IF NOT EXISTS kan_sekeri (
    id SERIAL PRIMARY KEY,
    hasta_id INTEGER NOT NULL,
    tarih_zaman TIMESTAMPTZ NOT NULL DEFAULT now(),
    kan_sekeri INTEGER NOT NULL CHECK (kan_sekeri BETWEEN 20 AND 500),
    FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE
);

-- Uyarı Türleri
CREATE TABLE IF NOT EXISTS public.uyari_turleri
(
    id integer NOT NULL DEFAULT nextval('uyari_turleri_id_seq'::regclass),
    tip character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT uyari_turleri_pkey PRIMARY KEY (id),
    CONSTRAINT uyari_turleri_tip_key UNIQUE (tip)
)

-- Uyarılar
CREATE TABLE IF NOT EXISTS uyarilar (
    id SERIAL PRIMARY KEY,
    hasta_id INTEGER NOT NULL,
    zaman TIMESTAMPTZ NOT NULL DEFAULT now(),
    tip_id INTEGER NOT NULL,
    mesaj TEXT NOT NULL,
    FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE,
    FOREIGN KEY (tip_id) REFERENCES uyari_turleri(id) ON DELETE CASCADE
);

-- Notlar
CREATE TABLE notlar_ve_oneriler (
    id SERIAL PRIMARY KEY,
    hasta_id INTEGER NOT NULL REFERENCES hastalar(id) ON DELETE CASCADE,
    doktor_id INTEGER NOT NULL REFERENCES doktorlar(id) ON DELETE CASCADE,
    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    baslik TEXT,
    aciklama TEXT
);

-- Egzersiz Türleri Durumları
INSERT INTO egzersiz_turleri (tur_adi) VALUES
('Yürüyüş'),
('Bisiklet'),
('Klinik Egzersiz');

INSERT INTO egzersiz_durumlari (durum_adi) VALUES
('yapıldı'),
('yapılmadı');

-- Diyet Türleri
INSERT INTO diyet_tanimlari (ad) VALUES
('Az Şekerli Diyet'),
('Şekersiz Diyet'),
('Dengeli Beslenme');

-- Belirti Türleri
INSERT INTO belirti_tanimlari (ad) VALUES
('Poliüri'),
('Polifaji'),
('Polidipsi'),
('Nöropati'),
('Kilo kaybı'),
('Yorgunluk'),
('Yaraların yavaş iyileşmesi'),
('Bulanık görme');

INSERT INTO uyari_turleri (tip) VALUES
('kritik'),
('normal'),
('bilgilendirme'),
('takip'),
('acil'),
('izleme');



ALTER TABLE kan_sekeri
ALTER COLUMN tarih_zaman TYPE timestamptz
USING tarih_zaman AT TIME ZONE 'Europe/Istanbul';

ALTER TABLE belirtiler
ALTER COLUMN tarih_zaman TYPE timestamptz
USING tarih_zaman AT TIME ZONE 'Europe/Istanbul';

ALTER TABLE egzersizler
ALTER COLUMN tarih_zaman TYPE timestamptz
USING tarih_zaman AT TIME ZONE 'Europe/Istanbul';

ALTER TABLE diyetler
ALTER COLUMN tarih_zaman TYPE timestamptz
USING tarih_zaman AT TIME ZONE 'Europe/Istanbul';

ALTER TABLE kan_sekeri ADD COLUMN olcum_grubu VARCHAR(10);

ALTER TABLE kan_sekeri
ADD CONSTRAINT olcum_grubu_check
CHECK (olcum_grubu IN ('sabah', 'öğle', 'ikindi', 'akşam', 'gece'));

