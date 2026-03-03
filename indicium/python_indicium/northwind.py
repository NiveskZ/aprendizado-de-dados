import pandas as pd

order_details = pd.read_csv('data/order_details.csv')

orders = pd.read_json('data/public-orders.jsonl', lines=True)

merged = pd.merge(order_details, orders, on='order_id', how='inner')

print(merged.head(5))

merged.to_csv('data/merged_dataframe.csv', index=False)