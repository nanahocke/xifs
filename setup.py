
"""Setup xifs."""

from setuptools import setup

setup(name='xifs',
      description='OpenIFS afterburner, post processing tool',
      packages=['xifs'],
      package_dir={'xifs': 'xifs'},
      install_requires=['setuptools', ],
      zip_safe=False
