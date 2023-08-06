# Author: Sirui Ray Li
# Created: 7/5/23
# Version: 1.0
# Description:
import time
from typing import Dict, Optional, Union
from urllib.parse import urljoin
import requests
from tkpysdk.utils.signature import create_300k_header
from tkpysdk.utils.shared_utils import process_response
from tkpysdk.utils.config import BASE_URL_300K_API


def get_order_history(
        api_key: str,
        api_secret: str,
        network: str,
        query: Dict[str, Optional[Union[str, int]]]
):
    """

    @param api_key:
    @param api_secret:
    @param network:
    @param query: format: {
                            walletAddress: string;
                            startTime?: number;
                            endTime?: number;
                            limit?: number;
                            tokenInSymbol?: string;
                            tokenOutSymbol?: string;
                            }
    @return:
    """
    path = f"/api/{network}/v1/history-orders"
    url = urljoin(BASE_URL_300K_API, path)
    headers = create_300k_header(method='GET',
                                 path=path,
                                 api_secret=api_secret,
                                 api_key=api_key,
                                 post_data=query)
    res = requests.get(url, params=query, headers=headers)

    return process_response(res)
