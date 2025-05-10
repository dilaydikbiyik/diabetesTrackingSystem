from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QVBoxLayout, QComboBox
from veritabani import baglanti_kur
from hashleme import hashle

class HastaEklemeEkrani(QWidget):
    def __init__(self, doktor_id):
        super().__init__()
        self.doktor_id = doktor_id
        self.setWindowTitle("Yeni Hasta Ekle")
        self.setGeometry(400, 300, 350, 300)

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

        self.lbl_sifre = QLabel("Şifre:")
        self.txt_sifre = QLineEdit()
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.lbl_sifre)
        layout.addWidget(self.txt_sifre)

        self.lbl_dogum_tarihi = QLabel("Doğum Tarihi (YYYY-MM-DD):")
        self.txt_dogum_tarihi = QLineEdit()
        layout.addWidget(self.lbl_dogum_tarihi)
        layout.addWidget(self.txt_dogum_tarihi)

        self.lbl_cinsiyet = QLabel("Cinsiyet:")
        self.cmb_cinsiyet = QComboBox()
        self.cmb_cinsiyet.addItems(["Erkek", "Kadın", "Diğer"])
        layout.addWidget(self.lbl_cinsiyet)
        layout.addWidget(self.cmb_cinsiyet)

        self.btn_ekle = QPushButton("Hastayı Ekle")
        self.btn_ekle.clicked.connect(self.hasta_ekle)
        layout.addWidget(self.btn_ekle)

        self.setLayout(layout)

    def hasta_ekle(self):
        tc = self.txt_tc.text()
        ad = self.txt_ad.text()
        soyad = self.txt_soyad.text()
        email = self.txt_email.text()
        sifre = self.txt_sifre.text()
        dogum_tarihi = self.txt_dogum_tarihi.text()
        cinsiyet = self.cmb_cinsiyet.currentText()

        if not all([tc, ad, soyad, email, sifre, dogum_tarihi]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        hashed_sifre = hashle(sifre)

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()

            query = """
                INSERT INTO hastalar (tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, doktor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (tc, ad, soyad, email, hashed_sifre, dogum_tarihi, cinsiyet, self.doktor_id))
            conn.commit()

            QMessageBox.information(self, "Başarılı", "Hasta başarıyla eklendi!")

            self.txt_tc.clear()
            self.txt_ad.clear()
            self.txt_soyad.clear()
            self.txt_email.clear()
            self.txt_sifre.clear()
            self.txt_dogum_tarihi.clear()

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
