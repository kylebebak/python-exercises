import xor





def random(size = 16):
    return open("/dev/urandom").read(size)




msgs = ['hey there now doc', 'this is a big big', 'encrypted string', 'with lots of text', 'that someone will', 'enjoy reading and', 'they will find out']
tgt = 'for their purposes'

msgs = ['a a a a ', 'b b b b ']
tgt = ' a b c d'

key = random(1024)



cts = [xor.xor_strings(key, msg) for msg in msgs]
ct_tgt = xor.xor_strings(key, tgt)


for ct in cts:
    print(xor.xor_strings(key, ct))

print

for ct in cts:
    print(xor.xor_strings(ct, ct_tgt))
