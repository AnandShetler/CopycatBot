# CopycatBot
Implements a basic copycat trading bot and backtester for politicians public trading data using alpaca, beautiful soup, and yahoo finance.

## Setup

Create a file config.py. This should contain the following:

```
POL_URL = "https://www.capitoltrades.com/trades?politician=P000197" # Pick any politician from www.capitoltrades.com to mimic. This url is for John Curtis.
SEC_KEY =  # Enter Your Secret Key from Alpaca Here
PUB_KEY = # Enter Your Public Key from Alpaca Here
BASE_URL = 'https://paper-api.alpaca.markets' # This is the base URL for paper trading
```

## Notes
Upon realizing just how ineffective this method can be after implementing the backtester I decided not to fully implement the bot. The backtester is fully operational.
