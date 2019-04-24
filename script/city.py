#!/usr/bin/env python

import math

class City:

    def __init__( self, x, y ):
        self.x = x
        self.y = y

    def distance( self, city ):
        ''' distance function
        '''
        #   find norm of each axis
        xDis = math.pow( self.x - city.x, 2 ) 
        yDis = math.pow( self.y - city.y, 2 )
        
        #   euclidian approach
        distance = math.sqrt( xDis + yDis )

        return distance

    def __repr__( self ):
        return "This city is located on ({},{})\n".format( self.x, self.y )


if __name__ == "__main__":
    
    city1 = City( 1, 2 )
    city2 = City( 5, 6 )

    print city1
    print city2

    print city1.distance( city2 )