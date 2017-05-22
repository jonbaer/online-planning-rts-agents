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
		
	print "\nHeld Resources"		
	for tgather in sim_gathering_action.keys():
		print "\nHeld Resource: ", tgather, " NumWorkers: ",sim_gathering_action[tgather]
		
	
	print "\n*************Game State - Volumetric Resourcs:*****************"
	for tKey in sim_volumetric_state:
		print sim_volumetric_state[tKey].name,  sim_volumetric_state[tKey].current_total
		
	print "Total GAME TIME: ", global_sim.game_time

#Function declarations and definitions
def calculatePlanFitness():
#	print "calculating plan fitness"
	minAmt = 0;
	gasAmt = 0;
	supAmt = 0;
	durAmt = 0;

	minGatherer = 0;
	gasGatherer = 0;
	suppGatherer = 0;

	minRate = 0;
	gasRate = 0;

	stateMinAmt = 0;
	stateGasAmt = 0;
	stateSuppAmt = 0;

	bldSuppMinAmt = 0;
	numSuppBldgNeeded = 0;

	#trying to minimize these so initalize at infinite values
	objDuration = 1000000;
	objProductionTime = 1000000;
	objMakespan = 1000000;
	minProductionTime =0;
	gasProductionTime =0;
	suppProductionTime =0;
	

	#Iterate through held_resources list to determine the rate of collection for gas and minerals & number of workers
	for tgather in sim_gathering_action.keys():
	    	if(tgather == "Mineral"):
			minGatherer = sim_gathering_action[tgather]
		if(tgather == "Gas"):
			gasGatherer = sim_gathering_action[tgather]
	
	#WARNING: Depending on the game, there might be other held resources that are hidden from sim_unary_state. 
	#Careful consideration of this must be done. Currently only workers are held resources and therefore handled appropriately
	for gUnary in global_sim.unary_goal_state.values():
		#print gUnary
		for sKey in sim_unary_state.keys():
		    #print sKey
		    if(sKey == gUnary.name):
			#Held_resources (workers) are hidden from the sim_unary_state so we need to include them as having been achieved
			if(sKey == "Worker"):
				diff = gUnary.total_amt - len(sim_unary_state[sKey]) - minGatherer - gasGatherer
#				print "worker diff: ", gUnary.total_amt, " - ", len(sim_unary_state[sKey]), " - ", minGatherer
			else:
				diff = gUnary.total_amt - len(sim_unary_state[sKey])
				#print "gUnary Name: ", gUnary.name, " sKeyUnary Name: ", sKey
				#print gUnary.name, " diff: ", gUnary.total_amt, " - ", len(sim_unary_state[sKey])
			#print gUnary.name, " difference: ", diff, "\n"
			if(diff > 0):
				minAmt = minAmt + (gUnary.minCostEa * diff)
				gasAmt = gasAmt + (gUnary.gasCostEa * diff)
				supAmt = supAmt + (gUnary.suppCostEa * diff)
				durAmt = durAmt + (gUnary.durAmtEa * diff)
#			if(diff < 0):
#				minAmt = minAmt - (gUnary.minCostEa * diff)
#				gasAmt = gasAmt - (gUnary.gasCostEa * diff)
#				supAmt = supAmt - (gUnary.suppCostEa * diff)
#				durAmt = durAmt - (gUnary.durAmtEa * diff)
	for gUnit in global_sim.unit_goals.values():
		for sKey in sim_combatUnit_state.keys():
			if(gUnit.name == sKey):
				diff = gUnit.total_amt - sim_combatUnit_state[sKey].total_amt
				#print "gUnit Name: ", gUnit.name, " sKeygUnit Name: ", sKey

				#print gUnit.name, " diff: ", gUnit.total_amt, " - ", sim_combatUnit_state[sKey].total_amt
				#print gUnit.name, " difference: ", diff, "\n"
				if(diff >0):
					minAmt = minAmt + (gUnit.minCostEa*diff)
					gasAmt = gasAmt + (gUnit.gasCostEa*diff)
					supAmt = supAmt + (gUnit.suppCostEa*diff)
					durAmt = durAmt + (gUnit.durAmtEa*diff)
				
	
