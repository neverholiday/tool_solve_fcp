#!/usr/bin/env python

class Fitness:

	def __init__( self, route ):

		self.route = route
		self.distance = 0
		self.fitness = 0.0
	
	def routeDistance(self):
		''' routeDistance function
		'''
		if self.distance == 0:
			pathDistance = 0
			for i in range(0, len(self.route)):
				fromCity = self.route[i]
				toCity = None
				if i + 1 < len(self.route):
					toCity = self.route[i + 1]
				else:
					toCity = self.route[0]
				pathDistance += fromCity.distance(toCity)
			self.distance = pathDistance
		return self.distance
	
	def routeFitness(self):
		''' routeFitness function
		'''
		if self.fitness == 0:
			self.fitness = 1 / float(self.routeDistance())
		return self.fitness