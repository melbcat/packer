packer
======
Packer is a simple bash script to pack a linux program and all needed .so libraries into a single .tar.gz files for easy distribution.

usage
------
usage: ./packer.sh elfname tarname
	elfname: the elf binary file to patch
	tarname: the final package name
	eg: ./packer.sh /bin/ls pack

which will generate pack.tar.gz:

--pack(folder)

----libs(folder, used for rpath)

----loader(folder, used for interpreter)

----pack.sh(script to run with the original interpreter)

----pack(elf file)

If the target system have the same interpreter with the host system, you can run the elf file 'pack' directly. If not, you can use 'pack.sh' to force to use the original interpreter to load the program. If you are not sure about this, you can always use 'pack.sh'. When you use 'pack.sh', all the args will be passed to the real program 'pack'.

