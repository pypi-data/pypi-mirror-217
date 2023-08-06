# Author: Sirui Ray Li
# Created: 7/5/23
# Version: 1.0
# Description:

from enum import Enum


class Network(Enum):
    ethereum = 'ethereum'
    arbitrum = 'arbitrum'
    polygon = 'polygon'
    bsc = 'bsc'
    celo = 'celo'
    optimism = 'optimism'
    avalanche = 'avalanche'


class ChainId(Enum):
    MAINNET = 1
    ROPSTEN = 3
    RINKEBY = 4
    GÖRLI = 5
    KOVAN = 42
    OPTIMISM = 10
    OPTIMISTIC_KOVAN = 69
    BSC = 56
    ARBITRUM_ONE = 42161
    ARBITRUM_RINKEBY = 421611
    POLYGON = 137
    POLYGON_MUMBAI = 80001
    CELO = 42220
    CELO_ALFAJORES = 44787
    GNOSIS = 100
    MOONBEAM = 1284
    AVALANCHE = 43114


network_to_chainid_map = {
    'ethereum': ChainId.MAINNET,
    'arbitrum': ChainId.ARBITRUM_ONE,
    'polygon': ChainId.POLYGON,
    'bsc': ChainId.BSC,
    'celo': ChainId.CELO,
    'optimism': ChainId.OPTIMISM,
    'avalanche': ChainId.AVALANCHE
}

chainid_to_network_map = {
    ChainId.MAINNET: 'ethereum',
    ChainId.ARBITRUM_ONE: 'arbitrum',
    ChainId.POLYGON: 'polygon',
    ChainId.BSC: 'bsc',
    ChainId.CELO: 'celo',
    ChainId.OPTIMISM: 'optimism',
    ChainId.AVALANCHE: 'avalanche'
}


def get_chain_id_from_network(network: str) -> ChainId:
    if network in network_to_chainid_map:
        return network_to_chainid_map[network]
    else:
        raise ValueError(f"getChainIdFromNetwork unsupported network {network}")


def get_network_from_chain_id(chain_id: ChainId) -> str:
    if chain_id in chainid_to_network_map:
        return chainid_to_network_map[chain_id]
    else:
        raise ValueError(f"unsupported chainId {chain_id}")
