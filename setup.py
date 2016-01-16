from setuptools import setup

import versioneer


setup(
    name='sphinxformat',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A compact and provably secure mix format',
    url='https://github.com/felipedau/sphinxformat',
    author='Felipe Dau',
    author_email='dau.felipe@gmail.com',
    license='LGPLv3',
    keywords='sphinx mix packet format',
    packages=['sphinxformat'],
    install_requires=[
        'curve25519-donna>=1.3',
        'pycrypto>=2.6.1',
    ]
)
