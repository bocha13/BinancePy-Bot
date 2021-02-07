# Binance Trading Bot

### Configuration

1. On yout Binance account go to API Center, [create new](https://www.binance.com/en/my/settings/api-management) Api Key
2. create a new file on the root of the folder named `config.py` and populate with your keys (`sample_config.py` as example)
3. run `python3 app.py` to start the bot

4. _optional_: at the moment the trading order wont execute, it's disabled you can uncomment the part of the code indicated in the `app.py` file

### Status

Still work in progress, DO NOT USE.

### DISCLAIMER

> I am not responsible for anything done with this bot.
> You use it at your own risk.
> There are no warranties or guarantees expressed or implied.
> You assume all responsibility and liability.

details of JSON kline returned:  
e -> Event type  
E -> Event time (unix timestamp)  
s -> Symbol  
k {  
 t -> Kline start time (unix timestamp)  
 T -> Kline close time (unix timestamp)  
 s -> Symbol  
 i -> Interval  
 f -> First trade ID  
 L -> Last trade ID  
 o -> Open price
c -> Close price  
 h -> High price  
 l -> Low price  
 v -> Base asset volume  
 n -> Number of trades  
 x -> Is this kline closed?  
 q -> Quote asset volume  
 V -> Taker buy base asset volume  
 Q -> Taker buy quote asset volume  
 B -> Ignore  
}

return from client.get_historical_klines:

1499040000000, # Open time  
"0.01634790", # Open  
"0.80000000", # High  
"0.01575800", # Low  
"0.01577100", # Close  
"148976.11427815", # Volume  
1499644799999, # Close time  
"2434.19055334", # Quote asset volume  
308, # Number of trades  
"1756.87402397", # Taker buy base asset volume  
"28.46694368", # Taker buy quote asset volume  
"17928899.62484339" # Ignore
