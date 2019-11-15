import sys
import requests
import time
import json
import csv
from operator import itemgetter
from itertools import groupby

print("########## Amazon EC2 On-Demand Pricing ##########")
region = sys.argv[1]
env = sys.argv[2]
print("Region: " + region)
print("Environment: " + env)
label = 'Linux/UNIX' if env == 'linux' else 'Red Hat Enterprise Linux' if env == 'rhel' else \
    'SUSE Linux Enterprise Server' if env == 'suse' else 'Windows' if env == 'windows' else 'Windows with SQL Standard' \
    if env == 'windows-std' else 'Windows with SQL Web' if env == 'windows-web' else 'Windows with SQL Enterprise' \
    if env == 'windows-enterprise' else 'Linux with SQL Standard' if env == 'linux-std' else 'Linux with SQL Web' \
    if env == 'linux-web' else 'Linux with SQL Enterprise'
timestamp = str(round(time.time()))
targetUrl = "https://a0.p.awsstatic.com/pricing/1.0/ec2/region/" + region + "/ondemand/" + env + "/index.json?timestamp=" + timestamp
response = requests.get(targetUrl)
print(response.status_code)
if str(response.status_code) == '200':
    print("Preparing data...")
    data = json.loads(response.text)
    prices = data.get("prices")
    newList = []

    print("Processing data...")
    for price in prices:
        attributes = price.get("attributes")
        attributes["id"] = price.get("id")
        attributes["price"] = price.get("price").get("USD")
        attributes["unit"] = price.get("unit")
        newList.append(attributes)

    newList.sort(key=itemgetter('aws:ec2:instanceFamily'))
    filename = 'aws-on-demand-pricing-' + region + '-' + env + '-' + timestamp + '.csv'
    print("Preparing csv file ...")
    with open(filename, 'w', newline='') as file:
        groupFlag = 0
        filePointer = csv.writer(file, delimiter='#', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for instance_family, items in groupby(newList, key=itemgetter('aws:ec2:instanceFamily')):
            if groupFlag > 0: filePointer.writerow([])
            filePointer.writerow([
                instance_family,
                'vCPU',
                'ECU',
                'Memory (GiB)',
                'Instance Storage (GB)',
                label + ' Usage'
            ])
            items = sorted(items, key=lambda i: (i['aws:ec2:instanceType'], i['price']))
            groupFlag = groupFlag + 1
            for item in items:
                filePointer.writerow([
                    item.get("aws:ec2:instanceType"),
                    item.get("aws:ec2:vcpu"),
                    item.get("aws:ec2:ecu"),
                    item.get("aws:ec2:memory"),
                    item.get("aws:ec2:storage"),
                    item.get("price")
                ])
    print("Successfully " + filename + " file created.")
else:
    print("Something went wrong, Please try again later")
