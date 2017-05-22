from collections import deque
from operator import attrgetter
import math
import copy
import unary
import volumetric
import actions
import effects
import global_sim
from global_sim import fail, unary_resource_state, volumetric_resource_state, combat_unit_state, fitness_values, action_plan

#Constant Values
DELTA_TIME = 1; #seconds
FRAMES_PER_SEC = 1; #frames per second 


#Game Clock

def printActionTable():
	print "Current Game State for action table below: \n"
	print "M/E Collection Rates: ", sim_volumetric_state["armmex"].collection_rate, "/", sim_volumetric_state["armsolar"].collection_rate
	print "M/E Production Rates: ", sim_volumetric_state["armmex"].production_rate, "/", sim_volumetric_state["armsolar"].production_rate
	print "M/E Quantities: ", sim_volumetric_state["armmex"].quantity, "/", sim_volumetric_state["armsolar"].quantity
	print "M/E Capacities: ", sim_volumetric_state["armmex"].capacity, "/", sim_volumetric_state["armsolar"].capacity

	for tAct in sim_activeAct_list:
		print "\n", "*********************"
		print "Name: ", tAct.name
		print "workTime: ", tAct.unary_ptr.worktime
		print "duration: ", tAct.duration
		print "m_cost: ", tAct.vol_cost_dict["armmex"]
		print "e_cost: ", tAct.vol_cost_dict["armsolar"]
		print "actM_cr: ", tAct.actM_cr
		print "actE_cr: ", tAct.actE_cr
		print "OptM_cr: ", tAct.optM_cr
		print "OptE_cr: ", tAct.optE_cr

	return

def printGameStateInfo():
	print "\n**************Game State - Unary Resources:**************"

	for tKey in sim_unary_state.keys():
		print "\n"
		print tKey, len(sim_unary_state[tKey])
		for tUnary in sim_unary_state[tKey]:
			if(len(tUnary.action_queue) > 0):
				for _tAction in tUnary.action_queue:
					if(_tAction == 0):
						print tUnary.name, " & Action:", "NO ACTION"
					else:
						print tUnary.name, " & Action:", tUnary.action.name
			elif(tUnary.action == 0):
				print tUnary.name, " & Action:", "NO ACTION"
			else:
				print tUnary.name, " & Action:", tUnary.action.name
		
			
	
	print "\n*************Game State - Volumetric Resourcs:*****************"
	for tKey in sim_volumetric_state:
		print sim_volumetric_state[tKey].name,  sim_volumetric_state[tKey].quantity
		
	print "Total GAME TIME: ", global_sim.game_time

#Function declarations and definitions
def calculatePlanFitness():
#	print "calculating plan fitness"
	metalRate = 0
	nrgRate = 0
	metalCapacity = 0
	nrgCapacity = 0
	numCombatUnit =0
	numConBotsAssisting = 0
	metAmt = 0
	nrgAmt = 0
	durAmt = 0

	#trying to minimize these so initalize at infinite values
	objDuration = 1000000;
	objProductionTime = 1000000;
	objMakespan = 1000000;
	metProductionTime =0;
	nrgProductionTime =0;
	

	#Determine number of construction bots assisting the commander
	for tgather in sim_gathering_action.keys():
	    	if(tgather == "Assist_Commander"):
			numConBotsAssisting = sim_gathering_action[tgather]
		
	
	#WARNING: Depending on the game, there might be other held resources that are hidden from sim_unary_state. 
	#Careful consideration of this must be done. Currently only workers are held resources and therefore handled appropriately
	for gUnary in global_sim.unary_goal_state.values():
		#print gUnary
		for sKey in sim_unary_state.keys():
		    #print sKey
		    if(sKey == gUnary.name):
			diff = gUnary.total_amt - len(sim_unary_state[sKey])
			#print "gUnary Name: ", gUnary.name, " sKeyUnary Name: ", sKey
			#print gUnary.name, " diff: ", gUnary.total_amt, " - ", len(sim_unary_state[sKey])
			#print gUnary.name, " difference: ", diff, "\n"
			if(diff > 0):
				metAmt = metAmt + (gUnary.minCostEa * diff)
				nrgAmt = nrgAmt + (gUnary.gasCostEa * diff)
				durAmt = durAmt + (gUnary.durAmtEa * diff)/300
