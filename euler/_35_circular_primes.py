import math
def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


# 10.4s >> 1.6s if non-eligible primes (primes at least one digit is even) are removed
candidate_primes = []
for n in range(3, 1000000 + 1):
    for c in str(n):
        if int(c) % 2 == 0:
            break
    else:
        if is_prime(n):
            candidate_primes.append(n)


circular_primes = set()
for p in candidate_primes:
    ps = str(p)
    cp = set()
    for c in range(0, len(ps)):
        pi = int(ps)
        if pi not in circular_primes and is_prime(pi):
            cp.add(pi)
            ps = ps[-1] + ps[:-1]
        else:
            break
    else:
        circular_primes = circular_primes | cp
circular_primes.add(2)


print(circular_primes)
print(len(circular_primes))
