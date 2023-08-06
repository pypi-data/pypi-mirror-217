
from setuptools import setup, find_packages


setup(
    name='excel-splitter',
    version='0.6',
    license='MIT',
    author="Jason Yearry",
    author_email='jasonyearry@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Guitarman-Waiting-In-The-Sky/excel_splitter',
    keywords=["Excel", "Split", "opensource"],
    install_requires=[
          'openpyxl>=3.0.10',
      ],

)