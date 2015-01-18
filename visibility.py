# Powered by Python 2.7

from tulip import *
import math

#obtain DD, MM, SS.SS from int lat and longitude
def compute_visibility(road, light, weather):
	visibility = 0
	
	if(road == 2) :
		visibility += 1
	elif(road == 8 or road == 9) :
		return -1
		
	if(light == 4 or light == 5) :
		visibility += 1
	elif(light == 3) :
		visibility += 2
	elif(light == 2) :
		visibility += 3
	elif(light == 9) :
		return -1
		
	if(weather == 2 or weather == 3 or weather == 4) :
		visibility += 1
	elif(weather == 5 or weather == 7) :
		visibility += 2
	elif(light == 9) :
		return -1
	
	return visibility
	
def color_node(node, visibility, color, position) :
	if(visibility == 0) : # perfect visibility conditions
		color[node] = tlp.Color(0, 255, 0)
		
	elif(visibility == 1) :
		color[node] = tlp.Color(0, 255, 0)
	
	elif(visibility == 2) :
		color[node] = tlp.Color(0, 86, 27)
		
	elif(visibility == 3) :
		color[node] = tlp.Color(112, 141, 35)
		
	elif(visibility == 4) :
		color[node] = tlp.Color(255, 127, 0)
		
	elif(visibility == 5) :
		color[node] = tlp.Color(231, 62, 1)
		
	elif(visibility == 6) : # worse visibility conditions
		color[node] = tlp.Color(255, 0, 0)
	
	elif(visibility < 0) : # no data
		color[node] = tlp.Color(0, 0, 0)
	
	return 0

def vehiculesVisibility(minRange, maxRange, graph, hashNV):
	
	VE_TOTAL =  graph.getIntegerProperty("VE_TOTAL")

	hashVV = {}
	vehiculeInfo = [] #nb, mean, min, max
	for i in range(minRange, maxRange+1) : 
		hashVV.update({i:vehiculeInfo})
		vehiculeInfo.append([0,0.0,9999,0])		
	
	for n in graph.getNodes():
		for i in range(minRange, maxRange+1):
			if(hashNV.get(n) == hashVV.keys()[i]):
				vehiculeInfo[i][0] += VE_TOTAL[n]
				if(vehiculeInfo[i][2] > VE_TOTAL[n]):
					vehiculeInfo[i][2] = VE_TOTAL[n];
				if(vehiculeInfo[i][3] < VE_TOTAL[n]):
					vehiculeInfo[i][3] = VE_TOTAL[n];
		
	##foreach visibility, n*moy NbVehicule_implique(vrai)				
	for i in range(minRange, maxRange+1):
		vehiculeInfo[i][1] = (float)(vehiculeInfo[i][2] + vehiculeInfo[i][3])/2
		
	hashVC={}
	for i in range(minRange, maxRange+1):
		hashVC.update({i:vehiculeInfo[i]})	
					
	print hashVC
	
def main(graph):
	ALIGNMNT = graph.getIntegerProperty("ALIGNMNT")
	LGT_COND = graph.getIntegerProperty("LGT_COND")
	WEATHER = graph.getIntegerProperty("WEATHER")
	VISIBILITY = graph.getIntegerProperty("VISIBILITY")
		
	#get the needed properties from the graph
	viewLayout = graph.getLayoutProperty("viewLayout") #nodes' position (x,y)
	viewSize = graph.getSizeProperty("viewSize") #nodes' size
	viewShape = graph.getIntegerProperty("viewShape") #nodes' shape
	viewColor = graph.getColorProperty("viewColor") #nodes' color

	graphCpy = graph # TO NOT DELETE/MODIFY ORIGINAL DATA

	visibilityCombin = []	
	hashNV = {}	
	
	for n in graphCpy.getNodes():
		v = compute_visibility(ALIGNMNT[n], LGT_COND[n], WEATHER[n])
		color_node(n, v, viewColor, viewLayout)
		visibilityCombin.append(v)
		hashNV.update({n:v})
		if(v > 0) :
			VISIBILITY[n] = v


	## to get from visibilityCom
	vehiculesVisibility(0, 6, graph, hashNV)

	##graph.
	
##	cutGraph(graphCpy) # TO NOT DELETE/MODIFY ORIGINAL DATA
