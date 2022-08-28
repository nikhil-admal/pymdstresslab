PyMDStressLab
=============

Python bindings for MDStressLab++. This repository contains the python module which will use libMDStressLab++ as a backend to compute continuous stress fields from MD trajectories.

Current dependencies
- KIM-API > 2.2
- Pybind11

Installation:
Currently it can be installed as a editable python module. It requires a functioning pybind11 installation on the system to compile, and at present need `libMDStressLab++.so` in its `LD_LIBRARY_PATH` variable. The latter requirement would be self contained in next iteration.

```
source /path/to/python_env
git clone https://github.com/nikhil-admal/pymdstresslab.git
cd pymdstesslab
git submodule init # to be sure that submodules are present
pip install -e .
```

Above shall compile and install PyMDStressLab. In some cases you might need to explicitly copy compiled `libMDStressLab++.so` to `src/pymdstresslab/shared_objects/mdstresslab`. Working on its workaround.
