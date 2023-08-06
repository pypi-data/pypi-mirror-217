# Author: Sirui Ray Li
# Created: 7/5/23
# Version: 1.0
# Description:

from typing import Any, Dict, List
import requests

from tkpysdk.utils.signature import create_300k_header
from tkpysdk.utils.config import BASE_URL_300K_API
from tkpysdk.utils.shared_utils import process_response


def create_position(api_key: str,
                    api_secret: str,
                    network: str,
                    post_body: Dict[str, any]) -> Dict[str, Any]:
    """

    @param api_key:
    @param api_secret:
    @param network:
    @param post_body: format: {
                                traderAddress: string;
                                walletAddress: string;
                                token0: string;
                                token1: string;
                                amount0Desired: number;
                                amount1Desired: number;
                                priceLower: string;
                                priceUpper: string;
                                fee: number;
                                burnPositionId?: number;
                                newClientOrderId?: string;
                                gasPrice?: string;
                                maxPriorityFeePerGas?: string;
                                estimateGasOnly?: boolean; # set estimateGasOnly = False to actually send transactions on chain
                                strategyId?: number;
                                strategyType?: number;
                              }
    @return: CreatePositionResponse {
                                      blockHash: string;
                                      blockNumber: number;
                                      contractAddress: any;
                                      cumulativeGasUsed: number;
                                      effectiveGasPrice: number;
                                      from: string;
                                      gasUsed: number;
                                      logsBloom: string;
                                      status: boolean;
                                      to: string;
                                      transactionHash: string;
                                      transactionIndex: number;
                                      type: string;
                                      events: any;
                                    }
    """
    
    path = f"/api/{network}/v1/v3-position"
    url = f"{BASE_URL_300K_API}{path}"
    headers = create_300k_header(method='POST',
                                 path=path,
                                 api_key=str(api_key),
                                 api_secret=str(api_secret),
                                 post_data=post_body)
    res = requests.post(url, json=post_body, headers=headers, timeout=120)
    return process_response(res)


def get_position_detail(network: str,
                        token_id: int,
                        api_key: str,
                        api_secret: str) -> Dict[str, Any]:
    """

    @param network:
    @param token_id:
    @param api_key:
    @param api_secret:
    @return: in the form of V3Position {
                                      tokenId: number;
                                      nonce: string;
                                      operator: string;
                                      token0: string;
                                      token1: string;
                                      fee: number;
                                      tickLower: number;
                                      tickUpper: number;
                                      liquidity: string;
                                      feeGrowthInside0LastX128: string;
                                      feeGrowthInside1LastX128: string;
                                      tokensOwed0: string;
                                      tokensOwed1: string;
                                      token0Symbol: string;
                                      token1Symbol: string;
                                      token0Decimals: number;
                                      token1Decimals: number;
                                      priceLower: string;
                                      priceUpper: string;
                                      priceLowerInvert: string;
                                      priceUpperInvert: string;
                                      amount0: string;
                                      amount1: string;
                                      sqrtPriceX96: string;
                                      tick: number;
                                      poolAddress: string;
                                    }
    """
    
    path = f"/api/{network}/v1/v3-position-detail"
    url = f"{BASE_URL_300K_API}{path}?tokenId={token_id}"
    headers = create_300k_header(method='GET',
                                 path=path,
                                 api_key=api_key,
                                 api_secret=api_secret,
                                 post_data={})
    res = requests.get(url, headers=headers)
    return process_response(res)


def get_position_details(network: str,
                         wallet_address: str,
                         api_key: str,
                         api_secret: str) -> List[Dict[str, Any]]:
    """

    @param network:
    @param wallet_address:
    @param api_key:
    @param api_secret:
    @return: In the form of V3Position[] (list of V3Position)
                V3Position is in the form of {
                                              tokenId: number;
                                              nonce: string;
                                              operator: string;
                                              token0: string;
                                              token1: string;
                                              fee: number;
                                              tickLower: number;
                                              tickUpper: number;
                                              liquidity: string;
                                              feeGrowthInside0LastX128: string;
                                              feeGrowthInside1LastX128: string;
                                              tokensOwed0: string;
                                              tokensOwed1: string;
                                              token0Symbol: string;
                                              token1Symbol: string;
                                              token0Decimals: number;
                                              token1Decimals: number;
                                              priceLower: string;
                                              priceUpper: string;
                                              priceLowerInvert: string;
                                              priceUpperInvert: string;
                                              amount0: string;
                                              amount1: string;
                                              sqrtPriceX96: string;
                                              tick: number;
                                              poolAddress: string;
                                            }
    """
    
    path = f"/api/{network}/v1/v3-positions"
    url = f"{BASE_URL_300K_API}{path}?walletAddress={wallet_address}"
    headers = create_300k_header(method='GET',
                                 path=path,
                                 api_key=api_key,
                                 api_secret=api_secret,
                                 post_data={})
    res = requests.get(url, headers=headers)
    return process_response(res)


def remove_liquidity_and_burn(api_key: str, api_secret: str, network: str, post_body: Dict[str, any]):
    """

    @param api_key:
    @param api_secret:
    @param network:
    @param post_body: format: {
                                positionId: number;
                                walletAddress: string;
                                traderAddress: string;
                                newClientOrderId?: string;
                                nonce?: number;
                                gasPrice?: string;
                                maxPriorityFeePerGas?: string;
                                estimateGasOnly?: boolean; # set estimateGasOnly = False to actually send transactions on chain
                                strategyId?: number;
                                strategyType?: number;
                              }
    @return:
    """
    
    path = f"/api/{network}/v1/remove-v3-position"
    url = f"{BASE_URL_300K_API}{path}"
    headers = create_300k_header(method='POST',
                                 path=path,
                                 api_key=api_key,
                                 api_secret=api_secret,
                                 post_data=post_body)
    res = requests.post(url, json=post_body, headers=headers, timeout=120)
    return process_response(res)
