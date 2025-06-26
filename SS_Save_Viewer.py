#!/usr/bin/env python3

import os
from collections import namedtuple

SAVE_FILE_SIZE = 32768
PAD_SAVE_FILE_SIZE = 65536

SaturnSaveEntry = namedtuple("SaturnSaveEntry", [
    # original physical slot (unused for display)
    "Slot", "Name", "Comment", "Language", "Date", "Blocks", "Size"
])


def read_until_null_byte(source, offset):
    """
    Read bytes from either
      1) a file-like object (with .seek()/.read()), or
      2) a plain bytes/bytearray (using slicing)
    Stops on 0x00 or 0x01, returns the bytes before that.
    """
    # case A: file‐like object
    if hasattr(source, "read") and hasattr(source, "seek"):
        source.seek(offset)
        result = bytearray()
        while True:
            b = source.read(1)
            if not b or b[0] in (0x00, 0x01):
                break
            result.extend(b)
        return bytes(result)

    # case B: bytes or bytearray
    data = source  # assume bytes-like
    result = bytearray()
    for b in data[offset:]:
        if b in (0x00, 0x01):
            break
        result.append(b)
    return bytes(result)

def deinterleave(data):
    dummy = data[::2]
    if all(b in (0xFF, 0x00) for b in dummy):
        return data[1::2]
    return data

file_path = "saves/bup-int-[MK-81804] DEEP FEAR.bin"
file_size = os.path.getsize(file_path)

# 32kb unpadded save file found
if file_size== SAVE_FILE_SIZE:

    print("32kb file found")

    with open(file_path, "rb") as f32:

        save_name = read_until_null_byte(f32, 0x84)
        comment = read_until_null_byte(f32, 0x90)

        name_string = str(save_name, "ascii")
        comment_string = str(comment, "shift_jis")

        print("Save Name:" + name_string)
        print("Comment:" + comment_string)

# 64kb "0xFF" or "0x00" padded save file found
elif file_size == PAD_SAVE_FILE_SIZE:

    print("64kb file found")

    # open file as binary and store it in file buffer.
    in_file = open(file_path, "rb")
    tmp_buf = in_file.read()
    in_file.close()

    # de-interleave down to 32 KB
    f64 = deinterleave(tmp_buf)

    save_name = read_until_null_byte(f64, 0x84)
    comment = read_until_null_byte(f64, 0x90)

    name_string = str(save_name, "ascii")
    comment_string = str(comment, "shift_jis")

    print("Save Name:" + name_string)
    print("Comment:" + comment_string)