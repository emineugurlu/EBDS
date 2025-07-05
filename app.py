# app.py - Streamlit Uygulaması (Gelişmiş)

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

@st.cache_resource
def load_resources():
    """NLP modelini ve bilgi bankası embedding'lerini yükler veya oluşturur."""
    st.spinner("NLP modelini yüklüyor ve bilgi bankası embedding'lerini hazırlıyor...")
    if os.path.exists(EMBEDDINGS_FILE):
        st.info(f"'{EMBEDDINGS_FILE}' dosyasından bilgi bankası embedding'leri yükleniyor...")
        with open(EMBEDDINGS_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        st.info("Bilgi bankası embedding'leri oluşturuluyor... Bu biraz zaman alabilir.")
        embeddings = {
            anahtar: get_embedding(anahtar) for anahtar in KNOWLEDGE_BASE.keys()
        }
        with open(EMBEDDINGS_FILE, 'wb') as f:
            pickle.dump(embeddings, f)
        st.success(f"Bilgi bankası embedding'leri '{EMBEDDINGS_FILE}' dosyasına kaydedildi.")
        return embeddings

# Kaynakları yükle (Streamlit uygulamasının başında bir kez çalışır)
# Bu kısmı Streamlit'in kendi lifecycle'ına bırakıyoruz, ilk yüklemede gösterilecek.
bilgi_bankasi_embeddings = load_resources()

def preprocess_query(query):
    """Kullanıcı sorgusunu temizler ve küçük harfe dönüştürür."""
    query = query.lower().strip()
    query = re.sub(r'[^\w\s]', '', query)
    query = re.sub(r'\s+', ' ', query).strip()
    return query

def get_assistant_response(soru):
    """
    NLP entegrasyonu ve Web Scraping ile daha akıllı bir temel bilim asistanı.
    Streamlit uygulaması için uyarlanmıştır.
    """
    islenmis_soru = preprocess_query(soru)
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
        with st.spinner("Bilgi bankasında bulunamadı. Web'de aranıyor..."):
            web_sonuc = search_and_scrape(soru) # Web scraping için orijinal soruyu kullan

        if web_sonuc and not ("Web'den çekilen metin anlamlı değil veya çok kısa." in web_sonuc or \
                              "DuckDuckGo aramasında uygun bir bağlantı bulunamadı." in web_sonuc or \
                              "Web isteği hatası" in web_sonuc or \
                              "Web sayfasını işlerken bir sorun oluştu" in web_sonuc):
            return f"EBDS Asistanı (Web'den): {web_sonuc}"
        else:
            # Hata mesajlarını daha anlaşılır hale getir
            error_message = "Üzgünüm, bu konu hakkında henüz bilgiye sahip değilim veya yeterince ilgili bir bilgi bulamadım."
            if "Web'den çekilen metin anlamlı değil veya çok kısa." in web_sonuc:
                error_message += " (Web sayfasından yeterli bilgi alınamadı.)"
            elif "DuckDuckGo aramasında uygun bir bağlantı bulunamadı." in web_sonuc:
                error_message += " (Web aramasında uygun bir kaynak bulunamadı.)"
            elif "Web isteği hatası" in web_sonuc:
                error_message += " (İnternet bağlantınızda veya erişimde bir sorun oluştu.)"
            elif "Web sayfasını işlerken bir sorun oluştu" in web_sonuc:
                error_message += " (Web sayfasını işlerken teknik bir sorun yaşandı.)"
            return f"EBDS Asistanı: {error_message}"


# --- Streamlit Arayüzü ---
st.set_page_config(page_title="EBDS Temel Bilim Asistanı", page_icon=":brain:", layout="wide")

st.title("🔬 EBDS Temel Bilim Asistanı")
st.markdown("Temel bilimler alanındaki sorularınıza yanıt bulmak için buradayım!")

# Sohbet geçmişini başlat (Streamlit session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sohbet geçmişini görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan soru alma
if kullanici_sorusu := st.chat_input("Sorunuzu buraya yazın..."):
    # Kullanıcı mesajını geçmişe ekle ve göster
    st.session_state.messages.append({"role": "user", "content": kullanici_sorusu})
    with st.chat_message("user"):
        st.markdown(kullanici_sorusu)

    # Asistan yanıtını al ve göster
    with st.chat_message("assistant"):
        with st.spinner("Yanıt aranıyor..."):
            response = get_assistant_response(kullanici_sorusu)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")
st.markdown("Bu asistan, 'insanlık için büyük bir proje' vizyonuyla geliştirilmiştir.")