# return word-level levenshtein distance between two strings with words separated by spaces
def levenshtein_dist_word_level(s1, s2):

	if len(s1.split()) < len(s2.split()):
		return levenshtein_dist_word_level(s2, s1)

	# split input strings on spaces to make input lists of words. because python indexes into strings the same way as it does into lists, all of the remaining code is identical. c1 refers to the word from s1 being considered, while c2 refers to the word from s2 being considered
	s1 = s1.split()
	s2 = s2.split()

	# the below assumes len(s1) >= len(s2)
	if len(s2) == 0:
		return len(s1)

	previous_row = range(len(s2) + 1)
	for i in range(len(s1)):
		current_row = [i + 1]
		for j in range(len(s2)):
			insertions = previous_row[j + 1] + 1
			# j+1 instead of j since previous_row and current_row are one character longer than s2
			deletions = current_row[j] + 1
			substitutions = previous_row[j] + (s1[i] != s2[j])
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row

	return previous_row[-1]
