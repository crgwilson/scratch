# Neovim

All my notes on Neovim (the best editor) mostly focused on writing plugins

## Index

* [lua plugins](lua.md)

## Command Cheatsheet

### Open nvim for plugin development

```console
~/workspace/my-cool-plugin: nvim --cmd "set rtp+=$(pwd)" .
```

### Re-source current file

```vim
so %
```

### View logs

```vim
:messages
```

### View the contents of a table

```vim
lua print(vim.inspect(vim.api.something_that_gives_me_a_table()))
```

### Please won't somebody help me

```vim
:h
:h vim
:h nvim
:h vim.*
:h vim.fn.nvim_*
```

### Run some lua

```vim
:lua print(vim.inspect(vim.api.nvim_list_uis()[1]))
```

### Get the current buffer filetype (in lua)

```vim
lua print(vim.api.nvim_buf_get_option(0, "filetype"))
```
