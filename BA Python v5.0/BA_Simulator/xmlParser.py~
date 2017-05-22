#Author: Lt Jason Blackford
#University: AFIT
#Date: 10 Oct 2013
#Source Description: This code pares through the xml definition files for the RTS game to be simulated.  In addition it instantiates necessary global variables defined
#in global_sim.py that keep track of defintions and game state information as the simulator executes.

#IMPORTANT: When defining actions, resources, effects in the xml files be sure to use a consistent naming scheme.  Therefore if you name
#a resource "Gold" in vol_resource.xml then you'll need to make sure the command.xml uses the name "Gold" when asssigning this volumetric resource to an action


import global_sim
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import actions
import unary
import combat_unit
import sys

print "RUNNING XML PARSER"
#print "****************************LOADING RTS GAME DEFINITIONS*****************************************"
#print "****************************AND INITIALIZING GAME STATE*****************************************"
#************************This section reads in the unary_resource.xml file to define all unary resources for the RTS game being simulated**********************
#print("Unary Resources:\n")
unary_tree = ET.parse('unary_resource.xml')	
unary_root = unary_tree.getroot()

for res in unary_root:
	tName = res.get('name')
	tWorkTime = float(res.get('worktime')) 
	tUnary = unary.Unary(tName, tWorkTime)
	global_sim.unary_definitions.update({tName:tUnary})
	
	#This list stores the duplicates of a specified type of unary resource (i.e. if player has 3 barracks all three are in a list).
	#This list is added to the unary_resource_state dictionary which keeps track of the game state.
	tUnaryList = []
	tExist = int(res.get('exist'))
	#print(tUnary.name)
	#Adds a unary object to the initial game state if specified by setting 'exist = Number of instances of resource' inside unary_resource.xml
	for i in range(1,tExist+1):
		#print i
		tCopy = unary.Unary(tName,tWorkTime)
		tUnaryList.append(tCopy)
	
	global_sim.unary_resource_state.update({tName:tUnaryList})
	
	
#************************This section reads in the vol_resource.xml file to define all volumetric resources for the RTS game being simulated**********************	
#print("Volumetric Resources:\n")
vol_tree  = ET.parse('vol_resource.xml')
vol_root = vol_tree.getroot()	

for res in vol_root:
	tName = res.get('name')
	tRate = float(res.get('rate'))
	tInitRate = float(res.get('init_rate'))
	tInitAmt = float(res.get('init_amt'))
	tCapacity = float(res.get('capacity'))
	tVol = volumetric.Volumetric(tName, tRate, tInitRate, tInitAmt,tCapacity)
	global_sim.volumetric_definitions.update({tName:tVol})
	#This dict contains only unique key:value pairs for each type of volumetric resource (i.e metal, food, gas, gold, wood, etc...'name':volumetric object).
	#These are the instantiated instances of these resources used throughout the simulator.
	global_sim.volumetric_resource_state.update({tName:tVol})
	#print(tVol.name, tVol.accumulation_rate, tVol.current_total)

#************************This section reads in the combat_unit.xml file to define all combat unit types for the RTS game being simulated**********************	
#print("Combat Unit Types:\n")
combUnit_tree = ET.parse('combat_unit.xml')	
combUnit_root = combUnit_tree.getroot()

for unit in combUnit_root:
	tName = unit.get('name')
	tAmt  = float(unit.get('init_amt'))
	tUnit = combat_unit.CombatUnit(tName, tAmt)
	global_sim.combatUnit_definitions.update({tName:tUnit})
	global_sim.combat_unit_state.update({tName:tUnit})
	#print(tUnit.name)
		
#************************This section reads in the unary_goal.xml file to define the unary goal state to be reached for the RTS game being simulated**********************
#print("Unary Goals:\n")
gUnary_tree = ET.parse('unary_goal.xml')	
gUnary_root = gUnary_tree.getroot()

for res in gUnary_root:
	tName = res.get('name')
	#tUnary = unary.Unary(tName)
	#global_sim.unary_definitions.update({tName:tUnary})
	tExist = float(res.get('exist'))
	tMinCost = float(res.get('metCost'))
	tGasCost = float(res.get('nrgCost'))
	tDurAmt = float(res.get('durAmt'))
	
	#This list stores the duplicates of a specified type of unary resource (i.e. if player has 3 barracks all three are in a list).
	#This list is added to the unary_resource_state dictionary which keeps track of the game state.
	#tUnaryList = []
	#tExist = int(res.get('exist'))
	#print(tUnary.name)      name,workTime,exist = None,minCost=None,gasCost=None,durAmt = None):
	tUnaryGoal = unary.Unary(tName,0,tExist,tMinCost,tGasCost,tDurAmt)
	#Adds a unary object to the initial game state if specified by setting 'exist = Number of instances of resource' inside unary_resource.xml
	#for i in range(1,tExist+1):
	#	print i
	#	tCopy = unary.Unary(tName)
	#	tUnaryList.append(tCopy)
	
	global_sim.unary_goal_state.update({tName:tUnaryGoal})
	
	
