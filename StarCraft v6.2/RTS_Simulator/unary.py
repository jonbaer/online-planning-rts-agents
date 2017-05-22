import global_sim
import actions
from collections import deque

#Functions for Unary Class Instances Include:
#	--update():  update action processing time
#	--addAction(): adds an action object to the queue of the unary instance
#	--nextAction(): select next action in action queue to execute
#	--getWorkload(): sets attr:workload and returns the summation of the duration for the set of actions queued on this 	resource

class Unary:
	#base class for unary resources
	null_action = actions.Action('null',0,'null','null','null',{"NOP":"NONE"})
	

	def __init__(self,name,exist = None,minCost=None,gasCost=None,suppCost=None,durAmt = None):
		 #means creating a goal instance of the unary object
		if(exist != None):
		
			self.name = name
			self.total_amt = exist
			self.minCostEa = minCost
			self.gasCostEa = gasCost
			self.suppCostEa = suppCost
			self.durAmtEa = durAmt;
		
		else: #creating a standard unary object 
			self.name = name
		
			#summation of all action durations in the action queue of this resource
			self.time_in_use = 0.0
		
			#time remaining on the action currently being executed by the resource
			self.time_till_completion = 0.0
		
			#action queue (list) of the unary resource
			self.action_queue = deque()
		
			#action being executed
			self.action = 0 #actions.Action('null','null','null','null','null','null')
		
			#workload in seconds
			self.workload = 0.0
		
	
		
	def update(self, deltaTime):
		#retrieve an action from the queue if it is not empty and an action isn't already being processed
		if(self.action == 0 ):
			#print("true")
			if(self.nextAction() == global_sim.no_actions_left):
				self.action = 0;
		
			return global_sim.continue_execution
		
		#game time has passed, so update the execution time of the action being processed
		self.time_till_completion = self.time_till_completion - deltaTime
		self.action.duration = self.action.duration - deltaTime
		#print "Inside update: action duration is: ", self.action.duration

		if(self.action!=0 and self.time_till_completion <= 0.0):
			return global_sim.process_effect
		else:
			return global_sim.continue_execution
	
	#used by simulation manager to tell the unary resource to begin executing the next action 
	def nextAction(self):
		#print("grabbing next action")
		if(len(self.action_queue) == 0):
			self.action = 0
			return global_sim.no_actions_left
		
		if(len(self.action_queue) != 0):
			self.action = self.action_queue.popleft()
			self.time_till_completion = self.action.duration
			return global_sim.continue_execution
			
					
	def addAction(self, action):
		#adds an action to the right side of the deque
		self.action_queue.append(action)
		
	def getWorkLoad(self):
		self.workload = 0
		for _tAction in self.action_queue:
			#print _tAction.name, _tAction.duration
			self.workload = self.workload + _tAction.duration
		
		if(self.action != 0):
			self.workload = self.workload + self.action.duration
			
		return self.workload
	
	
	
	
	
	
	
	
	
#****************Test Cards for Unary Class************************************************

#Instructions: These test cards should be run inside main.py to verify functionality of Unary functions

#This test card verifies that nextAction() operates correctly.  
# Result: should print out unary resource name, workload time, first action in the queue, the next action in the queue => build_something followed by produce_something
#tAct1 = actions.Action('build_something')
#tAct2 = actions.Action('produce_something')
#iterate through unary dictionary to call update funcition of unary objects stored in lists
# for tKey in unary_resource_state.keys():
	
	 # for tUnary in unary_resource_state[tKey]:
		 # print(tUnary.name)
		 # tUnary.addAction(tAct1)
		 # tUnary.addAction(tAct2)
		 # print(tUnary.getWorkLoad())
		 # tUnary.update(delta_time)
		 # print(tUnary.action.name)
		 # tUnary.nextAction()
		 # print(tUnary.action.name)

# #This test card verifies that getWorkLoad() returns the correct summation
# # 40
# tAct1 = actions.Action('build_something')
# tAct2 = actions.Action('produce_something')
# #iterate through unary dictionary to call update funcition of unary objects stored in lists
# for tKey in unary_resource_state.keys():
	
	 # for tUnary in unary_resource_state[tKey]:
		 # print(tUnary.name)
		 # tUnary.addAction(tAct1)
		 # tUnary.addAction(tAct2)
		 # print(tUnary.getWorkLoad())

# #This test card verifies that update() functions; an action can be assigned to the unary action queue using the update() and retrieved from the queue
# #it also ensures that deltaTime is passed and handled correctly by the update()
# #Result should be Unary Name, Initial Action Name == 0, added action name (tAction.name = build_something, -1
# tAction = actions.Action('build_something')
# #iterate through unary dictionary to call update funcition of unary objects stored in lists
# for tKey in unary_resource_state.keys():
	
	# for tUnary in unary_resource_state[tKey]:
		# print(tUnary.name)
		# tUnary.addAction(tAction)
		# print(tUnary.action)
		# tUnary.update(delta_time)
		# print(tUnary.action.name)
		# print(tUnary.time_till_completion)
		

		
# #This test card verifies addAction(); that an action can be assigned to the unary action queue and retrieved from the queue
# #Result should be Unary Name, Initial Action Name == 0, added action name (tAction.name = build_something
# tAction = actions.Action('build_something')
# #iterate through unary dictionary to call update funcition of unary objects stored in lists
# for tKey in unary_resource_state.keys():
	# for tUnary in unary_resource_state[tKey]:
		# print(tUnary.name)
		# tUnary.addAction(tAction)
		# print(tUnary.action)
		# tUnary.nextAction()
		# print(tUnary.action.name)
		# #tUnary.update(delta_time)
