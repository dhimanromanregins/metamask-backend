# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EthereumAccount, TokenContract, ChainDetails
from .serializers import EthereumAccountSerializer,TokenInfoSerializer,ChainDetailsSerializer
from web3 import Web3, Account
import requests
from .utils import get_token_logo_path
from Authentication.models import CustomUser


class GenerateNetworkAccount(APIView):
    def post(self, request):
        user_name = request.data.get('user_name')
        chain_symbol = request.data.get('chain_symbol', 'SSP')

        if user_name is None:
            return Response({"message": "user_name is required in the request data."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=user_name)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        chain_details = ChainDetails.objects.all()
        chain_details_serializer = ChainDetailsSerializer(chain_details, many=True)

        user_chain_account = EthereumAccount.objects.filter(user=user, chain_symbol=chain_symbol).first()
        if user_chain_account:
            return Response({
                "message": f"User Address already exists for chain_symbol {chain_symbol}",
                "address": user_chain_account.address,
                "Chains": chain_details_serializer.data,
                "Status": status.HTTP_409_CONFLICT
            }, status=status.HTTP_409_CONFLICT)

        rpc = ChainDetails.objects.filter(chain_symbol=chain_symbol).first()
        rpc_url = rpc.chain_rpc

        w3 = Web3(Web3.HTTPProvider(rpc_url))

        account = Account.create()
        private_key = account.key
        address = account.address

        try:
            ethereum_account = EthereumAccount.objects.create(
                user=user,
                chain_symbol=chain_symbol,
                address=address,
                private_key=private_key.hex()
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        ethereum_account_serializer = EthereumAccountSerializer(ethereum_account)

        response_data = {
            "User_data": ethereum_account_serializer.data,
            "Chains": chain_details_serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class CoinBalance(APIView):
    def get(self, request, address, symbol):
        chain_symbol = request.data.get('symbol')

        if chain_symbol:
            return Response({"message": "chain_symbol is required in the request data."},
                            status=status.HTTP_400_BAD_REQUEST)

        rpc = ChainDetails.objects.filter(chain_symbol=symbol).first()
        rpc_url = rpc.chain_rpc

        # Connect to an Ethereum node (e.g., Infura)
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        try:
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            return Response({"address": address, "balance_wei": balance_wei, "balance_eth": balance_eth}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CoinTransactionHistory(APIView):
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



class CoinTokenInfo(APIView):
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


class CoinPriceView(APIView):
    def get(self, request):
        crypto_name = request.query_params.get('crypto_name')
        currency = request.query_params.get('currency', 'usd')
        amount = request.query_params.get('amount')

        if crypto_name is None:
            return Response({"message": "crypto_name is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)
        if amount is None:
            return Response({"message": "amount is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)
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
                try:
                    # Convert token_price and amount to float, then calculate the USD price
                    token_price = float(token_price)
                    amount = float(amount)
                    usd_price = token_price * amount
                    return Response({f'{crypto_name}_{currency}': usd_price})
                except ValueError:
                    return Response({'error': 'Invalid numeric value for token_price or amount.'}, status=400)
            else:
                return Response({'error': f'Token price data not found for {crypto_name} in {currency} in the response.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SendCoinView(APIView):
    def post(self, request):
        try:
            data = request.data
            sender_address = data.get('sender_address')
            receiver_address = data.get('receiver_address')
            value = data.get('value')

            if not sender_address or not receiver_address or value is None:
                return Response({'error': 'sender_address, receiver_address, and value must be provided in the request body'}, status=400)

            # Connect to an Ethereum node
            w3 = Web3(Web3.HTTPProvider('https://wider-indulgent-brook.discover.quiknode.pro/67c3e69fe1b270b5f51fa0d46cc048a9963e9a21/'))

            # Check if the sender has a sufficient balance for the transfer
            sender_balance = w3.eth.get_balance(sender_address)
            if sender_balance <= value:
                return Response({'error': 'Insufficient balance in sender_address'}, status=400)

            # Create and send the transaction
            tx_hash = w3.eth.send_transaction({
                "from": sender_address,
                "to": receiver_address,
                "value": w3.to_wei(int(value), 'ether'),
            })

            return Response({'tx_hash': tx_hash}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
