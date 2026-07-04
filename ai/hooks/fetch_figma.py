#!/usr/bin/env python3
"""
Simple Figma fetch helper.

Usage:
  Set environment variable FIGMA_TOKEN and provide FILE_KEY as argument.
  python ai/hooks/fetch_figma.py <FIGMA_FILE_KEY>

This script will write:
 - artifacts/frontend/figma_raw.json
 - artifacts/frontend/figma_images/{frameName}__{nodeId}.png
 - artifacts/frontend/figma_design_intake.md

Do NOT store tokens in the repo. This is a convenience helper for local use by the UI/UX agent.
"""

import json
import os
import sys
from pathlib import Path

import requests

FIGMA_API = "https://api.figma.com/v1"


def mkdir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)


def download_image(url: str, dest: Path):
    r = requests.get(url, stream=True, timeout=20)
    r.raise_for_status()
    with open(dest, "wb") as fh:
        for chunk in r.iter_content(8192):
            fh.write(chunk)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ai/hooks/fetch_figma.py <FIGMA_FILE_KEY>")
        sys.exit(2)

    file_key = sys.argv[1]
    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        print("Please set FIGMA_TOKEN environment variable (do not commit it)")
        sys.exit(3)

    headers = {"X-Figma-Token": token}

    out_root = Path("artifacts/frontend")
    mkdir(out_root)
    raw_path = out_root / "figma_raw.json"
    images_dir = out_root / "figma_images"
    mkdir(images_dir)

    # fetch file
    resp = requests.get(f"{FIGMA_API}/files/{file_key}", headers=headers, timeout=30)
    resp.raise_for_status()
    doc = resp.json()
    write_json(raw_path, doc)
    print(f"Wrote {raw_path}")

    # collect top-level frame node ids (iterate document)
    def collect_frames(node, frames):
        typ = node.get("type")
        if typ == "FRAME":
            frames.append({"id": node["id"], "name": node.get("name", "frame")})
        for child in node.get("children", []):
            collect_frames(child, frames)

    frames = []
    collect_frames(doc.get("document", {}), frames)

    # request images for frames
    ids = ",".join([f["id"] for f in frames[:50]])
    if ids:
        img_resp = requests.get(
            f"{FIGMA_API}/images/{file_key}?ids={ids}&format=png&scale=2",
            headers=headers,
            timeout=30,
        )
        img_resp.raise_for_status()
        images = img_resp.json().get("images", {})
        intake = []
        for f in frames:
            node_id = f["id"]
            img_url = images.get(node_id)
            img_path = None
            if img_url:
                safe_name = f["name"].replace(" ", "_")[:80]
                img_path = images_dir / f"{safe_name}__{node_id}.png"
                try:
                    download_image(img_url, img_path)
                    print(f"Downloaded image for {f['name']} -> {img_path}")
                except Exception as e:
                    print(f"Failed to download image for {f['name']}: {e}")
                    img_path = None
            intake.append(
                {
                    "frame_name": f["name"],
                    "node_id": node_id,
                    "image": str(img_path) if img_path else None,
                }
            )

        # heuristic extraction: scan text nodes for common tokens
        # NOTE: basic heuristic: look for layer names containing 'required' 'email' 'password' 'min'
        validation_hints = []
        nodes = doc.get("nodes", {})

        # simple: scan all nodes' name and characters fields
        def scan_nodes_for_hints(node):
            hints = []
            name = node.get("name", "")
            if not name:
                return hints
            lname = name.lower()
            if "required" in lname:
                hints.append("required")
            if "email" in lname:
                hints.append("type:email")
            if "password" in lname:
                hints.append("type:password")
            if "min" in lname or "min:" in lname:
                hints.append("minLength heuristic")
            return hints

        # traverse document nodes
        def traverse(node, out):
            out.extend(scan_nodes_for_hints(node))
            for c in node.get("children", []):
                traverse(c, out)

        hints = []
        traverse(doc.get("document", {}), hints)

        # write intake md
        intake_md = out_root / "figma_design_intake.md"
        with open(intake_md, "w", encoding="utf-8") as fh:
            fh.write("# Figma Design Intake\n\n")
            fh.write(f"File Key: {file_key}\n\n")
            fh.write("## Frames\n\n")
            for i in intake:
                fh.write(
                    f"- **{i['frame_name']}** (`{i['node_id']}`) - image: {i['image']}\n"
                )
            fh.write("\n## Validation Hints (heuristic)\n\n")
            if hints:
                for h in set(hints):
                    fh.write(f"- {h}\n")
            else:
                fh.write("- No explicit validation hints found in layer names.\n")

        print(f"Wrote intake {intake_md}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
