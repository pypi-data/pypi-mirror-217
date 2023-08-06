from setuptools import setup, find_packages

setup(
    name='modelDrivenRpa',
    version='1.2',
    packages=find_packages(),
    package_data={'modelDrivenRpa': ['*.robot', 'utils/*.robot']},
)
