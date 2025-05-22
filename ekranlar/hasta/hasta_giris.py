from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from veritabani import baglanti_kur
from hashleme import hashle
from ekranlar.hasta.hasta_ana_ekran import HastaAnaEkrani

class HastaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hasta Girişi")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(300, 300, 350, 200)
        self.setFixedSize(350, 200)

        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
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
                background-color: #dc3545;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)

        # TC Kimlik No
        self.lbl_tc = QLabel("TC Kimlik No:", self)
        self.lbl_tc.move(20, 30)
        self.txt_tc = QLineEdit(self)
        self.txt_tc.move(120, 30)
        self.txt_tc.setPlaceholderText("12345678901")
        self.txt_tc.setFixedWidth(200)

        # Şifre
        self.lbl_sifre = QLabel("Şifre:", self)
        self.lbl_sifre.move(20, 70)
        self.txt_sifre = QLineEdit(self)
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        self.txt_sifre.move(120, 70)
        self.txt_sifre.setPlaceholderText("Şifrenizi Giriniz")
        self.txt_sifre.setFixedWidth(200)

        # Giriş Butonu
        self.btn_giris = QPushButton("Giriş Yap", self)
        self.btn_giris.move(120, 120)
        self.btn_giris.clicked.connect(self.giris_yap)

    def giris_yap(self):
        tc = self.txt_tc.text().strip()
        sifre = self.txt_sifre.text().strip()

        if not tc or not sifre:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        hashed_sifre = hashle(sifre)
        conn = baglanti_kur()

        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT ad, soyad FROM hastalar 
                    WHERE tc = %s AND sifre = %s
                """
                cursor.execute(query, (tc, hashed_sifre))
                result = cursor.fetchone()

                if result:
                    ad, soyad = result
                    QMessageBox.information(self, "Başarılı", f"Hoş geldiniz, {ad} {soyad}")
                    self.hasta_ekrani = HastaAnaEkrani(ad, soyad, tc)
                    self.hasta_ekrani.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Hata", "Giriş bilgileri hatalı veya hasta bulunamadı.")

                cursor.close()
                conn.close()

            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Veritabanı hatası:\n{e}")
        else:
            QMessageBox.critical(self, "Bağlantı Hatası", "Veritabanı bağlantısı sağlanamadı.")
