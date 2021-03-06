//  GDE3_Settings.h
//
//  Author:
//       Esteban L�pez <esteban@lcc.uma.es>
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

#ifndef __GDE3_SETTINGS__
#define __GDE3_SETTINGS__

#include <Settings.h>
#include <GDE3.h>
#include <DifferentialEvolutionCrossover.h>
#include <DifferentialEvolutionSelection.h>

class GDE3_Settings : public Settings{

private:

  double CR_          ;
  double F_           ;
  int populationSize_ ;
  int maxIterations_  ;

  Algorithm * algorithm ;
  Operator  * crossover ; // Crossover operator
  Operator  * selection ; // Selection operator

public:
	GDE3_Settings() ;
	GDE3_Settings(string problemName) ;
	~GDE3_Settings() ;

  Algorithm * configure() ;

}; // GDE3_Settings

#endif // __GDE3_SETTINGS__
