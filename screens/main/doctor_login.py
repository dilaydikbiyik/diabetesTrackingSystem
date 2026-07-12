from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QVBoxLayout, QFormLayout, QFrame
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from database import connect
from hashing import hash_password
from screens.doctor.doctor_main import DoktorAnaEkran

MAC_STYLE = """
QWidget {
    background-color: #f0f7ff;
    font-family: -apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
    color: #1a1a2e;
}
QFrame#card {
    background-color: white;
    border-radius: 14px;
    border: 1px solid #dbeafe;
}
QLabel#title {
    font-size: 22px;
    font-weight: bold;
    color: #1e3a8a;
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
    border: 1.5px solid #bfdbfe;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 15px;
    color: #111827;
    selection-background-color: #1d4ed8;
}
QLineEdit:focus {
    border: 1.5px solid #2563eb;
    background-color: #eff6ff;
}
QPushButton#loginBtn {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 0.5px;
}
QPushButton#loginBtn:hover {
    background-color: #1d4ed8;
}
QPushButton#loginBtn:pressed {
    background-color: #1e40af;
}
"""


class DoktorGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doktor Girişi")
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
        title = QLabel("🩺 Doktor Girişi", objectName="title")
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
            QMessageBox.warning(self, "Uyarı", "Lütfen TC ve şifre alanlarını doldurun!")
            return

        hashed_sifre = hash_password(sifre)
        conn = connect()

        if not conn:
            QMessageBox.critical(self, "Hata", "Veritabanı bağlantısı kurulamadı!")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, ad, soyad FROM doktorlar WHERE tc = ? AND sifre = ?",
                (tc, hashed_sifre)
            )
            result = cursor.fetchone()

            if result:
                doktor_id, ad, soyad = result[0], result[1], result[2]
                self.doktor_ana_ekran = DoktorAnaEkran(doktor_id)
                self.doktor_ana_ekran.show()
                self.close()
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz TC veya şifre!")

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası:\n{e}")
