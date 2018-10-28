#pylint: disable=C0111
from setuptools import setup

DESCRIPITON = (
    'Game of TicTacToe with a Neural network'
    ' that auto-leanrs how to play from zero')


def readme():
    with open('README.md') as _file:
        return _file.read()


setup(
    name="alvieja",
    version="0.2",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Artificial Inteligence :: Neural Network',
        'Programming Language :: Python :: 3',
    ],
    description=DESCRIPITON,
    long_description=readme(),
    author='Wolfang Torres',
    author_email='wolfang.torres@gmail.com',
    license='MIT',
    packages=['alvieja'],
    install_requires=['numpy', 'click'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'alvieja = alvieja.main:cli',
        ],
    },
)