#	print "Mineral Gatherers: ", minGatherer, " Gas Gatherers: ", gasGatherer
		 	
	for tKey in sim_volumetric_state.keys():
		for tVol in sim_volumetric_state.values():
			if(tVol.name == "Mineral"):
				minRate = tVol.accumulation_rate
				stateMinAmt = tVol.current_total
			elif(tVol.name == "Gas"):
				gasRate = tVol.accumulation_rate
				stateGasAmt = tVol.current_total
			elif(tVol.name == "Supply"):
				stateSuppAmt = tVol.current_total

#	print "gas rate: ", gasRate, "min rate: ", minRate

	#is this in seconds or gamecycles? Important to know
	#calculates how much more time is needed to collect minerals to meet goal state
		
	if(minAmt - stateMinAmt >0):
		if(minGatherer >0): #avoid divide by zero
			minProductionTime = (minAmt - stateMinAmt)/(minRate*minGatherer)
		else: #no gathers so set time to infinite
			minProductionTime = 1000000

	#calculates how much more time is needed to collect gas to meet goal state
	if(gasAmt - stateGasAmt >0):
		print gasAmt
		if(gasGatherer >0): #avoid divide by zero
			gasProductionTime = (gasAmt - stateGasAmt)/(gasRate*gasGatherer)
		else: #no gathers so set time to infinite
			gasProductionTime = 1000000

	#Obtaining information on supply depot in order to perform calculations below this for-loop
#	for tKey in global_sim.action_definitions.keys():
#		if(tKey == "Build_SupplyDepot"):
#			tAction = global_sim.action_definitions[tKey]
#			for aKey in tAction.vol_res_dict.keys():
#				if(aKey == "Mineral"):
#					bldSuppMinAmt = tAction.vol_res_dict[aKey]				
#					print "Supply Depot Cost: ", bldSuppMinAmt
				 
				
	#calculates how much more time is needed to build supply to meet goal state
#	if(supAmt - stateSuppAmt > 0):
		#WARNING: 10 is a user defined value (vol rate) that should be derived from xml (validate number is correct)
#		numSuppBldgNeeded = math.ceil((supAmt - stateSuppAmt)/10)
#		bldSuppMinAmt = bldSuppMinAmt * numSuppBldgNeeded

		#avoid divide by zero; if i have workers gathering and need more resources to build supply depot
#		if(minGatherer >0 and (stateMinAmt - bldSuppMinAmt <= 0)): 
#			suppProductionTime = (bldSuppMinAmt - stateMinAmt)/(minRate*minGatherer)
#		elif(stateMinAmt - bldSuppMinAmt >= 0): #have enough to bld supply
#			suppProductionTime = 0
#		elif(minGatherer < 0):
#			suppProductionTime = 1000000
		
	
	#Finalize the fitness values for the action plan
#	objProductionTime = minProductionTime + gasProductionTime + suppProductionTime
	objProductionTime = minProductionTime + gasProductionTime
	
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
def processEffect(efxKey,tUnary, efxValue):
	#print "Processing Effect for: ", tUnary.name
	#Increment Effect - add a new unary resource object of type efxValue to the game state
	if(efxKey == global_sim.effect_increment):
	#	print("\nIncrement Effect")#Bug here, "Marine" effect is only for combat_unit_definitions not unary_definitions...must fix this
	#	print "efxKey: ",efxKey, " efxValue: ",efxValue
		tNewUnary = copy.deepcopy(global_sim.unary_definitions[efxValue])
