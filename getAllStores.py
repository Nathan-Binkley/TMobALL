import requests
import bs4
import csv
from pyzipcode import ZipCodeDatabase
import random
import json
import threading

lock = threading.Lock()

with open('Economics.csv', 'rb') as f:
	reader = csv.reader(f)
	your_list = list(reader)



zcdb = ZipCodeDatabase()

allVals = []

for val in your_list:
	try:
		a = zcdb[val[0]]
		allVals.append((a.latitude, a.longitude))
	except Exception as exp:
		pass
x = len(allVals)
random.shuffle(allVals)
g = []
idList = []

url = "https://onmyj41p3c.execute-api.us-west-2.amazonaws.com/prod/getStoresByCoordinates?latitude=33.76969909667969&longitude=-84.377197265625&count=50&radius=2000&ignoreLoadingBar=false"
urls = []

def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def grabSite():
	url = "https://onmyj41p3c.execute-api.us-west-2.amazonaws.com/prod/getStoresByCoordinates?latitude={0}&longitude={1}&count=50&radius=2000&ignoreLoadingBar=false"
	for i, val in enumerate(allVals):
		a = val[0]
		b = val[1]
		try:
			ur = url.format(a, b)
			#print url
			urls.append(ur)
		except Exception as exp:
			print exp
	return g

def checkURLs(urlsZ):
	for ur in urlsZ:
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			res = requests.get(ur, headers=headers, timeout=10)
			#print res.text
			urls.remove(ur)
			print("FOUND: {} | URLS FINISHED: {}/30000".format(len(g), len(urls)))
			for val in res.json():
				lock.acquire()
				if val['id'] not in idList:
					g.append(val)
					idList.append(val['id'])
				lock.release()
		except Exception as exp:
			try:
				lock.release()
			except:
				pass
			print exp
	lock.acquire()
	with open('stores.json', 'w') as fp:
		json.dump(g, fp, indent=4)
	lock.release()



if __name__ == '__main__':
	grabSite()
	print len(urls)
	urlVals = chunks(urls, int(len(urls)/100))
	threads = [threading.Thread(target=checkURLs, args=(ar,)) for ar in urlVals]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()


