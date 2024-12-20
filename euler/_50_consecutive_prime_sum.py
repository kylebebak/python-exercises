
import math
def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


primes = []
sum_of_primes = 0
prime_sums_of_primes = []
candidate_prime = 2
while True:
    if is_prime(candidate_prime):
        sum_of_primes += candidate_prime
        if sum_of_primes < 1000000:
            primes.append(candidate_prime)
        else:
            break

        if is_prime(sum_of_primes):
            prime_sums_of_primes.append((len(primes), sum_of_primes))
    candidate_prime += 1



for i in range(1, len(primes) - prime_sums_of_primes[-1][0]):
    s = sum(primes[i:])
    if is_prime(s):
        print(i, s)
