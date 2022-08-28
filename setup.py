from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as build_ext_orig
import pathlib
import os
import subprocess

class CMakeExtension(Extension):
    """Solution from https://martinopilia.com/posts/2018/09/15/building-python-extension.html"""
    def __init__(self, name, cmake_lists_dir='.', **kwa):
        Extension.__init__(self, name, sources=[], **kwa)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)

class cmake_build_ext(build_ext_orig):
    def build_extensions(self):
        # Ensure that CMake is present and working
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        for ext in self.extensions:
            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
            cfg = 'Release'

            cmake_args = [
                '-DCMAKE_BUILD_TYPE=%s' % cfg,
                # containing the extension
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), self.build_temp),
                 ]
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)
            subprocess.check_call(['cmake', ext.cmake_lists_dir] + cmake_args, cwd=self.build_temp)
            subprocess.check_call(['cmake', '--build', '.', '--config', cfg], cwd=self.build_temp)


mdstresslab_bindings = CMakeExtension(
    "pymdstresslab.shared_objects.pymdstresslab",
    cmake_lists_dir="./")


setup(
    name="pymdstresslab",
    version="0.0.1",
    author="Nikhil Admal",
    ext_modules=[mdstresslab_bindings],
    cmdclass = {'build_ext': cmake_build_ext},
    package_data = {"pymdstresslab":['./build/mdstresslab/*.so' ,'pymdstresslab/shared_objects/mdstresslab/*.so']}
)
