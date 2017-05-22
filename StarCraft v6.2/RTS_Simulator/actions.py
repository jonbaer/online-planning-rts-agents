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
	   
	   #Reference dictionary of all the volumetric resources and their respective amounts the action requires (i.e 'gold':100)
	   self.vol_res_dict = copy.deepcopy(volumetricResourceDictionary)
	   
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
	   
	  
	  
#************Python Code for Parsing the XML file to instantiate actions*******************************	   
# command_tree = ET.parse('command.xml')	
# cmd_root = command_tree.getroot()

# for action in cmd_root:

	# tVolResDict = {}
	# tUnaryResList = []
	# tUnaryExistList = []
	# tEffectsList = []

	# tName = action.find('name').text
	# tDuration = float(action.find('duration').text)
	
	# #build vol dictionary
	# vol = action.find('volumetric_dictionary')
	# for attr in vol:
		# tKey = attr.get('key')
		# tValue = float(attr.get('value'))
		# print(tKey,tValue)
		# tVolResDict.update({tKey:tValue})
	
	# #build unary list
	# unary = action.find('unary_list')
	# for attr in unary:
		# tUnaryResList.append(attr.text)
		
		
	# #build exist list
	# exist = action.find('exist_list')
	# for attr in exist:
		# tUnaryExistList.append(attr.text)
	
	# #build effects list
	# effect = action.find('effect_list')
	# for attr in effect:
		# tEffectsList.append(attr.text)
	
	# #create new action from xml file and add to action definitions
	# tAction = actions.Action(tName,tDuration, tVolResDict, tUnaryResList, tUnaryExistList, tEffectsList)	
	# action_definitions.update({tName:tAction})
	# tVolResDict.clear()
	# tUnaryResList[:] = []
	# tUnaryExistList[:] = []
	# tEffectsList[:] = []
	
	# print(tAction.name, tAction.duration, tAction.vol_res_dict, tAction.unary_res_list, tAction.exist_list, tAction.effects_list)
	# print(tAction.duration + 20)