text=input("Enter the text: ")

print()

print("Char \t ASCII \t AND \t OR \t XOR")
for ch in text:
	val=ord(ch)
	print(f"{ch} \t {ord(ch)} \t{val&127} \t {val|127} \t {val^127}")

