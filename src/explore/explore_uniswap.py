import requests
import json
from tqdm import tqdm
from time import sleep
from etherscan import Etherscan

APIKEY  = 'X3UT5IJW3ED6GMFV7TYKPTPFJBGAFR8NCW'
ADDRESS = "0xE592427A0AEce92De3Edee1F18E0157C05861564"

# Script Run 1: startblock="13513629", endblock="13613629"
out_file = "uniswap_13513629_13613629"

# Script Run 2: startblock="13613629", endblock="13713629"
#   out_file = "uniswap_13613629_13713629"

eth = Etherscan(f"{APIKEY}")
uniswap_txl = eth.get_normal_txs_by_address(f"{ADDRESS}", startblock="13513629", endblock="13613629", sort="asc")

with open(out_file, mode='wt+', encoding='utf-8') as o:
  for tx in tqdm(uniswap_txl):
    if tx["isError"] == "0" and tx["value"] != "0":
      bal = eth.get_eth_balance(tx["from"])
      val = tx["value"]
      gas = tx["gas"]
      gasUsed = tx["gasUsed"]
      gasPrice = tx["gasPrice"]
      o.write(f'{bal}, {val}, {gas}, {gasUsed}, {gasPrice}, {gasPrice}\n')