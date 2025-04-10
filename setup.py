from setuptools import setup, find_packages

setup(
    name='DiscordUserAPI',
    version='0.12',
    packages=find_packages(),
    install_requires=[
        'requests~=2.32.0',
        'websockets',
        'aiohttp==3.8.6',
        'aiohttp-socks',
        'pydub',
        'aiofiles'
    ],
)