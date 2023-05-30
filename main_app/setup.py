from cx_Freeze import setup, Executable
sys.setrecursionlimit(5000)
build_exe_options = {"packages": ["os"], "excludes": []}
setup(
    name="interface",
    version="1.0",
    description="industry 4.0 interface",
    executables=[Executable("main.py")]
)
