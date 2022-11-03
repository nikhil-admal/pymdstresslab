PyMDStressLab
=============

Python bindings for MDStressLab++. This repository contains the python module which will use libMDStressLab++ as a backend to compute continuous stress fields from MD trajectories.

## Current dependencies
- KIM-API > 2.2
- Pybind11

## Installation:
Easiest way to run pymdstresslab right now is to use [KIM Developer Platform](https://github.com/openkim/developer-platform). 

Steps:
```shell
# 1. Clone the source code
git clone https://github.com/nikhil-admal/pymdstresslab.git

# 2. Initialize the submodules
cd pymdstresslab
git submodule init # to be sure that submodules are present
git submodule update

# 3. Launch KIM Developer Docker image
docker run -it --name mdstress_dev --mount type=bind,source=/full/path/to/pymdstresslab,target=/home/openkim/pymdstresslab ghcr.io/openkim/developer-platform /bin/bash

# 4. This should launch a new prompt, within docker image:
# Update pip, for some reason pip < 22.0 fails
openkim@xxxxxx$ sudo pip install --upgrade pip

# 5. Change directory to pymdstresslab and install
openkim@xxxxxx$ cd ~/pymdstresslab
openkim@xxxxxx$ pip install .

# 6. Test the installation
#    a. Install KIM model
openkim@xxxxxx$ kimitems install SW_StillingerWeber_1985_Si__MO_405512056662_006

#    b. Change to tests directory
cd tests
python testSW.py
```
You should now see a successful run.


## Old Installation:
Currently it can be installed as a editable python module. It requires a functioning pybind11 installation on the system to compile, and at present need `libMDStressLab++.so` in its `LD_LIBRARY_PATH` variable. The latter requirement would be self contained in next iteration.

```
source /path/to/python_env
git clone https://github.com/nikhil-admal/pymdstresslab.git
cd pymdstresslab
git submodule init # to be sure that submodules are present
pip install -e .
```

Above shall compile and install PyMDStressLab. In some cases you might need to explicitly copy compiled `libMDStressLab++.so` to `src/pymdstresslab/shared_objects/mdstresslab`. Working on its workaround.
