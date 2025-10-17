from setuptools import setup, find_packages

setup(
    packages=find_packages(include=['mcp_server*']),
    package_data={'mcp_server': ['examples/*.py']},
)
