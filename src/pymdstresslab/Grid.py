import numpy as np
from pymdstresslab.shared_objects import pymdstresslab as _pmsl_so

def Grid(grid_type:str, 
         from_file:str=None, 
         lower_limit:np.ndarray=None,
         upper_limit:np.ndarray=None,  
         x:int=None, 
         y:int=1, 
         z:int=1, 
         ngrid:int=None):
    """
    Defines the grid kind to be returned. Based on the kind of class asked for, it initializes and return appropriate class.

    :param grid_type: Type of grid to initialize, accepts "Current" or "Reference"
    :param from_file: Initialize grid from file 
    :param lower_limit: lower limit for grid vector
    :param upper_limit: upper limit for grid vector
    :param x: ngrid x
    :param y: ngrid y [:default = 1]
    :param z: ngrid z [:default = 1]
    :param ngrid: x * y * z
    """

    if grid_type.lower() == "current":
        if from_file:
            return _pmsl_so.GridCurrent(from_file)
        elif lower_limit and upper_limit and x:
            return _pmsl_so.GridCurrent(lower_limit, upper_limit, x, y, z)
        elif ngrid:
            return _pmsl_so.GridCurrent(ngrid)
        else:
            raise ValueError("Improper or conflicting arguments provided.")
    
    elif grid_type.lower() == "reference":
        if from_file:
            return _pmsl_so.GridReference(from_file)
        elif lower_limit and upper_limit and x:
            return _pmsl_so.GridReference(lower_limit, upper_limit, x, y, z)
        elif ngrid:
            return _pmsl_so.GridReference(ngrid)
        else:
            raise ValueError("Improper or conflicting arguments provided.")
    else:
        raise ValueError("grid_type can only take values Current or Reference")
