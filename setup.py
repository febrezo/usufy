from distutils.core import setup
import os

# Depending on the place in which the project is going to be upgraded
#from setuptools import setup
try:
	from pypandoc import convert
	read_md = lambda f: convert(f, 'rst')
except ImportError:
	print("warning: pypandoc module not found, could not convert Markdown to RST")
	read_md = lambda f: open(f, 'r').read()

setup(	name="Usufy",
	version="v1.1.0",
	description="usufy.py - Piece of software to check the existence of a given profile in different platforms.",
	author="Felix Brezo and Yaiza Rubio",
	author_email="contacto@i3visio.com",
	url="http://github.com/i3visio/usufy",
	license="COPYING",
	packages=["usufy", "usufy.wrappers"],
	scripts=["bin/_template.py", "bin/classgenerator.py"],
	long_description=read_md("README.md"),
#	long_description=open('README.md').read(),
#	install_requires=[
# 	"any >= 1.1.1",
#	],
)

