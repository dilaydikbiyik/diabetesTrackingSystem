from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QFormLayout,
    QDateTimeEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import QDateTime, Qt

MAC_STYLE = """
QDialog {
    background-color: #f9fafb;
    font-family: -apple-system, 'Segoe UI', Arial, sans-serif;
    color: #1a1a2e;
}
QLabel {
    font-size: 13px;
    color: #374151;
    font-weight: 600;
}
QDateTimeEdit {
    background-color: white;
    border: 1.5px solid #d1d5db;
    border-radius: 7px;
    padding: 8px 10px;
    font-size: 13px;
    color: #111827;
    min-height: 36px;
}
QDateTimeEdit:focus {
    border-color: #7c3aed;
}
QComboBox {
    background-color: white;
    border: 1.5px solid #d1d5db;
    border-radius: 7px;
    padding: 8px 10px;
    font-size: 13px;
    color: #111827;
    min-height: 36px;
    min-width: 160px;
}
QComboBox:focus {
    border-color: #7c3aed;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background-color: white;
    color: #111827;
    selection-background-color: #ede9fe;
    selection-color: #4c1d95;
    border: 1px solid #d1d5db;
}
QPushButton#saveBtn {
    background-color: #7c3aed;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 11px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton#saveBtn:hover { background-color: #6d28d9; }
QPushButton#saveBtn:pressed { background-color: #5b21b6; }
"""


class EgzersizGirisPenceresi(QDialog):
    def __init__(self, hasta_id, conn):
        super().__init__()
        self.setWindowTitle("Egzersiz Girisi")
        self.setMinimumSize(380, 320)
        self.resize(380, 340)
        self.hasta_id = hasta_id
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.setStyleSheet(MAC_STYLE)
        self.init_ui()

    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        title = QLabel("Egzersiz Bilgisi Ekle")
        title.setStyleSheet("font-size: 17px; font-weight: bold; color: #4c1d95;")
        title.setAlignment(Qt.AlignCenter)
        outer.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft)

        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        self.datetime_edit.setCalendarPopup(True)

        self.egzersiz_combo = QComboBox()
        self.cursor.execute("SELECT id, tur_adi FROM egzersiz_turleri ORDER BY id")
        self.egzersizler = self.cursor.fetchall()
        for _, ad in self.egzersizler:
            self.egzersiz_combo.addItem(ad)

        self.durum_combo = QComboBox()
        self.cursor.execute("SELECT id, durum_adi FROM egzersiz_durumlari ORDER BY id")
        self.durumlar = self.cursor.fetchall()
        for _, ad in self.durumlar:
            self.durum_combo.addItem(ad)

        form.addRow("Tarih ve Saat", self.datetime_edit)
        form.addRow("Egzersiz Türü", self.egzersiz_combo)
        form.addRow("Durum", self.durum_combo)
        outer.addLayout(form)

        kaydet_btn = QPushButton("Kaydet", objectName="saveBtn")
        kaydet_btn.setMinimumHeight(44)
        kaydet_btn.setCursor(Qt.PointingHandCursor)
        kaydet_btn.clicked.connect(self.veri_kaydet)
        outer.addWidget(kaydet_btn)

    def veri_kaydet(self):
        tarih = self.datetime_edit.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        tur_id = self.egzersizler[self.egzersiz_combo.currentIndex()][0]
        durum_id = self.durumlar[self.durum_combo.currentIndex()][0]

        self.cursor.execute("""
            INSERT INTO egzersizler (hasta_id, tarih_zaman, tur_id, durum_id)
            VALUES (?, ?, ?, ?)
        """, (self.hasta_id, tarih, tur_id, durum_id))
        self.conn.commit()

        QMessageBox.information(self, "Basarili", "Egzersiz verisi kaydedildi.")
        self.accept()
