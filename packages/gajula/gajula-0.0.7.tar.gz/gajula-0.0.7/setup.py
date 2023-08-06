import setuptools
import pickle

with open("README.md", "r") as fh:
    long_description = fh.read()

version = open('version', 'rb')
ver = pickle.load(version)
version.close()


version = open('version', 'wb')
pickle.dump(ver + 1,version)                     
version.close()

setuptools.setup(
    name="gajula",                     # This is the name of the package
    version=f"0.0.{ver}",                        # The initial release version
    author="Jagadeesh Gajula",                     # Full name of the author
    description="Gajula Package consists of useful utilites and functions",
    long_description="Gajula Package is developed for public use, it contains generic functions and utilities",      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["gajula"],             # Name of the python package
    package_dir={'':'gajula/src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)