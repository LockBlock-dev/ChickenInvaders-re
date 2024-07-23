import os
import hashlib

MD5_HASH_V_1_30 = "4b485d20519e07db91b3c69fa8ce9f2b"
FULLSCREEN_PATCH_OFFSET = 0x8D35
FULLSCREEN_PATCH_TRUE = b'\x01'
FULLSCREEN_PATCH_FALSE = b'\x00'

filename = "ChickenInvaders.exe"

with open(filename, "r+b") as bin:
    content = bin.read()
    md5_hash = hashlib.md5(content).hexdigest()

    print(f"MD5 hash of your {filename}: {md5_hash}")
    
    if md5_hash != MD5_HASH_V_1_30:
        print(f"MD5 hash mismatch! Patch already applied? Aborting...")
        exit(1)
    else:
        print(f"MD5 hash match! Patching...")

    with open(f"{filename}.bak", "wb") as bak:
        bak.write(content)

        print(f"Original executable saved at {filename}.bak!")

    ##################
    # Windowed patch #
    ##################

    bin.seek(FULLSCREEN_PATCH_OFFSET)

    bin_is_fullscreen = bin.read(1)
    is_fullscreen = False
    
    if bin_is_fullscreen == FULLSCREEN_PATCH_FALSE or bin_is_fullscreen == FULLSCREEN_PATCH_TRUE:
        is_fullscreen = True
    else:
        print(f"Invalid byte found at offset {FULLSCREEN_PATCH_OFFSET}! Aborting...")
        exit(1)
    
    if not is_fullscreen:
        print("Executable already patched! Exiting...")
        exit()

    bin.seek(-1, os.SEEK_CUR)
    
    bytes_written = bin.write(FULLSCREEN_PATCH_FALSE)
    
    if bytes_written == 1:
        print("Patched successfully! Exiting...")
    else:
        print("Something went wrong while patching! Exiting...")
