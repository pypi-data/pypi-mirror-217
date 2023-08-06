from setuptools import setup, find_packages

setup(
    name='GlioMRInter',
    version='1.0',
    url='https://github.com/GlioMRInter/GlioMRInter',
    author='Kacper Stasiełuk',
    author_email='kacperstasieluk@gmail.com',
    description='',
    packages=find_packages(),
    install_requires=[
    'numpy',
    'pandas',
    'scipy',
    'pydicom',
    'opencv-python',
    'sklearn',
    'statsmodels',
    'skfeature',
    'tensorflow',
    'tensorflow-io',
    'Keras',
    'pymrmr',
    'ReliefF',
    'matplotlib',
    'seaborn',
    'matplotlib-venn',
]

)
