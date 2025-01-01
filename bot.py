import requests
import json
import random

def get_proxy():
    try:
        with open('proxylist.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        if proxies:
            return random.choice(proxies)
        else:
            print("❌ Proxy list is empty!")
            return None
    except FileNotFoundError:
        print("❌ proxylist.txt not found!")
        return None

def auto_sign_in(token):
    url = 'https://task-api.testnet.mangonetwork.io/base/doSign'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json;charset=utf-8',
        'mgo-token': token,
        'Origin': 'https://task.testnet.mangonetwork.io',
        'Referer': 'https://task.testnet.mangonetwork.io/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    payload = {}

    proxy = get_proxy()
    proxies = {
        'http': proxy,
        'https': proxy
    } if proxy else None

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                print("✅ Sign-in successful!")
            else:
                print(f"❌ Sign-in failed: {data.get('msg')}")
        else:
            print(f"❌ Failed to sign in. Status Code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"❌ Sign-in request failed: {e}")

if __name__ == '__main__':
    token = input("Enter your mgo-token for sign-in: ").strip()
    if token:
        auto_sign_in(token)
    else:
        print("❌ Token cannot be empty!")
