import sys, random, time, pickle, numpy as np, helpers

start_time = time.time()



# shingles will be hashed to tokenized int values between 0 and universal_set_size - 1, henceforth a "shingle" is taken to mean its tokenized int value
universal_set_size = 100000
shingle_length = 2 # 10
signature_length = 50 # 100

# updated after input file is read
num_docs = 0







'''
input and main logic
''' #################################################################

docs_to_shingles = dict()

# build docs_to_shingles, which is a dict where each key-value pair is a doc number and the set of shingles belonging to the doc with that number
with open(sys.argv[1]) as f:
	for line in f:
		doc = line.split(' ', 1)[0]
		contents = line.split(' ', 1)[1]

		# shingles = helpers.get_shingles(contents, shingle_length)
		shingles = helpers.get_word_shingles(contents, shingle_length)
		docs_to_shingles[doc] = set()

		for shingle in shingles:
			docs_to_shingles[doc].add(hash(shingle) % universal_set_size)


num_docs = len(docs_to_shingles)


print 'shingling time: ' + str((time.time() - start_time)) + 's'



# invert docs_to_shingles to build shingles_to_docs, which is a dict where each key-value pair is a shingle and the list of numbers of the corresponding docs in which it appears

shingles_to_docs = dict()
for i in range(0, universal_set_size):
	shingles_to_docs[i] = list()

for doc in docs_to_shingles:
	for shingle in docs_to_shingles[doc]:
		shingles_to_docs[shingle].append(doc)






# create a family of hash functions and insert them into a list whose size will be the signature length of the minhash values
hash_function_family = list()

random.seed()
hash_family_seeds = random.sample(xrange(pow(2, 32)), signature_length)

for seed in hash_family_seeds:
	hash_function_family.append(helpers.hash_function(seed, universal_set_size))

random.seed()



# initialize a d by s signature matrix of nested lists with infinite numeric values, where d is the number of documents and s is the length of the signature. an m[doc][sig] matrix is preferable to an m[sig][doc] because the bottleneck operation is comparing the entire signature of a doc against the minhash_values for a given shingle to see which elements of the signature for that doc will be updated. this comparison is done much faster by indexing into a doc and retrieving its entire signature than by indexing one by one into elements of the signature and looking up that element's value for a given doc
m = [[float('inf') for x in xrange(signature_length)] for x in xrange(num_docs)]


# populate the signature matrix
for shingle in shingles_to_docs:
	minhash_values = list()
	for hash_function in hash_function_family:
		minhash_values.append(hash_function(shingle))

	for doc in shingles_to_docs[shingle]:
		doc_sig = m[int(doc)]
		for i in range(0, signature_length):
			if minhash_values[i] < doc_sig[i]:
				m[int(doc)][i] = minhash_values[i]








'''
output
''' #################################################################

# using object serialization
output = open(sys.argv[1] + '.mh.' + str(shingle_length) + '-sh', 'wb')
pickle.dump(m, output)
output.close()

# using numpy to write object to output
# m = np.array(m)
# np.savetxt('minhash_matrix.txt', m, fmt='%i')

print 'execution time: ' + str((time.time() - start_time)) + 's'






