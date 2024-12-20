import json
from mmap import ACCESS_READ, mmap

from custom.mixins import ComparableHashableMixin


class Node(ComparableHashableMixin):
    """Helper class for building Huffman encoding tree."""
    def __init__(self, count, left=None, right=None, char=None):
        self.count = count
        self.left = left
        self.right = right
        self.char = char

    def __lt__(self, other):
        return self.count < other.count


class Huffman:
    """Class for encoding (compressing) and decoding (decompressing)
    text files using Huffman encoding."""
    def __init__(self, in_file):
        self.in_file = in_file
        # count characters in input file
        char_count = dict()
        with open(in_file) as f:
            for line in f:
                for char in line:
                    char_count[char] = char_count[char]+1 if char in char_count else 1

        # build set of nodes
        nodes = set()
        for char, count in char_count.items():
            nodes.add(Node(count, None, None, char))

        # build tree from bottom up
        while len(nodes) > 1:
            left, right = sorted(nodes)[:2]
            nodes.remove(left)
            nodes.remove(right)
            nodes.add(Node(left.count+right.count, left, right))

        # get head, and traverse tree to construct codes for each leaf node (char)
        head = nodes.pop()
        self.char_code = dict()

        def preorder(node, code=''):
            if node.left is not None:
                preorder(node.left, code+'0')
                preorder(node.right, code+'1')
            else:
                self.char_code[node.char] = code
        preorder(head)

    def codes(self):
        return self.char_code

    def encode(self, out_file, code_file=None):
        """Encodes (compresses) the input file using the Huffman
        encoding built in the __init__ method."""
        code_file = out_file+'.encoding' if code_file is None else code_file
        with open(self.in_file) as i:
            with open(out_file, "wb") as o:

                bit_count, block = [0, '']
                for line in i:
                    for char in line:
                        code = self.char_code[char]
                        bit_count += len(code)
                        block += code
                        while len(block) > 8:
                            bits, block = block[:8], block[8:]
                            bits = int(bits, 2)
                            o.write(bytes([bits]))
                # pad remaining bits and write them to file
                if len(block):
                    bits = int(block.ljust(8, '0'), 2)
                    o.write(bytes([bits]))

        # write coding and bit count to separate file
        code_char = {v: k for k, v in self.char_code.items()}
        code_char['BITCOUNT'] = bit_count
        json.dump(code_char, open(code_file, 'w'))

    @staticmethod
    def decode(in_file, code_file=None):
        """Accepts an encoded file and a file with the encoding scheme,
        and decodes (decompresses) the file byte by byte."""
        code_file = in_file+'.encoding' if code_file is None else code_file
        code_char = json.load(open(code_file))

        BITCOUNT, bit_count, i, block, text = [int(code_char['BITCOUNT']), 0, 1, '', '']
        with open(in_file, "rb") as f, mmap(f.fileno(), 0, access=ACCESS_READ) as mm:
            for byte in mm:
                block += bin(byte[0])[2:].zfill(8)
                while i <= len(block):
                    if block[:i] in code_char:
                        text += code_char[block[:i]]
                        block = block[i:]
                        bit_count += i
                        i = 1
                        if bit_count >= BITCOUNT:
                            return text
                    else:
                        i += 1
        return text






if __name__ == '__main__':
    import sys

    in_file, out_file = sys.argv[1:3]
    h = Huffman(in_file)
    h.encode(out_file)
    print(Huffman.decode(out_file))


