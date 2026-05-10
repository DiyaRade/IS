IP=[1,5,2,0,3,7,4,6]
IP_INV=[3,0,2,4,6,1,7,5]
EP=[3,0,1,2,1,2,3,0]
P4=[1,3,2,0]

S0=[
	[1,0,3,2],
	[2,1,0,3],
	[3,2,1,0],
	[0,3,2,1]
]

S1=[
	[0,1,2,3],
	[3,0,1,2],
	[2,3,0,1],
	[1,2,3,0]
]

def permute(bits,table):
	return ''.join(bits[i] for i in table)

def xor(a,b):
	result=""
	for i in range(len(a)):
		result+=str(int(a[i]) ^ int(b[i]))
	return result

def sbox_lookup(bits,sbox):
	row=int(bits[0] +bits[3],2)
	col=int(bits[1] +bits[2],2)
	value=sbox[row][col]
	return format(value,'02b')

def generate_key(master_key):
	key=[]
	for i in range(16):
		shifted=master_key[i:] + master_key[:i]
		key.append(shifted[:8])
	return key

def feistal(right,key):
	expanded=permute(right,EP)
	xored=xor(expanded,key)
	left=xored[:4]
	right_half=xored[4:]
	s0=sbox_lookup(left,S0)
	s1=sbox_lookup(right_half,S1)
	combined=s0+s1
	return permute(combined,P4)

def encrypt(plaintext,round_keys):
	bits=permute(plaintext,IP)
	left=bits[:4]
	right=bits[4:]
	for i in range(16):
		temp=feistal(right,round_keys[i])
		new_right=xor(left,temp)
		left=right
		right=new_right
	combined=right+left
	return permute(combined,IP_INV)

def decrypt(cipher,round_keys):
	bits=permute(cipher,IP)
	left=bits[:4]
	right=bits[4:]
	for i in range(15,-1,-1):
		temp=feistal(right,round_keys[i])
		new_right=xor(left,temp)
		left=right
		right=new_right
	combined=right+left
	return permute(combined,IP_INV)

text=input("Enter string: ")
key=input("Enter key: ")

roundkeys=generate_key(key)
cipher=encrypt(text,roundkeys)
print("Encrypted string: ",cipher)
plain=decrypt(cipher,roundkeys)
print("Decrypted string: ",plain)