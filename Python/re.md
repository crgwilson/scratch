# re

Relearn how regexes work every time you try and use them

## re: Basic usage

Compile a regex pattern using `re.compile()`, and then search for that pattern using
`pattern.match()`.

You can search for multiple patterns and return all matches as a dict by labelling
your patterns in your regex with `?P<some-name>`, calling `groupdict()` on
your `match()` results.

After that you can access each match via `mygroupdict["some-name"]

```python
import re

pattern = re.compile(r"?P<foo>\S+\s?P<bar>\S+")

sample_text = "some text"
matches = pattern.match(sample_text).groupdict()

print(matches["foo"])  # some
print(matches["bar"])  # text
```

## Further reading

* [re docs](https://docs.python.org/3/library/re.html)
