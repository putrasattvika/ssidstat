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
