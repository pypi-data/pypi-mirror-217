from setuptools import setup, find_packages

setup(
    name="stoichiometric",
    version="0.1.2", 
    description="stoichiometric",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pymatgen'],
)
