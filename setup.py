# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: ascii -*-
import cx_Freeze

executables = [cx_Freeze.Executable("BrincandoComMatematica.py")]

cx_Freeze.setup(
    name="BrincandoComMatematica",
    options={"build_exe": {"packages":["pygame", "random", "sys", "copy", "os", "serial", "threading"],
                           "include_files":['resources/sounds/', 'resources/images/']}},
    executables = executables
    )
