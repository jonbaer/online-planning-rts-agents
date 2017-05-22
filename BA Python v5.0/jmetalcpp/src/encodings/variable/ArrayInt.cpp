//  ArrayInt.cpp
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


#include <ArrayInt.h>


/**
 * Constructor
 */
ArrayInt::ArrayInt() {
  problem_ = NULL;
  size_   = 0;
  array_ = NULL;
} // Constructor


/**
 * Constructor
 * @param size Size of the array
 */
ArrayInt::ArrayInt(int size, Problem * problem) {
  problem_ = problem;
  size_   = size;
  array_ = new int[size_];
	
  lowerBounds_ = new int[size_] ;
  upperBounds_ = new int[size_] ;
		
  for (int i = 0; i < size_ ; i++) {
			//lowerBounds_[i] = (int)(problem_->getLowerLimit(i)) ;
			//upperBounds_[i] = (int)(problem_->getUpperLimit(i)) ;
    
	  array_[i] = PseudoRandom::randInt(problem_->getLowerLimit(i), problem_->getUpperLimit(i));
	//cout<<"Array int value: " <<array_[i]<<endl;											
    //array_[i] = PseudoRandom::randDouble()*(problem_->getUpperLimit(i)-
     //                                     problem_->getLowerLimit(i))+
    //                                     problem_->getLowerLimit(i);
  } // for
} // Constructor


/**
 * Copy Constructor
 * @param arrayReal The arrayInt to copy
 */
ArrayInt::ArrayInt(ArrayInt * arrayInt) {
  problem_ = arrayInt->problem_ ;
  size_  = arrayInt->size_;
  array_ = new int[size_];

  for (int i = 0; i < size_; i++) {
    array_[i] = arrayInt->array_[i];
  } // for
} // Copy Constructor


/**
 * Destructor
 */
ArrayInt::~ArrayInt() {
  delete [] array_;
} // ~ArrayInt


/**
 * Creates an exact copy of a <code>BinaryReal</code> object.
 * @return The copy of the object
 */
Variable * ArrayInt::deepCopy() {
 //cout <<"returning this ArraInt::deepCopy()" << endl;
 //cout <<"before returning print out whats in arrayInt: " << ArrayInt[0]<<endl;
  return new ArrayInt(this);
} // deepCopy


/**
 * Returns the length of the arrayReal.
 * @return The length
 */
int ArrayInt::getLength(){
  return size_;
} // getLength


// /**
 // * getValue
 // * @param index Index of value to be returned
 // * @return the value in position index
 // */
// int ArrayInt::getValue(int index) {
  // if ((index >= 0) && (index < size_))
    // return array_[index] ;
  // else {
    // cout << "ArrayInt.getValue: index value (" << index << ") invalid" << endl;
  // } // if
// } // getValue

double ArrayInt::getValue() {
  cout << "ERROR: ArrayInt::getValue() without index" << endl;
} // getValue


/**
 * getValue
 * @param index Index of value to be returned
 * @return the value in position index
 */
int ArrayInt::getValueInt(int index) {
  if ((index >= 0) && (index < size_))
    return array_[index] ;
  else {
    cout << "ArrayInt.getValue: index value (" << index << ") invalid" << endl;
  } // if
} // getValue



/**
 * setValue
 * @param index Index of value to be returned
 * @param value The value to be set in position index
 */
void ArrayInt::setValue(int index, int value) {
  if ((index >= 0) && (index < size_))
    array_[index] = value;
  else {
    cout << "ArrayInt.getValue: index value (" << index << ") invalid" << endl;
  } // if
} // setValue

void ArrayInt::setValue(double value) {
  cout << "ERROR: ArrayInt::setValue(value) without index" << endl;
} // setValue


/**
 * Get the lower bound of a value
 * @param index The index of the value
 * @return the lower bound
 */
// int ArrayInt::getLowerBound(int index) {
  // if ((index >= 0) && (index < size_))
    // return problem_->getLowerLimit(index) ;
  // else {
    // cout << "ArrayInt.getValue: index value (" << index << ") invalid" << endl;
  // } // if
// } // getLowerBound

// int ArrayInt::getLowerBound() {
  // cout << "ERROR: ArrayInt::getLowerBound() without index" << endl;
// } // getLowerBound


/**
 * Get the upper bound of a value
 * @param index The index of the value
 * @return the upper bound
 */
// int ArrayInt::getUpperBound(int index) {
  // if ((index >= 0) && (index < size_))
    // return problem_->getUpperLimit(index);
  // else {
    // cout << "ArrayInt.getValue: index value (" << index << ") invalid" << endl;
  // } // if
// } // getLowerBound

double ArrayInt::getUpperBound() {
  cout << "ERROR: ArrayInt::getUpperBound() Not Defined" << endl;
} // getUpperBound

double ArrayInt::getLowerBound() {
  cout << "ERROR: ArrayInt::getUpperBound() Not Defined" << endl;
} // getUpperBound
/**
 * Returns a string representing the object
 * @return The string
 */
string ArrayInt::toString(){
  string string_ = "";
  stringstream nop;
  for (int i = 0; i < (size_); i ++) {
    //cout <<"array[i]"<<i<<" " << array_[i];
    nop << array_[i]<<",";
    string_ = nop.str();
   }
  //cout << "The Solution String" << string_ << endl;
  return string_ ;
} // toString
