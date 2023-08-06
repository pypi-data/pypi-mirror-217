from setuptools import find_packages,setup
from xesai import version
setup(
    name = 'xesai',
    version = version.version,
    author = 'xes',
    description = '学而思AI库',
    packages = find_packages(),
    install_requires = ["requests"],
    url = 'https://code.xueersi.com'
)