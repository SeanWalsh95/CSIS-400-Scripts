import re
import operator
import numpy as np
import sympy as sp
from collections import Counter

verbose = False

ENG_FRQ = {
    'A' : 0.08167,
    'B' : 0.01492,
    'C' : 0.02782,
    'D' : 0.04253,
    'E' : 0.12702,
    'F' : 0.02228,
    'G' : 0.02015,
    'H' : 0.06094,
    'I' : 0.06966,
    'J' : 0.00153,
    'K' : 0.00772,
    'L' : 0.04025,
    'M' : 0.02406,
    'N' : 0.06749,
    'O' : 0.07507,
    'P' : 0.01929,
    'Q' : 0.00095,
    'R' : 0.05987,
    'S' : 0.06327,
    'T' : 0.09056,
    'U' : 0.02758,
    'V' : 0.00978,
    'W' : 0.02360,
    'X' : 0.00150,
    'Y' : 0.01974, 
    'Z' : 0.00074 
    }

COMMON_CHARS = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

ALPHABET = "ZABCDEFGHIJKLMNOPQRSTUVWXY"

def euclids_gcd(a,b):
    print("{:>10} % {:<10} = {}".format(a,b,a%b))
    if a % b == 0:
        return b
    else:
        return euclids_gcd(b, a % b)


def hill_cipher_key_invert(key):
    return key.inv_mod( len(ALPHABET) )

def hill_cipher(matrix_key, block_size, string):
    blocks = [string[i:i+block_size] for i in range(0, len(string), block_size)]
    string = ""
    for block in blocks:
        char_int_list = [ALPHABET.find(char) for char in block]
        new_block = ""
        for char_int in matrix_key.dot( (char_int_list) ):
            new_block += ALPHABET[ char_int % len(ALPHABET) ]
        string += new_block
        if verbose:
            print( "{} -> {}".format(block , new_block) )
    if verbose:
        print ("\n")
    return string

def kasiski_examination(file_in,number_of_shifts):
    ct = ""
    with open(file_in, 'r') as file:
        ct=file.read().replace('\n', '')
    ct = re.sub('[.,?!"\'-]', '', ct)

    counts = []
    for i in range(0,number_of_shifts):
        counts.append(0)
        shifted_ct = ct[i+1:]
        for j in range(0,len(shifted_ct)):
            if ct[j] == shifted_ct[j] and ct[j] != " ":
                counts[i] += 1

    probable_shifts = []
    percentile_group = 80
    percentile_value = np.percentile(np.array(counts),percentile_group)
    print ("shift values in or above the {}'th percentile ({:.2f})".format(percentile_group,percentile_value))
    for i in range(0,len(counts)):
        if counts[i] > percentile_value:
            probable_shifts.append(i+1)
            print ( "shift of {:0>2}: {:<5}".format(i+1,counts[i]) )

    return probable_shifts

# returns a list of occurrences of characters based of on a offest
def count_chars(file_in,offset):
    ct = ""
    with open(file_in, 'r') as file:
        ct=file.read().replace('\n', '')
    ct = re.sub('[.,?!"\'-]', '', ct)

    frequency_list = []

    # combines every n'th character for frequency analysis
    freq_matches = [ct[i::offset] for i in range(offset)]
    for string in freq_matches:
        percent_freq = {}
        count = Counter(string)
        total_count =sum(count.values())
        for char in count:
            percent_freq[char] = round(count[char]/total_count, 5)
        frequency_list.append(percent_freq)

    return frequency_list



print ("\n")
kasiski_examination('ct.txt',20)
print ("\n")
print(sorted(ENG_FRQ.items(), key=operator.itemgetter(1)))
print ("\n")
char_freq_list = count_chars('ct.txt',5)
for char_freq in char_freq_list:
    print(sorted(char_freq.items(), key=operator.itemgetter(1)))
print ("\n")

#key = sp.Matrix( ([1,0,4],[2,3,4],[7,3,1]) )
key = sp.Matrix( ([1,2,7],[0,3,3],[4,4,1]) )

plain_text = "FOURSCOREANDSEVENYEAR"
# Encrypt
cipher_text = hill_cipher(key, 3, plain_text)
# Decrypt
decrypted_text = hill_cipher(hill_cipher_key_invert(key), 3, cipher_text)
print( "OG_PT:{}\n   CT:{}\nDC_PT:{}".format(plain_text,cipher_text,decrypted_text) )

print("\n")

print("GCD:{}".format(euclids_gcd(1201,160)))

print("\n")

