import urllib.request, json 
import requests
from _thread import start_new_thread
import sys
import time
import mysql.connector

def stock_analysis(stock_index, timeout):
	while True:
		print('made it to stock analysis with', stock_index)
		sitedata = download_stock_dat(stock_index)
		#print(sitedata)
		data=sitedata.json()
		#print(data)
		stocktime = []
		timekeys = ''
		mydb = mysql.connector.connect(host="nottellingyou",
										user="nottellingyou",
										passwd="nottellingyou",
										database="nottellingyou")
		dbcursor=mydb.cursor()
		sql="select ifnull(max(tickerdate), '0000-00-00 00:00:00') last_ticket_date "
		sql+=" from compfilemgmt.stockdat"
		sql+=" where ticker='%s'" % (stock_index)
		dbcursor.execute(sql)
		results=dbcursor.fetchall()
		for x in results:
			last_ticket_date=x[0]
		#print (data['Time Series (1min)'].keys())
		for time_periods in data['Time Series (Daily)'].keys():
			if time_periods > last_ticket_date:
				stocktime.append(time_periods)
			#print(time_periods)
		for time_period in stocktime:
			timekeys=list(data['Time Series (Daily)'][time_period].keys())
			collatedata = []
			for keys in timekeys:
				collatedata.append(data['Time Series (Daily)'][time_period][keys])
				print(time_period, keys, data['Time Series (Daily)'][time_period][keys])
			#print(data['Time Series (1min)'][time_period][values])	
			sql="insert into compfilemgmt.stockdat(ticker, tickerdate, openval, closeval, low, close, adjustclose, volume, dividend, splitcoeff)"
			sql+=" values ('%s','%s','%s','%s','%s','%s','%s', '%s', '%s', '%s')" %(stock_index, 
																	time_period, 
																	collatedata[0], 
																	collatedata[1], 
																	collatedata[2],
																	collatedata[3],
																	collatedata[4],
																	collatedata[5],
																	collatedata[6],
																	collatedata[7])
			dbcursor.execute(sql)
		mydb.commit()	
		time.sleep(86400)
	
def download_stock_dat(stock_index):
	print('downloading data for', stock_index)
	value='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol=&interval=1min&apikey='
	value=value[0:value.find('symbol=')+len('symbol=')]+stock_index+value[value.find('symbol=')+len('symbol='):len(value)]
	value+='nottellingyou'
	print('submitted request to site')
	print(requests.get(value))
	print(value)
	return requests.get(value)
	
stocks=['MSFT','NNN','SO','T','O','HASI','STAG','XLU','XLP','SPHD','ED','UNP','EMR','OHI','HD','VHT','LMT']
numstocks=len(stocks)
timer=numstocks*60
for stock in stocks:
	start_new_thread(stock_analysis, (stock,timer,))
	time.sleep(60)
c = input("Type something to quit.")
#with urllib.request.urlopen(value) as url:
#    data = json.loads(url.read().decode())
#    print(data)

#print(data['Time Series (1min)'][var]['1. open'])

#for key, value in data['Time Series (1min)']['2018-07-16 16:00:00']:
#    print("key: {} | value: {}".format(key, value))

