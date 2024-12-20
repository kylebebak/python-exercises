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


# read in docs one by one and hash symbols in their prefixes, such that the key -> value pairs in the map are symbol -> doc number
with open(sys.argv[1]) as f:
	for line in f:

		doc_num = int(line.split(' ', 1)[0])
		doc = line.split(' ', 1)[1].split()

		# prefix_length = int(len(doc) * max_jaccard_distance) + 1


		# symbol hash
		for s in range(0, prefix_length):
			symbol = doc[s]

			if symbol in candidate_pairs_map:
				candidate_pairs_map[symbol].append(doc_num)
			else:
				candidate_pairs_map[symbol] = [doc_num]




print 'prefix hashing time: ' + str((time.time() - start_time)) + 's'












# pairwise combinations are taken from each deduplicated list of documents that were hashed to the same bucket. these combinations are added to the set of tuples of candidate pairs, where the first document in any pair is always the one whose index is lower
candidate_pairs = set()
for bucket, doc_list in candidate_pairs_map.iteritems():
	if len(doc_list) > 1:
		for candidate_pair in itertools.combinations(sorted(set(doc_list)), 2):
			candidate_pairs.add(candidate_pair)




print 'pair computation time: ' + str((time.time() - start_time)) + 's'
print 'number of candidate pairs: ' + str(len(candidate_pairs))
















'''
output
''' #################################################################

# using object serialization
output = open(sys.argv[1] + '.cps', 'wb')
pickle.dump(candidate_pairs, output)
output.close()


print 'execution time: ' + str((time.time() - start_time)) + 's'



