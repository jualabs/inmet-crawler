
f =open('metadata.html','r')


metalist = []

for line in f:
	metadata = {
		'stationName': '',
		'stationCode': '',
		'latitude': 0,
		'longitude': 0,
		'altitude': 0,
		'url': ''
	}	
	data = line.split('<br>')
	#Get station Name and Code
	metadata['stationName'] = data[0].split('</b>')[1].replace(" ","").split("-")[0]
	code = data[0].split('</b>')[1].replace(" ","").split("-")[-1]
	if code[0] == 'A':
		metadata['stationCode'] = data[0].split('</b>')[1].replace(" ","").split("-")[-1]
	else:
		continue
	#Get URL
	try:
		if data[10][0:3] == '<ta':
			urlData = data[10].split('<a href=')[1].split(" ")[0]
		elif data[11][0:3] == '</a':
			urlData = data[11].split('<a href=')[1].split(" ")[0]
	except:
		continue

	metadata['url'] = urlData
	print(metadata['url'])
#	print(metadata)
#	try:
#		print(data[11])
#		print(data[11].split('<a href='))
#	except:
#		continue
	#print(data[3])
	metalist.append(metadata)
	for d in data:
		if d[0:3] == 'Lat':
			print(d.split(':'))
		elif d[0:3] == 'Lon':
			print(d)
		elif d[0:3] == 'Alt':
			print(d)

f.close()
f =open('url.data','w')
for m in metalist:
	print(m['url'])
	f.write(m['url']+'\n')
f.close()
