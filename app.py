import sys
from PyQt5.QtWidgets import QApplication
from ekranlar.ana.ana_giris import AnaGirisEkrani

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ana_ekran = AnaGirisEkrani()
    ana_ekran.show()
    sys.exit(app.exec())