#Author: Lt Jason M. Blackford 
#University: AFIT
#Date: 10/10/2013
#Class Description: Defines a volumetric/consumable resource object or raw material.  For example Gold, Wood, Food, Gas, Minerals from RTS games like AOE or Starcraft.
#Only one of each type of volumetric resource should be instantiated by the simulator.  

#Functions for Volumetric Class Instances Include:
#	--processAccumulatedAmount(): Passes in the number of workers currently gathering the resource and the number of frames that have elapsed.
#								  These values are used with the accumulation_rate to determine how much the workers have gathered of the resource given the elapsed frame count.

class Volumetric:

	 def __init__(self,name, rate, initAmt):
	 
		#Name of the volumetric resource (gold, gas, mineral, etc)
		self.name = name
				
		#Resource_Amount per worker per frame
		#If rate = -1 then this means the resource is not a collected resource (i.e. supply in starcraft)
		self.accumulation_rate = rate
		
		#Total amount of the resource currently available
		self.current_total = initAmt
	
	 def processAccumulatedAmount(self, frameCount):
		
		#handles resources that don't have an associated accumulation rate (i.e supply in starcraft)
		if(self.accumulation_rate < 0):
			#(i.e. supply in starcraft has rate = -10 set in the xml file.  The negative sign
			#signifies that it is not a rate but a discrete amount that should be added to the total.
			self.current_total = self.current_total + (-1 * self.accumulation_rate)
			return
			
		#update supply amount for the given number of elapsed frames - 1 corresponds to 1 worker
		self.current_total = self.current_total + (self.accumulation_rate * 1 * frameCount)