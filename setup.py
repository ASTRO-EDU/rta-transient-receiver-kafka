from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
        'kafkareceiver = kafkareceiver.KafkaReceiver:main',
    ]
} 

setup(
    name="kafkareceiver",
    author="Antonio Addis, Luca Babboni, Leonardo Baroncelli <leonardo.baroncelli@inaf.it>",
    version="2.0.0",
    packages=find_packages(),
    entry_points=entry_points,
    package_dir={ 'kafkareceiver': 'kafkareceiver'},
    include_package_data= True,
    license='GPL-3.0'
)
