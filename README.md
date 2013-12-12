***ABOUT AHO-CORASICK ALGORITHM***

Aho-Corasick algorithm provides efficient string matching algorithm
consisting of two parts. First we construct a finite state pattern
matching machine (DFA) using a finite number of keywords. After that,
we use the pattern matching machine to find all occurrences of any
keyword in a given text.

LABELS:
- keywords = {y1, y2,..., yk} => a finite set of keywords - strings
- x => a string called text string

PROBLEM:
Find all substrings of x which are elements of keywords.

INPUT:
- x, keywords

OUTPUT:
- locatins in x where certain keywords are found

STATES:
- states are defined by positive integers 
- start state = 0

3 functions are needed for pattern matching machine to work:
- goto function - based on keywords, goto function maps a pair
    consisting of a state and an input symbol into a transition
    state: g(state, a) = transition_state
- failure function - maps a state into a state. It's consulted
    whenever the goto function doesn't have defined transition for
    a certain pair (state, symbol). Only start state (0) doesn't
    have defined failure transition - start state has transition 
    back into 0 for all undefined transitions (0, a)
- output function - defines states in which certain keywords are 
    found

REFERENCES:
ftp://163.13.200.222/assistant/bearhero/prog/%A8%E4%A5%A6/ac_bm.pdf

----------------------------------------------------------------------
----------------------------------------------------------------------


This repository provides implementation of Aho-Corasick algorithm in
three different programming languages: Python, C#, Java.
Programs are written for Bio-Linux platform.


***INSTALLATION GUIDE***
- PYTHON:
   + open Terminal
   + go to directory where AhoCorasickAlgorithm.py file is located
   + run program using following line:
      python AhoCorasickAlgorithm.py file1 file2


- C#:
   + unpack AhoCorasick_C#.zip
   + open Terminal
   + get compiler for C# using following line:
      sudo apt-get install mono-complete
   + go to directory 'AhoCorasick_C#'
   + compile program using following line:
      xbuild /p:OutputPath='desired_output_directory' AhoCorasick.sln
   + run program using following line:
      mono AhoCorasick.exe file1 file2
   


- JAVA:
   + unpack AhoCorasick_Java.zip
   + open Terminal
   + go to directory 'src'
   + compile program using following line: 
      javac Start.java
   + run program using following line:
      java Start file1 file2


- file1 is a file consisting of a comma separated keywords (strings)
- file2 is a file consisting of a text (string) 



***OUTPUTS***
- Terminal:
   + time spent for loading files
   + time spent for construction of DFA
   + time spent for finding all keywords
   + total memory used
- file 'output':
   + all keywords found in given text at specific index 
     (indexes start with 0)



***GIVEN EXAMPLE FILES***

In repository there are two files given as an example of file1 
(keywords) and file2 (text). Running programs with those files should 
return the following output:

index:       1  =>  keyword: she       
index:       2  =>  keyword: he        
index:       2  =>  keyword: hers     



***CONTACTS***

This is done as a project for course Bioinformatics on Faculty of 
electrical engineering and computing in the year 2013 by:
- Janja Paliska 
   + Email: janjapaliska@yahoo.com
   + GitHub: janja0308
- Antonio Soldo 
   + Email: antonio.soldo11@gmail.com
   + GitHub: soky32
- Antonio Zemunik 
   + Email: zemunikantonio@gmail.com
   + GitHub: zema123
