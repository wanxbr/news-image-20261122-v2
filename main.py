#!/usr/bin/env python3
"""
Entry program for make.fun competition news-image-20261122.

This program copies the source image news-image-20261122.png to the
output directory specified by MAKEFUN_OUTPUT_DIR (default: /output)
as entry.png. It validates that the copied file:

1. Has a valid PNG 8-byte signature (\\x89PNG\\r\\n\\x1a\\n)
2. Contains an IHDR chunk with width=768 and height=768
3. Does not exceed 1 MiB (1048576 bytes)

On success, prints the output path and file size in bytes.
On failure, exits with a non-zero code and prints a descriptive
error message to stderr.
"""

import os
import sys
import struct


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 768
EXPECTED_HEIGHT = 768
MAX_SIZE = 1048576


def validate_png(data: bytes) -> tuple[int, int]:
    """Validate PNG signature and return (width, height) from IHDR chunk."""
    if len(data) < 8:
        raise ValueError("File too small to be a PNG")
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("Invalid PNG signature")

    offset = 8
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("Truncated PNG chunk header")
        length = struct.unpack(">I", data[offset:offset+4])[0]
        chunk_type = data[offset+4:offset+8]
        if offset + 8 + length > len(data):
            raise ValueError("Truncated PNG chunk data")
        chunk_data = data[offset+8:offset+8+length]
        if chunk_type == b"IHDR":
            if length < 13:
                raise ValueError("IHDR chunk too small")
            width, height = struct.unpack(">II", chunk_data[:8])
            return width, height
        if chunk_type == b"IEND":
            break
        offset += 12 + length

    raise ValueError("IHDR chunk not found")


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    source_path = os.path.join(os.path.dirname(__file__), "news-image-20261122.png")
    output_path = os.path.join(output_dir, "entry.png")

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating output directory: {e}", file=sys.stderr)
        return 1

    try:
        with open(source_path, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"Error reading source image: {e}", file=sys.stderr)
        return 1

    try:
        width, height = validate_png(data)
    except ValueError as e:
        print(f"Invalid PNG: {e}", file=sys.stderr)
        return 1

    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        print(f"Invalid dimensions: expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, got {width}x{height}", file=sys.stderr)
        return 1

    if len(data) > MAX_SIZE:
        print(f"Output file exceeds maximum allowed size: {len(data)} bytes > {MAX_SIZE} bytes (1 MiB)", file=sys.stderr)
        return 1

    try:
        with open(output_path, "wb") as f:
            f.write(data)
    except OSError as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        return 1

    print(f"{output_path} {len(data)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())