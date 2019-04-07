import requests
import bs4
from keys import *
import json
import os
import time

#(b'Authorization', b'Bearer f4e64eb5-67e9-4167-8cbe-93b4629ee82d')

def reset_token():
	try:
		open("rm done")
	except:
		pass
	os.system("./start.sh &")
	while not os.path.exists("done"):
		print("WAITING FOR FILE")
		time.sleep(1)
	os.system("./stopScript.sh")
	print(open("headers.json").read())
	os.system("rm done")


def long_lat_to_address(longVal, lat):
	res = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(lat, longVal, google))
	return res.json()['results'][0]['formatted_address']

def address_to_long_lat(address):
	address = address.replace(" ", "+")
	res = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, google))
	return res.json()['results'][0]['geometry']['location']

def find_stores(longLatDict):
	res = requests.get("https://onmyj41p3c.execute-api.us-west-2.amazonaws.com/prod/getStoresByCoordinates?latitude={}&longitude={}&count=50&radius=20&ignoreLoadingBar=false".format(longLatDict['lat'], longLatDict['lng']))
	return res.json()

def store_by_zip(zipCode):
	print(zipCode)
	a = address_to_long_lat(zipCode)
	return find_stores(a)

def get_info_store(zipCode, storeNum):
	a = store_by_zip(str(zipCode))
	for val in a:
		if val['id'] == str(storeNum):
			return "The store on {} in {} {}".format(val['name'], val['location']['address']["addressLocality"], val['location']['address']["addressRegion"])

def check_stock(itemNum, locations):
	headers = json.load(open('headers.json'))
	#print "{}".format([str(x) for x in locations])
	data = '{"products":["' + itemNum + '"],"locations":' + "{}".format(json.dumps([str(x) for x in locations])) + '}'
	response = requests.post('https://core.saas.api.t-mobile.com/supplychain/inventoryavailability/v1/inventory/search/inventory-details-view', headers=headers, data=data)
	#print response.text
	if 'Invalid Access Token' in str(response.text):
		print("RESETTING TOKEN")
		reset_token()
		headers = json.load(open('headers.json'))
		#print "{}".format([str(x) for x in locations])
		data = '{"products":["' + itemNum + '"],"locations":' + "{}".format(json.dumps([str(x) for x in locations])) + '}'
		response = requests.post('https://core.saas.api.t-mobile.com/supplychain/inventoryavailability/v1/inventory/search/inventory-details-view', headers=headers, data=data)
		#print response.text
	return response.json()


def search_query(query):
	res = requests.get("https://sp10050ebc.guided.ss-omtrdc.net/?category=device&count=20&do=redesign&i=1&is_auth=0&mlay=Grid&page=1&q={}&rank=device_rank".format(query.replace(" ", "+")))
	y = res.json()
	a = []
	g = []
	for val in y.get("suggestions", []):
		a.append(val['suggestion'])
	for val in y['resultsets']:
		for v in val['results']:
			g.append(v['OM_SKU'])
	return g

def get_suggestions(query):
	res = requests.get("https://sp10050ebc.guided.ss-omtrdc.net/?category=device&count=20&do=redesign&i=1&is_auth=0&mlay=Grid&page=1&q={}&rank=device_rank".format(query.replace(" ", "+")))
	y = res.json()
	a = []
	for val in y.get("suggestions", []):
		a.append(val['suggestion'])
	return a

def search(query):
	y = []
	a = [query] + get_suggestions(query)
	for val in a:
		y += search_query(val)
		if len(y) > 0:
			return y

if __name__ == '__main__':
	#reset_token()
	stores = [x['id'] for x in store_by_zip('29680')]
	#for store in stores:
	#	raw_input(get_info_store('29680', store))
	stockInfo = check_stock("190198451972", stores)
	for val in stockInfo.get('result', {}).get('inventoryAvailabilityList', []):
		try:
			s = val['storeId']
			q = val['skuDetails'][0]['quantity']['availableQuantity']
			print("Store ID: {} | Availability: {}".format(s, q))
		except:
			pass
	raw_input(" ")
	for val in store_by_zip("29680"):
		print val['id']
	query = raw_input("Query: ")
	val = search(query)
	raw_input(val)
	if len(val) > 0:
		print check_stock(val[0], stores)

#x = get_suggestions("ihpone xs")
#print search("ihpne xs")
#print x
#print x
