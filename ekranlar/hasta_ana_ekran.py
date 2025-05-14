from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class HastaAnaEkrani(QWidget):
    def __init__(self, ad, soyad):
        super().__init__()
        self.setWindowTitle("Hasta Ana Sayfası")
        self.setGeometry(400, 300, 400, 200)

        layout = QVBoxLayout()
        hosgeldin_label = QLabel(f"Hoş geldiniz {ad} {soyad}!")
        hosgeldin_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2e7d32;")
        layout.addWidget(hosgeldin_label)

        self.setLayout(layout)
