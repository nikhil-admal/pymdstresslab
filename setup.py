from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as build_ext_orig
import pathlib
import os
import subprocess
import shutil

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
        build_directory = os.path.abspath(self.build_temp)
        # cmake_args = [ '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + build_directory]
        cmake_args = [build_directory]
        cfg = 'Release'
        build_args = ['--config', cfg]
        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
        self.build_args = build_args
        # CMakeLists.txt is in the same directory as this setup.py file
        cmake_list_dir = os.path.abspath(os.path.dirname(__file__))
        subprocess.check_call(['cmake', cmake_list_dir] + cmake_args, cwd=self.build_temp)#, env=env)
        cmake_cmd = ['cmake', '--build', '.'] + self.build_args
        subprocess.check_call(cmake_cmd, cwd=self.build_temp)

        # Move from build temp to final position  
        for ext in self.extensions:
            # if "my_pyth_lib" in ext.name:
            print(os.listdir(self.build_temp))
            shutil.copy(self.build_temp + "/" + self.get_ext_filename(ext.name).split("/")[-1], self.get_ext_fullpath(ext.name))
            shutil.copy(self.build_temp + "/mdstresslab/libMDStressLab++.so", "/".join(self.get_ext_fullpath(ext.name).split("/")[:-1]) + "/mdstresslab/libMDStressLab++.so")
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