#			if(diff < 0):
#				metAmt = metAmt - (gUnary.minCostEa * diff)
#				nrgAmt = nrgAmt - (gUnary.gasCostEa * diff)
#				durAmt = durAmt - (gUnary.durAmtEa * diff)/300


	for gUnit in global_sim.unit_goals.values():
		for sKey in sim_combatUnit_state.keys():
			if(gUnit.name == sKey):
				diff = gUnit.total_amt - sim_combatUnit_state[sKey].total_amt
				#print "gUnit Name: ", gUnit.name, " sKeygUnit Name: ", sKey

				#print gUnit.name, " diff: ", gUnit.total_amt, " - ", sim_combatUnit_state[sKey].total_amt
				#print gUnit.name, " difference: ", diff, "\n"
				if(diff >0):
					metAmt = metAmt + (gUnit.minCostEa*diff)
					nrgAmt = nrgAmt + (gUnit.gasCostEa*diff)
					durAmt = durAmt + (gUnit.durAmtEa*diff)/100
#				if(diff < 0):
#					metAmt = metAmt - (gUnit.minCostEa*diff)
#					nrgAmt = nrgAmt - (gUnit.gasCostEa*diff)
#					durAmt = durAmt - (gUnit.durAmtEa*diff)/100
	
			 	
	for tVol in sim_volumetric_state.values():
		if(tVol.name == "armmex"):
			metRate = tVol.collection_rate
			stateMetAmt = tVol.quantity
		elif(tVol.name == "armsolar"):
			nrgRate = tVol.collection_rate
			stateNrgAmt = tVol.quantity
		

#	print "gas rate: ", gasRate, "min rate: ", minRate

	#is this in seconds or gamecycles? Important to know
	#calculates how much more time is needed to collect minerals to meet goal state
	if(stateMetAmt <0):	
		if(metAmt > 0):
			metProductionTime = (metAmt - stateMetAmt)/(metRate)
		else:
			metProductionTime = 0
	elif(metAmt - stateMetAmt >0):
		metProductionTime = (metAmt - stateMetAmt)/(metRate)
		
	#calculates how much more time is needed to collect gas to meet goal state
	if(stateNrgAmt <0):	
		if(nrgAmt > 0):
			nrgProductionTime = (nrgAmt - stateNrgAmt)/(nrgRate)
		else:
			nrgProductionTime = 0
	elif(nrgAmt - stateNrgAmt >0):
		nrgProductionTime = (nrgAmt - stateNrgAmt)/(nrgRate)
		
	
	#Finalize the fitness values for the action plan
#	objProductionTime = minProductionTime + gasProductionTime + suppProductionTime
	#if(metProductionTime >= nrgProductionTime):
	objProductionTime = metProductionTime + nrgProductionTime
	#else:
	#	objProductionTime = nrgProductionTime
	
	#time required to build the supBldgs; WARNING: 40 is user defined value (action duration) that should be derived from xml (validate # correct)
#	objDuration = durAmt + (numSuppBldgNeeded*40)
	objDuration = durAmt

	objMakespan = global_sim.game_time

	fitness_values[0] = objDuration
	fitness_values[1] = objProductionTime
	fitness_values[2] = objMakespan
	
#	print "Objective Scores: ", "Dur: ", fitness_values[0], " PT: ", fitness_values[1], " Makespan: ", fitness_values[2]
	
#Processes action effects of unary resources
#and tells unary resource to start next action depending on the effect of the action last processed	
def processEffect(efxKey, efxValue):
	BAgameCycles= 0