#		print(tNewUnary.name)
		sim_unary_state[efxValue].append(tNewUnary)
		tUnary.nextAction()
		# if(tUnary.action!=0):
			# tUnary.getWorkLoad()
			# print tUnary.name, " ", tUnary.action.name, " ",tUnary.workload
	
	if(efxKey == global_sim.effect_UnitIncrement):
		#print("\nUnit Increment Effect...Nothing is updated yet, this part of the simulator is incomplete")
		sim_combatUnit_state[efxValue].total_amt = sim_combatUnit_state[efxValue].total_amt +1
		tUnary.nextAction()
	#Decrement Effect - remove a unary resource object from the game state
	#Not Implemented
	
	#Accumulate Effect - Based on the rate of production increase the volumetric resource
	if(efxKey == global_sim.effect_accumulate):
		#print("Accumulate Effect")
		sim_volumetric_state[efxValue].processAccumulatedAmount(FRAMES_PER_SEC)	

	if(efxKey == global_sim.effect_accum_fixed):
#		print("\nFixed Accumulation Effect")
		sim_volumetric_state[efxValue].processAccumulatedAmount(FRAMES_PER_SEC)
		tUnary.nextAction()
	
	#NOP Effect
	if(efxKey == global_sim.effect_nop):
		#do nothing
		return
	
def checkSimulationCompleted():
	#print("checking")
	for tKey in sim_unary_state.keys():
		for tUnary in sim_unary_state[tKey]:
			tUnary.getWorkLoad()
			# if(tUnary.action != 0):
				# print(tUnary.name, " ",tUnary.action.name, " ", tUnary.workload," ",tUnary.action.duration)
				#if(tUnary.workload > 0):
				#	print(tUnary.name, " ", tUnary.workload)
				#	return False
			if(tUnary.workload > 0):
				#print "not completed ", global_sim.game_time
				return False
			
	
		
	# for tKey in sim_unary_state.keys():
		# for tUnary in sim_unary_state[tKey]:
			# print tUnary.name
			# if(tUnary.action != 0):
				# print(tUnary.name, " ",tUnary.action.name, " ", tUnary.workload," ",tUnary.action.duration)
	
	# for tUnary in held_resources:
			# print tUnary.name, tUnary.time_till_completion
			
#	print ("*************************Simulation Completed*************************")
	return True

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

	
def checkCummulativeConstraint(tmpAct):
	
	for volRes in tmpAct.vol_res_dict.keys():
		resDiff = sim_volumetric_state[volRes].current_total - tmpAct.vol_res_dict[volRes]
		#print sim_volumetric_state[volRes].current_total, " - ", tmpAct.vol_res_dict[volRes], " = ", resDiff
		if(resDiff < 0):
			for tgather in sim_gathering_action:
				##check if workers are gathering the resource named volRes
				numWorkersGathering = sim_gathering_action[tgather]
				if(tgather == volRes and numWorkersGathering>0):
					tVol = sim_volumetric_state[tgather]
					delay_time = (-1*resDiff)/(tVol.accumulation_rate * numWorkersGathering)
					return delay_time; #resource is being gathered so return False to trigger waiting
							
			#if this point is reached then there is no held resource accumulating the required resource; fail the action; grab a new action from the plan		
			return fail 		
	return 0 #delay_time =0

