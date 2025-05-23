import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QListWidget, QVBoxLayout, QWidget,
    QPushButton, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
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
        self.setGeometry(300, 100, 520, 600)

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Doktor bilgileri üst kısım
        self.doktor_bilgi_widget = QWidget()
        self.doktor_bilgi_layout = QVBoxLayout()
        self.doktor_bilgi_widget.setLayout(self.doktor_bilgi_layout)
        self.doktor_bilgi_widget.setStyleSheet("background-color: #e3f2fd; padding: 10px; border-radius: 6px;")
        self.layout.addWidget(self.doktor_bilgi_widget)

        # Profil resmi
        self.lbl_resim = QLabel()
        self.lbl_resim.setFixedSize(80, 80)
        self.lbl_resim.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        self.lbl_resim.setAlignment(Qt.AlignCenter)

        # Bilgi etiketleri
        self.lbl_ad = QLabel("Ad Soyad")
        self.lbl_email = QLabel("E-posta")
        self.lbl_uzmanlik = QLabel("Uzmanlık")

        for lbl in [self.lbl_ad, self.lbl_email, self.lbl_uzmanlik]:
            lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #333;")

        self.doktor_bilgi_layout.addWidget(self.lbl_resim, alignment=Qt.AlignLeft)
        self.doktor_bilgi_layout.addWidget(self.lbl_ad)
        self.doktor_bilgi_layout.addWidget(self.lbl_email)
        self.doktor_bilgi_layout.addWidget(self.lbl_uzmanlik)

        # Doktor bilgilerini yükle
        self.doktor_bilgilerini_yukle()

        # Stil
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
                font-size: 14px;
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
        self.hasta_listesi.setFont(QFont("Arial", 12))
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

        self.btn_arsiv_goruntule = QPushButton("💾 Arşiv Görüntüle")
        self.btn_arsiv_goruntule.clicked.connect(self.arsiv_goruntule_ekranini_ac)
        self.layout.addWidget(self.btn_arsiv_goruntule)

        for btn in [self.btn_detay, self.btn_hasta_ekle, self.btn_kan_sekeri_ekle,
                    self.btn_egzersiz_ekle, self.btn_diyet_ekle, self.btn_grafik,
                    self.btn_hastalik_teshisi, self.btn_arsiv_goruntule]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(45)

        # Hastaları getir
        self.hastalari_getir()

    def doktor_bilgilerini_yukle(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ad, soyad, email, uzmanlik_alani, profil_resmi
                FROM doktorlar
                WHERE id = %s
            """, (self.doktor_id,))
            doktor = cursor.fetchone()
            if doktor:
                ad, soyad, email, uzmanlik, resim = doktor
                self.lbl_ad.setText(f"👨‍⚕️ {ad} {soyad}")
                self.lbl_email.setText(f"📧 {email}")
                self.lbl_uzmanlik.setText(f"🩺 Uzmanlık: {uzmanlik}")

                if resim:
                    pixmap = QPixmap()
                    pixmap.loadFromData(resim)
                    self.lbl_resim.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Doktor bilgileri alınamadı:\n{e}")

    def hastalari_getir(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            query = "SELECT id, ad, soyad FROM hastalar WHERE doktor_id = %s"
            cursor.execute(query, (self.doktor_id,))
            hastalar = cursor.fetchall()
            self.hasta_listesi.clear()
            for hasta_id, ad, soyad in hastalar:
                self.hasta_listesi.addItem(f"{hasta_id} - {ad} {soyad}")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def hasta_detay_goster(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tarih_zaman, kan_sekeri FROM kan_sekeri
                WHERE hasta_id = %s ORDER BY tarih_zaman DESC
            """, (hasta_id,))
            veriler = cursor.fetchall()
            cursor.close()
            conn.close()

            if veriler:
                mesaj = "Kan Şekeri Verileri:\n"
                for tarih, seviye in veriler:
                    mesaj += f"Tarih: {tarih}, Seviye: {seviye}\n"
                QMessageBox.information(self, "Detay", mesaj)
            else:
                QMessageBox.information(self, "Bilgi", "Veri bulunamadı.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def hasta_ekle_ekranini_ac(self):
        self.hasta_ekle_ekrani = HastaEklemeEkrani(self.doktor_id)
        self.hasta_ekle_ekrani.show()

    def kan_sekeri_ekle_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.kan_sekeri_ekle_ekrani = KanSekeriEklemeEkrani(hasta_id)
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

    def arsiv_goruntule_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        from ekranlar.doktor.arsiv_goruntule import ArsivEkrani
        self.arsiv_pencere = ArsivEkrani(hasta_id)
        self.arsiv_pencere.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    doktor_ekran = DoktorAnaEkran(doktor_id=1)
    doktor_ekran.show()
    sys.exit(app.exec())