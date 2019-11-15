import requests
import time
import json
from operator import itemgetter
from itertools import groupby

timestamp = str(round(time.time()))
targetUrl = "https://a0.p.awsstatic.com/pricing/1.0/ec2/region/us-east-2/ondemand/linux/index.json?timestamp=" + timestamp
response = requests.get(targetUrl)
print("Status code: " + str(response.status_code))
data = json.loads(response.text)
prices = data.get("prices")
newList = []

for price in prices:
	attributes = price.get("attributes")
	attributes["id"] = price.get("id")
	attributes["price"] = price.get("price").get("USD")
	attributes["unit"] = price.get("unit")
	newList.append(attributes)

# First sort by required field
# Groupby only finds groups that are collected consecutively
newList.sort(key=itemgetter('aws:ec2:instanceFamily'))
file = open("aws-on-demand-pricing.txt","a")

# Now iterate through groups (here we will group by the year born)
for instance_family, items in groupby(newList, key=itemgetter('aws:ec2:instanceFamily')):
	file.write(instance_family)
	for i in items:
		file.write(str(i))