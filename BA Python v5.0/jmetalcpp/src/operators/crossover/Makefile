CPP  = g++
CC   = gcc
OBJ  = Crossover.o DifferentialEvolutionCrossover.o SBXCrossover.o SinglePointCrossover.o SinglePointCrossoverBoo.o
LIB  = libcrossover.a

LIBS +=  -lm 
INCS +=  -I. -I../../core -I../../util/wrapper -I../../encodings/solutionType -I../../encodings/variable \
	-I../../util

#CXXFLAGS += $(INCS) -g 
CXXFLAGS += $(INCS) 

CFLAGS = $(INCS) 

.PHONY: all all-before all-after clean clean-custom

all: all-before $(LIB) all-after

clean: clean-custom
	rm -f $(OBJ) $(LIB)

$(LIB): $(OBJ)
	ar -r $(LIB) *.o
	ranlib $(LIB)

.cpp.o:
	$(CPP) $(CXXFLAGS) -c $< 
