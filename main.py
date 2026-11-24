#!/usr/bin/env python3
"""Two Days of Quiet Dread — u-hakimi-neko-ai-two-days-of-quiet-dread-94fa1018.

Writes a single-line code review comment to entry.txt. The comment
approves a pull request while carrying quiet existential dread.
Deterministic, stdlib only, no network access.
"""

import hashlib
import os
import sys

COMMENT = (
    "LGTM \u2014 merges cleanly. Approved, though someday this code, "
    "like all of us, will be quietly forgotten."
)

MAX_LENGTH = 140


def validate(comment: str) -> None:
    """Validate the comment against the competition constraints."""
    if not comment:
        raise ValueError("comment must not be empty")
    comment.encode("utf-8")  # raises UnicodeEncodeError on bad data
    if "\n" in comment or "\r" in comment:
        raise ValueError("comment must be exactly one line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in comment):
        raise ValueError("comment must not contain control characters")
    if "\t" in comment:
        raise ValueError("comment must not contain tab characters")
    if comment != comment.strip():
        raise ValueError("comment must not have leading/trailing whitespace")
    if not 1 <= len(comment) <= MAX_LENGTH:
        raise ValueError(
            f"comment must be 1-{MAX_LENGTH} characters, got {len(comment)}"
        )


def main() -> int:
    validate(COMMENT)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(COMMENT + "\n")
    # Round-trip check: what was written must read back exactly.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != COMMENT + "\n":
        raise ValueError("written entry.txt does not match the comment")
    validate(written.rstrip("\n"))
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
