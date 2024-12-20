from Crypto.Cipher import AES
from Crypto.Util import Counter







'''
CTR
''' #################################################################

'''
key: 36f18357be4dbd77f050515c73fcf9f2
IV: 69dda8455c7dd4254bf353b773304eec
CT: 0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329
''' ########################################







'''
key: 36f18357be4dbd77f050515c73fcf9f2
IV: 770b80259ec33beb2561358a9f2dc617
CT: e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451
''' ########################################







def ctr_encrypt(key, iv, pt, is_hex = False, block_size = AES.block_size):

	if is_hex:
		key = key.decode("hex")
		iv = iv.decode("hex")
		pt = pt.decode("hex")


	assert len(key) is 16 and len(iv) is 16, "key and initialization vector lengths must each be 16 bytes"


	ctr = Counter.new(128, initial_value = long(iv.encode("hex"), 16))
	cipher = AES.new(key, AES.MODE_CTR, counter = ctr)

	ct = iv + cipher.encrypt(pt)
	return ct




def ctr_decrypt(key, ct, is_hex = False, block_size = AES.block_size):

	if is_hex:
		key = key.decode("hex")
		ct = ct.decode("hex")

	assert len(key) is 16, "key length must be 16 bytes"

	iv = ct[:block_size]

	ctr = Counter.new(128, initial_value = long(iv.encode("hex"), 16))
	cipher = AES.new(key, AES.MODE_CTR, counter = ctr)

	pt = cipher.decrypt(ct[block_size:])

	return pt








key_hex = "36f18357be4dbd77f050515c73fcf9f2"
ct_hex = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"

print(ctr_decrypt(key_hex, ct_hex, True))
# Basic CBC mode encryption needs padding.




key_hex = "36f18357be4dbd77f050515c73fcf9f2"
ct_hex = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"

print(ctr_decrypt(key_hex, ct_hex, True))
# Our implementation uses rand. IV











key = "kkkkkkkkkkkkkkkk"
iv = "iviviviviviviviv"
pt = "the message i'm going to send, which is not a multiple of 16 bytes"

print

print(
      ctr_decrypt(
                  key,
                  ctr_encrypt(key, iv, pt)
                  )
      )
