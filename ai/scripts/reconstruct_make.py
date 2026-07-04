#!/usr/bin/env python3
"""
reconstruct_make.py

A .make file (Figma Make export) is a zip archive. Inside it,
ai_chat.json contains the FULL agent transcript that built the app —
every view_tool / write_tool / edit_tool call the coding agent made.
This script replays that transcript to reconstruct the real, final
source files (not a guess — the actual code), regardless of project
structure or file names.

USAGE
    python3 reconstruct_make.py <path-to-file.make> <output-dir>

OUTPUT
    <output-dir>/source/...           reconstructed source tree
    <output-dir>/manifest.json        list of files + sizes + tool-call counts
    <output-dir>/ai_chat_raw.json     the raw chat transcript (kept for reference)
"""

import json
import os
import re
import shutil
import sys
import zipfile


def strip_line_numbers(content):
    """view_tool results are prefixed with 'N\\t' line numbers — strip them."""
    if isinstance(content, list):
        content = "\n".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )
    if not isinstance(content, str):
        return None
    lines = content.split("\n")
    cleaned = []
    for line in lines:
        m = re.match(r"^\d+\t(.*)$", line)
        cleaned.append(m.group(1) if m else line)
    return "\n".join(cleaned)


def reconstruct(chat_json_path):
    with open(chat_json_path, encoding="utf-8", errors="replace") as f:
        d = json.load(f)

    threads = d.get("threads", [])
    files = {}
    stats = {"write_tool": 0, "edit_tool": 0, "edit_failed": 0, "view_seed": 0}

    for thread in threads:
        calls = {}
        results = {}
        order = []

        for m in thread.get("messages", []):
            for p in m.get("parts", []):
                if p["partType"] == "tool-call-json-DO-NOT-USE-IN-PROD":
                    cj = json.loads(p["contentJson"])
                    tcid = cj["toolCallId"]
                    try:
                        args = json.loads(cj.get("argsJson", "{}"))
                    except Exception:
                        args = {}
                    calls[tcid] = {"tool": cj["toolName"], "args": args}
                    order.append(tcid)
                elif p["partType"] == "tool-result-json-DO-NOT-USE-IN-PROD":
                    cj = json.loads(p["contentJson"])
                    tcid = cj["toolCallId"]
                    try:
                        rj = json.loads(cj.get("resultJson", "{}"))
                    except Exception:
                        rj = {}
                    results[tcid] = rj

        for tcid in order:
            c = calls[tcid]
            tool = c["tool"]
            args = c["args"]
            path = args.get("path")
            if not path:
                continue

            if tool == "view_tool":
                r = results.get(tcid, {})
                content = strip_line_numbers(r.get("content"))
                if content and path not in files:
                    files[path] = content
                    stats["view_seed"] += 1

            elif tool == "write_tool":
                files[path] = args.get("file_text", "")
                stats["write_tool"] += 1

            elif tool == "edit_tool":
                old = args.get("old_str", "")
                new = args.get("new_str", "")
                if path in files and old in files[path]:
                    files[path] = files[path].replace(old, new, 1)
                    stats["edit_tool"] += 1
                else:
                    stats["edit_failed"] += 1
                    print(f"  WARN: could not apply edit to {path} (tool call {tcid})")

    return files, stats


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 reconstruct_make.py <path-to-file.make> <output-dir>")
        sys.exit(1)

    make_path, out_dir = sys.argv[1], sys.argv[2]
    work_dir = os.path.join(out_dir, "_extracted_zip")
    os.makedirs(work_dir, exist_ok=True)

    print(f"Unzipping {make_path} ...")
    with zipfile.ZipFile(make_path) as z:
        z.extractall(work_dir)

    chat_json_path = os.path.join(work_dir, "ai_chat.json")
    if not os.path.exists(chat_json_path):
        print(
            "ERROR: ai_chat.json not found inside the .make file. "
            "This export may not contain a build transcript (e.g. design-only file)."
        )
        sys.exit(1)

    print("Replaying build transcript...")
    with open(chat_json_path, encoding="utf-8", errors="replace") as f:
        # Use replacement mode for non-UTF-8 bytes inside exported transcripts.
        d = json.load(f)

    files, stats = reconstruct(chat_json_path)

    source_dir = os.path.join(out_dir, "source")
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
    for path, content in files.items():
        full = os.path.join(source_dir, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)

    manifest = {
        "sourceFile": os.path.basename(make_path),
        "reconstructedFiles": [
            {"path": p, "chars": len(c)} for p, c in sorted(files.items())
        ],
        "stats": stats,
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    shutil.copy(chat_json_path, os.path.join(out_dir, "ai_chat_raw.json"))
    shutil.rmtree(work_dir)

    print(f"\nReconstructed {len(files)} file(s) into {source_dir}/")
    for p, c in sorted(files.items()):
        print(f"  {p}  ({len(c)} chars)")
    print(
        f"\nEdit calls applied: {stats['edit_tool']}  failed: {stats['edit_failed']}  "
        f"(seeded from view: {stats['view_seed']}, full writes: {stats['write_tool']})"
    )
    if stats["edit_failed"] > 0:
        print(
            "Some edits failed to apply — usually means an earlier file state wasn't "
            "captured by a view_tool call. Reconstructed files may be slightly stale "
            "in those spots; check manifest.json and spot-check against the live preview."
        )


if __name__ == "__main__":
    main()
