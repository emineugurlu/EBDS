# main.py - Modüler Yapı

# Diğer modüllerden gerekli fonksiyonları içe aktaralım
from nlp_model import get_embedding # nlp_model.py dosyasından get_embedding fonksiyonunu import et
from web_scraper import search_and_scrape # web_scraper.py dosyasından search_and_scrape fonksiyonunu import et
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def temel_bilim_asistani(soru):
    """
    NLP entegrasyonu ve Web Scraping ile daha akıllı bir temel bilim asistanı.
    """
    bilgi_bankasi_raw = {
        "fotosentez nedir": "Fotosentez, bitkilerin güneş ışığını kullanarak karbondioksit ve suyu glikoza (şeker) ve oksijene dönüştürdüğü biyolojik bir süreçtir.",
        "yerçekimi nedir": "Yerçekimi, kütlesi olan cisimlerin birbirini çekmesini sağlayan temel bir kuvvettir. Isaac Newton tarafından tanımlanmıştır.",
        "atom nedir": "Atom, maddenin temel yapı taşıdır. Çekirdek (proton ve nötronlar) ve etrafında dönen elektronlardan oluşur.",
        "dna nedir": "DNA (Deoksiribonükleik asit), canlı organizmaların genetik bilgisini taşıyan bir moleküldür. İkili sarmal yapısındadır.",
        "karadelik nedir": "Karadelik, uzayda yerçekiminin o kadar güçlü olduğu bir bölgedir ki, hiçbir parçacık veya elektromanyetik radyasyon (ışık dahil) oradan kaçamaz.",
        "ışık hızı kaçtır": "Işık hızı boşlukta yaklaşık saniyede 299,792,458 metredir.",
        "evrim nedir": "Evrim, canlı popülasyonlarının nesiller boyunca genetik özelliklerinde meydana gelen değişikliklerdir. Doğal seçilim bu süreci yönlendiren önemli bir faktördür.",
        "su formülü": "Su molekülünün kimyasal formülü H2O'dur. Bir oksijen ve iki hidrojen atomundan oluşur.",
        "dünyanın en büyük okyanusu": "Dünya'nın en büyük okyanusu Pasifik Okyanusu'dur.",
        "güneş sistemindeki gezegenler": "Güneş sistemindeki gezegenler şunlardır: Merkür, Venüs, Dünya, Mars, Jüpiter, Satürn, Uranüs ve Neptün.",
        "pi sayısı nedir": "Pi ($ \\pi $) sayısı, bir dairenin çevresinin çapına oranıdır ve yaklaşık olarak 3.14159'dur.",
        "en küçük canlı birim": "Canlıların temel yapısal ve işlevsel birimi hücredir.",
        "dna hakkında bilgi": "DNA (Deoksiribonükleik asit), canlı organizmaların genetik bilgisini taşıyan bir moleküldür. İkili sarmal yapısındadır.",
        "DNA nedir hakkında": "DNA (Deoksiribonükleik asit), canlı organizmaların genetik bilgisini taşıyan bir moleküldür. İkili sarmal yapısındadır.",
        "dna ne işe yarar": "DNA, canlı organizmaların genetik bilgisini taşır ve protein sentezi gibi hücresel süreçlerde rol oynar.",
        "gezegenler nelerdir": "Güneş sistemindeki gezegenler şunlardır: Merkür, Venüs, Dünya, Mars, Jüpiter, Satürn, Uranüs ve Neptün.",
        "ışık hızı kaç metre": "Işık hızı boşlukta yaklaşık saniyede 299,792,458 metredir.",
        "kütle çekim nedir": "Yerçekimi, kütlesi olan cisimlerin birbirini çekmesini sağlayan temel bir kuvvettir. Isaac Newton tarafından tanımlanmıştır."
    }

    # Bilgi bankası anahtarlarını ve değerlerini gömülülerine dönüştürelim
    # Bu işlem artık her çağrıda değil, uygulamanın başında bir kez yapılabilir (ileride optimize ederiz)
    bilgi_bankasi_embeddings = {
        anahtar: get_embedding(anahtar) for anahtar in bilgi_bankasi_raw.keys()
    }

    islenmis_soru = soru.lower().strip()
    soru_embedding = get_embedding(islenmis_soru)

    en_yuksek_benzerlik = -1
    en_benzer_anahtar = None

    for anahtar, embedding in bilgi_bankasi_embeddings.items():
        benzerlik = cosine_similarity(soru_embedding.reshape(1, -1), embedding.reshape(1, -1))[0][0]
        if benzerlik > 0.65: # Eşik değeri
            en_yuksek_benzerlik = benzerlik
            en_benzer_anahtar = anahtar
            break # Eşiği geçen ilk eşleşmeyi alabiliriz

    # Bilgi bankası içinde en yüksek benzerlik skoru eşiğin üzerindeyse
    if en_benzer_anahtar and en_yuksek_benzerlik > 0.65:
        return f"EBDS Asistanı: {bilgi_bankasi_raw[en_benzer_anahtar]}"
    else:
        # Bilgi bankasında bulunamazsa web'den aramayı dene
        print("Bilgi bankasında bulunamadı. Web'de aranıyor...")
        web_cevap = search_and_scrape(soru) # Orijinal soruyu kullan
        # Eğer web_cevap uygun ve hata mesajı değilse
        if web_cevap and not ("Belirtilen bağlantıdan anlamlı bir metin çekilemedi." in web_cevap or \
                              "DuckDuckGo aramasında uygun bir bağlantı bulunamadı." in web_cevap or \
                              "Web'den bilgi çekerken bir sorun oluştu." in web_cevap or \
                              "Web sayfasını işlerken bir sorun oluştu." in web_cevap):
            return f"EBDS Asistanı (Web'den): {web_cevap}"
        else:
            return "EBDS Asistanı: Üzgünüm, bu konu hakkında henüz bilgiye sahip değilim veya yeterince ilgili bir bilgi bulamadım."

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