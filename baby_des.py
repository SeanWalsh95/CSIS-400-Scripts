import numpy as np
import sympy as sp

class des_block(object):
    
    def __init__(self, bitstring):
        if not isinstance(bitstring, str):
            raise TypeError("param must be string")
        self.left = str(bitstring[0:6])
        self.right = str(bitstring[6:12])
        self.round = 0
    
def DES_function(R,key):
    S_box_L = ["101","010","001","110","011","100","111","000","001","100","110","010","000","111","101","011"]
    S_box_R = ["100","000","110","101","111","001","011","010","101","011","000","111","110","010","001","100"]
    
    # Expand R from 6 to 8 bits  1,2,4,3,4,3,5,6
    R_exp = R[0:2] + R[3] + R[2:4] + R[2] + R[4:6]
    
    # ( Expanded R ) XOR ( key ) = 8 bit value for S-boxes
    S = bin( int(R_exp,2) ^ int(key,2) )[2:].zfill(8)
    
    # Retrieve values from S-boxes 
    S_box_L_result = S_box_L[ int( S[0:4],2 ) ]
    S_box_R_result = S_box_R[ int( S[4:8],2 ) ]
    
    # Combine S-box values and return result as new R
    R = S_box_L_result + S_box_R_result
    
    return R
    
def DES_round(block, key):
    
    if not isinstance(block, des_block):
        raise TypeError("block must be of type des_block")
    
    R = block.right
    L = block.left
    
    # perform DES function on R with key
    f_result = DES_function(R, key)
    
    # XOR result of DES function with L
    R = bin( int(L,2) ^ int(f_result,2) )[2:].zfill(6)
    
    # increase round count for both halves
    block.round += 1
    
    # Swap halves and return block n+1
    block.left = R
    block.right = L
    
    return block
    
def encrypt_DES(data, key, rounds):
    
    output = ""
    
    for b in range(0, len(data), 12):
        print( data[b:b+12] )
        block = des_block( data[b:b+12] )
        for i in range(0,rounds):
            # gets sliding window of key for block i
            key_window =  (key + key)[i%len(key):(i%len(key))+8]
            print(key_window)
            block = DES_round(block, key)
        output += (block.left + block.right)
    
    print( "out: {}".format(output) )
    return output

def unencrypt_DES(data, key, rounds):
    
    output = ""
    
    for b in range(len(data), -1, -12):
        block = des_block( data[b-12:b] )
        for i in range(rounds-1, -1,-1):
            # gets sliding window of key for block i
            key_window =  (key + key)[i%len(key):(i%len(key))+8]
            block = DES_round(block, key)
        output += (block.left + block.right)
        
    print( "out: {}".format(output) )
    
def XOR_example():
    a = "001100"
    b = "010010"
    y = int(a,2) ^ int(b,2)
    print('{0:06b}'.format(y))
    
#XOR_example()
print("Result: {}".format(DES_function('000100','11001100')))

block = des_block('011101000100')
new_block = DES_round(block,'11001100')
print( "{} {}".format(new_block.left,new_block.right ) )


#data = "111111111111111111111111111111111111111111111111111111111111"
data = "111111111111000000000000111111111111000000000000111111111111"


key = "010011001"
data_out = encrypt_DES(data, key, 5)
print("\n")
unencrypt_DES(data_out, key, 5)
