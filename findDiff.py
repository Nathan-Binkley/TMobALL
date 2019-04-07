import json


if __name__ == '__main__':
	first = json.load(open("firstTry.json"))
	second = json.load(open("secondRun.json"))
	for k, v in first.iteritems():
		if second[k] != v:
			print("SUCCESFULLY HACKED")
	#main()
