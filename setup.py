from setuptools import setup, find_packages

setup(
    name='DiscordUserAPI',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests~=2.32.0',
        'websockets',
        'aiohttp-socks>=0.12.0',
        'aiohttp>=3.14.5',
        'pydub',
        'aiofiles',
        'httpx==0.25.1'
    ],
)
