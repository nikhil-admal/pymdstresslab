from turtle import up
import pymdstresslab as pmsl
import numpy as np

# -------------------------------------------------------------------
# Input configuration and potential
# -------------------------------------------------------------------

modelname= "SW_StillingerWeber_1985_Si__MO_405512056662_005"
configFileName= "config.data"
referenceAndFinal= True

n_particle = 8000 #TODO: read from file

body = pmsl.Box(config_file="config.data")

kim = pmsl.Kim(modelname)

# -------------------------------------------------------------------
# Create grid
# -------------------------------------------------------------------

n_grid = 5
lower_vec = np.array([0., 0., 0.])
upper_vec = np.array([60., 60., 60.])

randomGrid = pmsl.Grid("Current",lower_limit=lower_vec, upper_limit=upper_vec,x=n_grid, y=n_grid, z=n_grid)
referenceRandomGrid = pmsl.Grid("Reference",lower_limit=lower_vec, upper_limit=upper_vec,x=n_grid, y=n_grid, z=n_grid)

n_grid = 3
referenceGrid = pmsl.Grid("Reference",lower_limit=lower_vec, upper_limit=upper_vec,x=n_grid, y=n_grid, z=n_grid)
gridFromFile = pmsl.Grid("Current", from_file="grid_cauchy.data")

# -------------------------------------------------------------------
# Calculate stress on the grid
# -------------------------------------------------------------------

hardy1 = pmsl.MethodSphere(5.29216036151419,"hardy")
hardyStress1 = pmsl.Stress(hardy1, gridFromFile, name="hardy1")

hardy2 = pmsl.MethodSphere(20.0,"hardy")
hardyStress2 = pmsl.Stress(hardy2, gridFromFile, name="hardy2")

hardy3 = pmsl.MethodSphere(5.0,"hardy")
hardyStress3 = pmsl.Stress(hardy3, referenceGrid, name="hardy3")

hardy4 = pmsl.MethodSphere(7.0,"hardy")
hardyStress4 = pmsl.Stress(hardy4, referenceGrid, name="hardy4")

hardyRandom = pmsl.MethodSphere(9.0,"hardy")
hardyStressRandomCauchy = pmsl.Stress(hardyRandom, randomGrid, name="hardyRandomCauchy")
hardyStressRandomPiola = pmsl.Stress(hardyRandom, referenceRandomGrid, name="hardyRandomPiola")

# Calculate only  Piola
pmsl.calculateStress(body, kim, tuple([hardyStressRandomCauchy]))

# Calculate only Cauchy
pmsl.calculateStress(body, kim, tuple([hardyStressRandomPiola]))

# # Calculate none # Not working
# pmsl.calculateStress(body, kim,tuple([]))

# Calculate all
pmsl.calculateStress(body, kim, tuple([hardyStress3,hardyStress4]))
pmsl.calculateStress(body, kim, tuple([hardyStress2]))

# alternate?
pmsl.calculateStress(body, kim, hardyStressRandomCauchy)
# calculate be a part of Stress class?


hardyStress1.write();
hardyStress2.write();
hardyStress3.write();
hardyStress4.write();
hardyStressRandomPiola.write();
hardyStressRandomCauchy.write();
