from setuptools import setup

setup(
    name='pycal',
    version='0.1.0',
    packages=['pycal'],
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ],
    entry_points={
        'console_scripts': [
            'pycal = pycal.__main__:main'
        ]
    }
)
