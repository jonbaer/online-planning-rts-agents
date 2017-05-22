Author: Capt Jason M. Blackford
Institute: AFIT
Date: 02 March 2014
Email: blackford.jay@gmail.com - don't hesitate to write with questions

Running Agent BOO_BA_v8.1C++ In Spring
-When in doubt about where to place the AI, code, and other folders just check the makefiles and source code for where dependencies are being grabbed from
--This will require some leg work, hopefully in the near-future I provide a user-manual over a ReadMe text file.
-The original setup I had placed BA_cpp (BA simulator c++ libraries) on my Desktop: (Linux) /home/jason/Desktop
-The jay folder is agent BOO.  This should be placed in the spring/AI/Skirmish/ folder.
- Be sure to assign Agent BOO goals utilizing the goal_table.xml file located under jay/BA_Simulator.  This file stores the cases
for a single strategy for the Case-Base Reasoning mechanism agent BOO utilizes to retrieve goals to execute.
- Be sure to set the exist values inside "unary_resources.xml" and "combat_unit.xml" to zero before each run of agent BOO.
These files store the game state information used by the planning tool to determine the Build-Order for BOO to execute.
Be sure not to set the "armcom" or commander attribute in "Unary_resources.xml" to zero, this is always 1 since the 
commander always exist unless it gets destroyed.


Starcraft Strategic Planning Tool (offline Implementation Only)
This is written in python.
SETTING A GOAL TO PLAN FOR
A goal is provided to the planning tool by filling in values for "unary_goal.xml", "unit_goal.xml", and "vol_goal.xml".
SETTING THE INITIAL STATE FOR THE PLANNER TO START PLANNING FROM
Be sure to set the initial state of the planner using "unary_resources.xml", "combat_unit.xml", and "vol_resource.xml" 
RUNNING THE PLANNER
Is run from the script run_sim.py using the Python Interpreter. Command looks like:
python run_sim.py
Just be sure to be in the directory of the run_sim.py script otherwise Python won't find it to run.
RETRIEVING THE OUTPUT
The best solutions returned by NSGAII are outputted to the VAR file located inside the RTS_Simulator file.


BA Python v5.0
This is the Python verision of the C++ implementation.  Not sure how up-to-date it is in terms of the functionality of Agent BOO,
so I don't recommend using this for online planning especially sinces its about 85% slower than the C++ verision.
However, it is great for offline planning and might be easier to work with than the C++ verision.  
It is utilized the same way as the Starcraft Strategic Planning Tool.


