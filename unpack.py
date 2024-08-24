import os

ASSET_NAME_MAX_SIZE = 80
INTEGER_SIZE = 4

filename = "ChickenInvaders.dat"
folder = f"{filename}_extracted"
assets = []

with open(filename, "rb") as bin:
    # Read the assets count
    count = int.from_bytes(
        bin.read(INTEGER_SIZE), byteorder="little", signed=False
    )
    
    for i in range(0, count):
        asset_name_size = 0
        name = ""
    
        while True:
            b = bin.read(1)
    
            # If we reached the end of the file or we encountered a null character, stop reading
            if b == b"" or b == b"\x00":
                break
    
            asset_name_size += 1
            name += b.decode("ascii", errors="ignore")
    
        # Move back by one byte from the current position
        bin.seek(-1, os.SEEK_CUR)
    
        # Skip empty bytes
        bin.read(ASSET_NAME_MAX_SIZE - asset_name_size)
    
        # Read the offset of the asset
        offset = int.from_bytes(
            bin.read(INTEGER_SIZE), byteorder="little", signed=False
        )
    
        # Read the size of the asset
        size = int.from_bytes(
            bin.read(INTEGER_SIZE), byteorder="little", signed=False
        )
    
        assets.append({
            "name": name,
            "offset": offset,
            "size": size,
        })
    
    assert count == len(assets), "Assets count mismatch, error while reading?"
    
    for asset in assets:
        path = f'{folder}/{asset["name"]}'
        head, tail = os.path.split(path)
    
        # Check if the directory part of the path exists
        if not os.path.exists(head):
            os.makedirs(head)
    
        bin.seek(asset["offset"])
    
        with open(path, "wb") as out:
            out.write(bin.read(asset["size"]))

print(f"Extracted {count} asset(s).")
