from setuptools import setup

setup(
    name='mdrpa',
    version='1.0',
    packages=['', 'utils'],
    package_data={'': ['*.robot'], 'utils': ['*.robot']},
    install_requires=['robotframework>=4.0.0,<=6.1'],
)
