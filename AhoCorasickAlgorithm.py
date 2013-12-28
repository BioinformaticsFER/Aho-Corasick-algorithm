# author: Janja Paliska
# This is code for Aho Corasick Algoritam - an efficient algorithm
# for finding substrings in text using deterministic finite automaton


import sys
import time
import os

#------------------memory usage------------------------#
# Lines 17-56 are taken from:
# http://code.activestate.com/recipes/286222/
# and are used to measure total memory spent while running
# this program
_proc_status = '/proc/%d/status' % os.getpid()
_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    '''Return memory usage in bytes.
    '''
    return _VmB('VmSize:') - since


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB('VmStk:') - since
#------------------------------------------------------#
#------------------------------------------------------#




# Function goto maps a pair consisting of a state and an input symbol
# into a transition state: g(state, a) = transition_state
# Transitions are created based on all keywords.
def goto(keywords):
    alphabet = []
    newstate = 0;
    g = {}
    output = {}
    for ki in keywords:
        for a in ki:
            if a not in alphabet: # Alphabet list contains all symbols 
                alphabet.append(a);
        g, output, newstate = enter(ki, g, output, newstate);
    # Make transition from 0 back to 0 for all undefined transitions g(0,a)
    for a in alphabet: 
        if (0, a) not in g:
            g[0, a] = 0;
    return g, output, alphabet


# Function enter is a side function used by goto function.
def enter(ki, g, output, newstate):
    state = 0;
    j = 0;
    # First find the longest ki's prefix already defined. 
    while ((state, ki[j]) in g):
        state = g[(state, ki[j])];
        j = j + 1;
    # Define transitions for the rest of ki.    
    for p in range(j, len(ki)):
        newstate = newstate + 1;
        g[(state, ki[p])] = newstate;
        state = newstate;
    # Output defines states in which certain keywords are found.
    if state not in output:
        output[state] = [];
    output[state].append(ki);
    return g, output, newstate;


# Function failure maps a state into a state. Failure function is
# consulted whenever goto function doesn't have defined transition
# for a certain pair (state, symbol). Only start state (0) doesn't
# have defined failure transition - start state has transition back
# into 0 for all undefined transitions (0, a).
def failure(g, output, alphabet):
    queue = [];
    f = {};
    # Failure starts with states s that have defined transition 0->s,
    # those states have f(s)=0. All failure functions for other
    # states are genereted based on states that have smaller depth.
    # (Depth(s) - number of transitions from 0 to s)
    for a in alphabet:
        if g[0, a] != 0:            
            queue.append(g[0, a]);
            f[g[0, a]] = 0;
    while queue != []:
        r = queue.pop(0);
        for a in alphabet:
            if (r, a) in g:
                s = g[r, a];
                queue.append(s);
                state = f[r];
                while (state, a) not in g:
                    state = f[state];
                f[s] = g[state, a];
                if s not in output:
                    output[s] = [];
                if s in f:
                    if f[s] in output:
                        for oi in output[f[s]]:
                            output[s].append(oi);

    return output, f;


# Function main reads keywords file, construct DFA and then, reading text
# line by line, locates keywords in text. It produces both Terminal and 
# file outputs: Terminal - performance (time spent constructing DFA, time
# spent locating all keywords, memory usage), file - keywords that were
# located in text and their indexes
def main(keywordsfile, textfile):
    m0 = memory(); # Start measuring memory 
    # Check if either file is empty and if so, exit
    if (os.stat(keywordsfile)[6] == 0) or (os.stat(textfile)[6] == 0):
        print("Files cannot be empty!");
        exit(-1);
    file = open(keywordsfile, 'r');    
    keywords_tmp = file.readline()[0:-1].split(',');
    file.close();
    keywords_tmp = list(filter(bool, keywords_tmp)); # Remove empty strings
    # Remove duplicates from list
    keywords = [];
    for k in keywords_tmp:
        if k not in keywords:
            keywords.append(k);

    # Constructing a DFA for pattern matching from the set of keywords.
    start = time.time();
    g, output, alphabet = goto(keywords); 
    output, f = failure(g, output, alphabet);
    print('Construction of DFA done in {} ms.'.format((time.time() - start)*1000));
    
    # Finding all occurrences of keywords in text using DFA.
    file = open('output', 'w');
    start = time.time();
    state = 0;
    position = 0;
    try:
        with open(textfile, 'r') as t:
            for text in t:
                for i in range(len(text)-1):
                    counter = 0;
                    if (state, text[i]) in g:
                        state = g[state, text[i]];
                        counter = 1;
                        
                    if counter == 0:
                        if text[i] not in alphabet:
                            alphabet.append(text[i]);
                            g[0, text[i]] = 0;
                        if state != 0:      # All transitions g(0, a) that are yet not defined
                            foundState = 0; # lead back to start state (0).
                            while(foundState == 0):
                                state = f[state];
                                if (state, text[i]) in g:
                                    foundState = 1;
                                    state = g[state, text[i]];
                                    break;
                    if state in output:
                            for oi in output[state]:
                                file.write('index: {0:7d}  =>  keyword: {1:10}\n'.format((int(position + i - len(oi) + 1)), oi));
                position += len(text) - 1;
    except IOError:
        print('Error while opening files');
        exit(-1);

    print('Finding all keywords in text done in {} ms.'.format((time.time() - start)*1000));
    file.close();
    m1 = memory(m0); # Stop measuring memory
    print('Total memory used: {} KiB'.format(m1/1024));

if __name__ == "__main__":
    try:
        keywordsfile = sys.argv[1];
        textfile = sys.argv[2];
    except IndexError:
        print("Keywords and/or text file not provided!");
        exit(-1);
    main(keywordsfile, textfile);
