class Goal():
    '''
    Goal
    
    The area that the players need to lead the sheep to.
    
    FUNCTIONS
    
    __init__(self, rectIn):
        Initializes the goal with a position and dimensions.
        
    isSheepInGoal(self, sheepPosition):
        Determins if the sheep is in the goal.
    '''    
    def __init__(self, rectIn):
        '''
        Initializes a Goal.
        
        Initializes a value for the Goal's position and dimensions
        
        Parameters
        ----------
        rectIn: List<float> or Tuple<float> [left, top, width, height]
            The position and dimentions of the Goal
        
        Returns
        -------
        None
        
        Raises:
        -------
        ValueError
            If one of the given values is not of the correct type and will cause errors later in the code.
        
        '''
        
        if(not type(rectIn) in (list, tuple)): raise ValueError(f'Parameter 1 rectIn must be of type list or tuple not {type(rectIn)}')
        if(not len(rectIn) == 4): raise ValueError(f'Parameter 1 rectIn must be of length 4 not {len(rectIn)}')
        if(any([not type(rectangleValue) in (float, int) for rectangleValue in rectIn])): raise ValueError('Each value in rectIn must be of type int or float')
        
        self.rect = rectIn
        
    def isSheepInGoal(self, sheepPosition):
        '''
        Determines if the sheep is in the goal.
        
        Uses the sheep's position to determine if its center is inside
        the Goal's rectangle.
        
        Parameters
        ----------
        sheepPosition: List<float> [x, y]
            The position of the sheep.
            
        Returns:
        bool
            True if the sheep is in the Goal otherwise False.
        '''
        
        return (sheepPosition[0] > self.rect[0] and
                sheepPosition[0] < self.rect[0] + self.rect[2] and
                sheepPosition[1] > self.rect[1] and
                sheepPosition[1] < self.rect[1] + self.rect[3])