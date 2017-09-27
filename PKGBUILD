pkgname=ssidstat
pkgver=20170927
pkgrel=1

source=('ssidstat:https://github.com/putrasattvika/ssidstat.git')

pkgdesc="Simple per-SSID bandwidth usage monitor"
arch=(i686 x86_64)
license=('GPLv2')

depends=(vnstat python2 python2-pip)
makedepends=('python2-setuptools')

package() {
    cd $srcdir/ssidstat
    python2 setup.py install
}