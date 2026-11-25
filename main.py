"""One-line roast for make.fun — Midnight Fridge Roast.

Writes exactly one line (1-200 chars) roasting a fridge to
/output/entry.txt.

Judge criteria, in order (head-to-head, funniest line wins):
1. A one-line roast of a fridge, funny on the first read.
2. A concrete scene: 3 AM, the hum, the leftovers.
3. A turn: the fridge does not just hum — it judges.
4. A landing final line: judged for the leftovers it was guarding.

Pattern: ONE concrete scene (3 AM hum, same song since 1998) +
ONE reversal (the hum is not noise — it is judgement) + ONE landing
final line (judged for the leftovers).
"""

import os

ENTRY = "At 3 AM my fridge hums the same song it hummed in 1998, and somehow it still judges me for the leftovers."
MAX_CHARS = 200
MAX_BYTES = 800


def validate(text):
    if not text or not text.strip():
        raise SystemExit("entry is empty")
    if text != text.strip():
        raise SystemExit("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit("entry exceeds 200 characters")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if any(ord(c) < 0x20 for c in text):
        raise SystemExit("entry contains a control character")
    # Prove UTF-8 encodability BEFORE any write: a lone/unpaired surrogate
    # raises UnicodeEncodeError here, so we exit 1 cleanly instead of
    # failing mid-write with a partially written entry.txt.
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError:
        raise SystemExit("entry is not valid UTF-8")
    # UTF-8 byte-length bound: at most 4 bytes per character.
    if len(encoded) > MAX_BYTES:
        raise SystemExit("entry exceeds UTF-8 byte limit")
    return text


def main():
    entry = validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    # Write round-trip verification: re-read the bytes we just wrote and
    # fail loudly if they are not exactly the entry's UTF-8 encoding, so
    # a truncated or re-encoded write can never pass silently.
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != entry.encode("utf-8"):
        raise SystemExit("entry.txt write verification failed")


if __name__ == "__main__":
    main()
