"""
Steam Wishlist Exporter
=======================

Exporta todos os jogos da sua wishlist da Steam para um CSV.

Como usar:
  1. Instale as dependências: pip install requests
  2. Descubra seu Steam ID (64-bit): https://www.steamidfinder.com/
     OU use sua URL customizada: https://steamcommunity.com/id/SEU_NOME
  3. Certifique-se de que sua wishlist está PÚBLICA:
     Steam > Perfil > Editar Perfil > Configurações de Privacidade > Detalhes do Jogo = Público
  4. Execute: python steam_wishlist_export.py

-----------------------
Exports your Steam wishlist to a CSV file with pricing and rating data.

Usage:
  1. pip install requests
  2. Set CUSTOM_URL to your Steam profile name (or fill STEAM_ID directly)
  3. Make sure your wishlist is set to Public on Steam:
     Profile > Edit Profile > Privacy Settings > Game Details = Public
  4. python steam_wishlist_export.py

Output — steam_wishlist.csv:
  AppID | Nome | Preco | Preco Promo | Data Adicionado | Data Lancamento | Rating (%)

The CSV is encoded as UTF-8 with BOM (utf-8-sig) so Excel opens it correctly
without needing a manual import step.
"""

import csv
import math
import time
from datetime import datetime

import requests


# -- config

STEAM_ID   = ""        # 64-bit Steam ID — leave empty if using CUSTOM_URL
CUSTOM_URL = ""  # Your Steam profile name (the part after /id/ in your URL)

COUNTRY_CODE = "BR"              # Controls currency — BR returns prices in BRL
OUTPUT_FILE  = "steam_wishlist.csv"
DELAY        = 1.2               # Seconds to wait between API calls. Steam rate-limits
                                 # aggressive scrapers, so don't set this below 1.0.


# -- http headers

# Steam's API rejects requests without a browser-like User-Agent header,
# returning an HTML login page instead of JSON. These headers mimic a normal browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}


# -- csv column order

# Defines the column order in the output file.
# Matches the SteamFamily table in the data model (Jogos | SteamFamily | Avaliacoes).
CSV_FIELDS = [
    "AppID",
    "Nome",
    "Preco",
    "Preco Promo",
    "Data Adicionado",
    "Data Lancamento",
    "Rating (%)",
]


# -- steam id resolution

def resolve_steam_id(steam_id: str, custom_url: str) -> str:
    """
    Returns the 64-bit Steam ID needed for API calls.

    If a direct STEAM_ID is provided, uses it as-is.
    Otherwise, fetches the Steam community XML profile to extract the ID
    from the <steamID64> tag — no API key required for public profiles.
    """
    if steam_id:
        return steam_id
    if not custom_url:
        raise ValueError("Set either STEAM_ID or CUSTOM_URL at the top of the script.")

    print(f"Resolving Steam ID for: {custom_url}...")
    r = requests.get(
        f"https://steamcommunity.com/id/{custom_url}/?xml=1",
        headers=HEADERS,
        timeout=10,
    )
    if "<steamID64>" not in r.text:
        raise ValueError(
            f"Could not resolve '{custom_url}'.\n"
            "Check that the profile exists and is set to Public."
        )
    sid = r.text.split("<steamID64>")[1].split("</steamID64>")[0]
    print(f"  Steam ID: {sid}")
    return sid


# -- wishlist fetch

def fetch_wishlist(steam_id: str) -> list[dict]:
    """
    Fetches the wishlist via the IWishlistService API.

    Returns a list of dicts with keys: appid, priority, date_added.
    Does not include game names or prices — those come from appdetails.
    """
    print("Fetching wishlist...")
    url = (
        f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/"
        f"?steamid={steam_id}"
    )
    r = requests.get(url, headers=HEADERS, timeout=15)

    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code} — is the wishlist set to Public?")

    items = r.json().get("response", {}).get("items", [])
    print(f"  {len(items)} games found.")

    # Sort by the user-defined wishlist priority so the CSV reflects their order
    return sorted(items, key=lambda x: x.get("priority", 9999))


# -- game details

