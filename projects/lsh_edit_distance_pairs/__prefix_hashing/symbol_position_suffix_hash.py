import sys, itertools, time, pickle, helpers

start_time = time.time()



# in all of these docs, the minimum number of words, henceforth symbols, is 10. we are looking for pairs whose word level edit distance is no more than 1, allowing for replacement, addition, and removal of symbols. the jaccard distance between any such pair is therefore maximized when each of the docs is of minimum length (10), and the edit operation is replacement of one symbol for another. such docs would have 9 symbols in common. the intersection of the sets of their symbols would have size 9, and the union woudl have size 11, leading to a jaccard distance of 2 / 11. i will round the max jaccard distance up to .182 to make sure that there are no pairs of potentially similar docs which are not considered, i.e. there are no false negatives

# the first floor(JL + 1) symbols of each doc (henceforth the prefix) must be hashed to buckets such that they key is (symbol, symbol_position, suffix_length) and the value is the index of the doc



max_jaccard_distance = .182
max_edit_distance = 1
prefix_length = max_edit_distance + 1

candidate_pairs_map = dict()









'''
input and main logic
''' #################################################################


# read in docs one by one and hash symbols in their prefixes, such that the key value pairs in the map are symbol -> doc number
with open(sys.argv[1]) as f:
	for line in f:

		doc_num = int(line.split(' ', 1)[0])
		doc = line.split(' ', 1)[1].split()

		# prefix_length = int(len(doc) * max_jaccard_distance) + 1

		# symbol-position-suffix_length hash
		for s in range(0, prefix_length):
			bucket_index = doc[s] + ',' + str(s) + ',_' + str(length_of_doc - 1 - s)

			if bucket_index in candidate_pairs_map:
				candidate_pairs_map[bucket_index].append(doc_num)
			else:
				candidate_pairs_map[bucket_index] = [doc_num]


print
print 'prefix hashing time: ' + str((time.time() - start_time)) + 's'













# pairwise combinations are taken from hash buckets. these combinations are added to the set of tuples of candidate pairs, where the first document in any pair is always the one whose index is lower
candidate_pairs = set()
for probe_bucket_index, probe_doc_list in candidate_pairs_map.iteritems():

	# parse bucket index
	indices = probe_bucket_index.split(',')
	symbol = indices[0]
	i = int(indices[1])
	sl_probe = int(indices[2][1:])


	# use a list comprehension to generate tuples for all target indices that need to be checked

	for target_indices in [(j, sl_target) for j in range(prefix_length) for sl_target in range(sl_probe - max_edit_distance, sl_probe + max_edit_distance + 1) if 1 - i >= j + abs(sl_probe - sl_target)]:

		target_doc_list = candidate_pairs_map.get(symbol + ',' + str(target_indices[0]) + ',_' + str(target_indices[1]))

		# print probe_bucket_index, symbol + ',' + str(target_indices[0]) + ',_' + str(target_indices[1])

		# concatenate probe and target doc lists
		if target_doc_list is not None:
			for candidate_pair in itertools.combinations(sorted(set(probe_doc_list + target_doc_list)), 2):
				candidate_pairs.add(candidate_pair)




print
print 'pair computation time: ' + str((time.time() - start_time)) + 's'
print 'number of candidate pairs: ' + str(len(candidate_pairs))









'''
to see if a significantly reduced subset of the original doc list can be produced to pass to lsh, whose runtime is dominated by the number of docs it has to process rather than the number of pairs it has to compare. it turns out the answer to this is no... a test produced a subset of ~ 8000 docs from the original 10000, which won't make a big difference is the lsh runtime
''' ########################################
# docs = set()
# for candidate_pair in candidate_pairs:
# 	for doc_num in candidate_pair:
# 		docs.add(doc_num)

# print docs

# sys.exit()











'''
output
''' #################################################################

# using object serialization
output = open(sys.argv[1] + '.cps', 'wb')
pickle.dump(candidate_pairs, output)
output.close()

print
print 'execution time: ' + str((time.time() - start_time)) + 's'



