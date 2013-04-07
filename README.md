packer
======
Packer is a simple python script to pack a linux program and all needed .so libraries into a single .tar.gz files for easy distribution.

usage
------
Before you run the python script, you need to compile patchelf "https://github.com/NixOS/patchelf" first. Just chdir into the patchelf folder and use "make" to compile it.

usage: ./packer.py elfname tarname
	elfname: the elf binary file to patch
	tarname: the final package name
	eg: ./packer.py /bin/ls pack

which will generate pack.tar.gz:

--pack(folder)

----libs(folder, used for rpath)

----loader(folder, used for interpreter)

----pack.sh(script to run with the original interpreter)

----pack(elf file)

If the target system have the same interpreter with the host system, you can run the elf file 'pack' directly. If not, you can use 'pack.sh' to force to use the original interpreter to load the program. If you are not sure about this, you can always use 'pack.sh'. When you use 'pack.sh', all the args will be passed to the real program 'pack'.

