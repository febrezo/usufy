from distutils.core import setup

setup(	name="Usufy",
<<<<<<< HEAD
	version="v1.0.2",
=======
	version="v1.0.1",
>>>>>>> 56d9942364eb8bb47e7386b3f0207566667b33c3
	description="usufy.py - Piece of software to check the existence of a given profile in different platforms.",
	author="Felix Brezo and Yaiza Rubio",
	author_email="contacto@i3visio.com",
	url="http://github.com/i3visio/usufy",
	license="COPYING",
	packages=["usufy", "usufy.wrappers"],
	scripts=["bin/_template.py", "bin/classgenerator.py"],
	long_description=open('README.md').read(),
#	install_requires=[
# 	"any >= 1.1.1",
#	],
)

