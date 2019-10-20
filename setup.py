from setuptools import setup

setup(
    name='pycal',
    version='0.1.0',
    packages=['pycal'],
    entry_points={
        'console_scripts': [
            'pycal = pycal.__main__:main'
        ]
    }
)
