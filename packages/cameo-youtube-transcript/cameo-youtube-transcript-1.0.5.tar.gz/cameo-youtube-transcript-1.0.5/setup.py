
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="cameo-youtube-transcript",
    version="1.0.5",
    packages=find_packages(),
    py_modules=['cameo_youtube_transcript'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'cameo_youtube_transcript = cameo_youtube_transcript:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
