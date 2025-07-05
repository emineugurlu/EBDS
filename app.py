# app.py - Streamlit Uygulaması

import streamlit as st
from nlp_model import get_embedding
from web_scraper import search_and_scrape
from knowledge_base import KNOWLEDGE_BASE
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os
import re

EMBEDDINGS_FILE = "embeddings.pkl"

@st.cache_resource # Modeli ve embedding'leri bir kez yüklemek için
def load_resources():
    """NLP modelini ve bilgi bankası embedding'lerini yükler veya oluşturur."""
    # NLP modeli nlp_model.py içinde zaten tek seferlik yüklendiği için
    # burada tekrar bir yükleme fonksiyonu çağırmaya gerek yok,
    # get_embedding çağrıldığında zaten yüklü olacaktır.

    if os.path.exists(EMBEDDINGS_FILE):
        st.write(f"'{EMBEDDINGS_FILE}' dosyasından bilgi bankası embedding'leri yükleniyor...")
        with open(EMBEDDINGS_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        st.write("Bilgi bankası embedding'leri oluşturuluyor...")
        embeddings = {
            anahtar: get_embedding(anahtar) for anahtar in KNOWLEDGE_BASE.keys()
        }
        with open(EMBEDDINGS_FILE, 'wb') as f:
            pickle.dump(embeddings, f)
        st.write(f"Bilgi bankası embedding'leri '{EMBEDDINGS_FILE}' dosyasına kaydedildi.")
        return embeddings

# Kaynakları yükle (Streamlit uygulamasının başında bir kez çalışır)
bilgi_bankasi_embeddings = load_resources()

def preprocess_query(query):
    """Kullanıcı sorgusunu temizler ve küçük harfe dönüştürür."""
    query = query.lower().strip()
    query = re.sub(r'[^\w\s]', '', query)
    query = re.sub(r'\s+', ' ', query).strip()
    return query

def temel_bilim_asistani(soru):
    """
    NLP entegrasyonu ve Web Scraping ile daha akıllı bir temel bilim asistanı.
    Streamlit uygulaması için uyarlanmıştır.
    """
    # "çıkış" komutu Streamlit arayüzünde doğrudan kontrol edilmeyecek,
    # uygulama kapatıldığında veya tarayıcı sekmesi kapatıldığında durur.

    islenmis_soru = preprocess_query(soru) # Bilgi bankası eşleşmesi için işlenmiş sorgu
    soru_embedding = get_embedding(islenmis_soru)

    en_yuksek_benzerlik = -1
    en_benzer_anahtar = None

    for anahtar, embedding in bilgi_bankasi_embeddings.items():
        benzerlik = cosine_similarity(soru_embedding.reshape(1, -1), embedding.reshape(1, -1))[0][0]
        if benzerlik > en_yuksek_benzerlik:
            en_yuksek_benzerlik = benzerlik
            en_benzer_anahtar = anahtar

    if en_yuksek_benzerlik > 0.65: # Eşik değeri
        return f"EBDS Asistanı: {KNOWLEDGE_BASE[en_benzer_anahtar]}"
    else:
        st.write("Bilgi bankasında bulunamadı. Web'de aranıyor...")
        web_sonuc = search_and_scrape(soru)

        if web_sonuc and not ("Web'den çekilen metin anlamlı değil veya çok kısa." in web_sonuc or \
                              "DuckDuckGo aramasında uygun bir bağlantı bulunamadı." in web_sonuc or \
                              "Web isteği hatası" in web_sonuc or \
                              "Web sayfasını işlerken bir sorun oluştu" in web_sonuc):
            return f"EBDS Asistanı (Web'den): {web_sonuc}"
        else:
            return f"EBDS Asistanı: Üzgünüm, bu konu hakkında henüz bilgiye sahip değilim veya yeterince ilgili bir bilgi bulamadım. ({web_sonuc})"


# --- Streamlit Arayüzü ---
st.set_page_config(page_title="EBDS Temel Bilim Asistanı", page_icon=":brain:")

st.title("🔬 EBDS Temel Bilim Asistanı")
st.markdown("Temel bilimler alanındaki sorularınıza yanıt bulmak için buradayım!")

# Kullanıcıdan soru alma
kullanici_sorusu = st.text_input("Sorunuzu buraya yazın:", key="user_input")

if kullanici_sorusu:
    with st.spinner("Yanıt aranıyor..."): # Kullanıcıya arama yapıldığını göster
        cevap = temel_bilim_asistani(kullanici_sorusu)
        st.info(cevap) # Yanıtı bilgi kutusunda göster

st.markdown("---")
st.markdown("Bu asistan, 'insanlık için büyük bir proje' vizyonuyla geliştirilmiştir.")