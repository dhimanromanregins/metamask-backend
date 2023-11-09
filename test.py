# import requests
#
# # Your Etherscan API key
# api_key = '7DI9U879W1P9613SHPVUEKMXF7WDT85D5X'
#
# # Set the API endpoint
# url = f'https://api.etherscan.io/api'
#
# # Parameters for token listing
# params = {
#     'module': 'account',
#     'action': 'tokentx',
#     'address': '0xa6462FFBD9CA38f1267E1323218D024F2d19145f',  # The address you want to check for token transactions
#     'startblock': 0,
#     'endblock': 99999999,
#     'sort': 'asc',
#     'apikey': api_key,
# }
#
# # Make the API request to get the list of token transactions
# response = requests.get(url, params=params)
# data = response.json()
#
# # Extract and display the token information
# if data['status'] == '1':
#     token_transactions = data['result']
#     for tx in token_transactions:
#         contract_address = tx['contractAddress']
#         token_name = tx['tokenName']
#         print(f'Token Name: {token_name}, Contract Address: {contract_address}')
# else:
#     print('Error:', data['message'])
#













import requests

# Define the CoinGecko API URL for Ethereum (ETH) price in INR
eth_price_url = 'https://api.coingecko.com/api/v3/simple/price'

# Define the parameters for the request (Ethereum, in INR)
params = {
    'ids': 'ethereum',
    'vs_currencies': 'inr',
}

try:
    # Make the API request
    response = requests.get(eth_price_url, params=params)
    data = response.json()

    if 'ethereum' in data and 'inr' in data['ethereum']:
        eth_price_inr = data['ethereum']['inr']
        print(f'Real-time Ethereum (ETH) price in INR: ₹{eth_price_inr:.2f}')
    else:
        print('Error: Ethereum price data not found in the response.')

except Exception as e:
    print(f'Error: {e}')




