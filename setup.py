from setuptools import setup, find_packages
import os

version = '0.1.2'

setup(name='nsi.multimedia',
      version=version,
      description="Multimedia",
      long_description=open("README").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rodrigo Manhaes / NSI - CEFETCampos',
      author_email='nsi@cefetcampos.br',
      url='http://nsi.iff.edu.br',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['nsi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
