# web_scraper.py (Daha da Gelişmiş Metin Temizliği ve İstenmeyen İçerik Filtreleme)

import requests
from bs4 import BeautifulSoup
import re
import time
import random # Rastgele bekleme süresi için

def search_and_scrape(query):
    search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"DuckDuckGo'da bilgi aranıyor: '{query}'...")
        time.sleep(random.uniform(1, 3)) # Rastgele bekleme süresi ekleyelim

        response = requests.get(search_url, headers=headers, timeout=15)
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
            time.sleep(random.uniform(1, 3)) # Linke gitmeden önce rastgele bekleme

            page_response = requests.get(first_link, headers=headers, timeout=15)
            page_response.raise_for_status()
            page_soup = BeautifulSoup(page_response.text, 'html.parser')

            # İstenmeyen etiketleri ve genellikle menü/navigasyon içeren etiketleri kaldır
            for unwanted_tag in page_soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', 'button', 'input', 'img', 'svg', 'picture', 'figure', 'iframe', 'audio', 'video', 'figcaption', 'noscript']):
                unwanted_tag.decompose()

            # İstenmeyen sınıflara sahip div'leri ve diğer öğeleri kaldır (genel menü, navigasyon, dipnotlar vb.)
            unwanted_classes = [
                'navbar', 'menu', 'sidebar', 'footer-links', 'header-links',
                'navigation', 'infobox', 'reference', 'ref-list', 'mw-jump-link',
                'toc', 'mw-indicators', 'thumb', 'noprint', 'portal' # Wikipedia'ya özgü bazı sınıflar
            ]
            for class_name in unwanted_classes:
                for tag in page_soup.find_all(class_=class_name):
                    tag.decompose()

            # Sayfanın ana içeriğini bulmaya çalış
            # Daha genel bir yaklaşım: <article> veya belirli id'lere sahip ana içerik div'leri
            main_content_area = page_soup.find('div', id='mw-content-text') # Wikipedia ana içerik ID'si
            if not main_content_area:
                main_content_area = page_soup.find('article')
            if not main_content_area:
                main_content_area = page_soup.find('main')
            if not main_content_area:
                main_content_area = page_soup.find('body') # Son çare tüm body'den al

            elements = []
            if main_content_area:
                # Ana içerik alanından sadece paragraf, başlık ve liste öğelerini çek
                elements = main_content_area.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
            else:
                # Ana içerik alanı bulunamazsa genel olarak paragraf, başlık ve liste elemanlarını çek
                elements = page_soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])

            extracted_texts = []
            for element in elements:
                text = element.get_text(separator=' ', strip=True)
                # Boş veya çok kısa metinleri atla
                if text and len(text) > 20: # Minimum metin uzunluğunu biraz artırdık
                    extracted_texts.append(text)

            clean_text = ' '.join(extracted_texts)

            # Fazla boşlukları, yeni satır karakterlerini ve Unicode boşluklarını temizle
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()

            # [1], [2] gibi referans numaralarını kaldır (bazı siteler için hala gerekli olabilir)
            clean_text = re.sub(r'\[\d+\]', '', clean_text)

            # Parantez içindeki sayıları veya kısa ifadeleri kaldırma (Örn: (Aralık 2023))
            clean_text = re.sub(r'\s*\(.*?\)\s*', ' ', clean_text) # Bu kısım dikkatli kullanılmalı, bazen önemli bilgiyi silebilir

            # Wikipedia'ya özgü "Koordinatlar" gibi başlangıç ifadelerini kaldırma
            if "Koordinatlar :" in clean_text:
                clean_text = clean_text.split("Koordinatlar :", 1)[1].strip()

            # Metnin başındaki ve sonundaki gereksiz özel karakterleri temizle
            clean_text = re.sub(r'^[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s]*', '', clean_text) # Başlangıçtaki özel karakterler
            clean_text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s]*$', '', clean_text) # Sondaki özel karakterler

            # Çok uzun metinleri kısalt
            if len(clean_text) > 800: # Kısaltma limitini biraz daha artırdık
                # Kelime ortasından kesmemek için son boşluğa kadar al
                clean_text = clean_text[:800].rsplit(' ', 1)[0] + "..." 
            elif len(clean_text) > 500 and not clean_text.endswith("..."):
                clean_text += "..."

            if clean_text and len(clean_text) > 70: # Minimum çekilen metin uzunluğunu artırdık
                return clean_text
            else:
                return f"Web'den çekilen metin anlamlı değil veya çok kısa. Bağlantı: {first_link}"
        else:
            return "DuckDuckGo aramasında uygun bir bağlantı bulunamadı. Lütfen sorgunuzu kontrol edin."

    except requests.exceptions.HTTPError as errh:
        return f"Web isteği hatası (HTTP): {errh}. Sunucuya erişilemiyor veya sayfa bulunamadı."
    except requests.exceptions.ConnectionError as errc:
        return f"Web isteği hatası (Bağlantı): {errc}. İnternet bağlantınızı kontrol edin."
    except requests.exceptions.Timeout as errt:
        return f"Web isteği hatası (Zaman Aşımı): {errt}. İstek zaman aşımına uğradı."
    except requests.exceptions.RequestException as err:
        return f"Beklenmedik web isteği hatası: {err}. Lütfen tekrar deneyin."
    except Exception as e:
        return f"Web sayfasını işlerken bir sorun oluştu: {e}. Lütfen tekrar deneyin."