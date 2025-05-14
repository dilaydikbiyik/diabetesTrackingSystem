from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from veritabani import baglanti_kur
from hashleme import hashle

class HastaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hasta Girişi")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(300, 300, 300, 200)

        # TC Kimlik No
        self.lbl_tc = QLabel("TC Kimlik No:", self)
        self.lbl_tc.move(20, 30)
        self.txt_tc = QLineEdit(self)
        self.txt_tc.move(120, 30)
        self.txt_tc.setPlaceholderText("12345678901")

        # Şifre
        self.lbl_sifre = QLabel("Şifre:", self)
        self.lbl_sifre.move(20, 70)
        self.txt_sifre = QLineEdit(self)
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        self.txt_sifre.move(120, 70)
        self.txt_sifre.setPlaceholderText("Şifrenizi Giriniz")

        # Giriş Butonu
        self.btn_giris = QPushButton("Giriş Yap", self)
        self.btn_giris.move(120, 110)
        self.btn_giris.clicked.connect(self.giris_yap)

    def giris_yap(self):
        """
        Giriş yap butonuna tıklandığında çalışır.
        Kullanıcıdan alınan TC ve şifre bilgilerini kontrol eder.
        """
        tc = self.txt_tc.text()
        sifre = self.txt_sifre.text()

        # Alanların boş olup olmadığını kontrol et
        if not tc or not sifre:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        # Şifreyi hashle
        hashed_sifre = hashle(sifre)

        # Veritabanı bağlantısı
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
                    # 🔽 Burada yeni ekranı açıyoruz
                    from ekranlar.hasta_ana_ekran import HastaAnaEkrani  # konuma göre ayarla
                    self.hasta_ekrani = HastaAnaEkrani(ad, soyad, tc)
                    self.hasta_ekrani.show()
                    self.close()  # Giriş ekranını kapat
                else:
                    QMessageBox.warning(self, "Hata", "Hasta bulunamadı!")

                cursor.close()
                conn.close()

            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bağlantı hatası: {e}")
