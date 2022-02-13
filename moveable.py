import pygame
import math
import random
from math_utilities import *

class Moveable():
    '''
    Moveable

    This class represents an object that can move
    
    FUNCTIONS
    
        __init__(self, spriteIn, positionIn)
            Initiates a new moveable
            
        draw(self, surfaceIn)
            Rotates the sprite and blits it to the given surface
            
        update(self, surfaceIn, deltatime)
            Calls the move and detectCollisions functions.
            Call this every frame if the object is being shown.
            
        accelerate(self, direction, deltatime)
            Changes the speed of the moveable object
            
        rotate(self, direction, deltatime)
            Changes the rotation of the moveable object
        
        move(self, deltatime)
            Calculates the new position of the moveable object
            
        detectCollisions(self, walls)
            Determines if the Moveable is colliding with a wall.
            Updates the Moveable's position if it needs to.
    '''
    
    def __init__(self, spriteIn, positionIn):
        '''
        Initializes a Moveable Object

        Object contains values needed to draw and move the object.

        Parameters
        ----------
        spriteIn: pygame.Surface()
            The sprite that represents the moveable object. 

        positionIn: List<int>
            the position of the moveable object in the scene.

        Returns
        -------
        None
        
        Raises:
        -------
        ValueError
            If one of the given values is not of the correct type and will cause errors later in the code.
        
        '''
        # Check if the input values are bad
        if(not type(spriteIn) is pygame.Surface): raise ValueError(f'Parameter 1 spriteIn must be of type pygame.Surface not {type(spriteIn)}')
        
        if(not type(positionIn) is list): raise ValueError(f'Parameter 2 positionin must be of type list not {type(positionIn)}')
        if(not len(positionIn) == 2): raise ValueError(f'Parameter 2 positionIn must be of length 2 not {len(positionIn)}')
        if(any([not type(positionValue) in (int, float) for positionValue in positionIn])): raise ValueError('Each value in positionIn must be of type int or float')
        
        # Sprite
        self.size = 20
        self.sprite =  pygame.transform.scale(spriteIn, (self.size, self.size))
        
        # Position and movement
        self.position = positionIn
        self.speed = 0
        self.maxSpeed = 150
        self.acceleration = 300
        
        self.rotationAngle = 0
        self.rotationSpeed = 100
        
    def draw(self, surfaceIn):
        '''
        Draws the moveable.

        Draws the moveable on a given surface using its
        position and rotation.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the moveable will be drawn onto.
            
        Returns
        -------
        None
        '''
        # Render and rotate the sprite onto a tempSurface
        tempSurface = pygame.transform.rotate(self.sprite, self.rotationAngle)
        tempSurface.set_colorkey((0, 255, 0))
        
        # Blit the tempSurface to surfaceIn using self.position as a center
        surfaceIn.blit(tempSurface, [self.position[0] - self.size /2, self.position[1] - self.size / 2])
    
    def accelerate(self, direction, deltatime):
        '''
        Updates the moveable's speed
        
        Uses a physics equation to calculate the new speed.
        The speed is capped between the maxSpeed and the negative maxSpeed.
        
        Parameters
        ----------
        direction: float
            The direction of acceleration of the moveable.
            Positive values accelerate forward, negative values
            accelerate backward, and a value of 0 decelerates until the
            object stops.
            
        deltatime: float
            The elapsed time between frames.
            
        Returns
        -------
        None
        '''
        if direction == 0:
            # Slow down to a stop
            if self.speed < 0: self.speed = min(self.speed + self.acceleration * deltatime, 0)
            elif self.speed > 0: self.speed = max(self.speed - self.acceleration * deltatime, 0)
        else:
            # Speed up (positivly or negatively) utill the maxSpeed is reached
            self.speed = min(max(self.speed + self.acceleration * direction * deltatime, -1 * self.maxSpeed), self.maxSpeed)
    
    def move(self, deltatime):
        '''
        Move the object
        
        Using the speed and the rotation up date the object's position
        
        Parameters
        ----------
        deltatime: float
            The elapsed time between frames.
        
        Returns
        -------
        None
        '''
        # If the object is not moveing fast enough do nothing
        if(self.speed > -1 and self.speed < 1): return
        
        # Update the position
        self.position[0] += math.sin(math.radians(self.rotationAngle + 90)) * self.speed * deltatime
        self.position[1] += math.cos(math.radians(self.rotationAngle + 90)) * self.speed * deltatime
        
    def rotate(self, direction, deltatime):
        '''
        Rotates the object.
        
        Changes the rotation angle depending on the direction and elapsed time.
        
        Parameters
        ----------
        direction: float
            The direction of rotation of the moveable.
            Positive values rotate counterclockwise, negative values
            rotate clockwise.
            
        deltatime: float
            The elapsed time between frames.
            
        Returns
        -------
        None
        '''
        # Rotate the object
        self.rotationAngle = (self.rotationAngle + direction * self.rotationSpeed * deltatime) % 360
    
    def detectCollisions(self, walls):
        '''
        Detects collisions with walls
        
        Determine  if the moveable is colliding with any players
        then updates the moveable's position if it needs to.
        
        Parameters
        ----------
        walls: List<Wall()>
            Walls that the moveable might be colliding with.
            Each one will be tested.
            
        Returns
        --------
        None
        '''
        # For every wall the object could collide with
        for wall in walls:
            result = wall.isCircleColliding(self.position, self.size)
            # If the object collided with a wall
            if(result[0]):
                # Flip its rotaion angle to move away from the wall
                self.rotationAngle = math.degrees(math.atan2(
                    math.sin(math.radians(self.rotationAngle)) * -1 if result[2] else math.sin(math.radians(self.rotationAngle))* 1,
                    math.cos(math.radians(self.rotationAngle)) * -1 if result[1] else math.cos(math.radians(self.rotationAngle)) * 1))
                
                # Change the position to be outside of the wall
                self.position = result[3].copy()
                
    
    def update(self, walls, deltatime):
        '''
        Update the moveable.
        
        Updates the moveable's position and checks for collisions.
        
        Parameters
        ----------        
        walls: List<Wall()>
            Walls that the moveable might be colliding with.
            
        deltatime: float
            The elapsed time between frames.
        
        Returns
        -------
        None
        '''
        
        self.move(deltatime)
        self.detectCollisions(walls)
        
