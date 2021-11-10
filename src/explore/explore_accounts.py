#!/usr/bin/env python3
#Investigating a txn on Ethereum Mainnet

import requests
import json
import time

APIKEY  = 'X3UT5IJW3ED6GMFV7TYKPTPFJBGAFR8NCW'
tag     = 'latest'

small_acc_1 = '../../data/3_small_addresses_from_13515990.txt'
small_acc_2 = '../../data/3_small_addresses_from_13516239.txt'

with open(small_acc_1) as f:
    lines = f.readlines()
    for line in lines:
      time.sleep(5)
      addr = line.strip('\n')
      print(addr)

      # query etherscan api
      response_txl = requests.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={addr}&sort=asc')
      response_bal = requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag={tag}&apikey={APIKEY}')
      parsed_txl = json.loads(response_txl.content)

      if response_txl.status_code != 200:
        print("ERR")

      if response_txl.status_code == 200:
        # compute metrics: average value, average gas paid, total transactions
        total_value = 0
        total_gas = 0
        total_gasPrice = 0
        total_gasUsed = 0

        total_txn = len(parsed_txl['result'])

        print(f'aggregating information about {addr}')
        print(total_txn)
        for tx in parsed_txl['result']:
          if type(tx) is str:
            print(parsed_txl['result'])
            break
          if type(tx) is dict:
            total_value += int(tx['value'])
            total_gas += int(tx['gas'])
            total_gasUsed += int(tx['gasUsed'])
            total_gasPrice += int(tx['gasPrice'])
        
        print('average value', (total_value / (total_txn * (10 ** (18)))))
        print('average gas: ', total_gas / total_txn)
        print('average gas used: ', total_gasUsed / total_txn)
        print('average gas price: ', total_gasPrice / total_txn)

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
