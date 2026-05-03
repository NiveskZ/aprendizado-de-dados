import matplotlib.pyplot as plt

# ── Dicionário com dados históricos de consumo de energia ──
dados = {
    "Jan": 450,
    "Fev": 390,
    "Mar": 520,
    "Abr": 480,
    "Mai": 610,
    "Jun": 570,
    "Jul": 630,
    "Ago": 600,
    "Set": 540,
    "Out": 510,
    "Nov": 480,
    "Dez": 420
}

meses  = list(dados.keys())
valores = list(dados.values())

print("Dados de consumo energético (kWh):")
for mes, val in dados.items():
    print(f"  {mes}: {val} kWh")
print(f"\nMédia anual : {sum(valores)/len(valores):.1f} kWh")
print(f"Mês de pico : {max(dados, key=dados.get)} ({max(valores)} kWh)")
print(f"Mês mínimo  : {min(dados, key=dados.get)} ({min(valores)} kWh)")

# --- Gráfico 1: Barras ---------------------------------------
plt.figure(figsize=(10, 5))
barras = plt.bar(meses, valores, color='steelblue', edgecolor='white', linewidth=0.8)

# Rótulo de valor em cima de cada barra
for barra, val in zip(barras, valores):
    plt.text(barra.get_x() + barra.get_width() / 2,
             barra.get_height() + 8,
             str(val),
             ha='center', va='bottom', fontsize=9)

plt.title("Consumo de Energia Elétrica por Mês (kWh)", fontsize=13, fontweight='bold')
plt.xlabel("Mês", fontsize=11)
plt.ylabel("Consumo (kWh)", fontsize=11)
plt.ylim(0, max(valores) + 80)
plt.tight_layout()
plt.show()

# --- Gráfico 2: Linha (tendência) ----------------------------
plt.figure(figsize=(10, 5))
plt.plot(meses, valores,
         marker='o', color='steelblue', linewidth=2,
         markerfacecolor='white', markeredgewidth=2, markersize=7)

# Rótulo de cada ponto
for i, (mes, val) in enumerate(zip(meses, valores)):
    plt.text(i, val + 12, str(val), ha='center', fontsize=9)

plt.title("Tendência de Consumo Energético ao Longo do Ano (kWh)", fontsize=13, fontweight='bold')
plt.xlabel("Mês", fontsize=11)
plt.ylabel("Consumo (kWh)", fontsize=11)
plt.ylim(0, max(valores) + 80)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
