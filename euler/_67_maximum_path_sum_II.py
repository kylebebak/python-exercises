triangle = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 3],
]

triangle = []
with open('assets/triangle.txt') as f:
    for line in f.readlines():
        row = str.strip(line).split()
        triangle.append(list(map(int, row)))



triangle = triangle[::-1]
previous_row = triangle[0]
for row in triangle[1:]:
    for i in range(len(row)):
        previous_row[i] = row[i] + max(previous_row[i], previous_row[i + 1])

print(previous_row)
