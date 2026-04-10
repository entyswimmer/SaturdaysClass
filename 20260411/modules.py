import hashlib
import secrets
import binascii

# 基本演算関数
def euclid(a, b):
    while b:
        a, b = b, a % b
    return a

def exEuclid(a, b):
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    
    while b != 0:
        q = a // b 
        a, b = b, a % b  
        x0, x1 = x1, x0 - q * x1  
        y0, y1 = y1, y0 - q * y1 
        
    if a == 1:
        output = [a, x0, y0]
        return output
    else:
        print("解は存在しません")
        return None

def lcm(a, b):
    return a*b // euclid(a, b)

def inv(a, n):
    output = exEuclid(a, n)
    if output:
        return output[1] % n
    else:
        print("逆元は存在しません")
        return None

def mod_binary(g, k, p):
    ans = 1
    g = g%p
    while k>0:
        if k%2 == 1:
            ans = (ans*g)%p
        g = (g*g)%p
        k = k//2
    return ans

def fermat_test(n, a):
    if euclid(a, n) != 1:
        return False
    return mod_binary(a, n - 1, n) == 1

def fermat_primegen2(iv_bit, k):
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    primes = []
    n = iv_bit // 8
    rb = secrets.token_bytes(n) 
    iv = int(binascii.hexlify(rb), 16)
    n = iv if iv % 2 == 1 else iv + 1  
    
    while True:
        passed = True
        for i in range(k):
            a = bases[i % len(bases)]
            if not fermat_test(n, a):
                passed = False
                break
        if passed:
            return n  
        n += 2

#　必要な鍵生成
def rsaKeygen(p, q):
    n = p * q
    phi = lcm(p - 1, q - 1) 
    iv_bit = 1024
    k = 10
    while True:
        e = fermat_primegen2(iv_bit, k)
        if 1 < e < phi and euclid(e, phi) == 1:
            break
    d = inv(e, phi)

    public_key = [n, e]
    private_key = d
    
    return public_key, private_key

#　RSA暗号化と復号化
def rsaEnc(m, n, e):
    c = mod_binary(m, e, n)
    return c

def rsaDec(c, n, d):
    m = mod_binary(c, d, n)
    return m

# ハッシュ化関数
def shake128(m, h_size):
    mh = hashlib.shake_128(m.encode()).hexdigest(h_size)
    return int(mh, 16)

def makeHash(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# 電子署名作成の関数
def rsaSignGen(m, n, d):
    h_size = 127
    m_hased = shake128(m, h_size)
    sigma = mod_binary(m_hased, d, n)
    return sigma

# 電子署名検証の関数
def rsaSignVerify(m, sigma, n, e):
    h_size = 127
    m_hashed = shake128(m, h_size)
    verify = mod_binary(sigma, e, n)
    if m_hashed == verify:
        return True
    else:
        return False

# 文字変換
def int_to_str(m):
    hex_str = format(m, 'x')  
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str  
    byte_data = binascii.unhexlify(hex_str)
    try:
        return byte_data.decode('utf-8')    
    except UnicodeDecodeError:
        print("error")
        return None
        
def str_to_int(m):
    m_bytes = m.encode('utf-8')                       
    m_hex = binascii.hexlify(m_bytes)                 
    m_int = int(m_hex, 16)                           
    return m_int



