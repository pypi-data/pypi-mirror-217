from setuptools import setup, find_packages

setup(
    name='modelDrivenRpa',
    version='1.1',
    packages=find_packages(),
    package_data={'model_driven_rpa': ['*.robot'], 'model_driven_rpa.utils': ['*.robot']},
)
