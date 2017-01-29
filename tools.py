#!/usr/bin/env python
from NFA import NFA as nfa

"""
    The validity checking and nfa construction are done simultaneously using the following
    function. It uses the fact that if a regular expression is valid then it is either of
    the form (E+E) OR (E*) OR (E.E) OR 1(epsilon) OR 0(phi) OR an alphabet where E is
    another valid regular expression. Its correctness can be shown by strong induction 
    using the fact that if the below algorithm is correct for smaller sizes of E, then 
    using the getOperatorDict function it can be shown that it is also correct for larger 
    sizes of E, it also returns the correct value for the base case of |E| = 1.
"""

def checkValidity(r, s, e):
    '''Returns the nfa if valid, None otherwise'''
    # To handle the case when expression in empty
    if (e-s+1 < 1):
        return None
    # Single character
    if (e-s+1 == 1):
        c = r[s:e+1]
        
        if (c.isalpha() or c == '0' or c == '1'):
            n = constructNFA(c)
            return n
    
    # o = location of the operator within the expression
    o = getOperatorIndex(s)
    
    # operator not present within the expression containing brackets
    if o is -1:
        return None
    
    if r[o] is not '*':
        n1 = checkValidity(r, s+1, o-1)
        n2 = checkValidity(r, o+1, e-1)
        
        if n1 is not None and n2 is not None:
            #print 'n1.d:', n1.d
            #print 'n2.d:', n2.d
            n = joinNFA(n1, n2, r[o])
            return n
        return None
    else:
        n1 = checkValidity(r, s+1, o-1)
        
        if n1 is not None:
            n = joinNFA(n1, None, "*")
            return n
        
        return None

def getOperatorIndex(s):
    try:
        return dbLocs[s]
    except KeyError:
        return -1

def setOperatorDict(s):
    global dbLocs
    dbLocs = s
    
def getOperatorDict(r):
    '''Identifies the locations of the operators
    
    Returns a dict containing start-bracket-index:operator-index pairs
    Returns None if an error is identified.
    '''
    
    bLocs = [] # stack for pushing bracket locations
    d = {}
    
    for i, c in enumerate(r):
        if c is '(':
            bLocs.append(i)
        
        if c is ')':
            try:
                if bLocs[-1] not in d:
                    return None     # if the operator is missing.
                bLocs.pop()
            except IndexError: # if the stack is empty
                return None
        
        if c in "+.*":
            try:
                if bLocs[-1] in d:  # if there is one operator already
                    return None
                
                d[bLocs[-1]] = i
            except IndexError: # if the stack is empty
                return None
        
    if len(bLocs) != 0: # the stack needs to be empty.
        return None
        
    return d

def constructNFA(c):
    '''Returns the NFA corresponding to the string c
    
    c = a-z | 0(phi) | 1(epsilon)
    '''
    # a-z
    if c.isalpha() and len(c) == 1:
        n = nfa(2, 2)
        n.setStartState('0')
        n.addFinalState('1')
        n.addTransition('0', '1', c)
        #print n.d
        return n
    # 0 (phi)
    elif c == '0':
        n = nfa(1, 1)
        n.setStartState('0')
        #print n.d
        return n
    # 1 (epsilon)
    elif c == '1':
        n = nfa(1, 1)
        n.setStartState('0')
        n.addFinalState('0')
        #print n.d
        return n
    else:
        return None

def joinNFA(n1, n2, op):
    '''creates a new NFA based on the operator.
    op = + or . or *
    '''
    if op == '*':
        n = nfa(n1.q+1, 1)
        n.setStartState(n1.s)
        n.addFinalState(n1.s)
        n.d = n1.d
        # add transitions from the final states to a new state
        for i in n1.f:
            n.addTransition(i, '0', '1')
        
        # to avoid creating epsilon transition cycles
        if n.s in n1.f:
            n.d[n.s]['1'].remove(n.map[0])
        
        # add transition from the new state to the start state
        n.addTransition('0', n.s, '1')
        return n
    elif op == '.':
        n = nfa(n1.q+n2.q)
        n.setStartState(n1.s)
        n.f = n2.f
        n1.d.update(n2.d)
        n.d = n1.d
        for i in n1.f:
            n.addTransition(i, n2.s, '1')
        return n
    elif op == '+':
        n = nfa(n1.q+n2.q+1, 1)
        #print '+'
        #print 'n1.d', n1.d
        #print 'n2.d', n2.d
        n.setStartState('0')
        n.f = n1.f.union(n2.f)
        n1.d.update(n2.d)
        n.d = n1.d
        #print n.d
        n.addTransition('0', n1.s, '1')
        n.addTransition('0', n2.s, '1')
        return n
    else:
        #raise Exception("Invalid operator")
        return None

def runNameOnNFA(n, name):
    def runStringOnNFA(curState, i):
        #print 'cur:', curState
        #print 'i:', i
        
        # if end of string is reached
        if i is len(name):
            if curState in n.f:
                return True
            
            # traverse through all the epsilon transition paths
            if '1' in n.d[curState]:
                for nextState in n.d[curState]['1']:
                    if (runStringOnNFA(nextState, i) is True):
                        return True
            return False
        
        if curState in n.d:
            if '1' in n.d[curState]:
                for nextState in n.d[curState]['1']:
                    if (runStringOnNFA(nextState, i) is True):
                        return True
            if name[i] in n.d[curState]:
                for nextState in n.d[curState][name[i]]:
                    if (runStringOnNFA(nextState, i+1) is True):
                        return True
        
        # the trivial case of an empty string (represented by an epsilon)
        if name[i] is '1':
            return runStringOnNFA(curState, i+1)
        
        return False
     
    return runStringOnNFA(n.s, 0)
        
def resetStateCounter():
    nfa.N = 0
            
