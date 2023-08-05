from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


readme = open('README.md').read()
VERSION = '1.0.2'



setup(
    name='createpassword',
    version=VERSION,
    description='createpassword can automatically create passwords',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    #package info
    packages=find_packages("createpassword"),
    #package_dir={"": "createpassword"},
    #py_modules=[splitext(basename(path))[0] for path in glob('createpassword/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)