"""Find and remove duplicate files by content hash."""
import hashlib
import os
import sys
from collections import defaultdict


def file_hash(path, chunk=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def find_duplicates(root):
    by_size = defaultdict(list)
    for dirpath, _, files in os.walk(root):
        for name in files:
            path = os.path.join(dirpath, name)
            if os.path.isfile(path) and not os.path.islink(path):
                by_size[os.path.getsize(path)].append(path)
    dups = {}
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        by_hash = defaultdict(list)
        for p in paths:
            by_hash[file_hash(p)].append(p)
        for h, group in by_hash.items():
            if len(group) > 1:
                dups[h] = group
    return dups


def main():
    if len(sys.argv) < 2:
        print("usage: dedupe.py DIR [--delete]")
        return
    root = sys.argv[1]
    delete = "--delete" in sys.argv
    dups = find_duplicates(root)
    total = 0
    for group in dups.values():
        keeper, *rest = sorted(group)
        for path in rest:
            size = os.path.getsize(path)
            total += size
            if delete:
                os.remove(path)
                print(f"removed {path}")
            else:
                print(f"duplicate: {path} (same as {keeper})")
    print(f"{len(dups)} duplicate groups, {total} bytes reclaimed")


if __name__ == "__main__":
    main()