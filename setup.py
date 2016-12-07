import cx_Freeze
from setuptools import setup

executables = [cx_Freeze.Executable("BrincandoComMatematica.py")]

cx_Freeze.setup(
    name="BrincandoComMatematica",
    options={"build_exe": {"packages":["pygame"],
                           "packages":["random"],
                           "packages":["sys"],
                           "packages":["copy"],
                           "packages":["os"],
                           "packages":["serial"],
                           "packages":["threading"],
                           "include_files":["ReadAndWrite.ino/ReadAndWrite.ino.ino"],
                           "include_files":["resources/sounds/"],
                           "include_files":["resources/images/"]}},
    executables = executables
    )
