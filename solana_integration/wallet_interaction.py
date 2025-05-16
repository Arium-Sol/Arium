# solana_integration/wallet_interaction.py

from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.exceptions import SolanaRpcException

def get_wallet_balance(wallet_address: str):
    """Gets the balance of a Solana wallet."""
    solana_client = Client("https://api.devnet.solana.com")  # Use mainnet-beta for production

    try:
        pubkey = Pubkey.from_string(wallet_address)
        balance = solana_client.get_balance(pubkey).value
        return balance
    except SolanaRpcException as e:
        print(f"Error getting balance (Solana RPC Error): {e}")
        return None
    except ValueError as e:
        print(f"Error getting balance (Invalid Wallet Address): {e}")
        return None
    except Exception as e:
        print(f"Unexpected error getting balance: {e}")
        return None

if __name__ == '__main__':
    wallet_address = "2nfjfW5E9JzLzWMmJCy5Y8Ks1nD4w2Y6PtMW9Scg8nNV"  # Replace with an actual wallet address
    balance = get_wallet_balance(wallet_address)

    if balance is not None:
        print(f"Wallet balance: {balance} lamports")
