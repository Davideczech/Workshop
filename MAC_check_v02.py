import csv 
import json 

names = []
intstatus = []
short_key = []
check = 0
#intstatusdict = {}

# Read in the JSON database
with open("json_data.json",encoding="utf-8") as json_file:
     json_text = json_file.read()
	 
# Use the json module to parse the JSON string into native Python data
json_data = json.loads(json_text)

# Open input file with MAC adresses(without dots) and interfaces. 
with open ("Device_MAC.csv") as switch_mac:
	mac = []
	macint = []
	ints = []
	switch_mac.readline()
# Creating lists from csv columns	
	for a, b, c in csv.reader(switch_mac, delimiter=","): 
	
		mac.append(a)
		macint.append(b)
		ints.append(c)

#Cutting the key to OUI

for key in mac: 
	t = iter(key)
	key=":".join(a+b for a,b in zip (t,t))
	key=key.upper()
	short_key.append(key[:8])

#Iteration through the short_key

for skey in short_key:
	try:
		names.append(json_data[skey]["name"])
	except KeyError:
		names.append("Other")

#Creating dictionary from the mac and macint

zipobj = zip (macint, names)
macdict = dict(zipobj)

#Creating csv file

for int in ints:
	int = int.strip()
	for macin in macdict:
		macin = macin.strip()
		if int == macin: 
#			intstatusdict[int] = macdict[macin]
			intstatus.append(macdict[macin])
			check = 1
			break
	if check == 0: 
		intstatus.append("Unknown")
#		intstatusdict[int] = "Unknown"
	else:
		check = 0

#print (intstatusdict)
		
# Creating output csv file		
	
with open ("MAC_result.csv", "w+", newline="") as myfile:
	wr = csv.writer(myfile)
	wr.writerow(mac)
	wr.writerow(macint)
	wr.writerow(names)
	wr.writerow(ints)
	wr.writerow(intstatus)
