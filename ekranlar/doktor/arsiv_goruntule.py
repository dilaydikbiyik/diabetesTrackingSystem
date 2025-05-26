from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QTabWidget, QLabel, QFrame,
                             QHeaderView, QScrollArea, QGroupBox,QTextEdit, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from veritabani import baglanti_kur
from ekranlar.moduller.oneri_motoru import oneri_getir

class ArsivEkrani(QWidget):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("Hasta Arşiv Verileri - Tıbbi Takip Sistemi")
        self.setGeometry(200, 100, 1200, 800)
        self.hasta_id = hasta_id

        # Ana stil ayarları
        self.setStyleSheet(self.get_main_stylesheet())

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Başlık bölümü
        self.create_header(main_layout)

        # Tab widget oluştur
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(self.get_tab_stylesheet())
        main_layout.addWidget(self.tab_widget)

        self.setLayout(main_layout)

        # Tabloları oluştur
        self.diyet_tablosu()
        self.egzersiz_tablosu()
        self.oneri_tablosu()
        self.kan_sekeri_tablosu()
        self.uyari_tablosu()

    def create_header(self, layout):
        """Başlık bölümünü oluşturur"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2E86AB, stop:1 #A23B72);
                border-radius: 10px;
                padding: 15px;
            }
        """)

        header_layout = QHBoxLayout()

        title_label = QLabel("📋 Hasta Arşiv Verileri")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)

        patient_info = QLabel(f"Hasta ID: {self.hasta_id}")
        patient_info.setStyleSheet("""
            QLabel {
                color: #E8F4FD;
                font-size: 14px;
                background: transparent;
            }
        """)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(patient_info)

        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)

    def get_main_stylesheet(self):
        """Ana pencere için stil"""
        return """
            QWidget {
                background-color: #F8FBFF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """

    def get_tab_stylesheet(self):
        """Tab widget için stil"""
        return """
            QTabWidget::pane {
                border: 2px solid #D1E7DD;
                border-radius: 8px;
                background-color: white;
                padding: 5px;
            }

            QTabWidget::tab-bar {
                alignment: left;
            }

            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E8F4FD, stop:1 #D1E7DD);
                border: 2px solid #B8D4E3;
                border-bottom: none;
                border-radius: 8px 8px 0px 0px;
                padding: 12px 20px;
                margin-right: 2px;
                font-weight: bold;
                color: #2E86AB;
                min-width: 120px;
            }

            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2E86AB, stop:1 #1B5E85);
                color: white;
                border-color: #1B5E85;
            }

            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #A8D0E6, stop:1 #7FB8D6);
                color: #1B5E85;
            }
        """

    def get_table_stylesheet(self):
        """Tablo için stil"""
        return """
            QTableWidget {
                gridline-color: #D1E7DD;
                background-color: white;
                alternate-background-color: #F8FBFF;
                selection-background-color: #A8D0E6;
                selection-color: #1B5E85;
                border: 1px solid #D1E7DD;
                border-radius: 6px;
                font-size: 11px;
            }

            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E8F4FD;
            }

            QTableWidget::item:selected {
                background-color: #A8D0E6;
                color: #1B5E85;
            }

            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2E86AB, stop:1 #1B5E85);
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }

            QHeaderView::section:first {
                border-top-left-radius: 6px;
            }

            QHeaderView::section:last {
                border-top-right-radius: 6px;
            }
        """

    def create_styled_table(self, row_count, column_count, headers):
        """Stilize edilmiş tablo oluşturur"""
        tablo = QTableWidget()
        tablo.setRowCount(row_count)
        tablo.setColumnCount(column_count)
        tablo.setHorizontalHeaderLabels(headers)
        tablo.setStyleSheet(self.get_table_stylesheet())

        # Tablo özellikleri
        tablo.setAlternatingRowColors(True)
        tablo.setSelectionBehavior(QTableWidget.SelectRows)
        tablo.verticalHeader().setVisible(False)

        # Sütun genişliklerini ayarla
        header = tablo.horizontalHeader()
        for i in range(column_count):
            if i == 0:  # Tarih sütunu
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        return tablo

    def add_summary_widget(self, layout, title, stats):
        """Özet bilgi widget'ı ekler"""
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E8F4FD, stop:1 #D1E7DD);
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }
        """)

        summary_layout = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2E86AB;
                background: transparent;
                font-size: 12px;
            }
        """)

        stats_label = QLabel(stats)
        stats_label.setStyleSheet("""
            QLabel {
                color: #1B5E85;
                background: transparent;
                font-size: 11px;
            }
        """)

        summary_layout.addWidget(title_label)
        summary_layout.addStretch()
        summary_layout.addWidget(stats_label)

        summary_frame.setLayout(summary_layout)
        layout.addWidget(summary_frame)

    def diyet_tablosu(self):
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

        # Ana widget
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Özet bilgiler
        cursor.execute("""
            SELECT COUNT(*), SUM(CASE WHEN durum = 'uygulandı' THEN 1 ELSE 0 END)
            FROM diyetler WHERE hasta_id = %s
        """, (self.hasta_id,))
        toplam, uygulanan = cursor.fetchone()
        oran = (uygulanan / toplam) * 100 if toplam > 0 else 0

        self.add_summary_widget(layout, "📊 Diyet İstatistikleri",
                                f"Toplam: {toplam} | Uygulanan: {uygulanan} | Başarı: %{oran:.1f}")

        # Tablo
        tablo = self.create_styled_table(len(veriler), 3, ["📅 Tarih", "🥗 Diyet Türü", "✅ Durum"])

        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                item = QTableWidgetItem(str(veri))
                if j == 2:  # Durum sütunu
                    if str(veri).lower() == 'uygulandı':
                        item.setBackground(QColor("#D4EDDA"))
                    else:
                        item.setBackground(QColor("#F8D7DA"))
                tablo.setItem(i, j, item)

        layout.addWidget(tablo)
        main_widget.setLayout(layout)

        self.tab_widget.addTab(main_widget, f"🥗 Diyetler (%{oran:.1f})")
        cursor.close()
        conn.close()

    def egzersiz_tablosu(self):
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

        # Ana widget
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Özet bilgiler
        cursor.execute("""
            SELECT COUNT(*), SUM(CASE WHEN durum_id = 1 THEN 1 ELSE 0 END)
            FROM egzersizler WHERE hasta_id = %s
        """, (self.hasta_id,))
        toplam, yapilan = cursor.fetchone()
        oran = (yapilan / toplam) * 100 if toplam > 0 else 0

        self.add_summary_widget(layout, "💪 Egzersiz İstatistikleri",
                                f"Toplam: {toplam} | Yapılan: {yapilan} | Başarı: %{oran:.1f}")

        # Tablo
        tablo = self.create_styled_table(len(veriler), 3, ["📅 Tarih", "🏃 Egzersiz Türü", "✅ Durum"])

        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                item = QTableWidgetItem(str(veri))
                if j == 2:  # Durum sütunu
                    if 'yapıldı' in str(veri).lower():
                        item.setBackground(QColor("#D4EDDA"))
                    else:
                        item.setBackground(QColor("#F8D7DA"))
                tablo.setItem(i, j, item)

        layout.addWidget(tablo)
        main_widget.setLayout(layout)

        self.tab_widget.addTab(main_widget, f"🏃 Egzersizler (%{oran:.1f})")
        cursor.close()
        conn.close()

    def oneri_tablosu(self):
        conn = baglanti_kur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tarih, baslik, aciklama
            FROM notlar_ve_oneriler
            WHERE hasta_id = %s
            ORDER BY tarih DESC
        """, (self.hasta_id,))
        veriler = cursor.fetchall()

        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)

        self.add_summary_widget(layout, "📝 Not ve Öneri Özeti",
                                f"Toplam Kayıt: {len(veriler)}")

        # Modern kartlar şeklinde önerileri göster
        for tarih, baslik, aciklama in veriler:
            kart = QFrame()
            kart.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border: 1px solid #D1E7DD;
                    border-radius: 10px;
                    padding: 15px;
                }
                QLabel {
                    font-size: 12px;
                    color: #333333;
                }
            """)
            kart_layout = QVBoxLayout(kart)

            baslik_label = QLabel(f"🗓️ {tarih.strftime('%d.%m.%Y %H:%M:%S')} - <b>{baslik}</b>")
            baslik_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #2E86AB;")
            baslik_label.setTextFormat(Qt.RichText)

            aciklama_text = QTextEdit(aciklama)
            aciklama_text.setReadOnly(True)
            aciklama_text.setFrameStyle(QFrame.NoFrame)
            aciklama_text.setStyleSheet("""
                QTextEdit {
                    background: #F8FBFF;
                    border: none;
                    padding: 8px;
                    font-size: 12px;
                    color: #2C3E50;
                }
            """)
            aciklama_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            aciklama_text.setMinimumHeight(100)

            kart_layout.addWidget(baslik_label)
            kart_layout.addWidget(aciklama_text)

            layout.addWidget(kart)

        layout.addStretch()
        main_widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(main_widget)

        self.tab_widget.addTab(scroll, "📝 Öneriler")
        cursor.close()
        conn.close()

    def kan_sekeri_tablosu(self):
        conn = baglanti_kur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tarih_zaman, kan_sekeri
            FROM kan_sekeri
            WHERE hasta_id = %s
            ORDER BY tarih_zaman DESC
        """, (self.hasta_id,))
        veriler = cursor.fetchall()

        # Ana widget
        main_widget = QWidget()
        layout = QVBoxLayout()

        # İstatistikler
        if veriler:
            kan_sekeri_degerleri = [float(v[1]) for v in veriler if v[1] is not None]
            if kan_sekeri_degerleri:
                ortalama = sum(kan_sekeri_degerleri) / len(kan_sekeri_degerleri)
                min_deger = min(kan_sekeri_degerleri)
                max_deger = max(kan_sekeri_degerleri)

                self.add_summary_widget(layout, "🩸 Kan Şekeri İstatistikleri",
                                        f"Ort: {ortalama:.1f} | Min: {min_deger:.1f} | Max: {max_deger:.1f} mg/dL")

        # Tablo
        tablo = self.create_styled_table(len(veriler), 2, ["📅 Tarih/Saat", "🩸 Kan Şekeri (mg/dL)"])

        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                item = QTableWidgetItem(str(veri))
                if j == 1:  # Kan şekeri değeri
                    try:
                        deger = float(veri)
                        if deger < 70:  # Düşük
                            item.setBackground(QColor("#F8D7DA"))
                        elif deger > 180:  # Yüksek
                            item.setBackground(QColor("#FFF3CD"))
                        else:  # Normal
                            item.setBackground(QColor("#D4EDDA"))
                    except:
                        pass
                tablo.setItem(i, j, item)

        layout.addWidget(tablo)
        main_widget.setLayout(layout)

        self.tab_widget.addTab(main_widget, "🩸 Kan Şekeri")
        cursor.close()
        conn.close()

    def uyari_tablosu(self):
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

        # Ana widget
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Özet bilgiler
        self.add_summary_widget(layout, "⚠️ Uyarı Özeti",
                                f"Toplam Uyarı: {len(veriler)}")

        # Tablo
        tablo = self.create_styled_table(len(veriler), 3, ["📅 Tarih", "⚠️ Uyarı Tipi", "💬 Mesaj"])

        for i, satir in enumerate(veriler):
            for j, veri in enumerate(satir):
                item = QTableWidgetItem(str(veri))
                if j == 1:  # Uyarı tipi
                    tip = str(veri).lower()
                    if 'kritik' in tip or 'acil' in tip:
                        item.setBackground(QColor("#F8D7DA"))
                    elif 'uyarı' in tip:
                        item.setBackground(QColor("#FFF3CD"))
                    else:
                        item.setBackground(QColor("#D1ECF1"))
                tablo.setItem(i, j, item)

        layout.addWidget(tablo)
        main_widget.setLayout(layout)

        self.tab_widget.addTab(main_widget, "⚠️ Uyarılar")
        cursor.close()
        conn.close()