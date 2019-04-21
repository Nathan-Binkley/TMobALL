import search
import stores
import threading
import json
import time

def get_inventory_for_all(sku):
	a = {}
	def sear(id):
		for i in range(5):
			for val in search.check_stock(sku, id)['result']['inventoryAvailabilityList']:
				#print(len(a))
				try:
					#print val['storeId']
					#print("{} - {}".format(val['storeId'], val['skuDetails'][0]['quantity']['availableQuantity']))
					a[val['storeId']] = val['skuDetails'][0]['quantity']['availableQuantity']
				except:
					pass
	threads = [threading.Thread(target=sear, args=(ar,)) for ar in stores.get_ids(50)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return a




if __name__ == '__main__':
	item = "610214656414"
	items = []
	for val in json.load(open("inventory.json"))['values']['products']:
		raw_input(val)
		for v in val["skuCode"].split("|"):
			if v not in items:
				items.append(v)
	while True:
		db = {}
		fileName = str(int(time.time()))
		i = 0
		for item in items:
			print("Checking: {}".format(item))
			try:
				db[item] = get_inventory_for_all(item)
				with open(fileName + '.json', 'w') as fp:
					json.dump(db, fp, indent=4)
			except:
				print("ERROR")
			print(i)
			i += 1
			print("Finished: {} | Found: {}".format(item, len(db[item])))
		print("Sleeping")
		time.sleep(60 * 60)
