import json

DB = json.load(open("fullStores.json"))

def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def get_ids(chunkVal=None):
	a = [d['id'] for d in DB]
	if chunks != None:
		a = chunks(a, len(a)/chunkVal)
	return a

