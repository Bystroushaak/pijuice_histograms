from setuptools import setup
from setuptools import find_packages

setup(
    name='pijuice_histograms',
    version='0.0.1',
    url='',
    license='MIT',
    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',
    description='Histograms created from pijuice data.',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=['scripts/pijuice_histograms_logger'],
)
