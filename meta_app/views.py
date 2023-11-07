# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EthereumAccount, TokenContract
from .serializers import EthereumAccountSerializer,TokenInfoSerializer
from web3 import Web3, Account
import requests
from .utils import get_token_logo_path

class GenerateEthereumAccount(APIView):
    def post(self, request):
        # Extract user_id from the request data (ensure user_id is provided)
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({"message": "user_id is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Connect to an Ethereum node (e.g., Infura)
        w3 = Web3(Web3.HTTPProvider('https://wider-indulgent-brook.discover.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))

        # Generate an Ethereum account
        account = Account.create()
        private_key = account.key
        address = account.address

        # Save the Ethereum account to the database, associated with the provided user_id
        try:
            ethereum_account = EthereumAccount.objects.create(user_id=user_id, address=address, private_key=private_key.hex())
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the Ethereum account details
        serializer = EthereumAccountSerializer(ethereum_account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EthereumBalance(APIView):
    def get(self, request, address):
        # Connect to an Ethereum node (e.g., Infura)
        w3 = Web3(Web3.HTTPProvider('https://wider-indulgent-brook.discover.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))

        try:
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            return Response({"address": address, "balance_wei": balance_wei, "balance_eth": balance_eth}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EthereumTransactionHistory(APIView):
    def get(self, request, address):
        # Replace with your Etherscan API key
        api_key = "7DI9U879W1P9613SHPVUEKMXF7WDT85D5X"

        # Etherscan API endpoint for getting the transaction list
        api_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "1":
                    transactions = data["result"]
                    return Response(transactions, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Etherscan API response status is not '1'."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Failed to connect to Etherscan API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EthereumTokenInfo(APIView):
    def get(self, request, address):
        # Initialize a web3.py instance
        w3 = Web3(Web3.HTTPProvider('https://wider-indulgent-brook.discover.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))

        # Define the contract address and ABI of the token
        token_contract_address = '0x50327c6c5a14DCaDE707ABad2E27eB517df87AB5'
        token_abi_url = 'https://api.etherscan.io/api?module=contract&action=getabi&address=' + token_contract_address

        # Fetch the ABI from Etherscan
        response = requests.get(token_abi_url)
        token_abi = response.json()['result']

        # Create a contract instance
        token_contract = w3.eth.contract(address=token_contract_address, abi=token_abi)

        # Function to get token balance
        def get_token_balance(address):
            balance = token_contract.functions.balanceOf(address).call()
            return balance

        # Function to get token name and symbol
        def get_token_info():
            token_name = token_contract.functions.name().call()
            token_symbol = token_contract.functions.symbol().call()
            return token_name, token_symbol

        try:
            token_balance = get_token_balance(address)
            token_name, token_symbol = get_token_info()
            logo = get_token_logo_path(token_contract_address)
            data = {
                'address': address,
                'token_balance': token_balance,
                'token_name': token_name,
                'token_symbol': token_symbol,
                'token_logo': logo
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)})


class EthPriceView(APIView):
    def get(self, request):
        crypto_name = request.query_params.get('crypto_name')
        currency = request.query_params.get('currency', 'usd')

        if crypto_name is None:
            return Response({"message": "crypto_name is required in the request data."},
                            status=status.HTTP_400_BAD_REQUEST)

        eth_price_url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': crypto_name,
            'vs_currencies': currency,
        }

        try:
            response = requests.get(eth_price_url, params=params)
            data = response.json()
            token_price = data.get(crypto_name, {}).get(currency)
            if token_price is not None:
                return Response({f'{crypto_name}_{currency}': token_price})
            else:
                return Response(
                    {'error': f'Token price data not found for {crypto_name} in {currency} in the response.'},
                    status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)