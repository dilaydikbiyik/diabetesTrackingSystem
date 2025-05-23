import sys
import hashlib
import random
import string
import smtplib
import psycopg2
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QVBoxLayout, QApplication
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
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
    mesaj = MIMEText(f"Yeni şifreniz: {yeni_sifre}\nLütfen giriş yaptıktan sonra değiştirin.")
    mesaj["Subject"] = "Diyabet Takip Sistemi - Şifre Sıfırlama"
    mesaj["From"] = "diabetestrackingsystem@gmail.com"
    mesaj["To"] = alici_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("diabetestrackingsystem@gmail.com", "rowg rgfa iago dzdg")
        server.send_message(mesaj)
        server.quit()
        return True
    except Exception as e:
        print("Mail gönderme hatası:", e)
        return False


class SifreSifirlaEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Şifremi Unuttum")
        self.setGeometry(500, 300, 400, 180)

        # Arka plan rengi ve yazı tipi
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#e6f0fa"))  # Açık mavi
        self.setPalette(palette)

        self.setFont(QFont("Arial", 10))

        self.layout = QVBoxLayout()

        self.label = QLabel("TC Kimlik Numaranızı Girin:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #003366; font-weight: bold;")

        self.txt_tc = QLineEdit()
        self.txt_tc.setPlaceholderText("Örn: 12345678901")
        self.txt_tc.setMaxLength(11)
        self.txt_tc.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 1px solid #99ccff;
                border-radius: 5px;
                background-color: white;
            }
        """)

        self.btn_gonder = QPushButton("📧 Şifreyi Yenile")
        self.btn_gonder.setStyleSheet("""
            QPushButton {
                background-color: #3399ff;
                color: white;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007acc;
            }
        """)
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

                    onay = QMessageBox(self)
                    onay.setWindowTitle("Onay")
                    onay.setText(f"{gizli} adresine şifre sıfırlama bağlantısı gönderilsin mi?")
                    onay.setIcon(QMessageBox.Question)
                    onay.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    onay.setStyleSheet("""
                        QMessageBox {
                            background-color: #f0f8ff;
                            font-family: Arial;
                        }
                        QLabel {
                            color: #003366;
                            font-size: 12pt;
                        }
                        QPushButton {
                            background-color: #3399ff;
                            color: white;
                            padding: 6px 12px;
                            border-radius: 4px;
                            font-weight: bold;
                            min-width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #007acc;
                        }
                    """)

                    cevap = onay.exec_()
                    if cevap == QMessageBox.Yes:
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
