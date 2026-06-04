# Breaking Crypto the Simple Way

Keys and Security
Cryptography relies on the idea that keys must be computationally infeasible to guess.

    - Length: A 128-bit key has 2^128 possibilities → impossible to crack via brute force with modern hardware.
    - Entropy: Keys must be random and not derived from predictable inputs (e.g., timestamps).

    - Uniqueness: Each key must be unique to prevent correlation attacks.

Practical example:

An 8-character alphanumeric password has ~62^8 combinations (~2.18e14).

An AES-128 key has 2^128 combinations (~3.4e38). → The difference is enormous.

## RSA Basics
RSA is based on the difficulty of factoring large numbers.

Public Key:
- 𝑛=𝑝×𝑞 (product of two large primes)
- 𝑒 (public exponent, commonly 65537).

### Private Key:
- 𝜑(𝑛)=(𝑝−1)(𝑞−1).
- 𝑑=𝑒−1 mod 𝜑(𝑛).

Example:

```python
from Crypto.Util.number import inverse, long_to_bytes

# Primos pequeños (solo para demo)
p = 61
q = 53
n = p * q
e = 17
phi = (p-1)*(q-1)

# Clave privada
d = inverse(e, phi)

# Ciphertext
c = 855

# Descifrado
m = pow(c, d, n)
print("Plaintext:", m)
```
In this example, the encrypted message c is decrypted using the private key d.
In practice, the prime numbers are very large (1024–4096 bits) → factoring 
𝑛  is impractical.

### Vulnerabilities
Weak primes: if 𝑝 or 𝑞 are small or poorly generated, RSA can be broken.

Shared primes: if two keys share a prime, both can be factored.

Low-entropy keys: predictable inputs → facilitate attacks.

Real-world example:

If 𝑛 has only 77 digits (like the one you worked with), Sympy can factor it.

In real RSA,𝑛 has hundreds of digits → factoring it is impractical.

### Conclusion
The security of cryptography depends on the length, entropy, and uniqueness of the keys.

RSA is strong only if the primes are large and well-generated.

Documenting practical examples (such as factoring a small 𝑛 and decrypting a ciphertext) shows how theory connects to offensive practice.

### How Factorisation Time Increases Exponentially
To demonstrate how factoring time grows with larger primes, we will test factorisation for different values of (n = p * q) using Python.

```python
import time
from sympy.ntheory import factorint

# Small n (product of two small primes)
n_small = 253  # 11 × 23
start = time.time()
factorint(n_small)
print(f"Time to factor {n_small}: {time.time() - start:.6f} seconds")

# Medium n
n_medium = 988027  # 941 × 1051
start = time.time()
factorint(n_medium)
print(f"Time to factor {n_medium}: {time.time() - start:.6f} seconds")

# Large n
n_large = 2147483647  # A large prime
start = time.time()
factorint(n_large)
print(f"Time to factor {n_large}: {time.time() - start:.6f} seconds")
```
The above script will have an output of:

```
Time to factor 253: 0.000019 seconds
Time to factor 988027: 0.000041 seconds
Time to factor 2147483647: 0.000094 seconds
```
As prime numbers grow larger, factorisation time increases exponentially, making brute-force factorisation infeasible for properly generated RSA keys.

### “P’s and Q’s” & RSA Weaknesses
Core Idea
RSA security depends on the primes 𝑝 and 𝑞 being large, random, and unique.
The “P’s and Q’s” paper shows that when this fails, critical vulnerabilities arise:

Predictable primes: if generated with a weak RNG (e.g., seed = system time), an attacker can reproduce the process and obtain 𝑝 and 𝑞.

Shared primes: if two keys share the same prime, it suffices to compute gcd⁡(𝑛1,𝑛2) to break both.

Primes that are too close: if 𝑝≈𝑞, algorithms such as Fermat’s factorization can factor 𝑛 quickly.

GCD exploits: the calculation of gcd⁡(𝑛1,𝑛2) is polynomial and trivial in practice.

### Educational Example in Python
- Factorization

```python
from sympy import factorint
from Crypto.Util.number import inverse, long_to_bytes

n = 43941819371451617899582143885098799360907134939870946637129466519309346255747
factors = factorint(n)
p, q = factors.keys()
print("p =", p)
print("q =", q)
```
- Calculate φ(n)

```python 
phi_n = (p - 1) * (q - 1)
print("Phi(n) =", phi_n)
```
- Get private key

```python 
e = 65537
d = inverse(e, phi_n)
print("Private key (d):", d)
```
- Decrypt ciphertext

