pkgname=ssidstat
pkgver=$(python2 -c "print __import__('ssidstat').__version__")
pkgrel=1

pkgdesc="Simple per-SSID bandwidth usage monitor"
arch=(i686 x86_64)
license=('Apache')

source=('ssidstat-git::git+https://github.com/putrasattvika/ssidstat.git')
sha256sums=('SKIP')

depends=(python2 python2-pip)
makedepends=('python2-setuptools')

package() {
    cd $srcdir/ssidstat-git
    python2 setup.py install -O1 --root="${pkgdir}" --prefix=/usr
    install -Dm644 "$srcdir/ssidstatd.service" "$pkgdir/usr/lib/systemd/system/ssidstatd.service"

    mkdir -p "$pkgdir"/var/lib/ssidstat
}