#allocate action to the unary resource object/instance with zero workload or idle
# ---Check that unary resource is avail or created
# ---Check if action has a hold effect on a resource
# ---Allocates two types of ations (gathering and non-gathering actions)
#	--gathering actions have the 'held' effect in their effects_list while non-gathering do not
#	--nongathering actions have a delay time if they have to wait for a unary resource to become avail
#	--gathering actions are not allowed to wait, they are automatically failed if a worker is unavail or unary resource unavail
#---Calls the processUnaryResources() for non-gathering actions whether or not they have a delay_time > 0 or equal to zero (meaning they can execute now)
#---Does NOT call processUnaryResources() for gathering ations
def allocateAction(tmpAct, cummulativeDelayTime):
	tUnaryList = []
	delayTime = 0
	#First verify the unary resources requried have been created or are in the game state
	for tUnaryName in tmpAct.unary_res_list:
		#Verify the unary resource exist
		if(len(sim_unary_state[tUnaryName])<1):
			#print "Unary Resource ", tUnaryName , " Has not been created."
			return fail
	
	#Now check if action has effect of holding a resource (generally a gather resource action)
	#Currently limited to handeling actions that have the 'hold' effect specified in their exist_list
	#This includes only gathering actions (i.e gold, minerals, etc). There is no waiting or delay for gathering actions.
	for tEffectKey in tmpAct.effects_dict.keys():
		if(tEffectKey == global_sim.effect_hold):
			resName = tmpAct.effects_dict[tEffectKey]
			#print "Holding Resource" ,resName
			for tRes in sim_unary_state[resName]:
				tRes.getWorkLoad()
				tUnaryList.append(tRes)
				#Worker must be idle to assign to gathering action
				#Sort the list of unary objects by workload for the specified type of unary resource
			tUnaryList = sorted(tUnaryList, key=attrgetter('workload'), reverse = False)
			if(tUnaryList[0].workload <= 0):			
				#allocate the action to the resource with the smallest workload
				tUnaryList[0].addAction(tmpAct)
				del tUnaryList[0] #delete the unary resource/workere (now unavail for other actions)
				#update game state to reflect removal of held resource - resource no longer avail to other actions
				sim_unary_state[resName] = tUnaryList[:]
				sim_gathering_action[tmpAct.name] = sim_gathering_action[tmpAct.name] +1
				return 0
			else:
				return fail

	#tUnaryList[:] = []		
	#This for-loop handles allocation of actions where the effect HOLD does not apply
	for tUnaryName in tmpAct.unary_res_list:
		#Locate the unary type list in the sim_unary_state
		for tRes in sim_unary_state[tUnaryName]:
			tRes.getWorkLoad()
			tUnaryList.append(tRes)
	
		#Sort the list of unary objects by time_till_completion for the specified type of unary resource
		tUnaryList = sorted(tUnaryList, key=attrgetter('time_till_completion'), reverse = False)
		#allocate the action to the resource with the smallest time_till_completion (this becomes delay_time)
		if(cummulativeDelayTime >= tUnaryList[0].time_till_completion):
			delayTime = cummulativeDelayTime
		else:
			delayTime = tUnaryList[0].time_till_completion
		
		tUnaryList[0].addAction(tmpAct)
		sim_unary_state[tUnaryName] = tUnaryList[:]	
		processUnaryResources(delayTime)
		
		
		
					
		#if(len(tUnaryList[0].action_queue) > 0):
		#	if(tUnaryList[0].action != 0):
				#print tUnaryList[0].name, tUnaryList[0].action.name
		#		for _tAction in tUnaryList[0].action_queue:
		#			if(_tAction == 0):
		#				print tUnaryList[0].name, " & Action:", "NO ACTION"
		#			else:
		#				print tUnaryList[0].name, " & Action:", _tAction.name
	return 0 
	
#may need to consider checking for empty action queues of unary objects to avoid errors	
#Runs through each unary resource in the game state and processes their actions.
#DOES NOT tell the unary resource to grab a next action or change the resources action.
#Does process effects of actions when applicable.
#Must process unary resources contained in the dictionaries sim_unary_state and held_resources 
#Updates level of volumetric resources given the passage of time and number of workers gathering
#UPDATES GAME_TIME
def processUnaryResources(Time):
	#print "processing unary resources"
	#print "size of sim_unary_state ", len(sim_unary_state["Worker"])
	#print "size of held_resource ", len(held_resources)
	volTotal = 0;
	accumRate = 0;
	
	for tKey in sim_unary_state.keys():
		#print('key', tKey) 
		for tUnary in sim_unary_state[tKey]:
			tFlag = tUnary.update(Time)
			#print "tFlag ", tFlag
			if(tFlag == global_sim.process_effect):
				#print "handeling sim state resource action"
				#print("Sim_State_Effects: Action Completed...Processing Effect Now...")
				#print tUnary.action.name
				for tEffect in tUnary.action.effects_dict.keys():
					#print tUnary.action.name, " ", tEffect, " ",tUnary.action.effects_dict[tEffect]
					processEffect(tEffect,tUnary,tUnary.action.effects_dict[tEffect])

	#update volumetric resources with respect to the passage of Time
	for tgather in sim_gathering_action.keys():
		volTotal = sim_volumetric_state[tgather].current_total
		accumRate = sim_volumetric_state[tgather].accumulation_rate
		sim_volumetric_state[tgather].current_total = volTotal + (accumRate*sim_gathering_action[tgather]*Time)
	
	global_sim.game_time = global_sim.game_time + Time #in seconds

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



