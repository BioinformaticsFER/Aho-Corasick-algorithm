import sys
import time
import os

#------------------memory usage------------------------#
#taken from: http://code.activestate.com/recipes/286222/
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
            if a not in alphabet:
                alphabet.append(a);
        g, output, newstate = enter(ki, g, output, newstate);
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


m0 = memory();
try:
    keywordsfile = sys.argv[1];
    textfile = sys.argv[2];
except IndexError:
    print("Keywords and/or text file not provided!");
    exit(-1);

start = time.time();    
file = open(keywordsfile, 'r');    
keywords = file.read()[0:-1].split(',');
file.close();

file = open(textfile, 'r');
text = file.read();
text = text[0 : (len(text) - 1)];
text = text.replace('\n', '');
file.close();
print('Loading files done in {} ms.'.format((time.time() - start)*1000)); 

# Constructing a DFA for pattern matching from the set of keywords.
start = time.time();
g, output, alphabet = goto(keywords);
output, f = failure(g, output, alphabet);
print('Construction of DFA done in {} ms.'.format((time.time() - start)*1000));

# Finding all occurrences of keywords in text using DFA.
file = open('output', 'w');
start = time.time();
state = 0;
for i in range(len(text)):
    if (state, text[i]) in g:       # transitions already defined
        state = g[state, text[i]];
    elif state == 0:                # undefined transitions from 0 return to state 0
        g[0, text[i]] = 0;
        alphabet.append(text[i]);
        state = 0;
    else:
        state = f[state];           # other undefined transitions find with failure function    
        if text[i] not in alphabet:
            g[0, text[i]] = 0;
        while ((state, text[i]) not in g):
            state = f[state];
        state = g[state, text[i]];
        
    if state in output:
        for oi in output[state]:
            file.write('index: {0:7d}  =>  keyword: {1:10}\n'.format((int(i - len(oi) + 1)), oi));

print('Finding all keywords in text done in {} ms.'.format((time.time() - start)*1000));
file.close();
m1 = memory(m0);
print('Total memory used: {} KiB'.format(m1/1024));
