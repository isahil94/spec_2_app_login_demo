import os
from collections import defaultdict

root = os.path.join("artifacts", "tests", "test_scripts")
counts = defaultdict(list)
for dirpath, _, files in os.walk(root):
    for f in files:
        counts[f].append(os.path.join(dirpath, f))
dups = {k: v for k, v in counts.items() if len(v) > 1}
if not dups:
    print("No duplicate filenames under artifacts/tests/test_scripts")
else:
    print("Duplicates found:")
    for k, v in dups.items():
        print(f"{k} -> {len(v)}")
        for p in v:
            print("  " + p)
