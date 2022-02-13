import pygame
from math_utilities import *

# Wall class adapted from maze-game project
class Wall():
    '''
    Wall
    
    A wall object that acts as an impassible barrier for moveable objects.
    
    FUNCTIONS
        __init__(self, rectangleIn, colorIn)
            Creates the wall object with initial values for its position, size, and color.
            
        draw(self, surfaceIn)
            Draws the wall as a rectangle on a surface.
        
        isCircleColliding(self, circlePos, circleSize)
            Returns true if the circle is colliding with the wall.
            
        isLineSegmentColliding(self, p1, p1)
            Returns the closest POI of a line segment and the wall.
    '''
    def __init__(self, rectangleIn, colorIn):
        '''
        Initializes a Wall Object

        Wall contains values for the position, the size, and the color of the wall.

        Parameters
        ----------
        rectangleIn: pygame.Rect() or [left, top, width, height]
            The rectangle object that represents the top-left position of the
            wall and its dimensions. 

        colorIn: pygame.Color()
            The color of the rectangle that represents the wall.

        Returns
        -------
        None
        
        Raises:
        -------
        ValueError
            If one of the given values is not of the correct type and will cause errors later in the code.
        
        '''
        # Check if the input values are bad
        if(not type(colorIn) is pygame.Color): raise ValueError(f'Parameter 2 colorIn must be of type pygame.Color not {type(colorIn)}')
        
        if(not type(rectangleIn) in (tuple, list)): raise ValueError(f'Parameter 1 rectangleIn must be of type list or tuple not {type(rectangleIn)}')
        if(not len(rectangleIn) == 4): raise ValueError(f'Parameter 1 rectangleIn must be of length 4 not {len(rectangleIn)}')
        if(any([not type(rectangleValue) in (int, float) for rectangleValue in rectangleIn])): raise ValueError('Each value in rectangleIn must be of type int or float')
        
        # Position and Size
        self.rectangle = rectangleIn
        
        # Color
        self.color = colorIn
        
    def draw(self, surfaceIn):
        '''
        Draws the wall.

        Draws the wall as a rectangle with the specified color, size, and position on a given surface.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the wall will be drawn onto.
            
        Returns
        -------
        None
        '''
        pygame.draw.rect(surfaceIn, self.color, self.rectangle)
            
    def isCircleColliding(self, circlePosition, circleSize):
        '''
        Determine if a circle is colliding with the wall.

        Using the position and dimensions of the wall and circle
        determine if they are colliding.

        Parameters
        ----------
        playerPos: List<int>
            The position of the circle on the surface.
            [x, y]
            
        playerSize: int
            The radius of the circle.
            
        Returns
        -------
        bool
            True if the player is colliding with the wall otherwise False.
        
        bool
            True if there is a collision on the x-axis.
        
        bool
            True if there is a collision on the y-axis.
        
        List<int>
            The new position of the circle.
            If the circle is colliding with a wall, the position will be adjusted
            otherwise, it will remain the same.
        '''
        # The highest and lowest y values of the circle
        circleTop    = circlePosition[1] - circleSize
        circleBottom = circlePosition[1] + circleSize
        
        # The highest and lowest y values of the wall's rectangle
        wallTop = self.rectangle[1]
        wallBottom = self.rectangle[1] + self.rectangle[3]
        
        # The highest and lowest x values of the circle
        circleLeft   = circlePosition[0] - circleSize
        circleRight  = circlePosition[0] + circleSize
        
        # The highest and lowest x values of the wall's rectangle
        wallLeft = self.rectangle[0]
        wallRight = self.rectangle[0] + self.rectangle[2]
        
        newPosition = circlePosition.copy()
        
        xCollision = False
        yCollision = False
        
        conditionsMet = 0
        
        # if the circle is to the left of the left side of the wall
        if(circlePosition[0] < wallLeft):
            # if the circle's right side is colliding with the wall
            if(circleRight > wallLeft):
                newPosition[0] -= 1
                xCollision = True
                conditionsMet += 1
                
        # if the circle is to the right of the right side of the wall
        elif(circlePosition[0] > wallRight):
            # if the circle's left side is colliding with the wall
            if(circleLeft < wallRight):
                newPosition[0] += 1
                xCollision = True
                conditionsMet += 1
                
        # if the circle is between the left and right edges
        else:
            conditionsMet += 1
        

        # if the circle is above the top side of the wall
        if(circlePosition[1] < wallTop):
            # if the circle's bottom side is colliding with the wall
            if(circleBottom > wallTop):
                newPosition[1] -= 1
                yCollision = True
                conditionsMet += 1
                
        # if the circle is below the bottom side of the wall
        elif(circlePosition[1] > wallBottom):
            # if the circle's top side is colliding with the wall
            if(circleTop < wallBottom):
                newPosition[1] += 1
                yCollision = True
                conditionsMet += 1
        
        # if the circle is between the top and bottom edges 
        else:
            conditionsMet += 1
                 
        return (conditionsMet == 2, xCollision, yCollision, newPosition)
    
    def isLineSegmentColliding(self, p1, p2):
        '''
        Checks if a line segment is colliding with the rectangle
        
        Test for collisions with each of the 4 edges of the wall and returns the closest collision
        or None if there are no collisions.
        
        Parameters
        ----------
        p1: List<float> [x, y]
            The starting point of the line segment
            
        p2: List<float> [x, y]
            The ending point of the line segment
        
        Returns
        -------
        Tuple<float> (x, y)
            The closest point of intersection
            
        None
            If there are no collisions with the wall
        '''
        # verticies of the wall
        topLeft = [self.rectangle[0], self.rectangle[1]]
        topRight = [self.rectangle[0] + self.rectangle[2], self.rectangle[1]]
        bottomLeft = [self.rectangle[0], self.rectangle[1] + self.rectangle[3]]
        bottomRight = [self.rectangle[0] + self.rectangle[2], self.rectangle[1] + self.rectangle[3]]
        
        # edges of the wall
        wallTop = [topLeft, topRight]
        wallBottom = [bottomLeft, bottomRight]
        wallLeft = [topLeft, bottomLeft]
        wallRight = [topRight, bottomRight]
        
        closestCollision = None
        
        # test a for collisions with each edge
        for edge in (wallTop, wallBottom, wallLeft, wallRight):
            intersection = findPointOfIntersection(p1, p2, edge[0], edge[1])
            
            # store the closest collision
            if(not intersection == None):
                # if there is no closest point
                if(closestCollision == None):
                    # made this intersection the new closest point
                    closestCollision = intersection
                    continue
                
                # if this intersection is closer than the previous closest point
                if(distance(p1, intersection) < distance(p1, closestCollision)):
                    # made this intersection the new closest point
                    closestCollision = intersection
        
        return closestCollision