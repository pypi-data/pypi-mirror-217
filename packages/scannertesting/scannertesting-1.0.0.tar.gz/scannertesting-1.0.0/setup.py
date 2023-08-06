from setuptools import setup, find_packages

setup(
    name="scannertesting",
    version= '1.0.0',
    author= 'Hariharan',
    description= 'Testing the pip for cli',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
    ],
    
)