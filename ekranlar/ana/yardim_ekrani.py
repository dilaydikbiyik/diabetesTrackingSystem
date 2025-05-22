from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTextEdit,
                             QHBoxLayout, QFrame)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class YardimPenceresi(QWidget):
    def __init__(self, dil="Türkçe"):
        super().__init__()
        self.setWindowTitle("Yardım / Help")
        self.setGeometry(500, 200, 600, 500)
        self.dil = dil

        self.setStyleSheet("background-color: #f5f5f5; border-radius: 10px;")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Başlık
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #3498db; border-radius: 10px;")
        header_layout = QHBoxLayout(header_frame)

        title_text = "Diyabet Takip Sistemi Yardım" if self.dil == "Türkçe" else "Diabetes Tracking System Help"
        baslik = QLabel(title_text)
        baslik.setFont(QFont("Arial", 16, QFont.Bold))
        baslik.setStyleSheet("color: white;")
        baslik.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(baslik)

        main_layout.addWidget(header_frame)

        # Yardım Metni
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
        """)
        content_layout = QVBoxLayout(content_frame)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            border: none;
            background-color: transparent;
            font-size: 14px;
            line-height: 150%;
        """)
        self.text_area.setFont(QFont("Arial", 11))

        if self.dil == "Türkçe":
            icerik = (
                "<h3 style='color: #3498db;'>Diyabet Takip Sistemi Yardım</h3>"
                "<p><b style='color: #3498db;'>🔹 Sistem Hakkında:</b><br>"
                "Bu sistem, doktorların hastalarının diyabet verilerini takip etmesini sağlar.</p>"
                "<p><b style='color: #3498db;'>🔸 Giriş Yapma:</b><br>"
                "Kullanıcı adınızı ve şifrenizi girerek sisteme giriş yapabilirsiniz.</p>"
                "<p><b style='color: #3498db;'>🩺 Doktor İşlevleri:</b><br>"
                "- Hasta ekleyebilir<br>"
                "- Kan şekeri verilerini inceleyebilir<br>"
                "- Egzersiz ve diyet bilgilerini takip edebilir<br>"
                "- Teşhis ve öneriler oluşturabilir</p>"
                "<p><b style='color: #3498db;'>😷 Hasta İşlevleri:</b><br>"
                "- Sadece kendi bilgilerini görüntüleyebilir<br>"
                "- Ölçüm verilerini girebilir</p>"
                "<p><b style='color: #2ecc71;'>🔒 Güvenlik:</b><br>"
                "Giriş bilgileriniz sistem tarafından şifrelenerek korunur.</p>"
                "<p><b style='color: #e74c3c;'>📞 Destek:</b><br>"
                "Yardım hattı: <a href='#' style='color: black; font-weight: bold;'>0850 000 00 00</a></p>"
            )
        else:
            icerik = (
                "<h3 style='color: #3498db;'>Diabetes Tracking System Help</h3>"
                "<p><b style='color: #3498db;'>🔹 About the System:</b><br>"
                "This system allows doctors to monitor their patients' diabetes data.</p>"
                "<p><b style='color: #3498db;'>🔸 Logging In:</b><br>"
                "Enter your username and password to log in.</p>"
                "<p><b style='color: #3498db;'>🩺 Doctor Functions:</b><br>"
                "- Add patients<br>"
                "- View and analyze blood sugar data<br>"
                "- Track exercise and diet info<br>"
                "- Provide recommendations</p>"
                "<p><b style='color: #3498db;'>😷 Patient Functions:</b><br>"
                "- View only their own records<br>"
                "- Submit measurement data</p>"
                "<p><b style='color: #2ecc71;'>🔒 Security:</b><br>"
                "Login information is encrypted for your protection.</p>"
                "<p><b style='color: #e74c3c;'>📞 Support:</b><br>"
                "Support line: <a href='#' style='color: black; font-weight: bold;'>0850 000 00 00</a></p>"
            )

        self.text_area.setHtml(icerik)
        content_layout.addWidget(self.text_area)
        main_layout.addWidget(content_frame)

        # Footer
        footer_label = QLabel(
            "© 2025 Diyabet Takip Sistemi" if self.dil == "Türkçe" else "© 2025 Diabetes Tracking System")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        main_layout.addWidget(footer_label)

        self.setLayout(main_layout)

    def set_dil(self, dil):
        self.dil = dil
        self.initUI()