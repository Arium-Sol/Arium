# solana_integration/nft_management.py

from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.transaction import Transaction, AccountMeta, TransactionInstruction
from solana.keypair import Keypair
import base64

def create_nft(
    funder_private_key: str,
    metadata_program_id: str,
    mint_address: str,
    metadata_address: str,
    name: str,
    symbol: str,
    uri: str,
    solana_client: Client,
) -> str | None:
    """Creates a Metaplex NFT."""
    try:
        funder_keypair = Keypair.from_bytes(base64.b64decode(funder_private_key))
        funder_pubkey = funder_keypair.pubkey()

        # Get recent blockhash
        latest_blockhash = solana_client.get_latest_blockhash().value.blockhash

        # Create transaction
        transaction = Transaction()
        transaction.recent_blockhash = latest_blockhash
        transaction.fee_payer = funder_pubkey

        # Construct the instruction data (this depends on the Metaplex program)
        instruction_data = bytes([0])  # Placeholder instruction data
        instruction_data += len(name).to_bytes(1, 'little') + name.encode('utf-8')
        instruction_data += len(symbol).to_bytes(1, 'little') + symbol.encode('utf-8')
        instruction_data += len(uri).to_bytes(2, 'little') + uri.encode('utf-8')
        instruction_data += bytes([1])  # Seller fee basis points (e.g., 100 for 1%)
        instruction_data += bytes([0, 0])  # Royalty

        # Create the instruction
        instruction = TransactionInstruction(
            keys=[
                AccountMeta(pubkey=funder_pubkey, is_signer=True, is_writable=True),  # Funder
                AccountMeta(pubkey=Pubkey.from_string(mint_address), is_signer=False, is_writable=True),  # Mint
                AccountMeta(pubkey=Pubkey.from_string(metadata_address), is_signer=False, is_writable=True),  # Metadata
                AccountMeta(pubkey=Pubkey.from_string("11111111111111111111111111111111"), is_signer=False, is_writable=False),  # System Program
                AccountMeta(pubkey=Pubkey.from_string("TokenkegQfeZyiNwmdBZoc51zh9UvIU2jsApzcun8fmjang"), is_signer=False, is_writable=False),  # Token Program
                AccountMeta(pubkey=Pubkey.from_string("metaqbxxUerdqcvzi28by2ctnizn3xnmoxjpbwhgszhn"), is_signer=False, is_writable=False),  # Metaplex program id
                AccountMeta(pubkey=Pubkey.from_string("SysvarRent111111111111111111111111111111111"), is_signer=False, is_writable=False), #Rent sysvar
                AccountMeta(pubkey=Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"), is_signer=False, is_writable=False), #Associated token account program
                AccountMeta(pubkey=Pubkey.from_string("Crea8tor224UroN9dkfP3e9WRqK9hTgKymjhes692k"), is_signer=False, is_writable=False) #Creators account - to update
            ],
            program_id=Pubkey.from_string(metadata_program_id),
            data=instruction_data,
        )
        transaction.add(instruction)

        # Sign the transaction
        transaction.sign(funder_keypair)

        # Send the transaction
        result = solana_client.send_raw_transaction(transaction.serialize())
        return result.value

    except Exception as e:
        print(f"Error creating NFT: {e}")
        return None


if __name__ == '__main__':
    # Replace with your actual private key (store securely!)
    funder_private_key = "YOUR_PRIVATE_KEY_ENCODED_IN_BASE64"

    # Replace with the Metaplex program ID
    metadata_program_id = "metaqbxxUerdqcvzi28by2ctnizn3xnmoxjpbwhgszhn"  # Metaplex program ID

    # Replace with a mint address
    mint_address = "Gh9Ej3q9Ep5wozK5716uwpbPYeCBatJ5gmdK5P59mY6w"  # Replace with an actual mint address

    # Replace with a metadata address
    metadata_address = "Gh9Ej3q9Ep5wozK5716uwpbPYeCBatJ5gmdK5P59mY6w"  # Replace with an actual metadata address

    # NFT metadata
    name = "Awesome NFT"
    symbol = "ANFT"
    uri = "https://example.com/nft/metadata.json"

    solana_client = Client("https://api.devnet.solana.com")

    # Create the NFT
    transaction_id = create_nft(
        funder_private_key, metadata_program_id, mint_address, metadata_address, name, symbol, uri, solana_client
    )

    if transaction_id:
        print(f"NFT created successfully! Transaction ID: {transaction_id}")
    else:
        print("Failed to create NFT.")
