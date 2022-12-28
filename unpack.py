import os

ASSET_NAME_MAX_SIZE = 80
ASSET_OFFSET_MAX_SIZE = 3
ASSET_SIZE_MAX_SIZE = 3

filename = "ChickenInvaders.dat"
bin = open(filename, "rb")

bin.seek(0, os.SEEK_END)  # Seek to the end

filesize = bin.tell()  # Get the file size

bin.seek(4)  # Ignore unknown first 4 bytes

# We don't know yet what is the size of the header
header_size = filesize
flag = False

assets = []

while bin.tell() < header_size:
    asset_name_size = 0
    name = ""

    while True:
        b = bin.read(1)

        # If we reached the end of the file or we encountered a null character, stop reading
        if b == b"" or b == b"\x00":
            break

        asset_name_size += 1
        name += b.decode("ascii", errors="ignore")

    # Move back by one byte (-1) from the current position (1)
    bin.seek(-1, 1)

    # Skip unknown bytes
    bin.read(ASSET_NAME_MAX_SIZE - asset_name_size)

    # Read the offset (3 bytes unsigned little-endian integer) of the asset
    offset = int.from_bytes(
        bin.read(ASSET_OFFSET_MAX_SIZE), byteorder="little", signed=False
    )

    # Header ends at the first asset
    if not flag:
        header_size = offset
        flag = True

    # Skip 1 null-byte
    bin.read(1)

    # Read the size (3 bytes unsigned little-endian integer) of the asset
    size = int.from_bytes(
        bin.read(ASSET_SIZE_MAX_SIZE), byteorder="little", signed=False
    )

    # Skip 1 null-byte
    bin.read(1)

    assets.append(
        {
            "name": name,
            "offset": offset,
            "size": size,
        }
    )

folder = f"{filename}_extracted"

for asset in assets:
    path = f'{folder}/{asset["name"]}'
    head, tail = os.path.split(path)

    # Check if the directory part of the path exists
    if not os.path.exists(head):
        os.makedirs(head)

    bin.seek(asset["offset"])

    out = open(path, "wb")

    out.write(bin.read(asset["offset"]))
    out.close()

bin.close()

print(f"Extracted {len(assets)} asset(s).")
