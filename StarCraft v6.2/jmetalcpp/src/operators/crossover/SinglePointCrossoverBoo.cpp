//  SinglePointCrossoverBoo.cpp
//
//  Author:
//       Antonio J. Nebro <antonio@lcc.uma.es>
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


#include <SinglePointCrossoverBoo.h>


/**
 * @class SinglePointCrossoverBoo
 * @brief This class is aimed at representing a SinglePointCrossoverBoo operator
 **/


/**
 * Constructor
 * Create a new SBX crossover operator whit a default
 * index given by <code>DEFAULT_INDEX_CROSSOVER</code>
 */
SinglePointCrossoverBoo::SinglePointCrossoverBoo(map<string, void *> parameters)
: Crossover(parameters) {
  crossoverProbability_ = 0.0 ;
  //TODO: crossoverProbability_ = NULL;
  if (parameters["probability"] != NULL)
    crossoverProbability_ = *(double *)parameters["probability"];
} // SinglePointCrossoverBoo


/**
 * Perform the crossover operation.
 * @param probability Crossover probability
 * @param parent1 The first parent
 * @param parent2 The second parent
 * @return An array containing the two offsprings
 **/
Solution ** SinglePointCrossoverBoo::doCrossover(double probability, Solution *parent1, Solution *parent2) {
//cout << "1Inside singlepointBoo crossover" <<  endl;
  Solution** offSpring = new Solution*[2];
//cout << "2Inside singlepointBoo crossover" <<  endl;
  if (offSpring == NULL) {
  //  cout << "Error grave: Impossible reserve memory for allocating new solutions when performing SinglePointCrossoverBoo " << endl;
    exit(-1);
  }
	//cout << "Parent 1 Inside singlepointBoo crossover" <<  endl;
  offSpring[0] = new Solution(parent1);
   //cout << "Parent 2 Inside singlepointBoo crossover" <<  endl;
  offSpring[1] = new Solution(parent2);
 
  // cout << "crossover point" <<  endl;
		  int crossoverPoint = PseudoRandom::randInt(0, parent1->getProblem()->getNumberOfVariables() - 1);
          int valueX1;
          int valueX2;
		 //  cout << "entering for-loop" <<  endl;
          for (int i = crossoverPoint; i < parent1->getProblem()->getNumberOfVariables(); i++) 
		  {
			//cout << "Inside singlepointBoo crossover" << i << endl;
        	 //For these 4 lines to work I had to add getValue1(int i) and setValue(int index, int value)
        	 //to the Variable.java file.
			// cout << "--Getting Parent 1" << endl;
        	valueX1 = ((ArrayInt*)(parent1->getDecisionVariables()[0]))->getValueInt(i);
			//cout << "--Getting Parent 2" << endl;
            valueX2 = ((ArrayInt*)(parent2->getDecisionVariables()[0]))->getValueInt(i);
			//cout << "--Setting Offspring 1" << endl;
            ((ArrayInt*)(offSpring[0]->getDecisionVariables()[0]))->setValue(i,valueX2);
			//cout << "--setting Offspring 2" << endl;
            ((ArrayInt*)(offSpring[1]->getDecisionVariables()[0]))->setValue(i,valueX1);
           // valueX1 = (int) parent1.getDecisionVariables()[i].getValue();
           // valueX2 = (int) parent2.getDecisionVariables()[i].getValue();
           // offSpring[0].getDecisionVariables()[i].setValue(valueX2);
         //   offSpring[1].getDecisionVariables()[i].setValue(valueX1);

          } // for

  // if (PseudoRandom::randDouble() < probability) {
		// //1. Compute the total number of bits
		// int totalNumberOfBits = 0;
		// for (int i = 0; i < parent1->getProblem()->getNumberOfVariables(); i++) {
		  // totalNumberOfBits +=
			  // ((Binary *)(parent1->getDecisionVariables()[0]))->getNumberOfBits() ;
		// }

		// //2. Calculate the point to make the crossover
		// int crossoverPoint = PseudoRandom::randInt(0, totalNumberOfBits - 1);

		// //3. Compute the variable containing the crossoverPoint bit
		// int variable = 0;
		// int acountBits =
			// ((Binary *)(parent1->getDecisionVariables()[0]))->getNumberOfBits() ;

		// while (acountBits < (crossoverPoint + 1)) {
		  // variable++;
		  // acountBits +=
			  // ((Binary *)(parent1->getDecisionVariables()[0]))->getNumberOfBits() ;
		// }

		// //4. Compute the bit into the variable selected
		// int diff = acountBits - crossoverPoint;
		// int intoVariableCrossoverPoint =
			// ((Binary *)(parent1->getDecisionVariables()[0]))->getNumberOfBits() - diff;


		// //5. Make the crossover into the the gene;
		// Variable* offSpring1, * offSpring2;
		// Binary * of1, *of2 ;
		// offSpring1 =
			// ((parent1->getDecisionVariables()[0]))->deepCopy();

		// offSpring2 =
			// ((parent2->getDecisionVariables()[0]))->deepCopy();
		// of1 = (Binary *)offSpring1 ;
		// of2 = (Binary *)offSpring2 ;

		// for (int i = intoVariableCrossoverPoint;
			// i < of1->getNumberOfBits();
			// i++) {
		  // bool swap = of1->getIth(i) ;
		  // of1->setIth(i, of2->getIth(i)) ;
		  // of2->setIth(i, swap) ;
		// }

		// delete offSpring[0]->getDecisionVariables()[0];
		// delete offSpring[1]->getDecisionVariables()[0];
		// offSpring[0]->getDecisionVariables()[0] = of1 ;
		// offSpring[1]->getDecisionVariables()[0] = of2 ;

		// //6. Apply the crossover to the other variables
		// //for (int i = 0; i < variable; i++) {

		  // delete offSpring[0]->getDecisionVariables()[0];
		  // offSpring[0]->getDecisionVariables()[0] =
			  // parent2->getDecisionVariables()[0]->deepCopy();

		  // delete offSpring[1]->getDecisionVariables()[0];
		  // offSpring[1]->getDecisionVariables()[0] =
			  // parent1->getDecisionVariables()[0]->deepCopy();

		// //}
	
	
	
  return offSpring;
} // doCrossover


/**
 * Executes the operation
 * @param object An object containing an array of two parents
 * @return An object containing the offSprings
 */
void * SinglePointCrossoverBoo::execute(void *object) {
  Solution ** parents = (Solution **) object;
  // TODO: Comprobar la longitud de parents
  // TODO: Chequear el tipo de parents

  Solution ** offSpring = (Solution **)doCrossover(crossoverProbability_, parents[0], parents[1]);

  return offSpring;
} // execute
