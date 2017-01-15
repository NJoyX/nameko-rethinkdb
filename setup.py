from setuptools import setup, find_packages

setup(
    name='nameko-rethinkdb',
    version='0.1-beta',
    description='@TODO',
    long_description='@TODO',
    author='Fill Q',
    author_email='fill@njoyx.net',
    url='https://github.com/NJoyX/nameko-rethinkdb',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    install_requires=[
        "nameko",
        "rethinkdb"
    ],
    include_package_data=True,
    zip_safe=True,
    keywords=['nameko', 'rethinkdb', 'database'],
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
