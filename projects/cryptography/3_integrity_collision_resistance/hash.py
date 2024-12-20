import sys
from Crypto.Hash import SHA256

# usage: python hash.py file
# https://class.coursera.org/crypto-013/quiz/attempt?quiz_id=122

file_blocks = list()

with open(sys.argv[1], 'rb') as f:
	while 1:
		last_kb = None
		kb = f.read(1024)

		if not kb:
			break

		file_blocks.append(kb)


block_hash = None
for block in reversed(file_blocks):
	if block_hash:
		block = block + block_hash.digest()

	block_hash = SHA256.new(block)

print(block_hash.hexdigest())


