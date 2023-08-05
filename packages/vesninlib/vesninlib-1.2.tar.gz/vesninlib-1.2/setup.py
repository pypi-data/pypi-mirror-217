from setuptools import setup

setup(
    name='vesninlib',
    version='1.2',
    description='',
    license='MIT',
    author='nech14',
    author_email='nech14@mail.ru',
    url='',
    packages=['vesninlib'],
    install_requires=['h5py', 'datetime',
                      'numpy', 'matplotlib',
                      'cartopy', 'dateutil',
                      'scipy', 'pathlib'],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
    python_requires='>=3',
)
