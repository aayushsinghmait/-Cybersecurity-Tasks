Task 02
Steganography

The challenge is a PNG file that has been corrupted. Find the flag in the format flag{...}.
Challenge file link
https://drive.google.com/file/d/1ELLQDWkqsSL-PM_xQcids8axmntXUiOL/view?usp=sharing
Find the flag that is in the format flag{}

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The PNG is corrupted in two main ways:

1. IHDR height was reduced from the true value 850 → 800 (hiding the bottom ~50 rows of the image). The CRC was not updated, so it still matches the original height.
2. A fake IEND chunk was inserted in the middle of the IDAT compressed data (plus the chunk lengths/CRCs are inconsistent).

How to recover

1. Initial Analysis

➜ The file started with a valid PNG signature (89 50 4E 47 0D 0A 1A 0A).
➜ IHDR chunk was present, but its CRC was wrong.
➜ Width = 724, Height = 800.
➜ There was an early IEND chunk in the middle of the file.
➜ Large amount of data existed after the early IEND.

2. Finding the real height

➜ The stored CRC of the IHDR chunk did not match the current height (800).
➜ I brute-forced the height value until the calculated CRC matched the stored CRC in the file.
➜ Correct height found: 850

3. Handling the fake IEND

➜ A fake IEND chunk (00 00 00 00 49 45 4E 44 AE 42 60 82) was inserted inside the compressed IDAT data.
➜ This broke normal PNG parsers.
➜ I removed those 12 bytes from the middle of the IDAT stream so the compressed data became continuous again.

4. Reconstructing the image data

➜ Extracted all IDAT compressed data (after removing the fake IEND).
➜ Used raw zlib inflate (wbits=-15) to decompress the pixel data.
➜ Applied PNG scanline unfiltering (None, Sub, Up, Average, Paeth filters).
➜ Rebuilt the image with correct dimensions: 724 × 850.

5. Result

➜ The bottom ~50 rows (which were previously hidden because height was reduced to 800) became visible.
➜ The flag was written in that hidden bottom area:

   flag{gOt_1t_in_plAin_sight}

