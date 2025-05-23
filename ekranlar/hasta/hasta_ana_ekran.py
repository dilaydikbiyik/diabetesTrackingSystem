from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QTextEdit, QHBoxLayout, \
    QFrame, QScrollArea, QGridLayout, QSizePolicy, QLineEdit
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from datetime import datetime
from veritabani import baglanti_kur
from PyQt5.QtWidgets import QPushButton
from ekranlar.hasta.kan_sekeri_giris import KanSekeriGirisPenceresi
from ekranlar.hasta.egzersiz_giris import EgzersizGirisPenceresi
from ekranlar.hasta.diyet_giris import DiyetGirisPenceresi
from PyQt5.QtWidgets import QInputDialog, QMessageBox
import hashlib

class HastaAnaEkrani(QWidget):
    def __init__(self, ad, soyad, tc):
        super().__init__()
        self.bilgi_yuklendi = False
        self.setWindowTitle("Diabetes Care - Hasta Paneli")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(200, 100, 1200, 800)

        # Modern stil ayarları
        self.setStyleSheet(self.get_modern_stylesheet())

        self.ad = ad
        self.soyad = soyad
        self.tc = tc

        self.conn = baglanti_kur()
        self.cursor = self.conn.cursor()

        # Ana layout için scroll area
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.layout = QVBoxLayout()

        self.init_ui()

        self.scroll_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def get_modern_stylesheet(self):
        return """
            QWidget {
                background-color: #f8fafc;
                color: #1e293b;
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            QScrollArea {
                border: none;
                background-color: #f8fafc;
            }

            QFrame.header-frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1e40af, stop:1 #3b82f6);
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }

            QFrame.content-card {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
                margin: 8px;
            }

            QFrame.stat-card {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ffffff, stop:1 #f1f5f9);
                border: 2px solid #e0e7ff;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }

            QFrame.warning-card {
                background-color: #fef3c7;
                border: 2px solid #f59e0b;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }

            QFrame.success-card {
                background-color: #dcfce7;
                border: 2px solid #16a34a;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }

            QLabel.header-title {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin: 0px;
            }

            QLabel.header-subtitle {
                color: #bfdbfe;
                font-size: 20px;
                margin: 0px;
            }

            QLabel.section-title {
                color: #1e40af;
                font-size: 20px;
                font-weight: bold;
                margin: 10px 0px 5px 0px;
                padding: 5px;
            }

            QLabel.stat-value {
                color: #1e40af;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel.stat-label {
                color: #64748b;
                font-size: 14px;
            }

            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3b82f6, stop:1 #1d4ed8);
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 20px;
                margin: 5px;
                min-height: 40px;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #60a5fa, stop:1 #2563eb);
            }

            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1d4ed8, stop:1 #1e3a8a);
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                selection-background-color: #dbeafe;
                gridline-color: #f1f5f9;
            }

            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }

            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f8fafc, stop:1 #e2e8f0);
                color: #374151;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #3b82f6;
            }

            QTextEdit {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                background-color: white;
            }
            QFrame.success-card QLabel, QFrame.warning-card QLabel {
                font-size: 16px;
            }
        """

    def get_hasta_bilgileri(self):
        self.cursor.execute("""
            SELECT id, ad, soyad, email, profil_resmi
            FROM hastalar
            WHERE tc = %s
        """, (self.tc,))
        return self.cursor.fetchone()

    def create_header_section(self, ad, soyad, email, profil_resmi):
        """Modern header bölümü oluştur"""
        header_frame = QFrame()
        header_frame.setObjectName("header-frame")
        header_frame.setFixedHeight(120)

        header_layout = QHBoxLayout()

        # Profil resmi
        profile_container = QFrame()
        profile_container.setFixedSize(80, 80)
        profile_container.setStyleSheet("""
            border: 3px solid white;
            border-radius: 40px;
            background-color: white;
        """)

        self.lbl_resim = QLabel()
        self.lbl_resim.setFixedSize(74, 74)
        self.lbl_resim.setAlignment(Qt.AlignCenter)

        if profil_resmi:
            pixmap = QPixmap()
            pixmap.loadFromData(profil_resmi)
            self.lbl_resim.setPixmap(pixmap.scaled(74, 74, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.lbl_resim.setText("👤")
            self.lbl_resim.setStyleSheet("font-size: 30px; color: #64748b;")

        profile_layout = QVBoxLayout()
        profile_layout.addWidget(self.lbl_resim)
        profile_container.setLayout(profile_layout)

        # Hasta bilgileri
        info_layout = QVBoxLayout()

        ad_label = QLabel(f"{ad} {soyad}")
        ad_label.setObjectName("header-title")

        email_label = QLabel(f"📧 {email}")
        email_label.setObjectName("header-subtitle")

        tarih_label = QLabel(f"📅 {datetime.now().strftime('%d %B %Y, %A')}")
        tarih_label.setObjectName("header-subtitle")

        info_layout.addWidget(ad_label)
        info_layout.addWidget(email_label)
        info_layout.addWidget(tarih_label)
        info_layout.addStretch()

        header_layout.addWidget(profile_container)
        header_layout.addSpacing(20)
        header_layout.addLayout(info_layout)
        header_layout.addStretch()

        # Şifre Yenile Butonu
        sifre_btn = QPushButton("🔒 Şifreyi Değiştir")
        sifre_btn.setFixedHeight(30)
        sifre_btn.setStyleSheet("font-size: 13px; padding: 4px 12px;")
        sifre_btn.clicked.connect(self.sifre_degistir)

        header_layout.addWidget(sifre_btn)

        header_frame.setLayout(header_layout)
        return header_frame

    def create_stats_cards(self, olcumler):
        """İstatistik kartları oluştur"""
        stats_frame = QFrame()
        stats_layout = QGridLayout()

        if olcumler:
            # Ortalama hesapla
            toplam = sum(seviye for _, seviye in olcumler)
            adet = len(olcumler)
            ortalama = toplam / adet

            # Son ölçüm
            son_olcum = olcumler[-1][1]

            # İnsülin dozu
            if ortalama < 70:
                doz = "Yok (Hipoglisemi)"
                doz_renk = "#dc2626"
            elif 70 <= ortalama <= 110:
                doz = "Yok (Normal)"
                doz_renk = "#16a34a"
            elif 111 <= ortalama <= 150:
                doz = "1 ml"
                doz_renk = "#ea580c"
            elif 151 <= ortalama <= 200:
                doz = "2 ml"
                doz_renk = "#dc2626"
            else:
                doz = "3 ml"
                doz_renk = "#dc2626"

            # Kartlar
            cards_data = [
                ("Son Ölçüm", f"{son_olcum} mg/dL", "🩸", "#3b82f6"),
                ("Ortalama", f"{ortalama:.1f} mg/dL", "📊", "#059669"),
                ("Ölçüm Sayısı", f"{adet}", "📈", "#7c3aed"),
                ("İnsülin Önerisi", doz, "💉", doz_renk)
            ]
        else:
            cards_data = [
                ("Son Ölçüm", "Veri Yok", "🩸", "#6b7280"),
                ("Ortalama", "Veri Yok", "📊", "#6b7280"),
                ("Ölçüm Sayısı", "0", "📈", "#6b7280"),
                ("İnsülin Önerisi", "Veri Yok", "💉", "#6b7280")
            ]

        for i, (title, value, icon, color) in enumerate(cards_data):
            card = self.create_stat_card(title, value, icon, color)
            stats_layout.addWidget(card, 0, i)

        stats_frame.setLayout(stats_layout)
        return stats_frame

    def create_stat_card(self, title, value, icon, color):
        """Tek istatistik kartı oluştur"""
        card = QFrame()
        card.setObjectName("stat-card")
        card.setFixedHeight(100)

        layout = QVBoxLayout()

        # Icon ve başlık
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 20px; color: {color};")

        title_label = QLabel(title)
        title_label.setObjectName("stat-label")

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Değer
        value_label = QLabel(value)
        value_label.setObjectName("stat-value")
        value_label.setStyleSheet(f"color: {color};")

        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        layout.addStretch()

        card.setLayout(layout)
        return card

    def init_ui(self):
        bilgiler = self.get_hasta_bilgileri()
        if not bilgiler:
            self.layout.addWidget(QLabel("Hasta bilgisi bulunamadı."))
            return

        self.hasta_id, ad, soyad, email, profil_resmi = bilgiler

        if not self.bilgi_yuklendi:
            # Header
            header = self.create_header_section(ad, soyad, email, profil_resmi)
            self.layout.addWidget(header)
            self.bilgi_yuklendi = True

        # Ölçümler
        olcumler = self.get_olcumler()

        # İstatistik kartları
        stats_cards = self.create_stats_cards(olcumler)
        self.layout.addWidget(stats_cards)

        if olcumler:
            # Grafik
            self.show_modern_grafik(olcumler)

            # Ölçüm tablosu
            self.show_modern_olcum_tablosu(olcumler)
        else:
            no_data_card = self.create_info_card("📊 Bugünkü Ölçümler",
                                                 "Bugün için henüz ölçüm verisi bulunmuyor.", "info")
            self.layout.addWidget(no_data_card)

        # Durum kartları
        self.show_durum_kartlari()

        # Uyarılar
        self.show_modern_uyarilar()

        # Günlük yüzdeler
        self.show_gunluk_yuzde_kartlari()

        # Aksiyon butonları
        self.show_action_buttons()

    def create_info_card(self, title, content, card_type="info"):
        """Bilgi kartı oluştur"""
        card = QFrame()
        if card_type == "warning":
            card.setObjectName("warning-card")
        elif card_type == "success":
            card.setObjectName("success-card")
        else:
            card.setObjectName("content-card")

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setObjectName("section-title")
        layout.addWidget(title_label)

        if isinstance(content, str):
            content_label = QLabel(content)
            content_label.setWordWrap(True)
            content_label.setStyleSheet("font-size: 16px; color: #1e293b;")
            layout.addWidget(content_label)
        else:
            layout.addWidget(content)

        card.setLayout(layout)
        return card

    def show_modern_grafik(self, olcumler):
        """Modern grafik göster"""
        # Matplotlib stilini ayarla
        plt.style.use('default')

        zamanlar = [ts for ts, _ in olcumler]
        degerler = [seviye for _, seviye in olcumler]

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('white')

        # Çizgi grafiği
        line = ax.plot(zamanlar, degerler, linewidth=3, color='#3b82f6',
                       marker='o', markersize=8, markerfacecolor='white',
                       markeredgecolor='#3b82f6', markeredgewidth=2)

        # Normal aralık
        # Kan şekeri seviyelerine göre arka plan renklendirmesi
        ax.axhspan(70, 110, alpha=0.2, color='#16a34a', label='Normal')
        ax.axhspan(110, 180, alpha=0.2, color='#facc15', label='Hafif Yüksek')
        ax.axhspan(180, 500, alpha=0.2, color='#f87171', label='Hiperglisemi')
        ax.axhspan(0, 70, alpha=0.2, color='#60a5fa', label='Hipoglisemi')

        ax.set_title("Kan Şekeri Trend Grafiği", fontsize=16, color='#1e40af',
                     fontweight='bold', pad=20)
        ax.set_xlabel("Zaman", fontsize=12, color='#374151')
        ax.set_ylabel("mg/dL", fontsize=12, color='#374151')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)

        # Eksen stilini ayarla
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')

        fig.autofmt_xdate()
        plt.tight_layout()

        canvas = FigureCanvas(fig)
        graph_card = self.create_info_card("", canvas)
        self.layout.addWidget(graph_card)

    def show_modern_olcum_tablosu(self, olcumler):
        """Modern ölçüm tablosu"""
        tablo = QTableWidget()
        tablo.setRowCount(len(olcumler))
        tablo.setColumnCount(3)
        tablo.setHorizontalHeaderLabels(["📅 Tarih", "🕐 Saat", "🩸 Kan Şekeri (mg/dL)"])

        # Tablo stilini ayarla
        tablo.setAlternatingRowColors(True)
        tablo.setSelectionBehavior(QTableWidget.SelectRows)
        tablo.verticalHeader().setVisible(False)
        tablo.horizontalHeader().setStretchLastSection(True)

        for i, (ts, seviye) in enumerate(olcumler):
            tarih = ts.strftime("%d.%m.%Y")
            saat = ts.strftime("%H:%M")

            tarih_item = QTableWidgetItem(tarih)
            saat_item = QTableWidgetItem(saat)
            seviye_item = QTableWidgetItem(str(seviye))

            # Seviye rengini ayarla
            if seviye < 70:
                seviye_item.setBackground(QColor("#fecaca"))  # Kırmızı
            elif 70 <= seviye <= 110:
                seviye_item.setBackground(QColor("#bbf7d0"))  # Yeşil
            else:
                seviye_item.setBackground(QColor("#fed7aa"))  # Turuncu

            tablo.setItem(i, 0, tarih_item)
            tablo.setItem(i, 1, saat_item)
            tablo.setItem(i, 2, seviye_item)

        tablo_card = self.create_info_card("📋 Detaylı Ölçüm Listesi", tablo)
        self.layout.addWidget(tablo_card)

    def show_durum_kartlari(self):
        """Egzersiz ve diyet durum kartları"""
        durum_frame = QFrame()
        durum_layout = QHBoxLayout()

        # Egzersiz durumu
        self.cursor.execute("""
            SELECT ed.durum_adi
            FROM egzersizler e
            JOIN egzersiz_durumlari ed ON e.durum_id = ed.id
            WHERE e.hasta_id = %s AND e.tarih_zaman::date = CURRENT_DATE
        """, (self.hasta_id,))
        egzersiz = self.cursor.fetchone()

        # Diyet durumu
        self.cursor.execute("""
            SELECT durum
            FROM diyetler
            WHERE hasta_id = %s AND tarih_zaman::date = CURRENT_DATE
            ORDER BY tarih_zaman DESC
            LIMIT 1
        """, (self.hasta_id,))
        diyet = self.cursor.fetchone()

        # Egzersiz kartı
        egzersiz_yapildi = egzersiz and egzersiz[0] == 'yapıldı'
        egzersiz_card = self.create_status_card("🏃‍♂️ Egzersiz", egzersiz_yapildi)

        # Diyet kartı
        diyet_uygulandi = diyet and diyet[0] == 'uygulandı'
        diyet_card = self.create_status_card("🍽️ Diyet", diyet_uygulandi)

        durum_layout.addWidget(egzersiz_card)
        durum_layout.addWidget(diyet_card)

        durum_frame.setLayout(durum_layout)
        self.layout.addWidget(durum_frame)

    def create_status_card(self, title, is_completed):
        """Durum kartı oluştur"""
        card = QFrame()
        if is_completed:
            card.setObjectName("success-card")
            status_icon = "✅"
            status_text = "Tamamlandı"
            status_color = "#16a34a"
        else:
            card.setObjectName("warning-card")
            status_icon = "❌"
            status_text = "Tamamlanmadı"
            status_color = "#dc2626"

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        status_layout = QHBoxLayout()
        icon_label = QLabel(status_icon)
        icon_label.setStyleSheet("font-size: 24px;")

        text_label = QLabel(status_text)
        text_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {status_color};")

        status_layout.addWidget(icon_label)
        status_layout.addWidget(text_label)
        status_layout.addStretch()

        layout.addWidget(title_label)
        layout.addLayout(status_layout)

        card.setLayout(layout)
        return card

    def show_modern_uyarilar(self):
        """Modern uyarılar bölümü"""
        self.cursor.execute("""
            SELECT mesaj FROM uyarilar
            WHERE hasta_id = %s AND zaman::date = CURRENT_DATE
        """, (self.hasta_id,))
        uyarilar = self.cursor.fetchall()

        if uyarilar:
            uyari_text = "⚠️ Bugünkü Önemli Uyarılar:\n\n"
            for i, (mesaj,) in enumerate(uyarilar, 1):
                uyari_text += f"{i}. {mesaj}\n"

            uyari_card = self.create_info_card("🚨 Uyarılar", uyari_text, "warning")
            self.layout.addWidget(uyari_card)
        else:
            success_text = "✅ Bugün için herhangi bir uyarı bulunmuyor.\nHer şey yolunda gözüküyor!"
            success_label = QLabel(success_text)
            success_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e3a8a;")
            success_label.setWordWrap(True)
            success_card = self.create_info_card("🎉 Durum İyi", success_text, "success")
            success_card.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e3a8a;")
            self.layout.addWidget(success_card)

    def show_action_buttons(self):
        """Aksiyon butonları"""
        button_frame = QFrame()
        button_layout = QHBoxLayout()

        # Kan şekeri butonu
        kan_btn = QPushButton("🩸 Kan Şekeri Girişi")
        kan_btn.clicked.connect(self.kan_sekeri_ekle)

        # Egzersiz butonu
        egzersiz_btn = QPushButton("🏃‍♂️ Egzersiz Girişi")
        egzersiz_btn.clicked.connect(self.egzersiz_ekle)

        # Diyet butonu
        diyet_btn = QPushButton("🍽️ Diyet Girişi")
        diyet_btn.clicked.connect(self.diyet_ekle)

        button_layout.addWidget(kan_btn)
        button_layout.addWidget(egzersiz_btn)
        button_layout.addWidget(diyet_btn)

        button_frame.setLayout(button_layout)
        self.layout.addWidget(button_frame)

    def show_gunluk_yuzde_kartlari(self):
        """Günlük yüzde kartları"""
        # Egzersiz yüzdesi
        self.cursor.execute("""
            SELECT ed.durum_adi
            FROM egzersizler e
            JOIN egzersiz_durumlari ed ON e.durum_id = ed.id
            WHERE e.hasta_id = %s AND e.tarih_zaman::date = CURRENT_DATE
        """, (self.hasta_id,))
        egzersizler = self.cursor.fetchall()
        toplam_e = len(egzersizler)
        yapilan_e = sum(1 for (durum,) in egzersizler if durum == "yapıldı")
        egzersiz_oran = (yapilan_e / toplam_e * 100) if toplam_e > 0 else 0

        # Diyet yüzdesi
        self.cursor.execute("""
            SELECT durum
            FROM diyetler
            WHERE hasta_id = %s AND tarih_zaman::date = CURRENT_DATE
        """, (self.hasta_id,))
        diyetler = self.cursor.fetchall()
        toplam_d = len(diyetler)
        uygulanan_d = sum(1 for (durum,) in diyetler if durum == "uygulandı")
        diyet_oran = (uygulanan_d / toplam_d * 100) if toplam_d > 0 else 0

        # Yüzde kartları
        yuzde_frame = QFrame()
        yuzde_layout = QHBoxLayout()

        egz_card = self.create_percentage_card("🏃‍♂️ Egzersiz Başarı", egzersiz_oran)
        diyet_card = self.create_percentage_card("🍽️ Diyet Başarı", diyet_oran)

        yuzde_layout.addWidget(egz_card)
        yuzde_layout.addWidget(diyet_card)

        yuzde_frame.setLayout(yuzde_layout)
        self.layout.addWidget(yuzde_frame)

    def create_percentage_card(self, title, percentage):
        """Yüzde kartı oluştur"""
        card = QFrame()
        card.setObjectName("stat-card")

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151;")

        percentage_label = QLabel(f"%{percentage:.0f}")

        if percentage >= 80:
            color = "#16a34a"
        elif percentage >= 50:
            color = "#ea580c"
        else:
            color = "#dc2626"

        percentage_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")

        layout.addWidget(title_label)
        layout.addWidget(percentage_label)
        layout.addStretch()

        card.setLayout(layout)
        return card

    def get_olcumler(self):
        self.cursor.execute("""
            SELECT tarih_zaman, kan_sekeri
            FROM kan_sekeri
            WHERE hasta_id = %s
              AND tarih_zaman >= CURRENT_DATE
              AND tarih_zaman < CURRENT_DATE + INTERVAL '1 day'
            ORDER BY tarih_zaman
        """, (self.hasta_id,))
        return self.cursor.fetchall()

    def kan_sekeri_ekle(self):
        pencere = KanSekeriGirisPenceresi(self.hasta_id, self.conn)
        pencere.exec_()
        self.refresh()

    def egzersiz_ekle(self):
        pencere = EgzersizGirisPenceresi(self.hasta_id, self.conn)
        pencere.exec_()
        self.refresh()

    def diyet_ekle(self):
        pencere = DiyetGirisPenceresi(self.hasta_id, self.conn)
        pencere.exec_()
        self.refresh()

    def closeEvent(self, event):
        if self.conn:
            self.cursor.close()
            self.conn.close()

    def refresh(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.bilgi_yuklendi = False
        self.init_ui()

    def sifre_degistir(self):
        yeni_sifre, ok = QInputDialog.getText(self, "Şifre Güncelle", "Yeni şifrenizi girin:", QLineEdit.Password)
        if ok and yeni_sifre:
            hashli = hashlib.sha256(yeni_sifre.encode()).digest()
            try:
                self.cursor.execute("UPDATE hastalar SET sifre = %s WHERE id = %s", (hashli, self.hasta_id))
                self.conn.commit()
                QMessageBox.information(self, "Başarılı", "Şifreniz başarıyla güncellendi.")
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Şifre güncellenemedi: {str(e)}")