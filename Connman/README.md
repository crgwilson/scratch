# Connman

Connman is a network manager designed for embedded devices which handles...

* IP configuration (ethernet / wifi / vpn)
* NTP
* DNS

## Cheatsheet

All the info below has been gathered from the arch wiki page and the connman docs

### Cheatsheet: Commands

| Command | Purpose |
| ------- | ------- |
| `connmanctl` | Command line operations |
| `connmand` | Manage the connman daemon |

### Cheatsheet: Configuration

| Item | Path |
| ---- | ---- |
| Systemd unit | `/lib/systemd/system/connman.service` |
| General settings | `/etc/connman/main.conf` |
| Profile settings | `/var/lib/connman` |

#### main.conf

Do not modify hostname:

```text
[General]
AllowHostnameUpdates=false
```

Prefer ethernet over wifi:

```text
[General]
PreferredTechnologies=ethernet,wifi
```

Do not connect to both ethernet and wifi at the same time:

```text
[General]
SingleConnectedTechnology=true
```

Do not manage virtual interfaces:

```text
NetworkInterfaceBlacklist=vmnet,vboxnet,virbr,ifb,docker,veth
```

#### Further reading: Configuration

* [main.conf docs][mainconf]
* [config format docs][confformat]

### Cheatsheet: Daemon

Default systemd unit:

<!-- markdownlint-disable line-length -->
```text
# /lib/systemd/system/connman.service
[Unit]
Description=Connection service
DefaultDependencies=false
Conflicts=shutdown.target
RequiresMountsFor=/var/lib/connman
After=dbus.service network-pre.target systemd-sysusers.service
Before=network.target multi-user.target shutdown.target
Wants=network.target
Conflicts=systemd-resolved.service

[Service]
Type=dbus
BusName=net.connman
Restart=on-failure
ExecStart=/usr/sbin/connmand -n
StandardOutput=null
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE CAP_NET_RAW CAP_SYS_TIME CAP_SYS_MODULE CAP_SYS_ADMIN
ProtectHome=true
ProtectSystem=full

[Install]
WantedBy=multi-user.target
```
<!-- markdownlint-enable line-length -->

Disable connman DNS proxy:

```text
# /lib/systemd/system/connman.service.d/disable_dns_proxy.conf
[Service]
ExecStart=
ExecStart=/usr/bin/connmand -n --nodnsproxy
```

### Cheatsheet: Wifi

Scan for wifi:

```console
connmanctl scan wifi
```

List networks found by scan:

```console
connmanctl services
```

Connect to an open network:

```console
connmanctl connect wifi_<network id from previous command>
```

Connect to a protected network:

```console
$ connmanctl
connmanctl> agent on
connmanctl> connect wifi_<network id from connmanctl services>
```

Enable wifi:

```console
connmanctl enable wifi
```

Disable wifi:

```console
connmanctl disable wifi
```

Connect to a protected network with a config file

```text
# /var/lib/connman/eduroam.config
[service_eduroam]
Type=wifi
Name=eduroam
EAP=peap
CACertFile=/etc/ssl/certs/certificate.cer
Phase2=MSCHAPV2
Identity=user@foo.edu
AnonymousIdentity=anonymous@foo.edu
Passphrase=password
```

## Further reading

* [Connman site][site]
* [Connman docs][docs]
* [Managing internet connections with ConnMan][article]
* [Arch wiki][arch]
* [Dbus API][dbus]

[site]:https://01.org/connman "https://01.org/connman"
[docs]:https://git.kernel.org/pub/scm/network/connman/connman.git/tree/doc?id=HEAD "https://git.kernel.org/pub/scm/network/connman/connman.git/tree/doc?id=HEAD"
[mainconf]:https://git.kernel.org/pub/scm/network/connman/connman.git/tree/src/main.conf "https://git.kernel.org/pub/scm/network/connman/connman.git/tree/src/main.conf"
[confformat]:https://git.kernel.org/pub/scm/network/connman/connman.git/tree/doc/config-format.txt "https://git.kernel.org/pub/scm/network/connman/connman.git/tree/doc/config-format.txt"
[dbus]:https://git.kernel.org/pub/scm/network/connman/connman.git/tree/doc?id=HEAD "https://git.kernel.org/pub/scm/network/connman/connman.git/tree/doc?id=HEAD"
[article]:https://www.embedded-computing.com/articles/the-connman "https://www.embedded-computing.com/articles/the-connman"
[arch]:https://wiki.archlinux.org/index.php/ConnMan "https://wiki.archlinux.org/index.php/ConnMan"
