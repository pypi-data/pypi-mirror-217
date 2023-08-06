from setuptools import find_packages, setup

VERSION = '0.1.1'

setup(
    name='facteur',
    version=VERSION,
    author='Alexis Bouchez',
    author_email='contact@alexisbouchez.com',
    description='A simple Python package to send emails with Facteur.',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
