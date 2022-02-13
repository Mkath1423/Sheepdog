import pygame

class Scene():
    '''
    Scene
    
    A scene that can draw all the visible objects onto a surface and
    return a scaled portion of that surface
    
    FUNCTIONS
    
    __init__(surfaceSizeIn, backgroundColorIn)
        Initialize the surface where the objects will be drawn
        
    render(cameraRect, outputSize)
        Gets a section of the surface, resizes it, then returns it.
        
    boundCameraPosition(cameraPosition, cameraSize)
        Stops a camera position from trying to see pixels that are outside of the scene 
    '''
    def __init__(self, surfaceSizeIn, backgroundColorIn):
        '''
        Initializes the Scene
        
        Initializes a surface, and a list for rendered objects.
        
        Parameters
        ----------
        surfaceSizeIn: [width, height]
            Size of the surface that the rendered objects will be drawn
        
        backgroundColorIn: pygame.Color()
            Background color of the surface
            
        Raises:
        -------
        ValueError
            If one of the given values is not of the correct type and will cause errors later in the code.
        
        Returns
        -------
        None
        '''
        if(not type(surfaceSizeIn) is list): raise ValueError(f'Parameter 1 surfaceSizeIn must be of type list not {type(surfaceSizeIn)}')
        if(not len(surfaceSizeIn) == 2): raise ValueError(f'Parameter 1 surfaceSizeIn must be of length 2 not {surfaceSizeIn}')
        if(any([not type(surfaceSizeValue) == int for surfaceSizeValue in surfaceSizeIn])): raise ValueError('Each value in surfaceSizeIn must be of type int')
        
        self.backgroundColor = backgroundColorIn
        self.surfaceSize = surfaceSizeIn
        self.sceneSurface = pygame.Surface((self.surfaceSize[0], self.surfaceSize[1]))
        
    def render(self, renderedObjects, cameraRect, outputSize):
        '''
        Renders and returns a scetion of the scene
        
        Draws all renderedObjects onto a scene then returns what the camera can see.
        
        Parameters
        ----------
        renderedObjects: list
            Objects that will be rendered onto the scene
        
        cameraRect: pygame.Rect() or [left, top, width, height]
            The position and dimensions of the camera in the scene.
        
        outputSize: (width, height)
            The size of the output. The output will be scaled to these dimensions.
            If the aspect ratio of the cameraRect's width and height are not the same,
            then the image will be warped
            
        Returns
        -------
        pygame.Surface()
            A scaled section of the scene.
        '''
        self.sceneSurface.fill(self.backgroundColor)
        
        # Draw each renderedObject onto the scene
        for renderedObject in renderedObjects:
            try:
                renderedObject.draw(self.sceneSurface)
            except Exception as e:
                print(f'{renderedObject} could not be drawn: {e}')
        
        # Cut out the part of the scene that the camera can see
        camera = pygame.Surface((cameraRect[2], cameraRect[3]))
        camera.blit(self.sceneSurface, (0, 0), cameraRect)
        
        # Scale to camera to the outputSize and return it
        return pygame.transform.scale(camera, outputSize)
               
               
    def boundCameraPosition(self, cameraPosition, cameraSize):
        '''
        Bounds the position of the camera.
        
        Prevents the camera from showing something that is outside of the scene.
        
        Parameters
        ----------
        cameraPosition: List<float> [left, top]
            The position of the camera in the scene.
            
        cameraSize: List<float> [width, height]
            The dimentions of the camera in the scene
            
        Returns
        -------
        None
        '''
        # Limit the camera position to be between 0 and the surfaceSize
        cameraPosition[0] = max(min(cameraPosition[0], self.surfaceSize[0] - cameraSize[0]), 0)
        cameraPosition[1] = max(min(cameraPosition[1], self.surfaceSize[1] - cameraSize[1]), 0)