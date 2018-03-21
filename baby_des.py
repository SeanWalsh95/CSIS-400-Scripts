#!/usr/bin/env python
__author__ = "Sean Walsh"
__version__ = "0.0.1"

import copy
from optparse import OptionParser

class des_block(object):
    def __init__(self, bitstring):
        if not isinstance(bitstring, str):
            raise TypeError("param must be string")
        self.left = str(bitstring[0:6])
        self.right = str(bitstring[6:12])
        self.round = 0
    
    def __str__(self):
        return  (self.left + self.right)
    def __repr__(self):
        return  (self.left + self.right)
    
    def swap(self):
        self.left, self.right = self.right, self.left


def XOR(s1,s2,zfill):
    # XOR's two bit-strings together, fills result with 
    # leading zeros to a given length
    return bin( int(s1,2) ^ int(s2,2) )[2:].zfill(zfill)
    
def sliding_window(key, block_num):
    # gets sliding window of key for a given block 
    return (key + key)[block_num%len(key):(block_num%len(key))+8]
    
def parse_blocks(data):
    blocks = []
    for b in range(0, len(data), 12):
        blocks.append( des_block( data[b:b+12] ) )
    return blocks


def DES_function(R,key):
    S_box_L = ["101","010","001","110","011","100","111","000","001","100","110","010","000","111","101","011"]
    S_box_R = ["100","000","110","101","111","001","011","010","101","011","000","111","110","010","001","100"]
    
    # Expand R from 6 to 8 bits  1,2,4,3,4,3,5,6
    R_exp = R[0:2] + R[3] + R[2:4] + R[2] + R[4:6]
    
    # ( Expanded R ) XOR ( key ) = 8 bit value for S-boxes
    S = XOR(R_exp, key, 8)
    
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
    L_XOR_func = XOR(block.left, f_result, 6)
    
    # increase round count for both halves
    block.round += 1
    
    # Swap halves and return block n+1
    block.left = block.right
    block.right = L_XOR_func
    
    return block
    
def encrypt_DES(data, key, rounds):
    results = []
    blocks = parse_blocks(data)
    for block in blocks:
        for i in range(0,rounds):
            key_window =  sliding_window(key, i)
            new_block = DES_round( block, key )
            if verbose: print("K:{} B:{} {} [{}] Bn:{} {} [{}]".format(key_window,block.left,block.right,block.round,new_block.left,new_block.right,new_block.round))
            block = new_block
        results.append(block)
    print( "CT: {}".format(results) )
    return results
    
def decrypt_DES(data, key, rounds):
    results = []
    blocks = parse_blocks(data)
    for block in blocks:
        block.swap()
        for i in range(rounds-1, -1,-1):
            key_window = sliding_window(key, i)
            new_block = DES_round( block, key )
            if verbose: print("K:{} B:{} {} [{}] Bn:{} {} [{}]".format(key_window,block.left,block.right,block.round,new_block.left,new_block.right,new_block.round))
            block = new_block
        block.swap()
        results.append(block)
    print( "PT: {}".format( results ) )
    return results
    
def encrypt_DES_CBC(data, init_v, key, rounds):
    results = []
    vector = init_v
    blocks = parse_blocks(data)
    for block in blocks:
        pt_block = copy.deepcopy(block)
        pt_XOR_iv = des_block( XOR(vector, str(block), 12) )
        for i in range(0,rounds):
            key_window =  sliding_window(key, i)
            new_block = DES_round( pt_XOR_iv, key )
            if verbose: print("K:{} B:{} {} [{}] Bn:{} {} [{}]".format(key_window,block.left,block.right,block.round,new_block.left,new_block.right,new_block.round))
            block = new_block
        print("PT:{} V:{} XOR:{} CT:{}".format(pt_block, vector, pt_XOR_iv,block))
        vector = str(block)
        results.append(block)
    
    print( "CT: {}".format(results) )
    return results
    
def decrypt_DES_CBC(data, init_v, key, rounds):
    results = []
    vector = init_v
    blocks = parse_blocks(data)
    for block in blocks:
        next_vector = str(block)
        block.swap()
        for i in range(rounds-1, -1,-1):
            key_window = sliding_window(key, i)
            new_block = DES_round( block, key )
            if verbose: print("K:{} B:{} {} [{}] Bn:{} {} [{}]".format(key_window,block.left,block.right,block.round,new_block.left,new_block.right,new_block.round))
            block = new_block
        block.swap()
        results.append(block)
        block_XOR_vector = des_block( XOR(vector, str(block), 12) )
        print("V:{} XOR:{} CT:{}".format(vector, block_XOR_vector,block))
        vector = next_vector
    print( "PT: {}".format( results ) )
    return results
    
    
    
def enc_file_DES(filename, key, rounds):
    with open(filename, 'r') as f:
        data  = f.read().replace('\n','')
        out = encrypt_DES(data, key, rounds)
        with open(filename.replace('.txt','_enc.txt'),'w') as f:
            for block in out: f.write( str(block) + "\n" )

def dec_file_DES(filename, key, rounds):
    with open(filename, 'r') as f:
        data  = f.read().replace('\n','')
        out = decrypt_DES(data, key, rounds)
        with open(filename.replace('.txt','_dec.txt'),'w') as f:
            for block in out: f.write( str(block) + "\n" )

def main():
    global verbose
    verbose = False
    rounds = 5
    key = "010011001"
    init_vector = "111111111111"

    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",action="store_true", dest="verbose",
                        help="prints extra information about encryption/decryption")
    
    parser.add_option("-e", "--ENC",action="store_true", dest="encrypt",
                        help="encrypt data from [filename]")
    parser.add_option("-d", "--DEC",action="store_true", dest="decrypt",
                        help="decrypt data from [filename]")
    
    parser.add_option("-r", action="store", type="int", dest="rounds",
                        help="how many rounds to perform DES [Default=4] ")
    parser.add_option("-k", action="store", type="string", dest="key",
                        help="flag to pass in key from cli [Default='010011001']")
    
    parser.add_option("--ECB",action="store_true", dest="ECB", default=True,
                        help="DES ECB mode [Default]")
    parser.add_option("--CBC",action="store_true", dest="CBC",
                        help="DES CBC mode")
    
    (options, args) = parser.parse_args()
    
    print(options)
    
    if options.verbose != None:
        verbose = options.verbose
    if options.rounds != None:
        rounds = options.rounds
    if options.key != None:
        key = options.key
    
    if options.encrypt:
        enc_file_DES(args[0], key, rounds)
    if options.decrypt:
        dec_file_DES(args[0], key, rounds)
    
    
    if True:
        verbose = False
        # data = "111111111111111111111111111111111111111111111111111111111111"
        # data = "111111111111000000000000111111111111000000000000111111111111"
        data = "000000111111000000111111000000111111000000111111000000111111"
        key = "010011001"
        
        print("\n\nECB:")
    
        enc = encrypt_DES(data, key, rounds)
        decrypt_DES( ''.join(map(str, enc)), key, rounds)
        
        print("\n\nCBC:")
        
        enc = encrypt_DES_CBC(data, init_vector, key, rounds)
        decrypt_DES_CBC( ''.join(map(str, enc)), init_vector, key, rounds)


main()


