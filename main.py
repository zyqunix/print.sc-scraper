import requests
from bs4 import BeautifulSoup
import string
import os
from time import sleep

def generate_ids(start='aaaaa0', end='zzzzz9'):
    base = string.ascii_lowercase
    start = list(start)
    end = list(end)
    current = start
    while current <= end:
        yield ''.join(current)
        # Increment base36-style
        i = len(current) - 1
        while i >= 0:
            if current[i] == '9':
                current[i] = 'a'
                break
            elif current[i] == 'z':
                current[i] = '0'
                i -= 1
            else:
                current[i] = chr(ord(current[i]) + 1)
                break
        else:
            break

def fetch_and_save(id_code):
    url = f'https://prnt.sc/{id_code}'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
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

for code in generate_ids('aaaaa1', 'zzzzz9'):  # adjust range as needed
    fetch_and_save(code)
