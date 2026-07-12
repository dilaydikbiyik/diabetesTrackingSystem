from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from database import connect
from datetime import datetime, timedelta, date


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

    def _parse_dt(self, s):
        """Parse SQLite TEXT datetime string into datetime object."""
        if isinstance(s, datetime):
            return s
        if isinstance(s, date):
            return datetime(s.year, s.month, s.day)
        try:
            return datetime.fromisoformat(str(s))
        except Exception:
            return None

    def verileri_yukle_ve_ciz(self):
        try:
            conn = connect()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT tarih_zaman, kan_sekeri 
                FROM kan_sekeri 
                WHERE hasta_id = ?
                ORDER BY tarih_zaman ASC
            """, (self.hasta_id,))
            seker_verileri = cursor.fetchall()

            cursor.execute("""
                SELECT date(tarih_zaman) 
                FROM diyetler 
                WHERE hasta_id = ? AND durum = 'uygulandı'
            """, (self.hasta_id,))
            diyet_tarihleri = [row[0] for row in cursor.fetchall()]

            cursor.execute("""
                SELECT date(e.tarih_zaman)
                FROM egzersizler e
                JOIN egzersiz_durumlari d ON e.durum_id = d.id
                WHERE e.hasta_id = ? AND d.durum_adi = 'yapıldı'
            """, (self.hasta_id,))
            egzersiz_tarihleri = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            if not seker_verileri:
                QMessageBox.information(self, "Bilgi", "Bu hastaya ait kan şekeri verisi bulunmamaktadır.")
                return

            ax = self.figure.add_subplot(111)
            ax.clear()

            tarih_saatler = [self._parse_dt(row[0]) for row in seker_verileri]
            tarih_saatler = [t for t in tarih_saatler if t is not None]
            sekerler = [row[1] for row in seker_verileri]
            ax.plot(tarih_saatler, sekerler, marker='o', linestyle='-', color='blue', label='Kan Şekeri')

            for tarih_str in diyet_tarihleri:
                try:
                    tarih = date.fromisoformat(str(tarih_str))
                    diyet_zaman = datetime.combine(tarih, datetime.min.time()) + timedelta(hours=12)
                    ax.axvline(diyet_zaman, color='green', linestyle='--', alpha=0.5, label='Diyet Uygulandı')
                except Exception:
                    pass

            for tarih_str in egzersiz_tarihleri:
                try:
                    tarih = date.fromisoformat(str(tarih_str))
                    egzersiz_zaman = datetime.combine(tarih, datetime.min.time()) + timedelta(hours=12)
                    ax.axvline(egzersiz_zaman, color='red', linestyle='--', alpha=0.5, label='Egzersiz Yapıldı')
                except Exception:
                    pass

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
