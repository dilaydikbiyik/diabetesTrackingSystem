from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt5.QtGui import QFont, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from datetime import datetime
from veritabani import baglanti_kur  # ← veritabanı bağlantı fonksiyonun
import psycopg2

class HastaAnaEkrani(QWidget):
    def __init__(self, ad, soyad, tc):
        super().__init__()
        self.setWindowTitle("Hasta Ana Sayfası")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(300, 150, 800, 700)

        self.ad = ad
        self.soyad = soyad
        self.tc = tc

        self.conn = baglanti_kur()
        self.cursor = self.conn.cursor()

        self.hasta_id = self.get_hasta_id()
        self.layout = QVBoxLayout()

        self.init_ui()
        self.setLayout(self.layout)

    def get_hasta_id(self):
        self.cursor.execute("SELECT id FROM hastalar WHERE tc = %s", (self.tc,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def init_ui(self):
        if not self.hasta_id:
            self.layout.addWidget(QLabel("Hasta bilgisi bulunamadı."))
            return

        # Hoş geldin
        hosgeldin = QLabel(f"👋 Hoş geldiniz, {self.ad} {self.soyad}!")
        hosgeldin.setStyleSheet("color: green; font-weight: bold; font-size: 18px")
        self.layout.addWidget(hosgeldin)

        # Ölçüm verilerini al ve tablo oluştur
        olcumler = self.get_olcumler()
        if olcumler:
            self.show_olcum_tablosu(olcumler)
            self.goster_ortalama_ve_doz(olcumler)
            self.goster_grafik(olcumler)
        else:
            self.layout.addWidget(QLabel("Bugün için ölçüm verisi bulunamadı."))

        # Uyarılar
        self.goster_uyarilar()

        # Egzersiz ve diyet
        self.goster_egzersiz_ve_diyet()

    def get_olcumler(self):
        self.cursor.execute("""
                            SELECT tarih_zaman, kan_sekeri
                            FROM olcumler
                            WHERE hasta_id = %s
                              AND tarih_zaman >= CURRENT_DATE
                              AND tarih_zaman < CURRENT_DATE + INTERVAL '1 day'
                            ORDER BY tarih_zaman
                            """, (self.hasta_id,))
        return self.cursor.fetchall()

    def show_olcum_tablosu(self, olcumler):
        tablo = QTableWidget()
        tablo.setRowCount(len(olcumler))
        tablo.setColumnCount(3)
        tablo.setHorizontalHeaderLabels(["Tarih", "Saat", "Kan Şekeri (mg/dL)"])

        for i, (ts, seviye) in enumerate(olcumler):
            tarih = ts.strftime("%d.%m.%Y")
            saat = ts.strftime("%H:%M")
            tablo.setItem(i, 0, QTableWidgetItem(tarih))
            tablo.setItem(i, 1, QTableWidgetItem(saat))
            tablo.setItem(i, 2, QTableWidgetItem(str(seviye)))

        self.layout.addWidget(QLabel("📊 Bugünkü Ölçümler"))
        self.layout.addWidget(tablo)

    def goster_ortalama_ve_doz(self, olcumler):
        toplam = sum(seviye for _, seviye in olcumler)
        adet = len(olcumler)
        ortalama = toplam / adet

        if ortalama < 70:
            doz = "Yok (Hipoglisemi)"
        elif 70 <= ortalama <= 110:
            doz = "Yok (Normal)"
        elif 111 <= ortalama <= 150:
            doz = "1 ml"
        elif 151 <= ortalama <= 200:
            doz = "2 ml"
        else:
            doz = "3 ml"

        ortalama_label = QLabel(f"➗ Ortalama Kan Şekeri: {ortalama:.2f} mg/dL")
        doz_label = QLabel(f"💉 İnsülin Önerisi: {doz}")
        ortalama_label.setFont(QFont("Arial", 11))
        doz_label.setFont(QFont("Arial", 11))

        self.layout.addWidget(ortalama_label)
        self.layout.addWidget(doz_label)

    def goster_uyarilar(self):
        self.cursor.execute("""
            SELECT mesaj FROM uyarilar
            WHERE hasta_id = %s AND zaman::date = CURRENT_DATE
        """, (self.hasta_id,))
        uyarilar = self.cursor.fetchall()

        if uyarilar:
            uyarilar_text = QTextEdit()
            uyarilar_text.setReadOnly(True)
            uyarilar_text.setStyleSheet("background-color: #fff3cd; color: #856404;")
            uyarilar_text.append("⚠️ Bugünkü Uyarılar:")
            for (mesaj,) in uyarilar:
                uyarilar_text.append(f"- {mesaj}")
            self.layout.addWidget(uyarilar_text)
        else:
            self.layout.addWidget(QLabel("✅ Bugün için herhangi bir uyarı bulunamadı."))

    def goster_egzersiz_ve_diyet(self):
        self.cursor.execute("""
            SELECT durum FROM egzersizler
            WHERE hasta_id = %s AND tarih = CURRENT_DATE
        """, (self.hasta_id,))
        egzersiz = self.cursor.fetchone()

        self.cursor.execute("""
            SELECT durum FROM diyetler
            WHERE hasta_id = %s AND tarih = CURRENT_DATE
        """, (self.hasta_id,))
        diyet = self.cursor.fetchone()

        egzersiz_label = QLabel(f"🏃 Egzersiz Durumu: {'✅ Yapıldı' if egzersiz and egzersiz[0] == 'yapıldı' else '❌ Yapılmadı'}")
        diyet_label = QLabel(f"🍽️ Diyet Durumu: {'✅ Uygulandı' if diyet and diyet[0] == 'uygulandı' else '❌ Uygulanmadı'}")

        self.layout.addWidget(egzersiz_label)
        self.layout.addWidget(diyet_label)

    def goster_grafik(self, olcumler):
        zamanlar = [ts for ts, _ in olcumler]
        degerler = [seviye for _, seviye in olcumler]

        fig, ax = plt.subplots()
        ax.plot(zamanlar, degerler, marker="o", color="tab:blue")
        ax.set_title("Kan Şekeri Zaman Grafiği")
        ax.set_xlabel("Zaman")
        ax.set_ylabel("mg/dL")
        ax.grid(True)
        fig.autofmt_xdate()
        canvas = FigureCanvas(fig)
        self.layout.addWidget(canvas)

    def closeEvent(self, event):
        if self.conn:
            self.cursor.close()
            self.conn.close()
