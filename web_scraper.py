# web_scraper.py (Daha da Gelişmiş Metin Temizliği ve Basit Özetleme)

import requests
from bs4 import BeautifulSoup
import re
import time
import random
import nltk # NLTK kütüphanesi için import (eğer yüklü değilse yükleyeceğiz)
from nltk.tokenize import sent_tokenize # Cümleleri ayırmak için

# NLTK'nın punkt tokenizer'ını indir (bir kez çalıştırılması yeterlidir)
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    print("NLTK 'punkt' tokenizer indiriliyor... Bu bir kez yapılacaktır.")
    nltk.download('punkt')
    print("NLTK 'punkt' tokenizer indirildi.")


def search_and_scrape(query):
    search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"DuckDuckGo'da bilgi aranıyor: '{query}'...")
        time.sleep(random.uniform(1, 3))

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
            time.sleep(random.uniform(1, 3))

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

            main_content_area = page_soup.find('div', id='mw-content-text')
            if not main_content_area:
                main_content_area = page_soup.find('article')
            if not main_content_area:
                main_content_area = page_soup.find('main')
            if not main_content_area:
                main_content_area = page_soup.find('body')

            elements = []
            if main_content_area:
                elements = main_content_area.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
            else:
                elements = page_soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])

            extracted_texts = []
            for element in elements:
                text = element.get_text(separator=' ', strip=True)
                if text and len(text) > 20:
                    extracted_texts.append(text)

            raw_text = ' '.join(extracted_texts) # Ham metni tutalım

            # Temizleme adımları
            clean_text = re.sub(r'\s+', ' ', raw_text).strip()
            clean_text = re.sub(r'\[\d+\]', '', clean_text)
            clean_text = re.sub(r'\s*\(.*?\)\s*', ' ', clean_text)

            # Başındaki ve sonundaki özel karakterleri temizle
            clean_text = re.sub(r'^[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s]*', '', clean_text)
            clean_text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s]*$', '', clean_text)

            # Cümlelere ayır ve özetle
            sentences = sent_tokenize(clean_text)

            # Belirli bir cümle sayısıyla sınırlı özet (örn. ilk 3-5 cümle)
            summary_sentences = []
            current_length = 0
            max_summary_length = 700 # Maksimum özet uzunluğu
            max_sentences = 5 # Maksimum cümle sayısı

            for i, sent in enumerate(sentences):
                if i < max_sentences and (current_length + len(sent) + 1) <= max_summary_length:
                    summary_sentences.append(sent)
                    current_length += len(sent) + 1
                else:
                    break

            final_summary = ' '.join(summary_sentences)

            if final_summary and len(final_summary) > 70:
                return f"{final_summary} [Kaynak: {first_link}]" # Kaynağı da ekleyelim
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