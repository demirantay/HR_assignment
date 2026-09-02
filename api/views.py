import json
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3

ABI_PATH = Path(__file__).resolve().parent / "contracts" / "escrow_abi.json"
with open(ABI_PATH) as f:
    ESCROW_ABI = json.load(f)


def get_contract():
    """Returns a connected web3 contract instance, or None if not configured."""
    if not settings.WEB3_RPC_URL or not settings.ESCROW_CONTRACT_ADDRESS:
        return None
    w3 = Web3(Web3.HTTPProvider(settings.WEB3_RPC_URL))
    return w3.eth.contract(
        address=Web3.to_checksum_address(settings.ESCROW_CONTRACT_ADDRESS),
        abi=ESCROW_ABI,
    )


def contract_status(request):
    """GET /api/contract/ - is the API wired up to a contract?"""
    configured = bool(settings.WEB3_RPC_URL and settings.ESCROW_CONTRACT_ADDRESS)
    return JsonResponse({
        "configured": configured,
        "rpc_url": settings.WEB3_RPC_URL,
        "contract_address": settings.ESCROW_CONTRACT_ADDRESS,
    })


def get_balance(request):
    """GET /api/contract/balance/ - reads getBalance() from the contract."""
    contract = get_contract()
    if contract is None:
        return JsonResponse({"error": "Contract not configured yet"}, status=503)
    try:
        balance = contract.functions.getBalance().call()
        return JsonResponse({"balance_wei": balance})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=502)


def get_listing(request, nft_id):
    """GET /api/contract/listing/<nft_id>/ - reads isListed/purchasePrice/buyer for one NFT."""
    contract = get_contract()
    if contract is None:
        return JsonResponse({"error": "Contract not configured yet"}, status=503)
    try:
        data = {
            "nft_id": nft_id,
            "is_listed": contract.functions.isListed(nft_id).call(),
            "purchase_price_wei": contract.functions.purchasePrice(nft_id).call(),
            "buyer": contract.functions.buyer(nft_id).call(),
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=502)


# MORE ENDPOINTS IN PRODUCTION ETC ...