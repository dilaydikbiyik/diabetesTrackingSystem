from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget
from veritabani import baglanti_kur

class ArsivEkrani(QWidget):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("Hasta Arşiv Verileri")
        self.setGeometry(400, 200, 900, 600)
        self.hasta_id = hasta_id

        self.tab_widget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.diyet_tablosu()
        self.egzersiz_tablosu()
        self.oneri_tablosu()
        self.kan_sekeri_tablosu()
        self.uyari_tablosu()

    def diyet_tablosu(self):
        tablo = QTableWidget()
        conn = baglanti_kur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tarih_zaman, ad, durum
            FROM diyetler d
            JOIN diyet_tanimlari dt ON d.diyet_id = dt.id
            WHERE hasta_id = %s
            ORDER BY tarih_zaman DESC
        """, (self.hasta_id,))
        veriler = cursor.fetchall()
        tablo.setRowCount(len(veriler))
        tablo.setColumnCount(3)
        tablo.setHorizontalHeaderLabels(["Tarih", "Diyet Türü", "Durum"])
        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                tablo.setItem(i, j, QTableWidgetItem(str(veri)))

        cursor.execute("""
            SELECT COUNT(*), SUM(CASE WHEN durum = 'uygulandı' THEN 1 ELSE 0 END)
            FROM diyetler WHERE hasta_id = %s
        """, (self.hasta_id,))
        toplam, uygulanan = cursor.fetchone()
        oran = (uygulanan / toplam) * 100 if toplam > 0 else 0
        self.tab_widget.addTab(tablo, f"Diyetler (%{oran:.1f} uygulandı)")

    def egzersiz_tablosu(self):
        tablo = QTableWidget()
        conn = baglanti_kur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tarih_zaman, et.tur_adi, ed.durum_adi
            FROM egzersizler e
            JOIN egzersiz_turleri et ON e.tur_id = et.id
            JOIN egzersiz_durumlari ed ON e.durum_id = ed.id
            WHERE hasta_id = %s
            ORDER BY tarih_zaman DESC
        """, (self.hasta_id,))
        veriler = cursor.fetchall()
        tablo.setRowCount(len(veriler))
        tablo.setColumnCount(3)
        tablo.setHorizontalHeaderLabels(["Tarih", "Egzersiz Türü", "Durum"])
        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                tablo.setItem(i, j, QTableWidgetItem(str(veri)))

        cursor.execute("""
            SELECT COUNT(*), SUM(CASE WHEN durum_id = 1 THEN 1 ELSE 0 END)
            FROM egzersizler WHERE hasta_id = %s
        """, (self.hasta_id,))  # "1" = "yapıldı"
        toplam, yapilan = cursor.fetchone()
        oran = (yapilan / toplam) * 100 if toplam > 0 else 0
        self.tab_widget.addTab(tablo, f"Egzersizler (%{oran:.1f} yapıldı)")

    def oneri_tablosu(self):
        tablo = QTableWidget()
        conn = baglanti_kur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tarih, baslik, aciklama
            FROM notlar_ve_oneriler
            WHERE hasta_id = %s
            ORDER BY tarih DESC
        """, (self.hasta_id,))
        veriler = cursor.fetchall()
        tablo.setRowCount(len(veriler))
        tablo.setColumnCount(3)
        tablo.setHorizontalHeaderLabels(["Tarih", "Başlık", "Açıklama"])
        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                tablo.setItem(i, j, QTableWidgetItem(str(veri)))
        self.tab_widget.addTab(tablo, "Öneriler / Notlar")

    def kan_sekeri_tablosu(self):
        tablo = QTableWidget()
        conn = baglanti_kur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tarih_zaman, kan_sekeri
            FROM kan_sekeri
            WHERE hasta_id = %s
            ORDER BY tarih_zaman DESC
        """, (self.hasta_id,))
        veriler = cursor.fetchall()
        tablo.setRowCount(len(veriler))
        tablo.setColumnCount(2)
        tablo.setHorizontalHeaderLabels(["Tarih/Saat", "Kan Şekeri (mg/dL)"])
        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                tablo.setItem(i, j, QTableWidgetItem(str(veri)))
        self.tab_widget.addTab(tablo, "Kan Şekeri")

    def uyari_tablosu(self):
        tablo = QTableWidget()
        conn = baglanti_kur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT zaman, ut.tip, mesaj
            FROM uyarilar u
            JOIN uyari_turleri ut ON u.tip_id = ut.id
            WHERE hasta_id = %s
            ORDER BY zaman DESC
        """, (self.hasta_id,))
        veriler = cursor.fetchall()
        tablo.setRowCount(len(veriler))
        tablo.setColumnCount(3)
        tablo.setHorizontalHeaderLabels(["Tarih", "Uyarı Tipi", "Mesaj"])
        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                tablo.setItem(i, j, QTableWidgetItem(str(veri)))
        self.tab_widget.addTab(tablo, "Uyarılar")
