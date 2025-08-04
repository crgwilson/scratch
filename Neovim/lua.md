# Neovim Lua Plugins

## Project layout

```console
cool-vim
├── lua
│   └── cool
│       └── init.lua
├── LICENSE
├── README.md
└── plugin
    └── cool.vim
```

### Project layout: plugin/cool.vim

`cool.vim` is the main entrypoint for our super cool neovim plugin

<!-- markdownlint-disable line-length -->
```vim
" This function can be ran with `:call Cool()` when sourced properly
fun! Cool()
  " This line is important! It will reload changes made to our lua src to ensure that any
  " changes we make will be reflected properly during runtime!
  lua for k in pairs(package.loaded) do if k:match("^cool") then package.loaded[k] = nil end end

  " Call the doSomethingCool function from "lua/cool/init.lua"
  lua require("cool").doSomethingCool()
endfun

let g:super_cool_value = "coooooooool"

" This augroup does a whole lot of nothing for the time being
augroup Cool
  autocmd!
augroup END
```
<!-- markdownlint-enable line-length -->

### Project layout: lua/init.lua

`init.lua` is the main entrypoint for our lua code. I'm still not super familiar
with lua so here is a super simply example to work with our `cool.vim` we already
have.

<!-- markdownlint-disable line-length -->
```lua
local function doSomethingCool()
  print("I am super cool because I write vim plugins")

  -- This is just an example of accessing global vim variables
  print(vim.g["super_cool_value"]
end

-- you have to return all your functions like this with lua
return {
  doSomethingCool = doSomethingCool
}
```
<!-- markdownlint-enable line-length -->
