pkgname=ssidstat
pkgver=20170927
pkgrel=1

source=("setup.py",
        "scripts/ssidstat",
        "scripts/ssidstatd",
        "ssidstat/__init__.py",
        "ssidstat/db.py",
        "ssidstat/ssidstat.py"
        "ssidstatd/__init__.py",
        "ssidstatd/db.py",
        "ssidstatd/daemon.py",
        "ssidstatd/monitor.py",
        "ssidstatd/sysutils.py",
        "ssidstatd/ssidstatd.py")

pkgdesc="Simple per-SSID bandwidth usage monitor"
arch=(i686 x86_64)
license=('GPLv2')

depends=(vnstat python2 python2-pip)
makedepends=('python2-setuptools')

package() {
    python2 setup.py install
}