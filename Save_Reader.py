import tempfile
import os
from SS_Save_Viewer_Test import *

def read_save_data():

    with open(file_name, 'rb') as f:

        offset = 0
        slot = 0

        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            if chunk.startswith(SAVE_PATTERN):

                slot += 1
                print("Save Slot: ", slot)

                # Name
                f.seek(offset+0x04)
                name = f.read(MAX_SAVE_NAME_LENGTH - 1)
                new_name = name.split(b'\x00')[0].decode('ascii')
                print("Name: ", new_name)

                # Comment
                f.seek(offset+0x10)
                comment_raw = f.read(MAX_SAVE_COMMENT_LENGTH - 1)
                comment = comment_raw.split(b'\x00')[0].decode("shift-jis")
                print("Comment: ", comment)

                # Language
                f.seek(offset+0x0F)
                lang = f.read(1)
                lang_id = int.from_bytes(lang, 'big')
                print("Language: ", get_language(lang_id))

                # Date
                f.seek(offset+0x1A)
                date_bytes = f.read(4)
                date_id = int.from_bytes(date_bytes, 'big')
                print("Date: ", convert_bytes_to_Datetime(date_id))

                # Size in Bytes
                f.seek(offset+0x1E)
                size = f.read(4)
                size_bytes = int.from_bytes(size)
                print("Bytes: ", size_bytes)

                # Block Size
                blocks = round(size_bytes / 64) + 1
                print("Blocks: ", blocks)
                print(" ")

                # Optionally seek back to continue scanning from next chunk
                f.seek(offset + CHUNK_SIZE)

            offset += CHUNK_SIZE

def remove_alternating_ff_to_tempfile(file_name):

    try:
        # Create a temporary file, opened in binary read/write mode
        # It's deleted automatically when closed.
        temp_file = tempfile.TemporaryFile(mode='w+b')

        with open(file_name, 'rb') as infile:
            is_ff_byte = True  # Flag to track if the current byte should be 0xFF
            while True:
                byte = infile.read(1)  # Read one byte at a time
                if not byte:
                    break  # End of file

                if is_ff_byte:
                    if byte == b'\xFF':
                        # This is the alternating 0xFF, skip it
                        is_ff_byte = False
                    else:
                        # Unexpected byte, write it and reset the flag
                        temp_file.write(byte)
                        is_ff_byte = True
                else:
                    # Not an alternating 0xFF byte, write it
                    temp_file.write(byte)
                    is_ff_byte = True

        temp_file.seek(0)  # Rewind the temporary file to the beginning for reading.

        return temp_file

    except FileNotFoundError:
        print(f"Error: Input file '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def read_pad_save_data(file_object): # Now accepts a file-like object
    with file_object as f: # Use the file-like object directly
        offset = 0
        slot = 0

        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            if chunk.startswith(SAVE_PATTERN):
                slot += 1
                print("Save Slot: ", slot)

                # Name
                f.seek(offset+0x04)
                name = f.read(MAX_SAVE_NAME_LENGTH - 1)
                new_name = name.split(b'\x00')[0].decode('ascii')
                print("Name: ", new_name)

                # Comment
                f.seek(offset+0x10)
                comment_raw = f.read(MAX_SAVE_COMMENT_LENGTH - 1)
                comment = comment_raw.split(b'\x00')[0].decode("shift-jis")
                print("Comment: ", comment)

                # Language
                f.seek(offset+0x0F)
                lang = f.read(1)
                lang_id = int.from_bytes(lang, 'big')
                print("Language: ", get_language(lang_id))

                # Date
                f.seek(offset+0x1A)
                date_bytes = f.read(4)
                date_id = int.from_bytes(date_bytes, 'big')
                print("Date: ", convert_bytes_to_Datetime(date_id))

                # Size in Bytes
                f.seek(offset+0x1E)
                size = f.read(4)
                size_bytes = int.from_bytes(size)
                print("Bytes: ", size_bytes)

                # Block Size
                blocks = round(size_bytes / 64) + 1
                print("Blocks: ", blocks)
                print(" ")

                # Optionally seek back to continue scanning from next chunk
                f.seek(offset + CHUNK_SIZE)

            offset += CHUNK_SIZE