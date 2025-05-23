from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QDateTimeEdit, QComboBox, QMessageBox
from PyQt5.QtCore import QDateTime

class EgzersizGirisPenceresi(QDialog):
    def __init__(self, hasta_id, conn):
        super().__init__()
        self.setWindowTitle("Egzersiz Girişi")
        self.setFixedSize(300, 250)
        self.hasta_id = hasta_id
        self.conn = conn
        self.cursor = self.conn.cursor()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tarih-saat seçimi
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        layout.addWidget(QLabel("Tarih ve Saat:"))
        layout.addWidget(self.datetime_edit)

        # Egzersiz türü
        self.egzersiz_combo = QComboBox()
        self.cursor.execute("SELECT id, tur_adi FROM egzersiz_turleri ORDER BY id")
        self.egzersizler = self.cursor.fetchall()
        for _, ad in self.egzersizler:
            self.egzersiz_combo.addItem(ad)
        layout.addWidget(QLabel("Egzersiz Türü:"))
        layout.addWidget(self.egzersiz_combo)

        # Durum (yapıldı/yapılmadı)
        self.durum_combo = QComboBox()
        self.cursor.execute("SELECT id, durum_adi FROM egzersiz_durumlari ORDER BY id")
        self.durumlar = self.cursor.fetchall()
        for _, ad in self.durumlar:
            self.durum_combo.addItem(ad)
        layout.addWidget(QLabel("Durum:"))
        layout.addWidget(self.durum_combo)

        # Kaydet butonu
        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.clicked.connect(self.veri_kaydet)
        layout.addWidget(kaydet_btn)

        self.setLayout(layout)

    def veri_kaydet(self):
        tarih = self.datetime_edit.dateTime().toPyDateTime()
        tur_id = self.egzersizler[self.egzersiz_combo.currentIndex()][0]
        durum_id = self.durumlar[self.durum_combo.currentIndex()][0]

        self.cursor.execute("""
            INSERT INTO egzersizler (hasta_id, tarih_zaman, tur_id, durum_id)
            VALUES (%s, %s, %s, %s)
        """, (self.hasta_id, tarih, tur_id, durum_id))
        self.conn.commit()

        QMessageBox.information(self, "Başarılı", "Egzersiz verisi kaydedildi.")
        self.accept()
