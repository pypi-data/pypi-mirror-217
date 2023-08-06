from setuptools import setup

setup(
    name='vesninlibrary',
    version='1.1',
    description='',
    license='MIT',
    author='romankuklin',
    author_email='romankuklin26@gmail.com',
    url='',
    packages=['vesninlibrary'],
    install_requires=['h5py', 'datetime',
                      'numpy', 'matplotlib',
                      'dateutil',
                      'scipy', 'pathlib'],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
    python_requires='>=3',
)
