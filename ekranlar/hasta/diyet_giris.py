from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QDateTimeEdit, QComboBox, QMessageBox
from PyQt5.QtCore import QDateTime

class DiyetGirisPenceresi(QDialog):
    def __init__(self, hasta_id, conn):
        super().__init__()
        self.setWindowTitle("Diyet Girişi")
        self.setFixedSize(300, 250)
        self.hasta_id = hasta_id
        self.conn = conn
        self.cursor = self.conn.cursor()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tarih-saat
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        layout.addWidget(QLabel("Tarih ve Saat:"))
        layout.addWidget(self.datetime_edit)

        # Diyet türü
        self.diyet_combo = QComboBox()
        self.cursor.execute("SELECT id, ad FROM diyet_tanimlari ORDER BY id")
        self.diyetler = self.cursor.fetchall()
        for _, ad in self.diyetler:
            self.diyet_combo.addItem(ad)
        layout.addWidget(QLabel("Diyet Türü:"))
        layout.addWidget(self.diyet_combo)

        # Durum
        self.durum_combo = QComboBox()
        self.durum_combo.addItems(["uygulandı", "uygulanmadı"])
        layout.addWidget(QLabel("Durum:"))
        layout.addWidget(self.durum_combo)

        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.clicked.connect(self.veri_kaydet)
        layout.addWidget(kaydet_btn)

        self.setLayout(layout)

    def veri_kaydet(self):
        zaman = self.datetime_edit.dateTime().toPyDateTime()
        diyet_id = self.diyetler[self.diyet_combo.currentIndex()][0]
        durum = self.durum_combo.currentText()

        self.cursor.execute("""
            INSERT INTO diyetler (hasta_id, tarih_zaman, diyet_id, durum)
            VALUES (%s, %s, %s, %s)
        """, (self.hasta_id, zaman, diyet_id, durum))
        self.conn.commit()

        QMessageBox.information(self, "Başarılı", "Diyet bilgisi kaydedildi.")
        self.accept()
