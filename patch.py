import os
import hashlib

MD5_HASH_V_1_30 = "4b485d20519e07db91b3c69fa8ce9f2b"
FULLSCREEN_PATCH_OFFSET = 0x8D35
FULLSCREEN_PATCH_TRUE = b'\x01'
FULLSCREEN_PATCH_FALSE = b'\x00'
RESTORE_WINDOW_STYLE_PATCH_OFFSET = 0x25055
RESTORE_WINDOW_STYLE_PATCH_ORIGINAL = b'\x74\x0C'
RESTORE_WINDOW_STYLE_PATCH_NOPED = b'\x90\x90'


def patch_windowed(bin):
    bin.seek(FULLSCREEN_PATCH_OFFSET)

    bin_is_fullscreen = bin.read(1)
    is_fullscreen = False
    
    if bin_is_fullscreen == FULLSCREEN_PATCH_FALSE or bin_is_fullscreen == FULLSCREEN_PATCH_TRUE:
        is_fullscreen = bin_is_fullscreen == FULLSCREEN_PATCH_TRUE
    else:
        print(f"[Patch: Windowed] Invalid byte found at offset {FULLSCREEN_PATCH_OFFSET}! Aborting...")
        return
    
    if not is_fullscreen:
        print("[Patch: Windowed] Executable already patched! Skipping...")
        return

    bin.seek(-1, os.SEEK_CUR)
    
    bytes_written = bin.write(FULLSCREEN_PATCH_FALSE)
    
    if bytes_written == 1:
        print("[Patch: Windowed] Patched successfully!")
    else:
        print("[Patch: Windowed] Something went wrong while patching!")

    bin.seek(0)


def patch_restore_window_style(bin):
    bin.seek(RESTORE_WINDOW_STYLE_PATCH_OFFSET)

    bin_je = bin.read(2)
    is_noped = False
    
    if bin_je == RESTORE_WINDOW_STYLE_PATCH_ORIGINAL or bin_je == RESTORE_WINDOW_STYLE_PATCH_NOPED:
        is_noped = bin_je == RESTORE_WINDOW_STYLE_PATCH_NOPED
    else:
        print(f"[Patch: Restore window style] Invalid byte found at offset {RESTORE_WINDOW_STYLE_PATCH_OFFSET}! Aborting...")
        return
    
    if is_noped:
        print("[Patch: Restore window style] Executable already patched! Skipping...")
        return

    bin.seek(-2, os.SEEK_CUR)
    
    bytes_written = bin.write(RESTORE_WINDOW_STYLE_PATCH_NOPED)
    
    if bytes_written == 2:
        print("[Patch: Restore window style] Patched successfully!")
    else:
        print("[Patch: Restore window style] Something went wrong while patching!")

    bin.seek(0)


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

    
    patch_windowed(bin)

    patch_restore_window_style(bin)

print("Goodbye!")
