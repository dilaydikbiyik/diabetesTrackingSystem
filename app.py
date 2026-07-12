import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from views.main.main_login import AnaGirisEkrani

if __name__ == "__main__":
    # Mac Retina / HiDPI support
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Set a clean, readable system font for Mac
    font = QFont("-apple-system", 13)
    app.setFont(font)

    main_screen = AnaGirisEkrani()
    main_screen.show()
    sys.exit(app.exec())