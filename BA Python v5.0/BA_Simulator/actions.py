import copy

#Functions for Action Class Instances Include:
#	--NONE--

class Action:
	#base class for unary resources
		
	def __init__(self, command, duration, volumetricResourceDictionary, unaryResourceList, unaryExistList, effectsDict):
	   
	   #Name of action
	   self.name = command
	   
	   #Time required to complete action
	   self.duration = duration
	   
	   #Optimal consumption rates; 
	   self.optM_cr = 0
	   self.optE_cr = 0
	  
	   #Actual consumption rates
	   self.actM_cr = 0
	   self.actE_cr = 0
	
	   #Assigned Unary resource
	   self.unary_ptr = 0
	   #Reference dictionary of all the volumetric resources and their respective amounts the action requires (i.e 'gold':100)
	   self.vol_cost_dict = copy.deepcopy(volumetricResourceDictionary)
	   
	   #List of the unary resources the action requires to be executed (unary resource that executes the action) (i.e. The action 'build marine' is executed by unary resource 'barracks')
	   self.unary_res_list = unaryResourceList[:]
	   
	   #List of the unary resources that the action requires to exist to complete its action (i.e. a worker in AOE requires a mining bldg in order to drop off the gold it mines).
	   #Or in Starcraft before an academy can be built a barracks must exist (this is the 3rd constraint of RTS games (other two are cummulative and disjunctive) - the ordering or existence constraint).
	   #The major difference between this list and the unary_res_list is that the action is not added to the action queue of unary resources included in the exist list or the
	   #action is not executed by the unary resource contained in the exist list.
	   self.exist_list = unaryExistList[:]
	   
	   #What is the effect of the action on the game state? This effects dictionary contains the type and impact of effects.
	   #Currently there are two types of effects an action can have (1) hold or (2) contribute.  These types are keys 
	   #for the dictionary.  The values associated with the keys are the names of a resource defined in either
	   #the unary or volumetric resource xml files.  The type states how the action effects the resource.
	   #hold worker, contribute worker, etc.
	   self.effects_dict = copy.deepcopy(effectsDict)
	   

