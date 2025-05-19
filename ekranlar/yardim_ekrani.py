from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class YardimPenceresi(QWidget):
    def __init__(self, dil="Türkçe"):
        super().__init__()
        self.setWindowTitle("Yardım / Help")
        self.setGeometry(500, 200, 500, 400)

        self.dil = dil
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        baslik = QLabel("Yardım" if self.dil == "Türkçe" else "Help")
        baslik.setFont(QFont("Arial", 16, QFont.Bold))
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        if self.dil == "Türkçe":
            icerik = (
                "🔹 Bu sistem, doktorların hastalarının diyabet verilerini takip etmesini sağlar.\n"
                "🔸 Giriş yapmak için kullanıcı adınızı ve şifrenizi girin.\n"
                "🔸 Doktor olarak giriş yaptıktan sonra hastalarınızı ekleyebilir, kan şekeri verilerini, egzersiz ve diyet bilgilerini görebilir ya da analiz edebilirsiniz.\n"
                "🔸 Hasta olarak giriş yaptıysanız sadece kendi bilgilerinizi görüntüleyebilirsiniz.\n"
                "📌 Sistem güvenlik amaçlı olarak giriş bilgilerini şifrelemektedir.\n"
                "❓ Yardım için destek hattı: 0850 000 00 00"
            )
        else:
            icerik = (
                "🔹 This system allows doctors to monitor their patients' diabetes data.\n"
                "🔸 Enter your ID and password to log in.\n"
                "🔸 As a doctor, you can add patients, view and analyze their blood sugar, exercise, and diet records.\n"
                "🔸 As a patient, you can only view your own data.\n"
                "📌 The system encrypts login credentials for security.\n"
                "❓ For help, contact support: 0850 000 00 00"
            )

        self.text_area.setText(icerik)
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    def set_dil(self, dil):
        self.dil = dil
        self.initUI()
