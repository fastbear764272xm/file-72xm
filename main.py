#!/usr/bin/env python3
"""File deduplication utility."""
import os, hashlib, argparse

def hash_file(path, block=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(block), b""):
            h.update(b)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Find duplicate files.")
    parser.add_argument("root", nargs="?", default=".", help="Root directory")
    args = parser.parse_args()
    d = {}
    for root, _, files in os.walk(args.root):
        for name in files:
            p = os.path.join(root, name)
            try:
                h = hash_file(p)
            except OSError:
                continue
            d.setdefault(h, []).append(p)
    dup = [l for l in d.values() if len(l) > 1]
    if dup:
        for group in dup:
            print("\n".join(group))
            print()
    else:
        print("No duplicates found.")

if __name__ == "__main__":
    main()