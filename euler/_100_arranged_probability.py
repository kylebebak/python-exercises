import math




bottom = 1000000000000
while False:
    bottom += 1
    b = bottom * (bottom - 1)
    half_b = b / 2
    top_estimate = math.sqrt(half_b)

    if top_estimate % 1 == 0:
        continue
    if math.floor(top_estimate) * math.ceil(top_estimate) == half_b:
        print(bottom, math.ceil(top_estimate))
        break


b = 15
n = 21
target = 1000000000000

while n < target:
    btemp = 3*b + 2*n - 2
    ntemp = 4*b + 3*n - 3

    b = btemp
    n = ntemp

print(b,n)
