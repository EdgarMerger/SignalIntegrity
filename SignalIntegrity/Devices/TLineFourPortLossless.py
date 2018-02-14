'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
import math
from TLineFourPort import TLineFourPort
# transmission line
#
#           +-----------------------+
#          / \                       \
#         |   |                       |
#   1 ----+-  |     Z    Td           +----- 2
#         |   |                       |
#          \ /                       /
#        +--+-----------------------+--+
#        |                             |
#   3 ---+                             +---- 4
#
#
# is either two or four ports
# ports 1 and 2 are the input and output
# ports 3 and 4 are the outer conductor
# when two ports, ports 3 and 4 are assumed grounded

def TLineFourPortLossless(Zc,Td,f,Z0):
    return TLineFourPort(Zc,1j*2.*math.pi*f*Td,Z0)