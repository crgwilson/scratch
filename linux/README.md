# Linux

Notes about Penguins

## Overview

### The GNU project

GNU is a collection of free software which make up the whole operating system
which one would refer to as "Linux"

The GNU project has worked since 1984 to put together a full OS comprised of entirely
free software.

### What is Linux, how does it differ from GNU?

"Linux" does not actually refer to the entire operating system (despite how the
term is used today).

The term "Linux" actually refers to the Linux Kernel alone. The kernel is typically
packaged with GNU software to make up a complete operating system distribution
(ie: debian, rhel, etc). This should actually be referred to as "GNU/Linux".

### What is POSIX?

POSIX stands for "Portable Operating System Interface" and is a collection of
standards defined by the IEEE Computer Society.

POSIX defines the application programming interface along with command line
shells, utility interfaces, etc in the hope of maintaining compatibility between
different flavors of Unix and other operating systems.

### What is the standard c library?

`libc` is the most basic c library and is crucial for the operation of any system.

### What is the Linux Kernel?

The Linux Kernel is the core of the GNU/Linux operating system which facilitates
access between the software and hardware components of a system.

### What is ELF?

Binaries in an executable and linkable format

### What does the Linux Kernel do?

The Linux Kernel is responsible for things such as...

* Process scheduling (including creation and termination)
* Memory management
* File system provisioning
* Access to connected hardware devices (NICs, peripherals, etc)
* Handling of system calls

### What is LD_LIBRARY_PATH?

`LD_LIBRARY_PATH` is an environment variable in linux which is a colon-separated
list of directories which should be searched when looking for specific libraries.

ie: It's basically `PATH` but for your shared libs instead of your bins

### What is sysctl and how is it used?

`sysctl` is a command line utility which can be used to read and modify various
attributes of the system kernel (kernel parameters).

These values can be found within `/proc/sys`, or configured via `/etc/sysctl.conf`
or `/etc/sysctl.d/*.conf`

Examples of something which can be modified via sysctl includes...

* Enabling or disabling of IPv6
* Swappiness

## Booting

### The Linux boot process

High level steps...

1. System startup / BIOS
2. Master boot record (MBR) in the first sector of the boot device
3. Grub Loads kernel and initramfs into memory
4. Kernel initializes hardware for which it has a driver for within the initramfs
5. Kernel runs `/sbin/init` (which is a symlink to `/lib/systemd/systemd`)
6. Systemd executes `initrd.target` (mounting the rootfs onto `/sysroot`)
7. Rootfs is switched from `/sysroot` to `/`
8. Systemd looks for `default.target` (which is the run level we want to go to)
9. Systemd starts / stops all units concurrently

### What is BIOS, and what does it do?

The BIOS is a firmware program that performs a very basic level of interaction
with the hardware. It is the first program that takes control when the computer
is powered on, and performs a test on all hardware components and peripherals
(called POST or Power on self test). It initializes all hardware necessary
for booting.

After POST is successful the BIOS will look for a boot device from a list of
devices. The BIOS selects a device from this list and check for the boot sector
on the bootable device. The boot sector is the first physical sector on the storage
device and contains the code required for booting the machine.

### What is the MBR?

The MBR consists of 512 bytes at the first sector of a given hard drive.
It is important to note that the MBR is not inside any partition. The MBR
precedes the first partition.

The MBR is split into 3 chunks...

* The first 446 bytes of the MBR contain bootable code
* The next 64 bytes contain partition info for (at most) 4 partitions
* The last 2 bytes are for the MBR signature (magic number) for error checking.
  If the magic number is the hex value (0x55, 0xaa) BIOS will try booting the system
  if not, then BIOS will error stating it could not find a bootable device

NOTE: The MBR does not contain the "real" bootloader, it simply knows the address
      on disk of the actual bootloader (probably grub2). Within `boot.img`.

### How does grub work?

The MBR points to the first sector of `core.img` which is by default written to
the sectors between the MBR and the first partition. Once executed `core.img`
will load its config file and any other modules needed, like filesystem drivers,
etc. At installation time it is generated from `diskboot.img` and configured to
load stage 2.

NOTE: The config files mentioned above live in `/boot/grub`
TLDR: grub's job is basically just to load the kernel and the initramfs

### What is initramfs?

The kernel wants to be able to mount the rootfs and initialize hardware, but to
do that it needs drivers and kernel modules which are not built in.

So... The kernel first starts in an initramfs which contains all these drivers, etc
that it needs.

### What does the Kernel do once it has been loaded?

Once the initramfs is up and the kernel has started, it will initialize all hardware
which it has a driver for (drivers and kernel modules live within the initramfs).

After that it starts the init system by calling `/sbin/init` (which nowadays is
just a link to `systemd`)

### Describe the init system's role during boot

Systemd (assuming that is the init system) is the first process started by the kernel.
It is parent of all processes and has a pid of `1`. This process will persist until
the computer is shut down.

From here, systemd will run all units for `initrd.target` which includes temporarily
mounting the rootfs onto `/sysroot`.

After that the root filesystem will be swapped from its temp mountpoint to `/` and
systemd will execute all units going to `default.target`

### What are systemd targets anyway?

During boot think about targets like run levels

### Ok, but what are the different run levels

The different run levels are...

0. Halt or shutdown
1. Single user mode
2. Multi-user mode
3. Full multi-user mode with NFS (typical for servers)
4. Officially not defined; Unused
5. Full multi-user mode with NFS and graphics (typical for desktops)
6. Reboot

There are also some special ones which are rarely used...

s. Single user mode
emergency. Bypass `rc.sysinit`

## Processes and memory

### What is a process

An abstraction of a running program including a set of resources such as open files
and pending signals, internal kernel data, processor state, an address space, one
or more threads of execution, and a data section containing global variables

### In Linux what is given the PID 0

The Kernel's process scheduler

### How are processes scheduled

The scheduler runs after each process (when a hardware interrupt is issued) to
determine what goes next.

### Describe Pre-emptive multitasking

1. CPU receives interrupt
2. Interrupt stores program counter (to remember where the process was when we
   get back to it)
3. Interrupt invokes the appropriate handler
4. The handler saves the state of CPU registers to be resumed later
5. The handler does whatever the interrupting device needs it to
6. The handler invokes the scheduler again
7. The scheduler selects the next process to run
8. The scheduler restores the state of the CPU registers to where they were before
9. The scheduler jumps to execution of that process

NOTE: A clock device on the board is configured to send an interrupt every 10-20
      milliseconds

### What is a process descriptor

The kernel stores a list of processes in a circular doubley linked list called
the task list which is stored within kernel space.

A process descriptor is an element of this list (of type `struct task_struct`),
and it contains all the information about a specific process

Each of these task struct objects are around 1.7kb on a 32-bit machine.

### What are the different states of a process

* Created
* Waiting
* Running
* Terminated
* Blocked

NOTE: Blocked processes do not get scheduled

