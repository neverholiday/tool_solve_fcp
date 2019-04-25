#!/usr/bin/env python

import pandas as pd

import numpy as np
import random
import operator
from matplotlib import pyplot as plt


from city import City
from fitness import Fitness

#   Helper function

def creatRoute( cityList ):
	''' createRoute function
	'''
	route = random.sample( cityList, len( cityList ) )
	return route

def initialPopulation( popSize, cityList ):
	''' initialPopulation function
	'''

	population = list()

	#   Add route to population
	for i in xrange( 0, popSize ):
		population.append( creatRoute( cityList ) )
	return population

def rankRoutes( population ):
	''' rankRoutes function
	'''
	#   Initial dict
	fitnessResutsDict = dict()

	for i in xrange( 0, len( population ) ):
		fitnessResutsDict[ i ] = Fitness( population[ i ] ).routeFitness()

	return sorted( fitnessResutsDict.items(), key = operator.itemgetter( 1 ), reverse = True )

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

def nextGeneration(currentGen, eliteSize, mutationRate):
	'''	nextGeneration function
	'''

	#	Rank routes
	popRanked = rankRoutes(currentGen)
	
	#	Selection parents
	selectionResults = selectionParent(popRanked, eliteSize)
	
	#	Mating pools
	matingpool = matingPool(currentGen, selectionResults)
	
	#	Make a children
	children = breedPopulation(matingpool, eliteSize)
	
	#	Mutate!!!
	nextGeneration = mutatePopulation(children, mutationRate)
	
	return nextGeneration

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
	pop = initialPopulation(popSize, population)
	print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
	
	for i in range(0, generations):
		pop = nextGeneration(pop, eliteSize, mutationRate)
		print "Distance each generation {} : {}".format( i, 1/rankRoutes( pop )[ 0 ][ 1 ] )
	
	print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
	bestRouteIndex = rankRoutes(pop)[0][0]
	bestRoute = pop[bestRouteIndex]
	return bestRoute

if __name__ == "__main__":

	random.seed(1)
	
	cityList = list()

	for i in range(0,25):
		cityList.append( City( x=int( random.random() * 200 ), y=int( random.random() * 200 ) ) )

	population = initialPopulation( 100, cityList )

	#	ranking
	popRanked = rankRoutes( population )

	#	Selection
	selectionResults = selectionParent( popRanked, 20 )

	#	Mating pools
	poolMate = matingPool(population, selectionResults)
	
	#	Make a children
	children = breedPopulation(poolMate, 20)

	print "Parent A : {}, Parent B : {}".format( len( poolMate[0] ), len( poolMate[1] ) )

	x = breed( poolMate[0], poolMate[1] )

	print "Children : {}".format( len( x ) )

	# print children

	# #	Mutate!!!
	# nextGeneration = mutatePopulation(children, 0.01)

	# # print len( nextGeneration )


	# for i in xrange(len(popRanked)):
	# 	if i < 20:
	# 		print popRanked[i]

	
	# # for i in cityList:
	# # 	print i

	# pop = initialPopulation( 100, cityList )

	# x = Fitness( pop[ 0 ] )

	# print x.routeDistance()
	# print x.routeFitness()
	# print 1/ x.routeDistance()

	# bestRoute = geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)

	# plotList = [ cityList, bestRoute ]

	# fig, axes = plt.subplots( nrows=1, ncols=2 )
	
	# for i, ax in enumerate( axes ):
	# 	for j in xrange( len(plotList[i]) ):
	# 		if j > 0:
	# 			xSegment = ( plotList[i][j-1].x, plotList[i][j].x )
	# 			ySegment = ( plotList[i][j-1].y, plotList[i][j].y )
	# 			ax.plot( xSegment, ySegment )
	# 		ax.scatter( plotList[i][j].x, plotList[i][j].y )

	# plt.show()
	# for row in ax:
	# 	for idx, col in enumerate( row ):
	# 		col.plot( x[idx] )
