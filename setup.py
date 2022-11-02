from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as build_ext_orig
import pathlib
import os
import subprocess
import shutil
from glob import glob



# class CMakeExtension(Extension):
#     """Solution from https://martinopilia.com/posts/2018/09/15/building-python-extension.html"""
#     def __init__(self, name, cmake_lists_dir='.', **kwa):
#         Extension.__init__(self, name, sources=[], **kwa)
#         self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)

# class cmake_build_ext(build_ext_orig):
#     def build_extensions(self):
#         # Ensure that CMake is present and working
#         try:
#             out = subprocess.check_output(['cmake', '--version'])
#         except OSError:
#             raise RuntimeError('Cannot find CMake executable')

#         for ext in self.extensions:
#             extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
#             cfg = 'Release'

#             cmake_args = [
#                 '-DCMAKE_BUILD_TYPE=%s' % cfg,
#                 # containing the extension
#                 '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
#                 '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), self.build_temp),
#                  ]
#             if not os.path.exists(self.build_temp):
#                 os.makedirs(self.build_temp)
#             subprocess.check_call(['cmake', ext.cmake_lists_dir] + cmake_args, cwd=self.build_temp)
#             subprocess.check_call(['cmake', '--build', '.', '--config', cfg], cwd=self.build_temp)


class CMakeExtension(Extension):
    def __init__(self, name):
        Extension.__init__(self, name, sources=[])


class cmake_build_ext(build_ext_orig):
    "adapted from https://gist.github.com/hovren/5b62175731433c741d07ee6f482e2936"
    def run(self):
        print("entered in run")
        build_directory = os.path.abspath(self.build_temp)
        lib_directory = os.path.abspath(self.build_lib)
        print(f"-> {build_directory} {lib_directory}\n")
        cmake_args = [ '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + lib_directory]
        # cmake_args = [build_directory]
        cfg = 'Release'
        build_args = ['--config', cfg]
        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
        self.build_args = build_args
        
        # CMakeLists.txt is in the same directory as this setup.py file
        cmake_list_dir = os.path.abspath(os.path.dirname(__file__))
        
        print("here")
        # Check python env flags for CMAKE
        # PYTHON_LIB  PYTHON_EXEC
        python_lib = os.environ.get("PYTHON_LIB", None)
        python_exec = os.environ.get("PYTHON_EXEC", None)
        if python_lib:
            cmake_args += ['-DPYTHON_LIBRARY=' + python_lib]
        if python_exec:
            cmake_args += ['-DPYTHON_EXECUTABLE=' + python_exec]
        print(f"build_temp::::{self.build_temp}  ::::{build_directory}")
        subprocess.check_call(['cmake', cmake_list_dir] + cmake_args, cwd=lib_directory)#, env=env)
        print("second subprocess call")
        cmake_cmd = ['cmake', '--build', '.'] + self.build_args
        subprocess.check_call(cmake_cmd, cwd=self.build_lib)

        # Move from build temp to final position  
        for ext in self.extensions:
            # if "my_pyth_lib" in ext.name:
            # print(os.listdir(self.build_lib+"/pymdstresslab"))
            in_file_name_mdstress = glob(self.build_lib + "/libMDStressLab++.*")[0]
            out_file_name_mdstress = "/".join(self.get_ext_fullpath(ext.name).split("/")[:-1]) + "/mdstresslab/" + in_file_name_mdstress.split("/")[-1]
            #print(in_file_name_mdstress, out_file_name_mdstress)
            #print(self.build_lib + "/" + self.get_ext_filename(ext.name).split("/")[-1])
            #print("/".join(self.get_ext_fullpath(ext.name).split("/")[2:-1]))
            os.makedirs(self.build_lib + "/" + "/".join(self.get_ext_fullpath(ext.name).split("/")[2:-1]), exist_ok=True)
            os.makedirs(self.build_lib + "/" + "/".join(self.get_ext_fullpath(ext.name).split("/")[2:-1]) + "/mdstresslab", exist_ok=True)
            print(os.listdir(self.build_lib+"/pymdstresslab"))
            print(os.listdir(self.build_lib))
            print("->",  self.build_lib , "/".join(self.get_ext_fullpath(ext.name).split("/")[2:-1]))
            shutil.copy(self.build_lib + "/" + self.get_ext_filename(ext.name).split("/")[-1], self.get_ext_fullpath(ext.name))
            print("copied ext file")
            shutil.copy(in_file_name_mdstress,out_file_name_mdstress)
            # else:
            #     shutil.copy(self.build_temp + "/" + self.get_ext_filename(ext.name).split("/")[-1], self.get_ext_fullpath(ext.name))



mdstresslab_bindings = CMakeExtension(
    "pymdstresslab.shared_objects.pymdstresslab")
    #cmake_lists_dir="./")


setup(
    name="pymdstresslab",
    version="0.0.1",
    author="Nikhil Admal",
    ext_modules=[mdstresslab_bindings],
    cmdclass = {'build_ext': cmake_build_ext},
)
