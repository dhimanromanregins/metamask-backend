from web3 import Web3, WebsocketProvider

# Connect to an Ethereum node (replace with the actual URL of an Ethereum node):
w3 = Web3(WebsocketProvider('wss://wider-indulgent-brook.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))

# Gas price in Wei (you can obtain it from the network)
gas_price_wei = w3.eth.gas_price

# Gas limit for your transaction (you need to set this value)
gas_limit = 10000  # Replace with your desired gas limit

# Calculate gas fee in Wei
gas_fee_wei = gas_price_wei * gas_limit

# Convert gas fee to Gwei (1 Gwei = 1e9 Wei)
gas_fee_gwei = gas_fee_wei / 1e9

print(f"Gas Fee in Wei: {gas_fee_wei} Wei")
print(f"Gas Fee in Gwei: {gas_fee_gwei} Gwei")