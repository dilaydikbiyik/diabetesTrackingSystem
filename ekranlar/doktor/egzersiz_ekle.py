from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QDateTimeEdit, QComboBox, QVBoxLayout
from PyQt5.QtCore import QDateTime
from veritabani import baglanti_kur
from datetime import datetime
import pytz

class EgzersizEklemeEkrani(QWidget):
    def __init__(self, hasta_id):
        super().__init__()
        self.hasta_id = hasta_id
        self.setWindowTitle("Egzersiz Ekle")
        self.setGeometry(400, 300, 300, 250)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tarih-Saat
        self.lbl_tarih = QLabel("Tarih ve Saat:")
        self.date_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_time_edit.setCalendarPopup(True)
        self.date_time_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")

        # Egzersiz Türü
        self.lbl_tur = QLabel("Egzersiz Türü:")
        self.cmb_tur = QComboBox()

        # Egzersiz Durumu
        self.lbl_durum = QLabel("Durum:")
        self.cmb_durum = QComboBox()

        # Kaydet Butonu
        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.clicked.connect(self.egzersiz_kaydet)

        # Ekle
        self.layout.addWidget(self.lbl_tarih)
        self.layout.addWidget(self.date_time_edit)
        self.layout.addWidget(self.lbl_tur)
        self.layout.addWidget(self.cmb_tur)
        self.layout.addWidget(self.lbl_durum)
        self.layout.addWidget(self.cmb_durum)
        self.layout.addWidget(self.btn_kaydet)

        self.egzersiz_turleri_yukle()
        self.egzersiz_durumlari_yukle()

    def egzersiz_turleri_yukle(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            cursor.execute("SELECT id, tur_adi FROM egzersiz_turleri ORDER BY tur_adi")
            self.turler = cursor.fetchall()
            self.cmb_tur.clear()
            for id, ad in self.turler:
                self.cmb_tur.addItem(ad, id)
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Egzersiz türleri yüklenemedi:\n{e}")

    def egzersiz_durumlari_yukle(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            cursor.execute("SELECT id, durum_adi FROM egzersiz_durumlari ORDER BY durum_adi")
            self.durumlar = cursor.fetchall()
            self.cmb_durum.clear()
            for id, ad in self.durumlar:
                self.cmb_durum.addItem(ad, id)
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Egzersiz durumları yüklenemedi:\n{e}")

    def egzersiz_kaydet(self):
        tarih_saat = self.date_time_edit.dateTime().toPyDateTime()
        tarih_saat = pytz.timezone("Europe/Istanbul").localize(tarih_saat)

        tur_id = self.cmb_tur.currentData()
        durum_id = self.cmb_durum.currentData()

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            query = """
                INSERT INTO egzersizler (hasta_id, tarih_zaman, tur_id, durum_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.hasta_id, tarih_saat, tur_id, durum_id))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Başarılı", "Egzersiz başarıyla eklendi.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri eklenemedi:\n{e}")
