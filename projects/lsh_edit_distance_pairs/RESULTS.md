/*
|-----------------------------------------------------------------
| for first 10000 docs in file
|-----------------------------------------------------------------
*/


kind of hashing: sh (symbol), sps (symbol-position-suffix), hh (half hash), lsh
# similar pairs: 20791, 20791, 20791, 20780 similar pairs with ed 1 or 0
# similar pairs with ed 1: 76, 76, 65



all missing pairs not found by lsh are those with ed = 1, which is not surprising, because strings that are identical (with ed = 0) are guaranteed to have the same lsh signature and therefore are guaranteed to be discovered by lsh, i.e. there can be no false negatives with ed = 0



false positive rate for sh is huge, ~ 1 - 20000/2000000 = 99%
false positive rate for for sps is about 87%
false positive rate for lsh is very small, < 1%
false positive rate for hh is very small, < 1%



lsh has some false negatives, (only 11 out of 20791), and very few false positives, < 1%. the other methods have no false negatives but lots of false positives


comparison of pairs with ed = 0 (identical strings) is much less costly because strings are checked for equality and not passed to the levenshtein function. the number of pairs with ed = 1 is very small in comparison with those with ed = 0. this means that even if the number of false positives was similar to the number of actual pairs, the time spent on comparison of pairs would be dominated by the number of false positives. in cases where there are many more false positives than actual pairs, as is the case with sh and sps, this effect is exaggerated. pair comparison with sps is roughly 15x faster than pair comparison with sh


with sps, the great majority of time is spent on pair comparison and not on generating pairs





half hash is better for ed = 1. it is comparable in speed and like the prefix methods has no false negatives, but it has many fewer false positives than the prefix methods







/*
|-----------------------------------------------------------------
| for first 1000000 docs in file
|-----------------------------------------------------------------
*/

candidate pairs: 13825751, similar pairs: 9119180
8905927 at dist = 0, 213253 at dist = 1
execution time: 479.394735098s



also, with all similar pairs written to standard output without deduplication, thus avoiding the use a set data structure to store all of the CP tuples, this took roughly 510 seconds, and produced a file of size ~ 350 mb with 28,000,000 pairs, ~70% of which needed to be deduplicated




/*
|-----------------------------------------------------------------
| for all 9397023 docs in file
|-----------------------------------------------------------------
*/


MEMORY usage is the issue

SOLUTION: i can write all of the unduplicated candidate pairs to a file, then i can sort/deduplicate the file unix sort or uniq commands, which can handle files that don't fit in memory by using what's called "external sorting", essentially reading chunks of the file into memory, sorting them, writing them to a temporary file and then merging these temporary files





python uses 24 BYTES to store an integer, and 40 bytes to store a 1 character string! this is because it stores an instance of the int or string class, and not just an int or string primitive. this means that instead of using 4 bytes per int, plus the overhead of placing the ints in a tuple

ints
>>> sys.getsizeof(10)
24
>>> sys.getsizeof(1000000)
24

strings
>>> sys.getsizeof('')
37
>>> sys.getsizeof('a')
38
>>> sys.getsizeof('ab')
39

tuples
>>> sys.getsizeof(('ab','cd'))
72
>>> sys.getsizeof((1,2))
72

lists
>>> sys.getsizeof([1,2])
88



sets
>>> a
set([(1, 2)])
>>> sys.getsizeof(a)
232


set([(7, 8), (54, 55), (92, 93), (94, 95), (40, 41), (18, 19), (74, 75), (80, 81), (89, 90), (6, 7), (76, 77), (51, 52), (11, 12), (27, 28), (25, 26), (28, 29), (35, 36), (36, 37), (33, 34), (29, 30), (14, 15), (97, 98), (96, 97), (55, 56), (17, 18), (72, 73), (48, 49), (99, 100), (45, 46), (83, 84), (46, 47), (15, 16), (22, 23), (69, 70), (8, 9), (71, 72), (87, 88), (65, 66), (58, 59), (12, 13), (68, 69), (16, 17), (37, 38), (73, 74), (62, 63), (50, 51), (23, 24), (38, 39), (77, 78), (3, 4), (49, 50), (57, 58), (84, 85), (66, 67), (59, 60), (34, 35), (42, 43), (61, 62), (82, 83), (13, 14), (95, 96), (32, 33), (93, 94), (75, 76), (39, 40), (64, 65), (41, 42), (2, 3), (90, 91), (43, 44), (53, 54), (47, 48), (85, 86), (67, 68), (30, 31), (79, 80), (10, 11), (52, 53), (5, 6), (98, 99), (31, 32), (1, 2), (24, 25), (70, 71), (63, 64), (56, 57), (4, 5), (0, 1), (91, 92), (60, 61), (9, 10), (78, 79), (44, 45), (19, 20), (86, 87), (81, 82), (26, 27), (21, 22), (88, 89), (20, 21)])
>>> len(a)
100
>>> sys.getsizeof(a)
8424



so, overhead clearly gets lower as more elements are added to a set, but in any case this set is using roughly 80 bytes per 2-int tuple, as opposed to something more reasonable like ~ 10 - 15! this means storing ~500,000,000 tuples in a set, even at 50 bytes per tuple, would use 25 gb of memory! yikes!





/*
|-----------------------------------------------------------------
| alternatives
|-----------------------------------------------------------------
*/

an interesing approach for finding all of the indentical sentences is to remove the line numbers

sed -E "s/^[0-9]+ //g" in_9397023 > in_9397023_no_line_numbers

sort the sentences with the unix sort, perhaps avoiding pipes and using temporary files along the way

sort in_9397023_no_line_numbers | uniq -c | sort -nr > in_9397023_sorted

and then taking all of the lines which had more than one occurence, and extracting this list of occurences with awk

awk '{print $1}' in_9397023_sorted | awk '$1 > 1' > 9397023_duplicates


then pass the list number of occurrences of each group of duplicate documents to a script which reads them into an array and prints a sum of the number of pairs generated by each group

python n_choose_2.py 9397023_duplicates

this returns 20715 pairs for the in_10000, which is the same number of edit distance 0 pairs returned by all of the hashing methods





duplicated documents: 1115005
total number of duplicate pairs: 426873920
this are the number of pairs that can be made from groups of duplicated docs in the big file

adding to this the number of ed = 1 doc pairs (2620033) gives us the total number of ed = 0 or ed = 1 pairs in the big file:
2620033 + 426873920 = 429493953

this is the correct answer


the ed = 1 doc pairs were computed with half_hash_no_dedup.py, in which the candidate pairs of the half_hash mapping were passed directly to the levenshtein function and only the pairs at edit distance 1 were printed to standard output. these pairs were then sorted and deduplicated to yield 2620033 unique pairs at edit distance 1. this avoids having python maintain a set of all candidate pairs (which isn't possible, because the set doesn't fit in memory), or trying to sort a document containing not only ed = 1 pairs but also ed = 0 pairs, which instead of containing roughly 3 million lines contained closer to 1.5 billion. sorting such a document is also impossible. even if the doc fit into memory (at ~15 bytes per line it has a size of over ~23gb, so it obviously doesn't), it would take roughly 

(1500000000 * math.log(1500000000,2)) / (3000000 * math.log(3000000,2))
= 708.346416425 times longer


but, the fact that the unix sort would have to use make use of the external sort would increase this by at least a factor of 4, which would lead to the sort taking at least 3000 times longer!

