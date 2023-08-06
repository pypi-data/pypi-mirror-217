from setuptools import setup, find_packages
import codecs
import os

# build instructions
#  python3 setup.py sdist
# twine upload dist/*

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding='utf-8') as fh:
    LONG_DESCRIPTION = '\n' + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Convert Chinese characters to Taiwanese'
#LONG_DESCRIPTION = 'Taiwanese Hokkien transliterator from Chinese characters.'

# Setting up
setup(
    name="example990420",
    version=VERSION,
    author="Andrei Harbachov",
    author_email="<andrei.harbachov@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_dir={'taibun': 'taibun'},
    package_data={'taibun': ['data/*.json']},
    license='MIT',
    url='https://github.com/andreihar/taibun',
    install_requires=[],
    keywords=['python', 'taiwan', 'taiwanese', 'taigi', 'hokkien', 'romanization', 'transliteration'],
    classifiers=[
        'Topic :: Text Processing :: Linguistic',
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)