from setuptools import setup

setup(
    name='SEVtras',
    version='0.1',
    author='Ruiqiao He',
    author_email='ruiqiaohe@gmail.com',
    packages=['SEVtras'],
    license="GPL",
    url='http://pypi.python.org/pypi/SEVtras/',
    description='sEV-containing droplet identification in scRNA-seq data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "scanpy>=1.6.0",
        "numpy>=1.21.5",
        "pandas>=1.1.2",
        "scipy>=1.5.4",
        "statsmodels>=0.12.1",
        "gseapy",
        # "copy",
        # "sys",
        # "os",
        # "multiprocessing",
        # "pickle>=4.0",
    ],
    python_requires='>=3.7.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'SEVtras=SEVtras.main:SEVtras_command',
        ]
    }
)
