# Powered by Python 2.7

from tulip import *
import math

#obtain DD, MM, SS.SS from int lat and longitude
def splitLatLon(latLon):
	#longitude= DDD MM SS.SS
	#latitude=   DD MM SS.SS
	latLon=str(latLon)
	latLonDD=int(latLon[0:len(latLon)-6])
	latLonMM=int(latLon[len(latLon)-6:len(latLon)-4])
	latLonSS=int(latLon[len(latLon)-4:len(latLon)])/100.0
	return [latLonDD, latLonMM, latLonSS]
	
def toDecimal(coords):
	return coords[0]+coords[1]/60.0+coords[2]/3600

def latLonTreatment(lat, lon, cptNA):
		if(lat==99999999 or lat==88888888 or lon==999999999 or lon==888888888):
			#print "data unknown for ",lat," ",lon
			cptNA+=1
			return tlp.Coord(-1,-1),tlp.Color(0,0,255), cptNA
		#obtain DD, MM, SS.SS from int lat and longitude
		coordLon=splitLatLon(lon)
		coordLat=splitLatLon(lat)	
		#first : convert to decimal
		lon=toDecimal(coordLon)
		lat=toDecimal(coordLat)
		#correction proj Miller
		x=math.radians(lon)
		rlat=math.radians(lat)
		y=(5/4)*math.log(math.tan(math.pi/4+2*rlat/5))
		return tlp.Coord(-x,y), tlp.Color(255,0,0), cptNA
        #sans correction
        #return tlp.Coord(-lon,lat), cptTreated, cptNA

def cleanData(graph, node, county, state, cptExited):
	if(county[node] == 0 or county[node] == 997 or county[node] == 999):
		graph.delNode(node)
		cptExited+=1
		return cptExited;
	if(state[node] == 0):
		graph.delNode(node)
		cptExited+=1
		return cptExited;
	return cptExited;
	
def cutGraph(graph):
	
	## Get the necessary properties	
	ALIGNMNT =  graph.getIntegerProperty("ALIGNMNT")
	C_M_ZONE =  graph.getIntegerProperty("C_M_ZONE")
	TRA_CONT =  graph.getIntegerProperty("TRA_CONT")
	SP_LIMIT =  graph.getIntegerProperty("SP_LIMIT")
	T_CONT_F =  graph.getIntegerProperty("T_CONT_F")
	ROUTE =  graph.getIntegerProperty("ROUTE")
	roadProperties=[]
	roadProperties.append(ALIGNMNT)
	roadProperties.append(C_M_ZONE)
	roadProperties.append(TRA_CONT)
	roadProperties.append(SP_LIMIT)
	roadProperties.append(T_CONT_F)
	roadProperties.append(ROUTE)

	latitude =  graph.getIntegerProperty("LATITUDE")
	longitude =  graph.getIntegerProperty("LONGITUD")
	VE_TOTAL =  graph.getIntegerProperty("VE_TOTAL")
	PERSONS =  graph.getIntegerProperty("PERSONS")
	DRUNK_DR =  graph.getIntegerProperty("DRUNK_DR")
	FATALS =  graph.getIntegerProperty("FATALS")
	accidentProperties=[]
	accidentProperties.append(latitude)
	accidentProperties.append(longitude)
	accidentProperties.append(VE_TOTAL)
	accidentProperties.append(PERSONS)
	accidentProperties.append(DRUNK_DR)
	accidentProperties.append(FATALS)
	
	WEATHER =  graph.getIntegerProperty("WEATHER")
	LGT_COND =  graph.getIntegerProperty("LGT_COND")
	SUR_COND =  graph.getIntegerProperty("SUR_COND")
	drivingProperties=[]
	drivingProperties.append(WEATHER)
	drivingProperties.append(LGT_COND)
	drivingProperties.append(SUR_COND)

	MONTH =  graph.getIntegerProperty("MONTH")
	DAY =  graph.getIntegerProperty("DAY")	
	dateProperties=[]
	dateProperties.append(MONTH)
	dateProperties.append(DAY)
	
	DAY_WEEK =  graph.getIntegerProperty("DAY_WEEK")
	HOUR =  graph.getIntegerProperty("HOUR")
	periodProperties=[]
	periodProperties.append(DAY_WEEK)
	periodProperties.append(HOUR)
	
	COUNTY =  graph.getIntegerProperty("COUNTY")
	CITY =  graph.getIntegerProperty("CITY")
	countyProperties=[]
	countyProperties.append(COUNTY)
	countyProperties.append(CITY)
	
	STATE =  graph.getIntegerProperty("STATE")
	
	graphProperties = [accidentProperties, drivingProperties, dateProperties, periodProperties, countyProperties]
	
	## Because of the growing nodes into graph => Pass only 1 times into nodes 
	graphCpy = graph
	##for propertie in graphProperties:
	##	##Create subGraph
	##for node in graphCpy.getNodes():
	##	for propertie in graphProperties:
	##		##Add node to subGraph if conditions are news
	##	##Edge between the 
	
	subState = graph.addSubGraph("states")
	for i in range(1,57):
		subState.addSubGraph(str(i)) 
		
	subCounty = graph.addSubGraph("counties")
	## New for if use city
	for i in range(0,841):
		subCounty.addSubGraph(str(i))

	for n in graphCpy.getNodes():
		state = subState.getSubGraph(str(STATE[n]))
		county = subCounty.getSubGraph(str(COUNTY[n]))
		state.addNode(n)
		county.addNode(n)	
		
	##Edges ?
		
