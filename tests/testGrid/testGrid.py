import pymdstresslab as pmsl
import numpy as np

lowerLimit = np.array([1.,2.,3.])
upperLimit = np.array([2.,4.,6.])

ngrid = 10

grid1 = pmsl.Grid("Reference",
        lower_limit=lowerLimit, 
        upper_limit=upperLimit, 
        x=ngrid, y=ngrid, z=ngrid)


with open("random.dat", "w") as f:
    f.write(f"{ngrid}\n")
    for position in grid1.coordinates:
        f.write("\n".join([str(c) for c in position]) + "\n")
