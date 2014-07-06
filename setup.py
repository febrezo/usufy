from distutils.core import setup

setup(	name="Usufy",
	version="v1.0.0",
	description="usufy.py - Piece of software to check the existence of a given profile in different platforms.",
	author="Felix Brezo and Yaiza Rubio",
	author_email="contacto@i3visio.com",
	url="http://www.usufy.com",
	license="COPYING",
	packages=["usufy", "usufy.wrappers"],
	scripts=["bin/_template.py", "bin/classgenerator.py"],
	long_description=open('README').read(),
#	install_requires=[
# 	"any >= 1.1.1",
#	],
)

