"""
RAWG Playtime Fetcher
---------------------
Reads steam_wishlist.csv, searches each game on RAWG,
and outputs hltb_results.csv with the following columns:

  AppID | Nome | Playtime (h)

How to use:
  1. Set up the virtualenv and install dependencies:
       python -m venv venv
       source venv/bin/activate
       pip install -r requirements.txt
  2. Copy .env.example to .env and fill in RAWG_API_KEY
  3. python rawg_fetch.py

The playtime value is the average hours reported by RAWG users (sourced
from Steam), not a completion-based estimate. It represents how long
people actually played, regardless of whether they finished the game.
"""

import csv
import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()


# -- config

RAWG_API_KEY = os.getenv("RAWG_API_KEY", "")

INPUT_FILE  = "steam_wishlist.csv"
OUTPUT_FILE = "hltb_results.csv"
DELAY       = 1.0  # seconds between requests

OUTPUT_FIELDS = ["AppID", "Nome", "Playtime (h)"]


def search_rawg(session: requests.Session, name: str) -> str:
    """
    Searches RAWG for a game and returns the average playtime in hours.
    Returns an empty string if the game is not found or has no playtime data.
    """
    try:
        r = session.get(
            "https://api.rawg.io/api/games",
            params={"key": RAWG_API_KEY, "search": name, "page_size": 1},
            timeout=15,
        )
        if r.status_code != 200:
            print(f"    HTTP {r.status_code}")
            return ""
        results = r.json().get("results", [])
        if not results:
            return ""
        playtime = results[0].get("playtime", 0)
        return str(playtime) if playtime > 0 else ""
    except Exception as e:
        print(f"    Error: {e}")
        return ""


def main():
    if not RAWG_API_KEY:
        raise ValueError("RAWG_API_KEY not set — copy .env.example to .env and fill it in.")

    games = list(csv.DictReader(open(INPUT_FILE, encoding="utf-8-sig")))
    games = [g for g in games if not g["Nome"].startswith("AppID ")]

    total = len(games)
    print(f"Fetching playtime for {total} games...\n")

    session = requests.Session()
    session.headers.update({"User-Agent": "personal-backlog-tool/1.0"})

    rows      = []
    not_found = []

    for i, game in enumerate(games, 1):
        name   = game["Nome"]
        app_id = game["AppID"]

        print(f"  [{i:>3}/{total}] {name}", end=" ... ", flush=True)

        playtime = search_rawg(session, name)

        if playtime:
            print(f"{playtime}h")
        else:
            print("not found")
            not_found.append(name)

        rows.append({"AppID": app_id, "Nome": name, "Playtime (h)": playtime})

        time.sleep(DELAY)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅  {OUTPUT_FILE} — {total} games processed")

    if not_found:
        print(f"\nNo results for {len(not_found)} games:")
        for n in not_found:
            print(f"  {n}")


if __name__ == "__main__":
    main()
