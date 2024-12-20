from Crypto.Cipher import AES



'''
CBC
''' #################################################################

'''
key: 140b41b22a29beb4061bda66b6747e14
IV: 4ca00ff4c898d61e1edbf1800618fb28
CT: 5b68629feb8606f9a6667670b75b38a528a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81
''' ########################################





'''
key: 140b41b22a29beb4061bda66b6747e14
IV: 5b68629feb8606f9a6667670b75b38a5
CT: 5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253
''' ########################################










def cbc_encrypt(key, iv, pt, is_hex = False, block_size = AES.block_size):

	if is_hex:
		key = key.decode("hex")
		iv = iv.decode("hex")
		pt = pt.decode("hex")

	assert len(key) is 16 and len(iv) is 16, "key and initialization vector lengths must each be 16 bytes"


	pad_bytes = block_size - len(pt) % block_size
	for i in range(pad_bytes):
		pt += chr(pad_bytes)


	cipher = AES.new(key, AES.MODE_CBC, iv)

	ct = iv + cipher.encrypt(pt)
	return ct




def cbc_decrypt(key, ct, is_hex = False, block_size = AES.block_size):

	if is_hex:
		key = key.decode("hex")
		ct = ct.decode("hex")

	assert len(key) is 16, "key length must be 16 bytes"

	iv = ct[:block_size]

	cipher = AES.new(key, AES.MODE_CBC, iv)
	pt = cipher.decrypt(ct[block_size:])

	unpad_bytes = ord(pt[-1])
	return pt[:-unpad_bytes]









key_hex = "140b41b22a29beb4061bda66b6747e14"
ct_hex = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"

print(cbc_decrypt(key_hex, ct_hex, True))
# Basic CBC mode encryption needs padding.




key_hex = "140b41b22a29beb4061bda66b6747e14"
ct_hex = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"

print(cbc_decrypt(key_hex, ct_hex, True))
# Our implementation uses rand. IV








key = "kkkkkkkkkkkkkkkk"
iv = "iviviviviviviviv"
pt = "the message i'm going to send, which is not a multiple of 16 bytes"

print

print(
      cbc_decrypt(
                  key,
                  cbc_encrypt(key, iv, pt)
                  )
      )



