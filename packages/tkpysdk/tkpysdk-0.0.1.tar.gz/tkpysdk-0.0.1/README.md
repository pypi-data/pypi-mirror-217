# 300k-python-sdk

pip install git+https://github.com/300k-xyz/python-sdk.git#egg=tkpysdk
 
 ### usage
```
from tkpysdk import get_order_book, create_order

order_book = get_order_book(network=self.NETWORK,
  query={
      'symbol': 'CELO/cUSD',
      'side': 'bid',
      'amountUSD': 100,
  },
  api_secret=self.API_SECRET,
  api_key=self.API_KEY)
ask_price = order_book['bids'][0][0]
allowed_slippage = 0.001  # Replace with the actual value
wallet_address = self.WALLET_ADDRESS  # Replace with the actual value
amount_in = 200  # Replace with the actual value
trader_address = self.TRADER_ADDRESS  # Replace with the actual value
# create an order to do swap
post_body = {
    'routeHashes': [order_book['bids'][0][2]],
    'expireTimestamp': int(time.time() + 12),
    'walletAddress': wallet_address,
    'amountIn': amount_in,
    'amountOutMin': (amount_in / ask_price) * (1 - allowed_slippage),
    'strategyId': 1,
    'strategyType': 2,
    'traderAddress': trader_address,
    'newClientOrderId': f"test-{int(time.time())}",
    'dynamicGasPrice': False,
    'estimateGasOnly': True  # set estimateGasOnly = False to actually send transactions on chain
}
result = create_order(api_key=self.API_KEY,
  api_secret=self.API_SECRET,
  network=self.NETWORK,
  post_body=post_body)
print(result)
```

### more usage examples
see examples here
[Sample usage](src/tests/test_utils.py)
