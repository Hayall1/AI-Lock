import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# ==== Firebase bağlantısı ====
if not firebase_admin._apps:
    cred = credentials.Certificate("ai-lock-8a369-firebase-adminsdk-fbsvc-18651bfe3b.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ai-lock-8a369-default-rtdb.firebaseio.com/'
    })

# ==== Oturum durumu ====
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False

# ==== Giriş ekranı ====
def show_giris_ekrani():
    st.image("logo.jpeg", use_container_width=True)
    st.header("AI Lock - Kapı Güvenlik Sistemi")
    if st.button("Devam Et"):
        st.session_state.giris_yapildi = True
        st.rerun()

# ==== Kapı durumu ekranı ====
def show_durum_paneli():
    st.subheader("🔒 Kapı Durumu")

    try:
        durum_ref = db.reference("/kilitDurumu")
        durum = durum_ref.get()

        if durum == "acik":
            st.success("Kapı şu anda: AÇIK")
        elif durum == "kilitli":
            st.error("Kapı şu anda: KİLİTLİ")
        else:
            st.warning("Kapı durumu bilinmiyor.")  # Eğer başka bir veri varsa
    except Exception as e:
        st.error(f"Firebase bağlantı hatası: {e}")

# ==== Kontrol ekranı (örnek) ====
def show_kontrol_paneli():
    st.subheader("Kapı Kontrolü")

    if st.button("Kapıyı Aç"):
        db.reference("/komutlar/manuelKomut").set("ac")
        st.success("Komut gönderildi: Aç")

    if st.button("Kapıyı Kilitle"):
        db.reference("/komutlar/manuelKomut").set("kapat")
        st.success("Komut gönderildi: Kilitle")

# ==== Kayıt ekranı (örnek) ====
def show_kayit_ekrani():
    st.subheader("Kullanıcı Kaydı")
    isim = st.text_input("İsim Soyisim")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Kaydı Tamamla"):
        if isim and sifre:
            st.success(f"Kayıt başarılı: {isim}")
        else:
            st.warning("Lütfen tüm alanları doldurun.")

# ==== Ana uygulama ====
if not st.session_state.giris_yapildi:
    show_giris_ekrani()
else:
    secim = st.sidebar.selectbox("Sayfa Seç", ["Durum Paneli", "Kontrol Paneli", "Kayıt Ekranı"])

    if secim == "Durum Paneli":
        show_durum_paneli()
    elif secim == "Kontrol Paneli":
        show_kontrol_paneli()
    elif secim == "Kayıt Ekranı":
        show_kayit_ekrani()
