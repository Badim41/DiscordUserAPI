from setuptools import setup, find_packages

setup(
    name='discord_tools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'Pillow==10.3.0',
        'g4f==0.3.2.2',
        'openai==1.10.0',
        'selenium==4.16.0',
        'webdriver-manager==4.0.1',
        'beautifulsoup4==4.12.2',
        'characterai==0.8.0',
        'mtranslate==1.8',
        'websockets',
        'cohere==5.2.6',
        'gradio_client',
        'svgwrite',
        'cairosvg',
        'fake_useragent',
        'pydub==0.25.1',
        'yt_dlp==2023.7.6',
        'PyExecJS'
    ],
)
