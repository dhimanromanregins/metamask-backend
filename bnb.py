# import requests
# from web3 import Web3, Account
# 
# def generate_bnb_address():
#     bsc_rpc_url = "https://binance.llamarpc.com"
#     web3 = Web3(Web3.HTTPProvider(bsc_rpc_url))
# 
#     if web3.is_connected():
#         # Generate a new BNB address
#         account = Account.create()
#         private_key = account.key
#         address = account.address
# 
#         print("BNB address", address)
#         print("BNB private_key", private_key)
#         return ("addcount created successfully...")
# 
#     else:
#         return {"message": "Failed to connect to the BSC node."}, None
# 
# 
# main = generate_bnb_address()
# 
# print(main)



import requests

crypto_name = "binancecoin"  # Replace with the cryptocurrency name you want to fetch the logo for
coingecko_url = f"https://api.coingecko.com/api/v3/coins/{crypto_name}"

response = requests.get(coingecko_url)
data = response.json()

if 'image' in data:
    logo_url = data['image']['large']  # You can use 'small', 'thumb', or other sizes as needed
    print(f'Ethereum Logo URL: {logo_url}')
else:
    print('Logo not found.')