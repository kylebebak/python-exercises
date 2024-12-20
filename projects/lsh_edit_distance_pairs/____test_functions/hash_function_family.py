import random



_memomask = {}
def hash_function(n):
	mask = _memomask.get(n)
	if mask is None:
		random.seed(n)
		mask = _memomask[n] = random.getrandbits(32)
	def myhash(x):
		return hash(x) ^ mask
	return myhash





random.seed()

hash_functions = list()

hash_family_seeds = random.sample(xrange(1000000), 100)
for seed in hash_family_seeds:
	hash_functions.append(hash_function(seed))

for hf in hash_functions:
	print hf(1)
