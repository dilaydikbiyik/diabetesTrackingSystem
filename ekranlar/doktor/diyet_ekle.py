from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QDateTimeEdit, QComboBox, QVBoxLayout
from PyQt5.QtCore import QDateTime
from veritabani import baglanti_kur
import pytz
from datetime import datetime

class DiyetEklemeEkrani(QWidget):
    def __init__(self, hasta_id):
        super().__init__()
        self.hasta_id = hasta_id
        self.setWindowTitle("Diyet Ekle")
        self.setGeometry(400, 300, 300, 250)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tarih Saat
        self.lbl_tarih = QLabel("Tarih ve Saat:")
        self.date_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_time_edit.setCalendarPopup(True)
        self.date_time_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")

        # Diyet Türü
        self.lbl_tur = QLabel("Diyet Türü:")
        self.cmb_tur = QComboBox()

        # Durum
        self.lbl_durum = QLabel("Durum:")
        self.cmb_durum = QComboBox()
        self.cmb_durum.addItems(["uygulandı", "uygulanmadı"])

        # Buton
        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.clicked.connect(self.diyet_kaydet)

        # Eklemeler
        self.layout.addWidget(self.lbl_tarih)
        self.layout.addWidget(self.date_time_edit)
        self.layout.addWidget(self.lbl_tur)
        self.layout.addWidget(self.cmb_tur)
        self.layout.addWidget(self.lbl_durum)
        self.layout.addWidget(self.cmb_durum)
        self.layout.addWidget(self.btn_kaydet)

        self.diyet_turlerini_yukle()

    def diyet_turlerini_yukle(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            cursor.execute("SELECT id, ad FROM diyet_tanimlari ORDER BY ad")
            self.turler = cursor.fetchall()
            self.cmb_tur.clear()
            for id, ad in self.turler:
                self.cmb_tur.addItem(ad, id)
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Diyet türleri yüklenemedi:\n{e}")

    def diyet_kaydet(self):
        tarih_saat = self.date_time_edit.dateTime().toPyDateTime()
        tarih_saat = pytz.timezone("Europe/Istanbul").localize(tarih_saat)

        diyet_id = self.cmb_tur.currentData()
        durum = self.cmb_durum.currentText()

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            query = """
                INSERT INTO diyetler (hasta_id, tarih_zaman, diyet_id, durum)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.hasta_id, tarih_saat, diyet_id, durum))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Başarılı", "Diyet kaydedildi.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri eklenemedi:\n{e}")
