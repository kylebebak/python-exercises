
ch = ''
counter = 1
while len(ch) < 1000000:
    ch += str(counter)
    counter += 1

digits = [1, 10, 100, 1000, 10000, 100000, 1000000]
product = 1
for digit in digits:
    product *= int(ch[digit - 1])

print(product)
