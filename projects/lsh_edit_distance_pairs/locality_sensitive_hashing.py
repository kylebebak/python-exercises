import sys, pickle, time, itertools

start_time = time.time()


'''
input
''' #################################################################

m_file = open(sys.argv[1], 'rb')
m = pickle.load(m_file)
m_file.close()


signature_length = len(m[0])
rows_per_band = 6
bands = signature_length / rows_per_band


print 'read time: ' + str((time.time() - start_time)) + 's'








'''
main logic
''' #################################################################

# m is a d by s matrix all of whose values are ints. each row of m contains the signature for a given document. contiguous bands of this signature are concatenated to strings and hashed. any pair of documents with a pair of corresponding bands that are hashed to the same bucket is considered a candidate pair. it is worth mentioning that if doc_a and doc_b are hashed to the same bucket because of two identical bands at different locations of their signatures, this is no indication of their underlying similarity. to avoid hashing documents like this to the same bucket, the number of the band must also be concatenated to the band string being hashed. the hashing creates a map where a key-value pair is a hash value and the list of docs (with possible duplicates) that were hashed to this value

candidate_pairs_map = dict()

for d in range(len(m)):
	doc = m[d]

	for band in range(bands):

		band_elements = doc[rows_per_band * band:rows_per_band * (band + 1)]
		band_elements.append('b' + str(band))

		hash_value = hash(",".join(str(signature_element) for signature_element in band_elements))

		if hash_value in candidate_pairs_map:
			candidate_pairs_map[hash_value].append(d)
		else:
			candidate_pairs_map[hash_value] = [d]











'''
output
''' #################################################################

# using object serialization
output = open(sys.argv[1] + '.cm.' + str(rows_per_band) + '-rpb', 'wb')
pickle.dump(candidate_pairs_map, output)
output.close()



print 'execution time: ' + str((time.time() - start_time)) + 's'




