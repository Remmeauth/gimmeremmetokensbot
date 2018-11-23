from setuptools import setup, find_packages

setup(
    name='remme-client',
    version='0.0.1',
    description='Remme Core Client',
    author='REMME',
    url='https://remme.io',
    packages=find_packages(),
    package_data={
        # 'remme.rest_api': ['openapi.yml'],
        # 'remme.settings': ['default_config.toml']
    }, install_requires=['requests', 'aiohttp', 'sawtooth-signing', 'sawtooth-sdk', 'cbor']
)
