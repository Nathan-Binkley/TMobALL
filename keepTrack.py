# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import search
import stores
import threading
import json
import time
import database
import os
lock = threading.Lock()
THREADS = 100
STORES_PER_THREAD = 80


X_VAL = 5648 / STORES_PER_THREAD

def get_inventory_for_all(sku):
	tempStores = list(stores.get_ids(X_VAL))
	a = {}
	def sear():
		while len(tempStores) > 0:
			try:
				lock.acquire()
				idVal = tempStores.pop(0)
				lock.release()
				for i in range(2):
					for val in search.check_stock(sku, idVal, isThreading=True)['result']['inventoryAvailabilityList']:
						#print(len(a))
						try:
							#print val['storeId']
							#print("{} - {}".format(val['storeId'], val['skuDetails'][0]['quantity']['availableQuantity']))
							a[val['storeId']] = val['skuDetails'][0]['quantity']['availableQuantity']
						except:
							pass
			except:
				try:
					lock.release()
				except:
					pass
				pass
	threads = [threading.Thread(target=sear) for i in range(THREADS)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return a




if __name__ == '__main__':
	item = "610214656414"
	items = []
	for val in json.load(open("inventory.json"))['values']['products']:
		#raw_input(val['productName'])
		if 'iphone' in str(val.get("productName", "").lower()):
			for v in val["skuCode"].split("|"):
				if v not in items:
					items.append(v)
	print("Searching for {} Iphones".format(len(items)))
	count = 0
	while True:
		db = {}
		fileName = str(int(time.time()))
		i = 0
		#raw_input(len(list(stores.get_ids(X_VAL))[0]))
		for item in items:
			print("Checking: {}".format(item))
			start = time.time()
			try:
				db[item] = get_inventory_for_all(item)
				with open(fileName + '.json', 'w') as fp:
					json.dump(db, fp, indent=4)
			except:
				print("ERROR")
			end = time.time()
			timeElapsed = end-start
			print("FINISHED | Time Elapsed: {}".format(timeElapsed))
			print(i)
			i += 1
			print("Finished: {} | Found: {}".format(item, len(db[item])))
		database.updateTable(fileName)
		count += 1
		print("Sleeping | Run: {}".format(count))
		os.system("echo {} > count.txt".format(count))
		time.sleep(60 * 60)
