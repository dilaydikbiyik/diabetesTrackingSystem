from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QVBoxLayout, QDateTimeEdit
from PyQt5.QtCore import QDateTime
from veritabani import baglanti_kur

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
        tarih_saat = self.dt_tarih_saat.dateTime().toString("yyyy-MM-dd HH:mm:ss")
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

            query = """
                        INSERT INTO kan_sekeri (hasta_id, tarih_zaman, kan_sekeri)
                        VALUES (%s, %s, %s)
                    """
            cursor.execute(query, (self.hasta_id, tarih_saat, kan_sekeri))
            conn.commit()

            QMessageBox.information(self, "Başarılı", "Kan şekeri verisi eklendi!")
            self.txt_kan_sekeri.clear()

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")