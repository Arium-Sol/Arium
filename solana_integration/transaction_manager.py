# solana_integration/transaction_manager.py

from solders.pubkey import Pubkey
from solders.hash import Hash
from solana.rpc.api import Client
from solana.transaction import Transaction, AccountMeta, TransactionInstruction
from solana.keypair import Keypair
import base64

def create_transfer_transaction(
    sender_private_key: str,
    recipient_address: str,
    amount: int,  # Amount in lamports
    solana_client: Client
) -> Transaction | None:
    """Creates a Solana transaction to transfer SOL."""

    try:
        sender_keypair = Keypair.from_bytes(base64.b64decode(sender_private_key))
        sender_pubkey = sender_keypair.pubkey()
        recipient_pubkey = Pubkey.from_string(recipient_address)

        # Get recent blockhash
        latest_blockhash = solana_client.get_latest_blockhash().value.blockhash

        # Create a transaction
        transaction = Transaction()
        transaction.recent_blockhash = latest_blockhash
        transaction.fee_payer = sender_pubkey

        # Add instruction to transfer SOL
        transfer_instruction = TransactionInstruction(
            keys=[
                AccountMeta(pubkey=sender_pubkey, is_signer=True, is_writable=True),
                AccountMeta(pubkey=recipient_pubkey, is_signer=False, is_writable=True),
            ],
            program_id=Pubkey.from_string("11111111111111111111111111111111"),  # System Program
            data=bytes([2, 0, 0, 0, amount & 0xFF, (amount >> 8) & 0xFF, (amount >> 16) & 0xFF, (amount >> 24) & 0xFF]),  # Transfer instruction data
        )
        transaction.add(transfer_instruction)

        # Sign the transaction
        transaction.sign(sender_keypair)

        return transaction

    except Exception as e:
        print(f"Error creating transaction: {e}")
        return None


def send_transaction(transaction: Transaction, solana_client: Client) -> str | None:
    """Sends a signed transaction to the Solana network."""
    try:
        # Send the transaction
        result = solana_client.send_raw_transaction(transaction.serialize())
        return result.value
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None


if __name__ == '__main__':
    # Replace with your actual private key (store securely!)
    sender_private_key = "YOUR_PRIVATE_KEY_ENCODED_IN_BASE64"
    recipient_address = "2nfjfW5E9JzLzWMmJCy5Y8Ks1nD4w2Y6PtMW9Scg8nNV"  # Replace with a recipient address
    amount = 1000000  # Amount in lamports

    solana_client = Client("https://api.devnet.solana.com")

    # Create the transaction
    transaction = create_transfer_transaction(sender_private_key, recipient_address, amount, solana_client)

    if transaction:
        # Send the transaction
        transaction_id = send_transaction(transaction, solana_client)

        if transaction_id:
            print(f"Transaction sent successfully! Transaction ID: {transaction_id}")
        else:
            print("Failed to send transaction.")
    else:
        print("Failed to create transaction.")
