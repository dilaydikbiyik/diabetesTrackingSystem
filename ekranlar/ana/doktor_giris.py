from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from veritabani import baglanti_kur
from hashleme import hashle
from ekranlar.doktor.doktor_ana_ekran import DoktorAnaEkran

class DoktorGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doktor Girişi")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(300, 300, 350, 200)
        self.setFixedSize(350, 200)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                font-family: Arial;
                font-size: 13px;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.lbl_tc = QLabel("TC Kimlik No:", self)
        self.lbl_tc.move(20, 30)
        self.txt_tc = QLineEdit(self)
        self.txt_tc.move(120, 30)
        self.txt_tc.setPlaceholderText("12345678901")
        self.txt_tc.setFixedWidth(200)

        self.lbl_sifre = QLabel("Şifre:", self)
        self.lbl_sifre.move(20, 70)
        self.txt_sifre = QLineEdit(self)
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        self.txt_sifre.move(120, 70)
        self.txt_sifre.setPlaceholderText("Şifrenizi Giriniz")
        self.txt_sifre.setFixedWidth(200)

        self.btn_giris = QPushButton("Giriş Yap", self)
        self.btn_giris.move(120, 120)
        self.btn_giris.clicked.connect(self.giris_yap)

    def giris_yap(self):
        tc = self.txt_tc.text().strip()
        sifre = self.txt_sifre.text().strip()

        if not tc or not sifre:
            QMessageBox.warning(self, "Uyarı", "Lütfen TC ve şifre alanlarını doldurun!")
            return

        hashed_sifre = hashle(sifre)
        conn = baglanti_kur()

        if not conn:
            QMessageBox.critical(self, "Hata", "Veritabanı bağlantısı kurulamadı!")
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT id, ad, soyad FROM doktorlar
                WHERE tc = %s AND sifre = %s
            """
            cursor.execute(query, (tc, hashed_sifre))
            result = cursor.fetchone()

            if result:
                doktor_id, ad, soyad = result
                QMessageBox.information(self, "Giriş Başarılı", f"Hoşgeldiniz, Dr. {ad} {soyad}")
                self.doktor_ana_ekran = DoktorAnaEkran(doktor_id)
                self.doktor_ana_ekran.show()
                self.close()
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz TC veya şifre!")

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası:\n{e}")
