#!/usr/bin/python3
from mitmproxy import http
from urllib import parse
import json
import os
found = [False]

def request(flow):
	if "https://core.saas.api.t-mobile.com" in flow.request.url and found[0] == False:
		for i in range(50):
			print("AYYYYO")
		print(flow.request.content)
		a = {}
		for k, v in flow.request.headers.items():
			a[k] = v
		os.system("touch done")
		if 'Authorization' in a:
			with open('headers.json', 'w') as fp:
				json.dump(a, fp, indent=4)
			found[0] = True
		for i in range(100):
			print("FOUND")