#Write action plan to file
#global_sim.f.write("\n")
#global_sim.f.write("StringLen: %s " %len(global_sim.action_plan_string))
#global_sim.f.write("ActionPlanLen: %s \n" %len(global_sim.action_plan))


#for aps in global_sim.action_plan_string:
#	global_sim.f.write("%s " % aps)
#global_sim.f.write("\n")

#for ap in global_sim.action_plan:
#	global_sim.f.write("%s " % ap.name)
#global_sim.f.write("\n")


simulation_completed = False
cummulative_constraint_flag = fail;
disjunctive_constraint_flag = fail;
actionCounter = -1

while(len(action_plan) > 0 ):  #while still actions to schedule
	
	#retrieve action from plan
	tAction = action_plan.popleft()
	actionCounter = actionCounter+1
		
	#print "Retrieved Next Action from Build Order Plan: ", tAction.name, tAction.duration, global_sim.game_time
	if(binary_plan[actionCounter] == 1):	
		#STEP1 - Check Exist/Tech Ordering Constraint
		if(checkExistConstraint(tAction)):
			#print "Passed Exist Constraint: ", True
			#STEP2 - Check Cummulative Constraints
			cummulative_constraint_flag = checkCummulativeConstraint(tAction)
			if(cummulative_constraint_flag >=0): #zero is associated with a delay_time of zero
	#			print "Passed Cummulative Constraint: Delay Time = ", cummulative_constraint_flag
				disjunctive_constraint_flag = allocateAction(tAction, cummulative_constraint_flag) #returns delay_time of >= 0 or a fail flag == -3
			
				if(disjunctive_constraint_flag >= 0):
	#				print "Passed Disjunctive Constraint: ", disjunctive_constraint_flag
					#update volumetric resource levels b/c the action has been assigned to a unary resource
					for volRes in tAction.vol_res_dict.keys():
						sim_volumetric_state[volRes].current_total = sim_volumetric_state[volRes].current_total - tAction.vol_res_dict[volRes]
				else:#fail flag
	#				print "Failed Disjunctive Constraint: ", disjunctive_constraint_flag
				
					global_sim.binary_dec_bits.append(actionCounter)
	
			elif(cummulative_constraint_flag == fail):
	#			print tAction.name, " Action is infeasible wrt Cummulative Constraint: ", fail,actionCounter
				global_sim.binary_dec_bits.append(actionCounter)
				#print "Going to grab the next action from the action plan..."	
		else:
			#print tAction.name, " Failed Exist Constraint: ", False,actionCounter
			global_sim.binary_dec_bits.append(actionCounter)
	
	
	#processUnaryResources(DELTA_TIME)
	
	delay_time = 0 #reset delay time with each iteration

		#STEP2 - Check Cummulative Constraints
		#	   	-- Must be able to handle waiting situation for when vol not avail yet	
		#STEP3 - Schedule action to unary resource
		#STEP4 - Update Unary Resources
		#	   -- Process actions and effects
		#STEP5 - Update Volumetric Resources

#print("Broke out")
while(simulation_completed == False):

	processUnaryResources(DELTA_TIME)

	#game_time = game_time + DELTA_TIME #in seconds
	simulation_completed = checkSimulationCompleted()


#printGameStateInfo()	
calculatePlanFitness()
#print global_sim.binary_dec_bits


		
