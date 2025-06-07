# main.py - Hızlı Başlangıç için Embedding Kaydetme/Yükleme

from nlp_model import get_embedding
from web_scraper import search_and_scrape
from knowledge_base import KNOWLEDGE_BASE
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os

EMBEDDINGS_FILE = "embeddings.pkl"

def load_or_create_embeddings():
    if os.path.exists(EMBEDDINGS_FILE):
        print(f"'{EMBEDDINGS_FILE}' dosyasından bilgi bankası embedding'leri yükleniyor...")
        with open(EMBEDDINGS_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        print("Bilgi bankası embedding'leri oluşturuluyor...")
        embeddings = {
            anahtar: get_embedding(anahtar) for anahtar in KNOWLEDGE_BASE.keys()
        }
        with open(EMBEDDINGS_FILE, 'wb') as f:
            pickle.dump(embeddings, f)
        print(f"Bilgi bankası embedding'leri '{EMBEDDINGS_FILE}' dosyasına kaydedildi.")
        return embeddings

# NLP modelini ve bilgi bankası embedding'lerini program başlangıcında bir kez yükle
bilgi_bankasi_embeddings = load_or_create_embeddings()

def temel_bilim_asistani(soru):
    """
    NLP entegrasyonu ve Web Scraping ile daha akıllı bir temel bilim asistanı.
    """
    islenmis_soru = soru.lower().strip()
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
        # Bilgi bankasında bulunamazsa web'den aramayı dene
        print("Bilgi bankasında bulunamadı. Web'de aranıyor...")
        web_sonuc = search_and_scrape(soru) # Orijinal soruyu kullan

        if web_sonuc and not ("Web'den çekilen metin anlamlı değil veya çok kısa." in web_sonuc or \
                              "DuckDuckGo aramasında uygun bir bağlantı bulunamadı." in web_sonuc or \
                              "Web isteği hatası" in web_sonuc or \
                              "Web sayfasını işlerken bir sorun oluştu" in web_sonuc):
            return f"EBDS Asistanı (Web'den): {web_sonuc}"
        else:
            return f"EBDS Asistanı: Üzgünüm, bu konu hakkında henüz bilgiye sahip değilim veya yeterince ilgili bir bilgi bulamadım. ({web_sonuc})" # Hata mesajını da gösterebiliriz.

# Kullanıcı ile etkileşim döngüsü
print("EBDS Temel Bilim Asistanı'na hoş geldiniz!")
print("Çıkmak için 'çıkış' yazabilirsiniz.")

while True:
    kullanici_sorusu = input("Sorunuz: ")
    if kullanici_sorusu.lower() == "çıkış":
        print("EBDS Asistanı: Güle güle!")
        break
    else:
        cevap = temel_bilim_asistani(kullanici_sorusu)
        print(cevap)