from Crypto.Cipher import AES
from Crypto import Random


# key = b'Sixteen byte key'
key = 'Sixteen byte key'

iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)

# ct = iv + cipher.encrypt(b'Attack at dawn')
ct = iv + cipher.encrypt('Attack at dawn!!')


print("ct: " + ct.encode("hex"))
print("iv: " + iv.encode("hex"))


pt = cipher.decrypt(ct)

print(pt[AES.block_size:])


