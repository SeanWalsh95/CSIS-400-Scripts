import re
import numpy as np
import statistics as stat
import math

ALPHABET = "ZABCDEFGHIJKLMNOPQRSTUVWXY"

def hill_cipher_key_invert(key):
    determinate = np.linalg.det(key).round()
    inverse_key = np.matrix( key.I * determinate ).round()
    print ("Inverse Key: \n{}\n".format(inverse_key))
    modded_inverse_key = inverse_key % len(ALPHABET)
    return modded_inverse_key

def hill_cipher_get_blocks(pt_string, block_size):
    return [pt_string[i:i+block_size] for i in range(0, len(pt_string), block_size)]

def get_str_as_int_list(string):
    int_list=[]
    for char in string:
        int_list.append(ALPHABET.find(char))
    return  int_list

# ---------------------------------------
# Testing code for hill_cipher_encrypt_block
# ---------------------------------------
# a = np.array([[1,2,7],[0,3,3],[4,4,1]])
# b = np.array([6,15,21])
# c = a @ b
# new_string = ""
# for num in c:
#     new_string += ALPHABET[num % 26]
# print (new_string)
# ---------------------------------------
def hill_cipher_encrypt_block(matrix_key, block_string):
    char_int_list = get_str_as_int_list(block_string)
    encrypted_block = ""
    for num in (matrix_key.dot(np.array(char_int_list))%len(ALPHABET)).tolist()[0]:
        encrypted_block += ALPHABET[int(num)]
    return encrypted_block

def kasisk_examination(file_in,number_of_shifts):
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



key = "1,2,7;0,3,3;4,4,1"
#key = "1,0,4;2,3,4;7,3,1"
print(key)

print ("\n")
kasisk_examination('ct.txt',20)
print ("\n")

print ("encrypted blocks:")
for block in hill_cipher_get_blocks("FOURSCOREANDSEVENYEAR",3):
    print("{} -> {}".format(block ,hill_cipher_encrypt_block(np.matrix(key),block) ) )

rev_key = "9,0,16;14,1,3;12,22,23"
#rev_key = "9,14,12;0,1,22;15,3,23"


print ("decrypted blocks:")
for block in hill_cipher_get_blocks("ADAYNUHQGEBLACNZMWCEP",3):
    print("{} -> {}".format(block ,hill_cipher_encrypt_block(np.matrix(rev_key),block) ) )