#	print "Processing Effect for: ", tUnary.name, " on action ", tUnary.action.name

	#Increment Effect - add a new unary resource object of type efxValue to the game state
	if(efxKey == global_sim.effect_increment):
		#print("\nIncrement Effect")#Bug here, "Marine" effect is only for combat_unit_definitions not unary_definitions...must fix this
		#print "efxKey: ",efxKey, " efxValue: ",efxValue
		tNewUnary = copy.deepcopy(global_sim.unary_definitions[efxValue])
	#	print(tNewUnary.name)
		sim_unary_state[efxValue].append(tNewUnary)
		#tUnary.nextAction()
		#effectConsumptionRates(tUnary.action)
		return
		# if(tUnary.action!=0):
			# tUnary.getWorkLoad()
			# print tUnary.name, " ", tUnary.action.name, " ",tUnary.workload
	
	#Decrement Effect - remove a unary resource object from the game state
	#Not Implemented
	
	#Accumulate Effect - Based on the rate of production increase the volumetric resource
	if(efxKey == global_sim.effect_accum_metal):
	#	print("Accum_Metal Effect")
		sim_volumetric_state["armmex"].collection_rate = sim_volumetric_state["armmex"].collection_rate + float(efxValue)		
		sim_volumetric_state["armmex"].capacity = sim_volumetric_state["armmex"].capacity + 50;
		#effectConsumptionRates(tUnary.action)
		#tUnary.nextAction()
		return
	if(efxKey == global_sim.effect_accum_NRG):
	#	print("Accum_NRG Effect")
		sim_volumetric_state["armsolar"].collection_rate = sim_volumetric_state["armsolar"].collection_rate + float(efxValue)
		sim_volumetric_state["armsolar"].capacity = sim_volumetric_state["armsolar"].capacity + 50;
		#tUnary.nextAction()
		#effectConsumptionRates(tUnary.action)
		return
	
	if(efxKey == global_sim.effect_IncrementUnit):
	#	print "incrementing_unit ", efxValue
		sim_combatUnit_state[efxValue].total_amt = sim_combatUnit_state[efxValue].total_amt + 1
		#tUnary.nextAction()
		
		return
	#assist commander effect
	if(efxKey == global_sim.effect_CmdWorkTime):
		comList = sim_unary_state["armcom"]
		commander = comList[0]
		
		commander.worktime = commander.worktime + float(efxValue)
		
		#tUnary.nextAction()
		return
	#assist factory effect
	if(efxKey == global_sim.effect_LabWorkTime):
		tUnaryList = []
		comList = sim_unary_state["armcom"]
		commander = comList[0]
		#Determine the factory/lab that is the busiest and assign the commander to assist them		
		for tRes in sim_unary_state["armlab"]:
			tRes.getWorkLoad()
			tUnaryList.append(tRes)
		
		tUnaryList = sorted(tUnaryList, key=attrgetter('workload'), reverse = True)
		#print tUnaryList[0].name, tUnaryList[0].action	
		
		tUnaryList[0].worktime = tUnaryList[0].worktime + commander.worktime
		commander.assist_lab = tUnaryList[0]
		#with the updated cmd worktime calculate the new remaining action duration in seconds
		sim_unary_state["armlab"] = tUnaryList[:]
		tUnaryList[:] = ()
		#tUnary.nextAction()
		return

	if(efxKey == global_sim.effect_MetalCapacity):
	#	print "Effect Increasing Metal Capacity"
		sim_volumetric_state["armmex"].capacity = sim_volumetric_state["armmex"].capacity + float(efxValue)
		return

	if(efxKey == global_sim.effect_NRGCapacity):
	#	print "Effect Increasing NRG Capacity"
		sim_volumetric_state["armsolar"].capacity = sim_volumetric_state["armsolar"].capacity + float(efxValue)
		return

	#NOP Effect
	if(efxKey == global_sim.effect_nop):
		#do nothing
		return
	
def checkSimulationCompleted():
	#print("checking")
	if(len(sim_activeAct_list) <= 0):
		return True
#	print ("*************************Simulation Completed*************************")
	return False

#This constraint should fail and invalidate an action if there does not exist in the simulation state the items
#listed in the actions exist_list (refer to commands.xml). For example, in starcraft a barracks must exist before
#an academy can be constructed or a refinery must exist before gas can be collected, etc.
def checkExistConstraint(tmpAct):
	if(len(tmpAct.exist_list) > 0):
			for i in range(1,len(tmpAct.exist_list)+1):
				#print "exist", i
				conNameExist = tmpAct.exist_list.pop()
				if(len(sim_unary_state[conNameExist]) < 1):
					return False
				
	return True	

