import sys, pickle, time, itertools, helpers

start_time = time.time()


'''
input
''' #################################################################

# read candidate pairs map
cm_file = open(sys.argv[1], 'rb')
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


print 'candidate pairs: ' + str(len(candidate_pairs))


print 'execution time: ' + str((time.time() - start_time)) + 's'
