#!/usr/bin/env python3
"""Refresh managed tag index sections from note frontmatter.

This script only writes files under tags/. For existing tag files, it replaces
the block between the managed markers and leaves all other content unchanged.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TAGS_DIR = ROOT / "tags"
START_MARKER = "<!-- tagged-notes:start -->"
END_MARKER = "<!-- tagged-notes:end -->"
MANAGED_BLOCK_RE = re.compile(
    rf"(?:\n\n|\n)?{re.escape(START_MARKER)}\n.*?\n{re.escape(END_MARKER)}\n?",
    re.DOTALL,
)


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def normalize_tag(value: str) -> str:
    value = strip_quotes(value.strip())
    if value.startswith("#"):
        return value.removeprefix("#").strip()

    return strip_quotes(re.split(r"\s+#", value, maxsplit=1)[0]).strip()


def frontmatter(path: Path) -> str | None:
    text = path.read_text()
    if not text.startswith("---\n"):
        return None

    closing = text.find("\n---\n", 4)
    if closing == -1:
        return None

    return text[4:closing]


def tags_from_frontmatter(raw_frontmatter: str) -> list[str]:
    lines = raw_frontmatter.splitlines()

    for index, line in enumerate(lines):
        if not re.match(r"^tags\s*:", line):
            continue

        _, raw_value = line.split(":", 1)
        raw_value = raw_value.strip()

        if raw_value.startswith("[") and raw_value.endswith("]"):
            tags = [normalize_tag(item) for item in raw_value[1:-1].split(",")]
            return sorted({tag for tag in tags if tag})

        if raw_value:
            tag = normalize_tag(raw_value)
            return [tag] if tag else []

        tags: list[str] = []
        for child in lines[index + 1 :]:
            if not child.startswith((" ", "\t")):
                break

            item = child.strip()
            if not item.startswith("- "):
                continue

            tag = normalize_tag(item[2:])
            if tag:
                tags.append(tag)

        return sorted(set(tags))

    return []


def note_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        relative_text = relative.as_posix()
        if relative_text.startswith("tags/"):
            continue
        if relative_text.endswith(".excalidraw.md"):
            continue
        files.append(path)
    return files


def title_for(tag: str) -> str:
    words = re.split(r"[-_ ./]+", tag)
    abbreviations = {"io", "uv", "re", "gdb", "dbus", "lru", "sql", "kv", "ssh", "gpg"}
    return " ".join(word.upper() if word.lower() in abbreviations else word.capitalize() for word in words if word)


def markdown_link(from_path: Path, note_relative: str) -> str:
    target = ROOT / note_relative
    link = os.path.relpath(target, from_path.parent).replace(os.sep, "/")
    label = note_relative.removesuffix(".md")
    return f"- [{label}]({link})"


def managed_block(tag_path: Path, notes: list[str]) -> str:
    lines = [START_MARKER, "## Tagged Notes", ""]
    lines.extend(markdown_link(tag_path, note) for note in notes)
    lines.append(END_MARKER)
    return "\n".join(lines)


def replacement_for(tag: str, notes: list[str]) -> tuple[Path, str, str | None]:
    tag_path = TAGS_DIR / f"{tag}.md"
    block = managed_block(tag_path, notes)

    if not tag_path.exists():
        return tag_path, f"# {title_for(tag)}\n\n{block}\n", None

    original = tag_path.read_text()
    if START_MARKER in original and END_MARKER in original:
        updated = MANAGED_BLOCK_RE.sub(f"\n\n{block}\n", original)
    else:
        separator = "\n" if original.endswith("\n") else "\n\n"
        updated = f"{original}{separator}{block}\n"

    return tag_path, updated, original


def collect_tags() -> dict[str, list[str]]:
    tags_to_notes: dict[str, set[str]] = {}

    for path in note_files():
        raw_frontmatter = frontmatter(path)
        if raw_frontmatter is None:
            continue

        note_tags = tags_from_frontmatter(raw_frontmatter)
        note_relative = path.relative_to(ROOT).as_posix()
        for tag in note_tags:
            tags_to_notes.setdefault(tag, set()).add(note_relative)

    return {tag: sorted(notes) for tag, notes in sorted(tags_to_notes.items())}


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh managed tag index sections under tags/.")
    parser.add_argument("--check", action="store_true", help="report stale tag indexes without writing files")
    args = parser.parse_args()

    changed: list[Path] = []
    for tag, notes in collect_tags().items():
        tag_path, updated, original = replacement_for(tag, notes)
        if updated == original:
            continue

        changed.append(tag_path)
        if not args.check:
            tag_path.parent.mkdir(parents=True, exist_ok=True)
            tag_path.write_text(updated)

    if args.check and changed:
        print("Tag indexes are stale:")
        for path in changed:
            print(path.relative_to(ROOT).as_posix())
        return 1

    action = "Would update" if args.check else "Updated"
    print(f"{action} {len(changed)} tag index file{'s' if len(changed) != 1 else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
