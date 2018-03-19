import numpy as np
import sympy as sp
import copy
debug = False

class des_block(object):
    def __init__(self, bitstring):
        if not isinstance(bitstring, str):
            raise TypeError("param must be string")
        self.left = str(bitstring[0:6])
        self.right = str(bitstring[6:12])
        self.round = 0

    def swap(self):
        self.left, self.right = self.right, self.left
    
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
    return ( S_box_L_result + S_box_R_result )
    
def DES_round(prev_block, key):
    if not isinstance(prev_block, des_block):
        raise TypeError("block must be of type des_block")
    block = copy.deepcopy(prev_block)

    # perform DES function on block.right with key
    f_result = DES_function(block.right, key)
    
    # XOR result of DES function with block.left
    L_XOR_func = bin( int(block.left,2) ^ int(f_result,2) )[2:].zfill(6)
    
    # increase round count for both halves
    block.round += 1
    
    # Swap halves and return block n+1
    block.left = block.right
    block.right = L_XOR_func
    
    return block
     
def sliding_window(key, block_num):
    # gets sliding window of key for a given block 
    return (key + key)[block_num%len(key):(block_num%len(key))+8]

def encrypt_DES(data, key, rounds):
    output = ""
    for b in range(0, len(data), 12):
        block = des_block( data[b:b+12] )
        for i in range(0,rounds):
            key_window =  sliding_window(key, i)
            new_block = DES_round( block, key )
            if debug: print("K:{} B:{} {} Bn:{} {}".format(key_window,block.left,block.right,new_block.left,new_block.right))
            block = new_block
        output += (new_block.left + new_block.right)
    
    print( "CT: {}".format(output) )
    return output

def decrypt_DES(data, key, rounds):
    output = ""
    for b in range(len(data), 0, -12):
        block = des_block( data[b-12:b] )
        block.swap()
        for i in range(rounds-1, -1,-1):
            key_window = sliding_window(key, i)
            new_block = DES_round( block, key )
            if debug: print("K:{} B:{} {} Bn:{} {}".format(key_window,block.left,block.right,new_block.left,new_block.right))
            block = new_block
        output += (new_block.right + new_block.left)
    
    print( "PT: {}".format(output) )
    return output
   
# data = "111111111111111111111111111111111111111111111111111111111111"
# data = "111111111111000000000000111111111111000000000000111111111111"
data = "000000111111000000111111000000111111000000111111000000111111"

key = "010011001"
decrypt_DES( encrypt_DES(data, key, 5) , key, 5)