from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

def parse_req(req):
    """WARNING: This depends on each line being structured like ``A==1``
    """
    [package, verion] = req.strip().split('==')
    return package

with open(path.join(here, 'requirements.txt')) as f:
    install_requires = [parse_req(l) for l in f if l.strip()]

setup(
    name='mkpass',
    version='0.0.1',
    description='Generate passwords',
    license='BSD 3-Clause',
    packages=find_packages(exclude=('test*',)),
    install_requires=install_requires,
    scripts=['bin/mkpass'],
)