def speedLimit(graph, nbState):
	SP_LIMIT =  graph.getIntegerProperty("SP_LIMIT")
	STATE =  graph.getIntegerProperty("STATE")

	speedType = []
	
	for n in graph.getNodes():
	 	exist = False;
		for i in range(0, len(speedType)):
			if(speedType[i] == SP_LIMIT[n]):
				exist = True				
				break;
		if(exist == False):
			speedType.append(SP_LIMIT[n])

	hashTotalMeanAccident = {}
	for i in range(0, len(speedType)):
		totalAccident = 0.0;
		meanAccident = 0.0;
		accidentPerState = [];			
		for n in graph.getNodes():
			if(speedType[i] == SP_LIMIT[n]):
				totalAccident+=1;
		meanAccident = totalAccident/nbState;
		hashTotalMeanAccident.update({speedType[i]:meanAccident})
	
	hashAccidentsPerSpeedState={}
	for i in range(1, 57):
		if(i==3 or i==7 or i==14 or i==52):
			continue
		speedAccidentList = []			
		for j in range(0, len(speedType)):
			speedAccidentList.append(0)
			for n in graph.getNodes():				
				if(i == STATE[n] and speedType[j] == SP_LIMIT[n]):
					speedAccidentList[j]+=1		
		hashAccidentsPerSpeedState.update({i:speedAccidentList})	
		
	
	hashConsSpeed = {}
	for key, value in hashAccidentsPerSpeedState.iteritems():
		sumAccident = 0
		for i in range(0, len(speedType)):
			sumAccident += (hashTotalMeanAccident.get(speedType[i]) - value[i])
		if(sumAccident < 0):
			sumAccident = 0
		hashConsSpeed.update({key:(sumAccident/len(speedType))})
	hashConsSpeed = normalizeHash(hashConsSpeed)
	
	return hashConsSpeed
	
	
def regulation(graph, nbState):
	TRA_CONT =  graph.getIntegerProperty("TRA_CONT")
	T_CONT_F =  graph.getIntegerProperty("T_CONT_F")
	STATE =  graph.getIntegerProperty("STATE")
	
	
	for n in graph.getNodes():
		if(T_CONT_F[n] == 0 or T_CONT_F[n] == 1 or T_CONT_F[n] == 2):
			TRA_CONT[n] == 0
		if(T_CONT_F[n] == 9):
			TRA_CONT[n] == 99
			
	for n in graph.getNodes():
		if(TRA_CONT[n] > 0 and TRA_CONT[n] <= 9):
			TRA_CONT[n] = 1
		elif(TRA_CONT[n] >= 20 and TRA_CONT[n] <= 29):
			TRA_CONT[n] = 2
		elif(TRA_CONT[n] >= 30 and TRA_CONT[n] <= 39):
			TRA_CONT[n] = 3
		elif(TRA_CONT[n] >= 40 and TRA_CONT[n] <= 41):
			TRA_CONT[n] = 4
		elif(TRA_CONT[n] == 50):
			TRA_CONT[n] = 5
		elif(TRA_CONT[n] >= 60 and TRA_CONT[n] <= 69):
			TRA_CONT[n] = 6
		elif(TRA_CONT[n] >= 70 and TRA_CONT[n] <= 79):
			TRA_CONT[n] = 7
		elif(TRA_CONT[n] >= 70 and TRA_CONT[n] <= 79):
			TRA_CONT[n] = 7
		elif(TRA_CONT[n] == 80):
			TRA_CONT[n] = 8
	
	regType = []
	
	for n in graph.getNodes():
	 	exist = False;
		for i in range(0, len(regType)):
			if(regType[i] == TRA_CONT[n]):
				exist = True				
				break;
		if(exist == False):
			regType.append(TRA_CONT[n])	
	
	for n in graph.getNodes():
		if(TRA_CONT[n] > 0 and TRA_CONT[n] < 99):
			TRA_CONT[n] = 1
			
	hashAccidentsRegulationPerState={}
	for i in range(1, 57):
		if(i==3 or i==7 or i==14 or i==52):
			continue
		meanRegulation = 0.0
		nbRegulation = 0.0
		for n in graph.getNodes():
			if(TRA_CONT[n] < 99 and STATE[n] == i):
				meanRegulation+=(TRA_CONT[n]+1) ## += 1 or 2
				nbRegulation+=1
		if(nbRegulation < 1):
			hashAccidentsRegulationPerState.update({i:1}) ## Very bad state
		else:
			hashAccidentsRegulationPerState.update({i:(meanRegulation/nbRegulation)})
	
	hashAccidentsRegulationPerState = normalizeHash(hashAccidentsRegulationPerState)
	
	return hashAccidentsRegulationPerState
	
