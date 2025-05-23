from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFrame, QSplitter, QCheckBox)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt
from veritabani import baglanti_kur
import datetime


class HastalikTeshisiEkrani(QWidget):
    def __init__(self, hasta_id=None, parent=None):
        super().__init__(parent)
        self.hasta_id = hasta_id
        self.parent = parent
        self.checkboxlar = []
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Hastalık Teşhisi")
        self.setMinimumSize(800, 600)

        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        title_label = QLabel("Hastalık Teşhisi ve Analizi")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2B579A;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        logo_label = QLabel()
        logo_pixmap = QPixmap("saglik_logo.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(40, 40, Qt.KeepAspectRatio))
            header_layout.addWidget(logo_label)

        main_layout.addLayout(header_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        self.hasta_bilgi_label = QLabel("Hasta: Yükleniyor...")
        self.hasta_bilgi_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(self.hasta_bilgi_label)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        belirtiler_label = QLabel("Belirtiler")
        belirtiler_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(belirtiler_label)

        self.belirtiler_table = QTableWidget()
        self.belirtiler_table.setColumnCount(2)
        self.belirtiler_table.setHorizontalHeaderLabels(["Belirti", "Seç"])
        self.belirtiler_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.belirtiler_table)

        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        teshis_frame = QFrame()
        teshis_frame.setFrameShape(QFrame.StyledPanel)
        teshis_frame.setStyleSheet("background-color: #F0F8FF; border-radius: 5px;")
        teshis_layout = QVBoxLayout(teshis_frame)

        teshis_baslik = QLabel("Teşhis Analizi")
        teshis_baslik.setFont(QFont("Arial", 12, QFont.Bold))
        teshis_layout.addWidget(teshis_baslik)

        self.teshis_label = QLabel("Teşhis analizi yapılıyor...")
        self.teshis_label.setFont(QFont("Arial", 11))
        teshis_layout.addWidget(self.teshis_label)

        self.oneri_label = QLabel("")
        self.oneri_label.setFont(QFont("Arial", 11))
        self.oneri_label.setWordWrap(True)
        teshis_layout.addWidget(self.oneri_label)

        right_layout.addWidget(teshis_frame)

        etik_label = QLabel("⚠️ Bu teşhis sistem önerisidir. Lütfen hasta ile paylaşmadan önce değerlendirme yapınız.")
        etik_label.setFont(QFont("Arial", 9))
        etik_label.setStyleSheet("color: #FF7F50;")
        right_layout.addWidget(etik_label)

        splitter.addWidget(right_widget)
        splitter.setSizes([400, 400])

        main_layout.addWidget(splitter)

        button_layout = QHBoxLayout()
        self.yenile_btn = QPushButton("Verileri Yenile")
        self.yenile_btn.clicked.connect(self.verileri_yukle)
        button_layout.addWidget(self.yenile_btn)

        self.kaydet_btn = QPushButton("Seçimleri Kaydet")
        self.kaydet_btn.clicked.connect(self.belirtileri_kaydet)
        button_layout.addWidget(self.kaydet_btn)

        self.kapat_btn = QPushButton("Kapat")
        self.kapat_btn.clicked.connect(self.close)
        button_layout.addWidget(self.kapat_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        if self.hasta_id:
            self.verileri_yukle()

    def verileri_yukle(self):
        bilgiler = self.hasta_bilgilerini_getir()
        if bilgiler:
            self.hasta_bilgi_label.setText(f"Hasta: {bilgiler['ad']} {bilgiler['soyad']} | TC: {bilgiler['tc_no']}")

        belirtiler = self.belirtileri_getir()
        self.belirtiler_table.setRowCount(len(belirtiler))
        self.checkboxlar = []
        for i, belirti in enumerate(belirtiler):
            self.belirtiler_table.setItem(i, 0, QTableWidgetItem(belirti['ad']))
            checkbox = QCheckBox()
            checkbox.setChecked(belirti['durum'])
            self.belirtiler_table.setCellWidget(i, 1, checkbox)
            self.checkboxlar.append((belirti['ad'], checkbox))

        self.teshisi_yap([{'ad': ad, 'durum': cb.isChecked()} for ad, cb in self.checkboxlar])

    def belirtileri_kaydet(self):
        try:
            conn = baglanti_kur()
            cur = conn.cursor()
            cur.execute("DELETE FROM belirtiler WHERE hasta_id = %s", (self.hasta_id,))
            for ad, cb in self.checkboxlar:
                if cb.isChecked():
                    cur.execute("""
                        INSERT INTO belirtiler (hasta_id, belirti_id)
                        SELECT %s, id FROM belirti_tanimlari WHERE ad = %s
                    """, (self.hasta_id, ad))
            conn.commit()
            cur.close()
            conn.close()
            QMessageBox.information(self, "Başarılı", "Seçilen belirtiler kaydedildi.")
            self.verileri_yukle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kaydetme sırasında hata oluştu:\n{e}")

    def hasta_bilgilerini_getir(self):
        try:
            conn = baglanti_kur()
            if conn is None:
                return None
            cur = conn.cursor()
            cur.execute("""
                        SELECT ad, soyad, tc
                        FROM hastalar
                        WHERE id = %s
                        """, (self.hasta_id,))
            row = cur.fetchone()
            conn.close()
            if row:
                return {"ad": row[0], "soyad": row[1], "tc_no": row[2]}
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hasta bilgisi alınamadı:\n{str(e)}")
        return None

    def belirtileri_getir(self):
        try:
            conn = baglanti_kur()
            if conn is None:
                return []

            cur = conn.cursor()

            cur.execute("SELECT id, ad FROM belirti_tanimlari ORDER BY id")
            tum_belirtiler = cur.fetchall()

            cur.execute("""
                SELECT belirti_id FROM belirtiler WHERE hasta_id = %s
            """, (self.hasta_id,))
            aktif_belirti_idler = {row[0] for row in cur.fetchall()}
            conn.close()

            sonuc = []
            for belirti_id, ad in tum_belirtiler:
                sonuc.append({
                    "id": belirti_id,
                    "ad": ad,
                    "durum": belirti_id in aktif_belirti_idler
                })
            return sonuc

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Belirti verileri alınamadı:\n{str(e)}")
            return []

    def teshisi_yap(self, belirtiler):
        aktif = set([b['ad'] for b in belirtiler if b['durum']])

        kurallar = {
            "Hipoglisemi": {
                "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)",
                "Polifaji (Aşırı açlık hissi)",
                "Yorgunluk"
            },
            "Normal Alt Düzey": {
                "Yorgunluk",
                "Kilo kaybı"
            },
            "Normal Üst Düzey": {
                "Bulanık görme",
                "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)"
            },
            "Hiperglisemi": {
                "Yaraların yavaş iyileşmesi",
                "Polifaji (Aşırı açlık hissi)",
                "Polidipsi (Aşırı susama hissi)"
            },
        }

        for ad, gerek in kurallar.items():
            if gerek.issubset(aktif):
                self.teshis_label.setText(f"Tespit edilen durum: {ad}")
                return

        self.teshis_label.setText("Tüm belirtiler sağlanmadığı için teşhis yapılamadı.")
