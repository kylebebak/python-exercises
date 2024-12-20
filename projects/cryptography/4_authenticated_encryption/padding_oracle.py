'''
f20bdba6ff29eed7b046d1df9fb70000||58b1ffb4210a580f748b4ac714c001bd||4a61044426fb515dad3f21f18aa577c0||bdf302936266926ff37dbf7035d5eeb4
16 byte random iv || 48 byte encoded aes message

i.e. 48 byte ct, with 128 bits (16 bytes) per block. so, there are 3 ct blocks and 3 pt blocks. to decrypt the third pt block, the second CT block is modified. to decrypt the second PT block, the first CT block is modified. to compute the first PT block, the IV block is modified

python padding_oracle.py f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb51000000000000000000bdf302936266926ff37dbf7035d5eeb4
doesn't work




python padding_oracle.py f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4
valid message

python padding_oracle.py f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0
invalid, bad padding

python padding_oracle.py f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd
invalid, bad padding

The Magic Words are Squeamish Os + [7 chars + 9 padding chars]


when a decrypted cbc ciphertext ends in an invalid pad the web server returns a 403 error code (forbidden request). when the cbc padding is valid, but the message is malformed, the web server returns a 404 error code (url not found)
'''


import urllib2, sys




class PaddingOracle(object):
	def query(self, q):
		# create query url
		target = 'http://crypto-class.appspot.com/po?er=' + urllib2.quote(q)
		# send http request to server
		req = urllib2.Request(target)
		try:
			urllib2.urlopen(req)
			print("no error")
			return 0
		except urllib2.HTTPError as e:
			# print(e.code)
			if e.code == 404:
				print(str(e.code) + " : good padding")
				return 1
			return 2





class CipherBlockPair:



	''' class variables and static methods
	______________________________ '''
	block_length = 16
	block_length_raw = 32

	@staticmethod
	def dec_to_hex(d):
		assert d >= 0 and d < 256 and type(d) is int, "d must be from 0 to 255 inclusive"
		return hex(d)[2:].zfill(2)

	@staticmethod
	def xor(xs, ys):
		return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs.decode("hex"), ys.decode("hex"))).encode("hex")



	''' constructor
	______________________________ '''
	def __init__(self, first, second, pre = "", n = 0):
		self.first = [first[i-2:i] for i in range(len(first), 0, -2)]
		self.first_bkp = list(self.first)

		self.second = second
		self.pre = pre

		self.n = n
		self.pad = CipherBlockPair.dec_to_hex(self.n + 1)
		self.chars = list()
		for i in range(self.n):
			self.chars.append(self.pad)

		self.prepare()


		self.guess = ""



	''' setters
	______________________________ '''
	# prepare all correctly guessed characters with current pad
	def prepare(self):
		for i in range(self.n):
			self.first[i] = CipherBlockPair.xor(CipherBlockPair.xor(self.pad, self.chars[i]), self.first_bkp[i])
		print(self.chars)


	def guess_last_char(self, g):
		assert g >= 0 and g < 256 and type(g) is int, "g must be from 0 to 255 inclusive"
		self.guess = CipherBlockPair.dec_to_hex(g)

		# xor unguessed char with pad and with guess
		self.first[self.n] = CipherBlockPair.xor(CipherBlockPair.xor(self.pad, self.guess), self.first_bkp[self.n])


	def set_last_char(self):
		# invoke this method if the most recent guess for the last char is correct
		self.chars.append(self.guess)
		# increment number of correct chars and update pad
		self.n = len(self.chars)
		self.pad = CipherBlockPair.dec_to_hex(self.n + 1)

		# prepare all correctly guessed characters with new pad
		self.prepare()



	''' getters
	______________________________ '''
	# preceding block, reverse and join hex char array to create string for first block, second block
	def get_ct(self):
		return self.pre + "".join(self.first[::-1]) + self.second








''' main logic of program
__________________________________________________ '''
bl = CipherBlockPair.block_length
blr = CipherBlockPair.block_length_raw


# create array of 16 byte CT blocks (32 hex chars each)
ct = sys.argv[1]
blocks = [ct[i:i+blr] for i in range(0, len(ct), blr)]

# remove last CT block if it's incomplete
if len(sys.argv[1]) % blr != 0:
	del blocks[-1]



# instantiate cipher block pairs and add them to list, starting with the last CT blocks
cbs = list()
for i in range(len(blocks) - 1, 0, -1):
	if i == len(blocks) - 1:
		# once you know how many padding bytes are in the leading block...
		# cbs.append(CipherBlockPair(blocks[i - 1], blocks[i], "".join(blocks[0:i-1]), n = int(sys.argv[2])))
		cbs.append(CipherBlockPair(blocks[i - 1], blocks[i], "".join(blocks[0:i-1])))
	else:
		cbs.append(CipherBlockPair(blocks[i - 1], blocks[i], "".join(blocks[0:i-1])))



for cb in cbs:
	print(cb.get_ct())
print("______________________________")
print



# instantiate padding oracle, empty plaintext string
po = PaddingOracle()
pt = ''





# iterate over all characters in all block cipher pairs and use the padding oracle to decode the plaintext one char at a time
for cb in cbs:
	for i in range(bl):

		for g in range(256):
			cb.guess_last_char(g)
			print(g)

			if po.query(cb.get_ct()) == 1:
				# print("guess: " + str(g) + ", " + str(cb.get_ct()))

				cb.set_last_char()

				pt = CipherBlockPair.dec_to_hex(g) + pt
				print(pt.decode('hex'))

				break







