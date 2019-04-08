import json
import glob

if __name__ == '__main__':
	stores = []
	h = {}
	for file in glob.glob("1*.json"):
		g = {}
		a = json.load(open(file))
		for key, val in a.iteritems():
			g[key] = []
			for k, v in val.iteritems():
				if k not in g:
					g[k] = []
				for i in range(v):
					g[k].append(key)
		for v in [(k, len(v)) for k, v in g.iteritems()]:
			if v[0] not in h:
				h[v[0]] = []
			h[v[0]].append(v[1])
	print h

