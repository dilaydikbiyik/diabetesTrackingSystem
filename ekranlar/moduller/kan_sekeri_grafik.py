from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from veritabani import baglanti_kur
from datetime import datetime, timedelta

class KanSekeriGrafik(QWidget):
    def __init__(self, hasta_id):
        super().__init__()
        self.hasta_id = hasta_id
        self.setWindowTitle("Kan Şekeri Değişimi ve Aktivite Takibi")
        self.setGeometry(400, 200, 800, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.verileri_yukle_ve_ciz()

    def verileri_yukle_ve_ciz(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT tarih_zaman, kan_sekeri 
                FROM kan_sekeri 
                WHERE hasta_id = %s
                ORDER BY tarih_zaman ASC
            """, (self.hasta_id,))
            seker_verileri = cursor.fetchall()

            cursor.execute("""
                SELECT tarih_zaman::date 
                FROM diyetler 
                WHERE hasta_id = %s AND durum = 'uygulandı'
            """, (self.hasta_id,))
            diyet_tarihleri = [row[0] for row in cursor.fetchall()]

            cursor.execute("""
                SELECT e.tarih_zaman::date
                FROM egzersizler e
                JOIN egzersiz_durumlari d ON e.durum_id = d.id
                WHERE e.hasta_id = %s AND d.durum_adi = 'yapıldı'
            """, (self.hasta_id,))
            egzersiz_tarihleri = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            if not seker_verileri:
                QMessageBox.information(self, "Bilgi", "Bu hastaya ait kan şekeri verisi bulunmamaktadır.")
                return

            ax = self.figure.add_subplot(111)
            ax.clear()

            tarih_saatler = [row[0] for row in seker_verileri]
            sekerler = [row[1] for row in seker_verileri]
            ax.plot(tarih_saatler, sekerler, marker='o', linestyle='-', color='blue', label='Kan Şekeri')

            for tarih in diyet_tarihleri:
                diyet_zaman = datetime.combine(tarih, datetime.min.time()) + timedelta(hours=12)
                ax.axvline(diyet_zaman, color='green', linestyle='--', alpha=0.5, label='Diyet Uygulandı')

            for tarih in egzersiz_tarihleri:
                egzersiz_zaman = datetime.combine(tarih, datetime.min.time()) + timedelta(hours=12)
                ax.axvline(egzersiz_zaman, color='red', linestyle='--', alpha=0.5, label='Egzersiz Yapıldı')

            ax.set_title("Kan Şekeri Zaman Serisi")
            ax.set_xlabel("Tarih")
            ax.set_ylabel("Kan Şekeri (mg/dL)")
            ax.grid(True)

            handles, labels = ax.get_legend_handles_labels()
            unique = dict(zip(labels, handles))
            ax.legend(unique.values(), unique.keys())

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri alınamadı:\n{e}")

