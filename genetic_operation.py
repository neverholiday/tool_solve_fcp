#!/usr/bin/env python
#
# Copyright (C) 2019  FIBO/KMUTT
#			Written by Nasrun Hayeeyama
#

########################################################
#
#	STANDARD IMPORTS
#

import sys
import os

import random
import operator

########################################################
#
#	LOCAL IMPORTS
#

import pandas as pd

import numpy as np

########################################################
#
#	GLOBALS
#

########################################################
#
#	EXCEPTION DEFINITIONS
#

########################################################
#
#	HELPER FUNCTIONS
#

def selectionParent( popRanked, eliteSize ):
	''' selectionParent function
	'''

	#   Intial empty list
	selectionResults = list()

	#   NOTE : It cum-sum and find percentage
	df = pd.DataFrame( np.array( popRanked ), columns=[ "Index", "Fitness" ] )
	df[ 'cum_sum' ] = df.Fitness.cumsum()
	df[ 'cum_perc' ] = 100*df.cum_sum/df.Fitness.sum()

	# print df

	for i in xrange( 0, eliteSize ):
		selectionResults.append( popRanked[i][0] )

	for i in xrange( 0, len( popRanked ) - eliteSize ):
		parentPick = 100 * random.random()

		for i in xrange( 0, len( popRanked ) ):
			if parentPick <= df.iat[ i, 3 ]:
				selectionResults.append( popRanked[ i ][ 0 ] )
				break
	return selectionResults

def matingPool( population, selectionResults ):
	''' matingPool function
	'''
	
	matingPoolList = list()

	for i in xrange( 0, len( selectionResults ) ):
		index = selectionResults[ i ]
		matingPoolList.append( population[ index ] )

	return matingPoolList

 
def breed( parent1, parent2 ):
	''' breed function (aka cross over)
	'''

	#   Intial hahahahaha
	child = list()
	childP1 = list()
	childP2 = list()

	#   Random select index of gene
	geneA = int( random.random() * len( parent1 ) )
	geneB = int( random.random() * len( parent1 ) )

	#   Start gene
	startGene = min( geneA, geneB )
	endGene = max( geneA, geneB )
	
	for i in xrange( startGene, endGene ):
		childP1.append( parent1[ i ] )

	#   Pull remain gene to child2
	childP2 = [ item for item in parent2 if item not in childP1 ]

	#   Sum it all
	child = childP1 + childP2

	return child

def breedPopulation(matingpool, eliteSize):
	children = []
	length = len(matingpool) - eliteSize
	pool = random.sample(matingpool, len(matingpool))

	for i in range(0,eliteSize):
		children.append(matingpool[i])
	
	for i in range(0, length):
		child = breed(pool[i], pool[len(matingpool)-i-1])
		children.append(child)
	return children


def mutate(individual, mutationRate):
	for swapped in range(len(individual)):
		if(random.random() < mutationRate):
			swapWith = int(random.random() * len(individual))
			
			city1 = individual[swapped]
			city2 = individual[swapWith]
			
			individual[swapped] = city2
			individual[swapWith] = city1
	return individual

def mutatePopulation(population, mutationRate):
	mutatedPop = []
	
	for ind in range(0, len(population)):
		mutatedInd = mutate(population[ind], mutationRate)
		mutatedPop.append(mutatedInd)
	return mutatedPop

########################################################
#
#	CLASS DEFINITIONS
#


