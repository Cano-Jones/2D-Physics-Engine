"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("./Physics_Engine/__init__.py") as fp:
    # pylint: disable=W0122
    exec(fp.read(), VERSION)

setup(
    name="Physics_Engine",
    author="Cano Jones, Alejandro",
    author_email="canojones.alejandro@gmail.com",
    description="Library amied to the creation of simple yet realistic simulations of collisions between particles and line segments.",
    version=VERSION.get("__version__", "0.0.0"),
    packages=find_packages(where=".", exclude=["tests"]),
    include_package_data=True,
    package_data={"Physics_Engine": ["src/Physics_Engine/resources/*"]},
    install_requires=[
        "pygame",
        "numpy",
        "math",
        "sys",
        "itertools",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)