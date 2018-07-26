from cx_Freeze import setup, Executable

target = Executable(
    script="mainSP.py",
    base="Win32GUI",
    )

setup(
    name="SP",
    version="1.0",
    description="for spare parts",
    author="Peter Yanush",
    executables=[target]
    )