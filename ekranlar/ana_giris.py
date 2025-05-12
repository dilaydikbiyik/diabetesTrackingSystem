from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
from ekranlar.hasta_giris import HastaGirisEkrani
from ekranlar.doktor_giris import DoktorGirisEkrani

class AnaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diabetes Following System")
        self.setGeometry(400, 150, 800, 600)
        self.setStyleSheet("background-color: white;")

        # 🔹 Dil seçimi ve logo (sağ üst)
        dil_combo = QComboBox()
        dil_combo.addItems(["Türkçe", "English"])
        dil_combo.setStyleSheet("padding: 5px; font-size: 12px;")

        logo = QLabel()
        pixmap = QPixmap("assets/saglik_logo.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)

        sag_ust_layout = QHBoxLayout()
        sag_ust_layout.addStretch()
        sag_ust_layout.addWidget(dil_combo)
        sag_ust_layout.addSpacing(10)
        sag_ust_layout.addWidget(logo)

        # 🔷 Başlık
        baslik = QLabel("Diabetes Following System")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #0d47a1;
            margin-top: 30px;
            margin-bottom: 30px;
        """)

        # 🔘 Butonlar
        self.hasta_button = QPushButton("Hasta Girişi")
        self.hasta_button.setFixedSize(280, 90)
        self.hasta_button.setStyleSheet("""
            QPushButton {
                background-color: #e53935;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
        """)

        self.doktor_button = QPushButton("Doktor Girişi")
        self.doktor_button.setFixedSize(280, 90)
        self.doktor_button.setStyleSheet("""
            QPushButton {
                background-color: #1e88e5;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)

        self.hasta_button.clicked.connect(self.hasta_girisi_ac)
        self.doktor_button.clicked.connect(self.doktor_girisi_ac)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.hasta_button)
        button_row.addSpacing(40)
        button_row.addWidget(self.doktor_button)
        button_row.addStretch()

        # 🔗 Şifremi Unuttum
        sifre_label = QLabel('<a href="#">Şifremi Unuttum</a>')
        sifre_label.setOpenExternalLinks(True)
        sifre_label.setAlignment(Qt.AlignCenter)
        sifre_label.setStyleSheet("color: #0d47a1; font-size: 12px; margin-top: 10px;")
        sifre_label.setCursor(QCursor(Qt.PointingHandCursor))

        # 🔧 Ana dikey düzen
        ana_layout = QVBoxLayout()
        ana_layout.addLayout(sag_ust_layout)
        ana_layout.addSpacing(10)
        ana_layout.addWidget(baslik)
        ana_layout.addSpacing(10)
        ana_layout.addLayout(button_row)
        ana_layout.addWidget(sifre_label)
        ana_layout.addStretch()

        self.setLayout(ana_layout)

    def hasta_girisi_ac(self):
        self.hasta_pencere = HastaGirisEkrani()
        self.hasta_pencere.show()

    def doktor_girisi_ac(self):
        self.doktor_pencere = DoktorGirisEkrani()
        self.doktor_pencere.show()
