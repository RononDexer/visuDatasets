# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import *
import math

# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph

def splitLatLon(latLon):
	#longitude= DDD MM SS.SS
	#latitude=   DD MM SS.SS
	latLon=str(latLon)
	print latLon
	latLonDD=int(latLon[0:len(latLon)-2])
	latLonMM=int(latLon[len(latLon)-2:len(latLon)])
	return [latLonDD, latLonMM]

def latLonTreatmentWithoutSplit(lat, lon):
		coordLon=splitLatLon(lon)
		coordLat=splitLatLon(lat)
		print coordLon, coordLat
		#first : convert to decimal
		lon=toDecimal(coordLon)
		lat=toDecimal(coordLat)
		print lat, lon
		#correction proj Miller
		x=math.radians(lon)
		rlat=math.radians(lat)
		y=(5/4)*math.log(math.tan(math.pi/4+2*rlat/5))
		return tlp.Coord(-x,y)
        #sans correction
        #return tlp.Coord(-lon,lat), cptTreated, cptNA
  
def toDecimal(coords):
	return coords[0]+coords[1]/60.0
	      
def main(graph): 
	AccidentPop_per_1000_people =  graph.getDoubleProperty("Accident/Pop per 1000 people")
	NbVehiclesPerState =  graph.getDoubleProperty("NbVehiclesPerState")
	Pop_Denssqmi =  graph.getDoubleProperty("Pop. Dens./sqmi.")
	Responsability =  graph.getDoubleProperty("Responsability")
	State =  graph.getStringProperty("State")
	Vehicles_per_1000_people =  graph.getIntegerProperty("Vehicles per 1000 people")
	accidentsNb =  graph.getIntegerProperty("accidentsNb")
	latitude =  graph.getIntegerProperty("latitude")
	latitudeREF =  graph.getStringProperty("latitudeREF")
	longitude =  graph.getIntegerProperty("longitude")
	longitudeREF =  graph.getStringProperty("longitudeREF")
	pop_total =  graph.getIntegerProperty("pop total")
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

	ratioAcc = []
	max = 0.0;
	min = 1000;

#	for n in graph.getNodes():
#		print n
#		if(AccidentPop_per_1000_people[n] > max):
#			max = AccidentPop_per_1000_people[n]
#		if(AccidentPop_per_1000_people[n] < min):
#			min = AccidentPop_per_1000_people[n]

#	mean = (max+min)/2	

	accidentsPerVehiculeState = graph.getDoubleProperty("accidentsPerVehiculeState")
	
	for n in graph.getNodes():
		accidentsPerVehiculeState[n] = accidentsNb[n]/NbVehiclesPerState[n]	
	
	_minAPCV = 9999.9
	_maxAPCV = 0.0
	for n in graph.getNodes():
		if(_minAPCV > Responsability[n]):
			_minAPCV = Responsability[n]
		if (_maxAPCV < Responsability[n]):
			_maxAPCV = Responsability[n]
	colorScale = tlp.ColorScale([])
	colorScale.setColorAtPos(_minAPCV, tlp.Color(255,0,0,200))
	colorScale.setColorAtPos((_minAPCV+_maxAPCV)/2, tlp.Color(0,255,0,200))
	colorScale.setColorAtPos(_maxAPCV, tlp.Color(0,0,255,200))
		
	
	for n in graph.getNodes():
		#if(AccidentPop_per_1000_people[n] < mean):
		viewColor[n] = colorScale.getColorAtPos(Responsability[n])
		viewSize[n] = (viewSize[n]/100)*(accidentsPerVehiculeState[n]*10000)
	##	viewLabel[n] = State[n]
		##viewSize[n]=viewSize[n]*AccidentPop_per_1000_people[n]*300;	
		viewLayout[n] = latLonTreatmentWithoutSplit(latitude[n], longitude[n])
		##viewLayout[n], viewColor[n] = latLonTreatmentWithoutSplit(longitude[n], longitude[n])
