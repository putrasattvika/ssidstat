# ssidstat [![Build Status](https://travis-ci.org/putrasattvika/ssidstat.svg?branch=master)](https://travis-ci.org/putrasattvika/ssidstat)
Simple per-SSID bandwidth usage monitor

## Requirements
 - python2 && python2-pip
 - iw

## Instalation

Installation is currently only supported for Arch Linux and its derivatives.

- Download the *.pkg.tar.xz file from releases
- `sudo pacman -U ssidstat-w.x.y-z-x86_64.pkg.tar.xz`

## Daemon Usage
- (With systemd) Allow the daemon to auto-start and then start it:
	```
	$ sudo systemctl enable ssidstatd
    $ sudo systemctl start ssidstatd
	```
   
- (Without systemd) Manually:
	```
    $ sudo ssidstatd
    ```

## CLI Utility Usage
- Help
	```
    $ ssidstat --help
    usage: ssidstat [--help] [--version] [--json] [--active] [--db DB]
                    [--ssid SSID] [--hour] [--day] [--week] [--month]

    optional arguments:
      --help                print this fabulous help message
      --version, -v         show ssidstat version
      --json, -j            output as json
      --active, -a          only outputs active connection
      --db DB               database file, default is
                            /var/lib/ssidstat/ssidstatd.db
      --ssid SSID, -s SSID  select one specific SSID. Used in conjuction with -h,
                            -d, -w, or -m
      --hour, -h            show hourly statistics
      --day, -d             show daily statistics
      --week, -w            show weekly statistics
      --month, -m           show monthly statistics
    ```

- Examples
    ```
    $ ssidstat       
    Adapter    SSID      Receive (rx)    Transmit (tx)    Total
    ---------  --------  --------------  ---------------  ----------
    enp2s0     enp2s0    0.00 B          0.00 B           0.00 B
    lo         lo        812.40 KiB      812.40 KiB       1.59 MiB
    wlp3s0     Waaai.fi  226.45 MiB      23.21 MiB        249.66 MiB
    wlp3s0     wlp3s0    0.00 B          0.00 B           0.00 B
    ```
    
    ```
    $ ssidstat --week --ssid "Waaai.fi"       
    Weekly traffic for SSID Waaai.fi

    Date                     Receive (rx)    Transmit (tx)    Total
    -----------------------  --------------  ---------------  ----------
    2017-11-20 ~ 2017-11-26  256.53 MiB      29.22 MiB        285.75 MiB
    2017-11-27 ~ 2017-12-03  26.34 MiB       18.32 MiB        44.66 MiB
    2017-12-04 ~ 2017-12-10  233.49 MiB      66.37 MiB        299.85 MiB
    2017-12-11 ~ 2017-12-17  687.83 MiB      131.57 MiB       819.39 MiB
    2017-12-18 ~ 2017-12-24  642.00 MiB      113.23 MiB       755.24 MiB

    ```