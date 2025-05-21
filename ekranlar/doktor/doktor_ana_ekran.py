import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QListWidget, QVBoxLayout, QWidget,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from veritabani import baglanti_kur
from ekranlar.doktor.doktor_hasta_ekle import HastaEklemeEkrani
from ekranlar.kan_sekeri.kan_sekeri_ekle import KanSekeriEklemeEkrani
from ekranlar.doktor.egzersiz_ekle import EgzersizEklemeEkrani
from ekranlar.doktor.diyet_ekle import DiyetEklemeEkrani
from ekranlar.kan_sekeri.kan_sekeri_grafik import KanSekeriGrafik


class DoktorAnaEkran(QMainWindow):
    def __init__(self, doktor_id):
        super().__init__()
        self.doktor_id = doktor_id
        self.setWindowTitle("Doktor Ana Ekranı")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(300, 100, 520, 550)

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Genel stil (arka plan ve yazı)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                font-family: Arial;
                font-size: 13px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;              /* Buton yazı büyüklüğü */
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
            }
        """)

        # Başlık
        baslik = QLabel("Hastalarınız:")
        baslik.setFont(QFont("Arial", 13, QFont.Bold))
        self.layout.addWidget(baslik, alignment=Qt.AlignLeft)

        # Hasta listesi
        self.hasta_listesi = QListWidget()
        self.hasta_listesi.setFont(QFont("Arial", 12))  # Yazı büyüklüğü
        self.hasta_listesi.setMinimumHeight(200)
        self.hasta_listesi.setMaximumHeight(300)
        self.layout.addWidget(self.hasta_listesi)

        # Butonlar
        self.btn_detay = QPushButton("📊 Hasta Detaylarını Görüntüle")
        self.btn_detay.clicked.connect(self.hasta_detay_goster)
        self.layout.addWidget(self.btn_detay)

        self.btn_hasta_ekle = QPushButton("➕ Yeni Hasta Ekle")
        self.btn_hasta_ekle.clicked.connect(self.hasta_ekle_ekranini_ac)
        self.layout.addWidget(self.btn_hasta_ekle)

        self.btn_kan_sekeri_ekle = QPushButton("🩸 Kan Şekeri Ekle")
        self.btn_kan_sekeri_ekle.clicked.connect(self.kan_sekeri_ekle_ekranini_ac)
        self.layout.addWidget(self.btn_kan_sekeri_ekle)

        self.btn_egzersiz_ekle = QPushButton("🤸 Egzersiz Ekle")
        self.btn_egzersiz_ekle.clicked.connect(self.egzersiz_ekle_ekranini_ac)
        self.layout.addWidget(self.btn_egzersiz_ekle)

        self.btn_diyet_ekle = QPushButton("🥗 Diyet Ekle")
        self.btn_diyet_ekle.clicked.connect(self.diyet_ekle_ekranini_ac)
        self.layout.addWidget(self.btn_diyet_ekle)

        self.btn_grafik = QPushButton("📈 Kan Şekeri Grafiği")
        self.btn_grafik.clicked.connect(self.kan_sekeri_grafik_ac)
        self.layout.addWidget(self.btn_grafik)

        self.btn_hastalik_teshisi = QPushButton("🩺 Hastalık Teşhisi")
        self.btn_hastalik_teshisi.clicked.connect(self.hastalik_teshisi_ekranini_ac)
        self.layout.addWidget(self.btn_hastalik_teshisi)

        for btn in [self.btn_detay, self.btn_hasta_ekle, self.btn_kan_sekeri_ekle,
                    self.btn_egzersiz_ekle, self.btn_diyet_ekle, self.btn_grafik]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(45)

        # Hastaları getir
        self.hastalari_getir()

    def hastalari_getir(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            query = """
                SELECT id, ad, soyad FROM hastalar 
                WHERE doktor_id = %s
            """
            cursor.execute(query, (self.doktor_id,))
            hastalar = cursor.fetchall()
            self.hasta_listesi.clear()
            for hasta in hastalar:
                hasta_id, ad, soyad = hasta
                self.hasta_listesi.addItem(f"{hasta_id} - {ad} {soyad}")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def hasta_detay_goster(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return
        hasta_id_str = self.hasta_listesi.currentItem().text().split(" - ")[0]
        hasta_id = int(hasta_id_str)

        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            query = """
                SELECT tarih_zaman, kan_sekeri 
                FROM kan_sekeri 
                WHERE hasta_id = %s
                ORDER BY tarih_zaman DESC
            """
            cursor.execute(query, (hasta_id,))
            kan_sekeri_verileri = cursor.fetchall()
            cursor.close()
            conn.close()

            if kan_sekeri_verileri:
                mesaj = "Kan Şekeri Verileri:\n"
                for veri in kan_sekeri_verileri:
                    tarih_saat, kan_sekeri = veri
                    mesaj += f"Tarih: {tarih_saat}, Kan Şekeri: {kan_sekeri}\n"
                QMessageBox.information(self, "Kan Şekeri Verileri", mesaj)
            else:
                QMessageBox.information(self, "Bilgi", "Bu hastanın kan şekeri verisi bulunmuyor.")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def hasta_ekle_ekranini_ac(self):
        self.hasta_ekle_ekrani = HastaEklemeEkrani(self.doktor_id)
        self.hasta_ekle_ekrani.show()

    def kan_sekeri_ekle_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return
        hasta_id_str = self.hasta_listesi.currentItem().text().split(" - ")[0]
        hasta_id = int(hasta_id_str)
        self.kan_sekeri_ekle_ekrani = KanSekeriEklemeEkrani(hasta_id=hasta_id)
        self.kan_sekeri_ekle_ekrani.show()

    def egzersiz_ekle_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return

        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.egzersiz_ekrani = EgzersizEklemeEkrani(hasta_id)
        self.egzersiz_ekrani.show()

    def diyet_ekle_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return

        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.diyet_ekrani = DiyetEklemeEkrani(hasta_id)
        self.diyet_ekrani.show()

    def kan_sekeri_grafik_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return

        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.grafik_pencere = KanSekeriGrafik(hasta_id)
        self.grafik_pencere.show()

    def hastalik_teshisi_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return

        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        from ekranlar.doktor.hastalik_teshisi import HastalikTeshisiEkrani
        self.teshis_pencere = HastalikTeshisiEkrani(hasta_id)
        self.teshis_pencere.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    doktor_ekran = DoktorAnaEkran(doktor_id=1)
    doktor_ekran.show()
    sys.exit(app.exec())