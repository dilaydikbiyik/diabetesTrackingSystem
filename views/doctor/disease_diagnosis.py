from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QSplitter, QCheckBox,
    QGroupBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from database import connect
import datetime
from utils.recommendation_engine import oneri_getir


class HastalikTeshisiEkrani(QWidget):
    def __init__(self, hasta_id=None, parent=None):
        super().__init__(parent)
        self.hasta_id = hasta_id
        self.parent = parent
        self.checkboxlar = []
        self.setupUI()
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #2c3e50;
            }
            #titleLabel {
                color: #2980b9;
                font-size: 24px;
                font-weight: bold;
                padding: 10px 0px;
            }
            #patientInfoLabel {
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #3498db;
                font-size: 14px;
                font-weight: 500;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2c3e50;
                font-size: 16px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
                        QCheckBox {
                spacing: 8px;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 3px;
                border: 2px solid #bdc3c7;
            }
            QCheckBox::indicator:checked {
                background-color: #27ae60;
                border-color: #27ae60;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #2ecc71;
            }
            #diagnosisFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stops: 0 #ffffff, 1 #f8f9fa);
                border: 2px solid #e74c3c;
                border-radius: 12px;
                padding: 20px;
            }
            #diagnosisResult {
                color: #2c3e50;
                font-size: 16px;
                font-weight: 600;
                padding: 15px;
                background-color: #fff3cd;
                border-radius: 8px;
                border-left: 4px solid #ffc107;
            }
            #recommendationText {
                color: #495057;
                font-size: 14px;
                line-height: 1.6;
                margin-top: 15px;
                padding: 12px;
                background-color: #e8f5e8;
                border-radius: 6px;
            }
            #warningLabel {
                background-color: #fff3cd;
                color: #856404;
                padding: 12px;
                border-radius: 6px;
                border-left: 4px solid #ffc107;
                font-size: 12px;
                font-style: italic;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            #saveButton {
                background-color: #27ae60;
            }
            #saveButton:hover {
                background-color: #229954;
            }
            #refreshButton {
                background-color: #f39c12;
            }
            #refreshButton:hover {
                background-color: #e67e22;
            }
            #closeButton {
                background-color: #95a5a6;
            }
            #closeButton:hover {
                background-color: #7f8c8d;
            }
        """

    def setupUI(self):
        self.setWindowTitle("Hastalık Teşhisi ve Analiz Sistemi")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        header_layout = QHBoxLayout()
        title_label = QLabel("🏥 Hastalık Teşhisi ve Analiz Sistemi")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        logo_label = QLabel()
        logo_pixmap = QPixmap("saglik_logo.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            header_layout.addWidget(logo_label)

        main_layout.addLayout(header_layout)

        self.hasta_bilgi_label = QLabel("👤 Hasta Bilgileri Yükleniyor...")
        self.hasta_bilgi_label.setObjectName("patientInfoLabel")
        main_layout.addWidget(self.hasta_bilgi_label)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        belirtiler_group = QGroupBox("📋 Hastalık Belirtileri")
        belirtiler_layout = QVBoxLayout(belirtiler_group)

        self.belirtiler_table = QTableWidget()
        self.belirtiler_table.setColumnCount(2)
        self.belirtiler_table.setHorizontalHeaderLabels(["Belirti Açıklaması", "Seçim Durumu"])
        header = self.belirtiler_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.belirtiler_table.setColumnWidth(1, 120)
        self.belirtiler_table.setAlternatingRowColors(True)
        self.belirtiler_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.belirtiler_table.verticalHeader().setVisible(False)
        self.belirtiler_table.setMinimumHeight(400)

        belirtiler_layout.addWidget(self.belirtiler_table)
        left_layout.addWidget(belirtiler_group)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        teshis_group = QGroupBox("🔬 Teşhis Analizi")
        teshis_layout = QVBoxLayout(teshis_group)

        teshis_frame = QFrame()
        teshis_frame.setObjectName("diagnosisFrame")
        teshis_frame_layout = QVBoxLayout(teshis_frame)

        self.teshis_label = QLabel("⏳ Teşhis analizi yapılıyor...")
        self.teshis_label.setObjectName("diagnosisResult")
        self.teshis_label.setWordWrap(True)
        teshis_frame_layout.addWidget(self.teshis_label)

        self.oneri_label = QLabel("")
        self.oneri_label.setObjectName("recommendationText")
        self.oneri_label.setWordWrap(True)
        teshis_frame_layout.addWidget(self.oneri_label)

        teshis_layout.addWidget(teshis_frame)

        etik_label = QLabel(
            "⚠️ Bu teşhis sistem önerisidir. Lütfen hasta ile paylaşmadan önce titizlikle değerlendirme yapınız.")
        etik_label.setObjectName("warningLabel")
        etik_label.setWordWrap(True)
        teshis_layout.addWidget(etik_label)

        right_layout.addWidget(teshis_group)
        right_layout.addStretch()

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([800, 400])

        main_layout.addWidget(splitter)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.yenile_btn = QPushButton("🔄 Verileri Yenile")
        self.yenile_btn.setObjectName("refreshButton")
        self.yenile_btn.clicked.connect(self.verileri_yukle)
        button_layout.addWidget(self.yenile_btn)

        self.kaydet_btn = QPushButton("💾 Seçimleri Kaydet")
        self.kaydet_btn.setObjectName("saveButton")
        self.kaydet_btn.clicked.connect(self.belirtileri_kaydet)
        button_layout.addWidget(self.kaydet_btn)

        button_layout.addStretch()

        self.kapat_btn = QPushButton("❌ Kapat")
        self.kapat_btn.setObjectName("closeButton")
        self.kapat_btn.clicked.connect(self.close)
        button_layout.addWidget(self.kapat_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        if self.hasta_id:
            self.verileri_yukle()

    def verileri_yukle(self):
        try:
            bilgiler = self.hasta_bilgilerini_getir()
            if bilgiler:
                self.hasta_bilgi_label.setText(
                    f"👤 Hasta: {bilgiler['ad']} {bilgiler['soyad']} | "
                    f"TC Kimlik: {bilgiler['tc_no']} | "
                    f"📧 E-posta: {bilgiler.get('email', 'Belirtilmemiş')}"
                )

            belirtiler = self.belirtileri_getir()
            self.belirtiler_table.setRowCount(len(belirtiler))
            self.checkboxlar = []

            for i, belirti in enumerate(belirtiler):
                item = QTableWidgetItem(belirti['ad'])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                # Explicitly set colors — required on macOS where system theme overrides stylesheet
                from PyQt5.QtGui import QColor, QBrush
                item.setForeground(QBrush(QColor("#1a1a2e")))
                item.setBackground(QBrush(QColor("#ffffff")))
                self.belirtiler_table.setItem(i, 0, item)

                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)

                checkbox = QCheckBox()
                checkbox.setChecked(belirti['durum'])
                checkbox.stateChanged.connect(self.belirti_degisti)
                checkbox_layout.addWidget(checkbox)

                self.belirtiler_table.setCellWidget(i, 1, checkbox_widget)
                self.checkboxlar.append((belirti['ad'], checkbox))

            for i in range(len(belirtiler)):
                self.belirtiler_table.setRowHeight(i, 50)

            self.teshisi_yap([{'ad': ad, 'durum': cb.isChecked()} for ad, cb in self.checkboxlar])

        except Exception as e:
            QMessageBox.critical(self, "Veri Yükleme Hatası", f"Veriler yüklenirken hata oluştu:\n{str(e)}")

    def belirti_degisti(self):
        QTimer.singleShot(100, self.teshisi_guncelle)

    def teshisi_guncelle(self):
        belirtiler = [{'ad': ad, 'durum': cb.isChecked()} for ad, cb in self.checkboxlar]
        self.teshisi_yap(belirtiler)

    def belirtileri_kaydet(self):
        try:
            conn = connect()
            if conn is None:
                QMessageBox.critical(self, "Bağlantı Hatası", "Veritabanı bağlantısı kurulamadı.")
                return

            cur = conn.cursor()
            cur.execute("DELETE FROM belirtiler WHERE hasta_id = ?", (self.hasta_id,))
            kayit_sayisi = 0

            for ad, cb in self.checkboxlar:
                if cb.isChecked():
                    cur.execute("""
                        INSERT INTO belirtiler (hasta_id, belirti_id, tarih_zaman)
                        SELECT ?, id, CURRENT_TIMESTAMP
                        FROM belirti_tanimlari
                        WHERE ad = ?
                    """, (self.hasta_id, ad))
                    kayit_sayisi += 1

            conn.commit()
            cur.close()
            conn.close()

            QMessageBox.information(
                self, "✅ Başarılı",
                f"Seçilen {kayit_sayisi} belirti başarıyla kaydedildi.\n"
                f"Kayıt zamanı: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            )

            ortalama = self.ogun_bazli_kan_sekeri_ortalama(self.hasta_id)
            if ortalama:
                self.otomatik_teshis_gonder(ortalama)

            self.verileri_yukle()

        except Exception as e:
            QMessageBox.critical(self, "❌ Kaydetme Hatası", f"Belirtiler kaydedilirken hata oluştu:\n{str(e)}")

    def hasta_bilgilerini_getir(self):
        try:
            conn = connect()
            if conn is None:
                return None

            cur = conn.cursor()
            cur.execute("""
                SELECT ad, soyad, tc, email FROM hastalar WHERE id = ?
            """, (self.hasta_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                return {
                    "ad": row[0],
                    "soyad": row[1],
                    "tc_no": row[2],
                    "email": row[3] if len(row) > 3 else None
                }
        except Exception as e:
            QMessageBox.warning(self, "⚠️ Uyarı", f"Hasta bilgisi alınamadı:\n{str(e)}")
        return None

    def belirtileri_getir(self):
        try:
            conn = connect()
            if conn is None:
                return []

            cur = conn.cursor()

            cur.execute("SELECT id, ad FROM belirti_tanimlari ORDER BY ad")
            tum_belirtiler = cur.fetchall()

            cur.execute("""
                SELECT belirti_id FROM belirtiler WHERE hasta_id = ?
            """, (self.hasta_id,))
            aktif_belirti_idler = {row[0] for row in cur.fetchall()}

            cur.close()
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
            QMessageBox.critical(self, "❌ Veri Hatası", f"Belirti verileri alınamadı:\n{str(e)}")
            return []

    def ogun_bazli_kan_sekeri_ortalama(self, hasta_id):
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("""
                SELECT olcum_grubu, kan_sekeri
                FROM kan_sekeri
                WHERE hasta_id = ? AND date(tarih_zaman) = date('now')
            """, (hasta_id,))
            veriler = cur.fetchall()
            cur.close()
            conn.close()

            ogunler = ["sabah", "öğle", "ikindi", "akşam", "gece"]
            gruplar = {ogun: [] for ogun in ogunler}
            for grup, seviye in veriler:
                if grup in gruplar:
                    gruplar[grup].append(seviye)

            ortalamalar = {}
            biriken = []
            for ogun in ogunler:
                biriken.extend(gruplar[ogun])
                if biriken:
                    ort = sum(biriken) / len(biriken)
                    ortalamalar[ogun] = round(ort, 2)

            return ortalamalar
        except Exception as e:
            print("Ortalama hesaplama hatası:", e)
            return {}

    def teshisi_yap(self, belirtiler):
        aktif = set([b['ad'] for b in belirtiler if b['durum']])
        kurallar = {
            "🔴 Hipoglisemi (Düşük Kan Şekeri)": {
                "gerekli": {
                    "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)",
                    "Polifaji (Aşırı açlık hissi)",
                    "Yorgunluk"
                },
                "oneri": "Acil olarak kan şekeri seviyesi kontrol edilmeli. Hızla şeker alımı sağlanmalı. Doktor kontrolü gereklidir."
            },
            "🟡 Normal Alt Seviye": {
                "gerekli": {
                    "Yorgunluk",
                    "Kilo kaybı"
                },
                "oneri": "Düzenli beslenme programı uygulanmalı. Kan şekeri takibi yapılmalı."
            },
            "🟠 Normal Üst Seviye": {
                "gerekli": {
                    "Bulanık görme",
                    "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)"
                },
                "oneri": "Diyet kontrolü ve düzenli egzersiz önerilir. Kan şekeri seviyesi izlenmelidir."
            },
            "🔴 Hiperglisemi (Yüksek Kan Şekeri)": {
                "gerekli": {
                    "Yaraların yavaş iyileşmesi",
                    "Polifaji (Aşırı açlık hissi)",
                    "Polidipsi (Aşırı susama hissi)"
                },
                "oneri": "Acil tıbbi müdahale gereklidir. İnsülin tedavisi ve sıkı kan şekeri kontrolü şarttır."
            }
        }

        teshis_bulundu = False
        for teshis_adi, kural in kurallar.items():
            if kural["gerekli"].issubset(aktif):
                self.teshis_label.setText(f"📊 Tespit Edilen Durum:\n{teshis_adi}")
                self.oneri_label.setText(f"📝 Öneriler:\n{kural['oneri']}")
                teshis_bulundu = True
                break

        if not teshis_bulundu:
            if len(aktif) == 0:
                self.teshis_label.setText("ℹ️ Henüz belirti seçilmemiş.")
                self.oneri_label.setText("Lütfen hastanın mevcut belirtilerini seçiniz.")
            else:
                self.teshis_label.setText("⚠️ Kesin teşhis konulamadı.")
                self.oneri_label.setText(
                    f"Seçili belirtiler ({len(aktif)} adet) tam bir teşhis için yeterli değil. "
                    f"Ek muayene ve testler gerekebilir."
                )


    def otomatik_teshis_gonder(self, ortalamalar):
        try:
            aktif = set([ad.split(" (")[0] for ad, cb in self.checkboxlar if cb.isChecked()])
            if not aktif or not ortalamalar:
                return

            ogunler = list(ortalamalar.keys())
            son_ogun = ogunler[-1]
            ort = ortalamalar[son_ogun]

            teshisler = [
                {
                    "isim": "Hipoglisemi",
                    "min": 0, "max": 70,
                    "belirtiler": {"Nöropati", "Polifaji", "Yorgunluk"},
                    "mesaj": "Hipoglisemi tespit edildi. Belirtiler ve ortalama seviye uyuşuyor. Acil müdahale gerekebilir.",
                    "tip": "kritik"
                },
                {
                    "isim": "Normal - Alt Düzey",
                    "min": 70, "max": 111,
                    "belirtiler": {"Yorgunluk", "Kilo Kaybı"},
                    "mesaj": "Kan şekeri normal alt düzeyde. Belirtiler izlenmeli.",
                    "tip": "bilgilendirme"
                },
                {
                    "isim": "Normal - Üst Düzey",
                    "min": 111, "max": 181,
                    "belirtiler": {"Bulanık Görme", "Nöropati"},
                    "mesaj": "Hafif yüksek kan şekeri. Belirtiler ve ortalama değer uyumlu. Diyet/egzersiz önerilmeli.",
                    "tip": "takip"
                },
                {
                    "isim": "Hiperglisemi",
                    "min": 181, "max": 999,
                    "belirtiler": {"Yaraların Yavaş İyileşmesi", "Polifaji", "Polidipsi"},
                    "mesaj": "Hiperglisemi tespit edildi. Sistem acil durum uyarısı oluşturdu.",
                    "tip": "acil"
                }
            ]

            for t in teshisler:
                if t["min"] <= ort < t["max"] and t["belirtiler"].issubset(aktif):
                    oneri = oneri_getir(ort, aktif)

                    if oneri:
                        conn = connect()
                        cur = conn.cursor()

                        cur.execute("SELECT doktor_id FROM hastalar WHERE id = ?", (self.hasta_id,))
                        doktor_row = cur.fetchone()
                        doktor_id = doktor_row[0] if doktor_row else None

                        try:
                            if doktor_id:
                                cur.execute("""
                                    INSERT INTO notlar_ve_oneriler (hasta_id, doktor_id, tarih, baslik, aciklama)
                                    VALUES (?, ?, datetime('now'), ?, ?)
                                """, (
                                    self.hasta_id,
                                    doktor_id,
                                    f"🧾 Otomatik Öneri ({oneri['aralik']})",
                                    f"📋 Belirtiler: {oneri['belirtiler']}\n"
                                    f"🥗 Diyet: {oneri['diyet']}\n"
                                    f"🏃 Egzersiz: {oneri['egzersiz']}"
                                ))
                            if not doktor_id:
                                print("Doktor ID bulunamadı, öneri eklenmedi.")
                                return

                            conn.commit()
                        except Exception as e:
                            print("Not ekleme hatası:", e)

                        cur.execute("SELECT id FROM uyari_turleri WHERE tip = ?", (t["tip"],))
                        tip_id = cur.fetchone()
                        if tip_id:
                            cur.execute("""
                                INSERT INTO uyarilar (hasta_id, tip_id, mesaj, zaman)
                                VALUES (?, ?, ?, datetime('now'))
                            """, (self.hasta_id, tip_id[0], f"🧪 Teşhis: {t['isim']} - {t['mesaj']}"))
                            conn.commit()

                        cur.close()
                        conn.close()
                    break

        except Exception as e:
            print("Teşhis bildirimi gönderme hatası:", e)