def fetch_app_details(app_id: int) -> dict:
    """
    Fetches name, price, release date and other metadata from the Steam Store API.

    The cc (country code) parameter sets the currency for prices.
    Returns an empty dict if the request fails or the app is not found.
    """
    url = (
        f"https://store.steampowered.com/api/appdetails"
        f"?appids={app_id}&cc={COUNTRY_CODE}&l=portuguese"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        if data.get(str(app_id), {}).get("success"):
            return data[str(app_id)]["data"]
    except Exception as e:
        print(f"    Warning: could not fetch details for {app_id}: {e}")
    return {}


def parse_price(price_overview: dict) -> tuple[str, str]:
    """
    Extracts the full price and the discounted price from a price_overview block.

    Steam returns prices as integers in cents (e.g. 4999 = R$49.99),
    so we divide by 100. Values are returned as plain decimal strings
    without currency symbols, making them easier to import into Excel.
    Returns empty strings for free games or missing data.
    """
    if not price_overview:
        return ("", "")

    initial  = price_overview.get("initial", 0) / 100   # original price in cents → reais
    final    = price_overview.get("final", 0) / 100     # discounted price
    discount = price_overview.get("discount_percent", 0)

    preco       = f"{initial:.2f}" if initial else "0.00"
    preco_promo = f"{final:.2f}" if discount > 0 else ""  # only set when there's an active discount
    return (preco, preco_promo)


def parse_release_date(details: dict) -> str:
    """
    Extracts and normalises the release date to DD/MM/YYYY.

    Steam returns dates as localised strings (e.g. "21 Aug, 2019" or "Aug 2019"),
    so we try multiple format strings until one matches.
    Returns "Em breve" for unreleased games, or the raw string if no format matches.
    """
    rd = details.get("release_date", {})
    if rd.get("coming_soon"):
        return "Em breve"
    date_str = rd.get("date", "")
    for fmt in ("%d %b, %Y", "%b %d, %Y", "%d %b %Y", "%b %Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return date_str  # fallback: return whatever Steam sent


# -- rating

def fetch_rating(app_id: int) -> str:
    """
    Calculates a review score using the Wilson Score lower bound formula.

    This is the same method SteamDB uses. Unlike a raw percentage
    (positive / total), Wilson Score accounts for sample size — a game with
    10/10 reviews scores lower than one with 9500/10000, which is more honest.

    z = 1.96 corresponds to a 95% confidence interval.
    Returns the score as a string like "87.3", or empty string if no reviews.
    """
    url = (
        f"https://store.steampowered.com/appreviews/{app_id}"
        f"?json=1&language=all&purchase_type=all&num_per_page=0"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        summary  = r.json().get("query_summary", {})
        positive = summary.get("total_positive", 0)
        total    = summary.get("total_reviews", 0)

        if total == 0:
            return ""

        z     = 1.96
        phat  = positive / total
        score = (
            phat + z * z / (2 * total)
            - z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total)
        ) / (1 + z * z / total)

        return str(round(score * 100, 1))
    except Exception:
        return ""


def timestamp_to_date(ts) -> str:
    """Converts a Unix timestamp (seconds since 1970) to DD/MM/YYYY."""
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime("%d/%m/%Y")
    except Exception:
        return ""


# -- main

def main():
    sid   = resolve_steam_id(STEAM_ID, CUSTOM_URL)
    items = fetch_wishlist(sid)

    if not items:
        print("Wishlist is empty or inaccessible.")
        return

    rows  = []
    total = len(items)
    print(f"\nFetching details for {total} games...\n")

    for i, item in enumerate(items, 1):
        app_id     = item["appid"]
        date_added = timestamp_to_date(item.get("date_added", ""))

        details = fetch_app_details(app_id)
        time.sleep(DELAY)  # wait between calls to avoid hitting Steam's rate limit

        rating = fetch_rating(app_id)
        time.sleep(DELAY * 0.5)

        nome            = details.get("name", f"AppID {app_id}")
        preco, preco_promo = parse_price(details.get("price_overview"))
        data_lancamento = parse_release_date(details)

        print(f"  [{i:>3}/{total}] {nome}")

        rows.append({
            "AppID":           app_id,
            "Nome":            nome,
            "Preco":           preco,
            "Preco Promo":     preco_promo,
            "Data Adicionado": date_added,
            "Data Lancamento": data_lancamento,
            "Rating (%)":      rating,
        })

    # utf-8-sig adds a BOM marker that tells Excel this is UTF-8,
    # preventing accented characters from showing up as garbage.
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    com_rating = sum(1 for r in rows if r["Rating (%)"])
    print(f"\n✅  {OUTPUT_FILE} — {len(rows)} games | {com_rating} with rating")


if __name__ == "__main__":
    main()