def checkDisjunctiveConstraint(tmpAct):

	for tUnaryName in tmpAct.unary_res_list:
		#Verify the unary resource exist
		if(len(sim_unary_state[tUnaryName])<1):
			#print "Unary Resource ", tUnaryName , " Has not been created."
			return fail

	for tUnary in tmpAct.unary_res_list:
		for sUnary in sim_unary_state.keys():
			if(tUnary == sUnary):
				unaryList = sim_unary_state[sUnary]
				for inst in unaryList:
					if(inst.owned == 0):
						inst.owned = 1
						tmpAct.unary_ptr = inst
						if(tAction.name == "Assist_Armlab"):
							inst.owned = 2						
						return global_sim.avail	
					#2 corresponds to action "assist_armlab"; used by commanders only.
					# this enables the commander to be removed from assisting to address other actions
					# aside from another assist command
					elif(inst.owned == 2 and tAction.name != "Assist_Armlab"):
						inst.owned =1
						tmpAct.unary_ptr = inst
						inst.assist_lab.worktime = 100
						return global_sim.avail
					elif(inst.owned == 2 and tAction.name == "Assist_Armlab"):
						return global_sim.fail
					
	if(tAction.name == "Assist_Armcom"):
		return global_sim.fail
	return global_sim.wait

			

def decConsumeRatesMetal():
	cummWorkTime = 0
	colRatePerWkTimeSec = 0
	dynamicDuration = 0
	
	for tAct in sim_activeAct_list:
		cummWorkTime = cummWorkTime + tAct.unary_ptr.worktime

	colRatePerWkTimeSec = sim_volumetric_state["armmex"].collection_rate/cummWorkTime	
	
	for tAct in sim_activeAct_list:
		#printActionTable()
		#print tAct.vol_cost_dict["armmex"], " ", tAct.vol_cost_dict["armsolar"]
		tAct.actM_cr = colRatePerWkTimeSec * tAct.unary_ptr.worktime
		dynamicDuration = tAct.vol_cost_dict["armmex"]/tAct.actM_cr
		tAct.actE_cr = tAct.vol_cost_dict["armsolar"]/dynamicDuration

	return

def decConsumeRatesEnergy():
	cummWorkTime = 0
	colRatePerWkTimeSec = 0
	dynamicDuration = 0
	
	for tAct in sim_activeAct_list:
		cummWorkTime = cummWorkTime + tAct.unary_ptr.worktime

	colRatePerWkTimeSec = sim_volumetric_state["armsolar"].collection_rate/cummWorkTime	
	
	
	for tAct in sim_activeAct_list:
		
		tAct.actE_cr = colRatePerWkTimeSec * tAct.unary_ptr.worktime
		dynamicDuration = tAct.vol_cost_dict["armsolar"]/tAct.actE_cr
		if(dynamicDuration == 0):
			tAct.actM_cr = (sim_volumetric_state["armmex"].collection_rate/cummWorkTime)*  tAct.unary_ptr.worktime
			tAct.actE_cr = 0
		else:
			tAct.actM_cr = tAct.vol_cost_dict["armmex"]/dynamicDuration
	
	return


