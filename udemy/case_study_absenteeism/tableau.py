# %%
import pandas as pd
import pygwalker as pyg

df = pd.read_csv('data/Absenteeism_predictions.csv')
pyg.walk(df)
# %%
# %%
# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv('data/Absenteeism_predictions.csv')

def get_reason(row):
    if row['Reason_1'] == 1: return 'Doencas'
    if row['Reason_2'] == 1: return 'Gravidez'
    if row['Reason_3'] == 1: return 'Causas Externas'
    if row['Reason_4'] == 1: return 'Razoes Leves'
    return 'Nao especificado'

df['Grupo'] = df.apply(get_reason, axis=1)

fig = plt.figure(figsize=(16, 12))
fig.suptitle('Absenteismo: Analise das Predicoes', fontsize=15, fontweight='bold', y=0.98)
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

# Chart 1: Age vs Probability
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(df['Age'], df['Probability'], alpha=0.4, color='steelblue', s=20)
m, b = np.polyfit(df['Age'], df['Probability'], 1)
x_line = np.linspace(df['Age'].min(), df['Age'].max(), 100)
ax1.plot(x_line, m * x_line + b, color='crimson', linewidth=2)
ax1.set_title('Idade vs Probabilidade', fontweight='bold')
ax1.set_xlabel('Idade')
ax1.set_ylabel('Probabilidade')

# Chart 2: Reasons vs Probability
ax2 = fig.add_subplot(gs[0, 1])
reason_avg = df.groupby('Grupo')['Probability'].mean().sort_values(ascending=False)
colors = ['#e07b54', '#5b9bd5', '#70ad47', '#ffc000']
bars = ax2.bar(range(len(reason_avg)), reason_avg.values, color=colors[:len(reason_avg)])
ax2.set_xticks(range(len(reason_avg)))
ax2.set_xticklabels(reason_avg.index, rotation=15, ha='right', fontsize=8)
ax2.set_title('Razao vs Probabilidade Media', fontweight='bold')
ax2.set_ylabel('Probabilidade Media')
for bar, val in zip(bars, reason_avg.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
             f'{val:.2f}', ha='center', va='bottom', fontsize=9)

# Chart 3: Transportation Expense vs Probability
ax3 = fig.add_subplot(gs[1, :])
colors_pred = df['Prediction'].map({0: 'steelblue', 1: 'crimson'})
ax3.scatter(df['Transportation Expense'], df['Probability'],
            c=colors_pred, alpha=0.5, s=25)
m, b = np.polyfit(df['Transportation Expense'], df['Probability'], 1)
x_line = np.linspace(df['Transportation Expense'].min(), df['Transportation Expense'].max(), 100)
ax3.plot(x_line, m * x_line + b, color='black', linewidth=2, linestyle='--')
ax3.set_title('Despesa de Transporte vs Probabilidade', fontweight='bold')
ax3.set_xlabel('Despesa de Transporte')
ax3.set_ylabel('Probabilidade')
legend = [mpatches.Patch(facecolor='steelblue', label='Predicao 0'),
          mpatches.Patch(facecolor='crimson', label='Predicao 1')]
ax3.legend(handles=legend, loc='upper right')

plt.savefig('dashboard_absenteeism.png', dpi=150, bbox_inches='tight')
plt.show()
# %%
