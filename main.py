# main.py dosyanızın içeriği - NLP Entegrasyonu ile Akıllı Asistan

from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Önceden Eğitilmiş Model ve Tokenizer Yükleme
# Bu model, cümleleri sayısal vektörlere (embedding) dönüştürmek için kullanılacak.
# "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" modeli çok dilli ve genel amaçlıdır.
print("NLP modelini yüklüyor...")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
model = AutoModel.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
print("NLP modeli başarıyla yüklendi.")

# Yardımcı fonksiyon: Cümleleri vektöre dönüştürme (Embedding)
def get_embedding(text):
    """
    Bir metni sayısal vektöre (embedding) dönüştürür.
    """
    # Tokenize the text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Get model outputs (embeddings)
    with torch.no_grad():
        model_output = model(**inputs)
    # Take the mean of the last hidden state to get sentence embedding
    # (Mean pooling)
    sentence_embedding = model_output.last_hidden_state.mean(dim=1).squeeze().numpy()
    return sentence_embedding

def temel_bilim_asistani(soru):
    """
    NLP entegrasyonu ile daha akıllı bir temel bilim asistanı.
    Soruyu en benzer bilgi ile eşleştirir.
    """
    bilgi_bankasi_raw = {
        "fotosentez nedir": "Fotosentez, bitkilerin güneş ışığını kullanarak karbondioksit ve suyu glikoza (şeker) ve oksijene dönüştürdüğü biyolojik bir süreçtir.",
        "yerçekimi nedir": "Yerçekimi, kütlesi olan cisimlerin birbirini çekmesini sağlayan temel bir kuvvettir. Isaac Newton tarafından tanımlanmıştır.",
        "atom nedir": "Atom, maddenin temel yapı taşıdır. Çekirdek (proton ve nötronlar) ve etrafında dönen elektronlardan oluşur.",
        "dna nedir": "dna (Deoksiribonükleik asit), canlı organizmaların genetik bilgisini taşıyan bir moleküldür. İkili sarmal yapısındadır.",
        "karadelik nedir": "Karadelik, uzayda yerçekiminin o kadar güçlü olduğu bir bölgedir ki, hiçbir parçacık veya elektromanyetik radyasyon (ışık dahil) oradan kaçamaz.",
        "ışık hızı kaçtır": "Işık hızı boşlukta yaklaşık saniyede 299,792,458 metredir.",
        "evrim nedir": "Evrim, canlı popülasyonlarının nesiller boyunca genetik özelliklerinde meydana gelen değişikliklerdir. Doğal seçilim bu süreci yönlendiren önemli bir faktördür.",
        "su formülü": "Su molekülünün kimyasal formülü H2O'dur. Bir oksijen ve iki hidrojen atomundan oluşur.",
        "dünyanın en büyük okyanusu": "Dünya'nın en büyük okyanusu Pasifik Okyanusu'dur.",
        "güneş sistemindeki gezegenler": "Güneş sistemindeki gezegenler şunlardır: Merkür, Venüs, Dünya, Mars, Jüpiter, Satürn, Uranüs ve Neptün.",
        "pi sayısı nedir": "Pi ($ \\pi $) sayısı, bir dairenin çevresinin çapına oranıdır ve yaklaşık olarak 3.14159'dur.",
        "en küçük canlı birim": "Canlıların temel yapısal ve işlevsel birimi hücredir."
    }

    # Bilgi bankası anahtarlarını ve değerlerini gömülülerine dönüştürelim (bir kez yapılır)
    # Bu adımı projenin başında yapmak, her soru geldiğinde yeniden hesaplamayı önler.
    bilgi_bankasi_embeddings = {
        anahtar: get_embedding(anahtar) for anahtar in bilgi_bankasi_raw.keys()
    }

    # Kullanıcının sorusunun embedding'ini alalım
    soru_embedding = get_embedding(soru.lower().strip())

    # En benzer bilgiyi bulmak için kosinüs benzerliği hesaplayalım
    en_yuksek_benzerlik = -1
    en_benzer_anahtar = None

    for anahtar, embedding in bilgi_bankasi_embeddings.items():
        benzerlik = cosine_similarity(soru_embedding.reshape(1, -1), embedding.reshape(1, -1))[0][0]
        if benzerlik > en_yuksek_benzerlik:
            en_yuksek_benzerlik = benzerlik
            en_benzer_anahtar = anahtar

    # Belirli bir eşiğin üzerindeyse yanıt ver
    # Bu eşik, yanıtın ne kadar alakalı olması gerektiğini belirler.
    # 0.7 veya 0.75 gibi bir değerle başlayabiliriz.
    if en_yuksek_benzerlik > 0.7:
        return f"EBDS Asistanı: {bilgi_bankasi_raw[en_benzer_anahtar]}"
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
        # Modelin ilk yüklenmesi biraz zaman alabilir, bu yüzden burada bekleyin.
        cevap = temel_bilim_asistani(kullanici_sorusu)
        print(cevap)