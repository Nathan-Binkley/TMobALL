import search
import stores
import threading
import json

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
	threads = [threading.Thread(target=sear, args=(ar,)) for ar in stores.get_ids(100)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return a




if __name__ == '__main__':
	item = "610214656414"
	"""for val in search.check_stock(item, stores.get_ids()[:100])['result']['inventoryAvailabilityList']:
					#print val
					try:
						#print val['storeId']
						print("{} - {}".format(val['storeId'], val['skuDetails'][0]['quantity']['availableQuantity']))
					except Exception as exp:
						print exp
						pass"""
	g = get_inventory_for_all(item)
	with open('secondRun.json', 'w') as fp:
		json.dump(g, fp, indent=4)
	for k, v in g.iteritems():
		print("Store: {} | Quantity: {}".format(k, v))
