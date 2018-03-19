import math

# base = 23
# exponent = 1246
# modulus = 53

# n = exponent
# y = 1
# u = base % modulus
# p = modulus

def modular_exponentiation(base, exponent, modulus):
    return rec_mod_expon(exponent, 1, (base % modulus), modulus)

def rec_mod_expon(n,y,u,p):
    #print( "n:{} y:{} u:{}".format(n,y,u) )
    if n == 0:
        return y
    if n % 2 != 0:
        y = ( y * u ) % p
    u = ( u * u ) % p
    n = math.floor( n / 2 )
    return rec_mod_expon(n,y,u,p)

print( modular_exponentiation( 23, 1246, 53 ) )