def updateGameState():
#	print "\n##Updating Game state##\n"
	global_sim.game_time = global_sim.game_time + DELTA_TIME
	cummActM_cr = 0
	cummActE_cr = 0	
	MAL = 0
	EAL = 0
	McolRate = sim_volumetric_state["armmex"].collection_rate
	EcolRate = sim_volumetric_state["armsolar"].collection_rate
	
	for tAct in sim_activeAct_list:
		cummActM_cr = cummActM_cr + tAct.actM_cr	
		cummActE_cr = cummActE_cr + tAct.actE_cr
	
	MAL = sim_volumetric_state["armmex"].quantity - ((cummActM_cr - McolRate) * DELTA_TIME)
	EAL = sim_volumetric_state["armsolar"].quantity - ((cummActE_cr - EcolRate) * DELTA_TIME)

	if(MAL > sim_volumetric_state["armmex"].capacity):
		MAL = sim_volumetric_state["armmex"].capacity
	if(EAL > sim_volumetric_state["armsolar"].capacity):
		EAL = sim_volumetric_state["armsolar"].capacity	
	#printActionTable()		
	if(MAL >=0 and EAL >= 0):
		sim_volumetric_state["armmex"].quantity = MAL
		sim_volumetric_state["armsolar"].quantity = EAL
		return
	else:
		if(sim_volumetric_state["armmex"].production_rate > 0):
			sim_volumetric_state["armmex"].ratio = sim_volumetric_state["armmex"].collection_rate/sim_volumetric_state["armmex"].production_rate
		else:
			sim_volumetric_state["armmex"].ratio = 1
		if(sim_volumetric_state["armsolar"].production_rate >0):
			sim_volumetric_state["armsolar"].ratio = sim_volumetric_state["armsolar"].collection_rate/sim_volumetric_state["armsolar"].production_rate
		else:
			sim_volumetric_state["armsolar"].ratio = 1
		if(sim_volumetric_state["armmex"].ratio <= sim_volumetric_state["armsolar"].ratio):
			#print "metal"			
			decConsumeRatesMetal()
		else:
			#print "Energy"
			decConsumeRatesEnergy()	
	
		cummActM_cr = 0
		cummActE_cr = 0
		for tAct in sim_activeAct_list:
			cummActM_cr = cummActM_cr + tAct.actM_cr	
			cummActE_cr = cummActE_cr + tAct.actE_cr

		MAL = sim_volumetric_state["armmex"].quantity - ((cummActM_cr - McolRate) * DELTA_TIME)
		EAL = sim_volumetric_state["armsolar"].quantity - ((cummActE_cr - EcolRate) * DELTA_TIME)
	
		if(MAL > sim_volumetric_state["armmex"].capacity):
			MAL = sim_volumetric_state["armmex"].capacity
		if(EAL > sim_volumetric_state["armsolar"].capacity):
			EAL = sim_volumetric_state["armsolar"].capacity	
	
		if(MAL < 0 or EAL < 0):
			#printActionTable()
			#print "1stupdateGameState(): MAL or EAL can't be negative ", MAL, " ", EAL
			#sys.exit(0)
			if(MAL < 0):
				decConsumeRatesMetal()
			elif(EAL < 0):
				decConsumeRatesEnergy()
			
			cummActM_cr = 0
			cummActE_cr = 0
			for tAct in sim_activeAct_list:
				cummActM_cr = cummActM_cr + tAct.actM_cr	
				cummActE_cr = cummActE_cr + tAct.actE_cr

			MAL = sim_volumetric_state["armmex"].quantity - ((cummActM_cr - McolRate) * DELTA_TIME)
			EAL = sim_volumetric_state["armsolar"].quantity - ((cummActE_cr - EcolRate) * DELTA_TIME)
			if(MAL < 0 or EAL < 0):
				global_sim.game_time = global_sim.game_time + 1
				sim_volumetric_state["armmex"].quantity = sim_volumetric_state["armmex"].quantity + McolRate*1
				sim_volumetric_state["armsolar"].quantity = sim_volumetric_state["armsolar"].quantity + EcolRate*1
				MAL = sim_volumetric_state["armmex"].quantity - ((cummActM_cr - McolRate) * DELTA_TIME)
				EAL = sim_volumetric_state["armsolar"].quantity - ((cummActE_cr - EcolRate) * DELTA_TIME)
				
			if(MAL > sim_volumetric_state["armmex"].capacity):
				MAL = sim_volumetric_state["armmex"].capacity
			if(EAL > sim_volumetric_state["armsolar"].capacity):
				EAL = sim_volumetric_state["armsolar"].capacity	
				
			sim_volumetric_state["armmex"].quantity = MAL
			sim_volumetric_state["armsolar"].quantity = EAL
		
		return	
	
