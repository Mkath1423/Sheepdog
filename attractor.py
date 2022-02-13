import math
import random

class Attractor:
    '''
    Attractor
    
    An object that Sheep will be attracted to if they are not scared.
    
    FUNCTIONS
        __init__(positionIn, radiusIn)
            Initializes the attractor with a position and radius
        
        getPointInAttractor()
            returns a random point in the attractor
    '''
    def __init__(self, positionIn, radiusIn):
        '''
        Initializes an attractor.

        Sets values for the position and radius of the attractor.

        Parameters
        ----------
        positionIn: List<int> [x, y]
            The position of the Attractor.
            
        radiusIn: int
            The radius of the Attractor.

        Returns
        -------
        None
        
        Raises:
        -------
        ValueError
            If one of the given values is not of the correct type and will cause errors later in the code.
        
        '''
        # Check if the input values are bad
        if(not type(positionIn) in (list, tuple)): raise ValueError(f'Parameter 1 positionIn must be of type list or tuple not {type(spriteIn)}')
        if(not len(positionIn) == 2): raise ValueError(f'Parameter 1 positionIn must be of length 2 not {len(positionIn)}')
        if(any([not type(positionValue) in (int, float) for positionValue in positionIn])): raise ValueError('Each value in positionIn must be of type int or float')
        
        
        if(not type(radiusIn) is int): raise ValueError(f'Parameter 2 radiusIn must be of type int not {type(radiusIn)}')
        
        # Position and Size
        self.position = positionIn
        self.radius = radiusIn
        
    def getPointInAttractor(self):
        '''
        Returns a point in the attractor's radius.

        Calculates a random point within the attractor.

        Parameters
        ----------
        None

        Returns
        -------
        List<int>
            A randomly chosen point within the attractor 
        '''
        # Choose a random angle and magnitiude within the radius
        randomAngle = random.random() * 360
        randomMagnitude = random.random() * self.radius
        
        # Use the angle and magnitude to calculate an x-y position within the attractor
        return [round(math.cos(math.radians(randomAngle)) * randomMagnitude) + self.position[0],
                round(math.sin(randomAngle) * randomMagnitude) + self.position[1]]
    
    