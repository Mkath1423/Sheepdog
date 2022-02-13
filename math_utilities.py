import math


def distance(point1, point2):
    '''
    Calculates the distance between two points
    
    Calculates and returns the positive distance between the points.
    The order of the points does not matter.
    
    Parameters
    ----------
    point1: List<float> [x, y]
        first point
    
    point2: List<float> [x, y]
        second point
    
    Return
    -------
    float
        The distance between the two points
    '''
    return(math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2))

def direction(point1, point2):
    '''
    Calculates the direction from one point to another
    
    The direction goes from the first point to the second point
    
    Parameters
    ----------
    point1: List<float> [x, y]
        the first point
    
    point2: List<float> [x, y]
        the second point
    
    Return
    -------
    float
        The direction from point1 to point2
    '''
    return math.degrees(math.atan2(-1*(point2[1]-point1[1]), (point2[0]-point1[0])))

def findPointOfIntersection(p1, p2, q1, q2):
    '''
    Finds the point of intersection of 2 line segments.
    
    Creates a linear system using the four points.
    Returns the POI of the lines if the POI is on both line segments.
    
    Parameters
    ----------
    p1: List<float> [x, y]
        A point on line p
        
    p2: List<float> [x, y]
        A point on line p
        
    q1: List<float> [x, y]
        A point on line q
        
    q2: List<float> [x, y]
        A point on line q
        
    Returns
    -------
    Tuple<float> (x, y)
        The point of intersection (POI)
        
    None
        If the lines are parallel or if the POI is not on the line segments
    '''
    # make p1 have the lower x value of p1 and p2
    if(p2[0] < p1[0]):
        temp = p1
        p1 = p2
        p2 = temp
        
    # make q1 have the lower x value of q1 and q2
    if(q2[0] < q1[0]):
        temp = q1
        q1 = q2
        q2 = temp
        
    poi = [None, None]
    
    # if both lines are vertical
    if(p2[0] - p1[0] == 0 and q2[0] - q1[0] == 0):
        return None
    
    # if line p is vertical
    elif(p2[0] - p1[0] == 0):
        # slope and x intercept of the non-vertical line
        qSlope = (q2[1] - q1[1])/(q2[0] - q1[0])
        qXIntercept = -1 * (qSlope * q1[0]) + q1[1]
        
        # make and use the linear equation to solve for the point of intersection 
        poi[0] = p1[0]
        poi[1] = -1 * (qSlope * q1[0]) + q1[1]
        
    # if line q is vertical
    elif(q2[0] - q1[0] == 0):
        # slope and x intercept of the non-vertical line 
        pSlope = (p2[1] - p1[1])/(p2[0] - p1[0])
        pXIntercept = -1 * (pSlope * p1[0]) + p1[1]
        
        # make and use linear equation to solve for the point of intersection 
        poi[0] = q1[0]
        poi[1] = (pSlope * poi[0]) + pXIntercept
        
    # if neither are vertical
    else:
        # slope of each line
        pSlope = (p2[1] - p1[1])/(p2[0] - p1[0])
        qSlope = (q2[1] - q1[1])/(q2[0] - q1[0])
    
        # if the lines are parallel there is no intersection
        if(pSlope == qSlope): return None
    
        # x intercept of each line
        pXIntercept = -1 * (pSlope * p1[0]) + p1[1]
        qXIntercept = -1 * (qSlope * q1[0]) + q1[1]
        
        # solve the linear system
        poi[0] = (qXIntercept - pXIntercept)/(pSlope - qSlope)
        poi[1] = (qSlope * poi[0]) + qXIntercept
        
    # if the POI exists on both lines
    # return it
    # otherwise return None   
    return poi if (poi[0] >= p1[0] and poi[0] <= p2[0] and poi[0] >= q1[0] and poi[0] <= q2[0]) else None