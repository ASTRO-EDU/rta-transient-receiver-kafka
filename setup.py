from setuptools import setup, find_packages

setup(
    name="kafkareceiver",
    author="Luca Babboni, Antonio Addis",
    version="1.0.0",
    packages=find_packages(),
    package_dir={ 'kafkareceiver': 'kafkareceiver'},
    include_package_data= True,
    license='GPL-3.0'
)
