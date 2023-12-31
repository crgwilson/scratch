# lua

## OOP in Lua

OOP in Lua feels a bit weird, since everything acts like a table under the hood. Here is a simple example of classes and inheritance.

```lua
-- Meta class
Shape = {area = 0}

-- Base class method new
function Shape:new(o, side)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    side = side or 0
    self.area = side*side;
    return o
end

-- Base class method printArea
function Shape:printArea()
    print("this area is ", self.area)
end

-- Creating an object
myshape = Shape:new(nil, 10)
myshape:printArea()


-- Derived class method new
function Square:new(o, side)
    o = o or Shape:new(o, side)
    setmetatable(o, self)
    self.__index = self
    return o
end

-- Derived class method printArea
function Square:printArea()
    print("The area of square is ", self.area)
end

-- Creating an object
mysquare = Square:new(nil, 10)
mysquare:printArea()


-- Derived class method new
function Rectangle:new(o, length, breadth)
    o = o or Shape:new(o, side)
    setmetatable(o, self)
    self.__index = self
    self.area = length * breadth
    return o
end

-- Derived class method printArea
function Rectangle:printArea()
    print("The area of Rectangle is ", self.area)
end

-- Creating an object
myrectangle = Rectangle:new(nil, 10, 20)
myrectangle:printArea()
```

## Cheatsheet

### Formatting

The main tool to use for linting and formatting lua is [stylua](https://github.com/JohnnyMorganz/StyLua) which is configured with a toml file like so...

```toml
column_width = 80
line_endings = "Unix"
indent_type = "Spaces"
indent_width = 4
quote_style = "ForceDouble"
call_parentheses = "Always"
collapse_simple_statement = "Never"
```

### Single line comment

```lua
-- my comment
```

### Multi line comment

```lua
--[[
my comment
]]
```
