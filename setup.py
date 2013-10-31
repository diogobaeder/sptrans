from setuptools import setup, find_packages

import sptrans

version = sptrans.release

setup(name='sptrans',
      version=version,
      description="Python library for the SPTrans API. Read the docs here: http://sptrans.readthedocs.org/",
      long_description="""\
""",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Scientific/Engineering :: GIS',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='sptrans api transporte sp',
      author='Diogo Baeder',
      author_email='diogobaeder@yahoo.com.br',
      url='http://sptrans.readthedocs.org/',
      license='BSD 2-clause',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
