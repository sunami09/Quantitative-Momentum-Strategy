from apikey import *
import pandas as pd
import sys
from scipy import stats
from toexcel import *
from requesturl import get_data
from statistics import mean
from orders import *

url = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={stockapi}"
data = get_data(url)
symbol = ""
for ticker in data:
   if symbol != "":
      symbol+=','
   symbol += ticker['symbol']

url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={stockapi}"
data = get_data(url)

columns = ['Name', 'Symbol', 'Price ($)', 'Market Cap ($)', '1D (%)', '5D (%)', '1M (%)', '3M (%)', '1D', '5D', '1M', '3M', 'HQM Score','H', 'M', 'TM', 'Shares to Buy', 'Weight (%)', 'Portfolio Allocation ($)']
df = pd.DataFrame(columns=columns)

for quote in data:
    df = df._append(
       pd.Series([
          quote['name'],
          quote['symbol'],
          quote['price'],
          quote['marketCap'],
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A'
       ], index = columns),
       ignore_index = True
    )

url = f"https://financialmodelingprep.com/api/v3/stock-price-change/{symbol}?apikey={stockapi}"
data = get_data(url)
time_frame = ['1D', '5D', '1M', '3M']
for i in range(0, len(df.index)):
   
   if df.loc[i, 'Symbol'] != data[i]['symbol']:
      sys.exit("Batch Request Failed")
   else:
      df.loc[i, '1D (%)'] = data[i]['1D']
      df.loc[i, '5D (%)'] = data[i]['5D']
      df.loc[i, '1M (%)'] = data[i]['1M']
      df.loc[i, '3M (%)'] = data[i]['3M']
      
for i in range(0, len(df.index)):
   for time in time_frame:
      df.loc[i, time] = stats.percentileofscore(df[f'{time} (%)'], df.loc[i, f'{time} (%)'])

for i in range(0, len(df.index)):
   d1 = df.loc[i, '1D']
   d5 = df.loc[i, '5D'] * 1.5
   m1 = df.loc[i, '1M'] * 1.25
   m3 = df.loc[i, '3M'] * 0.25
   df.loc[i, 'HQM Score'] = mean([d1, d5, m1, m3])



df.sort_values(by = 'HQM Score', ascending=False, inplace=True)
df = df[:50]
df.reset_index(inplace=True)

total_asset = 0
total_h = 0
for i in range(0, len(df.index)):
   total_asset += df.loc[i, 'Market Cap ($)']
   total_h += df.loc[i, 'HQM Score']

portfolio = float(input("Enter Your Portfolio Size: "))

for i in range(0, len(df.index)):
   df.loc[i, 'H'] = (df.loc[i, 'HQM Score'] / total_h) * 100
   df.loc[i, 'M'] = (df.loc[i, 'Market Cap ($)']/ total_asset) * 100
   df.loc[i, 'TM'] = (df.loc[i, 'H'] * 0.85) + (df.loc[i, 'M'] * 0.15)

total_w = 0
for i in range(0, len(df.index)):
   total_w += df.loc[i, 'TM']
percent = 0
for i in range(0, len(df.index)):
   df.loc[i, 'Weight (%)'] = (df.loc[i, 'TM'] / total_w) * 100
   percent += df.loc[i, 'Weight (%)']

# 'Shares to Buy', 'Weight (%)', 'Portfolio Allocation ($)'
money = 0
for i in range(0, len(df.index)):
   df.loc[i, 'Portfolio Allocation ($)'] = round(portfolio * (df.loc[i, 'Weight (%)']/100))
   money += df.loc[i, 'Portfolio Allocation ($)']
   df.loc[i, 'Shares to Buy'] = df.loc[i, 'Portfolio Allocation ($)']/df.loc[i, 'Price ($)']





df.drop(['index', '1D (%)', '5D (%)', '1M (%)', '3M (%)', '1D', '5D', '1M', '3M', 'Market Cap ($)', 'M', 'H', 'TM'], axis = 1, inplace=True)

for i in range(0, len(df.index)):
   order(df.loc[i, 'Symbol'], df.loc[i, 'Shares to Buy'], 'buy')

to_excel(df)
