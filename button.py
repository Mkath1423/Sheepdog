import pygame

# Button class adapted from maze-game project
class Button():
    '''
    Button
    
    A button that the user can click.
    The buttons will allow the user to navagite the menus.
    
    FUNCTIONS
        __init__(self, returnDataIn, buttonRectangeIn, buttonColorIn, textIn, textColorIn, fontIn)
            Creates the button object with initial values.
        
        draw(self, surfaceIn)
            Draws the button as a rounded rectangle with text.
            
        isMouseColliding(self, mousePosition)
            Returns true if the mouse is on the button.
            
        update(self, surfaceIn)
            Calls the draw function.
            This function is called every frame.
        
    '''    
    def __init__(self, returnDataIn, buttonRectangeIn, buttonColorIn, textIn, textColorIn, fontIn):
        '''
        Initializes a Button Object.

        Object contains all the values needed to make a button with text.

        Parameters
        ----------
        returnDataIn: str
            Some data that will be returned when clicked.
            Used for applying different functions to different buttons.

        buttonRectangeIn: List<float> [left, top, width, height] 
            The rectangle object that represents the top-left position of the
            Button and its dimensions.

        buttonColorIn: pygame.Color()
            The color of the button.
            
        textIn: str 
            The text that will appear on the button.
            
        textColorIn: pygame.Color()
            The color of the text on the button.
            
        fontIn: pygame.Font() 
            The font used to render the text.

        Returns
        -------
        None
        '''
        
        # Position and Size
        self.buttonRectangle = buttonRectangeIn
        
        # Colors
        self.buttonColor = buttonColorIn
        
        self.normalColor = buttonColorIn
        
        self.hoveringColor =  pygame.Color(0, 0, 0)
        self.hoveringColor.update(int(buttonColorIn.r * 0.75), int(buttonColorIn.g * 0.75), int(buttonColorIn.b * 0.75))
        
        self.textColor = textColorIn
        
        # Text
        self.text = textIn
        self.font = fontIn
        
        # Data to be returned when clicked
        self.returnData = returnDataIn
        
        
    def update(self, surfaceIn, mousePosition):
        '''
        Update the button.
        
        Redraw the button onto the given surface.
        Recolors it if the mouse is hovering over the button
        
        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the button will be drawn onto.
            
        mousePosition: List<float> [x, y]
            The position of the user's mouse on the surface
            
        Returns
        -------
        None
        '''
        # If the mouse if hovering over the button
        # Change to color of the button to the hovering color
        if(self.isMouseColliding(mousePosition)):
            self.buttonColor = self.hoveringColor
        else:
            self.buttonColor = self.normalColor
        
        # draw the button
        self.draw(surfaceIn)

    def draw(self, surfaceIn):
        '''
        Draws the Button Object

        Draws the Button as a rounded rectangle with text onto the given surface.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the button will be drawn onto.
            
        Returns
        -------
        None
        '''
        # draw a rounded rectangle onto surfaceIn
        pygame.draw.rect(surfaceIn, self.buttonColor, self.buttonRectangle, border_radius = 2)
        
        # render the text of the button
        buttonText = self.font.render(self.text, 1, self.textColor)
        
        # blit the text onto surfaceIn. Make it centered on the button rectangle. 
        surfaceIn.blit(buttonText, (self.buttonRectangle[0] + self.buttonRectangle[2]/2 - buttonText.get_width()/2,
                                    self.buttonRectangle[1] + self.buttonRectangle[3]/2 - buttonText.get_height()/2))
    
        
    def isMouseColliding(self, mousePosition):
        '''
        Determine if the player's mouse is colliding with the button.

        Using the position of the mouse and button determine if
        the mouse is on the button.

        Parameters
        ----------
        mousePosition: List<int>
            The position of the player's mouse on the surface.
            
        Returns
        -------
        bool
            True if the mouse is colliding with the button.
        '''
        # return true if the position of the mouse is inside the button rectangle 
        return(mousePosition[0] > self.buttonRectangle[0] and
               mousePosition[0] < self.buttonRectangle[0] + self.buttonRectangle[2] and
               mousePosition[1] > self.buttonRectangle[1] and
               mousePosition[1] < self.buttonRectangle[1] + self.buttonRectangle[3])
    
    