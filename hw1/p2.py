#!/usr/bin/env python3
#
# Please look for "TODO" in the comments, which indicate where you
# need to write your code.
#
# Part 2: Integer Negation and Subtraction Using NAND Gates (1 point)
#
# * Objective:
#   Implement a function that performs integer negation using only NAND
#   gates and use it to implement subtraction.
# * Details:
#   The description of the problem and the solution template can be
#   found in `hw1/p2.py`.
#
# From lecture `01w`, we learned that NAND is a universal gate, that
# any binary operations can be built by using only NAND gates.
# Following the lecture notes, we define the "NAND gate" as

def NAND(a, b):
    return 1 - (a & b)  # NOT (a AND b), & is an operator that is 1 if both a and b are 1. Otherwise, 0.

# Following the notes again, we define also other basic operations:

def NOT(a):
    return NAND(a, a) # NAND(0,0) = 1 - 0 = 1. NAND(1,1) = 1 - 1 = 0.

def AND(a, b):
    return NOT(NAND(a, b))

    # BOOLEAN TABLE
    #  a b AND(a,b)
    #  0 0    1
    #  0 1    0
    #  1 0    0
    #  1 1    1

def OR(a, b):
    return NAND(NOT(a), NOT(b))

def XOR(a, b):
    c = NAND(a, b)
    return NAND(NAND(a, c), NAND(b, c))

# We also implemented the half, full, and multi-bit adders:

def half_adder(A, B):
    S = XOR(A, B)  # Sum using XOR
    C = AND(A, B)  # Carry using AND
    return S, C

def full_adder(A, B, Cin): # Adds with history of carrying
    s, c = half_adder(A,   B) # Adds single bit A and B to yield sum in units place, s, and carry value c
    S, C = half_adder(Cin, s) # Adds the units place from adding A and B to the sum carried over from previous
    # addition operation.
    Cout = OR(c, C) #

    return S, Cout

def multibit_adder(A, B, carrybit=False):
    assert(len(A) == len(B))

    n = len(A)
    c = 0 # Initial carry
    S = []
    for i in range(n):
        s, c = full_adder(A[i], B[i], c)
        S.append(s)
    if carrybit:
        S.append(c)  # add the extra carry bit
    return S

# Now, getting into the assignment, we would like to first implement a
# negative function.
#
# Please keep the following function prototype, otherwise the
# auto-tester would fail, and you will not obtain point for this
# assigment.

def multibit_negative(A):
    """Multi-bit integer negative operator

    This function take the binary number A and return negative A using
    two's complement.
    In other words, if the input
        A = 3 = 0b011,
    then the output is
        -A = -3 = 0b101.
    # Specifically, given binary: b0 b1 b2 ... bn,
    # flip each bi (1 -> 0 or 0 -> 1) and add 1 to the result.

    Args:
        A: input number in binary represented as a python list, with
           the least significant digit be the first.
           That is, the binary 0b011 should be given by [1,1,0].

    Returns:
        Negative A using two's complement represented as a python
        list, with the least significant digit be the first.

    """
    # TODO: implement the function here

    B_temp = [] # Temporary array
    for i in range(len(A)):
        B_temp.append(0) # Don't have np in here, so this generates B_temp without numpy
    B_temp[0] = 1 # Because we have least significant bit junk, the left-most thingy is gonna be 1. It's reversed. 
    # I just found this out after an hour of Googling. I'm so cooked.
    
    more_temp_arrays = [] # Initially I wanted to replace all elements of A with its NOT(...) stuff, but: 
    # 1. It's probably not a good idea to redefine A like that...
    # 2. It didn't work (multibit_negator failed some tests).
    # After failure of tests, it got me thinking that (assuming my method is right, which I'm fairly sure but ehhh)
    # it was probably a good idea to isolate negated A from A instead of redefining A as negative of A with this
    # function. Hence this other approach where I generate an empty array to fill up.
    for i in range(len(A)):
        more_temp_arrays.append(NOT(A[i])) # This essentially flips every bit, 1 -> 0 and 0 -> 1
    return multibit_adder(more_temp_arrays,B_temp)

# TEST CASE

# A_test = [0,1,1,0,1]

# multibit_negative(A_test)

# We are now ready to implement subtraction using multibit_adder() and
# multibit_negative().

def multibit_subtractor(A, B):
    """Multi-bit integer subtraction operator

    This function take the binary numbers A and B, and return A - B.
    Be careful on how the carrying bit is handled in multibit_adder().
    Make sure that when A == B, the result A - B should be zero.

    Args:
        A, B: input number in binary represented as a python list,
           with the least significant digit be the first.
           That is, the binary 0b011 should be given by [1,1,0].

    Returns:
        A - B represented as a python list, with the least significant
        digit be the first.

    """
    # TODO: implement the function here

    return multibit_adder(A,multibit_negative(B))
