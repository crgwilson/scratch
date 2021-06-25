# Argparse

Write CLIs without having to install `click`

## Argparse: Basic usage

```python
# cli/cli.py
import argparse

def cli():
    parser = argparse.ArgumentParser(description="My fun CLI")
    parser.add_argument(
        "concat",
        meta_var="strings",
        type=str,
        nargs="+",
        required=True,
        help="an arbitrary number of strings to concatenate together",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="be more verbose about things",
    )
    args = parser.parse_args()
    print(args.concat)
    print(args.verbose)
```

## Argparse: `add_argument()`

How you can add args and flags into your parser,
it takes in a bunch of parameters which I mostly tend to not use...

* `name` of `flags` - Either a name or a list of option strings (`foo` or `-f, --foo`)
* `action` - The type of action to be taken when this argument is encountered
* `nargs` - The number of args that should be consumed
* `const` - A constant value required by some action and nargs selections
* `default` - The default value of the argument
* `type` - The type which the arg should be converted to (ie `int`, or `str`)
* `choices` - A container of allowable values
* `required` - Whether or not the arg is required
* `help` - Help text for this particular arg
* `metavar` - The name which is used to refer to the arg in generated usage messages
* `dest` - The name of the attribute to be added to the object returned by `parse_args()`

Some of these options require a bit more explanation...

### action

Describes what should be done with the consumed value. There are a few options
to choose from.

* `store` - Just store the arg value. This is the default behavior
* `store_const` - Store the value specified in the `const` parameter
* `store_true` / `store_false` - Used for flags mainly. If the arg is encountered
  it will be stored as the appropriate `bool`
* `append` - If more than one of these args are encountered, store them all in one
  list
* `append_const` - Store whats given in `const` in a list
* `count` - Store a count of the number of times the arg is encountered
* `help` - Print out the help text
* `version` - Print out whatever is present in the `version` keyword
  (ie: `%(prog)s 1.0`)
* `extend` - Store a list and extend each arg value to the list

### nargs

The number of values which can be taken for the given arg

* `(some int)` - Some explicit number of values
* `?` - One value if possible, otherwise just use the default
* `*` - Args are placed into a list
* `+` - The same as `*` except will error if no values are found

## Argparse: `FileType`

A common thing I pass into CLIs are file paths with the intent of
reading / writing / whatever. The easiest way to handle that is to use
`argparse.FileType` in the `type` param of `add_argument()`.

```python
parser.add_argument("--my-file", type argparse.FileType("r"))
```

## Argparse: Creating sub-parsers / sub-commands

```python
# cli/cli.py
import argparse

# create the top-level parser
parser = argparse.ArgumentParser(prog="PROG")
parser.add_argument("--foo", action="store_true", help="foo help")
subparsers = parser.add_subparser(help="sub-command help")

# create the parser for the "a" command
parser_a = subparsers.add_parser("a", help="a help")
parser_a.add_argument("bar", type=int, help="bar help")

# create the parser for the "b" command
parser_b = subparsers.add_parser("B", help="b help")
parser_b.add_argument("--baz", choices=["X", "Y", "Z"], help="baz help")

# parse some argument lists
parser.parse_args()
```

## Argparse: Mutually exclusive args

You can add mutually exclusive args using argument groups

```python
import argparse

parser = argparse.ArgumentParser(prog="PROG")
group = parser.add_mutually_exclusive_group()
group.add_argument("--foo", action="store_true")
group.add_argument("--bar", action="store_false")
parser.parse_args()
```

## Further reading

* [argparse docs](https://docs.python.org/3/library/argparse.html)
* [argparse tutorial](https://docs.python.org/3/howto/argparse.html)
