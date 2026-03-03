import pandas as pd

# Carregar os arquivos
order_details = pd.read_csv('src/order_details.csv')
# Para o jsonl, necessário também colocar o lines=True
orders = pd.read_json('src/public-orders.jsonl', lines=True)

# Join on 'order_id'
merged = pd.merge(order_details, orders, on='order_id', how='inner')

# Filtrando por unit_price > 100
unit_price_col=merged['unit_price']
filtered = merged[unit_price_col > 100]

# Pegando os unique customer_ids
customer_ids = filtered['customer_id'].unique()

# Exportar para um CSV
pd.DataFrame({'customer_id': customer_ids}).to_csv('customers_above_100.csv', index=False)

# Podem printar os dataframes em etapas anteriores para ver o que retorna