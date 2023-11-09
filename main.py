# from web3 import Web3, Account
#
# # Connect to an Ethereum node, you can use Infura or your own node
# w3 = Web3(Web3.HTTPProvider('https://wider-indulgent-brook.discover.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))
#
# account = Account.create()
# private_key = account.key
# address = account.address
#
# print("Private Key:", private_key)
# hex_private_key = private_key.hex()
# print("hex_private_key:", hex_private_key)
# print("Address:", address)
#
# try:
#     balance_wei = w3.eth.get_balance(address)
#     balance_eth = w3.from_wei(balance_wei, 'ether')
#     print("Balance in Wei:", balance_wei)
#     print("Balance in Ether:", balance_eth)
# except Exception as e:
#     print("Error:", str(e))
#
# try:
#     # Retrieve the list of transactions for the given address
#     transactions = w3.eth.get_transactions(address)
#
#     # Print the transaction history
#     for tx_hash in transactions:
#         tx = w3.eth.get_transaction(tx_hash)
#         print("Transaction Hash:", tx['hash'].hex())
#         print("From:", tx['from'])
#         print("To:", tx['to'])
#         print("Value (Wei):", tx['value'])
#         print("Block Number:", tx['blockNumber'])
#         print("Gas Used:", tx['gasUsed'])
#         print("Gas Price (Wei):", tx['gasPrice'])
#         print("\n")
#
# except Exception as e:
#     print("Error:", str(e))


import requests

# # Replace this with the Ethereum address you want to query
# address_to_query = "0xa6462FFBD9CA38f1267E1323218D024F2d19145f"
#
# # Replace with your Etherscan API key
# api_key = "7DI9U879W1P9613SHPVUEKMXF7WDT85D5X"
#
# # Etherscan API endpoint for getting the transaction list
# api_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address_to_query}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}"
#
# try:
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         data = response.json()
#         if data["status"] == "1":
#             transactions = data["result"]
#             for tx in transactions:
#                 print("Transaction Hash:", tx["hash"])
#                 print("From:", tx["from"])
#                 print("To:", tx["to"])
#                 print("Value (Wei):", tx["value"])
#                 print("Block Number:", tx["blockNumber"])
#                 print("Gas Used:", tx["gasUsed"])
#                 print("Gas Price (Wei):", tx["gasPrice"])
#                 print("\n")
#         else:
#             print("Etherscan API response status is not '1'.")
#     else:
#         print("Failed to connect to Etherscan API.")
#
# except Exception as e:
#     print("Error:", str(e))


import requests

# Replace with the Ethereum contract address for which you want to retrieve the ABI
contract_address = "0xD740806A02e78ABA46111750be296522e4cdb228"

# Replace with your Etherscan API key
api_key = "7DI9U879W1P9613SHPVUEKMXF7WDT85D5X"

# Etherscan API endpoint for getting the contract's ABI
api_url = f"https://api.etherscan.io/api?module=contract&action=getabi&address=0xD740806A02e78ABA46111750be296522e4cdb228&apikey=7DI9U879W1P9613SHPVUEKMXF7WDT85D5X"

try:
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1":
            abi = data["result"]
            print("Contract ABI:")
            print(abi)
        else:
            print("Etherscan API response status is not '1'.")
    else:
        print("Failed to connect to Etherscan API.")

except Exception as e:
    print("Error:", str(e))





#----------------------------------------------------------------------------_____# tranctinn



from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware

# Connect to an Ethereum node (you should replace 'http://your-ethereum-node' with the actual URL of an Ethereum node):
w3 = Web3(Web3.HTTPProvider('https://wider-indulgent-brook.discover.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))

# Instantiate an Account object from your key:
acct2 = "0x9669518B285e14Fac38Ac08406e267a3C179CcDd"

# For the sake of this example, fund the new account:
tx_hash = w3.eth.send_transaction({
    "from": acct2,  # Replace with the sender's address
    "value": w3.to_wei(3, 'ether'),
    "to": "0x0F31ee57A97FE2B7F1145363Fc708DA6CbbA623E"
})

tx = w3.eth.get_transaction(tx_hash)
assert tx["from"] == acct2