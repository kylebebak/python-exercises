import sys

with open(sys.argv[1]) as f:
    duplicates = f.readlines()


def n_choose_2(n):
    return n * (n - 1) / 2


sum = 0

for n in duplicates:
    sum += n_choose_2(int(n))

print "duplicated documents:", len(duplicates)
print "total number of duplicates:", sum
