from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QCursor, QColor, QPalette, QLinearGradient, QIcon
from ekranlar.hasta_giris import HastaGirisEkrani
from ekranlar.doktor_giris import DoktorGirisEkrani


class KartFrame(QFrame):
    def __init__(self, baslik, aciklama, icon_path, renk):
        super().__init__()
        self.setFixedSize(220, 200)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {renk};
                border-radius: 12px;
                color: white;
                padding: 15px;
            }}
            QFrame:hover {{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                                 stop:0 {renk}, stop:1 darker({renk}));
                border: 2px solid white;
            }}
        """)

        # İkon
        ikon_label = QLabel()
        if icon_path:
            ikon = QPixmap(icon_path).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            ikon_label.setPixmap(ikon)
            ikon_label.setAlignment(Qt.AlignCenter)

        # Başlık
        baslik_label = QLabel(baslik)
        baslik_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        baslik_label.setAlignment(Qt.AlignCenter)

        # Açıklama
        aciklama_label = QLabel(aciklama)
        aciklama_label.setStyleSheet("font-size: 12px; color: white; padding: 5px;")
        aciklama_label.setWordWrap(True)
        aciklama_label.setAlignment(Qt.AlignCenter)

        # Düzen
        kart_layout = QVBoxLayout()
        kart_layout.addWidget(ikon_label)
        kart_layout.addWidget(baslik_label)
        kart_layout.addWidget(aciklama_label)

        self.setLayout(kart_layout)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class AnaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diabetes Following System")
        self.setGeometry(400, 150, 1000, 700)

        # Arka plan rengi - e-Nabız tarzı gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#ffffff"))
        gradient.setColorAt(1, QColor("#f0f7ff"))

        palette = QPalette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Üst kısım - turkuaz şerit oluşturma
        ust_serit = QFrame()
        ust_serit.setFixedHeight(100)
        ust_serit.setStyleSheet("background-color: #42C2BC;")

        # 🔹 Dil seçimi ve logo (sağ üst)
        dil_combo = QComboBox()
        dil_combo.addItems(["Türkçe", "English"])
        dil_combo.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border-radius: 5px;
            background-color: white;
            border: 1px solid #ddd;
        """)

        # Sağlık Bakanlığı logosu
        saglik_logo = QLabel()
        pixmap = QPixmap("assets/saglik_logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        saglik_logo.setPixmap(pixmap)

        # e-Nabız logo ekleme
        enabiz_logo = QLabel()
        enabiz_pixmap = QPixmap("assets/enabiz_logo.png").scaled(220, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        enabiz_logo.setPixmap(enabiz_pixmap)

        ust_layout = QHBoxLayout(ust_serit)
        ust_layout.addWidget(enabiz_logo)
        ust_layout.addStretch()
        ust_layout.addWidget(dil_combo)
        ust_layout.addSpacing(10)
        ust_layout.addWidget(saglik_logo)
        ust_layout.setContentsMargins(20, 10, 20, 10)

        # 🔷 Başlık ve açıklama
        baslik_container = QFrame()
        baslik_container.setStyleSheet("background-color: transparent;")

        baslik = QLabel("Diabetes Following System")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("""
            font-size: 52px;
            font-weight: bold;
            color: #0d47a1;
            margin-top: 20px;
        """)

        aciklama = QLabel(
            "Kişisel diyabet bilgilerinizi yönetebileceğiniz, Türkiye'nin güvenilir sağlık takip sistemidir.")
        aciklama.setAlignment(Qt.AlignCenter)
        aciklama.setStyleSheet("""
            font-size: 16px; 
            color: #555;
            margin-bottom: 30px;
        """)

        baslik_layout = QVBoxLayout(baslik_container)
        baslik_layout.addWidget(baslik)
        baslik_layout.addWidget(aciklama)

        # 🔘 Giriş seçenekleri kartları
        kartlar_container = QFrame()
        kartlar_container.setStyleSheet("background-color: transparent;")

        kartlar_layout = QHBoxLayout(kartlar_container)

        # Hasta girişi kartı
        hasta_kart = KartFrame(
            "Hasta Girişi",
            "• T.C. Kimlik numaranız ile giriş yapabilirsiniz",
            "assets/maske.png",  # Varsayılan ikon yoksa oluşturmanız gerekebilir
            "#e53935"  # Kırmızı
        )
        hasta_kart.mousePressEvent = lambda event: self.hasta_girisi_ac()

        # Doktor girişi kartı
        doktor_kart = KartFrame(
            "Doktor Girişi",
            "• Hekim şifreniz ile giriş yapabilirsiniz",
            "assets/steteskop.png",  # Varsayılan ikon yoksa oluşturmanız gerekebilir
            "#1e88e5"  # Mavi
        )
        doktor_kart.mousePressEvent = lambda event: self.doktor_girisi_ac()

        # Yardım kartı
        yardim_kart = KartFrame(
            "Yardım",
            "• Kullanım kılavuzu\n• Sıkça sorulan sorular",
            "assets/soru_isareti.png",  # Varsayılan ikon yoksa oluşturmanız gerekebilir
            "#42C2BC"  # Turkuaz
        )

        kartlar_layout.addStretch()
        kartlar_layout.addWidget(hasta_kart)
        kartlar_layout.addSpacing(20)
        kartlar_layout.addWidget(doktor_kart)
        kartlar_layout.addSpacing(20)
        kartlar_layout.addWidget(yardim_kart)
        kartlar_layout.addStretch()

        # 🔗 Alt bilgi
        alt_bilgi = QFrame()
        alt_bilgi.setFixedHeight(60)
        alt_bilgi.setStyleSheet("background-color: transparent; margin-top: 30px;")

        sifre_label = QLabel('<a href="#">Şifremi Unuttum</a>')
        sifre_label.setOpenExternalLinks(True)
        sifre_label.setAlignment(Qt.AlignCenter)
        sifre_label.setStyleSheet("color: #0d47a1; font-size: 14px;")
        sifre_label.setCursor(QCursor(Qt.PointingHandCursor))

        iletisim_label = QLabel("Diabetes Following System: 0850 000 00 00")
        iletisim_label.setAlignment(Qt.AlignCenter)
        iletisim_label.setStyleSheet("color: #555; font-size: 14px;")

        alt_layout = QVBoxLayout(alt_bilgi)
        alt_layout.addWidget(sifre_label)
        alt_layout.addWidget(iletisim_label)

        # 🔧 Ana dikey düzen
        ana_layout = QVBoxLayout()
        ana_layout.addWidget(ust_serit)
        ana_layout.addSpacing(10)
        ana_layout.addWidget(baslik_container)
        ana_layout.addWidget(kartlar_container)
        ana_layout.addWidget(alt_bilgi)
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(10)

        self.setLayout(ana_layout)

    def hasta_girisi_ac(self):
        self.hasta_pencere = HastaGirisEkrani()
        self.hasta_pencere.show()

    def doktor_girisi_ac(self):
        self.doktor_pencere = DoktorGirisEkrani()
        self.doktor_pencere.show()