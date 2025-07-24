import os
from utils_test import *
from Save_Reader_Test import *

MAX_SAVE_NAME_LENGTH = 12
MAX_SAVE_COMMENT_LENGTH = 11

SAVE_FILE_SIZE = 32768
SAVE_FILE_WITH_RAM_CART = 557056
PAD_SAVE_FILE_SIZE = 65536
PAD_SAVE_FILE_WITH_RAM_CART = 1114112

BACKUP_RAM_HEADER = "BackUpRam Format" * 4
BUP_HEADER = "Vmem"

file_name = "path\to\save\file"

CHUNK_SIZE = 64
SAVE_PATTERN = b"\x80\x00\x00\x00"

file_size = os.path.getsize(file_name)

if __name__ == '__main__':

    # 32kb unpadded save file
    if file_size == SAVE_FILE_SIZE or file_size == SAVE_FILE_WITH_RAM_CART:
        read_save_data()

    # 64kb 0xFF padded save file
    elif file_size == PAD_SAVE_FILE_SIZE or file_size == PAD_SAVE_FILE_WITH_RAM_CART:

        cleaned_temp_file = remove_alternating_ff_to_tempfile(file_name)

        if cleaned_temp_file:

            read_pad_save_data(cleaned_temp_file)

        else:
            print("Error:Could not create the temporary file or process the input file.")