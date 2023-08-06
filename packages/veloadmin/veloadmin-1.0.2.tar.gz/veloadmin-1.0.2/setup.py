from setuptools import setup, find_packages

setup(
    name='veloadmin',
    version='1.0.2',
    author='Pawan kumar',
    author_email='control@vvfin.in',
    description='VeloAdmin is tool design to handle veloweb server',
    packages=find_packages(),
    py_modules=['veloadmin'],
    install_requires=[
        "veloweb"
    ],
    entry_points={
        'console_scripts': [
            'velo = veloAdmin.create:main',
        ],
    },
)
