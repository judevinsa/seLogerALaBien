import urllib2
import xml.etree.ElementTree
import threading
import json

url = 'http://ws.seloger.com/search.xml?idtt=1&pmax=1200&idtypebien=1,2,9,13,14&ci=750101,750102,750103,750104,750105,750106,750107,750108,750109,750110,750117,750118&tri=initial&nb_piecesmin=2'
mapsUrl = 'https://maps.googleapis.com/maps/api/directions/json?mode=transit'
workPlace = 'origin=48.900714,2.312832'
centerPlace = 'origin=48.854891,2.346708'
mapsKey = 'key={maps_api_key}'

class Annonce:
	prix = 0
	nbPiece = 0
	surface = 0
	permalien = ''
	latitude = ''
	longitude = ''
	timeWork = ''
	timeCenter = ''
	def getTime(self):
		print '\n\n'
		workUrl = mapsUrl + '&' + workPlace + '&destination=' + self.latitude + ',' + self.longitude + '&' +  mapsKey
		print workUrl
		centerUrl = mapsUrl + '&' + centerPlace + '&destination=' + self.latitude + ',' + self.longitude + '&' +  mapsKey
		print centerUrl
		workContent = urllib2.urlopen(workUrl).read()
		centerContent = urllib2.urlopen(centerUrl).read()
		objectWork = json.loads(workContent)
		self.timeWork = objectWork['routes'][0]['legs'][0]['duration']['text']
		objectCenter = json.loads(centerContent)
		self.timeCenter = objectCenter['routes'][0]['legs'][0]['duration']['text']

content = urllib2.urlopen(url).read()
transformed = content.replace('\r\n', '')
transformed = transformed.replace('\t','')

rootNode = xml.etree.ElementTree.fromstring(transformed)
annonces = rootNode.find('annonces')

allAnnonces = []

for annonce in annonces.findall('annonce'):
	x = Annonce()
	x.prix = annonce.find('prix').text
	x.nbPiece = annonce.find('nbPiece').text
	x.surface = annonce.find('surface').text
	if annonce.find('permalien') is not None:
		x.permalien = annonce.find('permalien').text
	if annonce.find('latitude') is not None:
		x.latitude = annonce.find('latitude').text
	if annonce.find('longitude') is not None:
		x.longitude = annonce.find('longitude').text
	x.getTime()
	print 'To Work : ' + x.timeWork
	print 'To Center : ' + x.timeCenter
