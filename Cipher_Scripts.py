import re
import numpy as np
import sympy as sp


ALPHABET = "ZABCDEFGHIJKLMNOPQRSTUVWXY"

def hill_cipher_key_invert(key):
    return key.inv_mod( len(ALPHABET) )

verbose = False
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

    percentile_group = 80
    percentile_value = np.percentile(np.array(counts),percentile_group)
    print ("values in or above the {}'th percentile ({:.2f})".format(percentile_group,percentile_value))
    for i in range(0,len(counts)):
        if counts[i] > percentile_value:
            print ( "shift of {:0>2}: {:<5}".format(i+1,counts[i]) )

print ("\n")
kasiski_examination('ct.txt',20)
print ("\n")

#key = sp.Matrix( ([1,0,4],[2,3,4],[7,3,1]) )
key = sp.Matrix( ([1,2,7],[0,3,3],[4,4,1]) )

plain_text = "FOURSCOREANDSEVENYEAR"
# Encrypt
cipher_text = hill_cipher(key, 3, plain_text)
# Decrypt
decrypted_text = hill_cipher(hill_cipher_key_invert(key), 3, cipher_text)
print( "OG_PT:{}\n   CT:{}\nDC_PT:{}".format(plain_text,cipher_text,decrypted_text) )
