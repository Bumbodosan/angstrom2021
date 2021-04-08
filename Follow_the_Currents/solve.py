import os
import zlib

'''
Disclaimer: Doesn't seem to work on windows, I don't know why...

The insight is that the keystream is initialized with one of 256**2 possible pairs of bytes. 
256**2 = 65536 is a pretty small number so we can just generate all keystreams and try all until 
we get a decrypted text containing "actf{". 
'''

def keystream(key):
    index = 0
    while 1:
        index += 1
        if index >= len(key):
            key += zlib.crc32(key).to_bytes(4,'big')
        yield key[index]


with open("enc", "rb") as f:
    enc = f.read()

for i in range(256):
    for j in range(256):
        k = keystream(bytes([i, j]))
        keys = []
        for _ in range(len(enc)):
            keys.append(next(k))
        
        res = bytes([c ^ key for c, key in zip(enc, keys)])

        if b"actf{" in res:
            print(res)
