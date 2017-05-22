from collections import deque
from operator import attrgetter
import copy
import unary
import volumetric
import actions
import effects
from global_sim import true, false, unary_resource_state, volumetric_resource_state, combat_unit_state

#Constant Values
DELTA_TIME = 1; #seconds
FRAMES_PER_SEC = 1; #frames per second 

#Game Clock
game_time = 0;  #seconds

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
	for hUnary in held_resources:
		print len(held_resources)
		if(hUnary.action == 0):
			print "\nHeld Resource: \n", hUnary.name, " & Action:", "NO ACTION"
		else:
			print "\nHeld Resource: \n", hUnary.name, " & Action:", hUnary.action.name
	
	print "\n*************Game State - Volumetric Resourcs:*****************"
	for tKey in sim_volumetric_state:
		print sim_volumetric_state[tKey].name,  sim_volumetric_state[tKey].current_total
		
	print "Total GAME TIME: ", game_time

#Function declarations and definitions
def calculatePlanFitness():
	print "calculating plan fitness"
	#uses the game state datastructures to derive values
	#need to provide an xml file specifying a goal state

#Processes action effects of unary resources
#and tells unary resource to start next action depending on the effect of the action last processed	
def processEffect(efxKey,tUnary, efxValue):
	
	#Increment Effect - add a new unary resource object of type efxValue to the game state
	if(efxKey == global_sim.effect_increment):
		print("\nIncrement Effect")
		tNewUnary = copy.deepcopy(global_sim.unary_definitions[efxValue])
		sim_unary_state[efxValue].append(tNewUnary)
		tUnary.nextAction()
		# if(tUnary.action!=0):
			# tUnary.getWorkLoad()
			# print tUnary.name, " ", tUnary.action.name, " ",tUnary.workload
	
	#Decrement Effect - remove a unary resource object from the game state
	#Not Implemented
	
	#Accumulate Effect - Based on the rate of production increase the volumetric resource
	if(efxKey == global_sim.effect_accumulate):
		#print("Accumulate Effect")
		sim_volumetric_state[efxValue].processAccumulatedAmount(FRAMES_PER_SEC)	

	if(efxKey == global_sim.effect_accum_fixed):
		print("\nFixed Accumulation Effect")
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
				#	return false
			if(tUnary.workload > 0):
				#print("not completed")
				return false
			
	for tUnary in held_resources:
		tUnary.getWorkLoad()
		if(tUnary.workload >0):
			
			return false
		
	# for tKey in sim_unary_state.keys():
		# for tUnary in sim_unary_state[tKey]:
			# print tUnary.name
			# if(tUnary.action != 0):
				# print(tUnary.name, " ",tUnary.action.name, " ", tUnary.workload," ",tUnary.action.duration)
	
	# for tUnary in held_resources:
			# print tUnary.name, tUnary.time_till_completion
			
	print ("*************************Simulation Completed*************************")
	return true
	
def checkExistConstraint(tmpAct):
	if(len(tmpAct.exist_list) > 0):
			for i in range(1,len(tmpAct.exist_list)+1):
				#print "exist", i
				conNameExist = tmpAct.exist_list.pop()
				if(len(sim_unary_state[conNameExist]) < 1):
					return false
	return true	

	
def checkCummulativeConstraint(tmpAct):
	for volRes in tmpAct.vol_res_dict.keys():
		resDiff = sim_volumetric_state[volRes].current_total - tmpAct.vol_res_dict[volRes]
		#print sim_volumetric_state[volRes].current_total, " - ", tmpAct.vol_res_dict[volRes], " = ", resDiff
		if(resDiff < 0):
			return false		
	return true

