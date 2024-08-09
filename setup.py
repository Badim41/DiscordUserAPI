from setuptools import setup, find_packages

setup(
    name='DiscordUserAPI',
    version='0.101',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'websockets',
        'aiohttp',
        'aiohttp-socks'
    ],
)