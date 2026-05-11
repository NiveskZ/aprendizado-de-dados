"""
HowLongToBeat Fetcher
---------------------
Reads steam_wishlist.csv, searches each game on HowLongToBeat,
and outputs hltb_results.csv with the following columns:

  AppID | Nome | HLTB Main (h) | HLTB Main+Extra (h) | HLTB Completionist (h)

How to use:
  1. Activate the HLTB virtualenv (Python 3.11):
       source venv-hltb/bin/activate
  2. pip install -r requirements-hltb.txt
  3. python hltb_fetch.py

Why a separate venv:
  howlongtobeatpy depends on aiohttp, which is incompatible with Python 3.14.
  Python 3.11 handles TLS permissively by default — no patches needed.

Best match logic:
  HLTB returns results ranked by similarity. The entry with the highest
  similarity score is used. Games with no results are written with empty
  time columns and listed at the end.
"""

import asyncio
import csv
import ssl
import time

# Patch ssl.create_default_context before importing howlongtobeatpy.
# aiohttp (used internally by the library) calls create_default_context at
# import time. The HLTB server sometimes closes TLS connections before the
# handshake completes — OP_IGNORE_UNEXPECTED_EOF tells OpenSSL to treat
# that as a normal EOF instead of raising SSLEOFError.
# Available on Python 3.10+ with OpenSSL 3.0+.
_orig_create_default_context = ssl.create_default_context

def _patched_create_default_context(*args, **kwargs):
    ctx = _orig_create_default_context(*args, **kwargs)
    if hasattr(ssl, "OP_IGNORE_UNEXPECTED_EOF"):
        ctx.options |= ssl.OP_IGNORE_UNEXPECTED_EOF
    return ctx

ssl.create_default_context = _patched_create_default_context

from howlongtobeatpy import HowLongToBeat


INPUT_FILE  = "steam_wishlist.csv"
OUTPUT_FILE = "hltb_results.csv"
DELAY       = 2.0  # seconds between requests

OUTPUT_FIELDS = [
    "AppID",
    "Nome",
    "HLTB Main (h)",
    "HLTB Main+Extra (h)",
    "HLTB Completionist (h)",
]


def hours_str(value) -> str:
    """Returns the value rounded to 1 decimal, or empty string if zero or missing."""
    try:
        h = float(value)
        return str(round(h, 1)) if h > 0 else ""
    except Exception:
        return ""


async def search_hltb(hltb: HowLongToBeat, name: str) -> dict:
    """
    Searches HLTB for a game and returns the best match's times.
    Best match = entry with highest similarity score.

    Receives a shared HowLongToBeat instance so the library reuses its
    internal aiohttp session and cached API endpoint across all searches,
    avoiding a JS file discovery request on every game.

    Retries up to 3 times on connection errors with increasing delays.
    """
    empty = {"HLTB Main (h)": "", "HLTB Main+Extra (h)": "", "HLTB Completionist (h)": ""}
    for attempt in range(1, 4):
        try:
            results = await hltb.async_search(name)
            if not results:
                return empty
            best = max(results, key=lambda r: r.similarity)
            return {
                "HLTB Main (h)":          hours_str(best.main_story),
                "HLTB Main+Extra (h)":    hours_str(best.main_extra),
                "HLTB Completionist (h)": hours_str(best.completionist),
            }
        except Exception as e:
            if attempt < 3:
                wait = attempt * 5
                print(f"    Error (attempt {attempt}/3): {e} — retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"    Error: {e}")
    return empty


async def main():
    games = list(csv.DictReader(open(INPUT_FILE, encoding="utf-8-sig")))
    games = [g for g in games if not g["Nome"].startswith("AppID ")]

    total = len(games)
    print(f"Fetching HLTB data for {total} games...\n")

    rows      = []
    not_found = []

    # One shared instance — the library reuses its aiohttp session and
    # cached API endpoint instead of re-discovering it on every search.
    hltb = HowLongToBeat()

    for i, game in enumerate(games, 1):
        name   = game["Nome"]
        app_id = game["AppID"]

        print(f"  [{i:>3}/{total}] {name}", end=" ... ", flush=True)

        hltb_data = await search_hltb(hltb, name)

        if hltb_data["HLTB Main (h)"]:
            print(f"Main: {hltb_data['HLTB Main (h)']}h")
        else:
            print("not found")
            not_found.append(name)

        rows.append({"AppID": app_id, "Nome": name, **hltb_data})

        time.sleep(DELAY)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅  {OUTPUT_FILE} — {total} games processed")

    if not_found:
        print(f"\nNo HLTB results for {len(not_found)} games (check manually):")
        for n in not_found:
            print(f"  {n}")


if __name__ == "__main__":
    asyncio.run(main())
