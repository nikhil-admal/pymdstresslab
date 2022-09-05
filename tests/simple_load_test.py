from pymdstresslab import pymdstresslab as  pmsl
from pymdstresslab import Box
from pymdstresslab import Grid

body = Box(config_file="config.data")
body.read("config.data")
grid = Grid(grid_type="Current",from_file="grid_cauchy.data")