<!-- markdownlint-disable line-length -->
| State Name | Description |
| ---------- | ----------- |
| `TASK_INTERRUPTIBLE` | The process is sleeping (that is, it is blocked), waiting for some condition to exist. When this condition exists, the kernel sets the process's state to `TASK_RUNNING` |
| `TASK_UNINTERRUPTIBLE` | The state is identical to `TASK_INTERRUPTIBLE` except that it does not wake up and become runnable if it receives a signal. This is used in situations where the process must wait without interruption or when the event is excepted to occur quickly. |
| `TASK_ZOMBIE` | The task has terminated, but its parent has not yet issued a `wait4()` system call. The task's process descriptor must remain in case the parent wants to access it. If the parent calls `wait4()`, the process descriptor is deallocated |
| `TASK_STOPPED` | Process execution has stopped; the task is not running nor is it eligible to run. This occurs if the task receives a `SIGSTOP`, `SIGTSTP`, `SIGTTIN`, or `SIGTTOU` signal or if it receives any signal while it is being debugged |
| `TASK_RUNNING` | The process is runnable; it is either currently running or on a runqueue waiting to run. This is the only possible state for a process executing in user-space, it can also apply to a process in kernel space that is actively running |
<!-- markdownlint-enable line-length -->

### How is a process's state changed

The preferred way for kernel code to change the state of a process is by using
`set_task_state(task, state)`

NOTE: The method `set_current_state(state)` is synonymous to
      `set_task_state(current, state)`

### What is a thread

Threads are a unit of execution within a program

### What is a Kernel thread

A kernel thread is a kernel task running only in kernel mode.

It has usually not been...

* Created by `fork()`
* Created by `clone()`

...an example would be `kworker` or `kswapd`

Kernel threads do not have an address space (their mm pointer is null) as it is
the address space which contains the kernel

Kernel threads also...

* Only operate in kernel-space
* Schedulable and preemptable as normal processes
* Linux delegates several tasks to kernel threads, most notably the `pdflush` task
  and the `ksoftirqd` task.

These threads are created on system boot by other kernel threads. A kernel thread
can only be created by another kernel thread, by the usual `clone()` system call.

### What is the difference between a thread and a process

Threads all exist within the same process, meaning if one thread were to `exec`
something, the whole process would be terminated

That said, each thread within a process has a unique...

1. program counter
2. process stack
3. set of processor registers

...but are lighter weight because they do not have their own memory spaces

Also, if a thread's parent process were to be suspended then all of the threads
would be as well.

### What is "user space"

User space is the non-privileged portion of virtual memory which is segregated
out from the kernel (or "kernel space") to protect system memory from malicious
software behavior.

When running within user space, a program will only have access to memory marked
for that user space, whereas in kernel mode memory access is unrestricted.

### Describe userspace and kernel space and how processes go between them

* Here kernel space and user space corresponds to their Virtual address space
* Every process in linux utilizes its own separate virtual space
* In a linux system based on 32 bit architecture, user space address corresponds
  to lower 3GB of virtual space and kernel space the upper 1GB (general way)
* The kernel space virtual address space is shared between all processes
* When a process is active, it can either be running in "user mode" or "kernel mode"
* In a process in running in user mode it means that the CPU is running the user
  space side of code
* A process running in the user mode has limited capability and is controlled by
  a flag in the CPU
* Even though the kernel memory is present in the process's memory map the user
  space code is not allowed to access the kernel space code
* When a process wants to do something other than move data around in its own
  virtual memory (ie user space), like opening a file, it must make a syscall to
  communicate with kernel space
* Each CPU architecture has it's unique way of making a system call but the basics
  remain the same
* The magic instruction is executed, the CPU turns on the "privileged mode" flag,
  and jumps to a special address in kernel space, the "syscall entry point"
* Now when the syscall has reached the kernel space then the process is running
  in kernel mode and executing instructions from the kernel space memory
* Taking the same example of an open system call, to find the requested file, the
  kernel may consult with filesystem drivers (to figure out where the file is) and
  block device drivers (to load the necessary blocks) or network device drivers
  and protocols (to load the file from a remote source)
* These drivers can be either built in or can be loaded as a module but the key
  point that remains is that they are part of kernel space
* Loading a module is done with a syscall that asks the kernel to copy the module's
  code and data into kernel space and run its initialization code in kernel mode
* If the kernel can't process the request then the process is made to sleep by the
  kernel and when the request is complete then the syscall returns back to user space
* Returning back to user mode means restoring the CPU registers to what they were
  before coming to kernel mode and changing the CPU privilege level to non-privilege
* Apart from syscalls there are some other things that take the CPU to kernel mode,
  such as page faults, and interrupts

### What is a "syscall"

Syscalls are a way for programs running in user mode (or "userland") to access
functionality owned by Kernel space.

They are essentially function calls which submit a request for the kernel to handle.

### How does a "syscall" work

Userspace will initiate the system call and submit its request to the system stack.
The system stack has a table of pointers to all the different system calls, which
it uses to jump into the system call function.

### What are "capabilities"

Capabilities are used during permission checks to determine what a process is
allowed to do. They allow non-privileged processes to make privileged syscalls.
Capabilities are a per-thread attribute.

### What are some examples of "syscalls"

* `bind (2)` - Bind name to a socket
* `chdir (2)` - Change working directory
* `chmod (2)` - Change the permissions of a file
* `chown (2)` - Change the ownership of a file
* `chroot (2)` - Change root directory
* `clone (2)` - Create a child process
* `clone2 (2)` - create a child process
* `fork (2)` - Create a child process
* `vfork (2)` - create a child process and block parent
* `fstat (2)` - Get the status of a file
* `capget (2)` - get capabilities of threads
* `capset (2)` - set capabilities of threads
* `close (2)` - close a file descriptor
* `connect (2)` - initiate a connection on a socket
* `create (2)` - open and possibly create a file or device
* `dup2 (2)` - duplicate a file descriptor

* `accept (2)` - accept a connection on a socket
* `accept4 (2)` - accept a connection on a socket
* `access (2)` - check real user's permissions for a file
* `acct (2)` - switch process accounting on or off
* `add_key (2)` - add a key to the kernel's key management facility
* `adjtimex (2)` - tune kernel clock
* `alarm (2)` - set an alarm clock for delivery of a signal
* `alloc_hugepages (2)` - allocate or free huge pages
* `arch_prctl (2)` - set architecture-specific thread state
* `arm_fadvise (2)` - pre-declare an access pattern for file data
* `arm_fadvise64_64 (2)` - pre-declare an access pattern for file data
* `arm_sync_file_range (2)` - sync a file segment with disk
* `bdflush (2)` - start, flush, or tune buffer-dirty-flush daemon
* `brk (2)` - change data segment size
* `cacheflush (2)` - flush contents of instruction and / or data cache
* `clock_getres (2)` - clock and time functions
* `clock_gettime (2)` - clock and time functions
* `clock_nanosleep (2)` - high-resolution sleep with specifiable clock
* `clock_settime (2)` - clock and time functions
* `create_module (2)` - create a loadable module entry
* `delete_module (2)` - unload a kernel module
* `epoll_create (2)` - open an epoll file descriptor
* `epoll_ctl (2)` - control interface for an epoll descriptor
* `epoll_pwait (2)` - wait for an I/O event on an epoll file descriptor

### Describe the `fork()` system call

`fork()` is a system call which creates new processes.

After the creation of the child process, both the parent and the child continue
on from the next instruction.

It has no arguments, and returns an integer.

* If the value returned is positive then it is the pid of the child process
* If the value returned is zero then you are running within the child process
* If the value returned is negative then it is an error code

### Describe `open()`

The `open()` syscall opens a file specified by `pathname`. If the specified file
does not exist, it may optionally (if `O_CREAT` is specified in `flags`) be created
by `open()`.

