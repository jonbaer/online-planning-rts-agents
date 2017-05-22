import global_sim
import unary
import volumetric
import actions
import effects

#This is used to run the simulator from jMetal inside Boo.cpp.  The evaluation function of Boo.cpp will
#call this function and pass in the action string defined by the MOEA.  The sim_main.py class will decode the
#received action string into actions to be taken.  It decodes action_string from global_sim.

try:
	import os
	import sys
	os.chdir('/home/jason/Desktop/BA_Simulator')
	execfile("xmlParser.py")
except SystemExit:
	pass


def run(actionPlan=()):

	#global_sim.action_plan_string = actionPlan
	#global_sim.game_time = 0;  #seconds
	#global_sim.binary_dec_bits[:]=()
	#global_sim.fitness_values[:] = ()
	#global_sim.fitness_values = [100000,100000,100000]
	
	import sim_main
	global_sim.action_plan_string = actionPlan
	global_sim.game_time = 0;  #seconds
	global_sim.binary_dec_bits[:]=()
	global_sim.fitness_values[:] = ()
	global_sim.fitness_values = [100000,100000,100000]
	reload(sim_main)

	for db in global_sim.binary_dec_bits:
		global_sim.fitness_values.append(db)

#	for fv in global_sim.fitness_values:
#		global_sim.f.write("%s " %fv)
	
#	global_sim.f.write("\n")
#	global_sim.f.close()

#	print global_sim.fitness_values
	return global_sim.fitness_values


####USED FOR TESTING RTS SIM OUTSIDE OF USING JMETALCPP

#[8,2,4,4,1,1,1,1]
#[0,1,5,1,2,5,4,8,1,8,8,6,2,5,7,0,6,5,2,0,8,0,8,3,2,9,3,6,0,7, 			0,0,0,1,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,1]
LINUX_test_plan =[2,8,2,4,6,4,9,2,6,0,6,9,6,5,9,8,8,8,7,9,7,6,0,6,3,7,8,4,2,8,0,5,2,8,9,9,1,5,8,3,1,7,5,4,6,0,8,3,8,1,6,6,4,3,9,2,4,4,6,2, 0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,1,0,1,1,0,1,0,1,1,0,0,0,0,0,1,1,1,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,1,1,0,0,1,0,0,0,1,0,]
#[4,5,5,0,0,2,6,5,5,0,4,4,4,1,2,7,1,2,0,7,1,1,7,9,2,8,0,5,7,2,8,9,1,1,9,9,8,7,5,5,4,5,3,5,2,6,1,3,9,6,1,8,3,3,6,8,4,0,0,4,8,0,9,5,8,1,8,8,6,6,8,3,3,5,3,7,3,0,5,0,6,5,6,8,0,8,1,6,0,8,0,8,9,9,6,1,9,9,9,8, 0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,1,0,0,0,0,1]

global_sim.f= open("sim_log.txt","a")
run(LINUX_test_plan)

#WINDOWS_test_plan = #[1,1,1,1,3,5,4,3,0,3,0,1,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1][3,1,3,0,0,0]#[1,1,1,5,4,7,5,0,4,0,3,3,3,3,3,1,1,1,1,1,0,0,1,0,1,1,1,1,1,1]
#global_sim.f= open("sim_log.txt","a")
#run(WINDOWS_test_plan)


#planCounter = 6
#test_plan1 = [1,2,3,4,5,0,1,1,0,1]
#test_plan2 = [6,7,7,7,7,1,1,1,1,1]
#test_plan3 = [3,2,3,2,5,1,1,1,1,1]
#test_plan4 = [1,2,3,3,5,0,1,1,0,1]
#test_plan5 = [1,2,3,4,4,0,0,0,0,0]
#test_plan6 = [0,1,2,3,4,5,6,7,1,1,1,1,1,1,1,1]
#while(planCounter > 0):
	
#	if(planCounter ==1):
#		global_sim.f= open("sim_log.txt","a")
#		run(test_plan1)
#	elif(planCounter ==2):
#		global_sim.f= open("sim_log.txt","a")
#		run(test_plan2)
#	elif(planCounter ==3):
#		global_sim.f= open("sim_log.txt","a")
#		run(test_plan3)
#	elif(planCounter ==4):
#		global_sim.f= open("sim_log.txt","a")
#		run(test_plan4)
#	elif(planCounter ==5):
#		global_sim.f= open("sim_log.txt","a")
#		run(test_plan5)
#	elif(planCounter ==6):
#		global_sim.f= open("sim_log.txt","a")
#		run(test_plan1)
#	planCounter = planCounter -1
#	planCounter = planCounter -1


