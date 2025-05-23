from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QVBoxLayout, QComboBox, QFileDialog
from veritabani import baglanti_kur
from hashleme import hashle
import datetime
import secrets
import smtplib
from email.mime.text import MIMEText

class HastaEklemeEkrani(QWidget):
    def __init__(self, doktor_id):
        super().__init__()
        self.doktor_id = doktor_id
        self.setWindowTitle("Yeni Hasta Ekle")
        self.setGeometry(400, 300, 350, 350)

        layout = QVBoxLayout()

        self.lbl_tc = QLabel("TC Kimlik No:")
        self.txt_tc = QLineEdit()
        self.txt_tc.setPlaceholderText("12345678901")
        layout.addWidget(self.lbl_tc)
        layout.addWidget(self.txt_tc)

        self.lbl_ad = QLabel("Ad:")
        self.txt_ad = QLineEdit()
        layout.addWidget(self.lbl_ad)
        layout.addWidget(self.txt_ad)

        self.lbl_soyad = QLabel("Soyad:")
        self.txt_soyad = QLineEdit()
        layout.addWidget(self.lbl_soyad)
        layout.addWidget(self.txt_soyad)

        self.lbl_email = QLabel("Email:")
        self.txt_email = QLineEdit()
        layout.addWidget(self.lbl_email)
        layout.addWidget(self.txt_email)

        self.lbl_dogum_tarihi = QLabel("Doğum Tarihi (YYYY-MM-DD):")
        self.txt_dogum_tarihi = QLineEdit()
        layout.addWidget(self.lbl_dogum_tarihi)
        layout.addWidget(self.txt_dogum_tarihi)

        self.lbl_cinsiyet = QLabel("Cinsiyet:")
        self.cmb_cinsiyet = QComboBox()
        self.cmb_cinsiyet.addItems(["Erkek", "Kadın", "Diğer"])
        layout.addWidget(self.lbl_cinsiyet)
        layout.addWidget(self.cmb_cinsiyet)

        self.lbl_resim = QLabel("Profil Resmi (isteğe bağlı):")
        self.btn_resim_sec = QPushButton("Dosya Seç")
        self.btn_resim_sec.clicked.connect(self.profil_resmi_sec)
        self.profil_resmi_yolu = None
        layout.addWidget(self.lbl_resim)
        layout.addWidget(self.btn_resim_sec)

        self.btn_ekle = QPushButton("Hastayı Ekle")
        self.btn_ekle.clicked.connect(self.hasta_ekle)
        layout.addWidget(self.btn_ekle)

        self.setLayout(layout)

    def profil_resmi_sec(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Profil Resmi Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)")
        if dosya_yolu:
            self.profil_resmi_yolu = dosya_yolu
            self.lbl_resim.setText(f"Seçilen: {dosya_yolu.split('/')[-1]}")

    def rastgele_sifre_olustur(self, uzunluk=10):
        return secrets.token_urlsafe(uzunluk)

    def sifreyi_eposta_ile_gonder(self, alici_email, tc, sifre):
        try:
            mesaj = f"""
            Sayın Kullanıcımız,

            Diyabet Takip Sistemi'ne giriş bilgileriniz aşağıdadır:

            Kullanıcı Adı (TC): {tc}
            Şifre: {sifre}

            Lütfen sistemimize giriş yaptıktan sonra şifrenizi değiştiriniz.
            Sağlıklı günler dileriz.
            """
            msg = MIMEText(mesaj)
            msg['Subject'] = "Diyabet Takip Sistemi Giriş Bilgileri"
            msg['From'] = "merome813@gmail.com"
            msg['To'] = alici_email

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login("merome813@gmail.com", "srkc dako ymmi bqkt")
            smtp.send_message(msg)
            smtp.quit()
        except Exception as e:
            print("E-posta gönderme hatası:", e)

    def hasta_ekle(self):
        tc = self.txt_tc.text().strip()
        ad = self.txt_ad.text().strip()
        soyad = self.txt_soyad.text().strip()
        email = self.txt_email.text().strip()
        dogum_tarihi = self.txt_dogum_tarihi.text().strip()
        cinsiyet = self.cmb_cinsiyet.currentText()

        if not all([tc, ad, soyad, email, dogum_tarihi]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            datetime.datetime.strptime(dogum_tarihi, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Doğum tarihi formatı hatalı! (YYYY-MM-DD)")
            return

        sifre = self.rastgele_sifre_olustur()
        hashed_sifre = hashle(sifre)

        profil_resmi = None
        if self.profil_resmi_yolu:
            with open(self.profil_resmi_yolu, "rb") as dosya:
                profil_resmi = dosya.read()

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()

            query = """
                INSERT INTO hastalar 
                (tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, profil_resmi, doktor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                tc, ad, soyad, email, hashed_sifre, dogum_tarihi, cinsiyet,
                profil_resmi, self.doktor_id
            ))
            conn.commit()

            self.sifreyi_eposta_ile_gonder(email, tc, sifre)

            QMessageBox.information(self, "Başarılı", "Hasta başarıyla eklendi ve şifresi e-posta ile gönderildi!")

            self.txt_tc.clear()
            self.txt_ad.clear()
            self.txt_soyad.clear()
            self.txt_email.clear()
            self.txt_dogum_tarihi.clear()
            self.lbl_resim.setText("Profil Resmi (isteğe bağlı)")
            self.profil_resmi_yolu = None

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
