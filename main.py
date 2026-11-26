"""Place the finished front-page poster where the grader expects it.

The artwork file (poster.png) lives beside this script. Running this
script copies it into the output folder as entry.png, then inspects the
copy to prove it arrived intact: it has to be a genuine PNG, large
enough to hold the artwork, and its SHA-256 digest has to match the
poster's known digest.

Standard library only. The bytes written are identical on every run.
"""

import hashlib
import os
import shutil
import sys

POSTER_NAME = "poster.png"
ENTRY_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MIN_BYTES = 10_000
EXPECTED_POSTER_SHA256 = (
    "588ef4568ec955f246ef90e94932570d6db4caf1b308b01cc3821b8c692cf2d1"
)
DEFAULT_OUTPUT_DIR = "/output"


def source_dir():
    """Folder holding poster.png (override with MAKEFUN_BOT_DIR)."""
    return (
        os.environ.get("MAKEFUN_BOT_DIR")
        or os.environ.get("SOURCE_DIR")
        or os.path.dirname(os.path.abspath(__file__))
    )


def output_dir():
    """Folder receiving entry.png (override with MAKEFUN_OUTPUT_DIR)."""
    return (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or DEFAULT_OUTPUT_DIR
    )


def poster_path():
    return os.path.join(source_dir(), POSTER_NAME)


def entry_path():
    return os.path.join(output_dir(), ENTRY_NAME)


def digest_hex(data):
    return hashlib.sha256(data).hexdigest()


def require_png_magic(data):
    if data[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise SystemExit("error: not a PNG file (bad magic bytes)")


def require_min_size(data):
    if len(data) < MIN_BYTES:
        raise SystemExit(
            f"error: PNG too small: {len(data)} bytes "
            f"(need at least {MIN_BYTES})"
        )


def require_known_digest(data):
    got = digest_hex(data)
    if got != EXPECTED_POSTER_SHA256:
        raise SystemExit(f"error: sha256 mismatch: got {got}")


def inspect_copy(path):
    """Read the copied file back and run every integrity check on it."""
    with open(path, "rb") as handle:
        data = handle.read()
    require_png_magic(data)
    require_min_size(data)
    require_known_digest(data)
    return len(data)


def place_poster():
    src = poster_path()
    dst = entry_path()
    if not os.path.isfile(src):
        raise SystemExit(f"error: poster not found: {src}")
    os.makedirs(output_dir(), exist_ok=True)
    print(f"copying {src} -> {dst}")
    shutil.copyfile(src, dst)
    return dst


def main():
    dst = place_poster()
    print(f"verifying {dst} ...")
    size = inspect_copy(dst)
    print(f"ok: {ENTRY_NAME} verified ({size} bytes, sha256 matches)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
