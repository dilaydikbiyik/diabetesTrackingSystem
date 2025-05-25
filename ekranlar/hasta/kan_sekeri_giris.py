from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDateTimeEdit, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QDateTime, Qt
from datetime import datetime

def saat_araligina_gore_grup(zaman):
    saat = zaman.hour
    dakika = zaman.minute

    if 7 <= saat < 8 or (saat == 8 and dakika == 0):
        return "sabah"
    elif 12 <= saat < 13 or (saat == 13 and dakika == 0):
        return "öğle"
    elif 15 <= saat < 16 or (saat == 16 and dakika == 0):
        return "ikindi"
    elif 18 <= saat < 19 or (saat == 19 and dakika == 0):
        return "akşam"
    elif 22 <= saat < 23 or (saat == 23 and dakika == 0):
        return "gece"
    return None

class KanSekeriGirisPenceresi(QDialog):
    def __init__(self, hasta_id, conn):
        super().__init__()
        self.setWindowTitle("🩸 Kan Şekeri Ölçümü Girişi")
        self.setFixedSize(450, 380)
        self.hasta_id = hasta_id
        self.conn = conn
        self.cursor = self.conn.cursor()

        self.setStyleSheet(self.get_stylesheet())

        self.init_ui()

    def get_stylesheet(self):
        """Dialog için modern stil"""
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8FBFF, stop:1 #E8F4FD);
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            QGroupBox {
                font-weight: bold;
                border: 2px solid #D1E7DD;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: white;
                color: #2E86AB;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #1B5E85;
                font-size: 14px;
            }

            QLabel {
                color: #2E86AB;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
            }

            QLineEdit {
                border: 2px solid #D1E7DD;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                color: #1B5E85;
            }

            QLineEdit:focus {
                border-color: #2E86AB;
                background-color: #F8FBFF;
            }

            QDateTimeEdit {
                border: 2px solid #D1E7DD;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                color: #1B5E85;
            }

            QDateTimeEdit:focus {
                border-color: #2E86AB;
                background-color: #F8FBFF;
            }

            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2E86AB, stop:1 #1B5E85);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 12px 20px;
                min-height: 20px;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3A94BB, stop:1 #2A6E95);
            }

            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1B5E85, stop:1 #14456B);
            }

            QPushButton#cancelBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6C757D, stop:1 #495057);
            }

            QPushButton#cancelBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7C858D, stop:1 #596067);
            }
        """

    def init_ui(self):
        layout = QVBoxLayout()

        # Başlık etiketi
        title_label = QLabel("🩸 Kan Şekeri Ölçüm Girişi")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1B5E85;
                padding: 10px 0px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tarih/Saat Girişi
        tarih_label = QLabel("📅 Ölçüm Zamanı:")
        layout.addWidget(tarih_label)

        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        self.datetime_edit.setCalendarPopup(True)
        layout.addWidget(self.datetime_edit)

        # Kan şekeri değeri girişi
        seker_label = QLabel("🧪 Kan Şekeri (mg/dL):")
        layout.addWidget(seker_label)

        self.giris_edit = QLineEdit()
        self.giris_edit.setPlaceholderText("Örn: 120")
        layout.addWidget(self.giris_edit)

        # Bilgilendirme notu
        info_label = QLabel("📌 Lütfen geçerli bir saat aralığında ölçüm yapınız:\n"
                            "• Sabah: 07:00–08:00\n• Öğle: 12:00–13:00\n• İkindi: 15:00–16:00\n"
                            "• Akşam: 18:00–19:00\n• Gece: 22:00–23:00")
        info_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #6c757d;
                margin-top: 10px;
            }
        """)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Butonlar
        kaydet_btn = QPushButton("💾 Kaydet ve Kapat")
        kaydet_btn.clicked.connect(self.veri_kaydet)

        iptal_btn = QPushButton("İptal")
        iptal_btn.setObjectName("cancelBtn")
        iptal_btn.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(kaydet_btn)
        btn_layout.addWidget(iptal_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def veri_kaydet(self):
        try:
            seviye = int(self.giris_edit.text())
            if seviye < 20 or seviye > 500:
                raise ValueError("Kan şekeri değeri aralık dışında.")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir sayı girin (20-500 arası)")
            return

        zaman = self.datetime_edit.dateTime().toPyDateTime()
        grup = saat_araligina_gore_grup(zaman)

        if not grup:
            QMessageBox.warning(self, "Hata",
                                "Seçilen saat, geçerli bir ölçüm grubuna ait değil!\nLütfen aşağıdaki saat aralıklarını kullanın:\n\nSabah: 07:00–08:00\nÖğlen: 12:00–13:00\nİkindi: 15:00–16:00\nAkşam: 18:00–19:00\nGece: 22:00–23:00")
            return

        tarih_baslangic = datetime(zaman.year, zaman.month, zaman.day, 0, 0, 0)
        tarih_bitis = datetime(zaman.year, zaman.month, zaman.day, 23, 59, 59)

        self.cursor.execute("""
                    SELECT COUNT(*) FROM kan_sekeri
                    WHERE hasta_id = %s AND olcum_grubu = %s
                    AND tarih_zaman BETWEEN %s AND %s
                """, (self.hasta_id, grup, tarih_baslangic, tarih_bitis))
        sonuc = self.cursor.fetchone()

        if sonuc[0] > 0:
            QMessageBox.warning(self, "Uyarı", f"Aynı gün içinde {grup} için zaten bir ölçüm yapılmış.")
            return

        self.cursor.execute("""
            INSERT INTO kan_sekeri (hasta_id, tarih_zaman, kan_sekeri, olcum_grubu)
            VALUES (%s, %s, %s, %s)
        """, (self.hasta_id, zaman, seviye, grup))
        self.conn.commit()

        if not grup:
            QMessageBox.warning(self, "Uyarı", "⚠️ Bu saat dışı bir ölçümdür. Ortalamaya dahil edilmeyecek.")
        else:
            QMessageBox.information(self, "Başarılı", f"{grup.title()} ölçümü başarıyla kaydedildi.")

        self.accept()
