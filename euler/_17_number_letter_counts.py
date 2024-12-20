
words = [
[191, ['one']],
[190, ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']],
[10, ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']],
[100, ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']],
[900, ['hundred']],
[1, ['thousand']],
[891, ['and']],
]

num_letters = 0

for word in words:
    num_letters += word[0] * len(''.join(word[1]))


print(num_letters)



