from setuptools import setup
try:
    from pypandoc import convert_file
    read_md = lambda f: convert_file(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
  name = 'LZGraphs',
  packages = ['LZGraphs'],
  version = '0.26',
  license='MIT',
  description='An Implementation of LZ76 Based Graphs for Repertoire Representation',
  long_description_content_type="text/markdown",
  long_description=read_md('README.md'),
  author = 'Thomas Konstantinovsky',
  author_email = 'thomaskon90@gmail.com',
  url='https://github.com/MuteJester/LZGraphs',
  download_url='https://github.com/MuteJester/LZGraphs/archive/refs/tags/V2.6.tar.gz',
    keywords=[
        'Graph Theory',
        'Immunology',
        'Bioinformatics',
        'TCRB Repertoire',
        'CDR3 Sequences',
        'LZGraph',
        'Lempel-Ziv 76 Algorithm',
        'K1000 Diversity Index',
        'LZCentrality',
        'Sequence Analysis',
        'Python',
        'Adaptive Immune Receptor Repertoires',
        'Sequence Encoding',
        'Data Compression'
    ],   # Keywords that define your package best
    install_requires=[
        'tqdm',
        'numpy==1.21.5',
        'pandas==1.3.5',
        'networkx==2.8.4',
        'matplotlib==3.5.1',
        'seaborn==0.12.1'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Natural Language :: English'
    ],
)
