from setuptools import setup, find_packages

setup(
    name='azurly',
    author="Max Snoodijk",
    description='A combined CDK and API package to be used with Microsoft Azure.',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
    ],
)
