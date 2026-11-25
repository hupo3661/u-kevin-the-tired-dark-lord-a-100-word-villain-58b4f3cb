#!/usr/bin/env python3
"""Write the 100-word villain monologue to /output/entry.txt and print it.

Deterministic, no network, no input: the entry is one fixed monologue,
spoken by a fantasy villain who is secretly just very tired. The
tiredness lives in the voice -- the request to sit down, the breath, the
quiet minute, the pause -- never in a plain statement of weariness, and
the speaker stays a villain throughout: three centuries of plotting, a
retired dragon, a unionised bat colony, a crown that still fits, a plan
that still holds, and a sting in the last line.
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

MONOLOGUE = (
    "You stand before me, hero, sword raised, destiny rehearsed \u2014 and I must ask: "
    "could we do this sitting down? Three centuries I have plotted. Three centuries of maps, "
    "of minions, of monologues in empty halls. The dragon retired. The bats unionised. Even the "
    "cursed sword filed a complaint. The crown still fits. The plan still holds. The world will "
    "kneel, in time. But first \u2014 one breath. One quiet minute. Not mercy. Not surrender. "
    "Only... a pause. Then rise, if you must. I shall be here. I always am. That, perhaps, is the curse."
)

MAX_CHARS = 600
WORD_TARGET = 100
WORD_TOLERANCE = 20


class EntryError(ValueError):
    """The fixed entry text fails one of the competition gates."""


def word_count(text: str) -> int:
    """Count whitespace-separated words in the entry text."""
    return len(text.split())


def check_shape(text: str) -> None:
    """Reject text that is not clean, single-block entry text."""
    if not isinstance(text, str):
        raise EntryError("entry must be text")
    if not text.strip():
        raise EntryError("entry must not be only white space")
    if text != text.strip():
        raise EntryError("entry must not have leading/trailing space")


def check_size(text: str) -> None:
    """Reject text outside the competition's character and word gates."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise EntryError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    words = word_count(text)
    if abs(words - WORD_TARGET) > WORD_TOLERANCE:
        raise EntryError(
            f"entry must be about {WORD_TARGET} words, got {words}"
        )
    # Round-trip through UTF-8 explicitly: the grader reads bytes, not str.
    if text.encode("utf-8").decode("utf-8") != text:
        raise EntryError("entry must be UTF-8")


def validate(text: str) -> str:
    """Fail loudly unless the text satisfies the competition gate."""
    check_shape(text)
    check_size(text)
    return text


def parse_args(argv=None) -> argparse.Namespace:
    """Parse the one optional flag: where entry.txt goes.

    Default is MAKEFUN_OUTPUT_DIR, else /output -- the entry text itself
    never changes, only its destination.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--output-dir",
        default=None,
        help="directory for entry.txt (default: $MAKEFUN_OUTPUT_DIR or /output)",
    )
    return parser.parse_args(argv)


def resolve_output_path(output_dir: str | None = None) -> Path:
    """Return the entry.txt path, honouring --output-dir, then env, then /output."""
    raw = output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    directory = Path(raw).expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "entry.txt"


def entry_bytes(text: str) -> bytes:
    """Encode exactly the text plus a trailing newline as UTF-8 bytes."""
    return (text + "\n").encode("utf-8")


def write_entry(text: str, target: Path) -> Path:
    """Write exactly the text plus a trailing newline, then verify it."""
    payload = entry_bytes(text)
    target.write_bytes(payload)
    # What the grader reads is the file, so verify the file -- not the constant:
    # compare SHA-256 digests of what was written and what is on disk.
    written = hashlib.sha256(payload).hexdigest()
    on_disk = hashlib.sha256(target.read_bytes()).hexdigest()
    if on_disk != written:
        raise EntryError("entry.txt does not hold exactly the chosen monologue")
    return target


def main(argv=None) -> int:
    """Validate the fixed monologue, write it out, and print it."""
    try:
        args = parse_args(argv)
        text = validate(MONOLOGUE)
        write_entry(text, resolve_output_path(args.output_dir))
    except EntryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
