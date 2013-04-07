#!/usr/bin/env python
import sys, os

if len(sys.argv) != 3:
	print "Usage: %s elfname tarname" % sys.argv[0]
	print "\telfname: the elf binary file to patch"
	print "\ttarname: the final package name"
	print "\teg: ./packer.py /bin/ls pack"
	sys.exit(-1)

elfname = sys.argv[1]
tarname = sys.argv[2]

tmppath = "TEMP_PATH"
basepath = "./%s/%s" % (tmppath, tarname)

patchelf = "%s/patchelf/patchelf" % os.path.split(os.path.realpath(__file__))[0]
command = r'ldd %s | sort | grep -oE "=> /[^(]*" | grep -oE "/[^(]*"' % elfname
loaderpath = "loader"
libpath = "libs"

print "test"
if not os.path.isfile(patchelf):
	print "You should compile patchelf first!"
	print "You can read README for more information."
	sys.exit(-1)

print "mkdir"
os.system("rm -rf %s" % tmppath)
os.makedirs("%s/%s" % (basepath, loaderpath))
os.makedirs("%s/%s" % (basepath, libpath))

print "cp libs"
path = "%s/%s" % (basepath, libpath)
for lib in os.popen(command).readlines():
	cpcommand = "cp -L %s %s" % (lib.strip(), path)
	os.system(cpcommand)
	print cpcommand

print "cp elffile"
cpcommand = "cp -L %s %s" % (elfname, basepath)
os.system(cpcommand)
print cpcommand

print "modify rpath"
elfonly = elfname[elfname.rindex('/'):]
os.system(r"%s --force-rpath --set-rpath \$ORIGIN/%s %s%s" % (patchelf, libpath, basepath, elfonly))

print "cp loader"
loader = os.popen("%s --print-interpreter %s" % (patchelf, elfname)).read().strip()
os.system("cp -L %s %s/%s" % (loader, basepath, loaderpath))
print "loader:", loader

print "create script"
shname = "%s/%s.sh" % (basepath, elfonly)
os.system(r"echo '#!/bin/sh' > %s" % shname)
os.system(r"echo '`dirname $0`/%s%s `dirname $0`%s $@' >> %s" % (loaderpath, loader[loader.rindex('/'):], elfonly, shname))
os.system("chmod +x %s" % shname)

os.chdir(tmppath)
print "create tar"
os.system("tar czf %s.tar.gz %s" % (tarname, tarname))
os.system("mv %s.tar.gz ../" % tarname)
os.chdir("../")
os.system("rm -rf %s" % tmppath)

print "done"

