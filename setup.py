from distutils.core import setup


setup(
    name="voeventhandler",
    author="Antonio Addis, Luca Babboni",
    version="2.0.0",
    packages=['voeventhandler/', 'voeventhandler/extractors/' ,'voeventhandler/utilis', 'voeventhandler/test'],
    data_files=[('voevent_handler_config', ['./config.json'])],
    license='GPL-3.0'
)
