all: patchelf.cc elf.h
	g++ -O3 patchelf.cc -o patchelf -DPACKAGE_STRING=\"0.7\"

clean:
	rm -f patchelf

.PHONY: all clean

