# dbus-python

[dbus-python][dbus-python] provides bindings to interact with dbus on linux systems.

## dbus-python: Connecting

You can connect to the main system bus or an individual session using either the
`SystemBus()` or `SessionBus()` respectively.

```python
import dbus

system_bus = dbus.SystemBus()
session_bus = dbus.SessionBus()
```

## dbus-python: Listing all services

Calling `list_names()` on an instance of a bus will give you a list of every
service listening on dbus

```python
import dbus

system_bus = dbus.SystemBus()
for service in system_bus.list_names():
    print(service)
```

## dbus-python: Fetching objects

You can access objects from various services by calling `get_object()` on a bus
instance. This method expects...

1. The name of the service
1. The path to the object

```python
import dbus

system_bus = dbus.SystemBus()
system.get_object("org.ganesha.nfsd", "/org/ganesha/nfsd/ExportMgr")
```

## dbus-python: Calling methods

Once you have an instance of your object all DBUS methods will be accessible on it.
You can call them so long as you also pass in the dbus interface name

Snippet from docs...

```python
import dbus
bus = dbus.SystemBus()
eth0 = bus.get_object(
    'org.freedesktop.NetworkManager',
    '/org/freedesktop/NetworkManager/Devices/eth0'
)
props = eth0.getProperties(dbus_interface='org.freedesktop.NetworkManager.Devices')
# props is a tuple of properties, the first of which is the object path
```

...or...

```python
import dbus
bus = dbus.SystemBus()
eth0 = bus.get_object(
    'org.freedesktop.NetworkManager',
    '/org/freedesktop/NetworkManager/Devices/eth0'
)
eth0_dev_iface = dbus.Interface(eth0, dbus_interface='org.freedesktop.NetworkManager.Devices')
props = eth0_dev_iface.getProperties()
# props is the same as before
```

## dbus-python: Debugging

### Cannot autolaunch dbus without $DISPLAY

Run `dbus-launch` before running your script
(note: this mostly happens when using a session bus)

```bash
#!/bin/bash

export $(dbus-launch)
```

## dbus-python: Examples

* [Async client][example_client]
* [Async service using classes][example_service]

[dbus-python]:https://dbus.freedesktop.org/doc/dbus-python/index.html "https://dbus.freedesktop.org/doc/dbus-python/index.html"
[example_client]:https://github.com/freedesktop/dbus-python/blob/master/examples/example-async-client.py "https://github.com/freedesktop/dbus-python/blob/master/examples/example-async-client.py"
[example_service]:https://github.com/freedesktop/dbus-python/blob/master/examples/example-service.py "https://github.com/freedesktop/dbus-python/blob/master/examples/example-service.py"