```python 
c = 9002431156311360251224219512084136121048022631163334079215596223698721862766
plaintext = pow(c, d, n)
flag = long_to_bytes(plaintext)
print("Decrypted Plaintext:", flag.decode())
```

### Key Takeaways
Never use small or predictable primes → they make attacks easier.

Avoid small public exponents (e.g., 𝑒=3); use 𝑒=65537.

Use random padding (PKCS#1, OAEP) to prevent mathematical attacks.

Key diversity: do not reuse primes or plaintexts across recipients.

- Conclusion
The exercise demonstrates how, if 𝑛 is composed of weak primes, it can be factored and the plaintext recovered. In real RSA, the primes are enormous and generated using secure RNGs, making this attack impractical.

```python
from Crypto.Util.number import inverse, long_to_bytes

# Primos factorizados
p = 205237461320000835821812139013267110933
q = 214102333408513040694153189550512987959
n = p * q

# Calcular phi
phi_n = (p - 1) * (q - 1)

# Exponente público
e = 65537

# Clave privada
d = inverse(e, phi_n)

# Ciphertext
c = 9002431156311360251224219512084136121048022631163334079215596223698721862766

# Descifrado
plaintext = pow(c, d, n)
flag = long_to_bytes(plaintext)
print(flag.decode())
```

# Breaking hashes

- What is Hashing?
Hashing transforms an input (e.g., password, message) into a fixed-length string.

One-way: it cannot be reversed to obtain the original input.

- Main uses:
Password storage (storing hashes instead of passwords).

Data integrity (verifying that a file has not been altered).

Message authentication (HMAC with a secret key).

- Vulnerabilities in Hashing Weak algorithms: 
MD5 and SHA-1 → insecure due to collisions.

No salting: same input → same hash → attackers use rainbow tables.

- Insecure HMACs: 
if the hash function is weak or the key is short/predictable.

SHA-256 for passwords: too fast → allows billions of attempts per second on a GPU.

### Example – Hashing a Password

```python
import hashlib

password = "mypassword123"
hash_sha256 = hashlib.sha256(password.encode()).hexdigest()
print("SHA-256:", hash_sha256)
```
- Output: a 64-character hexadecimal hash.
 Secure for data integrity, not for storing passwords.

 ### Password Hashing Schemes (PHS)
Functions designed to be slow and adaptable:

    - bcrypt

    - Argon2

    - PBKDF2

- Example using bcrypt:

```python 
import bcrypt

password = b"mypassword123"
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password, salt)
print("bcrypt:", hashed)
```
-  bcrypt allows you to adjust the “cost” (rounds) → slower = more secure against brute-force attacks.

- Choosing the Right Hash
    - Passwords → Argon2, bcrypt, PBKDF2 (slow and adaptable).

    - Data integrity → SHA-256, SHA-3, BLAKE2 (fast and efficient).

    - Message authentication → HMAC-SHA256, HMAC-SHA3.

- Key Takeaway
Hashing ≠ absolute security.

SHA-256 is excellent for integrity and digital signatures.

For passwords, speed is the enemy → use hashing functions designed to slow down attacks.

# 
# HMAC Challenge Summary
Concept
HMAC (Hash-based Message Authentication Code) combines a cryptographic hash (SHA-1 in this case) with a secret key.

It is used to verify the integrity and authenticity of a message.

If the key is weak, an attacker can recover it and generate valid HMACs → manipulate messages.

- Example of the challenge
    - Message: CanYouGuessMySecret

    - Digest (SHA1): 1484c3a5d65a55d70984b4d10b1884bda8876c1d

    - Objective: to find the secret key used in the HMAC.

### Step 1 – Save the hash and message:
```
echo -n "1484c3a5d65a55d70984b4d10b1884bda8876c1d:CanYouGuessMySecret" > digest.txt
```
### Step 2 – Run Hashcat
```
hashcat -a 0 -m 150 digest.txt /usr/share/wordlists/rockyou.txt
```
    - -m 150 → modo HMAC‑SHA1.

### Step 3 – Result
Hashcat tests millions of passwords per second.
When it finds the correct one, it displays:
```
1484c3a5d65a55d70984b4d10b1884bda8876c1d:CanYouGuessMySecret:<secret_key>
Status: Cracked
```
- The value <secret_key> is the recovered weak key.


- The programme compares the calculated digest with the digest you had (1484c3a5d65a55d70984b4d10b1884bda8876c1d).

The output you showed appears as follows:
```
1484c3a5d65a55d70984b4d10b1884bda8876c1d:CanYouGuessMySecret:sunshine
Status...........: Cracked
Recovered........: 1/1 (100.00%) Digests
```
That third field (sunshine) is the key that has been found.
Hashcat displays it alongside the message and the original digest, confirming that this key generates exactly the same HMAC.

### Key Takeaways
Short or common passwords → easy to crack using dictionary attacks.

SHA-1 is no longer secure for critical integrity applications.

- Best practices:

    - Use long, random passwords.

    - Avoid SHA-1 → opt for SHA-256 or SHA-3.

    - Do not reuse passwords across multiple systems.

### Conclusion
This exercise demonstrates how an HMAC with a weak key can be easily cracked using tools such as Hashcat. In practice, security depends on both the hash function and the strength of the key.

# Risks of Exposing Cryptographic Keys in Client-Side Code


- Why It’s Dangerous
When a key is embedded in code that runs in the browser (JavaScript, front-end frameworks), any user can inspect it using developer tools. This undermines the security that the key is intended to provide.

- Key Risks
Unauthorised Access: an attacker can use the key to decrypt sensitive data or authenticate against APIs.

- Data Tampering: with the key, signed payloads can be generated or encrypted messages modified, bypassing integrity checks.

- API Abuse: exposed API keys allow unauthorised access to privileged endpoints.

Common Scenarios
Hardcoded API Keys in JavaScript: visible in the source code, accessible from the browser.

- Encryption Keys in Client-Side Frameworks: included in libraries for local encryption, easy to extract.

- Unsecured Config Files: configuration files exposed in the application containing credentials in plain text.

Example:
```javascript
// ❌ Insecure: hardcoded API key in client-side code
const apiKey = "ABCD1234SECRET";
fetch(`https://api.example.com/data?key=${apiKey}`);

```
-  Anyone who opens DevTools can view the API key and misuse the API.

### Best Practices
Never embed keys in client-side code.

Use server-side storage for keys and credentials.

Environment variables and secret management systems (Vault, AWS Secrets Manager).

Rotate keys regularly and apply the principle of least privilege.

### Conclusion
Exposing keys on the client is like leaving the door open: any attacker can get in. Security depends on keeping keys out of the end user’s reach, managed on the server and protected by good DevOps practices.

###  Client-Side Key Exposure
- Concept
The website encrypts messages on the client side using JavaScript with a hardcoded key (1234567890123456).
This allows an attacker to:

Extract the key directly from the code.

Automate the encryption of potential messages.

Send requests to the server until the correct message is found.

- Example of the attack
Brute force script:

```python
import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Configuration
url = "http://bcts.thm/labs/lab3/process.php"
encryption_key = b"1234567890123456"  # Must be 16 bytes (same as in the JavaScript)
wordlist_path = "wordlist.txt"        # Path to the wordlist

# Function to encrypt a message
def encrypt_message(message, iv):
    # Pad the message to a multiple of the block size (16 bytes for AES)
    padded_message = pad(message.encode(), AES.block_size)
    # Encrypt using AES-CBC
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_message)
    # Encode ciphertext and IV in Base64 for transmission
    return base64.b64encode(ciphertext).decode(), base64.b64encode(iv).decode()

