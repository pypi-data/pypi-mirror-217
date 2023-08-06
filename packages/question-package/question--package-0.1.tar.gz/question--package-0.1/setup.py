
from setuptools import setup, find_packages

setup(
    name='question--package',
    version='0.1',
    license='MIT',
    author="Patrick Saade",
    author_email='patrick_saade@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
          'scikit-learn',
          'numpy',
      ],

)       