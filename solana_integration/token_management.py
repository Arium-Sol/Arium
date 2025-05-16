# solana_integration/token_management.py

from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from spl.token.instructions import initialize_mint, MintInstructions, mint_to, MintToParams,  get_associated_token_address, transfer, TransferParams
from solders.pubkey import Pubkey
from solders.hash import Hash
from solana.rpc.api import Client
from solana.transaction import Transaction, AccountMeta, TransactionInstruction
from solana.keypair import Keypair
import base64
from spl.token._layouts import MINT_LAYOUT

def create_mint(
    funder_private_key: str,
    decimals: int,
    mint_authority: Pubkey,
    freeze_authority: Pubkey,
    solana_client: Client,
) -> Pubkey | None:
    """Creates a new SPL token mint."""
    try:
        funder_keypair = Keypair.from_bytes(base64.b64decode(funder_private_key))
        funder_pubkey = funder_keypair.pubkey()

        new_mint_keypair = Keypair()
        new_mint_pubkey = new_mint_keypair.pubkey()

        # Get recent blockhash
        latest_blockhash = solana_client.get_latest_blockhash().value.blockhash

        # Calculate rent-exempt minimum balance
        rent_exempt_minimum_balance = solana_client.get_minimum_balance_for_rent_exemption(MINT_LAYOUT.sizeof()).value

        # Create transaction
        transaction = Transaction()
        transaction.recent_blockhash = latest_blockhash
        transaction.fee_payer = funder_pubkey

        # Instruction 1: Create account for the mint
        transaction.add(
            AccountMeta(pubkey=funder_pubkey, is_signer=True, is_writable=True),
            AccountMeta(pubkey=new_mint_pubkey, is_signer=False, is_writable=True),
            AccountMeta(pubkey=Pubkey.from_string("11111111111111111111111111111111"), is_signer=False, is_writable=False),  # System Program
        )

        # Instruction 2: Initialize the mint
        transaction.add(
            initialize_mint(
                MintInstructions.InitializeMintParams(
                    mint=new_mint_pubkey,
                    decimals=decimals,
                    mint_authority=mint_authority,
                    freeze_authority=freeze_authority,
                    program_id=TOKEN_PROGRAM_ID,
                )
            )
        )

        # Sign the transaction
        transaction.sign(funder_keypair, new_mint_keypair)

        # Send the transaction
        result = solana_client.send_raw_transaction(transaction.serialize())

        return new_mint_pubkey

    except Exception as e:
        print(f"Error creating mint: {e}")
        return None

def mint_tokens(
    mint: Pubkey,
    destination: Pubkey,
    amount: int,
    mint_authority_private_key: str,
    solana_client: Client,
) -> str | None:
    """Mints new tokens to the specified destination."""
    try:
        mint_authority_keypair = Keypair.from_bytes(base64.b64decode(mint_authority_private_key))
        mint_authority_pubkey = mint_authority_keypair.pubkey()

        # Get recent blockhash
        latest_blockhash = solana_client.get_latest_blockhash().value.blockhash

        # Create transaction
        transaction = Transaction()
        transaction.recent_blockhash = latest_blockhash
        transaction.fee_payer = mint_authority_pubkey

        # Add mint instruction
        transaction.add(
            mint_to(MintToParams(
                mint=mint,
                dest=destination,
                amount=amount,
                mint_authority=mint_authority_pubkey,
                program_id=TOKEN_PROGRAM_ID,
            ))
        )

        # Sign the transaction
        transaction.sign(mint_authority_keypair)

        # Send the transaction
        result = solana_client.send_raw_transaction(transaction.serialize())
        return result.value

    except Exception as e:
        print(f"Error minting tokens: {e}")
        return None

if __name__ == "__main__":
    # Replace with your actual private key (store securely!)
    funder_private_key = "YOUR_PRIVATE_KEY_ENCODED_IN_BASE64"

    # Replace with the desired decimals for your token
    decimals = 9

    # Define the mint authority (can be the same as the funder)
    mint_authority = Keypair().pubkey()  # Replace with an actual Pubkey if needed

    # Define the freeze authority (can be the same as the funder, or None)
    freeze_authority = Keypair().pubkey()  # Replace with an actual Pubkey if needed

    solana_client = Client("https://api.devnet.solana.com")

    # Create the mint
    mint_pubkey = create_mint(funder_private_key, decimals, mint_authority, freeze_authority, solana_client)

    if mint_pubkey:
        print(f"Mint created successfully! Mint address: {mint_pubkey}")
    else:
        print("Failed to create mint.")
