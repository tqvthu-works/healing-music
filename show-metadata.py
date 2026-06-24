#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TPE2, TCON, COMM, APIC


TAG_NAMES = {
    "TIT2": "Title",
    "TPE1": "Artist",
    "TPE2": "Album Artist",
    "TALB": "Album",
    "TDRC": "Year",
    "TRCK": "Track",
    "TPOS": "Disc",
    "TCON": "Genre",
    "TCOM": "Composer",
}


def fmt_seconds(secs):
    m, s = divmod(int(secs), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h{m:02}m{s:02}s"
    return f"{m}m{s:02}s"


def read_tags(path):
    audio = File(path)
    if audio is None:
        return None, None

    info = {
        "format": audio.mime[0] if audio.mime else "unknown",
        "duration": audio.info.length if hasattr(audio.info, "length") else 0,
        "bitrate": getattr(audio.info, "bitrate", 0),
        "sample_rate": getattr(audio.info, "sample_rate", 0),
        "channels": getattr(audio.info, "channels", 0),
    }

    tags = {}
    if audio.tags is None:
        return info, tags

    for fid, frame in audio.tags.items():
        if fid in TAG_NAMES:
            tags[TAG_NAMES[fid]] = str(frame)
        elif fid == "COMM":
            tags["Comment"] = str(frame)
        elif fid.startswith("APIC"):
            tags["Cover Art"] = f"Yes ({frame.mime}, {len(frame.data)} bytes)"

    return info, tags


def print_plain(path, info, tags):
    print(f"\n{'='*60}")
    print(f"File: {path}")
    print(f"{'='*60}")

    if info:
        print(f"  Duration:    {fmt_seconds(info['duration'])}")
        print(f"  Bitrate:     {info['bitrate']//1000} kbps")
        print(f"  Sample Rate: {info['sample_rate']} Hz")
        print(f"  Channels:    {info['channels']}")
        print(f"  Format:      {info['format']}")
        print()

    if tags:
        for k, v in tags.items():
            print(f"  {k:<15} {v}")
    else:
        print("  (no metadata tags)")


def print_json(path, info, tags):
    data = {"file": str(path), "info": info, "tags": tags}
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Show MP3 metadata using mutagen")
    parser.add_argument("files", nargs="+", metavar="FILE", help="MP3 file(s) to inspect")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    has_error = False
    for fpath in args.files:
        p = Path(fpath)
        if not p.exists():
            print(f"[-] File not found: {p}", file=sys.stderr)
            has_error = True
            continue

        info, tags = read_tags(p)
        if info is None:
            print(f"[-] Cannot read: {p} (not a valid audio file)", file=sys.stderr)
            has_error = True
            continue

        if args.json:
            print_json(p, info, tags)
        else:
            print_plain(p, info, tags)

    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
