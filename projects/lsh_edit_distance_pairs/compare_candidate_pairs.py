import sys, pickle, time, itertools, helpers

start_time = time.time()



# any doc pair with word-level levenshtein distance below this threshold will be printed to standard output
levenshtein_threshold = 2



'''
input
''' #################################################################

# read in all documents and store them in a list
docs = list()

with open(sys.argv[1]) as f:
	for line in f:
		docs.append(line.split(' ', 1)[1])


# read in candidate pairs map using object serialization
cm_file = open(sys.argv[2], 'rb')
candidate_pairs_map = pickle.load(cm_file)
cm_file.close()



print 'read time: ' + str((time.time() - start_time)) + 's'





'''
main logic
''' #################################################################

# pairwise combinations are taken from each deduplicated list of documents that were hashed to the same bucket for a given band. these combinations are added to the set of tuples of candidate pairs, where the first document in any pair is always the one whose index is lower
candidate_pairs = set()
for bucket, doc_list in candidate_pairs_map.iteritems():
	if len(doc_list) > 1:
		for candidate_pair in itertools.combinations(sorted(set(doc_list)), 2):
			candidate_pairs.add(candidate_pair)






# compare all candidate pairs and print those whose word-level levenshtein distance is below a certain threshhold
similar_pair_counter = 0

for candidate_pair in candidate_pairs:

	if docs[candidate_pair[0]] == docs[candidate_pair[1]]:
		similar_pair_counter += 1
		print str(candidate_pair) + ', dist = 0'
	else:
		levenshtein_distance = helpers.levenshtein_dist_word_level(docs[candidate_pair[0]], docs[candidate_pair[1]])
		if levenshtein_distance < levenshtein_threshold:
			similar_pair_counter += 1
			print str(candidate_pair) + ', dist = ' + str(levenshtein_distance)
			# print docs[candidate_pair[0]]
			# print docs[candidate_pair[1]]

print 'candidate pairs: ' + str(len(candidate_pairs)) + ', similar pairs: ' + str(similar_pair_counter)


print 'execution time: ' + str((time.time() - start_time)) + 's'