class Sheep(Moveable):
    '''
    Sheep
    
    The class is for a Sheep object. It can move automatically through an algorithm
    
    FUNCTIONS
    __init__(spriteIn, positionIn)
        Initialize with position, sprite, and values for the sheep's movement and movement algorithm
    
    update(self, herd, sheepdogs, attractors, surfaceIn, walls, deltatime)
            Calculates how the sheep should move then moves the sheep.
            Call this every frame that the object is being shown.
    
    applyMovementAlgorithm(self, herd, sheepdogs, attractors, deltatime)
        Calculates which direction the sheep should go in and how fast.
    '''
    def __init__(self, spriteIn, positionIn):
        '''
        Initializes a Sheep object

        Initialized with position, sprite, and values for the sheep's movement
        
        Parameters
        ----------
        spriteIn: pygame.Surface()
            Sprite that represents the Sheep
            
        positionIn: List<int>
            x-y position of the Sheep
        
        Returns
        -------
        None
        '''
        super().__init__(spriteIn, positionIn)
        
        # Control what parts of the algorithm are applied
        self.applySheepdogAvoidance = True
        self.applyAttraction = True
        self.applyCohesion = True
        self.applySeperation = True
        self.applyAlignment = True
        self.applyWallAvoidance = True
        
        # Algorithm values
        self.visualRange = 200
        
        self.cohesion = 0
        
        self.alignment = 0
        
        self.seperationDistance = 30
        self.seperation = 0
        
        self.avoidanceRange = 50
        self.avoidance = 15
        
        self.isScared = False
        
        self.fearDistance = 70
        self.fear = 15
        self.fearTimerDefault = 0.5
        self.fearTimer = 0
        
        self.attraction = 15
        self.attractionPoint = [0, 0]
        
    def update(self, herd, sheepdogs, attractors, walls, deltatime):
        '''
        Updates the sheep's position

        Uses the movement agorithm to determine how the sheep should move then
        moves the sheep.
        
        Parameters
        ----------
        herd: List<Sheep()>
            Sheep objects that are in the level
            
        sheepdogs: List<Moveable()>
            Moveable objects that are in the level
            
        attractors: List<Attractor()>
            Attractor objects that are in the level
            
        walls: List<Wall()>
            Wall objects that are in the level
            
        deltatime: float
            The time that has passed between frames
        
        Returns
        -------
        None
        '''
        
        super().update(walls, deltatime)
        self.applyMovementAlgorithm(herd, sheepdogs, attractors, walls, deltatime)
       
    def applyMovementAlgorithm(self, herd, sheepdogs, attractors, walls, deltatime):
        '''
        Determines how the Sheep should move.

        Uses the movement algorithm to determine how the sheep should move.
        If the sheep is scared then it will run away otherwise it
        will approach a random attractor.
        
        Parameters
        ----------
        herd: List<Sheep()>
            Sheep objects that are in the level
            
        sheepdogs: List<Moveable()>
            Moveable objects that are in the level
            
        attractors: List<Attractor()>
            Attractor objects that are in the level
            
        walls: List<Wall()>
            Wall objects that are in the level
            
        deltatime: float
            The time that has passed between frames
        
        Returns
        -------
        None
        '''
        finalVector = [0, 0]
        
        # Find the closest sheepdog
        distanceToClosestSheepDog = 10000000
        closestSheepdog = None
        
        # For every sheepdog
        for sheepdog in sheepdogs:
            # If it is closer than the distanceToClosestSheepDog
            distanceToSheepdog = distance(sheepdog.position, self.position)
            if distanceToClosestSheepDog > distanceToSheepdog:
                # Store that sheepdog and its position
                distanceToClosestSheepDog = distanceToSheepdog
                closestSheepdog = sheepdog
        
        # CONDITIONAL FORCES
        # If there is a sheep dog nearby
        if(distanceToClosestSheepDog < self.fearDistance):
            # If there was not a sheepdog nearby on the previous frame
            if(self.isScared == False):
                # Update algorithm values
                self.isScared = True
                self.maxSpeed = 150
                
                self.cohesion = 1
                self.alignment = 6
                self.seperation = 7
                
                self.attractionPoint = None
                
                # Turn away from the sheepdog
                self.rotationAngle = direction(closestSheepdog.position, self.position) % 360
                
            # reset the fear timer
            self.fearTimer = self.fearTimerDefault
        
        # If there is no sheep dog nearby
        elif(self.fearTimer < 0.000001):
            # If there was a sheepdog nearby on the previous frame
            if(self.isScared == True):
                # Update algorithm values
                self.isScared = False
                self.maxSpeed = 30
                
                self.cohesion = 1
                self.alignment = 2
                self.seperation = 8
                
                # Choose a new attraction point
                if(not len(attractors) == 0):
                    self.attractionPoint = random.choice(attractors).getPointInAttractor()
                
        # If there is no sheepdog nearby but the timer has not runout   
        else:
            # Decrement the fear timer by the elapsed time
            self.fearTimer -= deltatime
            
        # If the sheep is scared               
        if(self.isScared):
            if(self.applySheepdogAvoidance):
                # Apply Sheepdog Avoidance
                directionToClosestSheepdog = direction(self.position, closestSheepdog.position)
                self.attractionPoint = None
            
            
                finalVector[0] += -1 * directionToClosestSheepdog * self.fear
                finalVector[1] += self.fear
        
        # If the sheep is not scared
        else:
            # If the sheep has reached the attraction point then stop moving
            if(not self.attractionPoint == None):
                if(distance(self.position, self.attractionPoint) < 30): self.maxSpeed = 0
                else: self.maxSpeed = 30
                
                if(self.applyAttraction):
                    # Apply Attraction
                    # Only appy attraction is the sheep can see the attraction point
                    if(distance(self.position, self.attractionPoint) < self.visualRange):
                        directionToAttractionPoint = direction(self.position, self.attractionPoint) % 360
                        directionToAttractionPoint -= self.rotationAngle
                        
                        if(directionToAttractionPoint > 180): directionToAttractionPoint = -360 + directionToAttractionPoint
                        finalVector[0] += directionToAttractionPoint * self.attraction
                        finalVector[1] += self.attraction 
        
        # CONSTANT FORCES
        midpoint = [0, 0]
        nearbySheep = 0
        
        closestSheepPosition = []
        closestSheepDistance = 100000
        
        averageRotation = 0
        nearbySheep = 0
        
        # FIND VECTORS FOR ALIGNMENT, COHESION, SPERATION
        # alignment: average rotaion of nearby sheep
        # cohestion: average position of nearby sheep
        # seperation: position of the nearest sheep
        for sheep in herd:
            distanceToOtherSheep = distance(sheep.position, self.position)
            # if the sheep can be seen and is not this sheep
            if(distanceToOtherSheep < self.visualRange and not distanceToOtherSheep == 0):
                
                # Add its position to the midpoint
                midpoint[0] += sheep.position[0]
                midpoint[1] += sheep.position[1]
                
                # Add its rotation to the average rotation
                averageRotation += sheep.rotationAngle
                
                # Increment nearbySheep
                nearbySheep += 1

            # If the sheep is closer than the closest sheep store its position    
            if(distanceToOtherSheep < self.seperationDistance):
                if(distanceToOtherSheep < closestSheepDistance and not distanceToOtherSheep == 0):
                    closestSheepPosition = sheep.position
        
        if(self.applyCohesion):
            # Apple Cohesion
            if(not nearbySheep == 0):
                # Calculate the midpoint of all nearby sheep
                midpoint[0] = midpoint[0]/nearbySheep
                midpoint[1] = midpoint[1]/nearbySheep      
                
                # Calculate the relative direction to the midpoint
                directionToMidpoint = direction(self.position, midpoint) % 360
                directionToMidpoint -= self.rotationAngle
                if(directionToMidpoint > 180): directionToMidpoint = -360 + directionToMidpoint
                
                # Add the direction with the cohesion scaler to the final vector 
                finalVector[0] += directionToMidpoint * self.cohesion
                finalVector[1] += self.cohesion
            
        if(self.applySeperation):
            # Apply Seperation
            if(not closestSheepPosition == []):
                # Calculate the relative direction to the closest sheep
                directionToClosestSheep = direction(self.position, closestSheepPosition) % 360
                directionToClosestSheep -= self.rotationAngle
                if(directionToClosestSheep > 180): directionToClosestSheep = -360 + directionToClosestSheep
                
                # Add the direction with the seperation scaler to the final vector 
                finalVector[0] += -1 * directionToClosestSheep * self.seperation
                finalVector[1] += self.seperation
            
        if(self.applyAlignment):
            # Apply Alignment  
            if(not nearbySheep == 0):
                # Calculate the average rotation of all nearby sheep
                averageRotation /= nearbySheep
                
                # Make that value relative to the sheep's rotation
                averageRotation -= self.rotationAngle
                if(averageRotation > 180): averageRotation = -360 + averageRotation
                
                # Add the averageRoation with the alignment scaler to the final vector 
                finalVector[0] += averageRotation * self.alignment
                finalVector[1] += self.alignment
                
        if(self.applyWallAvoidance):
            # Wall Avoidance
            averageAvoidanceRotation = 0
            avoidanceRays = 0
            
            # Angle of each ray that will be tested
            for angle in [60, 30, -30, -60]:
                relativeAngle = angle - self.rotationAngle
                
                # End point of the ray
                visualRay = (self.position[0] + self.avoidanceRange * math.cos(math.radians(relativeAngle)),
                             self.position[1] + self.avoidanceRange * math.sin(math.radians(relativeAngle)))
                
                # check if the ray is colliding with a wall
                closestCollision = None
                for wall in walls:
                    rayCollision = wall.isLineSegmentColliding(self.position, visualRay)
                    
                    # Store the nearest collision to the sheep
                    if(rayCollision == None): continue
                    if(closestCollision == None): closestCollision = rayCollision
                    
                    if(distance(self.position, rayCollision) < distance(self.position, closestCollision)):
                        closestCollision = rayCollision
            
                
                if(not closestCollision == None):
                    
                    # Determine how the sheep should turn based on this ray
                    # If the collision is near then turn further
                    # Ture towards the opposite direction of the collision
                    closestCollisionDistance = distance(self.position, closestCollision)
                    
                    averageAvoidanceRotation += (angle / abs(angle)) * 180 - ((closestCollisionDistance / self.visualRange) * 180)
                    avoidanceRays += 1

            
            if(not avoidanceRays == 0):
                # Take the average direction that the sheep should turn based on the determined values from each ray
                averageAvoidanceRotation /= avoidanceRays
                
                # Add this rotation to the final vector
                finalVector[0] += averageAvoidanceRotation * self.avoidance
                finalVector[1] += self.avoidance
            # Move away from nearby collisions
        
        # Move the sheep according to the vector found by the algorithm
        self.accelerate(1, deltatime)
        
        if(not finalVector[1] == 0):
            #print(f'Final Rotaion: (finalVector[0] / finalVector[1])/ 180', end = '\n\n')
            self.rotate((finalVector[0] / finalVector[1])/ 180, deltatime)