# web_scraper.py (Geliştirilmiş Metin Temizliği)

import requests
from bs4 import BeautifulSoup
import re
import time

def search_and_scrape(query):
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
        for link in soup.find_all('a', class_='result__a'):
            href = link.get('href')
            if href and href.startswith('http'):
                if "duckduckgo.com/l/" in href:
                    match = re.search(r'uddg=(.*?)(?:&|$)', href)
                    if match:
                        decoded_url = requests.utils.unquote(match.group(1))
                        if decoded_url.startswith('http'):
                            first_link = decoded_url
                            break
                else:
                    first_link = href
                    break

        if first_link:
            print(f"Bulunan ilk bağlantı (DuckDuckGo): {first_link}")
            time.sleep(1)

            page_response = requests.get(first_link, headers=headers, timeout=10)
            page_response.raise_for_status()
            page_soup = BeautifulSoup(page_response.text, 'html.parser')

            # Geliştirilmiş Metin Temizliği:
            # Sadece paragraf (<p>) etiketlerinin içeriğini çekmeye çalışalım.
            # Alternatif olarak, ana içerik div'lerini bulabiliriz, ancak bu genel bir başlangıç.
            paragraphs = page_soup.find_all('p')
            extracted_texts = []
            for p in paragraphs:
                text = p.get_text(separator=' ', strip=True) # Boşluklarla birleştir ve boşlukları temizle
                if text:
                    extracted_texts.append(text)

            clean_text = ' '.join(extracted_texts)

            # JavaScript ve CSS gibi istenmeyen etiketleri tamamen kaldır
            for script_or_style in page_soup(['script', 'style', 'header', 'footer', 'nav']):
                script_or_style.decompose()

            # Çok uzun metinleri kısalt (ilk 500 karakter yine iyi bir başlangıç)
            if len(clean_text) > 500:
                clean_text = clean_text[:500] + "..."

            if clean_text and len(clean_text) > 50:
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