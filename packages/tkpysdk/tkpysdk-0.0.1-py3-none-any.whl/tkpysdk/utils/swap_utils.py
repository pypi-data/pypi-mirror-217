# Author: Sirui Ray Li
# Created: 7/5/23
# Version: 1.0
# Description:
from typing import Optional, Dict, Any
import requests

from tkpysdk.utils.signature import create_300k_header
from tkpysdk.utils.config import BASE_URL_300K_API
from tkpysdk.utils.shared_utils import process_response


def create_order(api_key: str, api_secret: str, network: str, post_body: Dict[str, Any],
                 timeout: Optional[int] = 120):
    """

    @param api_key:
    @param api_secret:
    @param network:
    @param post_body: In the form of CreateOrderParams {
                                                          routeHashes: string[];
                                                          expireTimestamp?: number;
                                                          gasPrice?: string;
                                                          maxPriorityFeePerGas?: string;
                                                          walletAddress: string;
                                                          amountIn: number;
                                                          amountInRaw?: string;
                                                          amountOutMin: number;
                                                          nonce?: number;
                                                          strategyId?: number;
                                                          strategyType?: number;
                                                          traderAddress: string;
                                                          newClientOrderId?: string;
                                                          dynamicGasPrice?: boolean;
                                                          estimateGasOnly?: boolean | 'skip'; # set estimateGasOnly = False to actually send transactions on chain
                                                        }
    @param timeout:
    @return:
    """
    path = f"/api/{network}/v1/order"
    url = f"{BASE_URL_300K_API}{path}"

    headers = create_300k_header(method='POST',
                                 path=path,
                                 api_key=api_key,
                                 api_secret=api_secret,
                                 post_data=post_body)
    res = requests.post(url, json=post_body, timeout=timeout, headers=headers)
    return process_response(res)
