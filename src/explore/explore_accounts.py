#!/usr/bin/env python3
#Investigating a txn on Ethereum Mainnet

import requests
import json
from time import sleep
from tqdm import tqdm

APIKEY  = 'X3UT5IJW3ED6GMFV7TYKPTPFJBGAFR8NCW'
tag     = 'latest'

small_acc_1 = '../../data/250_small_addresses_from_13515990.txt'
small_acc_2 = '../../data/250_small_addresses_from_13516239.txt'
large_acc_1 = '../../data/250_large_addresses_from_13516239.txt'

in_file  = large_acc_1
out_file = f'{in_file}_processed'

lines = []
with open(in_file) as f:
    lines = f.readlines()

with open(out_file, mode='wt+', encoding='utf-8') as o:
  res = []

  for line in tqdm(lines):
    # getting rate limited...
    sleep(5)
    addr = line.strip('\n')

    # query etherscan api
    response_txl = requests.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={addr}&sort=asc')
    response_bal = requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag={tag}&apikey={APIKEY}')

    if response_txl.status_code == 200 and response_bal.status_code == 200:
      parsed_bal = json.loads(response_bal.content)
      parsed_txl = json.loads(response_txl.content)

      # account balance as of the latest block
      balance = parsed_bal['result']

      # total number of transactions as of the latest block
      total_txn = len(parsed_txl['result'])

      # compute metrics: average value, average gas paid, total transactions
      total_value = 0
      total_gas = 0
      total_gasPrice = 0
      total_gasUsed = 0

      if type(parsed_txl['result'][0]) == str:
        continue

      for tx in parsed_txl['result']:
        total_value += int(tx['value'])
        total_gas += int(tx['gas'])
        total_gasUsed += int(tx['gasUsed'])
        total_gasPrice += int(tx['gasPrice'])
      
      avg_val = round(total_value / total_txn, 3)
      avg_gas = round(total_gas / total_txn, 3)
      avg_gasUsed = round(total_gasUsed / total_txn, 3)
      avg_gasPrice = round(total_gasPrice / total_txn, 3)

      # bal, num of txs, avg tx value, avg gas, avg gas used, avg gas price
      res.append(f'{balance}, {total_txn}, {avg_val}, {avg_gas}, {avg_gasUsed}, {avg_gasPrice}')
      o.write(f'{balance}, {total_txn}, {avg_val}, {avg_gas}, {avg_gasUsed}, {avg_gasPrice}\n')

# # account balance in wei
# if response_tok.status_code == 200:
#   # parsed_bal = json.loads(response_bal.content)
#   # eth_balance = round(int(parsed_bal['result']) * 10 ** (-18), 5)
#   # print(f'{address} has {eth_balance} ETH')

#   # parsed_txl = json.loads(response_txl.content)
#   # print(len(parsed_txl['result']))

#   parsed_tok = json.loads(response_tok.content)
  
#   print(len(parsed_tok['result']))

#   # visualize the json dump
#   with open('parsed_tok.json', 'w', encoding='utf-8') as f:
#       json.dump(parsed_tok, f, ensure_ascii=False, indent=4)
