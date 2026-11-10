"""Fill the {{PLACEHOLDERS}} in the briefing prompts from a JSON config.

Usage:
    python3 scripts/fill_placeholders.py config.json out/

Writes one filled prompt per file in prompts/ to the output folder, reports any
placeholder left unfilled, and warns if a prompt exceeds the 64 KB limit on
scheduled-task prompts.
"""
import json
import pathlib
import re
import sys

LIMIT = 64 * 1024


def main(config_path: str, out_dir: str) -> int:
    config = json.loads(pathlib.Path(config_path).read_text(encoding="utf-8"))
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    status = 0
    for src in sorted(pathlib.Path(__file__).resolve().parent.parent.glob("prompts/*.md")):
        text = src.read_text(encoding="utf-8")
        for key, value in config.items():
            text = text.replace("{{" + key + "}}", value)
        left = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))
        size = len(text.encode("utf-8"))
        (out / src.name).write_text(text, encoding="utf-8")
        note = f"{src.name}: {size:,} bytes"
        if left:
            note += f"; unfilled: {', '.join(left)}"
            status = 1
        if size > LIMIT:
            note += f"; OVER the {LIMIT:,}-byte prompt limit, trim before scheduling"
            status = 1
        print(note)
    return status


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
