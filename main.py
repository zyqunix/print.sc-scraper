import requests
from bs4 import BeautifulSoup
import string
import os
from concurrent.futures import ThreadPoolExecutor
from itertools import product

chars = string.ascii_lowercase + string.digits

def generate_ids():
    for combo in product(chars, repeat=5):
        if any(c.isalnum() for c in combo):
            yield ''.join(combo)

def fetch_and_save(id_code):
    url = f'https://prnt.sc/{id_code}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        img = soup.find('img', {'class': 'no-click screenshot-image'})
        if img and 'src' in img.attrs:
            img_url = img['src']
            if not img_url.startswith('http'):
                print(f"[{id_code}] No valid image found.")
                return
            img_res = requests.get(img_url, headers=headers)
            if img_res.status_code == 200:
                ext = img_url.split('.')[-1]
                with open(f'{id_code}.{ext}', 'wb') as f:
                    f.write(img_res.content)
                print(f"[{id_code}] Saved.")
            else:
                print(f"[{id_code}] Image URL returned {img_res.status_code}.")
        else:
            print(f"[{id_code}] No image tag found.")
    except Exception as e:
        print(f"[{id_code}] Error: {e}")

os.makedirs('screenshots', exist_ok=True)
os.chdir('screenshots')

with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(fetch_and_save, generate_ids())
