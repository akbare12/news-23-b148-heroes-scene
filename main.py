#!/usr/bin/env python3
"""news-23 b148 heroes-scene: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Validates the PNG header by hand with struct: signature,
first chunk must be IHDR 13 bytes 1024x1024 (bit depth 8, colour type 2/6),
compression/filter/interlace must be 0, IHDR CRC checked explicitly, every chunk
CRC checked while walking chunks, every IDAT non-empty (total payload >= 1000
bytes), IEND 0-byte as the last chunk with no trailing data, size min 10000
bytes and <= 1 MiB. Writes ONLY to os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
Guards: refuses empty MAKEFUN_OUTPUT_DIR, an output dir inside the repo, an
output path that is a file, and writing over the source; re-reads the output
to confirm it is byte-identical and prints the sha256.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "fea8e7330efef077b845475312074bf02cc2abce818a2f98e4ca7cf2878aa462"
EXPECTED_SIZE = 181807
MAX_BYTES = 1024 * 1024
MIN_BYTES = 10000


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    repo = os.path.dirname(os.path.abspath(__file__))
    if os.path.commonpath([outdir_abs, repo]) == repo:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(outdir_abs) and not os.path.isdir(outdir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    dst = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        fail("entry.png over 1 MiB: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    # first chunk must be IHDR, 13 bytes
    if len(data) < 33:
        fail("PNG truncated before IHDR")
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk is not a 13-byte IHDR")
    ihdr = data[16:29]
    width, height, bitdepth, colour, comp, filt, interlace = struct.unpack(
        ">IIBBBBB", ihdr)
    if (width, height) != (1024, 1024):
        fail("expected 1024x1024, got %dx%d" % (width, height))
    if bitdepth != 8:
        fail("expected bit depth 8, got %d" % bitdepth)
    if colour not in (2, 6):
        fail("expected colour type 2 or 6, got %d" % colour)
    if comp != 0 or filt != 0 or interlace != 0:
        fail("compression/filter/interlace must all be 0")
    # CRC covers type+data, not length
    crc_stored = struct.unpack(">I", data[29:33])[0]
    crc_calc = zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF
    if crc_stored != crc_calc:
        fail("IHDR CRC mismatch")
    # walk chunks
    off = 33
    idat_total = 0
    saw_iend = False
    while off < len(data):
        if off + 8 > len(data):
            fail("truncated chunk header at offset %d" % off)
        clen = struct.unpack(">I", data[off:off + 4])[0]
        ctype = data[off + 4:off + 8]
        if off + 12 + clen > len(data):
            fail("truncated chunk %r at offset %d" % (ctype, off))
        chunk_crc = struct.unpack(">I", data[off + 8 + clen:off + 12 + clen])[0]
        calc = zlib.crc32(ctype + data[off + 8:off + 8 + clen]) & 0xFFFFFFFF
        if chunk_crc != calc:
            fail("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if off + 12 != len(data):
                fail("trailing data after IEND")
            saw_iend = True
            break
        off += 12 + clen
    if not saw_iend:
        fail("no IEND chunk found")
    if idat_total < 1000:
        fail("IDAT payload too small: %d bytes" % idat_total)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "PLACEHOLDER" and sha != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s" % sha)
    os.makedirs(outdir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("re-read output differs from source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))


if __name__ == "__main__":
    main()
