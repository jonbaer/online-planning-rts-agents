#Author: Lt Jason Blackford
#University: AFIT

#Combat units are generally assigned actions by a tactical planner, however,
#the strategic planner is responsible for producing an army. Therefore
#combat units are represented by a single class with a name attribute and quantity attribute.
#A combat unit instance is defined for each type of combat unit not for each unit created (i.e. CombatUnit Marine defines
#an instance for combat units that are of type marine)  Combat units are not treated as separate objects since
#this simulator does not assign actions to units.  A tactical planner may look at combat units as a unary resource, but
#that is not the case for strategic planning.

class CombatUnit:

	def __init__(self,name,exist = None,minCost=None,gasCost=None,suppCost=None, durAmt=None):
		#means creating a goal instance of the unary object
		if(minCost != None): 
			self.name = name
			self.total_amt = exist
			self.minCostEa = minCost
			self.gasCostEa = gasCost
			self.suppCostEa = suppCost
			self.durAmtEa = durAmt
		else:
			self.name = name
			self.total_amt = exist
		
		
	
	def __addUnit__(amtToAdd):
		self.total_amt = self.total_amt + amtToAdd
