from setuptools import setup, find_packages

setup(
    name='DiscordUserAPI',
    version='0.13',
    packages=find_packages(),
    install_requires=[
        'requests~=2.32.0',
        'websockets',
        'aiohttp-socks',
        'pydub',
        'aiofiles',
        'httpx'
    ],
)