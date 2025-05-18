from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit, QComboBox
from PyQt5.QtCore import QDate
from veritabani import baglanti_kur

class EgzersizEklemeEkrani(QWidget):
    def __init__(self, hasta_id):
        super().__init__()
        self.hasta_id = hasta_id
        self.setWindowTitle("Egzersiz Ekle")
        self.setGeometry(400, 300, 300, 200)

        # Tarih
        self.lbl_tarih = QLabel("Tarih:", self)
        self.lbl_tarih.move(20, 20)
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.move(120, 20)

        # Egzersiz Türü
        self.lbl_tur = QLabel("Egzersiz Türü:", self)
        self.lbl_tur.move(20, 60)
        self.txt_tur = QLineEdit(self)
        self.txt_tur.setPlaceholderText("Örn: Yürüyüş")
        self.txt_tur.move(120, 60)

        # Durum
        self.lbl_durum = QLabel("Durum:", self)
        self.lbl_durum.move(20, 100)
        self.cmb_durum = QComboBox(self)
        self.cmb_durum.addItems(["yapıldı", "yapılmadı"])
        self.cmb_durum.move(120, 100)

        # Kaydet butonu
        self.btn_kaydet = QPushButton("Kaydet", self)
        self.btn_kaydet.move(120, 140)
        self.btn_kaydet.clicked.connect(self.egzersiz_kaydet)

    def egzersiz_kaydet(self):
        tarih = self.date_edit.date().toPyDate()
        tur = self.txt_tur.text().strip()
        durum = self.cmb_durum.currentText()

        if not tur:
            QMessageBox.warning(self, "Uyarı", "Egzersiz türünü giriniz!")
            return

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            query = """
                INSERT INTO egzersizler (hasta_id, tarih, tur, durum)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.hasta_id, tarih, tur, durum))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Başarılı", "Egzersiz kaydedildi.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri eklenemedi:\n{e}")
