from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QVBoxLayout, QFormLayout, QFrame
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from database import connect
from utils.hashing import hash_password
from views.patient.patient_main import HastaAnaEkrani

MAC_STYLE = """
QWidget {
    background-color: #f5f7fa;
    font-family: -apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
    color: #1a1a2e;
}
QFrame#card {
    background-color: white;
    border-radius: 14px;
    border: 1px solid #e0e0e0;
}
QLabel#title {
    font-size: 22px;
    font-weight: bold;
    color: #1a1a2e;
}
QLabel#subtitle {
    font-size: 13px;
    color: #6b7280;
}
QLabel {
    font-size: 14px;
    color: #374151;
    font-weight: 600;
}
QLineEdit {
    background-color: #ffffff;
    border: 1.5px solid #d1d5db;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 15px;
    color: #111827;
    selection-background-color: #dc3545;
}
QLineEdit:focus {
    border: 1.5px solid #dc3545;
    background-color: #fff8f8;
    outline: none;
}
QLineEdit::placeholder {
    color: #9ca3af;
}
QPushButton#loginBtn {
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 0.5px;
}
QPushButton#loginBtn:hover {
    background-color: #b91c2c;
}
QPushButton#loginBtn:pressed {
    background-color: #991b1b;
}
"""


class HastaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hasta Girişi")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setFixedSize(440, 380)
        self.setStyleSheet(MAC_STYLE)
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 30, 30, 30)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame(objectName="card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 28, 30, 28)
        card_layout.setSpacing(18)

        # Header
        title = QLabel("🏥 Hasta Girişi", objectName="title")
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("TC Kimlik No ve şifrenizle giriş yapın", objectName="subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)

        # Form
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignLeft)

        self.txt_tc = QLineEdit()
        self.txt_tc.setPlaceholderText("11 haneli TC kimlik numaranız")
        self.txt_tc.setMaxLength(11)
        self.txt_tc.setMinimumHeight(44)

        self.txt_sifre = QLineEdit()
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        self.txt_sifre.setPlaceholderText("Şifrenizi girin")
        self.txt_sifre.setMinimumHeight(44)
        self.txt_sifre.returnPressed.connect(self.giris_yap)

        form.addRow("TC Kimlik No", self.txt_tc)
        form.addRow("Şifre", self.txt_sifre)
        card_layout.addLayout(form)

        btn = QPushButton("Giriş Yap", objectName="loginBtn")
        btn.setMinimumHeight(46)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.giris_yap)
        card_layout.addWidget(btn)

        outer.addWidget(card)

    def giris_yap(self):
        tc = self.txt_tc.text().strip()
        sifre = self.txt_sifre.text().strip()

        if not tc or not sifre:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        hashed_sifre = hash_password(sifre)
        conn = connect()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ad, soyad FROM hastalar WHERE tc = ? AND sifre = ?",
                    (tc, hashed_sifre)
                )
                result = cursor.fetchone()

                if result:
                    ad, soyad = result[0], result[1]
                    self.hasta_ekrani = HastaAnaEkrani(ad, soyad, tc)
                    self.hasta_ekrani.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Hata", "TC kimlik veya şifre hatalı.")

                conn.close()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Veritabanı hatası:\n{e}")
        else:
            QMessageBox.critical(self, "Bağlantı Hatası", "Veritabanına bağlanılamadı.")
