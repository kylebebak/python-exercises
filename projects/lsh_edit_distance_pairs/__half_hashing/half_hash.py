import sys, itertools, time, helpers

start_time = time.time()





candidate_pairs_map = dict()
docs = list()







'''
input and main logic
''' #################################################################


# read in docs one by one, and hash the first and second halves of each doc such that the key -> value pairs in the map are doc_half -> doc_num. for the time being i'm not worried about numbering the halves -- this would avoid comparison of hypothetical false positives where the first half of one doc is identical to the second half of another doc. this is specifically designed for finding pairs of docs whose max word level edit distance is 1, and would not work for a max word-level edit distance > 1
with open(sys.argv[1]) as f:
	for line in f:


		doc_num = int(line.split(' ', 1)[0])
		docs.append(line.split(' ', 1)[1])
		doc = line.split(' ', 1)[1].split()


		l = len(doc)
		halves = list()


		if l % 2 == 0:
			halves.append(doc[0:l / 2])
			halves.append(doc[l / 2:l])
		else:
			halves.append(doc[0:l / 2])
			halves.append(doc[0:l / 2 + 1])
			halves.append(doc[l / 2 + 1:l])
			halves.append(doc[l / 2:l])

		# half hash
		for half in halves:
			half = ','.join(half)

			if half in candidate_pairs_map:
				candidate_pairs_map[half].append(doc_num)
			else:
				candidate_pairs_map[half] = [doc_num]




print 'half hashing time: ' + str((time.time() - start_time)) + 's'









# pairwise combinations are taken from each deduplicated list of documents that were hashed to the same bucket. these combinations are added to the set of tuples of candidate pairs, where the first document in any pair is always the one whose index is lower
candidate_pairs = set()
for bucket, doc_list in candidate_pairs_map.iteritems():
	if len(doc_list) > 1:
		for candidate_pair in itertools.combinations(sorted(set(doc_list)), 2):
			candidate_pairs.add(candidate_pair)




print 'pair computation time: ' + str((time.time() - start_time)) + 's'
print 'number of candidate pairs: ' + str(len(candidate_pairs))



# sys.exit()










'''
compare candidate pairs
''' #################################################################

levenshtein_threshold = 2

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
			# print str(candidate_pair) + ', dist = ' + str(levenshtein_distance)
			# print docs[candidate_pair[0]]
			# print docs[candidate_pair[1]]


print 'candidate pairs: ' + str(len(candidate_pairs)) + ', similar pairs: ' + str(similar_pair_counter)


print 'execution time: ' + str((time.time() - start_time)) + 's'
