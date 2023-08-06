from setuptools import setup, find_namespace_packages
import os.path as osp

current_directory = osp.dirname(osp.realpath(__file__))
filename = osp.join(current_directory, 'README.md')
with open(filename) as file:
    readme = file.read()

filename = osp.join(current_directory, "requirements.txt")
with open(filename) as file:
    requirements = file.read()

setup(
    # name = "plexonNEX5Converter",     # will probably want to change this before deploying for real
    name = "h21ak9_42f821",
    version = "0.1.1",  # right now this is hard coded -- read from src/plexonNEX5Converter/__init__.py
    #license = ??
    description="Placeholder for description",
    # long_description=readme,
    # author="Nikhil Chandra (Plexon)",
    # author_email="nikhil@plexon.com",
    # url="https://www.plexon.com",
    author="h21ak9",
    author_email="h21ak9@gmail.com",
    packages = find_namespace_packages(where="src"),
    package_dir={"":"src"},
    package_data={
        "plexonNEX5Converter.bin": ["*.dll"],
        "": ["*.txt", "*.md"],
    },
    entry_points={"console_scripts": ["nex5conv=plexonNEX5Converter:run"]},
    install_requires=requirements,
)