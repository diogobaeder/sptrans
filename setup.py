from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='sptrans',
      version=version,
      description="Biblioteca para facilitar o uso da API da SPTrans",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='sptrans api transporte sp',
      author='Diogo Baeder',
      author_email='diogobaeder@yahoo.com.br',
      url='',
      license='BSD 2-clause',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
