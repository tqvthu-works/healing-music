#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "config.json"

DEFAULT_CONFIG = {
    "artist": "Your Artist Name",
    "album_artist": "Your Artist Name",
    "album": "Unknown Album",
    "title": "",
    "genre": "",
    "year": "",
    "track": "",
    "output_suffix": "_tagged",
    "overwrite": False,
}


def load_config():
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        print(f"[+] Created default config: {CONFIG_FILE}")
        return dict(DEFAULT_CONFIG)
    with open(CONFIG_FILE) as f:
        cfg = json.load(f)
    for k, v in DEFAULT_CONFIG.items():
        cfg.setdefault(k, v)
    return cfg


def build_ffmpeg_cmd(input_path, output_path, metadata, dry_run=False):
    cmd = ["ffmpeg", "-i", str(input_path), "-y" if metadata.get("overwrite", False) else "-n"]
    fields = ["artist", "album_artist", "album", "title", "genre", "year", "track"]
    for f in fields:
        val = metadata.get(f, "")
        if val:
            cmd += ["-metadata", f"{f}={val}"]
    cmd += ["-codec", "copy", str(output_path)]
    return cmd


def run_ffmpeg(cmd, dry_run=False):
    if dry_run:
        print(" ".join(cmd))
        return True
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[-] FFmpeg error:\n{result.stderr.strip()}")
            return False
        print(f"[+] {cmd[-1]}")
        return True
    except FileNotFoundError:
        print("[-] ffmpeg not found. Install it first.")
        sys.exit(1)


def process_file(input_path, output_path, metadata, dry_run):
    if output_path.exists() and not metadata.get("overwrite", False):
        print(f"[~] Skip (exists): {output_path}")
        return
    cmd = build_ffmpeg_cmd(input_path, output_path, metadata, dry_run)
    run_ffmpeg(cmd, dry_run)


def single_mode(input_path, output_path, metadata, dry_run):
    input_path = input_path.resolve()
    if not output_path:
        stem = input_path.stem
        suffix = metadata.get("output_suffix", "_tagged")
        output_path = input_path.with_name(f"{stem}{suffix}{input_path.suffix}")
    else:
        output_path = Path(output_path).resolve()
    process_file(input_path, output_path, metadata, dry_run)


def batch_mode(input_dir, output_dir, metadata, dry_run):
    input_dir = Path(input_dir).resolve()
    if not output_dir:
        output_dir = input_dir.parent / f"{input_dir.name}{metadata.get('output_suffix', '_tagged')}"
    else:
        output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    mp3_files = sorted(input_dir.glob("*.mp3"))
    if not mp3_files:
        print(f"[-] No .mp3 files found in {input_dir}")
        return
    for f in mp3_files:
        out = output_dir / f.name
        process_file(f, out, metadata, dry_run)


def merge_metadata(config, args):
    meta = dict(config)
    cli_map = {
        "artist": "artist",
        "album_artist": "album_artist",
        "title": "title",
        "album": "album",
        "genre": "genre",
        "year": "year",
        "track": "track",
    }
    for cli_key, meta_key in cli_map.items():
        val = getattr(args, cli_key.replace("-", "_"), None)
        if val is not None:
            meta[meta_key] = val
    if args.force or args.overwrite:
        meta["overwrite"] = True
    return meta


def show_usage(config):
    print("Usage:")
    print("  Single file:  python metadata-tagger.py -i input.mp3")
    print("  Batch:        python metadata-tagger.py -i ./music/")
    print("  Dry run:      python metadata-tagger.py -i input.mp3 --dry-run")
    print("\nCurrent config:")
    print(json.dumps(config, indent=2, ensure_ascii=False))


def main():
    if not shutil.which("ffmpeg"):
        print("[-] ffmpeg is not installed or not in PATH.")
        sys.exit(1)

    config = load_config()

    parser = argparse.ArgumentParser(description="Tag MP3 metadata using ffmpeg")
    parser.add_argument("-i", "--input", help="Input file or folder")
    parser.add_argument("-o", "--output", help="Output file or folder")
    parser.add_argument("--artist", help="Override artist")
    parser.add_argument("--album-artist", dest="album_artist", help="Override album_artist")
    parser.add_argument("--title", help="Override title")
    parser.add_argument("--album", help="Override album")
    parser.add_argument("--genre", help="Override genre")
    parser.add_argument("--year", help="Override year")
    parser.add_argument("--track", help="Override track number")
    parser.add_argument("--force", action="store_true", help="Replace existing output file (same as --overwrite)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output (alias for --force)")
    parser.add_argument("--dry-run", action="store_true", help="Preview commands without running")
    args = parser.parse_args()

    if not args.input:
        show_usage(config)
        sys.exit(0)

    metadata = merge_metadata(config, args)
    input_path = Path(args.input)

    if input_path.is_dir():
        batch_mode(input_path, args.output, metadata, args.dry_run)
    else:
        single_mode(input_path, args.output, metadata, args.dry_run)


if __name__ == "__main__":
    main()
