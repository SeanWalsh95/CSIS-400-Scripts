import re
import numpy as np

ALPHABET = "ZABCDEFGHIJKLMNOPQRSTUVWXY"

def hill_cipher_get_blocks(pt_string, block_size):
    return [pt_string[i:i+block_size] for i in range(0, len(pt_string), block_size)]

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
def hill_cipher_encrypt_block(matrix_key_string, block_string):
    key = np.matrix(matrix_key_string)
    char_int_list = []
    for char in block_string:
        char_int_list.append(ALPHABET.find(char))
    encrypted_block = ""
    for num in (key.dot(np.array(char_int_list))%26).tolist()[0]:
        encrypted_block += ALPHABET[num]
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

    for i in range(0,len(counts)):
        print ( "shift of {:0>2}: {:<5}".format(i+1,counts[i]) )


print ("\n")
kasisk_examination('ct.txt',10)
print ("\n")

print ("encrypted blocks:")
for block in hill_cipher_get_blocks("FOURSCOREAND",3):
    print("{} -> {}".format(block ,hill_cipher_encrypt_block("1,2,7;0,3,3;4,4,1",block) ) )

print ("\n")