# Function to send the payload
def send_payload(ciphertext, iv):
    payload = {"data": ciphertext, "iv": iv}
    response = requests.post(url, json=payload)
    return response.text

# Main bruteforce function
def bruteforce():
    with open(wordlist_path, "r") as f:
        words = f.readlines()

    for word in words:
        word = word.strip()
        print(f"Trying: {word}")
        # Generate a random IV (16 bytes)
        iv = AES.get_random_bytes(16)
        # Encrypt the current word
        ciphertext, iv_base64 = encrypt_message(word, iv)
        # Send the payload to the server
        response = send_payload(ciphertext, iv_base64)
        print(f"Response: {response}")
        # Check if the response indicates success
        if "Access granted!" in response:
            print(f"[+] Found the correct message: {word}")
            break

if __name__ == "__main__":
    bruteforce()

```

Brute-force script (simplified):
```python 
import requests, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

url = "http://bcts.thm/labs/lab3/process.php"
key = b"1234567890123456"

def encrypt(msg, iv):
    padded = pad(msg.encode(), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(padded)).decode(), base64.b64encode(iv).decode()

def send(ciphertext, iv):
    return requests.post(url, json={"data": ciphertext, "iv": iv}).text

with open("wordlist.txt") as f:
    for word in f:
        iv = AES.get_random_bytes(16)
        ct, iv_b64 = encrypt(word.strip(), iv)
        resp = send(ct, iv_b64)
        if "Access granted!" in resp:
            print(f"[+] Found: {word.strip()}")
            print(resp)
            break
