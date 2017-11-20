build:
	makepkg -c -f && rm -rf ssidstat-git

build-local:
	zip -r ssidstat-local.zip * && makepkg -p PKGBUILDLOCAL -c -f && rm ssidstat-local.zip

install:
	makepkg -i -c -f && rm -rf ssidstat-git

install-local:
	zip -r ssidstat-local.zip * && makepkg -p PKGBUILDLOCAL -i -c -f && rm ssidstat-local.zip

remove:
	pacman -R ssidstat

clean:
	rm -rf *.pkg.tar.xz ssidstat-local.zip src/ pkg/ ssidstat-git/ && find . -type f | grep -e ".pyc" | xargs rm

test:
	python2 -m unittest discover -s ssidstat/test -p "*_test.py"
