from collections import deque

#f= open("sim_log.txt","w")
#contains string passed from jmetallcpp 
action_plan_string =()
#Contains the sequence of actions to be executed or the action plan
action_plan = deque()
#used to repair infeasible actions to generate a feasible action plan
binary_dec_bits = []

game_time =0

#Contains global values utilized by the RTS simulator modules
fail = -3
#These are dictionaries that store definitions of actions, resources, effects, and combat unit types; Used for reference or copying, should never be modified.
#These dictionaries should be initialized either manually in python or by utilizing an XML parser.
action_definitions = {}
effect_definitions = {}
unary_definitions ={}
volumetric_definitions = {}
combatUnit_definitions = {}
#tracks actions that hold workers or a unary resource forever in order to collect gold, wood, minerals, etc
gathering_actions = {}

#These are dictionaries that store the state of the game with respect to player resources;  Modified throughout the execution of the action plan.
unary_resource_state = {}         #This dict contains a list struct for each type of unary resource (lists allow for dynamically adding resouces as they are created during play
volumetric_resource_state = {}    #This dict contains only unique key:value pairs for each type of volumetric resource (i.e metal, food, gas, gold, wood, etc)
combat_unit_state = {}			#This stores combat units created during simulation	

#These are dictionaries that store the goal state to be reached
volumetric_goal_state = {}
unary_goal_state = {}
unit_goals = {}

#Objective values dictionary - stores the fitness of the action plan executed by the simulator (fitness is captured by 3 objectives) -- (key=="one":value==numeric score) Only three entries in the dictionary corresponding to the three objectives.
fitness_values = [1,5,3]


#Flag used by unary resources to tell main.py (simulation manager) whether or not an action
#is completed or if execution is still continuing.
continue_execution = 'continue'
no_actions_left = 'no_actions_left'
process_effect = 'effect'

#Describe the effects actions can have on the game state
#than 0.  In addition, they assign the workload of the worker to a very large number.
#Actions are flagged with this via their effects_list in command.xml
effect_hold = "Hold"			  #On unary or volumetric resources
effect_increment = "Increment"	  #Strictly on unary resources
effect_decrement = "Decrement"	  #Strictly on unary resources	
effect_accumulate = "Accumulate"  #Strictly on volumetric resources
effect_accum_fixed = "Accumulate_Fixed" #Strictly for volumetric resources that are not rates, not held and are fixed (i.e supply in starcraft)
effect_nop = "NOP"				  #Reserved for null actions
effect_UnitIncrement = "Unit_Increment"

