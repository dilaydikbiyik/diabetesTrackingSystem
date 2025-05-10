from PyQt5.QtWidgets import QWidget, QPushButton
from ekranlar.hasta_giris import HastaGirisEkrani
from ekranlar.doktor_giris import DoktorGirisEkrani

class AnaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Seçimi")
        self.setGeometry(300,300,300,150)

        self.hasta_button = QPushButton("Hasta Girişi",self)
        self.hasta_button.setGeometry(100, 30, 100, 30)
        self.hasta_button.clicked.connect(self.hasta_girisi_ac)

        self.doktor_button = QPushButton("Doktor Girişi", self)
        self.doktor_button.setGeometry(100, 70, 100, 30)
        self.doktor_button.clicked.connect(self.doktor_girisi_ac)

    def hasta_girisi_ac(self):
        self.hasta_pencere = HastaGirisEkrani()
        self.hasta_pencere.show()

    def doktor_girisi_ac(self):
        self.doktor_pencere = DoktorGirisEkrani()
        self.doktor_pencere.show()
