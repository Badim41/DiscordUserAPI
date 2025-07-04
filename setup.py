from setuptools import setup, find_packages

setup(
    name='DiscordUserAPI',
    version='0.151',
    packages=find_packages(),
    install_requires=[
        'requests~=2.32.0',
        'websockets',
        'aiohttp-socks',
        'aiohttp==3.8.6',
        'pydub',
        'aiofiles',
        'httpx==0.25.1'
    ],
)