## Normalize between 1 & 2	
def normalizeHash(hashStateConseq): 
	_max = 0.0
	_min = 9999.9
	hashStateConseqNormalized = {}
	for key, value in hashStateConseq.iteritems():
		if(value < _min) :
			_min = value;
		if(value > _max):
			_max = value
	for key, value in hashStateConseq.iteritems():
		hashStateConseqNormalized.update({key:(value - _min)/(_max-_min)+1})
	return hashStateConseqNormalized
	
def stateResponsability(hashSpeedStateCons, hashRegStateCons, nbState):
	hashStateCons = {}
	for i in range(1, 57):
		if(i==3 or i==7 or i==14 or i==52):
			continue
		for key, value in hashSpeedStateCons.iteritems():
			hashStateCons.update({i:(hashRegStateCons.get(i)/value)})
	
	hashStateCons = normalizeHash(hashStateCons)
	return hashStateCons
	
	
def daysSubGraph(graph):
	DAY_WEEK =  graph.getIntegerProperty("DAY_WEEK")
	subGphDayWeek=graph.addSubGraph("dayWeek")
	
	dayType = []
	
	for n in graph.getNodes():
	 	exist = False;
		for i in range(0, len(dayType)):
			if(dayType[i] == DAY_WEEK[n]):
				exist = True				
				break;
		if(exist == False):
			dayType.append(DAY_WEEK[n])
	
	subGraphDays = []		
	for i in range(1, 8):
		currentSubGraph = subGphDayWeek.addSubGraph(str(i))
		for n in graph.getNodes():
			if(DAY_WEEK[n] == i):
				currentSubGraph.addNode(n)
		subGraphDays.append(currentSubGraph)		
	
