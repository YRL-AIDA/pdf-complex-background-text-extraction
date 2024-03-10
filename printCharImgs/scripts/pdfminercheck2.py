import re
import string
from pprint import pprint

# Input string containing tuples
# \
input_string = """BT\n/F1 1 Tf\n22 0 0 22 207.4294 444.0927 Tm\n0 0 0 1 k\n/GS2 gs\n-0.0043 Tc\n
[(\x01\x02\x03\x04\x05\x06\x07\x04\x08\x08\t\\012\x0b\x0c)-68.2(\\015\x04\x08\x06\x0e\x0b)]
TJ\n-2.7991 -1.2275 TD\n-0.0042 Tc\n
[(\x0f\x10\x0b\x11\x04\x02\x08\t\x12\x13\x0e\x14\x07\t\x07\x14\x15\x0c)-33.5(\x0e\x04\x16\t\x0e\\012\x14\x17\x0c)-33.5(\x18\x0c)-33.5(\x19\x1a\x0c)-33.5(\x1b\x04\x06)]
TJ\n/F2 1 Tf\n14 0 0 14 252.4666 362.6941 Tm\n-0.0049 Tc\n
[(\x01\x02\x03\x04\x05\x06\x07)-67.9(\x08)]
TJ\n11 0 0 11 257.0597 68.1022 Tm\n-0.0038 Tc\n
[(\t\\012\x0b\x0c\\015\x0e\x0f\x07)-113.6(\x10\x11\x11\x08)]
TJ\n/F1 1 Tf\n30 0 0 30 245.2369 570.9539 Tm\n/GS1 gs\n0.0018 Tc\n
(\x1c\x1d\x10\x1e\x1f !)
Tj\n-2.1562 -1.2007 TD\n0.0015 Tc\n
(\x1c\x01\x10\x10\x1e"\x1f\x01\x1c \x1e\x1d#$\x1f\x01%)
Tj\n1.9705 -1.1993 TD\n0.0009 Tc\n(&\x10\x1e \'  )Tj\nET\n"""
pattern = r"(F\d+\s[\s\S]*?)(?=F\d+|$)"
q = re.findall(pattern, input_string)
p = r'(\[.*?\]|\([^()]*?\))'
p = r'\((.*?)\)'
hex_pattern = r'\\x(..)'

# def convert_to_decimal(value):
#     hex_match = re.search(hex_pattern, value)
#     if hex_match:
#         return str(int(hex_match.group(1), 16))
#     elif value.startswith('\\'):
#         return str(int(value[1:], 8))
#     else:
#         return eval(value)
def convert_to_decimal(value):
    if value.startswith('\\x'):
        return str(int(value[3:], 16))
    elif value.startswith('\\'):
        return str(int(value[2:], 8))
    else:
        return str(ord(value))

def filter_out_junk(text):
    return ''.join(x for x in text if x in set(string.printable))
result = []
print(result)
hex_oct_pattern = r'\\(?:x([0-9A-Fa-f]{2})|([0-7]{3}))'
for match in q:
    left_side = re.match(r'F\d+', match).group(0)  # Extract "F#" string from the beginning of each match
    right_side = re.findall(p, match)  # Extract characters within parentheses and square brackets
    for value in right_side:
        for char in re.findall(hex_oct_pattern, value):
            print(q)
    right_side_decimal = [convert_to_decimal(char) for value in right_side for char in re.findall(hex_oct_pattern, value)]

    result.append((left_side, right_side))

print(result)
