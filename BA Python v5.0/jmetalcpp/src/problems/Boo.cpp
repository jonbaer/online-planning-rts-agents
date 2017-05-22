//  Boo.cpp
//
//  Author:
//       Lt Jason Blackford
//	Description: RTS build order optimization problem.

//  Copyright (c) 2011 Antonio J. Nebro, Juan J. Durillo
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Lesser General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.


#include <Boo.h>


/**
 * @class Boo
 * @brief Class representing the problem RTS build order problem
 **/


 /**
   * Constructor.
   * Creates a new instance of the Boo problem.
   * @param numberOfVariables Number of variables of the problem is the number of possible decisions for a given strategy as defined by Weber (i.e. TvZ is 56 + my added decisions for units).
   * @param solutionType The solution type must "Binary".
   */
Boo::Boo(string solutionType, int numberOfVariables, int decisionBitLength) {
  numberOfVariables_   = numberOfVariables;
  decisionBitLength_ = decisionBitLength;
  numberOfObjectives_  = 3;
  numberOfConstraints_ = 0;
  problemName_         = "Boo";

   cout<<"Initializing Python Interpreter"<<endl;
    Py_Initialize();
   cout<<"Python ready"<<endl;

///"sys.path.append('/usr/share/RTS_Simulator')\n"
    PyRun_SimpleString("import sys\n" "sys.path.append('/home/jason/Desktop/BA_Simulator')\n"
	"print sys.path\n"); //"import sim_main\n");
    if((pName = PyString_FromString("run_sim")) == NULL)
	cout<<"Error pName"<<endl;

   if((pModule = PyImport_Import(pName)) == NULL) 
	cout<<"Error pModule"<<endl;
    
   if((pFunc = PyObject_GetAttrString(pModule,"run")) == NULL)
    	cout<<"Error PFunc"<<endl;
    
    
    
  lowerLimit_ = new double[decisionBitLength_];
  if (lowerLimit_ == NULL) {
    cout << "Impossible to reserve memory for storing the variable lower limits" << endl;
    exit(-1);
  }

  upperLimit_ = new double[decisionBitLength_];
  if (upperLimit_ == NULL) {
    cout << "Impossible to reserve memory for storing the variable lower limits" << endl;
    exit(-1);
  }

  //Limits relate to the labels of the actions. A rand generator will assign actions randomly to an int array
  for (int i = 0; i < decisionBitLength_; i++) {
    lowerLimit_[i] =  0;
    upperLimit_[i] =  9; //Number of actions
  }

  if (solutionType.compare("ArrayIntAndBinary") == 0)
    solutionType_ = new ArrayIntAndBinarySolutionType(this,decisionBitLength_,decisionBitLength_);
  else {
    cout << "Error: solution type " << solutionType << " invalid" << endl;
    exit(-1) ;
  }
	
} // Kursawe


/**
 * Destructor
 */
Boo::~Boo() {
  delete [] lowerLimit_ ;
  delete [] upperLimit_ ;
  delete solutionType_ ;
} // ~Kursawe


/**
 * Evaluates a solution
 * @param solution The solution to evaluate
 */
void Boo::evaluate(Solution *solution) {
	//Boo::fs.open("sim_data.txt", std::fstream::out | std::fstream::app); 

  pArgs = PyTuple_New(Boo::decisionBitLength_*2);
	

  //cout<<"Size of tuple: "<<PyTuple_Size(pArgs)<<endl;
  Variable** variable = solution->getDecisionVariables();
  ArrayInt* var0 = (ArrayInt*)variable[0];
  Binary* var1 = (Binary*)variable[1];

 for(int i = 0; i<Boo::decisionBitLength_; i++)
 {
	//cout<<var0->getValueInt(i);
	pValue = PyInt_FromLong(var0->getValueInt(i));
	
	if(PyTuple_SetItem(pArgs, i, pValue) != 0)
	{
		cout<<"Error: Setting pArgs from ArrayInt failed"<<endl;
	}
	else
	{
		//cout<<"Tuple ArrayInt item: "<< PyTuple_GetItem(pArgs,i)<<endl;
	}
 }

 //cout << endl;

 for(int i = 0; i<Boo::decisionBitLength_; i++)
 {
	
	if(var1->getIth(i) == false)
        {	   
	   
	    pValue = PyInt_FromLong(0);
        }
	else
	{
  	   
	    pValue = PyInt_FromLong(1);
	}
	
	
	if(PyTuple_SetItem(pArgs,Boo::decisionBitLength_ + i, pValue) != 0)
	{
		cout<<"Error: Setting pArgs from Binary failed"<<endl;
	}
	else
	{
		//cout<<"Tuple Binary item: "<< PyTuple_GetItem(pArgs,i)<<endl;
	}
 }

fs << endl;
for(int i = 0; i<Boo::decisionBitLength_*2; i++)
 {
     //cout<<"pArgs: "<< PyInt_AsLong(PyTuple_GetItem(pArgs,i))<<endl;
	//fs<< PyInt_AsLong(PyTuple_GetItem(pArgs,i));
 }
/*cout<<"Before execution: "<<endl;
	for(int i=0; i<Boo::decisionBitLength_;i++)
	{
		cout<<var1->getIth(i);
	}

	cout<<endl;
*/	
if((pValue = PyObject_CallFunctionObjArgs(pFunc, pArgs,NULL))==NULL)
   {		
	//cout<<"Error: Couldn't Run Simulator"<<endl;
	//fs<<"Error: Couldn't Run Simulator"<<endl;
	solution->setObjective(0,0);
  	solution->setObjective(1,0);
  	solution->setObjective(2,0);
   }	
 else
   {
	//cout<<"Ran Simulator"<<endl;
	//fs<<"Ran Simulator"<<endl;
	PyObject* temp = PyList_GetItem(pValue,0);
	solution->setObjective(0,PyInt_AsLong(temp));
	//cout<<"List items: "<<PyInt_AsLong(temp)<<endl;
	//fs<<"List items: "<<PyInt_AsLong(temp)<<endl;
	temp = PyList_GetItem(pValue,1);
  	solution->setObjective(1,PyInt_AsLong(temp));
	//cout<<"List items: "<<PyInt_AsLong(temp)<<endl;
	//fs<<"List items: "<<PyInt_AsLong(temp)<<endl;
	temp = PyList_GetItem(pValue,2);
  	solution->setObjective(2,PyInt_AsLong(temp));
	//cout<<"List items: "<<PyInt_AsLong(temp)<<endl;
	//fs<<"List items: "<<PyInt_AsLong(temp)<<endl;
	int size = PyList_Size(pValue);
	for(int i =3; i< size; i++)
	{
		temp = PyList_GetItem(pValue,i);
		int pos = PyInt_AsLong(temp);
				
		// cout<<"bit pos: " <<pos<<endl;
		//cout<<" Original value: "<<var1->getIth(pos);
		 var1->setIth(pos,false);
		//cout<<" Flipped value: "<<var1->getIth(pos)<<endl;
		
	}
	
   }



  //Boo::fs.close();

  //Py_DECREF(pArgs);
  //Py_DECREF(pValue);
 
  // delete [] fx;
  // delete [] x;
  // delete vars;

} // evaluate

