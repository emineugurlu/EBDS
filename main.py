# main.py - Çıkış Komutu Düzeltmesi

from nlp_model import get_embedding
from web_scraper import search_and_scrape
from knowledge_base import KNOWLEDGE_BASE
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os
import re

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

def preprocess_query(query):
    """Kullanıcı sorgusunu temizler ve küçük harfe dönüştürür."""
    query = query.lower().strip()
    # Noktalama işaretlerini kaldır
    query = re.sub(r'[^\w\s]', '', query) # Alfanümerik karakterler ve boşluklar dışındaki her şeyi kaldır
    # Birden fazla boşluğu tek boşluğa indirge
    query = re.sub(r'\s+', ' ', query).strip()
    return query

def temel_bilim_asistani(soru):
    """
    NLP entegrasyonu ve Web Scraping ile daha akıllı bir temel bilim asistanı.
    """
    # Buradaki `soru` zaten kullanıcıdan alınan orijinal soru.
    # Web aramasını orijinal soru ile yapmamız daha doğru olabilir, çünkü preprocess_query
    # bazı önemli anahtar kelimeleri veya yapıları kaldırabilir.
    # Ancak bilgi bankası eşleşmesi için işlenmiş soruyu kullanmaya devam edeceğiz.
    
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
        # Bilgi bankasında bulunamazsa web'den aramayı dene
        print("Bilgi bankasında bulunamadı. Web'de aranıyor...")
        # Web scraping için orijinal, işlenmemiş kullanıcı sorusunu kullanıyoruz
        web_sonuc = search_and_scrape(soru) 
        
        if web_sonuc and not ("Web'den çekilen metin anlamlı değil veya çok kısa." in web_sonuc or \
                              "DuckDuckGo aramasında uygun bir bağlantı bulunamadı." in web_sonuc or \
                              "Web isteği hatası" in web_sonuc or \
                              "Web sayfasını işlerken bir sorun oluştu" in web_sonuc):
            return f"EBDS Asistanı (Web'den): {web_sonuc}"
        else:
            return f"EBDS Asistanı: Üzgünüm, bu konu hakkında henüz bilgiye sahip değilim veya yeterince ilgili bir bilgi bulamadım. ({web_sonuc})"

# Kullanıcı ile etkileşim döngüsü
print("EBDS Temel Bilim Asistanı'na hoş geldiniz!")
print("Çıkmak için 'çıkış' yazabilirsiniz.")

while True:
    kullanici_sorusu = input("Sorunuz: ")
    
    # Çıkış kontrolünü en başta yapıyoruz, böylece diğer işlemlere gitmez
    if kullanici_sorusu.lower().strip() == "çıkış":
        print("EBDS Asistanı: Güle güle!")
        break
    else:
        cevap = temel_bilim_asistani(kullanici_sorusu)
        print(cevap)