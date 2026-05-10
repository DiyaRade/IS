import math

def gcd(a,b):
	while b:
		a,b=b,a%b
	return a

def mod_inverse(e,phi):
	g,x,_=extended_gcd(e,phi)
	if g!=1:
		return None
	return x%phi

def extended_gcd(a,b):
	if a==0:
		return b,0,1
	g,x,y=extended_gcd(b%a,a)
	return g,y - (b//a) *x, x

def is_prime(n):
	if n<2:
		return False
	for i in range(2,int(math.sqrt(n))+1):
		if n%i==0:
			return False
	return True

def generate_keys(p,q):
	n=p*q
	phi=(p-1)*(q-1)
	
	e=2
	while e<phi:
		if gcd(e,phi)==1:
			break
		e+=1

	d=mod_inverse(e,phi)
	return (e,n),(d,n)

def encrypt(plain,public):
	e,n=public
	return ''.join(chr(pow(ord(ch),e,n)) for ch in plain)

def decrypt(cipher,private):
	d,n=private
	return ''.join(chr(pow(ord(ch),d,n)) for ch in cipher)

p=int(input("Enter prime p: "))
q=int(input("Enter prime q: "))

if not is_prime(p) or not is_prime(q):
	print("Both numbers should be prime")
else:
	public,private=generate_keys(p,q)
	print(f"Public key (e,n): {public}")
	print(f"Private key (d,n): {private}")
	
	msg=input("Enter text: ")
	
	e=encrypt(msg,public)
	print(f"Encrypted message: {e}")
	d=decrypt(e,private)
	print(f"Decrypted message: {d}")
