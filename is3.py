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



# Convert text to binary
def text_to_binary(text):
	binary=''
	for ch in text:
		binary += format(ord(ch),'08b')
	return binary

# Convert binary to text
def binary_to_text(binary):
	text=''
	for i in range(0,len(binary),8):
		byte=binary[i:i+8]
		text += chr(int(byte,2))
	return text


text=input("Enter string: ")
key=input("Enter 8-bit key: ")
binary_key=text_to_binary(key)
roundkeys=generate_key(binary_key)

binary_text=text_to_binary(text)

cipher_binary=''

# Encrypt each 8-bit block
for i in range(0,len(binary_text),8):
	block=binary_text[i:i+8]

	# padding if block less than 8 bits
	if len(block) < 8:
		block = block.ljust(8,'0')

	cipher_binary += encrypt(block,roundkeys)

print("Encrypted Binary:",cipher_binary)

# Decrypt
decrypted_binary=''

for i in range(0,len(cipher_binary),8):
	block=cipher_binary[i:i+8]
	decrypted_binary += decrypt(block,roundkeys)

plain=binary_to_text(decrypted_binary)

print("Decrypted String:",plain)