The return value of `open()` is a file descriptor, a small non-negative integer
that is used in subsequent system calls (`read()`, `write()`, `lseek()`, `fcntl()`,
etc) to refer to the open file. The file descriptor returned by a successful call
will be the lowest-numbered file descriptor not currently open for the process.

By default, the new file descriptor is set to remain open across an `execve()`.
This can be changed by setting the `O_CLOEXEC` flag. The file offset is set to the
beginning of the file (see `lseek()`)

Parameters:

* `pathname` - pointer to the file path string
* `flags` - flags to set when opening a file (like create if doesn't exist)
* `mode_t` - the mode to open the file in (read, read / write, etc)

Returns:

* `int` - the lowest available file descriptor available to the process

### Describe `openat()`

`openat()` is basically the same as `open()` but opens a relative file

### Describe `getdents()`

The system call `getdents()` reads several `linux_dirent` structures from the
directory referred to by the open file descriptor `fd` into the buffer pointed
to by `dirp`. The argument count specifies the size of that buffer.

Parameters:

* `fd` - file descriptor of target directory
* `dirp` - buffer to write to
* `count` - the size of the buffer

Returns:

* On success returns the number of bytes read
* On end of directory 0 is returned
* On error, -1 is returned

### Describe `readdir()`

`readdir()` is a (supposedly obsolete, yet confusingly posix conforming) function
which returns a pointer to a `dirent` structure representing the next directory
entry in the directory stream pointed to by `dirp`. It returns `NULL` upon reaching
the end of the directory stream or if an error has occurred.

Parameters:

* `dirp` - pointer to directory stream

Returns:

* `dirent` - `dirent` struct (described below) or `NULL` if something bad happened

`dirent` struct contains:

* `d_ino` - Inode number
* `d_off`
* `d_reclen` - Length of this record
* `d_type` - Type of file
* `d_name` - Null-terminated file name

### Describe `mq_open()`

`mq_open()` creates a new POSIX message queue or opens an existing one. The queue
is identified by name.

Parameters:

* `name` - the name of the target message queue
* `oflag` - flags that control the operation of the call (`O_RDONLY`, `O_WRONLY`,
            `O_RDWR`, `O_CREAT`, `O_CLOEXEC`, `O_EXCL`, `O_NON_BLOCK`)

Returns:

* on success, returns a message queue descriptor for use
* on error, returns -1

### Describe `pause()`

`pase()` causes the calling process (or thread) to sleep until a signal is delivered
that either terminates the process or causes the invocation of a signal-catching
function.

Parameters:

N/A

Return:

* returns only when a signal was caught and the signal-catching function returned.
  In this case, `pause()` returns -1

### Describe `pipe()`

`pipe()` creates a pipe, a unidirectional data channel that can be used for interprocess
communication. The array `pipefd` is used to return two file descriptors referring
to the ends of the pipe. `pipefd[0]` refers to the read end of the pipe. `pipefd[1]`
refers to the write end of the pipe. Data written to the write end of the pipe is
buffered by the kernel until it is read from the read end of the pipe.

If flags is 0, then `pipe2()` is the same as `pipe()`. The following values can
be bitwise `Ored` in `flags` to obtain different behavior.

Parameters:

* `pipfd[2]` - an array to write the two file descriptors to
* `flags` - flags to change the behavior of the created pipe (`O_CLOEXEC`,
            `O_DIRECT`, `O_NON_BLOCK`)

Returns:

* on success, returns 0
* on error, -1 is returned

### Describe `mkfifo()`

`mkfifo()` makes a FIFO special file with name pathname. `mode` specifies the
FIFOs permissions. It is modified by the process's umask in the usual way: the
permissions of the created file are (`mode` & `~umask`).

A FIFO special file is similar to a pipe, except that is created in a different
way. Instead of being an anonymous communications channel, a FIFO special file
is entered into the filesystem by calling `mkfifo()`.

Once you have created a FIFO special file in this way, any process can open it
for reading and writing, in the same way as an ordinary file. However, it has to
be open at both ends simultaneously before you can proceed to do any input or
output operations on it. Opening a FIFO for reading normally blocks operations on
it. Opening a FIFO for reading normally blocks until some other process opens the
same FIFO for writing, and vice versa.

Parameters:

* `pathname` - the path to create the file at
* `mode` - the permissions of the created file

Returns:

* on success, return 0
* on error, return -1

### Describe `dup2()`

The `dup()` system call creates a copy of the file descriptor `oldfd`, using the
value of `newfd` (this is different than `dup()` which uses the lowest-numbered
unused file descriptor).

After a successful return the lowest-numbered unused file descriptors may be used
interchangeably. They refer to the same open file description and thus share file
offset and file status flags; for example, if the file offset is modified by using
`lseek()` on one of the file descriptors, the offset is also changed for the other.

The two file descriptors do not share file descriptor flags (like the close-on-exec
flag). The close-on exec flag for the duplicate descriptor is off

Parameters:

* `oldfd` - the file descriptor to copy
* `newfd` - the new file descriptor to copy the old one to

Returns:

* on success, these system calls return the new file descriptor
* on error, -1 is returned

### Describe `socket()`

`socket()` creates an endpoint for communication and returns a file descriptor
that refers to that endpoint. The file descriptor returned by a successful call
will be the lowest-numbered file descriptor not currently open for the process.

The `domain` argument specifies a communication domain; this selects the protocol
family which will be used for communication. These families are defined in `<sys/socket.h>`.
Some of the formats currently understood by the kernel include...

* `AF_UNIX` - local communication
* `AF_LOCAL` - synonymous for `AF_UNIX`
* `AF_INET` - IPv4 internet protocols
* `AF_INET6` - IPv6 internet protocols

Parameters:

* `domain` - communication domain
* `type` - communication semantics like `SOCK_PACKET`, `SOCK_RAW`, `SOCK_STREAM`
* `protocol` - the protocol to use for communication (ICMP, HTTP, whatever)

Returns:

* on success, a file descriptor for the new socket is returned
* on error, -1 is returned

### Describe `listen()`

`listen()` marks the socket referred to by `sockfd` as a passive socket, that is,
as a socket that will be used to accept incoming connection requests using `accept()`

The `sockfd` argument is a file descriptor that refers to a socket of type `SOCK_STREAM`
or `SOCK_SEQPACKET`.

The `backlog` argument defines the maximum length to which the queue of pending
communications for `sockfd` may grow. If a connection request arrives when the
queue is full, the client may receive an error with an indication of `ECONNREFUSED`
or, if the underlying protocol supports retransmission, the request may be ignored
so that a later reattempt at connection succeeds.

Parameters:

* `sockfd` - the file descriptor of the socket to listen on
* `backlog` - the max length of the queue holding pending messages

Returns:

* on success, return 0
* on error, return -1

### Describe `bind()`

When a socket is created with `socket()`, it exists in a name space (address family)
but has no address assigned to it. `bind()` assigns the address specified by `addr`
to the socket referred to by the file descriptor `sockfd`. `addrLen` specifies
the size, in bytes, of the address structure pointed to by `addr`. Traditionally,
this operation is called "assigning a name to a socket".

It is normally necessary to assign a local address using `bind()` before a `SOCK_STREAM`
socket may receive connections.

The rules used in name binding vary between address families. Consult man pages
in section 7 for detailed info.

Parameters:

* `sockfd` - the file descriptor of the open socket
* `addr` - the address to assign to the provided socket
* `addrLen` - size in bytes of the address struct pointed to by `addr`

Returns:

* on success, return 0
* on error, return -1

### Describe `sendmsg()`

The system calls `send()`, `sendto()`, and `sendmsg()` are used to transmit a
message to another socket.

`sockfd` is the file descriptor for the socket to send the message over. `msghdr`
is a struct defining the message to send. `flags` are the flags to set on the
message such as...

* `MSG_CONFIRM`
* `MSG_DONTROUTE`
* `MSG_DONTWAIT`
* `MSG_EOR`
* `MSG_MORE`
* `MSG_NOSIGNAL`
* `MSG_OOB`

Parameters:

* `sockfd` - the file descriptor of the socket to send the message over
* `msghdr` - the struct defining the message to send
* `flags` - flags to set changing the behavior of the syscall

Returns:

* on success, 0
* on error, -1

### Describe `recvmsg()`

Used to receive messages from a socket. May be used to receive data on both connectionless
and connection-oriented sockets. `sockfd` is the file descriptor of the receiving
socket. `msghdr` is a struct representing the received message. `flags` are different
flags to change the behavior of the function (see above).

Parameters:

* `sockfd`
* `msghdr`
* `flags`

Returns:

* on success, 0
* on error, -1

### Describe `connect()`

The `connect()` syscall connects the socket referred to by the file descriptor
`sockfd` to the address specified by `addr`. The `addrLen` argument specifies the
size of `addr`. The format of the address in `addr` is determined by the address
space of the socket `sockfd`.

If the socket `sockfd` is of type `SOCK_DGRAM`, then `addr` is the file address
to which datagrams are sent by default, and the only address to which datagrams
are sent by default, and the only address from which datagrams are received. If
the socket is of type `SOCK_STREAM` or `SOCK_SEQPACKET`, this call attempts to
make a connection to the socket that is bound to the address specified by `addr`.

Some protocol sockets (e.g. UNIX domain stream sockets) may successfully `connect()`
only once.

Some protocols sockets (e.g. datagram sockets in the UNIX internet domains) may use
`connect()` multiple times to change their association.

Some protocol sockets (e.g., TCP sockets as well as datagram sockets in the UNIX
and internet domains) may dissolve the association by connecting to an address
with the `sa_family` member of `sockaddr` set to `AD_UNSPEC`; thereafter, the
socket can be connected to another address.

Parameters:

* `sockfd` - the file descriptor of the socket to connect to the remote address
* `sockaddr` - the address of the socket to connect to
* `addrLen` - the size of the address given in `sockaddr`

Returns:

* on success, 0
* on error, -1

### Describe `accept()` & `accept4()`

The `accept()` system call is used with connection-based socket types (`SOCK_STREAM`,
`SOCK_SEQPACKET`). It extracts the first connection request on the queue of pending
connections for the listening socket, `sockfd`, creates a new connected socket,
and returns a new file descriptor referring to that socket. The newly created socket
is not in the listening state. The original socket `sockfd` is unaffected by this
call.

The argument `sockfd` is a socket that has been created with `socket()`, bound
to a local address with `bind()`, and is listening for connections after a `listen()`.

The argument `addr` is a pointer to a `sockaddr` struct. This struct is filled
in with the address of the peer socket, as known to the communications layer.
The exact format of the address returned `addr` is determined by the socket's
address family. When `addr` is `NULL`, nothing is filled in; in this case, `addrLen`
is not used, and should also be `NULL`.

If no pending connections are present on the queue, and the socket is not marked
as nonblocking `accept()` blocks the caller until a connection is present. If
the socket is marked nonblocking and no pending connections are present on the
queue, `accept()` failed with the error `EAGAIN` or `EWOULDBLOCK`

Returns:

* on success, return a file descriptor for the accepted socket (a non-negative integer)
* on error, return -1

NOTE: The difference between `accept()` and `accept4()` is that `accept4()` accepts
      flags

### Describe `_exit()`

`_exit()` terminates the calling process "immediately". Any open file descriptors
belonging to the process are closed. Any children of the process are inherited by
`init()` The process's parent is sent to a `SIGCHLD` signal.

The value status & 0xFF is returned to the parent process as the process's exit
status, and can be collected by the parent using one of the `wait()` family of calls

NOTE: `_Exit()` is equivalent to `_exit()`

Return:

N/A

### Describe `exit_group()`

This syscall is equivalent to `_exit()` that it terminates not only the calling
thread, but all threads in the calling process's thread group

Return:

N/A

### Describe `access()`

`access()` checks whether the calling process can access the file `pathname`.
If `pathname` is a symlink, it is dereferenced.

The check is done using the calling process's real UID and GUI, rather than the
effective IDs as is done when actually attempting an operation on the file.
Similarly, for the root user, the check uses the set of permitted capabilities
rather than the set of effective capabilities; and for non-root users, the check
uses an empty set of capabilities.

This allows set-user-ID programs and capability-endowed programs to easily determine
the invoking user's authority. In other words, `access()` does nto answer the
"can I read/write/execute this file?" question. It answers a slightly different question:
"(assuming I'm a setuid binary) can the user who invoked me read/write/execute
this file?", which gives set-user-ID programs the possibility to prevent malicious
users from causing them to read files which users shouldn't be able to read.

If the calling process is privileged (ie: its real UID is 0), then an `X_OK` check
is successful for a regular file if execute permission is enabled for any of the
file owner, group, or other

Parameters:

* `pathname` - The path of the file we are working with
* `mode` - specifies the accessibility checks to be performed
           (`F_OK`, `R_OK`, `W_OK`, `X_OK`)

Returns:

* on success, (all requested permissions are granted, or mode is `F_OK` and the
  file exists), 0 is returned
* on error, -1 is returned

### Describe `kill()`

The `kill()` system call can be used to send any signal to any process group or process

If `pid` is positive, then signal `sig` is sent to the process with the ID specified
by `pid`

If `pid` is 0, then `sig` is sent to every process in the process group of the
calling process

If `pid` is -1, then `sig` is sent to every process for which the calling process
has permission to send signals, except for process 1 (init), but see below

If `pid` is less than -1, then `sig` is sent to every process in the process group
whose ID is `-pid`

If `sig` is 0, then no signal is sent, but existence and permission checks are
still performed; this can be used to check for the existence of a process ID or
process group ID that the caller is permitted to signal.

For a process to have permission to send a signal, it must either be privileged
(under Linux: have the `CAP_KILL` capability in the user namespace of the target
process), or the real or effective user ID of the sending process must equal the
real or saved set-user-ID of the target process. In the case of `SIGCONT`, it suffices
when the sending and receiving processes belong to the same session.

Parameters:

* `pid` - the process ID to send the signal to
* `sig` - the signal to send

Returns:

* on success, 0 is returned
* on error, -1 is returned

### Describe `signal()`

`signal()` sets the disposition of the signal `signum` to `handler`, which is either
`SIG_IGN`, `SIG_DFL`, or the address of a programmer defined function
(a "signal handler")

If the signal `signum` is delivered to the process, then one of the following happens:

* If the disposition is set to `SIG_IGN`, then the signal is ignored
* If the disposition is set to `SIG_DFL`, then the default action associated with
  the signal occurs
* If the disposition is set to a function, then first either the disposition is
  reset to `SIG_DFL`, or the signal is blocked, and the handler is called with
  argument `signum`. If invocation of the handler caused the signal to be blocked,
  then the signal is unblocked upon return from the handler

Parameters:

* `signum` - the signal to trigger the supplied handler
* `handler` - a function to be called and passed `signum`

### Describe `sigaction()`

The `sigaction()` system call is used to change the action taken by a process on
receipt of a specific signal.

`signum` specifies the signal and can be any valid signal except `SIGKILL` and `SIGSTOP`

If `act` is non-NULL, the new action for signal `signum` is installed from `act`.
If `oldact` is non-NULL, the previous action is saved in `oldact`.

The `sigaction` struct contains a handler, flags to change behavior
(`SA_NOCLDSTOP`, `SA_NOCLDWAIT`, `SA_NODEFER`, `SA_RESTART`)

Parameters:

* `signum` - the signal to overwrite
* `sigaction` - struct containing the handler to overwrite
* `oldact` - the previous action assigned?

Returns:

* on success, 0
* on error, -1

### Describe `mmap()`

`mmap()` creates a new mapping in the virtual address space of the calling process.
The starting address for the new mapping is specified with `addr`. The `length`
argument specifies the length of the mapping (which must be greater than 0).

If `addr` is `NULL`, then the kernel chooses the (page-aligned) address at which
to create the mapping; this is the most portable method of creating a new mapping.
If `addr` is not `NULL`, then the kernel takes it as a hint about where to place
the mapping; on Linux, the kernel will pick a nearby page boundary (but always
above or equal to the value specified by `/proc/sys/vm/mmap_min_addr`) and attempt
to create the mapping there. If another mapping already exists there, the kernel
picks a new address that may or may not depend on the hint. The address of the
new mapping is returned as the result of the call.

The contents of a file mapping (as opposed to an anonymous mapping; see `MAP_ANONYMOUS`
below), are initialized using `length` bytes starting at offset `offset` in the
file (or other object) referred to by the file descriptor `fd`. `offset` must be
a multiple of the page size as returned by `sysconf(_SC_PAGE_SIZE)`

After the `mmap()` call has returned, the file descriptor, `fd` can be closed
immediately without invalidating the mapping

The `prot` argument describes the desired memory protection of the mapping (and
must not conflict with the open mode of the file). It is either `PROT_NONE` or
the bitwise OR of one or more of the following flags:

* `PROT_EXEC` - Pages may be executed
* `PROT_READ` - Pages may be read
* `PROT_WRITE` - Page may be written
* `PROT_NONE` - Pages may not be accessed

The `flags` argument determines whether updates to the mapping are visible to
other processes mapping the same region, and whether updates are carried through
to the underlying file. This behavior is determined by including exactly one of
the following values in `flags`:

* `MAP_SHARED` - Share this mapping. Updates to the mapping are visible to other
                 processes mapping the same region, and (in the case of file-backed
                 mappings) are carried through to the underlying file.
* `MAP_SHARED_VALIDATE` - This flag provides the same behavior as `MAP_SHARED`
                          except that `MAP_SHARED` mappings ignore unknown flags
                          in `flags`. By contrast, when creating a mapping using
                          `MAP_SHARED_VALIDATE`, the kernel verifies all passed
                          flags are known and fails the mapping with the error
                          `EOPNOTSUPP` for unknown flags.
* `MAP_PRIVATE` - Create a private copy-on-write mapping. Updates to the mapping
                  are not visible to other processes mapping the same file, and
                  are not carried through to the underlying file. It is unspecified
                  whether changes made to the file after `mmap()` call are visisble
                  in the mapped region

Parameters:

* `addr` - the virtual address where the mapping should start
* `length` - the length of the address space to map
* `prot` - the type of memory protection to apply
* `flags` - flags to change the behaviour of the function
* `fd` - the file descriptor of the file to map
* `offset` - where to start in the file

Returns:

* on success, return a pointer to the mapped area
* on error, `MAP_FAILED`

### Describe `munmap()`

The `munmap()` syscall deletes the mappings for the specified address range, and
causes further references to addresses within the range to generate invalid memory
references. The region is also automatically unmapped when the process is terminated.
On the other hand, closing the file descriptor does not unmap the region.

The address `addr` must be a multiple of the page size (but length need not be).
All pages containing a part of the indicated range are unmapped, and subsequent
references to these pages will generate a `SIGSEGV`. It is not an error if the
indicated range does not contain any mapped pages.

Parameters:

* `addr` - the address to start deleting mapped memory
* `length` - the size of the area to delete

Returns:

* on success, 0
* on error, -1

### Describe `sysctl()`

The `_sysctl()` call reads and/or writes kernel parameters. For example, the
hostname, or max number of open files. This call does a search in a tree structure,
possibly resembling a directory tree under `/proc/sys`, and if the requested item
is found calls some appropriate routine to read or modify the value.

Parameters:

* `args` - struct describing the sysctl values to set

Returns:

* on success, 0
* on error, -1

### How does a process terminate itself

By calling the `exit()` system call

### What is the difference between fork and clone

Forking:

An existing process creates an almost identical copy of itself which receives a
new pid and has the parent pid (PPID) assigned to it

Cloning:

Similar to forking, cloning creates a new child process, but these children may
share parts of their execution context with the caller (such as memory space,
table of file descriptors, table of signal handlers). When a clone is created it
executes `fn(arg)`. This fn argument is a pointer to a function that is called
by the child process at the beginning of its execution. The arg argument is
passed to the fn function. Once this function call returns the child process
terminates, the integer returned by the function is the exit code for the child process.

### What is the difference between fork and exec

Fork creates a child process which is a clone of the parent. With exec, no child
is created. The calling process is overwritten by the program whos filename is
passed as the first argument.

Also, since exec replaces the current process image, it cannot return anything to
the caller. The process will have an exit status, but that value is collected by
the parent process.

### Describe the `system` system call

`system()` uses fork to create a child process to execute a shell command specified
in command using `execl()`. `system()` will return after the command has been completed.
During execution of the command, `SIGCHILD` will be blocked, and `SIGINT` and `SIGQUIT`
will be ignored. If the command is `NULL` then `system()` returns a status indicating
whether a shell is available on the system

### Describe execve

`execve()` executes the given program referred to by pathname.

`pathname` must be either a binary executable, or a script starting with a shebang.

`argv` is an array of string pointers which will be passed into the program from
command line arguments, and `argc` is the number of args given

`envp` is another array of string pointers referring to key/value pairs to be used
as the environment

### What is the basic memory layout of a process

1. Text - The instructions of the program
2. Data - The static variables
3. Heap - The area in which programs can dynamically allocate more memory
4. Stack - A piece of memory which grows and shrinks as functions are called and
    return which is used to allocate storage for local variables and function
    call linkage information

### Describe the stack

Stack:

* This is the memory area used by our thread of execution
* When a function is called the local variables and return addresses are stored here
* The space becomes available when the function exits
* The user doesn't need to take care of the memory allocation and deallocation

### Describe the heap

Heap:

* It is the memory set aside for dynamic allocation
* Generally, an application is given a separate heap memory and it allocates memory
  from the given heap on a need basis
* We can allocate and free heap at any time
* User must take care of deallocation of memory when it is not needed
* To get heap memory we use malloc and calloc if we are in user space and if we
  are in kernel space we use kmalloc, vmalloc
* We must free the memory allocated by using free, kfree, and vfree respectively

### What is the stack boundary

A pointer used to keep track of the size of the stack. It can be moved if needed
but a stack is only allowed to grow so large. If the stack boundary is tried to
be moved too far you get a stack overflow.

### Describe paging

Memory is divided into 4kb pages

Paging:

* Physical memory is broken into fixed sized blocks called frames
* Logical memory is also broken into same sized blocks called pages
* Every logical address generated by CPU is divided into two parts -
  Page number (p) and pageoffset (d)
* The system maintains a page table which has a mapping of logical and physical
  addresses eg. apge 3 in logical memory corresponds to frame number 8 in physical
  memory
* When a pointer tries to access a page that is currently not mapped to the physical
  memory page fault occurs (it is a normal occurrence and not observed by user)

### What is virtual memory

Virtual memory is an abstraction on top of system memory which encompasses physical
RAM and SWAP space

### What is the page table

Every process has its own page table. The page table maps virtual memory addresses
within a process's address space to the virtual memory address.

### What is a page fault

A page fault occurs when a process accesses a page that is mapped in virtual address
space, but not loaded into physical memory (it's in swap).

* A major fault occurs when disk access is required
* A minor fault occurs due to page allocation

### How can you see the number of page faults

`ps` with `-o min_flt,maj_flt` flags

### Describe page cache

A page cache / disk cache is a transparent cache for pages originating from a
secondary storage device (a hard drive). These pages will be stored in otherwise
unused sections of RAM (since the memory would otherwise be idle).

### What is a dirty page

A dirty page means that the data is stored in the page cache (the "cached" section
of `free -m`), but needs to be written to the underlying storage device first.
The content of these dirty pages is periodically transferred (as well as with the
system calls sync or fsync) to the underlying storage device. The system may, in
this last instance, be a RAID controller or the hard disk directly.

### Describe segmentation

* Segmentation differs from paging in the sense that in segmentation the blocks
  of memory (both logical and physical) are of different size
* The segment table (analogous to the page table in case of paging) keeps two values
  for each segment - Segment base & Segment limit
* The segment table uses these two values to generate physical addresses
* If a program tries to access the data beyond the limit specified by segment base
  and segment limit the kernel receives a trap called the segmentation fault and
  it can abort the program
* In segmentation, the address space is typically divided into a preset number of
  segments like data segment (read / write), code segment (read-only), stack
  (read / write) etc. The programs are divided into these segments accordingly.
  Logical addresses are represented as tuple `<segment, offset>`

### What is a Control Group

Control groups, or, `cgroups` are a feature of the Linux Kernel which accounts
for, isolates, and limits resource usage (CPU, Memory, Disk I/O, Network, etc)
by a collection of processes.

They allow you to control which of you applications are allowed to hog the most
of your resources.

Control groups are often used in...

* Hypervisors (such as libvirt)
* Container runtimes (such as docker)
* Process managers / init systems (such as systemd)

### How does userspace access network resources

Userland processes can create and bind to sockets listening on a given IP and
(higher) port number using the `socket()`, and `bind()` syscalls. This provides
the process with a buffer to read from (via `recvfrom()`) containing packets
received and processed by the kernel.

FYI - they can also send messages over the network using `sendmsg()` which sends
a buffer over a socket

### Whats the lifecycle of an incoming packet to userspace

Here's a high level overview...

1. Network driver is loaded and initialized
2. Packet arrives at the NIC from the network
3. Packet is compared against MAC address filter and dropped if we don't want it
   (This can be disabled if you are setting promiscuous mode)
4. Verifies packet's layer 2 checksum
5. Packet is copied (via DMA) to a ring buffer in kernel memory
6. Hardware interrupt is generated to let the system know a packet is in memory
7. The driver calls NAPI to start a pool loop if one was not already running
8. Specific processes (which are registered during boot) pull the packet out of
   the buffer by calling the NAPI poll function that the device driver registered
   during initialization
9. Regions of memory which had network data written to them are unmapped
10. Data that was DMA'd into memory is passed up the networking layer as an `skb`
   for more processing
11. Packet steering happens to distribute packet processing load to multiple CPUs
12. Packets are handed to the protocol layers from the queues
13. Protocol layers add them to receive buffers which are attached to sockets in userspace

NOTES:

* `skb` - Socket buffer, structure in memory which collects metadata belonging to
          a packet. This includes the receiving interface, protocol, head, data,
          tail, end
* `netfilter` - IPtables `PRE_ROUTING` happens during layer 3 handler, `INPUT` during
                layer 4 handler
* `NAPI` - New API will poll for new packets constantly
           (and can be moved into a dedicated kernel thread)
* `https://www.youtube.com/watch?v=6Fl1rsxk4JQ&t=8s`
* `https://lwn.net/Articles/833840/`

### What are system load averages

Linux load averages are "system load averages" that show the running thread (task)
demand on the system as an average number of running plus waiting threads. This
measures demand, which can be greater than what the system is currently processing.
Most tools show three averages, for 1, 5, and 15 minutes.

* If the averages are 0.0 then your system is idle
* If the 1 minute average is higher than the 5 or 15 minute average, then load
  is increasing
* If the 1 minute average is lower than the 5 or 15 minute averages, then load
  is decreasing
* If they are higher than your CPU count, then you might have a performance problem
  (it depends)

### What is CPU affinity

CPU affinity is a scheduler property that "bonds" a process to a given set of
CPUs on the system. The Linux scheduler will honor the given CPU affinity and
the process will not run on any other CPUs. CPU affinity is represented as a
bitmask, the lowest order bit corresponds to the first logical CPU and the highest
order bit corresponds to the last.

0x00000001 is processor #0
0x00000003 is processor #0 and #1
0xFFFFFFFF is all processors (0 through 31)

### How can you set CPU affinity

If you're root or you have the `CAP_SYS_NICE` capability set you can use the `taskset`
CLI

### What is the "OOM killer"

The "Out of Memory Killer" is a process that the kernel uses when the system is
critically low on memory. This situation occurs because processes on the server
are consuming a large amount of memory, and the system requires more memory for
its own processes and to allocate other processes.

Whenever out of memory failures occur, the `out_of_memory()` function will be
called. Within it the `select_bad_process()` function is used which gets a score
from the `badness()` function. The most "bad" process is the one which will be
killed.

There are a few rules that determine a process's "badness"

### What is eBPF

`eBPF` is a kernel feature which allows you to extend or customize the linux kernel
without recompiling it.

You basically write a restricted C program which conforms to specific safety
requirements and then have the kernel load it

`bcc` is the SDK for eBPF program development (check out opensnoop)

It can be used to do things like create audit messages when a syscall is run or
when some network event happens

### What is a zombie process

A defunct process that has completed execution (via the exit system call) but
still has an entry in the process table

### What is a memory leak

When a process which does not release memory which is not required during execution.

### What is a kernel panic

An action taken by the linux kernel when it experiences a situation from where it
cannot recover safely. In many cases the system may keep on running but due to security
risk by fearing security breach the kernel reboots or instructs to be rebooted manually.

### What can cause a kernel panic

1. Hardware failure
2. Software bus in the OS
3. During boot a kernel panic can happen if...
    * The kernel is not correctly configured, compiled, or installed
    * OS incompatibility, hardware failure including RAM
    * Missing device driver
    * Kernel unable to locate root file system
    * After booting the init process dies

### What does IPC stand for

Inter-process communication

### What are different types of IPC

* Signals
* Pipes
* Sockets
* File locking
* Message Queues
* Semaphores
* Shared memory

### What is a signal

A signal is a message sent by the kernel to a process, asking a process to do something

Signals include...

<!-- markdownlint-disable line-length -->
| Signal name | Description |
| ----------- | ----------- |
| `SIGABRT` | Abort signal |
| `SIGALRM` | Timer signal |
| `SIGBUS` | Bus error (bad memory access) |
| `SIGCHLD` | Child stopped or terminated |
| `SIGCLD` | A synonym for `SIGCHLD` |
| `SIGCONT` | Continue if stopped |
| `SIGEMT` | Emulator trap |
| `SIGFPE` | Floating-point exception |
| `SIGHUP` | Hangup detected on controlling terminal or death of controlling process |
| `SIGILL` | Illegal instruction |
| `SIGINFO` | A synonym for `SIGPWR` |
| `SIGINT` | Interrupt on keyboard |
| `SIGIO` | I/O now possible |
| `SIGIOT` | IOT trap. A synonym for `SIGABRT` |
| `SIGKILL` | Kill signal |
| `SIGLOST` | File lock lost (unused) |
| `SIGPIPE` | Broken pipe: write to pipe with no readers |
| `SIGPOLL` | Pollable event |
| `SIGPROF` | profiling timer expired |
| `SIGPWR` | Power failure |
| `SIGQUIT` | Quit from keyboard |
| `SIGSEGV` | Invalid memory reference |
| `SIGSTKFLT` | Stack fault on coprocessor (unused) |
| `SIGSTOP` | Stop process |
| `SIGTSTP` | Stop typed at terminal |
| `SIGSYS` | Bad system call |
| `SIGTERM` | Termination signal |
| `SIGTRAP` | Trace / breakpoint trap |
| `SIGTTIN` | Terminal input for background process |
| `SIGTTOU` | Terminal output for background process |
| `SIGUNUSED` | Synonym for `SIGSYS` |
| `SIGURG` | Urgent condition on socket |
| `SIGUSR1` | User-defined signal 1 |
| `SIGUSR2` | User-defined signal 2 |
| `SIGVTALRM` | Virtual alarm clock |
| `SIGXCPU` | CPU time limit exceeded |
| `SIGXFSZ` | File size limit exceeded |
| `SIGWINCH` | Window resize signal |
<!-- markdownlint-enable line-length -->

NOTE: `SIGKILL` and `SIGSTOP` cannot be caught

### What is a semaphore

A semaphore is an unsigned integer that can be incremented and decremented with
`wait()` and `post()` (post is sometimes called signal).

Both of these operations are atomic, ie: they must not interrupt each other.

If the value is decremented to 0 then the next call of `wait()` will block until
the value is incremented again

### What is a memory / message queue

Memory queues are a thread-safe form of IPC. Its basically just a queue that exists
in shared memory and is accessible to multiple processes. You know what a message
queue is my dude.

### What is a namespace

Namespaces are a feature of the linux kernel that partitions kernel resoruces such
that one set of processes sees one set of resources while another set of processes
see something different.

### What is the difference between a cgroup and a namespace

namespace = how much resources you can see
cgroup = how much resources you can use

## File systems

### How do file permissions work

Upon calling `open()` the linux kernel will check the file permissions set within
the appropriate inode in order to determine whether or not the user is allowed to
read it.

### What happens when you open a file

When you open a file (assuming you have the correct permissions) a file descriptor
is created using the unique inode number associated with the file name. As many
processes / applications can point to the same file, the inode has a link field
that maintains the total count of lints to the file. If a file is present in a directory,
its link count is one, if it has a hard link its link count will be two, and if
a file is opened by a process, its link count will be incremented by one.

### What are sticky bits

A sticky bit is a permission bit that is set on a file or directory that lets only
the owner of that file / directory or the root user delete or rename it. No other
user is given privileges to delete the file created by some other user.

### What do the `setuid` and `setgid` bits do

The `setuid` or `setgid` bits can be applied to a file making it so any time that
file is executed by any user, it will run as if they were the owner.

### How can you set the `setuid` or `setgid` bit

Set the `setuid` bit

```
chmod u+s myfile
```

Set the `setgid` bit

```
chmod u+g myfile
```

### What is a umask

The umask defines the default permissions of a created file. The umask is subtracted
from 777 to determine the default permissions.

ie: 777 - 022 = 755

### How do you set sticky bits

Sticky bits can be set using the `+t` flag with `chmod`

ie: `chmod +t myDir`

NOTE: `-t` can be used to remove it

### What is the `/proc` file system

Proc is a pseudo filesystem that is generally mounted as `/proc`. It provides an
interface into the kernel data structures. Proc contains a directory for each of
the pids running on the system. Inside each of the pid directories you can find
out additional information about the process.

Such as...

* `fd` - a subdirectory containing links to all open files
* `environ` - a file containing all environment variables for the process
* `exe` - a link to the running binary
* `limits` - limits defined in `/etc/security/limits.conf`

Other stuff includes...

* `cpuinfo`
* `devices`
* `filesystems`
* `interrupts`
* `ioports`
* `kmsg` logs
* `loadavg`
* `meminfo`
* `modules`
* `net` - open sockets
* `uptime`

### What are some file system mount options

Common options...

<!-- markdownlint-disable line-length -->
| Option | Description |
| ------ | ----------- |
| `async` | Allows the asynchronous input / output operations on the filesystem |
| `auto` | Allows the filesystem to be mounted automatically using a `mount -a` command |
| `defaults` | Alias for `async,auto,dev,exec,nouser,rw,suid` |
| `exec` | Allows the execution of binary files on a particular filesystem |
| `loop` | Mounts an image as a loop device (the image acts as a filesystem) |
| `noauto` | Default behavior disallows the automatic mount of the filesystem using the `mount -a` command |
| `noexec` | Disallows the execution of the binary files on the particular filesystem |
| `nouser` | Disallows an ordinary user (that is not root) to mount and unmount the filesystem |
| `remount` | Remounts the file system in case it is already mounted |
| `ro` | Read only |
| `rw` | Read write |
| `user` | Allows a non-root user to mount and unmount the filesystem |
<!-- markdownlint-enable line-length -->

Others ...

* `-r`: Read only
* `-rw`: Read Write
* `-L`: Label
* `-U`: UUID
* `-t`: Types
* async
* atime/noatime
* auto/noauto
* context
* defaults
* dev/nodev
* diraatime/nodiratime
* dirsync
* exec/noexec
* group
* iversion/noiversion
* suid/nosuid

### Describe The Virtual Filesystem

Virtual filesystem (VFS) or Virtual filesystem switch is an abstraction layer on
top of a more concrete filesystem. The purpose of a VFS is to allow for client
applications to access different types of concrete filesystems in a uniform way.

VFS is a kernel software layer that handles all system calls related to
filesystems. Its main strength is providing a common interface to several kinds of
filesystems. It also helps different types of filesystems to interoperate.

The VFS substitutes the generic system call like read and write with the native
function for that particular filesystem, eg: NTFS. Each specific filesystem
implementation must translate its physical organization into VFS's common file model.

### What are the 4 filesystem related abstractions UNIX provides

1. Mount points
2. Directory entries
3. Files
4. Inodes

The main VFS objects are...

A file object is an open file associated with a process. It is really just a block
of logically related arbitrary data.

An Inode object represents metadata about a file. An inode contains essential
information about ownership (user, group), access mode (read, write, execute),
and file type.

Dentry object, it is the glue that holds inodes and files together by relating
inode numbers to file names. Dentries also play a role in directory caching which
ideally keeps the most frequently used files on-hand for faster access. File system
traversal is another aspect of the dentry as it maintains a relationship between
directories and their files

Superblock object, it is basically the file system metadata and defines the file
system type, size, status, and information about other metadata structures. The superblock
is very critical to the file system and therefore is stored in multiple
redendant copies for each file system. The superblock is a very "high level"
metadata structure for the file system. For example, if the superblock of a partition
`/var`, becomes corrupt then the file system in question cannot be mounted by the
operating system. Commonly in this event `fsck` is run and will automatically
select an alternate, backup copy of the superblock and attempt to recover the
file system. The backup copies themselves are stored in block groups spread through
the file system with the first stored at a 1 block offset from the start of the
partition. This is important in the event that a manual recovery is necessary.

### What are some file system types

* vfat
* ext3
* ext4
* btrfs
* zfs
* nfs
* nfs4

### What are the basic file I/O methods

* `open()`
* `read()`
* `write()`
* `close()`

### What is a file descriptor

A number that uniquely identifies an open file in a computer's OS. It describes
a data resource, and how that resource may be accessed

### When do filesystems runs out of space

1. There is no space left for adding new data
2. All inodes are consumed

### What is an inode

An inode is a data structure.

Every file (and directory) has an inode in which metadata is stored.
This metadata includes...

* Device ID
* File serial numbers
* The file mode which determines file types and how the file owners can access
  the file
* Link count telling how many hard links point to the file
* User ID of the file owners
* Group ID of the file
* Device ID of the file if its a device file
* File size in bytes
* Timestamps telling when the inode itself was last modified (ctime), the file
  content was modified (mtime) and last accessed (atime)
* Preferred I/O block size
* The number of blocks allocated to this file

When a file is created inside a directory then the file-name and the Inode number
are assigned to a file. These two entries are associated with every file in a directory.

When a user tries to access a file or any information related to the file then
they use the file name to do so but internally the file-name is first mapped with
its Inode number stored ina  table. Then through that Inode number the corresponding
Inode is accessed. There is a table (Inode table) where this mapping of Inode numbers
with the respective Inodes is provided

### Where are inodes stored

All of a file system's inodes are collected together to form an inode table.

### How can you see inode info

* `df -i`
* `stat`
* `ls -i`

### Whats an easy way to increase the speed up file access

Disable `atime` modification in `/etc/fstab`

### Where are filenames stored

Unix directories map file system names to inode numbers that contain relevant data.
A directory is a special file that the kernel maintains. Only kernel modifies
directories, but processes can read them. The contents of a directory are a list
of filename and inode number pairs. When new directories are created, the kernel
makes two entries named '.' (pointer to the directory itself) and '..'
(the parent directory). The system call for creating directories is `mkdir`

### What is a hard link

Hard links are exact replicas of the actual file it is pointing to. Both the hard
link and the linked file shares the same inode

### What is a soft link

A symlink is a link between files. It's just a shortcut to the file.

### What is the maximum length of a filename in linux

This depends on the file system, but generally its 255 bytes

### What are filenames which are preceded by a dot

A hidden file

### What is a FIFO pipe

First-in-first-out pipe also known as a "named-pipe"

### What is the difference between ext4 and ext3

* Ext4 has a max file size of 16TB, ext3 is only 2TB
* Ext4 max file system size is 1EB, ext3 is 32TB
* Ext4 has the option to turn journaling off
* Ext4 supports unlimited subdirectories
* Ext4 checksums its journals
* Ext4 marks unallocated blocks and sections as such, allowing `fsck` to skip them
  improving speeds

### What is file system journaling

File system journalling keeps track of changes that have not yet been committed

### What is lost+found

The lost+found directory is a directory on the file system where `fsck`
will restore partially deleted files to when repairing a file system.
This is when the file itself is salvageable, but the file name and path
info has been lost.

### What is the difference between an NFS share and a samba share

NFS is linux exclusive, samba also works on windows

### How can you list all logical volume info

`lvs` or `lvdisplay`

### What is the format of an `fstab` entry

1. `fs_spec`: This field describes the block special device, remtoe filesystem or
   filesystem image for loop device to be mounted or swap file or swap partition
   to be enabled
2. `fs_file`: This field describes the mount point (target) for the filesystem
3. `fs_vfstype`: The type of the filesystem
4. `fs_mntops`: Mount options
5. `fs_freq`: The field used by `dump(8)` to determine which filesystems need to
   be dumped
6. `fs_passno`: This field is used by `fsck(8)` to determine the order in which
   filesystem checks are done at boot time. The root filesystem should be specified
   with a `fs_passno` of 1. Other filesystems should have a `fs_passno` of 2.
   Filesystems within a drive will be checked sequentially, but filesystems on
   different drives will be checked at the same time to utilize parallelism available
   in the hardware. Defaults to zero (do not `fsck`) if not present

### What is a command to view all available partitions on the system

* `fdisk -l`
* `df -h`
* `mount`

### What are the journaling modes supported by ext3 file system

* Journaled: Lowest risk mode, writing both data and metadata to the journal before
             committing it to the filesystem. This ensures consistency of the file
             being written to, as well as the filesystem as a whole, but can significantly
             decrease performance
* Ordered: The default mode, journals **ONLY** metadata but the ordering is strict.
           First metadata is written to the journal, then data is written to the
           filesystem, and only then is the associated metadata in the journal
           flushed to the filesystem. This ensures that, in the event of a crash,
           the metadata associated with incomplete writes is still in the journal,
           and the filesystem can sanitize those incomplete writes while rolling
           back the journal. In ordered mode, a crash may result in corruption of
           the file or files being actively written to during the crash, but the
           filesystem itself - and files not being written to are guaranteed safe
* Writeback: The least safe, Journal updates are not atomic, but this gives better
             performance

### What is an extent

An extent is a range of contiguous physical blocks (up to 128MB assuming a 4KB
block size) that can be reserved and addressed at once. Utilizing extents decreases
the number of inodes required by a given file and significantly decreases fragmentation
and increases performance when writing large files

### How do you kill all processes in a file system

`fuser -km mnt_point`

### Why do we need partitions

Separate partitions improve performance by keeping data together which reduces the
disk head seek

### What are extended filesystem attributes

Extended attributes are name:value pairs associated permanently with files and
directories, similar to the environment strings associated with a process

### What are common file attributes supported by many common file systems

* `noatime`
* `append-only`
* `immutable`
* `nodump`
* `securedeletion`
* `synchronous updates`

### What are the extended attribute namespaces

* user
* trusted
* system
* security

### Where are the extended attributes stored

Extended attributes are stored directly in inodes (on file systems with inodes
bigger than 128 bytes) and on additional disk blocks. The i_file_acl field contains
the block number if an inode uses an additional block. All addtributes must fit
into the inode and one additional block

### What is swap

Linux divides its physical RAM into chunks of memory called pages. Swapping is
the process whereby a page of memory is copied to the preconfigured space on the
hard disk, called swap space, to free up that page of memory.

### What is swappiness

Swappiness is a `sysctl` parameter that represents the kernel's preference
(or avoidance) of using swap space. Swappiness is a value between 0 and 100.

### What does IOP stand for, what can you use it for

Input / Output Operations per second

IOPS are a measurement of disk performance

### How can you measure disk performance

A few CLI commands I've used before...

* `hdparam`
* `iostat`
* `sar`

### What is a device file

A special file which is an interface to a device driver that appears on the filesystem