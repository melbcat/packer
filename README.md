packer
======
Packer is a simple python script to pack linux program and needed .so libraries into a single .tar.gz files for distribution.

To use packer, you must have patchelf "https://github.com/NixOS/patchelf" installed in your $PATH.

usage
------
usage: ./packer.py exefile tarpath

example: ./packer.py ~/test pack, 

which will generate pack.tar.gz:

--pack(folder)

----libs(folder, used for rpath)

----linker(folder, used for interpreter)

----test(elf file)

note
------

If the target os has different interpreter with your own os, you should run your program in one of the following ways:

1. cd to the exefile path and run it, e.g. cd pack && ./test
2. use the interpreter explicitly, e.g ./pack/linker/ld-XXXX.so ./pack/test

