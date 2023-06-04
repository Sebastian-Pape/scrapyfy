from setuptools import setup


setup(
    name='scrapyfy',
    version='1.0',
    author='sp, ma',
    packages=[
        'scripts',
    ],
    install_requires=[
        'argparse',
        'numpy',
        'matplotlib',
        'scipy',
        'pandas',
        'googletrans',
        'geopandas',
        'flask',
        'scikit-learn',
        'lyricsgenius',
        'tqdm',
    ],
)