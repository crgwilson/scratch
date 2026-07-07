# What happens when you curl something

Who knows dude...

## Shell reads the command

The shell will read the user input from `stdin` after it has been entered

## Bash executes the command

1. Bash calls `fork()` to create a child process
2. Bash connects to pipes to parent process (via `dup2()` syscall)
3. Look up command in `$PATH`
4. `execve()` the command
5. If `execve()` fails, see if the file has the `x` bit set. If so, and it isn't
   a directory, run it as a shell script

[Refer here](https://github.com/bminor/bash/blob/8868edaf2250e09c4e9a1c75ffe3274f28f38581/execute_cmd.c#L5417-L5436)

## Curl binary is loaded

1. Parsed the file as an ELF binary
2. Setup initial register & virtual memory
3. Call `start_thread()` to mark the process as available for the scheduler
4. Kernel parses the INTERP header to find the dynamic loader. If it is present...
    * Kernel mmaps the dynamic loader and the ELF to be executed in memory
    * In userland, the loader parses the elf headers, and does `dlopen` to load them
    * `dlopen` uses a configurable search path to find those libs (`ldd` and friends),
      mmaps them to memory, and informs the ELF where to find its missing symbols
    * Loader calls `_start` of the ELF

NOTE: `INTERP` points to `ldd` or `ld-linux.so` or something, `DYNAMIC` includes
      the dependencies

## Curl actually runs

1. Check hosts file for target entry
2. ARP to find our way to our DNS server
3. DNS request for target
4. Routing to target (AS, BGP, etc)
5. TCP handshake
6. If HTTPS, TLS handshake
7. Server composes a response (http if http server, other stuff if a different protocol)
8. Receives output from server