#!/bin/sh

if [ $# -lt 2 ]; then
 	echo "Usage: $0 elfname tarname"
 	echo "\telfname: the elf binary file to patch"
 	echo "\ttarname: the final package name"
 	echo "\teg: ./packer.py /bin/ls pack"
	return 1
fi

selfpath=`pwd`
temppath=`mktemp -d`
basepath=${temppath}/$2
patchelfpath=`dirname $0`/patchelf
patchelf=${patchelfpath}/patchelf
loaderpath=${basepath}/loader
libpath=${basepath}/libs
elfonly=`basename $1`

echo "make"
if [ ! -x $patchelf ]; then
	make -C $patchelfpath
fi

echo "mkdir"
mkdir -p ${libpath}
mkdir -p ${loaderpath}

echo "cp elffile"
cp -L $1 $basepath

echo "modify rpath"
${patchelf} --force-rpath --set-rpath \$ORIGIN/libs ${basepath}/${elfonly}

echo "cp libs"
for lib in `ldd $1 | grep -oE "=> /[^(]*" | grep -oE "/[^(]*"`
do
	echo "\t${lib}"
	cp -L $lib $libpath
done

echo "cp loader"
loader=`${patchelf} --print-interpreter $1`
cp -L ${loader} ${loaderpath}
echo "\t${loader}"

echo "create script"
shname="${basepath}/${elfonly}.sh"
echo '#!/bin/sh' > ${shname}
echo '`dirname $0`/loader/'"`basename ${loader}`"' `dirname $0`/'"${elfonly}"' $@' >> ${shname}
chmod +x ${shname}

echo "create tar"
tar czf $2.tar.gz -C $temppath $2
cd ${selfpath}

echo "done"

