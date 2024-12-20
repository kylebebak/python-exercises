'''
meet in the middle attack for solving an equation of the form h = g ** x in Zp, where p is a large prime, and h and g are large numbers less than p. x is not known, but it is in the range [0, 2 ** 40)

the package used for modular arithmetic is gmpy2

this is done by writing the equation as h * inv(g ** x0)  = (g ** B) ** x1 in Zp, where B = 2 ** 20, and x0, x1 are in the range [0, B). x0 is the lsd of x written in base B, and x1 is the msd

a hash table is built for all values of h * inv(g ** x0) in Zp, and then (g ** B) ** x1 in Zp is calculated for all x1 until a match is found in the hash table, and then x is reconstructed as x = B * x1 + x0




modular arithmetic
__________________________________________________


for exponentiation:
gmpy2.powmod(x, y, m) returns (x ** y) mod m


for finding the inverse:
gmpy2.divm(a, b, m) returns x such that b * x == a modulo m. raises a ZeroDivisionError exception if no such value x exists

gmpy2.divm(1, b, m) returns the inverse of b mod m



'''





import gmpy2
from gmpy2 import mpz


p = mpz('13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171')

g = mpz('11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568')

h = mpz('3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333')





# compute left-hand side, h * inv(g ** x0), for all x0 in [0, 2 ** 20). first, modulo exponentiation is performed, and then modulo inversion
B = 2 ** 20






# make hash table for all values of left-hand side of equation
lhs = dict()

for x0 in range(B):
	denom = gmpy2.powmod(g, x0, p)
	lhs[h * gmpy2.divm(1, denom, p) % p] = x0



# compute values of the right-hand side, (g ** B) ** x1, until there is a collision with one of the values in the hash table (i.e. a solution to the equation is found)
for x1 in range(B):
	base = gmpy2.powmod(g, B, p)
	rhs = gmpy2.powmod(base, x1, p)
	if rhs in lhs:
		print("x0: " + str(lhs[rhs]))
		print("x1: " + str(x1))


# x0: 787046
# x1: 357984


# x = B * x1 + x0
# 2 ** 20 * 357984 + 787046
# 375374217830