def updateActionList():
#	print "\n##Updating Action List##\n"
	list_index = 0
	keep_list = []
	temp_list = []
	for tAct in sim_activeAct_list:
		#print tAct.vol_cost_dict["armmex"], " =  ",tAct.vol_cost_dict["armmex"], " - ", (tAct.actM_cr * DELTA_TIME)
		tAct.vol_cost_dict["armmex"] = tAct.vol_cost_dict["armmex"] - (tAct.actM_cr * DELTA_TIME)
		
			
		#print tAct.vol_cost_dict["armsolar"], " =  ",tAct.vol_cost_dict["armsolar"], " - ", (tAct.actE_cr * DELTA_TIME)		
		tAct.vol_cost_dict["armsolar"] = tAct.vol_cost_dict["armsolar"] - (tAct.actE_cr * DELTA_TIME)
		#print 	tAct.vol_cost_dict["armsolar"]

		if(tAct.vol_cost_dict["armmex"] < 0): #and tAct.name == "Build_Armmex"):
			#print tAct.vol_cost_dict["armmex"]
			#sys.exit(0)
			tAct.vol_cost_dict["armmex"] = 0
			#print tAct.vol_cost_dict["armmex"], tAct.vol_cost_dict["armsolar"]
		if(tAct.vol_cost_dict["armsolar"] < 0):
			tAct.vol_cost_dict["armsolar"] = 0
		#print tAct.name, " ", tAct.vol_cost_dict["armmex"], tAct.vol_cost_dict["armsolar"]	

	for tAct in sim_activeAct_list:
		
		if((tAct.vol_cost_dict["armmex"]<1) and (tAct.vol_cost_dict["armsolar"] <1)):
			
			for tEffect in tAct.effects_dict.keys():
				processEffect(tEffect, tAct.effects_dict[tEffect])
			
			sim_volumetric_state["armmex"].production_rate = sim_volumetric_state["armmex"].production_rate - tAct.optM_cr
			sim_volumetric_state["armsolar"].production_rate = sim_volumetric_state["armsolar"].production_rate - tAct.optE_cr
			#releasing the unary resource
			tAct.unary_ptr.owned = 0
			#sim_activeAct_list.pop(list_index)
		else:
			keep_list.append(list_index)
			
		list_index = list_index + 1
		
	
		
	#Actions not included in the keep_list are removed from the sim_activeAct_list
	for num in keep_list:
		temp_list.append(sim_activeAct_list[num])

	sim_activeAct_list[:] = temp_list
	
	for tAct in sim_activeAct_list:
		
		if((tAct.actM_cr < tAct.optM_cr and tAct.actE_cr < tAct.optE_cr)):
			if(sim_volumetric_state["armmex"].production_rate > 0):
				sim_volumetric_state["armmex"].ratio = sim_volumetric_state["armmex"].collection_rate/sim_volumetric_state	["armmex"].production_rate
			else:
				sim_volumetric_state["armmex"].ratio = 1
			if(sim_volumetric_state["armsolar"].production_rate >0):
				sim_volumetric_state["armsolar"].ratio = sim_volumetric_state["armsolar"].collection_rate/sim_volumetric_state["armsolar"].production_rate
			else:
				sim_volumetric_state["armsolar"].ratio = 1
			if(sim_volumetric_state["armmex"].ratio <= sim_volumetric_state["armsolar"].ratio):
				decConsumeRatesMetal()
			else:
				decConsumeRatesEnergy()	
			return

	return

def allocateNewAction(tAction):
	#Avail: unary resource now owned by tAction
	#update action attributes/state

	if(tAction.name == "Assist_Armcom" or tAction.name == "Assist_Armlab"):
		for tEffect in tAction.effects_dict.keys():
			processEffect(tEffect, tAction.effects_dict[tEffect])
		return


	tAction.optM_cr = tAction.vol_cost_dict["armmex"]/ (tAction.duration/tAction.unary_ptr.worktime)
	tAction.optE_cr = tAction.vol_cost_dict["armsolar"]/(tAction.duration/tAction.unary_ptr.worktime)
	#update game state
	sim_volumetric_state["armmex"].production_rate = sim_volumetric_state["armmex"].production_rate + tAction.optM_cr
	sim_volumetric_state["armsolar"].production_rate = sim_volumetric_state["armsolar"].production_rate + tAction.optE_cr
	
	if((sim_volumetric_state["armmex"].quantity >0) and (sim_volumetric_state["armsolar"].quantity > 0)):
		tAction.actM_cr = tAction.optM_cr
		tAction.actE_cr = tAction.optE_cr
	else:
		if(sim_volumetric_state["armmex"].production_rate > 0):
			sim_volumetric_state["armmex"].ratio = sim_volumetric_state["armmex"].collection_rate/sim_volumetric_state	["armmex"].production_rate
		else:
			sim_volumetric_state["armmex"].ratio = 1
		if(sim_volumetric_state["armsolar"].production_rate >0):
			sim_volumetric_state["armsolar"].ratio = sim_volumetric_state["armsolar"].collection_rate/sim_volumetric_state["armsolar"].production_rate
		else:
			sim_volumetric_state["armsolar"].ratio = 1
		if(sim_volumetric_state["armmex"].ratio <= sim_volumetric_state["armsolar"].ratio):
			decConsumeRatesMetal()
		else:
			decConsumeRatesEnergy()	
	#add action to active list
	sim_activeAct_list.append(tAction)
	return			