# the main(graph) function must be defined to run the script on the current graph
# this script will redraw the graph as a onion graph. The input graph must be a tree.
def main(graph):
	ALIGNMNT =  graph.getIntegerProperty("ALIGNMNT")
	ARR_HOUR =  graph.getIntegerProperty("ARR_HOUR")
	ARR_MIN =  graph.getIntegerProperty("ARR_MIN")
	CITY =  graph.getIntegerProperty("CITY")
	COUNTY =  graph.getIntegerProperty("COUNTY")
	C_M_ZONE =  graph.getIntegerProperty("C_M_ZONE")
	DAY =  graph.getIntegerProperty("DAY")
	DAY_WEEK =  graph.getIntegerProperty("DAY_WEEK")
	DRUNK_DR =  graph.getIntegerProperty("DRUNK_DR")
	FATALS =  graph.getIntegerProperty("FATALS")
	HARM_EV =  graph.getIntegerProperty("HARM_EV")
	HOSP_HR =  graph.getIntegerProperty("HOSP_HR")
	HOSP_MN =  graph.getIntegerProperty("HOSP_MN")
	HOUR =  graph.getIntegerProperty("HOUR")
	LATITUDE =  graph.getIntegerProperty("LATITUDE")
	LGT_COND =  graph.getIntegerProperty("LGT_COND")
	LONGITUD =  graph.getIntegerProperty("LONGITUD")
	MINUTE =  graph.getIntegerProperty("MINUTE")
	MONTH =  graph.getIntegerProperty("MONTH")
	NOT_HOUR =  graph.getIntegerProperty("NOT_HOUR")
	NOT_MIN =  graph.getIntegerProperty("NOT_MIN")
	NO_LANES =  graph.getIntegerProperty("NO_LANES")
	PAVE_TYP =  graph.getIntegerProperty("PAVE_TYP")
	PERSONS =  graph.getIntegerProperty("PERSONS")
	PROFILE =  graph.getIntegerProperty("PROFILE")
	REL_JUNC =  graph.getIntegerProperty("REL_JUNC")
	REL_ROAD =  graph.getIntegerProperty("REL_ROAD")
	ROUTE =  graph.getIntegerProperty("ROUTE")
	SCH_BUS =  graph.getBooleanProperty("SCH_BUS")
	SP_LIMIT =  graph.getIntegerProperty("SP_LIMIT")
	STATE =  graph.getIntegerProperty("STATE")
	ST_CASE =  graph.getIntegerProperty("ST_CASE")
	SUR_COND =  graph.getIntegerProperty("SUR_COND")
	TRAF_FLO =  graph.getIntegerProperty("TRAF_FLO")
	TRA_CONT =  graph.getIntegerProperty("TRA_CONT")
	T_CONT_F =  graph.getIntegerProperty("T_CONT_F")
	VE_TOTAL =  graph.getIntegerProperty("VE_TOTAL")
	WEATHER =  graph.getIntegerProperty("WEATHER")
	viewBorderColor =  graph.getColorProperty("viewBorderColor")
	viewBorderWidth =  graph.getDoubleProperty("viewBorderWidth")
	viewColor =  graph.getColorProperty("viewColor")
	viewFont =  graph.getStringProperty("viewFont")
	viewFontSize =  graph.getIntegerProperty("viewFontSize")
	viewLabel =  graph.getStringProperty("viewLabel")
	viewLabelBorderColor =  graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth =  graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor =  graph.getColorProperty("viewLabelColor")
	viewLabelPosition =  graph.getIntegerProperty("viewLabelPosition")
	viewLayout =  graph.getLayoutProperty("viewLayout")
	viewMetaGraph =  graph.getGraphProperty("viewMetaGraph")
	viewMetric =  graph.getDoubleProperty("viewMetric")
	viewRotation =  graph.getDoubleProperty("viewRotation")
	viewSelection =  graph.getBooleanProperty("viewSelection")
	viewShape =  graph.getIntegerProperty("viewShape")
	viewSize =  graph.getSizeProperty("viewSize")
	viewSrcAnchorShape =  graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize =  graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture =  graph.getStringProperty("viewTexture")
	viewTgtAnchorShape =  graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize =  graph.getSizeProperty("viewTgtAnchorSize")
	#if longitude=999 99 99.99 or 888 88 88.88 unknown
	#if latitude=  99 99 99.99 or  88 88 88.88 unknown

	# TO NOT DELETE/MODIFY ORIGINAL DATA	
	graphCpy = graph
	
	cptTreated, cptNA=0,0
	for n in graphCpy.getNodes():
		cptTreated+=1
		cptNA = cleanData(graphCpy, n, COUNTY, STATE, cptNA)
	for n in graphCpy.getNodes():
		viewSize[n] = viewSize[n]/100
		viewLayout[n], viewColor[n], cptNA=latLonTreatment(LATITUDE[n],LONGITUD[n], cptNA)
	print  "traites : ",cptTreated-cptNA, ", non traites : ", cptNA
	
##	stateResponsability(speedLimit(graph, 52), regulation(graph, 52), 52)
	
	daysSubGraph(graph)
##	cutGraph(graphCpy)

	#########################################################################
	# Regarder le nombre d'accidents en fonction de la zone geographique : Le faire par pallier(1 sous arbre hierarchique) => (Etat, County, Ville, Route)
	# Reprendre ce nombre et associer un poids en fonction de : 
	#	-> Resultante significative de :  Environnement (meteo, etc) + Route condition => poids
	#	-> Legislation (vitesse max, arrivee secours, etc) => poids
	#	-> La gravite de l'accident (Bus scolaire, nombre de personne/vehicule implique) => poids
	# ==> Somme des poids (multidimentionnel) pour une approximation en 2D (nuage de points, histogramme, etc) suivant la moyenne des poids (methode simple)
	# pour savoir, a differentes granularites, quels sont les endroits a fort poids (genre un etat a faible poids mais un pic local)
	#########################################################################
