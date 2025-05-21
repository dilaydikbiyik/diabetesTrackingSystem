from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt

class AramaEkrani(QWidget):
    def __init__(self, numara="08500000000"):
        super().__init__()
        self.setWindowTitle("Arama Ekranı")
        self.setFixedSize(300, 500)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Üstte numara gösterimi
        self.numara_label = QLabel(numara)
        self.numara_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.numara_label.setStyleSheet("color: white;")
        self.numara_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.numara_label)

        # Tuşlar
        tus_takimi = QGridLayout()
        tuslar = [
            ("1", ""), ("2", "ABC"), ("3", "DEF"),
            ("4", "GHI"), ("5", "JKL"), ("6", "MNO"),
            ("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ"),
            ("*", ""), ("0", "+"), ("#", "")
        ]

        for i, (sayi, harfler) in enumerate(tuslar):
            btn = QPushButton()
            btn.setText(f"{sayi}\n{harfler}")
            btn.setFixedSize(70, 70)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: #222;
                    border-radius: 35px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #444;
                }
            """)
            tus_takimi.addWidget(btn, i // 3, i % 3)

        layout.addLayout(tus_takimi)

        # Yeşil arama butonu
        arama_buton = QPushButton()
        arama_buton.setFixedSize(70, 70)
        arama_buton.setStyleSheet("""
            QPushButton {
                background-color: #00cc66;
                border-radius: 35px;
            }
        """)
        arama_buton.setIcon(QIcon("assets/phone_icon.png"))  # yeşil arama simgesi ikon olarak
        arama_buton.setIconSize(arama_buton.size() * 0.6)
        arama_buton.clicked.connect(self.close)  # Tıklandığında ekranı kapat

        layout.addWidget(arama_buton, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