```

- Expected output:
```
Trying: qdmicq
Response: Message qdmicq is invalid!
[--snip--]
Response: Access granted! Here's your flag: THM{XXXXXXXXXXXXXXXXXXXXXXX}
[+] Found the correct message: XXXXXXXXXXX

```

### Key Takeaways
- Never Hardcode Keys: any user can inspect the code and retrieve them.

- Secure Key Management: use secure storage on the server (AWS KMS, Azure Key Vault).

- Backend Encryption: encrypt and decrypt on the server, never on the client.

- Developer Awareness: many developers make this mistake out of ignorance.

### Conclusion
This exercise demonstrates how a hardcoded key in JavaScript renders security illusory: simply automating the process is enough to retrieve the message and the flag. The correct practice is to manage keys on the backend and never expose them on the client.


# Bit Flipping Attacks

- Unauthenticated Encryption
Concept
Unauthenticated encryption: encryption that does not verify the integrity or authenticity of the ciphertext.

The system decrypts any data received, even if it has been tampered with.

This allows for attacks such as bit flipping, where the attacker modifies the ciphertext and controls changes to the plaintext.

- Main risk
AES-CBC without authentication: encrypts securely, but does not detect alterations.

If an attacker changes bits in a block of ciphertext, the corresponding block of plaintext is modified in a predictable manner.

The system accepts this as valid because there is no integrity check.

### Example – Bit Flipping Attack
Suppose the encrypted payload contains:

```json
{"role":"0"}
```
The attacker alters the ciphertext whilst it is in transit.

- Upon decryption, the system obtains:

```json
{"role":"1"}
```
-  Result: the attacker escalated privileges without needing to crack the password or the algorithm.

### Mitigación
- Usar cifrado autenticado: AES‑GCM, ChaCha20‑Poly1305.

- Agre gar MAC/HMAC: verificar integridad antes de aceptar datos.

Nunca confiar en ciphertext sin validación.

### Conclusión
El cifrado sin autenticación es como un candado sin sello de seguridad: protege contra miradas externas, pero no detecta si alguien lo manipuló. Los ataques de bit flipping muestran que confidencialidad sin integridad no es suficiente en sistemas criptográficos.

### Unauthenticated Encryption – Bit Flipping Demo
Background
The PHP code generates cookies:

auth_token → contains the encrypted username.

role → contains the encrypted value ‘0’.

As the encryption is AES-CBC without authentication, the system accepts any ciphertext and decrypts it without checking integrity. This allows the IV or the ciphertext to be manipulated to change the plaintext.

- Example of an attack
Bit flipping script

```python 
import base64, sys
from binascii import unhexlify, hexlify

original_token = sys.argv[1]  # token cifrado del cookie "role"

cipher_bytes = bytearray(unhexlify(original_token))
block_size = 16

print("\n[DEBUG] Original IV (First 16 Bytes):", hexlify(cipher_bytes[:block_size]).decode())

# Queremos cambiar '0' -> '1'
xor_diff = [0x01]

for i, diff in enumerate(xor_diff):
    print(f"[DEBUG] Modifying byte at offset {i}: {hex(cipher_bytes[i])} XOR {hex(diff)}")
    cipher_bytes[i] ^= diff

print("\n[DEBUG] Modified IV (First 16 Bytes):", hexlify(cipher_bytes[:block_size]).decode())

modified_token = hexlify(cipher_bytes).decode()
print("\nModified Token:\n", modified_token)
print("\nUse this token as the new 'role' cookie in your browser to log in as admin.")

```
- Expected output

```
[DEBUG] Original IV (First 16 Bytes): fc16a0b6f9b185f987fbe88e21e9ebc9
[DEBUG] Modifying byte at offset 0: 0xfc XOR 0x1
[DEBUG] Modified IV (First 16 Bytes): fd16a0b6f9b185f987fbe88e21e9ebc9

Modified Token:
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

```
- When you replace the “role” cookie with the modified token and refresh the page, the system interprets “role”:'1' as admin access.

### Key Takeaways
Confidentiality ≠ Integrity: encrypting without authentication allows data to be manipulated.

AES-CBC without a MAC is vulnerable to bit flipping.

- Mitigation: use authenticated modes (AES-GCM, ChaCha20-Poly1305) or add a MAC/HMAC to validate integrity.

Never trust ciphertext without verification.

### Conclusion
This example shows how an attacker can escalate privileges simply by altering the IV/ciphertext, without needing to know the key. It is practical proof that an application using encryption without authentication is exposed to direct manipulation.

