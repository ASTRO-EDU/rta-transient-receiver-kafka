from setuptools import setup, find_packages

setup(
    name="voeventhandler",
    author="Antonio Addis, Luca Babboni",
    version="2.0.0",
    packages=find_packages(),
    package_dir={ 'voeventhandler': 'voeventhandler'},
    include_package_data= True,
    license='GPL-3.0'
)
