//  BitFlipMutation.h
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

#ifndef __BITFLIP_MUTATION_BOO__
#define __BITFLIP_MUTATION_BOO__

#include <Mutation.h>
#include <Solution.h>
#include <math.h>
#include <float.h>
#include <PseudoRandom.h>
#include <Binary.h>

/**
  * @class Mutation
  * @brief This class implements a polynomial mutation operator.
**/
class BitFlipMutationBoo : public Mutation {

public:
  BitFlipMutationBoo(map<string, void *> parameters);
  ~BitFlipMutationBoo();
  void * execute(void *);

private:
  double mutationProbability_;
  // TODO: VALID_TYPES;
  void * doMutation(double probability, Solution * solution);

}; // BitFlipMutation

#endif