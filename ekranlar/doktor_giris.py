from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QWidget
from veritabani import baglanti_kur
from hashleme import hashle
from ekranlar.doktor_ana_ekran import DoktorAnaEkran

class DoktorGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doktor Girişi")
        self.setGeometry(300,300,300,200)

        self.lbl_tc =QLabel("TC Kimlik No:", self)
        self.lbl_tc.move(20,30)
        self.txt_tc = QLineEdit(self)
        self.txt_tc.move(120,30)
        self.txt_tc.setPlaceholderText("12345678901")

        self.lbl_sifre= QLabel("Şifre:",self)
        self.lbl_sifre.move(20,70)
        self.txt_sifre =QLineEdit(self)
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        self.txt_sifre.move(120,70)
        self.txt_sifre.setPlaceholderText("Şifrenizi Giriniz")

        self.btn_giris= QPushButton("Giriş Yap",self)
        self.btn_giris.move(120,110)
        self.btn_giris.clicked.connect(self.giris_yap)

    def giris_yap(self):
        tc= self.txt_tc.text()
        sifre= self.txt_sifre.text()

        if not tc or not sifre:
            QMessageBox.warning(self,"Hata","Lütfen tüm alanları doldurun!")
            return

        hashed_sifre= hashle(sifre)

        conn = baglanti_kur()

        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT id, ad, soyad FROM doktorlar WHERE tc = %s AND sifre = %s"
                cursor.execute(query, (tc, hashed_sifre))
                result = cursor.fetchone()

                if result:
                    doktor_id, ad, soyad = result
                    QMessageBox.information(self, "Başarılı", f"Hoşgeldiniz, Dr. {ad} {soyad}")

                    # Doktor ana ekranını aç
                    self.doktor_ana_ekran = DoktorAnaEkran(doktor_id=doktor_id)
                    self.doktor_ana_ekran.show()

                    self.close()
                else:
                    QMessageBox.warning(self, "Hata", "Doktor bulunamadı!")

                cursor.close()
                conn.close()

            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bağlantı hatası: {e}")