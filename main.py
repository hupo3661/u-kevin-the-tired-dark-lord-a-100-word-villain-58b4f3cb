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

import os
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


def validate(text: str) -> str:
    """Fail loudly unless the text satisfies the competition gate."""
    assert isinstance(text, str), "entry must be text"
    assert text == text.strip(), "entry must not have leading/trailing space"
    assert text.strip(), "entry must not be only white space"
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
    )
    assert text.encode("utf-8").decode("utf-8") == text, "entry must be UTF-8"
    return text


def resolve_output_path() -> Path:
    """Return the entry.txt path, honouring MAKEFUN_OUTPUT_DIR if set."""
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / "entry.txt"


def write_entry(text: str, target: Path) -> Path:
    """Write exactly the text plus a trailing newline, then verify it."""
    target.write_text(text + "\n", encoding="utf-8")
    # What the grader reads is the file, so verify the file -- not the constant.
    assert target.read_text(encoding="utf-8") == text + "\n", (
        "entry.txt does not hold exactly the chosen monologue"
    )
    return target


def main() -> None:
    text = validate(MONOLOGUE)
    write_entry(text, resolve_output_path())
    print(text)


if __name__ == "__main__":
    main()
