from setuptools import setup

requirements = ["requests","aiohttp"]

long_description_b = """

Hello.
This is an open source library for creating self-bots in Rubino in the Rubica program.

You can easily import this library
How to import by sync:
	
from robino import rubinoBot

How to import async:

from robino import async_rubinoBot

You can read our document library in our Telegram channel to learn better.
Library document on Telegram channel:
https://t.me/document_robino

document: https://t.me/document_robino

My Telegram ID: @BeniProgrammer

My projects channel: https://t.me/Hells_team
	
"""

setup(
	name = "robino",
	version = "1.0.2",
	author = "Benyamin karimi",
	author_email = "benkarimi2006@gmail.com",
	description = "Rubino(Rubika) Library self Bot",
	license = "MIT",
	keywords = ['rubika', 'rubino', 'chat', 'bot', 'robot', 'asyncio', 'robino'],
	packages = ["robino"],
	install_requires = requirements,
	long_description = long_description_b,
	classifiers=['Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',],
        )