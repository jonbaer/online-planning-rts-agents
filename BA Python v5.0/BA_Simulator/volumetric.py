#Author: Lt Jason M. Blackford 
#University: AFIT
#Date: 10/10/2013
#Class Description: Defines a volumetric/consumable resource object or raw material.  For example Gold, Wood, Food, Gas, Minerals from RTS games like AOE or Starcraft.
#Only one of each type of volumetric resource should be instantiated by the simulator.  

#Functions for Volumetric Class Instances Include:
#	--processAccumulatedAmount(): Passes in the number of workers currently gathering the resource and the number of frames that have elapsed.
#								  These values are used with the accumulation_rate to determine how much the workers have gathered of the resource given the elapsed frame count.

class Volumetric:

	 def __init__(self,name=None, rate=None,initRate=None, initAmt=None, capacity=None):
	 
		if(capacity == None): #then this is a goal instance
			self.name = name
			self.current_total = initAmt
			self.total_rate = initRate	
		else:
			#Name of the volumetric resource (gold, gas, mineral, etc)
			self.name = name
						
			#The cummulative rate given the total number of collectors times accumulation_rate.
			self.collection_rate = initRate
			self.production_rate = 0		

			#Total amount of the resource currently available
			self.quantity = initAmt
		
			#Storage capacity - The maximum amount of the material the player can hold
			self.capacity = capacity
			self.ratio = 0
	
