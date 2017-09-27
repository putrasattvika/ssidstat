pkgname=ssidstat
pkgver=20170927
pkgrel=1

pkgdesc="Simple per-SSID bandwidth usage monitor"
arch=(i686 x86_64)
license=('GPLv2')

source=('ssidstat-git::git+https://github.com/putrasattvika/ssidstat.git')
sha256sums=('SKIP')

depends=(vnstat python2 python2-pip)
makedepends=('python2-setuptools')

package() {
    cd $srcdir/ssidstat-git
    python2 setup.py install -O1 --root="${pkgdir}" --prefix=/usr

    mkdir -p "$pkgdir"/var/lib/ssidstat
}