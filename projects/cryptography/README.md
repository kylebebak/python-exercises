


'''
XOR and conversion in bash
''' #################################################################
# hex to ascii
# echo hexstring | xxd -r -p

# ascii to binary
# echo asciistring | xxd -b

# hex to binary
# echo hexstring | xxd -r -p | xxd -b

# binary to decimal
# printf '%x\n' "$((2#11010010))"
# printf '%x\n' "$((2#1101001011100011))"



'''
XOR and conversion in python
''' #################################################################
# ascii/binary to hex
# hex(ord('a'))
# 'a'.encode("hex")

# hex to ascii/binary
# binascii.a2b_hex('61')
# '61'.decode("hex")





# xor two strings of different lengths
def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))


def xor_hex_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs.decode("hex"), ys.decode("hex"))).encode("hex")




