import web3
from web3 import Web3
import requests

# Initialize a web3.py instance
w3 = Web3(Web3.HTTPProvider('https://wider-indulgent-brook.discover.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))

# Define the contract address and ABI of the token
token_contract_address = '0xD740806A02e78ABA46111750be296522e4cdb228'
token_abi_url = 'https://api.etherscan.io/api?module=contract&action=getabi&address=' + token_contract_address

# Fetch the ABI from Etherscan
response = requests.get(token_abi_url)
token_abi = response.json()['result']

# Create a contract instance
token_contract = w3.eth.contract(address=token_contract_address, abi=token_abi)

# Ethereum address you want to check
address = '0x9669518B285e14Fac38Ac08406e267a3C179CcDd'

# Function to get token balance
def get_token_balance(address):
    balance = token_contract.functions.balanceOf(address).call()
    return balance

try:
    token_balance = get_token_balance(address)
    print(f'Token balance for {address}: {token_balance}')
except Exception as e:
    print(f'Error: {e}')
