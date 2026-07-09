---
tags:
  - note-taking
  - obsidian
---
# Obsidian Cheat sheet

Tips on how to use this app...

### Open fuzzy finder
```
cmd+o
```

### Add tags to a note

Use `cmd+p` to open the command palette, then run `Add file property`.

Name the property `tags`, and add values without `#`.

```yaml
---
tags:
  - python
  - testing
---
```

Obsidian writes the same frontmatter directly into the note. Keep it at the top of the file.

Run `python3 scripts/update_tag_indexes.py` to refresh the matching pages in `tags/`.
