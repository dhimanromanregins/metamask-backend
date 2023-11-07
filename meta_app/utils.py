import requests

def get_token_logo_path(address):
    try:
        # Make an API request to CoinGecko to get token metadata
        api_url = f'https://api.coingecko.com/api/v3/coins/ethereum/contract/{address}'
        response = requests.get(api_url)
        data = response.json()

        # Extract the logo URL from the response
        token_logo_url = data.get('image', {}).get('small')

        if token_logo_url:
            return token_logo_url
        else:
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None



