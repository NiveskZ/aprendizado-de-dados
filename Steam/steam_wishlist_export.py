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

Colunas geradas:
  AppID, Game, Preco, Preco Promocao, Desconto (%), Data Adicionado,
  Data Lancamento, Rating (%), Total Reviews, Generos, Desenvolvedor, Publisher
"""

import requests
import csv
import time
import math
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURAÇÃO — edite aqui
# ─────────────────────────────────────────────
STEAM_ID = "SEU_STEAM_ID_AQUI"   # Ex: "76561198XXXXXXXXX"
# OU use seu perfil customizado (deixe STEAM_ID vazio e preencha abaixo):
CUSTOM_URL = ""                   # Ex: "meuNomeSteam" (sem barra)

COUNTRY_CODE = "BR"               # Moeda: BR = Real brasileiro
LANGUAGE = "portuguese"           # Idioma das descrições
OUTPUT_FILE = "steam_wishlist.csv"
DELAY_BETWEEN_REQUESTS = 1.2      # Segundos entre chamadas (respeita rate limit)
# ─────────────────────────────────────────────


def resolve_steam_id(steam_id: str, custom_url: str) -> str:
    """Resolve Steam ID a partir de URL customizada se necessário."""
    if steam_id and steam_id != "SEU_STEAM_ID_AQUI":
        return steam_id
    if custom_url:
        print(f"Resolvendo Steam ID para: {custom_url}...")
        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?vanityurl={custom_url}&key="
        # Sem API key funciona para vanity URLs públicas via endpoint alternativo
        fallback = f"https://steamcommunity.com/id/{custom_url}/?xml=1"
        r = requests.get(fallback, timeout=10)
        if "<steamID64>" in r.text:
            sid = r.text.split("<steamID64>")[1].split("</steamID64>")[0]
            print(f"Steam ID encontrado: {sid}")
            return sid
    raise ValueError(
        "Configure STEAM_ID ou CUSTOM_URL no início do script.\n"
        "Encontre seu Steam ID em: https://www.steamidfinder.com/"
    )


def fetch_wishlist(steam_id: str) -> dict:
    """Busca todos os jogos da wishlist (paginada)."""
    all_games = {}
    page = 0
    print("Buscando wishlist...")

    while True:
        url = (
            f"https://store.steampowered.com/wishlist/profiles/{steam_id}"
            f"/wishlistdata/?p={page}"
        )
        r = requests.get(url, timeout=15)

        if r.status_code != 200:
            print(f"  Erro HTTP {r.status_code} — wishlist pública?")
            break

        data = r.json()
        if not data:
            break

        all_games.update(data)
        print(f"  Página {page}: +{len(data)} jogos (total: {len(all_games)})")
        page += 1
        time.sleep(0.5)

    return all_games


def fetch_app_details(app_id: str) -> dict:
    """Busca detalhes do jogo na Steam Store API."""
    url = (
        f"https://store.steampowered.com/api/appdetails"
        f"?appids={app_id}&cc={COUNTRY_CODE}&l={LANGUAGE}"
    )
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get(str(app_id), {}).get("success"):
            return data[str(app_id)]["data"]
    except Exception as e:
        print(f"    Erro ao buscar detalhes ({app_id}): {e}")
    return {}


def fetch_review_score(app_id: str) -> tuple[float, int]:
    """
    Calcula o rating de reviews ao estilo SteamDB.
    Usa a fórmula de Wilson Score (intervalo de confiança inferior).
    Retorna: (score_percentual, total_reviews)
    """
    url = (
        f"https://store.steampowered.com/appreviews/{app_id}"
        f"?json=1&language=all&purchase_type=all&num_per_page=0"
    )
    try:
        r = requests.get(url, timeout=10)
        summary = r.json().get("query_summary", {})
        positive = summary.get("total_positive", 0)
        total = summary.get("total_reviews", 0)

        if total == 0:
            return (None, 0)

        # Wilson Score (fórmula usada pelo SteamDB)
        z = 1.96  # 95% de confiança
        phat = positive / total
        score = (
            phat + z * z / (2 * total)
            - z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total)
        ) / (1 + z * z / total)

        return (round(score * 100, 1), total)
    except Exception:
        return (None, 0)


def parse_price(price_data: dict) -> tuple[str, str, str]:
    """Extrai preço atual, preço com desconto e % de desconto."""
    if not price_data:
        return ("", "", "")

    currency = price_data.get("currency", "BRL")
    initial = price_data.get("initial", 0) / 100
    final = price_data.get("final", 0) / 100
    discount = price_data.get("discount_percent", 0)

    fmt = lambda v: f"R$ {v:.2f}" if currency == "BRL" else f"{v:.2f} {currency}"

    preco = fmt(initial) if initial else "Gratuito"
    preco_promo = fmt(final) if (discount > 0 and final) else ""
    desc_str = f"{discount}%" if discount > 0 else ""

    return (preco, preco_promo, desc_str)


def parse_release_date(details: dict) -> str:
    """Extrai data de lançamento formatada."""
    rd = details.get("release_date", {})
    if rd.get("coming_soon"):
        return "Em breve"
    date_str = rd.get("date", "")
    # Tenta converter para formato padronizado DD/MM/AAAA
    for fmt in ("%d %b, %Y", "%b %d, %Y", "%d %b %Y", "%b %Y", "%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return date_str


def timestamp_to_date(ts) -> str:
    """Converte Unix timestamp para DD/MM/AAAA."""
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime("%d/%m/%Y")
    except Exception:
        return ""


def main():
    sid = resolve_steam_id(STEAM_ID, CUSTOM_URL)
    wishlist_raw = fetch_wishlist(sid)

    if not wishlist_raw:
        print("Wishlist vazia ou inacessível. Verifique se está pública.")
        return

    # Ordena pela prioridade (ordem que o usuário definiu)
    sorted_games = sorted(
        wishlist_raw.items(),
        key=lambda x: x[1].get("priority", 9999)
    )

    rows = []
    total = len(sorted_games)

    print(f"\nBuscando detalhes de {total} jogos...\n")

    for i, (app_id, wl_data) in enumerate(sorted_games, 1):
        name = wl_data.get("name", f"App {app_id}")
        print(f"  [{i}/{total}] {name} (AppID: {app_id})")

        # Detalhes da store
        details = fetch_app_details(app_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        # Rating de reviews
        rating, total_reviews = fetch_review_score(app_id)
        time.sleep(DELAY_BETWEEN_REQUESTS * 0.5)

        # Preços
        price_data = details.get("price_overview") or wl_data.get("subs", [{}])[0] if wl_data.get("subs") else None
        if details:
            preco, preco_promo, desconto = parse_price(details.get("price_overview"))
        else:
            preco, preco_promo, desconto = "", "", ""

        # Data de lançamento
        data_lancamento = parse_release_date(details) if details else ""

        # Data adicionado à wishlist
        date_added = timestamp_to_date(wl_data.get("added", ""))

        # Gêneros
        genres = ", ".join(
            g.get("description", "") for g in details.get("genres", [])
        ) if details else ""

        # Desenvolvedor / Publisher
        dev = ", ".join(details.get("developers", [])) if details else ""
        pub = ", ".join(details.get("publishers", [])) if details else ""

        rows.append({
            "AppID": app_id,
            "Game": name,
            "Preco": preco,
            "Preco Promocao": preco_promo,
            "Desconto (%)": desconto,
            "Data Adicionado": date_added,
            "Data Lancamento": data_lancamento,
            "Rating (%)": rating if rating is not None else "",
            "Total Reviews": total_reviews if total_reviews > 0 else "",
            "Generos": genres,
            "Desenvolvedor": dev,
            "Publisher": pub,
        })

    # Salva CSV
    fieldnames = [
        "AppID", "Game", "Preco", "Preco Promocao", "Desconto (%)",
        "Data Adicionado", "Data Lancamento", "Rating (%)", "Total Reviews",
        "Generos", "Desenvolvedor", "Publisher"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Exportado com sucesso: {OUTPUT_FILE}")
    print(f"   {len(rows)} jogos | {sum(1 for r in rows if r['Rating (%)'] != '')} com rating")


if __name__ == "__main__":
    main()
