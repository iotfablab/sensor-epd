#Install the ea_epd_sensor_values python package to display data from .json file on EPD.

from setuptools import setup

setup(name='ea_epd_sensor_values',
      version='1.01',
      description='Display .json file on Embedded Artists 2.7" EPD',
      url='https://gitlab.ips.biba.uni-bremen.de/iotfablab/ea-epd-sensor-values',
      author='Mikolaj Dobielewski',
      author_email='dob@biba.uni-bremen.de',
      license='Apache License, Version 2.0',
      packages=['ea_epd_sensor_values'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['Pillow'],
      scripts=['ea_epd_sensor_values/bin/EPD_json', 'ea_epd_sensor_values/bin/EPD_button']
      )