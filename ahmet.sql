INSERT INTO doktorlar (tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, uzmanlik_alani) 
VALUES (
    '12345678901',   -- TC Kimlik No
    'Ahmet',         -- Ad
    'Yılmaz',        -- Soyad
    'ahmet.yilmaz@ornek.com',  -- Email
    digest('12345', 'sha256'), -- Şifre (SHA-256 ile şifreleme)
    '1980-05-12',    -- Doğum Tarihi (YYYY-MM-DD)
    'Erkek',         -- Cinsiyet
    'Endokrinoloji'  -- Uzmanlık Alanı
);


