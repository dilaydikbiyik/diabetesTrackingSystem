from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDateTimeEdit, QMessageBox
from PyQt5.QtCore import QDateTime
from datetime import datetime

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

class KanSekeriGirisPenceresi(QDialog):
    def __init__(self, hasta_id, conn):
        super().__init__()
        self.setWindowTitle("Kan Şekeri Girişi")
        self.setFixedSize(300, 200)
        self.hasta_id = hasta_id
        self.conn = conn
        self.cursor = self.conn.cursor()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        layout.addWidget(QLabel("Tarih ve Saat:"))
        layout.addWidget(self.datetime_edit)

        self.giris_edit = QLineEdit()
        self.giris_edit.setPlaceholderText("Örn: 120")
        layout.addWidget(QLabel("Kan Şekeri (mg/dL):"))
        layout.addWidget(self.giris_edit)

        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.clicked.connect(self.veri_kaydet)
        layout.addWidget(kaydet_btn)

        self.setLayout(layout)

    def veri_kaydet(self):
        try:
            seviye = int(self.giris_edit.text())
            if seviye < 20 or seviye > 500:
                raise ValueError("Kan şekeri değeri aralık dışında.")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir sayı girin (20-500 arası)")
            return

        zaman = self.datetime_edit.dateTime().toPyDateTime()
        grup = saat_araligina_gore_grup(zaman)

        self.cursor.execute("""
            INSERT INTO kan_sekeri (hasta_id, tarih_zaman, kan_sekeri, olcum_grubu)
            VALUES (%s, %s, %s, %s)
        """, (self.hasta_id, zaman, seviye, grup))
        self.conn.commit()

        if not grup:
            QMessageBox.warning(self, "Uyarı", "⚠️ Bu saat dışı bir ölçümdür. Ortalamaya dahil edilmeyecek.")
        else:
            QMessageBox.information(self, "Başarılı", f"{grup.title()} ölçümü başarıyla kaydedildi.")

        self.accept()
