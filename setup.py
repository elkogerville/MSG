import setuptools

setuptools.setup(
     name = "MSGpy",
     version = "0.1.0",
     author = "Elko Gerville-Reache",
     author_email = "elko.gerville-reache@yale.edu",
     license='MIT',
     description = "python program that simulates the interaction of merging galaxies using restricted N-Body calculations",
     packages = ["MSGpy"],
     install_requires=['numpy','matplotlib','random']
)
