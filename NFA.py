#!/usr/bin/env python

class NFA():
    '''Constructs an NFA'''
    N = 0 # total number of states created in all NFAs
    
    def __init__(self, numStates, num = 0):
        '''num is the number of new states of the form '0', '1'... which are going to be added'''
        self.q = numStates
        self.s = 0
        self.f = set()
        self.d = {} # transition function
        
        # map between new states of the form '0' ... and 0+N ... to maintain uniqueness
        self.map = {x:x+NFA.N for x in range(num)} 
        NFA.N += num
    
    def getLabel(self, x):
        m = self.map
        if type(x) is int:
            return x
        else:
            x = int(x)
            x = m[x]
            return x

    # in cases where other nfa's attributes are being used 
    # to directly set the attributes of the current nfa
    # do not use the following functions to set the values, 
    # instead modify s, f, d directly. (as it is faster)
    def setStartState(self, s):
        s = self.getLabel(s)
        self.s = s
    
    def addFinalState(self, f):
        f = self.getLabel(f)
        self.f.add(f)
    
    def addTransition(self, f, t, c):
        #print 'addTransition'
        f = self.getLabel(f)
        t = self.getLabel(t)
        
        d = self.d
        
        #print 'f', f
        #print 't', t
        #print 'c', c
        #print 'n.d', d
        
        try:
            df = d[f]
        except KeyError:
            d[f] = {c:[t]}
            return
        
        try:
            dfc = df[c]
        except KeyError:
            df[c] = [t]
            return
        
        dfc.append(t)
    
    # string representation of the NFA
    def __str__(self):
        s = 'n.q: ' + str(self.q) + '\n'
        s += 'n.s: ' + str(self.s) + '\n'
        s += 'n.f: ' + str(self.f) + '\n'
        s += 'n.d: ' + str(self.d) + '\n'
        
        s += 'NFA.N: ' + str(NFA.N) + '\n'
        
        return s
            
        
        
                
            
            
                
            
