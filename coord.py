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
	latitude =  graph.getIntegerProperty("LATITUDE")
	longitude =  graph.getIntegerProperty("LONGITUD")
	#get the needed properties from the graph
	viewLayout =  graph.getLayoutProperty("viewLayout")#nodes' position (x,y)
	viewSize =  graph.getSizeProperty("viewSize") #nodes' size
	viewShape =  graph.getIntegerProperty("viewShape") #nodes' shape
	viewColor =  graph.getColorProperty("viewColor") #nodes' color
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
		viewLayout[n], viewColor[n], cptNA=latLonTreatment(latitude[n],longitude[n], cptNA)
	print  "traites : ",cptTreated-cptNA, ", non traites : ", cptNA

	#########################################################################
	# Regarder le nombre d'accidents en fonction de la zone geographique : Le faire par pallier(1 sous arbre hierarchique) => (Etat, County, Ville, Route)
	# Reprendre ce nombre et associer un poids en fonction de : 
	#	-> Resultante significative de :  Environnement (meteo, etc) + Route condition => poids
	#	-> Legislation (vitesse max, arrivee secours, etc) => poids
	#	-> La gravite de l'accident (Bus scolaire, nombre de personne/vehicule implique) => poids
	# ==> Somme des poids (multidimentionnel) pour une approximation en 2D (nuage de points, histogramme, etc) suivant la moyenne des poids (methode simple)
	# pour savoir, a differentes granularites, quels sont les endroits a fort poids (genre un etat a faible poids mais un pic local)
	#########################################################################
