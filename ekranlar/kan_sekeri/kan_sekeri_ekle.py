from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QVBoxLayout, QDateTimeEdit
from PyQt5.QtCore import QDateTime
from veritabani import baglanti_kur
from datetime import datetime
import pytz

def saat_araligina_gore_grup(zaman):
    saat = zaman.hour
    dakika = zaman.minute
    if 7 <= saat < 8 or (saat == 8 and dakika == 0):
        return "sabah"
    elif 12 <= saat < 13 or (saat == 13 and dakika == 0):
        return "öğle"
    elif 15 <= saat < 16 or (saat == 16 and dakika == 0):
        return "ikindi"
    elif 18 <= saat < 19 or (saat == 19 and dakika == 0):
        return "akşam"
    elif 22 <= saat < 23 or (saat == 23 and dakika == 0):
        return "gece"
    return None

class KanSekeriEklemeEkrani(QWidget):
    def __init__(self, hasta_id):
        super().__init__()
        self.hasta_id = hasta_id
        self.setWindowTitle("Kan Şekeri Girişi")
        self.setGeometry(400, 300, 300, 250)

        layout = QVBoxLayout()

        self.lbl_tarih_saat = QLabel("Tarih ve Saat:")
        self.dt_tarih_saat = QDateTimeEdit(QDateTime.currentDateTime())
        self.dt_tarih_saat.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        layout.addWidget(self.lbl_tarih_saat)
        layout.addWidget(self.dt_tarih_saat)

        self.lbl_kan_sekeri = QLabel("Kan Şekeri (mg/dL):")
        self.txt_kan_sekeri = QLineEdit()
        self.txt_kan_sekeri.setPlaceholderText("20-500 arası bir değer giriniz")
        layout.addWidget(self.lbl_kan_sekeri)
        layout.addWidget(self.txt_kan_sekeri)

        self.btn_ekle = QPushButton("Kan Şekeri Ekle")
        self.btn_ekle.clicked.connect(self.kan_sekeri_ekle)
        layout.addWidget(self.btn_ekle)

        self.setLayout(layout)

    def kan_sekeri_ekle(self):
        tarih_saat = self.dt_tarih_saat.dateTime().toPyDateTime()
        tarih_saat = pytz.timezone("Europe/Istanbul").localize(tarih_saat)

        grup = saat_araligina_gore_grup(tarih_saat)
        kan_sekeri_str = self.txt_kan_sekeri.text()

        if not kan_sekeri_str:
            QMessageBox.warning(self, "Hata", "Lütfen kan şekeri değerini giriniz!")
            return

        try:
            kan_sekeri = int(kan_sekeri_str)
            if not (20 <= kan_sekeri <= 500):
                raise ValueError("Kan şekeri 20-500 aralığında olmalıdır.")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
            return

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()

            # Kan şekeri verisini ekle
            cursor.execute("""
                INSERT INTO kan_sekeri (hasta_id, tarih_zaman, kan_sekeri, olcum_grubu)
                VALUES (%s, %s, %s, %s)
            """, (self.hasta_id, tarih_saat, kan_sekeri, grup))

            # Uyarı üretimi
            uyari_tip_id = None
            mesaj = None

            if kan_sekeri < 70:
                uyari_tip_id = 1
                mesaj = "Hastanın kan şekeri seviyesi 70 mg/dL'nin altına düştü. Hipoglisemi riski! Hızlı müdahale gerekebilir."
            elif 111 <= kan_sekeri <= 150:
                uyari_tip_id = 3
                mesaj = "Hastanın kan şekeri 111-150 mg/dL arasında. Durum izlenmeli."
            elif 151 <= kan_sekeri <= 200:
                uyari_tip_id = 4
                mesaj = "Hastanın kan şekeri 151-200 mg/dL arasında. Diyabet kontrolü gereklidir."
            elif kan_sekeri > 200:
                uyari_tip_id = 5
                mesaj = "Hastanın kan şekeri 200 mg/dL'nin üzerinde. Hiperglisemi durumu. Acil müdahale gerekebilir."

            if uyari_tip_id and mesaj:
                cursor.execute("""
                    INSERT INTO uyarilar (hasta_id, tip_id, mesaj, zaman)
                    VALUES (%s, %s, %s, %s)
                """, (self.hasta_id, uyari_tip_id, mesaj, tarih_saat))

            conn.commit()

            if not grup:
                QMessageBox.warning(self, "Uyarı", "Bu saat dışı bir ölçümdür. Ortalamaya dahil edilmeyecek.")
            else:
                QMessageBox.information(self, "Başarılı", f"{grup.title()} ölçümü başarıyla eklendi.")

            self.txt_kan_sekeri.clear()
            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")