#allocate action to the unary resource object/instance with the smallest workload given its type
# ---Check that unary resource is avail or created
# ---Check if action has a hold effect on a resource
# ---Allocate action to unary resource: sorting a unary resource list by workload
# ---add the action to the action queue of the unary res with smallest workload
def allocateAction(tmpAct):
	tUnaryList = []
	
	#First verify the unary resources requried have been created or are in the game state
	for tUnaryName in tmpAct.unary_res_list:
		#Verify the unary resource exist
		if(len(sim_unary_state[tUnaryName])<1):
			print "Unary Resource ", tUnaryName , " Has not been created."
			return false
	
	#Now check if action has effect of holding a resource (generally a gather resource action)
	for tEffectKey in tmpAct.effects_dict.keys():
		if(tEffectKey == global_sim.effect_hold):
			resName = tmpAct.effects_dict[tEffectKey]
			print "Holding Resource" ,resName
			for tRes in sim_unary_state[resName]:
				tRes.getWorkLoad()
				tUnaryList.append(tRes)
	
			#Sort the list of unary objects by workload for the specified type of unary resource
			tUnaryList = sorted(tUnaryList, key=attrgetter('workload'), reverse = false)
			#allocate the action to the resource with the smallest workload
			tUnaryList[0].addAction(tmpAct)
			#add resource to held resources dictionary and remove from game state
			held_resources.append(tUnaryList.pop(0))
			#update game state to reflect removal of held resource - resource no longer avail to other actions
			sim_unary_state[resName] = tUnaryList[:]
			#if the action has been assigned to a unary resource then we are done
			return true
			
	#tUnaryList[:] = []		
	#This for-loop handles allocation of actions where the effect HOLD does not apply
	for tUnaryName in tmpAct.unary_res_list:
		#Locate the unary type list in the sim_unary_state
		for tRes in sim_unary_state[tUnaryName]:
			tRes.getWorkLoad()
			tUnaryList.append(tRes)
	
		#Sort the list of unary objects by workload for the specified type of unary resource
		tUnaryList = sorted(tUnaryList, key=attrgetter('workload'), reverse = false)
		#allocate the action to the resource with the smallest workload
		tUnaryList[0].addAction(tmpAct)
		if(len(tUnaryList[0].action_queue) > 0):
			if(tUnaryList[0].action != 0):
				print tUnaryList[0].name, tUnaryList[0].action.name
				for _tAction in tUnaryList[0].action_queue:
					if(_tAction == 0):
						print tUnaryList[0].name, " & Action:", "NO ACTION"
					else:
						print tUnaryList[0].name, " & Action:", _tAction.name
	return true
	
#may need to consider checking for empty action queues of unary objects to avoid errors	
#Runs through each unary resource in the game state and processes their actions.
#DOES NOT tell the unary resource to grab a next action or change the resources action.
#Does process effects of actions when applicable.
#Must process unary resources contained in the dictionaries sim_unary_state and held_resources 
def processUnaryResources():
	#print "processing unary resources"
	#print "size of sim_unary_state ", len(sim_unary_state["Worker"])
	#print "size of held_resource ", len(held_resources)
	
	for tKey in sim_unary_state.keys():
		#print('key', tKey) 
		for tUnary in sim_unary_state[tKey]:
			tFlag = tUnary.update(DELTA_TIME)
			#print "tFlag ", tFlag
			if(tFlag == global_sim.process_effect):
				#print "handeling sim state resource action"
				#print("Sim_State_Effects: Action Completed...Processing Effect Now...")
				#print tUnary.action.name
				for tEffect in tUnary.action.effects_dict.keys():
					#print tUnary.action.name
					processEffect(tEffect,tUnary,tUnary.action.effects_dict[tEffect])
		
	#Since these resources are held they continue to process the same effects throughout the life of the simulation.
	#Note that held resources may be continuing to process actions of finite duration before finaling processing the
	#action responsible for holding them.  This means a worker might have been told to build 4 buildings before being
	#held by a gather resource request.  Those four bldgs will be constructed first before the gather resource action
	#is started.  Once started, the resource will continue to process the holding actions effect repeatedly.
	for tUnary in held_resources:
		#print "held resource action"
		
		if(tUnary.update(DELTA_TIME) == global_sim.process_effect):
			#print("Held_Resources_Effects: Action Completed...Processing Effect Now...")
		#	print tUnary.name, tUnary.action.name
			for tEffect in tUnary.action.effects_dict.keys():
				processEffect(tEffect,tUnary,tUnary.action.effects_dict[tEffect])				
	
#Load definition files of RTS Game being simulated and initialize game state datastructures
try:
	execfile("xmlParser.py")
except SystemExit:
	print("Starting Simulator")



#********Initialize simulator game state************************
#These are copies of the initialization state in order for the MOEA to utilize the same initial state #settings for each solution or plan it evaluates.
sim_unary_state = {}
sim_unary_state = copy.deepcopy(unary_resource_state)
sim_volumetric_state = {}
sim_volumetric_state = copy.deepcopy(volumetric_resource_state)
sim_combatUnit_state = {}
sim_combatUnit_state = copy.deepcopy(combat_unit_state)

#This dictionary keeps track of held resources (i.e. workers assigned actions to gather minerals, gas,etc).
#This occurs when an action is allocated and it specifies in its effect list that it will
#hold onto a resource.  The dictionary properties (key = "resource name being gathered": value = resource unary object)
held_resources = []

#Contains the sequence of actions to be executed or the action plan
action_plan = deque()

#copy actions from dictionary to instantiate plan


