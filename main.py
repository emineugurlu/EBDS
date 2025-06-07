# main.py dosyanızın içeriği - Geliştirilmiş Bilgi Bankası (anahtarlar küçük harf)

def temel_bilim_asistani(soru):
    """
    Basit bir temel bilim asistanı.
    Önceden tanımlanmış bilgilerle soruları yanıtlar.
    """
    # Bilgi bankasındaki anahtarları da küçük harf olarak tanımladık
    bilgi_bankasi = {
        "fotosentez nedir": "Fotosentez, bitkilerin güneş ışığını kullanarak karbondioksit ve suyu glikoza (şeker) ve oksijene dönüştürdüğü biyolojik bir süreçtir.",
        "yerçekimi nedir": "Yerçekimi, kütlesi olan cisimlerin birbirini çekmesini sağlayan temel bir kuvvettir. Isaac Newton tarafından tanımlanmıştır.",
        "atom nedir": "Atom, maddenin temel yapı taşıdır. Çekirdek (proton ve nötronlar) ve etrafında dönen elektronlardan oluşur.",
        "dna nedir": "DNA (Deoksiribonükleik asit), canlı organizmaların genetik bilgisini taşıyan bir moleküldür. İkili sarmal yapısındadır.", # DNA'yı küçük harf yaptık
        "karadelik nedir": "Karadelik, uzayda yerçekiminin o kadar güçlü olduğu bir bölgedir ki, hiçbir parçacık veya elektromanyetik radyasyon (ışık dahil) oradan kaçamaz.",
        "ışık hızı kaçtır": "Işık hızı boşlukta yaklaşık saniyede 299,792,458 metredir.",
        "evrim nedir": "Evrim, canlı popülasyonlarının nesiller boyunca genetik özelliklerinde meydana gelen değişikliklerdir. Doğal seçilim bu süreci yönlendiren önemli bir faktördür."
    }

    # Kullanıcının sorusunu küçük harfe çevirerek ve boşlukları temizleyerek işleyelim
    islenmis_soru = soru.lower().strip()

    # Bilgi bankasında eşleşen bir yanıt arayalım
    # Artık hem anahtarlar hem de kullanıcının sorusu küçük harf olduğundan
    # 'anahtar in islenmis_soru' daha güvenilir çalışacak.
    for anahtar, deger in bilgi_bankasi.items():
        if anahtar in islenmis_soru:
            return f"EBDS Asistanı: {deger}"

    return "EBDS Asistanı: Üzgünüm, bu konu hakkında henüz bilgiye sahip değilim."

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