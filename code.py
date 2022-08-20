# import libraries
from cryptocomapi import CryptoComApi
import pandas as pd
import asyncio
import cryptocom.exchange as cro
import requests
import time
from binance.client import Client


import numpy as np
#### crypto.com ####



# my crypto

api = CryptoComApi(api_key="your api key", secret_key="your secret key")
all_asset = api.get_account()
df= pd.DataFrame.from_dict(all_asset['coin_list'])
df1 = df.loc[df['locked'] != '0']

df3 = df1
df3['normal'] = pd.to_numeric(df3['normal'])
df3['locked'] = pd.to_numeric(df3['locked'])
df3['quantity'] = df3.apply(lambda row: row['normal'] + row['locked'], axis=1)
df3 = df3.reindex(['coin','normal','locked', 'quantity'], axis=1)
print(df3)

# crypto price

asset = api.get_market_trades()


res = dict((k, asset[k]) for k in ['crousdt', 'vetusdt', 'thetausdt',
 'chzusdt', 'linkusdt', 'csprusdt', 'usdcusdt'])

res['CRO'] = res.pop("crousdt")
res['VET'] = res.pop("vetusdt")
res['THETA'] = res.pop("thetausdt")
res['CHZ'] = res.pop("chzusdt")
res['LINK'] = res.pop("linkusdt")
res['CSPR'] = res.pop("csprusdt")
res['USDC'] = res.pop("usdcusdt")
df0 = pd.DataFrame(res.items(), columns=['coin', 'price'])

print(df0)

# i want to merge the two dataframes
df4 = pd.merge(df3, df0, on='coin')

# add the total value of each coin
df4['value'] = df4.apply(lambda row: row['quantity'] * row['price'], axis=1)
print(df4)

# export to csv
df4.to_csv('crypto_price.csv')

#### binance ####

# keys
api_key = 'your api key'
api_secret = 'your secret key'
client=Client(api_key,api_secret)

crypto = ['DOT', 'FTM', 'EGLD','BCD', 'USDT', 'USDC']
my_crypto = []
for i in range(len(crypto)):
    my_crypto.append(client.get_asset_balance(asset=crypto[i]))


df_bi = pd.DataFrame.from_dict(my_crypto)
df_bi['free'] = pd.to_numeric(df_bi['free'])
df_bi['locked'] = pd.to_numeric(df_bi['locked'])

df_bi['quantity'] = df_bi.apply(lambda row: row['free'] + row['locked'], axis=1)
print(df_bi)   
print(df0) 

#print(df_bi)
df_bi.rename(columns = {'asset':'coin', 'free':'normal'}, inplace = True)
print(df_bi)
# create the value "row usdt" because it is not in the dataframe crypto_price
row_usdt = df_bi.loc[df_bi['coin'] == 'USDT']
# add to row usdt price and value

df_bi = df_bi.append(row_usdt, ignore_index=True)

# crypto price

asset = api.get_market_trades()
resu = dict((k, asset[k]) for k in ['dotusdt', 'ftmusdt', 'egldusdt','usdcusdt'])

resu['DOT'] = resu.pop("dotusdt")
resu['FTM'] = resu.pop("ftmusdt")
resu['EGLD'] = resu.pop("egldusdt")
resu['USDC'] = resu.pop("usdcusdt")


df0_bi = pd.DataFrame(resu.items(), columns=['coin', 'price'])

print(df0_bi)

# merge df_bi and df0_bi
df_result_bi = pd.merge(df_bi, df0_bi, on='coin')
print(df_result_bi)
df_result_bi['value'] = df_result_bi.apply(lambda row: row['quantity'] * row['price'], axis=1)
print(df_result_bi)

# join datafram crypto.com and binance
df_all_rows = pd.concat([df_result_bi, df4])
df_all_rows = df_all_rows.append(row_usdt, ignore_index=True)



# delete the duplicated rows
#df_all_rows = df_all_rows.drop([5 , 6, 7])

print(df_all_rows)

# round all colums in the data frame
df_all_rows = df_all_rows.round(2)
print(df_all_rows)


