#!/usr/bin/env python3
"""
Entry point: validate and copy a source PNG to the output directory as entry.png.
"""

import os
import sys
import struct


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_SIZE = 1024 * 1024  # 1 MiB
REQUIRED_WIDTH = 768
REQUIRED_HEIGHT = 768
SOURCE_IMAGE = "news-image-20261122.png"


def read_source_image(path: str) -> bytes:
    """Read the source image file, handling errors."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        sys.stderr.write(f"Failed to read source image: {e}\n")
        sys.exit(1)
    return data


def validate_png(data: bytes) -> None:
    """Validate PNG signature, size, IHDR dimensions, and IEND chunk."""
    if len(data) > MAX_SIZE:
        sys.stderr.write(f"Image too large: {len(data)} bytes (max {MAX_SIZE})\n")
        sys.exit(1)

    if not data.startswith(PNG_SIGNATURE):
        sys.stderr.write("Invalid PNG signature\n")
        sys.exit(1)

    # Parse chunks to find IHDR (dimensions) and IEND (terminator)
    has_ihdr = False
    has_iend = False
    offset = 8  # Skip 8-byte PNG signature

    while offset < len(data):
        if offset + 8 > len(data):
            sys.stderr.write("Truncated chunk header\n")
            sys.exit(1)

        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]

        if offset + 8 + length + 4 > len(data):
            sys.stderr.write("Truncated chunk data or CRC\n")
            sys.exit(1)

        chunk_data = data[offset + 8:offset + 8 + length]

        if chunk_type == b"IHDR":
            if length != 13:
                sys.stderr.write("Invalid IHDR chunk length\n")
                sys.exit(1)
            width, height = struct.unpack(">II", chunk_data[:8])
            if width != REQUIRED_WIDTH or height != REQUIRED_HEIGHT:
                sys.stderr.write(f"Invalid dimensions: {width}x{height} (expected {REQUIRED_WIDTH}x{REQUIRED_HEIGHT})\n")
                sys.exit(1)
            has_ihdr = True

        elif chunk_type == b"IEND":
            if length != 0:
                sys.stderr.write("Invalid IEND chunk length\n")
                sys.exit(1)
            has_iend = True

        offset += 8 + length + 4

    if not has_ihdr:
        sys.stderr.write("Missing IHDR chunk\n")
        sys.exit(1)

    if not has_iend:
        sys.stderr.write("Missing IEND chunk\n")
        sys.exit(1)


def write_output(data: bytes, output_dir: str) -> str:
    """Write the validated image to output_dir/entry.png."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "entry.png")
        with open(output_path, "wb") as f:
            f.write(data)
    except OSError as e:
        sys.stderr.write(f"Failed to write output: {e}\n")
        sys.exit(1)
    return output_path


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

    if not os.path.exists(SOURCE_IMAGE):
        sys.stderr.write(f"Source image not found: {SOURCE_IMAGE}\n")
        sys.exit(1)

    image_data = read_source_image(SOURCE_IMAGE)
    validate_png(image_data)
    output_path = write_output(image_data, output_dir)

    print(f"Written {len(image_data)} bytes to {output_path}")


if __name__ == "__main__":
    main()