from pymdstresslab.shared_objects import pymdstresslab as _pmsl_so


def Stress(method, grid, name:str=None):
    """
    Stress wrapper function, returns stress type Piola with grid type Current
    and stress type Cauchy with grid type Reference.

    :param method: Currently assumes method type is MethodSphere
    :param grid: The grid type to be used for stress evaluation. Kind of grid determines kind of stress class initialized.
    :param name: Optional, name of evaluated stress.

    :returns class of kind Stress Piola or Cauchy.
    """
    grid_type = type(grid).__name__
    if grid_type == "GridCurrent":
        stress = _pmsl_so.StressCauchy(name, method, grid) if name else \
                 _pmsl_so.StressCauchy(method, grid)
    elif grid_type =="GrigReference":
        stress = _pmsl_so.StressPiola(name, method, grid) if name else \
                 _pmsl_so.StressPiola(method, grid)
    else:
        raise ValueError("Grid type not supported yet.")
    return stress
    
