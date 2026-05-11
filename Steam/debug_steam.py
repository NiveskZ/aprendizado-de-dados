"""
Debug: mostra exatamente o que a Steam retorna para sua wishlist.
Execute: python debug_steam.py
"""
import os

import requests
from dotenv import load_dotenv


load_dotenv()

STEAM_ID = os.getenv("STEAM_ID", "")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

urls = [
    f"https://store.steampowered.com/wishlist/profiles/{STEAM_ID}/wishlistdata/?p=0",
    f"https://store.steampowered.com/wishlist/profiles/{STEAM_ID}/wishlistdata/",
    f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={STEAM_ID}",
]

for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    r = requests.get(url, headers=HEADERS, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers.get('Content-Type', 'n/a')}")
    print(f"Tamanho resposta: {len(r.text)} chars")
    print(f"Primeiros 300 chars:\n{r.text[:300]}")
