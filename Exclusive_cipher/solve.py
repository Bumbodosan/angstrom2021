from pwn import xor

'''
We know the key is 5 bytes and we conveniently know the flag starts with the 5 bytes actf{
The resulting string from xoring with actf{ should therefore contain the 5 byte key, this we can brute force
'''

cipher = bytes.fromhex("ae27eb3a148c3cf031079921ea3315cd27eb7d02882bf724169921eb3a469920e07d0b883bf63c018869a5090e8868e331078a68ec2e468c2bf13b1d9a20ea0208882de12e398c2df60211852deb021f823dda35079b2dda25099f35ab7d218227e17d0a982bee7d098368f13503cd27f135039f68e62f1f9d3cea7c")
potential_keys = xor(cipher, b"actf{")

for i in range(len(potential_keys) - 5):
	res = xor(cipher, potential_keys[i : i + 5])
	if b"actf" in res:
		print(res.decode())
