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
