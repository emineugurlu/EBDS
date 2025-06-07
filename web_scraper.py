
# web_scraper.py (DuckDuckGo Entegrasyonu)

import requests
from bs4 import BeautifulSoup
import re
import time

def search_and_scrape(query):
    """
    Belirli bir sorgu için DuckDuckGo'da arama yapar ve ilk uygun sonuçtan metin çeker.
    DuckDuckGo, Google'a göre botlar için daha dostane olabilir.
    """
    search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"DuckDuckGo'da bilgi aranıyor: '{query}'...")
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        first_link = None
        # DuckDuckGo'nun arama sonuç linklerini bulmaya çalışalım
        # Genellikle 'result__a' sınıfına sahip a etiketleridir.
        for link in soup.find_all('a', class_='result__a'):
            href = link.get('href')
            if href and href.startswith('http'):
                # Bazı linkler DDG'nin kendi yönlendirme linkleri olabilir, bunları filtreleyelim
                if "duckduckgo.com/l/" in href:
                    # DDG'nin yönlendirme linklerini temizleyelim (örneğin: https://duckduckgo.com/l/?uddg=...)
                    # Bu regex ile uddg parametresinin değerini çekebiliriz.
                    match = re.search(r'uddg=(.*?)(?:&|$)', href)
                    if match:
                        decoded_url = requests.utils.unquote(match.group(1))
                        if decoded_url.startswith('http'): # Sadece geçerli bir URL ise al
                            first_link = decoded_url
                            break
                else: # Doğrudan URL ise al
                    first_link = href
                    break

        if first_link:
            print(f"Bulunan ilk bağlantı (DuckDuckGo): {first_link}")
            time.sleep(1) # Bot olarak algılanmamak için kısa bir bekleme

            # Şimdi bu bağlantıdaki sayfayı ziyaret edip içeriği çekelim
            page_response = requests.get(first_link, headers=headers, timeout=10)
            page_response.raise_for_status()
            page_soup = BeautifulSoup(page_response.text, 'html.parser')

            # Sayfa içeriğinden sadece metinleri çekelim ve temizleyelim
            # script ve style etiketlerini temizle
            for script_or_style in page_soup(['script', 'style']):
                script_or_style.decompose()
            text = page_soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)

            # Çok uzun metinleri kısaltalım (örneğin ilk 500 karakter)
            if len(clean_text) > 500:
                clean_text = clean_text[:500] + "..."

            if clean_text and len(clean_text) > 50: # En az 50 karakter olmalı ki anlamlı olsun
                return clean_text
            else:
                return "Belirtilen bağlantıdan anlamlı bir metin çekilemedi."
        else:
            return "DuckDuckGo aramasında uygun bir bağlantı bulunamadı."

    except requests.exceptions.RequestException as e:
        print(f"Web isteği hatası: {e}")
        return "Web'den bilgi çekerken bir sorun oluştu."
    except Exception as e:
        print(f"Web kazıma hatası: {e}")
        return "Web sayfasını işlerken bir sorun oluştu."