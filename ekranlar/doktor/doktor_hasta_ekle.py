from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QMessageBox, QWidget,
                             QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog, QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QIcon
from veritabani import baglanti_kur
from hashleme import hashle
import datetime
import secrets
import smtplib
from email.mime.text import MIMEText


class HastaEklemeEkrani(QWidget):
    def __init__(self, doktor_id):
        super().__init__()
        self.doktor_id = doktor_id
        self.profil_resmi_yolu = None
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.setWindowTitle("🏥 Yeni Hasta Kayıt Sistemi")
        self.setGeometry(300, 200, 500, 650)
        self.setFixedSize(550, 700)

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        self.create_header(main_layout)

        # Form container
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 30, 40, 30)

        # Form alanları
        self.create_form_fields(form_layout)

        # Buton alanı
        self.create_buttons(form_layout)

        main_layout.addWidget(form_container)
        self.setLayout(main_layout)

    def create_header(self, layout):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(80)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)

        # Başlık
        title = QLabel("👤 Yeni Hasta Kaydı")
        title.setObjectName("headerTitle")
        title.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        layout.addWidget(header)

    def create_form_fields(self, layout):
        # TC Kimlik
        self.create_form_group("👤 TC Kimlik Numarası", "tc", "11 haneli TC kimlik numaranızı giriniz", layout)

        # Ad Soyad (yan yana)
        name_layout = QHBoxLayout()
        name_layout.setSpacing(15)

        # Ad
        ad_container = QFrame()
        ad_layout = QVBoxLayout(ad_container)
        ad_layout.setContentsMargins(0, 0, 0, 0)
        ad_layout.setSpacing(8)

        lbl_ad = QLabel("📝 Ad")
        lbl_ad.setObjectName("fieldLabel")
        self.txt_ad = QLineEdit()
        self.txt_ad.setObjectName("inputField")
        self.txt_ad.setPlaceholderText("Adınızı giriniz")

        ad_layout.addWidget(lbl_ad)
        ad_layout.addWidget(self.txt_ad)

        # Soyad
        soyad_container = QFrame()
        soyad_layout = QVBoxLayout(soyad_container)
        soyad_layout.setContentsMargins(0, 0, 0, 0)
        soyad_layout.setSpacing(8)

        lbl_soyad = QLabel("📝 Soyad")
        lbl_soyad.setObjectName("fieldLabel")
        self.txt_soyad = QLineEdit()
        self.txt_soyad.setObjectName("inputField")
        self.txt_soyad.setPlaceholderText("Soyadınızı giriniz")

        soyad_layout.addWidget(lbl_soyad)
        soyad_layout.addWidget(self.txt_soyad)

        name_layout.addWidget(ad_container)
        name_layout.addWidget(soyad_container)
        layout.addLayout(name_layout)

        # Email
        self.create_form_group("📧 E-posta Adresi", "email", "ornek@email.com", layout)

        # Doğum Tarihi ve Cinsiyet (yan yana)
        birth_gender_layout = QHBoxLayout()
        birth_gender_layout.setSpacing(15)

        # Doğum Tarihi
        birth_container = QFrame()
        birth_layout = QVBoxLayout(birth_container)
        birth_layout.setContentsMargins(0, 0, 0, 0)
        birth_layout.setSpacing(8)

        lbl_dogum = QLabel("📅 Doğum Tarihi")
        lbl_dogum.setObjectName("fieldLabel")
        self.txt_dogum_tarihi = QLineEdit()
        self.txt_dogum_tarihi.setObjectName("inputField")
        self.txt_dogum_tarihi.setPlaceholderText("YYYY-MM-DD")

        birth_layout.addWidget(lbl_dogum)
        birth_layout.addWidget(self.txt_dogum_tarihi)

        # Cinsiyet
        gender_container = QFrame()
        gender_layout = QVBoxLayout(gender_container)
        gender_layout.setContentsMargins(0, 0, 0, 0)
        gender_layout.setSpacing(8)

        lbl_cinsiyet = QLabel("⚥ Cinsiyet")
        lbl_cinsiyet.setObjectName("fieldLabel")
        self.cmb_cinsiyet = QComboBox()
        self.cmb_cinsiyet.setObjectName("comboBox")
        self.cmb_cinsiyet.addItems(["Erkek", "Kadın", "Diğer"])

        gender_layout.addWidget(lbl_cinsiyet)
        gender_layout.addWidget(self.cmb_cinsiyet)

        birth_gender_layout.addWidget(birth_container)
        birth_gender_layout.addWidget(gender_container)
        layout.addLayout(birth_gender_layout)

        # Profil Resmi
        self.create_file_selector(layout)

    def create_form_group(self, label_text, field_name, placeholder, layout):
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)

        label = QLabel(label_text)
        label.setObjectName("fieldLabel")

        field = QLineEdit()
        field.setObjectName("inputField")
        field.setPlaceholderText(placeholder)

        # Field'ı instance variable olarak sakla
        setattr(self, f"txt_{field_name}", field)

        container_layout.addWidget(label)
        container_layout.addWidget(field)
        layout.addWidget(container)

    def create_file_selector(self, layout):
        file_container = QFrame()
        file_layout = QVBoxLayout(file_container)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.setSpacing(8)

        self.lbl_resim = QLabel("🖼️ Profil Resmi (İsteğe Bağlı)")
        self.lbl_resim.setObjectName("fieldLabel")

        self.btn_resim_sec = QPushButton("📁 Dosya Seç")
        self.btn_resim_sec.setObjectName("fileButton")
        self.btn_resim_sec.clicked.connect(self.profil_resmi_sec)

        file_layout.addWidget(self.lbl_resim)
        file_layout.addWidget(self.btn_resim_sec)
        layout.addWidget(file_container)

    def create_buttons(self, layout):
        # Spacer
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buton container
        button_container = QFrame()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Ana buton
        self.btn_ekle = QPushButton("✅ Hastayı Kaydet")
        self.btn_ekle.setObjectName("primaryButton")
        self.btn_ekle.clicked.connect(self.hasta_ekle)

        button_layout.addWidget(self.btn_ekle)
        layout.addWidget(button_container)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            #header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
                border-radius: 0px;
            }

            #headerTitle {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
            }

            #formContainer {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e9ecef;
                margin: 20px;
            }

            #fieldLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 5px;
            }

            #inputField {
                padding: 12px 15px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 14px;
                background-color: #ffffff;
                min-height: 20px;
            }

            #inputField:focus {
                border-color: #667eea;
                outline: none;
                background-color: #f8f9ff;
            }

            #inputField:hover {
                border-color: #adb5bd;
            }

            #comboBox {
                padding: 12px 15px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                min-height: 20px;
            }

            #comboBox:focus {
                border-color: #667eea;
                outline: none;
            }

            #comboBox:hover {
                border-color: #adb5bd;
            }

            #comboBox::drop-down {
                border: none;
                width: 30px;
            }

            #comboBox::down-arrow {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMuNSA1LjI1TDcgOC43NUwxMC41IDUuMjUiIHN0cm9rZT0iIzY2N2VlYSIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
                width: 14px;
                height: 14px;
            }

            #fileButton {
                padding: 12px 20px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                min-height: 20px;
            }

            #fileButton:hover {
                background-color: #5a6268;
                transform: translateY(-1px);
            }

            #fileButton:pressed {
                background-color: #545b62;
                transform: translateY(0px);
            }

            #primaryButton {
                padding: 15px 30px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 180px;
                min-height: 25px;
            }

            #primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1);
                transform: translateY(-2px);
            }

            #primaryButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c51bf, stop:1 #553c9a);
                transform: translateY(0px);
            }

            QMessageBox {
                background-color: white;
                color: #212529;
            }

            QMessageBox QPushButton {
                padding: 8px 16px;
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: 600;
                min-width: 80px;
            }

            QMessageBox QPushButton:hover {
                background-color: #5a67d8;
            }
        """)

    def profil_resmi_sec(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(
            self,
            "Profil Resmi Seç",
            "",
            "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if dosya_yolu:
            self.profil_resmi_yolu = dosya_yolu
            dosya_adi = dosya_yolu.split('/')[-1]
            self.lbl_resim.setText(f"🖼️ Seçilen: {dosya_adi}")
            self.btn_resim_sec.setText("✓ Seçildi")

    def rastgele_sifre_olustur(self, uzunluk=10):
        return secrets.token_urlsafe(uzunluk)

    def sifreyi_eposta_ile_gonder(self, alici_email, tc, sifre):
        try:
            mesaj = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #667eea; text-align: center;">🏥 Diyabet Takip Sistemi</h2>
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #495057;">Sayın Kullanıcımız,</h3>
                        <p>Diyabet Takip Sistemi'ne başarıyla kaydınız oluşturulmuştur. Giriş bilgileriniz aşağıdadır:</p>

                        <div style="background-color: white; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
                            <p><strong>👤 Kullanıcı Adı (TC):</strong> {tc}</p>
                            <p><strong>🔐 Şifre:</strong> {sifre}</p>
                        </div>

                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #ffc107;">
                            <p><strong>⚠️ Önemli:</strong> Güvenliğiniz için sistemimize ilk giriş yaptıktan sonra şifrenizi mutlaka değiştiriniz.</p>
                        </div>

                        <p style="margin-top: 20px;">Sağlıklı günler dileriz.</p>
                        <p style="color: #6c757d; font-style: italic;">Diyabet Takip Sistemi Ekibi</p>
                    </div>
                </div>
            </body>
            </html>
            """
            msg = MIMEText(mesaj, 'html', 'utf-8')
            msg['Subject'] = "🏥 Diyabet Takip Sistemi - Giriş Bilgileri"
            msg['From'] = "diabetestrackingsystem@gmail.com"
            msg['To'] = alici_email

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login("diabetestrackingsystem@gmail.com", "rowg rgfa iago dzdg")
            smtp.send_message(msg)
            smtp.quit()
            return True
        except Exception as e:
            print("E-posta gönderme hatası:", e)
            return False

    def hasta_ekle(self):
        # Veri toplama
        tc = self.txt_tc.text().strip()
        ad = self.txt_ad.text().strip()
        soyad = self.txt_soyad.text().strip()
        email = self.txt_email.text().strip()
        dogum_tarihi = self.txt_dogum_tarihi.text().strip()
        cinsiyet = self.cmb_cinsiyet.currentText()

        # Validasyon
        if not all([tc, ad, soyad, email, dogum_tarihi]):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("⚠️ Eksik Bilgi")
            msg.setText("Lütfen tüm zorunlu alanları doldurunuz!")
            msg.setDetailedText("TC Kimlik, Ad, Soyad, E-posta ve Doğum Tarihi alanları zorunludur.")
            msg.exec_()
            return

        # TC Kimlik kontrolü
        if len(tc) != 11 or not tc.isdigit():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("⚠️ Geçersiz TC Kimlik")
            msg.setText("TC Kimlik numarası 11 haneli olmalı ve sadece rakam içermelidir!")
            msg.exec_()
            return

        # Email format kontrolü (basit)
        if "@" not in email or "." not in email.split("@")[-1]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("⚠️ Geçersiz E-posta")
            msg.setText("Lütfen geçerli bir e-posta adresi giriniz!")
            msg.exec_()
            return

        # Tarih format kontrolü
        try:
            datetime.datetime.strptime(dogum_tarihi, "%Y-%m-%d")
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("⚠️ Geçersiz Tarih")
            msg.setText("Doğum tarihi formatı hatalı!")
            msg.setDetailedText("Lütfen YYYY-MM-DD formatında giriniz (örnek: 1990-05-15)")
            msg.exec_()
            return

        # Şifre oluştur
        sifre = self.rastgele_sifre_olustur()
        hashed_sifre = hashle(sifre)

        # Profil resmi
        profil_resmi = None
        if self.profil_resmi_yolu:
            try:
                with open(self.profil_resmi_yolu, "rb") as dosya:
                    profil_resmi = dosya.read()
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("⚠️ Dosya Hatası")
                msg.setText("Profil resmi yüklenirken bir hata oluştu!")
                msg.setDetailedText(str(e))
                msg.exec_()

        # Veritabanı işlemi
        try:
            conn = baglanti_kur()
            cursor = conn.cursor()

            # TC kontrolü
            cursor.execute("SELECT tc FROM hastalar WHERE tc = %s", (tc,))
            if cursor.fetchone():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("⚠️ Kayıt Mevcut")
                msg.setText("Bu TC Kimlik numarası ile zaten bir hasta kaydı bulunmaktadır!")
                msg.exec_()
                cursor.close()
                conn.close()
                return

            # Hasta ekleme
            query = """
                INSERT INTO hastalar 
                (tc, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, profil_resmi, doktor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                tc, ad, soyad, email, hashed_sifre, dogum_tarihi, cinsiyet,
                profil_resmi, self.doktor_id
            ))
            conn.commit()

            # E-posta gönder
            email_basarili = self.sifreyi_eposta_ile_gonder(email, tc, sifre)

            # Başarı mesajı
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("✅ Başarılı")
            if email_basarili:
                msg.setText("Hasta başarıyla kaydedildi!")
                msg.setDetailedText(f"Giriş bilgileri {email} adresine gönderildi.")
            else:
                msg.setText("Hasta kaydedildi ancak e-posta gönderilemedi!")
                msg.setDetailedText("Lütfen giriş bilgilerini hastaya manuel olarak iletin.")
            msg.exec_()

            # Formu temizle
            self.form_temizle()

            cursor.close()
            conn.close()

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("❌ Veritabanı Hatası")
            msg.setText("Hasta kaydı sırasında bir hata oluştu!")
            msg.setDetailedText(f"Hata detayı: {str(e)}")
            msg.exec_()

    def form_temizle(self):
        """Formu temizle"""
        self.txt_tc.clear()
        self.txt_ad.clear()
        self.txt_soyad.clear()
        self.txt_email.clear()
        self.txt_dogum_tarihi.clear()
        self.cmb_cinsiyet.setCurrentIndex(0)
        self.lbl_resim.setText("🖼️ Profil Resmi (İsteğe Bağlı)")
        self.btn_resim_sec.setText("📁 Dosya Seç")
        self.profil_resmi_yolu = None