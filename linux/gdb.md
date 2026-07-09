---
tags:
  - debugging
  - linux
  - operating-systems
---
# GDB

## Allow core dumps (CentOS)

1. Create a directory `/var/coredumps` with the permission set to `777`
2. Create `/etc/sysctl.d/core.conf` with the following entries:
    * `kernel.core_pattern = /var/coredumps/core-%e-sig%s-user%u-group%g-pid%p-time%t`
    * `kernel.core_uses_pid = 1`
    * `fs.suid_dumpable = 2`
3. Create a directory `/etc/security/limits.d/core.conf` with the following entries:
    * hard core unlimited
    * soft core unlimited
4. Uncomment the entry of `DefaultLimitCORE` in `/etc/systemd/system.conf` and set
   it to infinity (`DefaultLimitCORE=infinity`).
5. Run the command `systemctl daemon-reexec`

If you're not running a `systemd` system then you'll need to add `DAEMON_COREFILE_LIMIT='unlimited'`
into `/etc/sysconfig/init`

NOTE: You may also need to run `ulimit -c unlimited`

## Debugging symbols

Compile something with debugging symbols

```console
# CFLAGS="-g" ./configure
# make
# make install
```

## Cheatsheet

| Command | Description |
| ------- | ----------- |
| `help all` | List all available commands |
| `where` | Print backtrace of stack frames |
| `frame` | Get current stack frame |