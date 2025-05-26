import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QListWidget, QVBoxLayout, QWidget,
    QPushButton, QMessageBox, QSizePolicy, QHBoxLayout, QGridLayout,
    QFrame, QScrollArea, QSpacerItem
)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette
from PyQt5.QtCore import Qt
from veritabani import baglanti_kur
from ekranlar.doktor.doktor_hasta_ekle import HastaEklemeEkrani
from ekranlar.moduller.kan_sekeri_ekle import KanSekeriGirisEkrani
from ekranlar.moduller.egzersiz_ekle import EgzersizGirisPenceresi
from ekranlar.moduller.diyet_ekle import DiyetGirisPenceresi
from ekranlar.moduller.kan_sekeri_grafik import KanSekeriGrafik
from PyQt5.QtWidgets import QInputDialog, QLineEdit
import hashlib


class DoktorAnaEkran(QMainWindow):
    def __init__(self, doktor_id):
        super().__init__()
        self.doktor_id = doktor_id
        self.setWindowTitle("Doktor Ana Ekran")
        self.setWindowIcon(QIcon("assets/enabiz_logo.png"))
        self.setGeometry(200, 50, 1200, 800)
        self.setMinimumSize(1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.create_sidebar()

        self.create_main_content()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        self.doktor_bilgilerini_yukle()

    def create_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
            }
        """)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(20)
        self.sidebar.setLayout(sidebar_layout)

        title_label = QLabel("Doktor Panel")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 10px 0;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title_label)

        self.create_profile_card(sidebar_layout)

        self.create_navigation_menu(sidebar_layout)

        sidebar_layout.addStretch()

        logout_btn = QPushButton("🚪 Çıkış Yap")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        sidebar_layout.addWidget(logout_btn)

        self.main_layout.addWidget(self.sidebar)

    def create_profile_card(self, layout):
        profile_card = QFrame()
        profile_card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 15px;
            }
        """)

        profile_layout = QVBoxLayout()
        profile_layout.setSpacing(8)
        profile_card.setLayout(profile_layout)

        self.lbl_resim = QLabel()
        self.lbl_resim.setFixedSize(80, 80)
        self.lbl_resim.setStyleSheet("""
            QLabel {
                border: 3px solid white;
                border-radius: 40px;
                background-color: white;
            }
        """)
        self.lbl_resim.setAlignment(Qt.AlignCenter)
        self.lbl_resim.setText("👨‍⚕️")
        self.lbl_resim.setStyleSheet(self.lbl_resim.styleSheet() + "font-size: 40px;")

        self.lbl_ad = QLabel("Dr. Doktor Adı")
        self.lbl_email = QLabel("email@example.com")
        self.lbl_uzmanlik = QLabel("Uzmanlık Alanı")

        for lbl in [self.lbl_ad, self.lbl_email, self.lbl_uzmanlik]:
            lbl.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 12px;
                    font-weight: 500;
                }
            """)
            lbl.setAlignment(Qt.AlignCenter)

        self.lbl_ad.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        profile_layout.addWidget(self.lbl_resim, alignment=Qt.AlignCenter)
        profile_layout.addWidget(self.lbl_ad)
        profile_layout.addWidget(self.lbl_email)
        profile_layout.addWidget(self.lbl_uzmanlik)

        layout.addWidget(profile_card)

    def create_navigation_menu(self, layout):
        nav_title = QLabel("Menü")
        nav_title.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                font-weight: 600;
                margin-top: 10px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(nav_title)

        menu_items = [
            ("👥", "Hastalarım", self.show_patients_tab),
            ("🔐", "Şifre Değiştir", self.sifre_degistir)
        ]

        for icon, text, callback in menu_items:
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    padding: 12px 15px;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

    def create_main_content(self):
        self.content_area = QFrame()
        self.content_area.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border: none;
            }
        """)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        self.content_area.setLayout(self.content_layout)

        self.create_header()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(25)
        scroll_content.setLayout(self.scroll_layout)

        scroll.setWidget(scroll_content)
        self.content_layout.addWidget(scroll)

        self.main_layout.addWidget(self.content_area)

    def create_header(self):
        header_layout = QHBoxLayout()

        title = QLabel("Hoşgeldiniz")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2d3748;
            }
        """)

        from datetime import datetime
        date_label = QLabel(datetime.now().strftime("%d %B %Y"))
        date_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #718096;
            }
        """)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(date_label)

        self.content_layout.addLayout(header_layout)

    def create_patients_section(self):
        patients_title = QLabel("Hastalarınız")
        patients_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 10px;
            }
        """)
        self.scroll_layout.addWidget(patients_title)

        patients_card = QFrame()
        patients_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)

        patients_layout = QVBoxLayout()
        patients_layout.setContentsMargins(20, 20, 20, 20)
        patients_card.setLayout(patients_layout)

        self.hasta_listesi = QListWidget()
        self.hasta_listesi.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                font-size: 14px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
                border-radius: 6px;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background-color: #f7fafc;
            }
            QListWidget::item:selected {
                background-color: #e6fffa;
                color: #2d3748;
            }
        """)
        self.hasta_listesi.setMinimumHeight(200)
        patients_layout.addWidget(self.hasta_listesi)

        self.scroll_layout.addWidget(patients_card)

        self.create_action_buttons()

    def create_action_buttons(self):
        actions_title = QLabel("Hasta İşlemleri")
        actions_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 10px;
            }
        """)
        self.scroll_layout.addWidget(actions_title)

        buttons_grid = QGridLayout()
        buttons_grid.setSpacing(15)

        button_configs = [
            ("👤", "Yeni Hasta Ekle", "#48bb78", self.hasta_ekle_ekranini_ac),
            ("🩸", "Kan Şekeri Ekle", "#ed8936", self.kan_sekeri_ekle_ekranini_ac),
            ("🤸", "Egzersiz Planı", "#4299e1", self.egzersiz_ekle_ekranini_ac),
            ("🥗", "Diyet Planı", "#38b2ac", self.diyet_ekle_ekranini_ac),
            ("📈", "Grafik Görüntüle", "#9f7aea", self.kan_sekeri_grafik_ac),
            ("📋", "Hasta Detayları", "#667eea", self.hasta_detay_goster),
            ("🩺", "Hastalık Teşhisi", "#f56565", self.hastalik_teshisi_ekranini_ac),
            ("💾", "Arşiv Görüntüle", "#718096", self.arsiv_goruntule_ekranini_ac)
        ]

        for i, (icon, text, color, callback) in enumerate(button_configs):
            btn = self.create_action_button(icon, text, color, callback)
            row = i // 4
            col = i % 4
            buttons_grid.addWidget(btn, row, col)

        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_grid)
        self.scroll_layout.addWidget(buttons_widget)

    def create_action_button(self, icon, text, color, callback):
        btn = QPushButton()
        btn.setFixedHeight(120)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.8)};
            }}
        """)

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(text)
        text_label.setStyleSheet("""
            font-size: 12px;
            font-weight: 600;
            color: white;
        """)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)

        btn_widget = QWidget()
        btn_widget.setLayout(btn_layout)
        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)

        btn.clicked.connect(callback)
        btn.setText(f"{icon}\n{text}")

        return btn

    def darken_color(self, hex_color, factor=0.9):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    def show_patients_tab(self):
        self.clear_scroll_content()
        self.create_patients_section()
        self.hastalari_getir()

    def clear_scroll_content(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def doktor_bilgilerini_yukle(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ad, soyad, email, uzmanlik_alani, profil_resmi
                FROM doktorlar
                WHERE id = %s
            """, (self.doktor_id,))
            doktor = cursor.fetchone()
            if doktor:
                ad, soyad, email, uzmanlik, resim = doktor
                self.lbl_ad.setText(f"Dr. {ad} {soyad}")
                self.lbl_email.setText(email)
                self.lbl_uzmanlik.setText(uzmanlik)

                if resim:
                    pixmap = QPixmap()
                    pixmap.loadFromData(resim)
                    self.lbl_resim.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Doktor bilgileri alınamadı:\n{e}")

    def hastalari_getir(self):
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            query = "SELECT id, ad, soyad FROM hastalar WHERE doktor_id = %s"
            cursor.execute(query, (self.doktor_id,))
            hastalar = cursor.fetchall()
            self.hasta_listesi.clear()
            for hasta_id, ad, soyad in hastalar:
                self.hasta_listesi.addItem(f"{hasta_id} - {ad} {soyad}")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def hasta_detay_goster(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tarih_zaman, kan_sekeri FROM kan_sekeri
                WHERE hasta_id = %s ORDER BY tarih_zaman DESC LIMIT 10
            """, (hasta_id,))
            veriler = cursor.fetchall()
            cursor.close()
            conn.close()

            if veriler:
                mesaj = "Son Kan Şekeri Verileri:\n\n"
                for i, (tarih, seviye) in enumerate(veriler, 1):
                    mesaj += f"{i}. {tarih.strftime('%d.%m.%Y %H:%M')} - {seviye} mg/dL\n"
                QMessageBox.information(self, "Hasta Detayları", mesaj)
            else:
                QMessageBox.information(self, "Bilgi", "Bu hasta için henüz veri bulunmuyor.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def hasta_ekle_ekranini_ac(self):
        self.hasta_ekle_ekrani = HastaEklemeEkrani(self.doktor_id)
        self.hasta_ekle_ekrani.show()

    def kan_sekeri_ekle_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.kan_sekeri_ekle_ekrani = KanSekeriGirisEkrani(hasta_id, baglanti_kur())
        self.kan_sekeri_ekle_ekrani.show()

    def egzersiz_ekle_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.egzersiz_ekrani = EgzersizGirisPenceresi(hasta_id,baglanti_kur())
        self.egzersiz_ekrani.show()

    def diyet_ekle_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.diyet_ekrani = DiyetGirisPenceresi(hasta_id,baglanti_kur())
        self.diyet_ekrani.show()

    def kan_sekeri_grafik_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        self.grafik_pencere = KanSekeriGrafik(hasta_id)
        self.grafik_pencere.show()

    def hastalik_teshisi_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        from ekranlar.doktor.hastalik_teshisi import HastalikTeshisiEkrani
        self.teshis_pencere = HastalikTeshisiEkrani(hasta_id)
        self.teshis_pencere.show()

    def arsiv_goruntule_ekranini_ac(self):
        if not self.hasta_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçiniz!")
            return
        hasta_id = int(self.hasta_listesi.currentItem().text().split(" - ")[0])
        from ekranlar.doktor.arsiv_goruntule import ArsivEkrani
        self.arsiv_pencere = ArsivEkrani(hasta_id)
        self.arsiv_pencere.show()

    def sifre_degistir(self):
        yeni_sifre, ok = QInputDialog.getText(self, "Şifre Güncelle", "Yeni şifrenizi girin:", QLineEdit.Password)
        if ok and yeni_sifre:
            try:
                hashed = hashlib.sha256(yeni_sifre.encode()).digest()
                conn = baglanti_kur()
                cursor = conn.cursor()
                cursor.execute("UPDATE doktorlar SET sifre = %s WHERE id = %s", (hashed, self.doktor_id))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Başarılı", "Şifreniz başarıyla güncellendi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Şifre güncellenemedi:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    doktor_ekran = DoktorAnaEkran(doktor_id=1)
    doktor_ekran.show()
    sys.exit(app.exec())