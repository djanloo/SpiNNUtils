try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from collections import defaultdict
import os

__version__ = None
exec(open("spinn_utilities/_version.py").read())
assert __version__

# Build a list of all project modules, as well as supplementary files
main_package = "spinn_utilities"
data_extensions = {".aplx", ".boot", ".json", ".xml", ".xsd"}
config_extensions = {".cfg", ".template"}
main_package_dir = os.path.join(os.path.dirname(__file__), main_package)
start = len(main_package_dir)
packages = []
package_data = defaultdict(list)
for dirname, dirnames, filenames in os.walk(main_package_dir):
    if '__init__.py' in filenames:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        packages.append(package)
    ext_set = set()
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext in data_extensions:
            ext_set.add(ext)
        if ext in config_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append(filename)
    for ext in ext_set:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        package_data[package].append("*{}".format(ext))
       package_data[package].append("*{}".format(ext))

setup(
    name="SpiNNUtilities",
    version=__version__,
    description="Utility classes and functions for SpiNNaker projects",
    url="https://github.com/SpiNNakerManchester/SpiNNUtilities",
    license="GNU GPLv3.0",
    packages=packages,
    package_data=package_data,
    install_requires=['appdirs',
                      'six']
)
