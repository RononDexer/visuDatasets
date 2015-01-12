# Powered by Python 2.7

from tulip import *
import math

#obtain DD, MM, SS.SS from int lat and longitude
def compute_visibility(road, light, weather):
	visibility = 0
	
	if(road == 2) :
		visibility += 1
		
	if(light == 4 or light == 5) :
		visibility += 1
	elif(light == 3) :
		visibility += 2
	elif(light == 2) :
		visibility += 3
		
	if(weather == 2 or weather == 3 or weather == 4) :
		visibility += 1
	elif(weather == 5 or weather == 7) :
		visibility += 2
	
	return visibility
	
def color_node(node, visibility, color, position) :
	if(visibility == 0) : # perfect visibility conditions
		color[node] = tlp.Color(0, 255, 0)
#		position[node] = tlp.Coord(0, 0, 0)
		
	elif(visibility == 1 or visibility == 2) :
		color[node] = tlp.Color(0, 125, 125)
#		position[node] = tlp.Coord(30, 0, 0)
		
	elif(visibility == 3 or visibility == 4) :
		color[node] = tlp.Color(125, 125, 0)
#		position[node] = tlp.Coord(60, 0, 0)
		
	elif(visibility == 5 or visibility == 6) : # worse visibility conditions
		color[node] = tlp.Color(255, 0, 0)
#		position[node] = tlp.Coord(90, 0, 0)
	
	return 0

def main(graph):
	ALIGNMNT = graph.getIntegerProperty("ALIGNMNT")
	LGT_COND = graph.getIntegerProperty("LGT_COND")
	WEATHER = graph.getIntegerProperty("WEATHER")
	
	#get the needed properties from the graph
	viewLayout = graph.getLayoutProperty("viewLayout") #nodes' position (x,y)
	viewSize = graph.getSizeProperty("viewSize") #nodes' size
	viewShape = graph.getIntegerProperty("viewShape") #nodes' shape
	viewColor = graph.getColorProperty("viewColor") #nodes' color

	graphCpy = graph # TO NOT DELETE/MODIFY ORIGINAL DATA
	
	for n in graphCpy.getNodes():
		v = compute_visibility(ALIGNMNT[n], LGT_COND[n], WEATHER[n])
		color_node(n, v, viewColor, viewLayout)
		
	
	cutGraph(graphCpy) # TO NOT DELETE/MODIFY ORIGINAL DATA
