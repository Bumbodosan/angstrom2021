from pwn import remote
from Crypto.Util.number import inverse

'''
If we assume we know the number of characters in the flag we can work through what happens when the substitution function is called. 
Here is 4 variables, yi is the ith flag character, v is "value" from chall, all is mod 691:
    reduce() process: y1 => v * y1 + y2 => (v * y1 + y2) * v + y3 => ((v * y1 + y2) * v + y3) * v + y4

We rewrite the final formula:
    ((v * y1 + y2) * v + y3) * v + y4 = v^3 * y1 + v^2 * y2 + v * y3 + y4

If we try different values for v we get:
    v1^3 * y1 + v1^2 * y2 + v1 * y3 + y4 = k1 (mod p)
    v2^3 * y1 + v2^2 * y2 + v2 * y3 + y4 = k2 (mod p)
    v3^3 * y1 + v3^2 * y2 + v3 * y3 + y4 = k3 (mod p)

Since we know all vi^j and we can make a request for each ki this is simply an equation system mod p (p = 691) which we can solve using Gauss-Jordan. 

Again this is only possible if we know how many variables are involved but the flag probably isn't very long so we can just test a few and keep the one containing "actf{". 
(Turns out the flag was 40 characters long, 1 longer than my initial solve script brute-forced because I used range(40) which took me some time to figure out :P)
'''

r = remote("crypto.2021.chall.actf.co", "21601")
r.recvuntil("technique\n")

p = 691

for n in range(7, 60):
    print("Size:", n)
    matrix = [[0] * (n + 1) for _ in range(n)]
    for row in range(n):
        for col in range(n):
            matrix[row][col] = pow(row, n - col - 1, p)
    
    for i in range(n):
        r.recvuntil("> ")
        r.sendline(str(i))
        matrix[i][n] = int(r.recvline().decode().strip()[len(">> ") : ])
    
    for row in range(n):
        col = row
        if matrix[row][col] == 0:
            for i in range(row, n):
                if matrix[i][col] != 0:
                    temp = matrix[i].copy()
                    matrix[i] = matrix[row]
                    matrix[row] = temp
                    break
        
        coeff = inverse(matrix[row][col], p)
        for i in range(col, n + 1):
            matrix[row][i] = (matrix[row][i] * coeff) % p
        
        for i in range(n):
            if i != row:
                prev_val = matrix[i][col]
                for j in range(col, n + 1):
                    mult = (prev_val * matrix[row][j]) % p
                    res = (matrix[i][j] - mult) % p
                    if res < 0:
                        matrix[i][j] = res + p
                    else:
                        matrix[i][j] = res
        # print("\n".join([str(i) for i in matrix]) + "\n")
        solved = [0] * n
        for i in range(n):
            solved[i] = matrix[i][n]
        flag = "".join([chr(i % 128) for i in solved])
        if "actf{" in flag:
            print(flag)

r.close()
