import sys
import hashlib
import random
import string
import smtplib
import psycopg2
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QVBoxLayout, QApplication)
from email.mime.text import MIMEText

from veritabani import baglanti_kur


def gizle_email(email):
    kullanici, domain = email.split("@")
    gizli = kullanici[:3] + "*" * (len(kullanici) - 6) + kullanici[-3:]
    return f"{gizli}@{domain}"


def yeni_sifre_uret():
    karakterler = string.ascii_letters + string.digits + "!@#"
    return ''.join(random.choices(karakterler, k=8))


def hashle(sifre):
    return hashlib.sha256(sifre.encode()).digest()


def mail_gonder(alici_email, yeni_sifre):
    mesaj = MIMEText(f"Yeni şifreniz: {yeni_sifre}\nLütfen giris yaptiktan sonra degistirin.")
    mesaj["Subject"] = "Diyabet Takip Sistemi - Şifre Sıfırlama"
    mesaj["From"] = "merome813@gmail.com"  # kendi gmail adresin
    mesaj["To"] = alici_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("merome813@gmail.com", "srkc dako ymmi bqkt")
        server.send_message(mesaj)
        server.quit()
        return True
    except Exception as e:
        print("Mail gönderme hatası:", e)
        return False


class SifreSifirlaEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifremi Unuttum")
        self.setGeometry(500, 300, 350, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("TC Kimlik Numaranızı Girin:")
        self.txt_tc = QLineEdit()
        self.txt_tc.setPlaceholderText("12345678901")

        self.btn_gonder = QPushButton("Şifreyi Yenile")
        self.btn_gonder.clicked.connect(self.sifre_yenile)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.txt_tc)
        self.layout.addWidget(self.btn_gonder)
        self.setLayout(self.layout)

    def sifre_yenile(self):
        tc = self.txt_tc.text().strip()

        if not tc:
            QMessageBox.warning(self, "Uyarı", "Lütfen TC numarasını girin.")
            return

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()

            for tablo in ["doktorlar", "hastalar"]:
                cursor.execute(f"SELECT id, email FROM {tablo} WHERE tc = %s", (tc,))
                sonuc = cursor.fetchone()
                if sonuc:
                    kullanici_id, email = sonuc
                    gizli = gizle_email(email)

                    onay = QMessageBox.question(self, "Onay",
                                                 f"{gizli} adresine şifre sıfırlama bağlantısı gönderilsin mi?",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if onay == QMessageBox.Yes:
                        yeni_sifre = yeni_sifre_uret()
                        hashed = hashle(yeni_sifre)

                        cursor.execute(f"UPDATE {tablo} SET sifre = %s WHERE id = %s",
                                       (hashed, kullanici_id))
                        conn.commit()

                        if mail_gonder(email, yeni_sifre):
                            QMessageBox.information(self, "Başarılı", "Yeni şifre e-posta adresinize gönderildi.")
                        else:
                            QMessageBox.critical(self, "Hata", "Mail gönderilemedi.")
                    break
            else:
                QMessageBox.warning(self, "Bulunamadı", "Bu TC'ye sahip bir kayıt bulunamadı.")

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = SifreSifirlaEkrani()
    pencere.show()
    sys.exit(app.exec())
