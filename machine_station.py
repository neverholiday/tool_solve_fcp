#!/usr/bin/env python
#
# Copyright (C) 2019  FIBO/KMUTT
#			Written by Nasrun Hayeeyama
#

import sys
import os

import random
import operator

from matplotlib import pyplot as plt

random.seed(0)
import numpy as np
np.random.seed(0)

from genetic_operation import selectionParent, matingPool, breedPopulation, mutatePopulation

def calculateFitness( individual, mat ):
    ''' calculateFitness function
    '''

    #   Initial fitness value
    fitnessValue = 0

    #   loop through individual
    for i in  xrange( len( individual ) ):
        if i == 0:
            continue

        #   individual
        fitnessValue += mat[ individual[ i-1 ], individual[ i ] ]

    return fitnessValue

def rankPop( population, mat ):
    ''' rankPop function
    '''

    #   Rank dict 
    rankDict = dict()
    
    #   loop through population
    for i in xrange( len( population ) ):

        #   calculate and store
        rankDict[ i ] = 1./calculateFitness( population[i], mat )

    return sorted( rankDict.items(), key = operator.itemgetter(1), reverse = True )


#   initial machine number 
numMachine = 25

#   Parameter for population
populationSize = 65
eliteSize = 20
mutateRate = 0.01
generation = 600

#   chromosome of machine
machine = range( 25 )

#   initial rect linear distance
rectLinearDistance = np.random.randint( 50, high = 500, size=( numMachine, numMachine ) )

for i in xrange( numMachine ):
    rectLinearDistance[ i, i ] = 0

rectLinearDistance = rectLinearDistance + rectLinearDistance.T - np.diag( rectLinearDistance.diagonal() )

#   Initial population
population = list()

#   Generate population
for i in xrange( populationSize ):
    population.append( random.sample( machine, len( machine ) ) )

print "[Matrix distance]"
print rectLinearDistance, '\n'

popStart = population

distanceList = list()

#   loop through this
for i in xrange( generation ):
    
    popRank = rankPop( population, rectLinearDistance )

    print " Generation {} : {}".format( i, 1./popRank[0][1] )

    distanceList.append( 1./popRank[0][1] )

    selectionResult = selectionParent( popRank, eliteSize )

    matePool = matingPool( population, selectionResult )

    children = breedPopulation( matePool, eliteSize )

    population = mutatePopulation( children, mutateRate )


print "Finish!"

topPopStart = rankPop( popStart, rectLinearDistance )

print "Original, distance : {}".format( 1./topPopStart[ 0 ][ 1 ] )
print popStart[ topPopStart[ 0 ][ 0 ] ]
popRank = rankPop( population, rectLinearDistance )
print "Arranged, distance : {}".format( 1./popRank[ 0 ][ 1 ] )
print population[ popRank[ 0 ][ 0 ] ]

# print rectLinearDistance
# print calculateFitness( machine, rectLinearDistance )

import pandas as pd
x = pd.DataFrame( rectLinearDistance )
x.to_csv( '/tmpfs/test.csv' )

plt.xlabel( 'Generations' )
plt.ylabel( 'Distance' )
plt.plot( distanceList )
plt.show()