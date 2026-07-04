import os

backend_root = os.path.join("artifacts", "tests", "test_scripts", "backend_tests")
frontend_root = os.path.join("artifacts", "tests", "test_scripts", "tests")

b = set()
for dirpath, _, files in os.walk(backend_root):
    for f in files:
        b.add(f)

fset = set()
for dirpath, _, files in os.walk(frontend_root):
    for f in files:
        fset.add(f)

dups = sorted(b & fset)
if dups:
    print("DUPLICATES:")
    for d in dups:
        print(d)
else:
    print("No duplicate filenames between backend and frontend tests")
