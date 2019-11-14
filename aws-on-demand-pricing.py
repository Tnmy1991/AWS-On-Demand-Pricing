import requests
import time
import json

timestamp = str(round(time.time()))
targetUrl = "https://a0.p.awsstatic.com/pricing/1.0/ec2/region/us-east-2/ondemand/linux/index.json?timestamp=" + timestamp
response = requests.get(targetUrl)
print("Status code: " + str(response.status_code))
data = json.loads(response.text)
prices = data.get("prices")
sortList = {}

for price in prices:
	attributes = price.get("attributes")
	sortList.setdefault(attributes.get("aws:ec2:instanceFamily"), {}) = price
	print(sortList)
	exit()