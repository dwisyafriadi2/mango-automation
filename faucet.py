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

def request_gas(recipient):
    url = 'https://faucet.testnet.mangonetwork.io/gas'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'chrome-extension://jiiigigdinhhgjflhljdkcelcjfmplnd',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    payload = {
        "FixedAmountRequest": {
            "recipient": recipient
        }
    }

    proxy = get_proxy()
    proxies = {
        'http': proxy,
        'https': proxy
    } if proxy else None

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies)
        if response.status_code == 201:
            data = response.json()
            print("✅ Gas transfer successful!")
            print(f"Amount: {data['transferredGasObjects'][0]['amount']}")
            print(f"Transaction ID: {data['transferredGasObjects'][0]['id']}")
            print(f"Transfer Digest: {data['transferredGasObjects'][0]['transferTxDigest']}")
        else:
            print(f"❌ Failed to request gas. Status Code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == '__main__':
    recipient = input("Enter the recipient wallet address: ").strip()
    if recipient:
        request_gas(recipient)
    else:
        print("❌ Recipient address cannot be empty!")
