#!/usr/bin/env python3
"""Entry for make.fun news-image-20261126: "The World in One Day — 26 November 2026".

Copies the poster (poster.png, committed in this same directory) to
/output/entry.png and verifies the copy against the poster's known SHA-256.
Standard library only. Deterministic: the same bytes on every run.
"""
import hashlib
import os
import shutil

POSTER_SHA256 = "588ef4568ec955f246ef90e94932570d6db4caf1b308b01cc3821b8c692cf2d1"


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MIN_POSTER_BYTES = 10_000


def main():
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR", os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(bot_dir, "poster.png")
    with open(src, "rb") as f:
        magic = f.read(len(PNG_MAGIC))
    assert magic == PNG_MAGIC, f"{src} is not a PNG file"
    src_size = os.path.getsize(src)
    assert src_size >= MIN_POSTER_BYTES, f"{src} is suspiciously small ({src_size} bytes)"
    print(f"poster OK: {src} ({src_size} bytes, valid PNG)")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    size = os.path.getsize(dst)
    print(f"wrote {dst} ({size} bytes, sha256 {digest})")
    assert digest == POSTER_SHA256, "SHA-256 mismatch — poster copy is corrupt"
    print("sha256 OK")


if __name__ == "__main__":
    main()
