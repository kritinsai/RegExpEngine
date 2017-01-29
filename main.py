#!/usr/bin/env python

from sys import argv
from tools import *

"""Please represent epsilon as 1 and phi as 0."""

for infile in argv[1:]:
    with open(infile, "r") as f:
        #print infile
        r = f.readline().rstrip()
        #print r
        N = int(f.readline().rstrip())
        d = getOperatorDict(r)
        
        if d is not None:
            setOperatorDict(d)
            resetStateCounter()
            
            n = checkValidity(r, 0, len(r)-1)
            
            #print n
            
            if n is not None:
                for i in range(N):
                    name = f.readline().rstrip()
                    #print name
                    if (runNameOnNFA(n, name) is True):
                        print "Yes"
                    else:
                        print "No"
            else:
                print "Wrong Expression"
        else:
            print "Wrong Expression"
    
    #print
