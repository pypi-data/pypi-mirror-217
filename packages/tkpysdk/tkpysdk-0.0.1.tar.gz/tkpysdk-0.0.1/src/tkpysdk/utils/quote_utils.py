# Author: Sirui Ray Li
# Created: 7/5/23
# Version: 1.0
# Description:

from dataclasses import dataclass

import requests
from typing import Optional, Tuple, List, Dict, Any

from tkpysdk.utils.signature import create_300k_header
from tkpysdk.utils.config import BASE_URL_300K_API
from tkpysdk.utils.shared_utils import process_response

QuoteArr = Tuple[float, float, str, str, float]


@dataclass
class OrderbookResponse:
    symbol: str
    amount_usd: float
    last_update_ts: int
    asks: Optional[List[QuoteArr]] = None
    bids: Optional[List[QuoteArr]] = None


def get_erc20_balance(api_key: str, api_secret: str, network: str, query: Dict[str, str]) -> str:
    """

    @param api_key:
    @param api_secret:
    @param network:
    @param query: formate: {
                            walletAddress: string;
                            erc20TokenAddress: string;
                          }
    @return:
    """

    path = f"/api/{network}/v1/get-balance"
    url = f"{BASE_URL_300K_API}{path}"
    headers = create_300k_header(method='GET',
                                 path=path,
                                 api_secret=api_secret,
                                 api_key=api_key,
                                 post_data={})
    res = requests.get(url, params=query, headers=headers)
    return process_response(res)


def get_order_book(api_key: str, api_secret: str, network: str, query: Dict[str, any]) -> Dict[str, Any]:
    """

    @param api_key:
    @param api_secret:
    @param network:
    @param query: format:
                    {
                    symbol: string;
                    side: 'bid' | 'ask';
                    // if LINK/USDC, can use amountUSD to specify how much USD trade to quote
                    amountUSD?: number;
                    // if LINK/WETH, can use amountQuote to specify how much WETH worth of trade to quote
                    amountQuote?: number;
                  }
    @return: In the form of: OrderbookResponse {
                                                  symbol: string;
                                                  amountUSD: number;
                                                  lastUpdateTs: number;
                                                  // [price, amountAsset, hash, path, gasUSD]
                                                  asks?: QuoteArr[];
                                                  bids?: QuoteArr[];
                                                }
    """

    path = f"/api/{network}/v1/rfq/orderbook"
    url = f"{BASE_URL_300K_API}{path}"
    headers = create_300k_header(method='GET',
                                 path=path,
                                 api_key=api_key,
                                 api_secret=api_secret,
                                 post_data={})
    amount_usd = query.get('amountUSD')
    amount_quote = query.get('amountQuote')
    if not amount_usd and not amount_quote:
        raise ValueError("either amountQuote or amountUSD is required")
    res = requests.get(url, params=query, headers=headers)
    return process_response(res)
