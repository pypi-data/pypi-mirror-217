<p align="center">
  <img align="center" src="art/logo.png" height="320px" />
</p>

<h1 align="center">Echion</h1>

<p align="center">Near-zero-overhead, in-process CPython frame stack sampler</p>


## Synopsis

Echion is an in-process CPython frame stack sampler. It can achieve
near-zero-overhead, similar to [Austin][austin], by sampling the frame stack of
each thread without holding the GIL. Native stacks can be sampled too, but the
overhead is higher.

Echion is also the first example of a high-performance sampling async profiler
for CPython.


## Installation

Currently Echion is available to install from sources via this repository.

```console
pipx install git+https://github.com/p403n1x87/echion
```

Compilation requires a C++ compiler.


## Usage

The following is the output of the `echion --help` command.

```
usage: echion [-h] [-i INTERVAL] [-c] [-n] [-o OUTPUT] [-s] [-w] [-v] [-V] ...

In-process CPython frame stack sampler

positional arguments:
  command               Command string to execute.

options:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        sampling interval in microseconds
  -c, --cpu             sample stacks on CPU only
  -n, --native          sample native stacks
  -o OUTPUT, --output OUTPUT
                        output location (can use %(pid) to insert the process ID)
  -s, --stealth         stealth mode (sampler thread is not accounted for)
  -w, --where           where mode: display thread stacks on SIGQUIT (usually CTRL+\)
  -v, --verbose         verbose logging
  -V, --version         show program's version number and exit
```
The output is written to a file specified with the `--output` option. Curretly, this is in
the format of the normal [Austin][austin] format, that is collapsed stacks with
metadata at the top. This makes it easy to re-use existing visualisation tools,
like the [Austin VS Code][austin-vscode] extension.


## Compatibility

Supported platforms: Linux (amd64), Darwin (amd64)

Supported interpreters: CPython 3.8-3.12


## Where mode

The where mode is similar to [Austin][austin]'s where mode. Since Echion cannot
attach a running process, it instead relies on the user to send a SIGQUIT to a
process that has been started with the `echion` wrapper command. On most
terminals, this is done by pressing <kbd>CTRL</kbd>+<kbd>\\</kbd>. This will
cause Echion to dump the stacks of all running threads to standard error. This
is useful for debugging deadlocks and other issues that may occur in a running
process.


## Why Echion?

Sampling in-process comes with some benefits. One has easier access to more
information, like thread names, and potentially the task abstraction of async
frameworks, like `asyncio`, `gevent`, ... . Also available is more accurate
per-thread CPU timing information.

Currently, Echion supports sampling asyncio-based applications, but not in
native mode. This makes Echion the very first example of an async profiler for
CPython.

Echion relies on some assumptions to collect and sample all the running threads
without holding the GIL. This makes Echion very similar to tools like
[Austin][austin]. However, some features, like multiprocess support, are more
complicated to handle and would require the use of e.g. IPC solutions. Attaching
to a running CPython process is also equally challenging, and this is where
out-of-process tools like Austin provide a better, zero-instrumentation
alternative.


## How it works

On a fundamental level, there is one key assumption that Echion relies upon:

> The main thread lives as long as the CPython process itself.

All unsafe memory reads are performed indirectly via copies of data structure
obtained with the use of system calls like `process_vm_readv`. This is
essentially what allows Echion to run its sampling thread without the GIL.


[austin]: http://github.com/p403n1x87/austin
[austin-vscode]: https://marketplace.visualstudio.com/items?itemName=p403n1x87.austin-vscode