#********Initialize simulator game state************************
#These are copies of the initialization state in order for the MOEA to utilize the same initial state #settings for each solution or plan it evaluates.
sim_unary_state = {}
sim_unary_state = copy.deepcopy(unary_resource_state)
sim_volumetric_state = {}
sim_volumetric_state = copy.deepcopy(volumetric_resource_state)
sim_combatUnit_state = {}
sim_combatUnit_state = copy.deepcopy(combat_unit_state)

sim_gathering_actions = {}
sim_gathering_action = copy.deepcopy(global_sim.gathering_actions)
sim_activeAct_list = []
#Contains the sequence of actions to be executed or the action plan
#print "*********************************Initializing Action Plan************************************"
global_sim.f= open("sim_log.txt","a")
binary_plan = []
action_list = []
#Initializing action plan from action_plan_string
for l in global_sim.action_definitions.keys():
	action_list.append(l)

actionCounter = 0
lenActionPlan = len(global_sim.action_plan_string)

for t in global_sim.action_plan_string:
	actionCounter = actionCounter + 1
	actNum = int(t)
	aKey = action_list[actNum]
	#print actionCounter, lenActionPlan
	if(actionCounter <= lenActionPlan/2):
		global_sim.action_plan.append(copy.deepcopy(global_sim.action_definitions[aKey]))

#During execution if a action is infeasible then we need to change its decision bit to 0 so that 
#the overall action plan becomes a feasible action plan.  This binary decision list must be passed
#back to jmetalcpp so it can update the solution accordingly

actionCounter = 0

for bd in global_sim.action_plan_string:
	if(actionCounter >= lenActionPlan/2):
		if(bd == 1):
			binary_plan.append(1)
		else:
			binary_plan.append(0)

	actionCounter = actionCounter + 1 



simulation_completed = False
disjunctive_constraint_flag = fail;
actionCounter = -1
wait_flag = False


while(len(action_plan) > 0 or wait_flag == True):  #while still actions to schedule
	
	#retrieve action from plan
	if(wait_flag == False):
		tAction = action_plan.popleft()
		actionCounter = actionCounter+1
		
#		print "Retrieved Next Action from Build Order Plan: ", tAction.name, " ",global_sim.game_time
		if(binary_plan[actionCounter] == 1):	
			#STEP1 - Check Exist/Tech Ordering Constraint
			if(checkExistConstraint(tAction)):
				#Step2 - Checks if unary resource is avail; Returns: 1 if avail, 2 if wait, -3 if fail
				disjunctive_constraint_flag = checkDisjunctiveConstraint(tAction)
				if(disjunctive_constraint_flag == global_sim.avail):			
					allocateNewAction(tAction)
#					print "#Action allocated"
					
					updateGameState()
#					print "#updated Game State"
#					printActionTable()					
					
					updateActionList()
#					print "#updated Action Table"
#					printActionTable()
				elif(disjunctive_constraint_flag == global_sim.wait):
					wait_flag = True
#					print "Waiting...: ", wait_flag
				elif(disjunctive_constraint_flag == global_sim.fail):
					global_sim.binary_dec_bits.append(actionCounter)
	
			else:
	#			print tAction.name, " Failed Exist Constraint: ", False,actionCounter
				global_sim.binary_dec_bits.append(actionCounter)
	
	if(wait_flag == True):
#		printActionTable()
		updateGameState()
#		print "#updated Game State"
#		printActionTable()								
		updateActionList()
#		print "#updated Action Table"
#		printActionTable()
		disjunctive_constraint_flag = checkDisjunctiveConstraint(tAction)
		if(disjunctive_constraint_flag == global_sim.avail):
			wait_flag = False
			allocateNewAction(tAction)
#			print "#Action allocated"
#			print "done waiting, action allocated"
			updateGameState()
#			print "#updated Game State"
#			printActionTable()
			updateActionList()
#			print "#updated Action Table"
			
#	print tAction.name
#	printActionTable()
#print("Broke out")

while(simulation_completed == False):
	
	updateGameState()
#	print "#updated Game State"
#	printActionTable()
	updateActionList()
#	print "#updated Action Table"
#	printActionTable()

	simulation_completed = checkSimulationCompleted()
	



#printActionTable()
#printGameStateInfo()	
calculatePlanFitness()



		
