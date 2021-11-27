import pandas as pd

small = pd.read_csv('../../data/250_small_addresses_from_13516239_processed.txt')
medium = pd.read_csv('../../data/250_large_addresses_from_13516239_processed.txt')

col_names = ['balance', 'num_txn', 'avg_tx_value', 'avg_gas', 'avg_gas_used', 'avg_gas_price']
small.columns = col_names[:]
medium.columns = col_names[:]

# add a new column to small: 
small['avg_tx_fee'] = small['avg_gas_used'] * small['avg_gas_price']
small['avg_tx_pct'] = small['avg_tx_fee'] / small['avg_tx_value']

medium['avg_tx_fee'] = medium['avg_gas_used'] * medium['avg_gas_price']
medium['avg_tx_pct'] = medium['avg_tx_fee'] / medium['avg_tx_value']

large = medium[medium['balance'] >= str(240 * (10 ** 18))]
medium = medium[medium['balance'] < str(240 * (10 ** 18))]

print(small.describe())
print(medium.describe())
print(large.describe())

compress_small = dict(method='zip', archive_name='small.csv')  
small.to_csv('../../data/small.zip', index=False, compression=compress_small)  

compress_medium = dict(method='zip', archive_name='medium.csv')  
medium.to_csv('../../data/medium.zip', index=False, compression=compress_medium) 

compress_large = dict(method='zip', archive_name='large.csv')  
large.to_csv('../../data/large.zip', index=False, compression=compress_large) 