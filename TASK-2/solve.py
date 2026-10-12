pip install pillow
import zlib
import struct
from PIL import Image

# ====================== CONFIG ======================
input_file = "corrupted.png"          # apna corrupted file ka naam
output_file = "repaired_flag.png"     # output image ka naam
# ====================================================

with open(input_file, "rb") as f:
    data = bytearray(f.read())

print("[*] File loaded, size:", len(data))

# ---------- Step 1: Fix IHDR Height + CRC ----------
# Original height was reduced. Real height = 850
width = 724
height = 850

ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
crc = zlib.crc32(b"IHDR" + ihdr_data) & 0xffffffff

# IHDR data starts at offset 16
data[16:29] = ihdr_data
data[29:33] = crc.to_bytes(4, "big")

print("[+] IHDR fixed → Height set to 850, CRC updated")

# ---------- Step 2: Remove Fake IEND ----------
# Fake IEND was inserted at position 138381
fake_iend_pos = 138381
fake_iend = data[fake_iend_pos : fake_iend_pos + 12]

if fake_iend == b"\x00\x00\x00\x00IEND\xaeB`\x82":
    print("[+] Fake IEND found and removed")
    # Remove the 12 bytes of fake IEND
    data = data[:fake_iend_pos] + data[fake_iend_pos + 12:]
else:
    print("[!] Fake IEND not found at expected location")

# ---------- Step 3: Extract & Decompress IDAT ----------
# Collect all IDAT data
pos = 8
idat_data = b""

while pos < len(data):
    length = int.from_bytes(data[pos:pos+4], "big")
    chunk_type = data[pos+4:pos+8]
    
    if chunk_type == b"IDAT":
        idat_data += data[pos+8 : pos+8+length]
    elif chunk_type == b"IEND":
        break
        
    pos += 12 + length

print("[*] Total compressed IDAT size:", len(idat_data))

# Decompress (using raw inflate)
try:
    # Skip zlib header (first 2 bytes) and use raw deflate
    raw = zlib.decompress(idat_data[2:], -15)
    print("[+] Decompressed successfully, size:", len(raw))
except Exception as e:
    print("[-] Decompression failed:", e)
    exit()

# ---------- Step 4: Unfilter and rebuild image ----------
def paeth(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc: return a
    if pb <= pc: return b
    return c

def unfilter(raw_data, width, height):
    bpp = 3
    row_size = 1 + width * bpp
    result = bytearray()
    prev = bytearray(width * bpp)

    for y in range(height):
        row = raw_data[y*row_size : (y+1)*row_size]
        filter_type = row[0]
        filtered = bytearray(row[1:])
        recon = bytearray(width * bpp)

        if filter_type == 0:  # None
            recon[:] = filtered
        elif filter_type == 1:  # Sub
            for i in range(len(filtered)):
                left = recon[i - bpp] if i >= bpp else 0
                recon[i] = (filtered[i] + left) & 0xff
        elif filter_type == 2:  # Up
            for i in range(len(filtered)):
                recon[i] = (filtered[i] + prev[i]) & 0xff
        elif filter_type == 3:  # Average
            for i in range(len(filtered)):
                left = recon[i - bpp] if i >= bpp else 0
                recon[i] = (filtered[i] + (left + prev[i]) // 2) & 0xff
        elif filter_type == 4:  # Paeth
            for i in range(len(filtered)):
                left = recon[i - bpp] if i >= bpp else 0
                up = prev[i]
                up_left = prev[i - bpp] if i >= bpp else 0
                recon[i] = (filtered[i] + paeth(left, up, up_left)) & 0xff
        else:
            recon[:] = filtered

        result.extend(recon)
        prev = recon

    return bytes(result)

pixels = unfilter(raw, width, height)
img = Image.frombytes("RGB", (width, height), pixels)
img.save(output_file)

print(f"\n[✓] Successfully repaired! Saved as → {output_file}")
print(f"[✓] Image size: {width} x {height}")
print("[✓] Flag is at the bottom of the image")
