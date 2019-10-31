import sys
from collections import deque

ACCEPT      = 'aceita'
STATES      = 'estados'
INITIAL     = 'inicial'
TRANSITIONS = 'transicoes'

formalDef = {STATES: [], INITIAL: '', ACCEPT: [], TRANSITIONS: {}}

# readInputFile() reads a file.txt in the specified format 
# and inserts the data into `formalDef` object.
# required filename passed by argument.
def readInputFile():
    inputFile = open(sys.argv[1], 'r')
    while True:
        line = inputFile.readline()
        if not line: break

        args = line.strip().split(' ', 1)
        if(args[0] in formalDef):
            formalDef[args[0]] = args[1].split(', ')
        else:
            currentState, nextState, symbol = line.strip().split(' ')
            if (formalDef[TRANSITIONS].has_key(currentState)):
                if (formalDef[TRANSITIONS].has_key(symbol)):
                    formalDef[TRANSITIONS][currentState][symbol].append(nextState)
                else:
                    formalDef[TRANSITIONS][currentState][symbol] = [nextState]
            else:
                formalDef[TRANSITIONS][currentState] = {symbol: [nextState]}
    formalDef[INITIAL] = formalDef[INITIAL][0]

# simulate() simulate the automaton specified in the formatDef object
# when it reads the word given in the sys argument and returns a list
# with the states where the automaton stops at the end of the word.
def simulate():
    word = sys.argv[2]
    toProcess = deque([])
    toProcess.append(formalDef[INITIAL])

    print 'ESTADO', '\t', 'PALAVRA'
    print formalDef[INITIAL], '\t', word
    while(len(word) > 0):
        currentState = toProcess.popleft()
        symbol = word[0]
        word = word[1:len(word)]
        for nextState in formalDef[TRANSITIONS][currentState][symbol]:
            toProcess.append(nextState)
            print nextState, '\t', word if len(word) > 0 else 'e'
    showVeredict(toProcess)
    
# showVeredict() receives a list with the states the automaton stops
# at the end of a word and verifies if one of them is an accept state
# and shows a message according to it.
def showVeredict(states):
    accept = False
    for state in states:
        if (state in formalDef[ACCEPT]): accept = True
    print '\nA palavra %sfoi aceita' % ('nao ' if not accept else '')

# generateComplement(formalDef) generate the complement automaton for the
# automaton received in the param. It returns a formal definition for the
# complement automaton.
def generateComplement(formalDef):
    complementDef = {}
    complementDef[INITIAL] = formalDef[INITIAL]
    complementDef[TRANSITIONS] = formalDef[TRANSITIONS].copy()
    complementDef[STATES] = formalDef[STATES][:]
    complementDef[ACCEPT] = list(set(formalDef[STATES]) - set(formalDef[ACCEPT]))
    return complementDef