#action_plan.append(copy.deepcopy(global_sim.action_definitions['Gather_Mineral']))
#action_plan.append(copy.deepcopy(global_sim.action_definitions['Gather_Mineral']))

action_plan.append(copy.deepcopy(global_sim.action_definitions['Build_Refinery']))
action_plan.append(copy.deepcopy(global_sim.action_definitions['Gather_Mineral']))

action_plan.append(copy.deepcopy(global_sim.action_definitions['Build_Refinery']))
# action_plan.append(copy.deepcopy(global_sim.action_definitions['Gather_Gas']))
# action_plan.append(copy.deepcopy(global_sim.action_definitions['Gather_Gas']))
# action_plan.append(copy.deepcopy(global_sim.action_definitions['Gather_Mineral']))
# action_plan.append(copy.deepcopy(global_sim.action_definitions['Build_SupplyDepot']))


wait_for_action = false
simulation_completed = false

while(len(action_plan) > 0 or wait_for_action == true):  #while still actions to schedule
	#retrieve action from plan
	# if(len(action_plan) <= 0):
		# while(simulation_completed == false):
			# processUnaryResources()
			# checkSimulationCompleted()
			# game_time = game_time + 1 
	
		
	if(wait_for_action == false and len(action_plan) !=0):
		tAction = action_plan.popleft()
		wait_for_action = false
		print "Retrieved Next Action from Build Order Plan: ", tAction.name, tAction.duration
	elif(wait_for_action == false and len(action_plan) ==0):
		break
		
	
	#STEP1 - Check Exist/Tech Ordering Constraint
	if(checkExistConstraint(tAction)):
		print "Passed Exist Constraint: ", true
		
		#STEP2 - Check Cummulative Constraints
		#	   	-- Must be able to handle waiting situation for when vol res not avail yet
		if(checkCummulativeConstraint(tAction)):
			print "Passed Cummulative Constraint: ", true
		
			if(allocateAction(tAction) == true):
				print "Passed Disjunctive Constraint: Action Allocated Successfully"
				
				#Action allocated so deduct from volumetric resource levels
				for volRes in tAction.vol_res_dict.keys():
					sim_volumetric_state[volRes].current_total = sim_volumetric_state[volRes].current_total - tAction.vol_res_dict[volRes]
				
				wait_for_action = false
			else:	
				print "Failed Disjunctive Constraint: unary resource not available or created"
		else:
			print "Failed Cummulative Constraint: ", false
			print "Going to wait until resources become available..."
			wait_for_action = true
	else:
		print "Failed Exist Constraint: ", false
	
	
	processUnaryResources()
	
	game_time = game_time + 1 #in seconds
	
	#STEP2 - Check Cummulative Constraints
	#	   	-- Must be able to handle waiting situation for when vol not avail yet	
	#STEP3 - Schedule action to unary resource
	#STEP4 - Update Unary Resources
	#	   -- Process actions and effects
	#STEP5 - Update Volumetric Resources

print("Broke out")
while(simulation_completed == false):

	processUnaryResources()

	game_time = game_time + 1 #in seconds
	simulation_completed = checkSimulationCompleted()

printGameStateInfo()	
#Receives effect to process on resources.  In general there are two types of effects an action has:
# (1): Unary resource effect: creating a new unary resource
# (2): Volumetric resource effect: gathered more of a specified type of volumetric resource
#def processEffect(effectString):

#Retrieves the next action to attempt to execute from the plan
#def scheduleNxtAction():



#tAct1 = global_sim.action_definitions['Build_Barracks']
# tAct2 = actions.Action('produce_something')
# #iterate through unary dictionary to call update funcition of unary objects stored in lists
#for tKey in global_sim.unary_resource_state.keys():
	#print('key', tKey) #lists are currently empty in the unary state dictionary - no unary objects yet.
#	for tUnary in global_sim.unary_resource_state[tKey]:
#	 print('res name', tUnary.name)
	 # tUnary.addAction(tAct1)
	 # tUnary.addAction(tAct2)
	 #print(tUnary.getWorkLoad())
	 # tUnary.update(delta_time)
	 # print(tUnary.action.name)
	 # tUnary.nextAction()
	 # print(tUnary.action.name)

# for tVol in volumetric_resource_state.keys():

		# print(volumetric_resource_state[tVol].name)
		# print(volumetric_resource_state[tVol].current_total)
		# print(volumetric_resource_state[tVol].accumulation_rate)
		# volumetric_resource_state[tVol].processAccumulatedAmount(2, frames_per_sec)
		# print(volumetric_resource_state[tVol].current_total)
		
		
