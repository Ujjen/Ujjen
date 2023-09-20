'''7- and 8-bit ASCII binary decoding function - Team Stegosaurus - CSC 442 001'''
import sys

# reading the binary using stdin
binary = sys.stdin.readline().strip()

length = len(binary)

# checking whether the ASCII code is 7 bit or 8 bit
if length % 7 == 0:
    bits = 7
if length % 8 == 0:
    bits = 8

def bintochr(binstr: str, bit: int) -> str:
    '''Decodes the binary-encoded ASCII using a given bit length'''
    charVal = ''

    # splits the string into groups of [bit] bits and converts them
    for i in range(0, len(binstr), bit):
        decimal = int(binstr[i:i + bit], 2)
        charVal += chr(decimal)

    return charVal

# writing the output using stdout
if length % 7 == 0 and length % 8 == 0: # if ASCII code can be represented by both 7 and 8 bits
    sys.stdout.write('7-bit decoding: ' + bintochr(binary, 7) + '\n')
    sys.stdout.write('8-bit decoding: ' + bintochr(binary, 8) + '\n')
else:
    sys.stdout.write(bintochr(binary, bits) + '\n')
