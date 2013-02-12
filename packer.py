#!/bin/python
import sys, os

if len(sys.argv) != 3:
	print "usage: %s exefile tarpath" % sys.argv[0]
	sys.exit(-1)

exefile = sys.argv[1]
tarpath = sys.argv[2]

patchelf = "patchelf"
basepath = "./%s" % tarpath
command = r'ldd %s | sort | grep -oE "=> /[^(]*" | grep -oE "/[^(]*"' % exefile
linkerpath = "linker"
libpath = "libs"

print "mkdir"
os.system("rm -rf %s" % basepath)
os.makedirs("%s/%s" % (basepath, linkerpath))
os.makedirs("%s/%s" % (basepath, libpath))
path = "%s/%s" % (basepath, libpath)

for lib in os.popen(command).readlines():
	cpcommand = "cp -L %s %s" % (lib.strip(), path)
	os.system(cpcommand)
	print cpcommand

print "cp exefileram"
os.system("cp -L %s %s" % (exefile, basepath))
newexefile = "%s%s" % (basepath, exefile[exefile.rindex('/'):])

print "modify rpath"
os.system("%s --force-rpath --set-rpath ./%s %s" % (patchelf, libpath, newexefile))

linker = os.popen("%s --print-interpreter %s" % (patchelf, exefile)).read().strip()
os.system("cp -L %s %s/%s" % (linker, basepath, linkerpath))
print "linker:", linker

os.chdir(basepath)
print "modify linker"
newlinker = "./%s%s" % (linkerpath, linker[linker.rindex('/'):])
os.system("%s --set-interpreter %s .%s" % (patchelf, newlinker, newexefile))

os.chdir("../")
print "create tar"
os.system("tar czf %s.tar.gz %s" % (tarpath, tarpath))
os.system("rm -rf %s" % tarpath)

print "done"

