import config, json, numpy, talib, pprint, csv
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "BNBUSDT"
TRADE_QUANTITY = 0.5

closes = []
in_position = False

class User_Info(object):
  makerCommission: 0
  takerCommission: 0
  buyerCommission: 0
  sellerCommission: 0
  bnbBalance: 0
  usdtBalance: 0

  def __init__(self, makerCommission, 
               takerCommission, 
               buyerCommission, 
               sellerCommission, 
               bnbBalance,
               usdtBalance):
    self.makerCommission = makerCommission
    self.takerCommission = takerCommission
    self.buyerCommission = buyerCommission
    self.sellerCommission = sellerCommission
    self.bnbBalance = bnbBalance
    self.usdtBalance = usdtBalance

  def user_bnb_balance(self):
    return "bnbBalance: %s" % (self.bnbBalance)

  def user_usdt_balance(self):
    return "usdtBalance: %s" % (self.usdtBalance)

def load_user_info(makerCommission, 
                   takerCommission,
                   buyerCommission, 
                   sellerCommission, 
                   bnbBalance,
                   usdtBalance):
  user_info = User_Info(makerCommission, 
                        takerCommission, 
                        buyerCommission, 
                        sellerCommission, 
                        bnbBalance,
                        usdtBalance)
  return user_info


client = Client(config.API_KEY, config.API_SECRET)

#set url to testnet
#client.API_URL = 'https://testnet.binance.vision/api'
account_info = client.get_account()

# retrieve last 14 candlesticks so we can start to mesure the RSI from the first closed candle
last_14_klines = client.get_historical_klines(TRADE_SYMBOL, "5m", "12 hours ago UTC", limit=196)
for close in last_14_klines:
  closes.append(float(close[4]))

# remove last element of list (current candle that it's not closed)
closes.pop()

if account_info:
  bnbBalance = ""
  usdtBalance = ""
  for balance in account_info['balances']:
    if balance['asset'] == "BNB":
      bnbBalance = balance['free']
    elif balance['asset'] == "USDT":
      usdtBalance = balance['free']

  user = load_user_info(account_info['makerCommission'],
                        account_info['takerCommission'],
                        account_info['buyerCommission'],
                        account_info['sellerCommission'],
                        bnbBalance,
                        usdtBalance)

  print(user.user_bnb_balance())
  print(user.user_usdt_balance())

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
  try:
    print("sending order")
    print("symbol {}".format(symbol))
    print("side {}".format(side))
    print("type {}".format(order_type))
    print("quantity {}".format(quantity))
    # uncomment to trigger order
    #order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    #print(order)
  except Exception as e:
    print("an exception ocurred - {}".format(e))
    return False
  
  return True

def process_message(msg):

  global closes, in_position

  if msg['e'] == 'error':
    #error handling here D:
    print(msg['e'])
  else:
    print('message received')
    candle = msg['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
      print("candle closed at {}".format(close))
      closes.append(float(close))

      if len(closes) > RSI_PERIOD:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes, RSI_PERIOD)
        # print("all rsi calculated so far")
        # print(rsi)
        last_rsi = rsi[-1]
        print("the current rsi is {}".format(last_rsi))

        if (last_rsi > RSI_OVERBOUGHT):
          if in_position:
            print("OVERBOUGHT!! SELL!!")
            with open("trades.csv", "a") as fd:
              fd.write("sell price: {}".format(close))
            order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
            if order_succeeded:
              in_position = False
          else:
            print("it is overbought, but we don't own any.")
        
        if last_rsi < RSI_OVERSOLD:
          if in_position:
            print("It is oversold, but you already own it.")
          else:
            print("OVERSOLD!! BUY!!")
            with open("trades.csv", "a") as fd:
              fd.write("buy price: {}".format(close))
            order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
            if order_succeeded:
              in_position = True


bsm = BinanceSocketManager(client)
conn_key = bsm.start_kline_socket(TRADE_SYMBOL, process_message, interval=KLINE_INTERVAL_5MINUTE)
bsm.start()