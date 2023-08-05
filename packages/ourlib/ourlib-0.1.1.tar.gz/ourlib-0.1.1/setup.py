import setuptools
import re

# Configurations
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     install_requires=['torch','numpy','pandas','scikit-learn'],        # Dependencies
     python_requires='>=3.8',                                           # Minimum Python version
     name='ourlib',                                                     # Package name
     version="0.1.1",                                                      # Version
     author="PT",                                     # Author name
     author_email="name@gmail.com",                           # Author mail
     description="Python package for ourlib.",    # Short package description
     long_description=long_description,                       # Long package description
     long_description_content_type="text/markdown",
     url="https://github.com/kunxl-gg/Mercor-pypi",       # Url to your Git Repo
     packages=setuptools.find_packages(),                     # Searches throughout all dirs for files to include
     include_package_data=True,                               # Must be true to include files depicted in MANIFEST.in
     license_files=["LICENSE"],                               # License file
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     entry_points={
      'console_scripts': [
         'ourlib=ourlib.command_line:main',
      ],
   },
 )