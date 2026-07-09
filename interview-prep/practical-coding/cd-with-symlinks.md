---
tags:
  - coding-exercise
  - interview-prep
  - practical-coding
---
# Unix `cd` with Symlinks
## Setup
Implement the logic behind the shell's `cd` command. Given the current working directory (absolute) and a target path, return the resulting absolute path, like `cd <target> && pwd`.
## Part A - Basic Resolution
```python
cd("/home/user/docs", "../photos/./img")   # "/home/user/photos/img"
cd("/home/user", "/etc/config")            # "/etc/config"  (absolute target)
cd("/", "..")                              # "/"            (can't go above root)
cd("/a/b", "c//d///e")                     # "/a/b/c/d/e"   (collapse slashes)
cd("/a/b", "")                             # define behavior; state it
```
Stack-based: split on `/`, push names, pop on `..`, skip `.` and empties.
## Part B - Home directory
Support `~` meaning `/home/<user>` (user or home path provided): `cd(cwd, "~/docs")`.
## Part C - Symlinks
You're given `symlinks: dict[str, str]` mapping absolute paths to absolute targets, e.g. `{"/photos": "/media/external/photos"}`. Resolution rule: after (or while) normalizing, if any prefix of the path is a symlink, replace it and continue resolving.
```python
symlinks = {"/photos": "/media/ext/photos"}
cd("/", "photos/2024", symlinks)   # "/media/ext/photos/2024"
```
State your resolution-order choice out loud (resolve component-by-component left to right is the defensible one - it matches real filesystems).
## Part D - Cycles
```python
symlinks = {"/a": "/b", "/b": "/a"}
cd("/", "a/file", symlinks)   # must not infinite-loop: raise error or return sentinel
```
Detect with a visited set of (path) states or a max-hop limit (real kernels cap symlink hops ~40).
