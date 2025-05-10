import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidget, QVBoxLayout, QWidget, QPushButton, QMessageBox
from veritabani import baglanti_kur
from ekranlar.doktor_hasta_ekle import HastaEklemeEkrani
from ekranlar.kan_sekeri_ekle import KanSekeriEklemeEkrani

class DoktorAnaEkran(QMainWindow):
    def __init__(self, doktor_id):
        super().__init__()
        self.doktor_id = doktor_id
        self.setWindowTitle("Doktor Ana Ekranı")
        self.setGeometry(300, 100, 400, 400)

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Hasta listesi
        self.hasta_listesi = QListWidget()
        self.layout.addWidget(QLabel("Hastalarınız:"))
        self.layout.addWidget(self.hasta_listesi)

        # Seçili hastanın verilerini görmek için buton
        self.btn_detay = QPushButton("Hasta Detaylarını Görüntüle")
        self.btn_detay.clicked.connect(self.hasta_detay_goster)
        self.layout.addWidget(self.btn_detay)

        # DoktorAnaEkran sınıfının init fonksiyonuna ekle
        self.btn_hasta_ekle = QPushButton("Yeni Hasta Ekle")
        self.btn_hasta_ekle.clicked.connect(self.hasta_ekle_ekranini_ac)
        self.layout.addWidget(self.btn_hasta_ekle)

        # DoktorAnaEkran sınıfının init fonksiyonuna ekle
        self.btn_kan_sekeri_ekle = QPushButton("Kan Şekeri Ekle")
        self.btn_kan_sekeri_ekle.clicked.connect(self.kan_sekeri_ekle_ekranini_ac)
        self.layout.addWidget(self.btn_kan_sekeri_ekle)

        # Hastaları veritabanından çekme
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

            # Listeyi temizle
            self.hasta_listesi.clear()

            # Hastaları listeye ekle
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

            # Verileri ekrana yazdır
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
        """
        Hasta ekleme ekranını açar.
        """
        self.hasta_ekle_ekrani = HastaEklemeEkrani(self.doktor_id)
        self.hasta_ekle_ekrani.show()

    def kan_sekeri_ekle_ekranini_ac(self):
        """
        Kan şekeri ekleme ekranını açar.
        """
        # Listeden bir hasta seçilmemişse uyarı ver
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Hata", "Lütfen bir hasta seçiniz!")
            return

        # Seçilen hastanın ID'sini al
        hasta_id_str = self.hasta_listesi.currentItem().text().split(" - ")[0]
        hasta_id = int(hasta_id_str)

        # Kan şekeri ekleme ekranını aç
        self.kan_sekeri_ekle_ekrani = KanSekeriEklemeEkrani(hasta_id=hasta_id)
        self.kan_sekeri_ekle_ekrani.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    doktor_ekran = DoktorAnaEkran(doktor_id=1)  # Örnek doktor_id ile başlatıyoruz
    doktor_ekran.show()
    sys.exit(app.exec())
