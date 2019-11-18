import requests
import time
import json
import csv
import sys
from operator import itemgetter
from itertools import groupby

print("=========== Amazon EC2 On-Demand & Spot Price compare csv ===========")
region = sys.argv[1]
env = sys.argv[2]
print("Region: " + region)
print("Environment: " + env)
onDemandLabel = 'Linux/UNIX' if env == 'linux' else 'Red Hat Enterprise Linux' if env == 'rhel' else \
    'SUSE Linux Enterprise Server' if env == 'suse' else 'Windows' if env == 'windows' else 'Windows with SQL Standard' \
    if env == 'windows-std' else 'Windows with SQL Web' if env == 'windows-web' else 'Windows with SQL Enterprise' \
    if env == 'windows-enterprise' else 'Linux with SQL Standard' if env == 'linux-std' else 'Linux with SQL Web' \
    if env == 'linux-web' else 'Linux with SQL Enterprise'
spotLabel = 'Linux/UNIX' if 'Linux' in onDemandLabel else 'Windows'
spotEnvName = 'linux' if 'Linux' in spotLabel else 'mswin'
timestamp = str(round(time.time()))
onDemandUrl = "https://a0.p.awsstatic.com/pricing/1.0/ec2/region/" + region + "/ondemand/" + env + "/index.json?timestamp=" + timestamp
spotUrl = "https://website.spot.ec2.aws.a2z.com/spot.js?callback=callback&_=" + timestamp
print("Getting data ...")
response_1 = requests.get(onDemandUrl)
response_2 = requests.get(spotUrl)
if str(response_1.status_code) == '200' and str(response_2.status_code) == '200':
    print("Preparing data ...")
    spotPrice = response_2.text
    spotPrice = spotPrice.replace("callback(", "").replace(");", "")
    spotPrice = json.loads(spotPrice)
    spotPricing = {}

    for regionSpotPricing in spotPrice.get("config").get("regions"):
        region = 'us-east' if region == 'us-east-1' else region
        if regionSpotPricing.get("region") == region:
            regionSpotPricing = regionSpotPricing.get("instanceTypes")
            break

    for item in regionSpotPricing:
        for i in item.get("sizes"):
            size = i.get("size")
            for j in i.get("valueColumns"):
                if j.get("name") == spotEnvName:
                    price = j.get("prices").get("USD")
                    spotPricing[size + "_" + spotEnvName] = price

    onDemandPrice = json.loads(response_1.text)
    onDemandPrices = onDemandPrice.get("prices")
    newList = []

    for price in onDemandPrices:
        attributes = price.get("attributes")
        attributes["id"] = price.get("id")
        attributes["price"] = price.get("price").get("USD")
        attributes["unit"] = price.get("unit")
        attributes["spot"] = spotPricing.get(attributes.get("aws:ec2:instanceType")+"_"+spotEnvName)
        newList.append(attributes)

    newList.sort(key=itemgetter('aws:ec2:instanceFamily'))
    print("Data successfully prepared.")
    print("Preparing csv file ...")
    filename = 'aws-on-demand-pricing-' + region + '-' + env + '-' + timestamp + '.csv'
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
                onDemandLabel + ' Usage',
                spotLabel + ' Spot Usage'
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
                    item.get("price"),
                    item.get("spot")
                ])
    print("Successfully " + filename + " file created.")
else:
    print("Something went wrong, Please try again later")
