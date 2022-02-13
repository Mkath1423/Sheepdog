import pygame

class Decal():
    '''
    Decal
    
    An object that is drawn on the ground.
    This can be used to guide players in-game or to add decorations.
    
    FUNCTIONS
        __init__(self, spriteIn, positionIn, decalSize)
            Initializes a Decal.
            
        draw(self, surfaceIn)
            Draws the Decal
        
    '''
    def __init__(self, spriteIn, positionIn, decalSize):
        '''
        Initializes a Decal.
        
        Initializes the Decal's sprite and position.
        
        Parameters
        ----------
        spriteIn: pygame.Suface()
            The sprite that represents the Decal
        
        positionIn: List<float> [x, y]
            The position of the Decal.
        
        decalSize: List<float> [width, height]
            The size of the Decal.
            
        Returns:
        --------
        None
            
        Raises:
        -------
        ValueError
            If one of the given values is not of the correct type and will cause errors later in the code.
        '''
        # Check if the input values are bad
        if(not type(spriteIn) is pygame.Surface): raise ValueError(f'Parameter 1 spriteIn must be of type pygame.Surface not {type(spriteIn)}')
        
        if(not type(positionIn) in (list, tuple)): raise ValueError(f'Parameter 2 positionIn must be of type list or tuple not {type(spriteIn)}')
        if(not len(positionIn) == 2): raise ValueError(f'Parameter 2 positionIn must be of length 2 not {len(positionIn)}')
        if(any([not type(positionValue) in (int, float) for positionValue in positionIn])): raise ValueError('Each value in positionIn must be of type int or float')
        
        if(not type(decalSize) in (list, tuple)): raise ValueError(f'Parameter 3 decalSize must be of type list or tuple not {type(decalSize)}')
        if(not len(decalSize) == 2): raise ValueError(f'Parameter 2 decalSize must be of length 2 not {len(decalSize)}')
        if(any([not type(decalSizeValue) in (int, float) for decalSizeValue in decalSize])): raise ValueError('Each value in decalSize must be of type int or float')
        
        # Sprite scaled to correct size
        self.sprite =  pygame.transform.scale(spriteIn, decalSize)
        
        # Position
        self.position = positionIn
    
    def draw(self, surfaceIn):
        '''
        Draws the Decal
        
        Blits the Decal onto a given surface.
        
        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the decal will be drawn onto.
            
        Returns
        -------
        None
        '''
        surfaceIn.blit(self.sprite, self.position)