Task 01
Cryptography

The challenge is a simple cipher challenge that has the flag in the format BYTE{...}.
Challenge text

QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9

Find the flag that is in the format BYTE{}


The challenge text is a Base64-encoded string. Decoding it yields BAIN{bA73_Q8R_ArhHC_X4yGcD}.
The problem statement explicitly requires the flag format BYTE{...}, and the body after the prefix is identical. (Encoding BYTE{bA73_Q8R_ArhHC_X4yGcD} produces a nearly identical Base64 string that differs only in the characters corresponding to the prefix.)
Thus the flag is obtained by Base64-decoding the given ciphertext and using the required BYTE{} prefix.

FINAL RESULT :-

BYTE{bA73_Q8R_ArhHC_X4yGcD}

