from pymdstresslab.shared_objects import pymdstresslab as _pmsl_so


def Stress(method, grid, name:str=None, user_defined:bool=False):
    """
    Stress wrapper function, returns stress type Piola with grid type Current
    and stress type Cauchy with grid type Reference.

    :param method: Currently assumes method type is MethodSphere
    :param grid: The grid type to be used for stress evaluation. Kind of grid determines kind of stress class initialized.
    :param name: Optional, name of evaluated stress.

    :returns class of kind Stress Piola or Cauchy.
    """
    grid_type = type(grid).__name__
    if grid_type == "GridCurrent" and not user_defined:
        stress = _pmsl_so.StressCauchy(name, method, grid) if name else \
                 _pmsl_so.StressCauchy(method, grid)
    elif grid_type =="GridReference" and not user_defined:
        stress = _pmsl_so.StressPiola(name, method, grid) if name else \
                 _pmsl_so.StressPiola(method, grid)
    elif grid_type =="GridCurrent" and user_defined:
        stress = _pmsl_so.StressCauchyUser(name, method, grid) if name else \
                 _pmsl_so.StressCauchyUser(method, grid)
    elif grid_type =="GridReference" and user_defined:
        stress = _pmsl_so.StressPiolaUser(name, method, grid) if name else \
                 _pmsl_so.StressPiolaUser(method, grid)
    else:

        raise ValueError(f"Grid type {grid_type} not supported yet.")
    return stress
    
