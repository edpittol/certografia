import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='certografia',
    version='0.1b',
    packages=['certografia'],
    include_package_data = True,
    license='GPL', 
    description='Spell checker for Portuguese language.',
    long_description=README,
    url='http://edpittol.github.io',
    author='Eduardo Pittol',
    author_email='edpittol@gmail.com',
    install_requires=[
        "elementTree == 1.2.6-20050316",
        "hunspell == 0.1",
        "numpy == 1.7.1",
        "PyYAML == 3.10",
        "nltk == 2.0.4",
        "sqlalchemy == 0.8.3",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing'
    ],
)