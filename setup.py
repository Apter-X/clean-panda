from pathlib import Path

from setuptools import find_packages, setup

long_description = Path('README.md').read_text(encoding='utf-8')

setup(
    name='clean-panda',
    packages=find_packages(include=['clean_panda']),
    version='0.1.3',
    description='Data cleaner based on pandas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Iliass Raihani',
    url='https://github.com/Apter-X/clean-panda',
    license='MIT',
    python_requires='>=3.7',
    install_requires=['pandas', 'numpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=['pytest'],
    test_suite='tests',
)
