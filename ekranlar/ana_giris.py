from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QCursor, QColor, QPalette, QLinearGradient, QIcon
from ekranlar.hasta_giris import HastaGirisEkrani
from ekranlar.doktor_giris import DoktorGirisEkrani
from ekranlar.yardim_ekrani import YardimPenceresi
from ekranlar.sifre_sifirla import SifreSifirlaEkrani

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
        self.baslik_label = QLabel(baslik)
        self.baslik_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        self.baslik_label.setAlignment(Qt.AlignCenter)

        # Açıklama
        self.aciklama_label = QLabel(aciklama)
        self.aciklama_label.setStyleSheet("font-size: 12px; color: white; padding: 5px;")
        self.aciklama_label.setWordWrap(True)
        self.aciklama_label.setAlignment(Qt.AlignCenter)

        # Düzen
        kart_layout = QVBoxLayout()
        kart_layout.addWidget(ikon_label)
        kart_layout.addWidget(self.baslik_label)
        kart_layout.addWidget(self.aciklama_label)

        self.setLayout(kart_layout)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class AnaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diabetes Tracking System")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(400, 150, 1000, 700)

        # Dil ayarları
        self.dil_secimi = "Türkçe"
        self.dil_dict = {
            "Türkçe": {
                "baslik": "DİYABET TAKİP SİSTEMİ",
                "aciklama": "Kişisel diyabet bilgilerinizi yönetebileceğiniz, Türkiye'nin güvenilir sağlık takip sistemidir.",
                "hasta_girisi": "Hasta Girişi",
                "hasta_aciklama": "• T.C. Kimlik numaranız ile giriş yapabilirsiniz",
                "doktor_girisi": "Doktor Girişi",
                "doktor_aciklama": "• Hekim şifreniz ile giriş yapabilirsiniz",
                "yardim": "Yardım",
                "yardim_aciklama": "• Kullanım kılavuzu\n• Sıkça sorulan sorular",
                "sifremi_unuttum": "Şifremi Unuttum",
                "iletisim": "Diyabet Takip Sistemi: 0850 000 00 00"
            },
            "English": {
                "baslik": "DIABETES TRACKING SYSTEM",
                "aciklama": "Manage your diabetes data securely with Turkey's trusted health monitoring system.",
                "hasta_girisi": "Patient Login",
                "hasta_aciklama": "• Log in with your National ID",
                "doktor_girisi": "Doctor Login",
                "doktor_aciklama": "• Log in with your medical credentials",
                "yardim": "Help",
                "yardim_aciklama": "• User guide\n• Frequently asked questions",
                "sifremi_unuttum": "Forgot Password",
                "iletisim": "Diabetes Tracking System: 0850 000 00 00"
            }
        }

        # Arka plan
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#ffffff"))
        gradient.setColorAt(1, QColor("#f0f7ff"))

        palette = QPalette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Üst bar
        ust_serit = QFrame()
        ust_serit.setFixedHeight(100)
        ust_serit.setStyleSheet("background-color: #42C2BC;")

        self.dil_combo = QComboBox()
        self.dil_combo.addItems(["Türkçe", "English"])
        self.dil_combo.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border-radius: 5px;
            background-color: white;
            border: 1px solid #ddd;
        """)
        self.dil_combo.currentIndexChanged.connect(self.dil_degisti)

        saglik_logo = QLabel()
        pixmap = QPixmap("assets/enabiz_logo.png").scaled(220, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        saglik_logo.setPixmap(pixmap)

        enabiz_logo = QLabel()
        enabiz_pixmap = QPixmap("assets/saglik_logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        enabiz_logo.setPixmap(enabiz_pixmap)

        ust_layout = QHBoxLayout(ust_serit)
        ust_layout.addWidget(enabiz_logo)
        ust_layout.addStretch()
        ust_layout.addWidget(self.dil_combo)
        ust_layout.addSpacing(10)
        ust_layout.addWidget(saglik_logo)
        ust_layout.setContentsMargins(20, 10, 20, 10)

        # Başlık ve açıklama
        self.baslik = QLabel()
        self.baslik.setAlignment(Qt.AlignCenter)
        self.baslik.setStyleSheet("""
            font-size: 52px;
            font-weight: bold;
            color: #0d47a1;
            margin-top: 20px;
        """)

        self.aciklama = QLabel()
        self.aciklama.setAlignment(Qt.AlignCenter)
        self.aciklama.setStyleSheet("""
            font-size: 16px; 
            color: #555;
            margin-bottom: 30px;
        """)

        baslik_layout = QVBoxLayout()
        baslik_layout.addWidget(self.baslik)
        baslik_layout.addWidget(self.aciklama)

        # Kartlar
        self.hasta_kart = KartFrame("", "", "assets/maske.png", "#e53935")
        self.hasta_kart.mousePressEvent = lambda event: self.hasta_girisi_ac()

        self.doktor_kart = KartFrame("", "", "assets/steteskop.png", "#1e88e5")
        self.doktor_kart.mousePressEvent = lambda event: self.doktor_girisi_ac()

        self.yardim_kart = KartFrame("", "", "assets/soru_isareti.png", "#42C2BC")
        self.yardim_kart.mousePressEvent= lambda event : self.yardim_ekrani_ac()

        kartlar_layout = QHBoxLayout()
        kartlar_layout.addStretch()
        kartlar_layout.addWidget(self.hasta_kart)
        kartlar_layout.addSpacing(20)
        kartlar_layout.addWidget(self.doktor_kart)
        kartlar_layout.addSpacing(20)
        kartlar_layout.addWidget(self.yardim_kart)
        kartlar_layout.addStretch()

        # Alt bilgi
        self.sifre_label = QLabel()
        self.sifre_label.setOpenExternalLinks(True)
        self.sifre_label.setAlignment(Qt.AlignCenter)
        self.sifre_label.setStyleSheet("color: #0d47a1; font-size: 14px;")
        self.sifre_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.sifre_label.mousePressEvent = lambda event: self.sifre_sifirlama_ac()

        self.iletisim_label = QLabel()
        self.iletisim_label.setAlignment(Qt.AlignCenter)
        self.iletisim_label.setStyleSheet("color: #555; font-size: 14px;")

        alt_layout = QVBoxLayout()
        alt_layout.addWidget(self.sifre_label)
        alt_layout.addWidget(self.iletisim_label)

        # Ana düzen
        ana_layout = QVBoxLayout()
        ana_layout.addWidget(ust_serit)
        ana_layout.addSpacing(10)
        ana_layout.addLayout(baslik_layout)
        ana_layout.addLayout(kartlar_layout)
        ana_layout.addLayout(alt_layout)
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(10)

        self.setLayout(ana_layout)

        self.dil_degisti()  # Varsayılan dil ile başlat

    def dil_degisti(self):
        dil = self.dil_combo.currentText()
        secim = self.dil_dict[dil]

        self.baslik.setText(secim["baslik"])
        self.aciklama.setText(secim["aciklama"])
        self.hasta_kart.baslik_label.setText(secim["hasta_girisi"])
        self.hasta_kart.aciklama_label.setText(secim["hasta_aciklama"])
        self.doktor_kart.baslik_label.setText(secim["doktor_girisi"])
        self.doktor_kart.aciklama_label.setText(secim["doktor_aciklama"])
        self.yardim_kart.baslik_label.setText(secim["yardim"])
        self.yardim_kart.aciklama_label.setText(secim["yardim_aciklama"])
        self.sifre_label.setText(f'<a href="#">{secim["sifremi_unuttum"]}</a>')
        self.iletisim_label.setText(secim["iletisim"])

    def hasta_girisi_ac(self):
        self.hasta_pencere = HastaGirisEkrani()
        self.hasta_pencere.show()

    def doktor_girisi_ac(self):
        self.doktor_pencere = DoktorGirisEkrani()
        self.doktor_pencere.show()

    def yardim_ekrani_ac(self):
        self.yardim_pencere = YardimPenceresi(dil=self.dil_combo.currentText())
        self.yardim_pencere.show()

    def sifre_sifirlama_ac(self):
        self.sifre_pencere = SifreSifirlaEkrani()
        self.sifre_pencere.show()