#************************This section reads in the vol_goal.xml file to define the volumetric goal state to be reached by the RTS game being simulated**********************	
#print("Volumetric Goals:\n")
gVol_tree  = ET.parse('vol_goal.xml')
gVol_root = gVol_tree.getroot()	

for res in gVol_root:
	tName = res.get('name')
	tInitRate = float(res.get('init_rate'))
	tInitAmt = float(res.get('init_amt'))
	tVol = volumetric.Volumetric(tName, 0,tInitRate,tInitAmt)
	#global_sim.volumetric_definitions.update({tName:tVol})
	#This dict contains only unique key:value pairs for each type of volumetric resource (i.e metal, food, gas, gold, wood, etc...'name':volumetric object).
	#These are the instantiated instances of these resources used throughout the simulator.
	global_sim.volumetric_goal_state.update({tName:tVol})
	#print(tVol.name, tVol.accumulation_rate, tVol.current_total)

#************************This section reads in the combat_unit.xml file to define all combat unit types for the RTS game being simulated**********************	
#print("Unit Goals:\n")
gUnit_tree = ET.parse('unit_goal.xml')	
gUnit_root = gUnit_tree.getroot()

for unit in gUnit_root:
	tName = unit.get('name')
	tExist = float(unit.get('exist'))
	tMinCost = float(unit.get('metCost'))
	tGasCost = float(unit.get('nrgCost'))
	tDurAmt = float(unit.get('durAmt'))
	tUnit = combat_unit.CombatUnit(tName, tExist,tMinCost,tGasCost,tDurAmt)
	global_sim.unit_goals.update({tName:tUnit})
	#print(tUnit.name)

#************************This section reads in the command.xml file to define all actions for the RTS game being simulated**********************
#print("Commands:\n")
command_tree = ET.parse('command.xml')	
cmd_root = command_tree.getroot()

for action in cmd_root:

	tVolResDict = {}
	tUnaryResList = []
	tUnaryExistList = []
	tEffectsDict = {}

	tName = action.find('name').text
	tDuration = float(action.find('duration').text)
	
	#build vol dictionary
	vol = action.find('volumetric_dictionary')
	for attr in vol:
		tKey = attr.get('key')
		tValue = float(attr.get('value'))
		#print(tKey,tValue)
		tVolResDict.update({tKey:tValue})
	
	#build unary list
	unary = action.find('unary_list')
	for attr in unary:
		tUnaryResList.append(attr.text)
		
		
	#build exist list
	exist = action.find('exist_list')
	for attr in exist:
		tUnaryExistList.append(attr.text)
	
	#build effects list
	effect = action.find('effect_list')
	for attr in effect:
		tKey = attr.get('key')
		#identify hold actions and add their names to the gather_action dictionary.
		#The initial value is 0.  This value represents the number of unary resources (i.e workers)
		#collecting the volumetric resource this action collects (i.e. gold, mineral, etc).
		#IMPORTANT: The action should have the same name as the resource it gathers (set inside commands.xml & volumetric_res.xml)
		if(tKey == global_sim.effect_hold):
			global_sim.gathering_actions.update({tName:0})
		tValue = attr.get('value')
		tEffectsDict.update({tKey:tValue})
	
	#create new action from xml file and add to action definitions
	tAction = actions.Action(tName,tDuration, tVolResDict, tUnaryResList, tUnaryExistList, tEffectsDict)	
	global_sim.action_definitions.update({tName:tAction})
	tVolResDict.clear()
	tUnaryResList[:] = []
	tUnaryExistList[:] = []
	tEffectsDict.clear()
	
	#print(tAction.name, tAction.duration, tAction.vol_res_dict, tAction.unary_res_list, tAction.exist_list, tAction.effects_dict)
	#print(tAction.duration + 20)

#************Exit Parser Statement (note Indentation so its outside the above For-Loop***************
#force execution to return to main.py
#***********************construct command reference table*************************************
tCmd = Element('command')
actionCounter = 0
for t in global_sim.action_definitions.keys():
	tnew = SubElement(tCmd,'action', name = t, intID = str(actionCounter))
	#SubElement(tnew,'action', name = t, intID = str(actionCounter))
	actionCounter = actionCounter + 1

output_file = open('command_parser.xml','w')
output_file.write(ElementTree.tostring(tCmd))
output_file.close()
#print("****************************LOADING COMPLETE*****************************************")
sys.exit(0)
