//  NSGAIIStudy_main.cpp
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

#include <NSGAIIStudy.h>
#include <stdlib.h>

int main(int argc, char ** argv) {

  cout << "Creando NSGAIIStudy" << endl;
  NSGAIIStudy * exp = new NSGAIIStudy() ; // exp = experiment
  cout << "Creado NSGAIIStudy" << endl;

  exp->experimentName_ = "NSGAIIStudy";

  const char * algorithmNameList_[] = {
      "NSGAIIa", "NSGAIIb", "NSGAIIc", "NSGAIId"};
  exp->algorithmNameList_.assign(algorithmNameList_, end(algorithmNameList_));

  const char * problemList_[] = {
      "ZDT1", "ZDT2", "ZDT3", "ZDT4", "DTLZ1"};
  exp->problemList_.assign(problemList_, end(problemList_));

  const char * paretoFrontFile_[] = {
      "ZDT1.pf", "ZDT2.pf", "ZDT3.pf","ZDT4.pf", "DTLZ1.2D.pf"};
  exp->paretoFrontFile_.assign(paretoFrontFile_, end(paretoFrontFile_));

  const char * indicatorList_[] = {
      "HV", "SPREAD", "IGD", "EPSILON"};
  exp->indicatorList_.assign(indicatorList_, end(indicatorList_));

  int numberOfAlgorithms = exp->algorithmNameList_.size();

  exp->experimentBaseDirectory_ = "C:/antonio/Softw/pruebas/jmetal/kk/" +
                                 exp->experimentName_;
  exp->paretoFrontDirectory_ = "C:/antonio/Softw/pruebas/data/paretoFronts";

  exp->algorithmSettings_ = new Settings*[numberOfAlgorithms];

  exp->independentRuns_ = 4;

  // Run the experiments
  int numberOfThreads;
  cout << "Comenzando runExperiment" << endl;
  exp->runExperiment(numberOfThreads = 1);
  cout << "Terminando runExperiment" << endl;

  // TODO Continuar más allá de abrir hebras
  //  // Generate latex tables (comment this sentence is not desired)
  //  exp->generateLatexTables() ;
  //
  //  // Configure the R scripts to be generated
  //  int rows = 2 ;
  //  int columns = 3 ;
  //  string prefix = "Problems";
  //  const char * problemsValues[] = {
  //      "ZDT1", "ZDT2","ZDT3", "ZDT4", "DTLZ1", "WFG2"};
  //  vector<string> problems (problemsValues, end(problemsValues));
  //
  //  bool notch;
  //  exp->generateRBoxplotScripts(rows, columns, problems, prefix, notch = true, exp);
  //  exp->generateRWilcoxonScripts(problems, prefix, exp);

} // main
