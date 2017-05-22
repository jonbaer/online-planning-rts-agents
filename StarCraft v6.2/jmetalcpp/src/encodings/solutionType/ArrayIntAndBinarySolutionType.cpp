//  ArrayIntAndBinarySolutionType.cpp
//
//  Author:
//       Esteban López <esteban@lcc.uma.es>
//
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


#include <ArrayIntAndBinarySolutionType.h>
#include <cstddef>


/**
 * Constructor
 * @param problem
 */
// ArrayIntAndBinarySolutionType::ArrayIntAndBinarySolutionType(Problem * problem)
// : SolutionType(problem) { }


ArrayIntAndBinarySolutionType::ArrayIntAndBinarySolutionType(Problem *problem, int intVariables,int binaryStringLength):SolutionType(problem)
{
	binaryStringLength_ = binaryStringLength;
	numberOfIntVariables_ = binaryStringLength;
	
	
}
											  
/**
 * Creates the variables of the solution
 * @param decisionVariables
 */
Variable ** ArrayIntAndBinarySolutionType::createVariables() {
  int i;

  Variable **variables = new Variable*[2]; //malloc(sizeof(Real) * problem->getNumberOfVariables());
  if (problem_->getSolutionType() ==  NULL) {
    cout << "Error grave: Impossible to reserve memory for variable type" << endl;
    exit(-1);
  }
   
   variables[0] = new ArrayInt(binaryStringLength_, problem_);
   variables[1] = new Binary(binaryStringLength_);

  return variables;
} // createVariables

int ArrayIntAndBinarySolutionType::getSize(){
		return problem_->getNumberOfVariables();//numberOfIntVariables_;
	}


/**
 * Copy the variables
 * @param decisionVariables
 * @return An array of variables
 */
Variable ** ArrayIntAndBinarySolutionType::copyVariables(Variable ** vars) {
  cout <<"1ArrayIntAndBinary::copyVariables"<<endl;
  Variable **variables = new Variable*[2];
  cout <<"2ArrayIntAndBinary::copyVariables"<<endl;
  variables[0] = vars[0]->deepCopy();
  variables[1] = vars[1]->deepCopy();
  return variables ;
} // copyVariables
