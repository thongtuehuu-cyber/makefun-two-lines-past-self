"""Two Lines to Your Past Self — make.fun bounty entry.

Writes exactly two lines to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR):
a warning to the writer's past self about one specific moment, and one
sentence on why that moment mattered and what changed because of it.
Deterministic: no network, no randomness, no time, no environment input
beyond the output directory.
"""

import os

ENTRY = (
    "When the hospital calls at 2 a.m., don't tell them you'll come in the morning — drive there now.\n"
    "Those six hours are the last ones your father is awake, and he spends them waiting for you."
)

MAX_CHARS = 280


def validate(text):
    """Enforce the gate: exactly 2 lines, 1-280 chars, no trailing newline."""
    if not text:
        raise ValueError("entry is empty")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if text.endswith("\n"):
        raise ValueError("entry has a trailing newline")
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly 2 lines, got %d" % len(lines))
    if not all(line.strip() for line in lines):
        raise ValueError("entry lines must not be blank")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d chars, got %d" % (MAX_CHARS, len(text)))
    text.encode("utf-8")  # must be valid UTF-8
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = validate(ENTRY)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read-back gate: the file on disk must be byte-identical to what
    # was written, or the run fails loudly instead of passing silently.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != text.encode("utf-8"):
        raise RuntimeError("read-back mismatch: entry.txt differs from ENTRY")
    print("wrote %s (%d chars)" % (path, len(text)))


if __name__ == "__main__":
    main()
