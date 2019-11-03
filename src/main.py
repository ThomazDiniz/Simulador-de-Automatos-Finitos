import sys
import itertools
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
            if currentState in formalDef[TRANSITIONS]:
                if (symbol in formalDef[TRANSITIONS][currentState]):
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

    print('ESTADO', '\t', 'PALAVRA')
    print(formalDef[INITIAL], '\t', word)
    while(len(word) > 0):
        currentState = toProcess.popleft()
        symbol = word[0]
        word = word[1:len(word)]
        for nextState in formalDef[TRANSITIONS][currentState][symbol]:
            toProcess.append(nextState)
            print(nextState, '\t', word if len(word) > 0 else 'e')
    showVeredict(toProcess)
    
# showVeredict() receives a list with the states the automaton stops
# at the end of a word and verifies if one of them is an accept state
# and shows a message according to it.
def showVeredict(states):
    accept = False
    for state in states:
        if (state in formalDef[ACCEPT]): accept = True
    print('\nA palavra %sfoi aceita' % ('nao ' if not accept else ''))

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



# writeOutputFile(formalDef) writes an automaton to the default output
def writeOutputFile(formalDef):
    automataAsStr = STATES   +  ' '  + ', '.join(str(state) for state in formalDef[STATES]) + '\n'
    automataAsStr += INITIAL +  ' '  + formalDef[INITIAL] + '\n'
    automataAsStr += ACCEPT  +  ' '  + ', '.join(str(state) for state in formalDef[ACCEPT]) + '\n'
    transitions = formalDef[TRANSITIONS]
    for state in transitions:
        for symbol in transitions[state]:
            for nextState in transitions[state][symbol]:
                automataAsStr += state + ' ' + nextState + ' ' + symbol
                automataAsStr += '\n'
    print(automataAsStr)

#traverse(formalDef,state,symbol) traverses through the automata 
#and returns all the states it should be after the input is set
def traverse(formalDef,state,symbol):
    if state in formalDef[TRANSITIONS]:
        if symbol in formalDef[TRANSITIONS][state]:
            return formalDef[TRANSITIONS][state][symbol]
    return []
#traverse(formalDef,state,symbol) traverses through the automata 
#and returns all the states it should be after all the inputs are set
#the difference from this to traverse is that it receives multiple states
def traverseMultipleStates(formalDef,states,symbol):
    finalStates = []
    for state in states:
        if state in formalDef[TRANSITIONS]:
            if symbol in formalDef[TRANSITIONS][state]:
                finalStates = finalStates + formalDef[TRANSITIONS][state][symbol]
    return finalStates


#traverseIndefinitely(formalDef,state,symbol) traverse indefinitely 
#using a symbol. It only stops when the set of states
#doesn't change after a traverse
def traverseIndefinitely(formalDef,states, symbol):
    previousStates = []
    while True:
        states = set(states).union(set(traverseMultipleStates(formalDef,states,symbol)))
        if states == previousStates:
            break
        previousStates = states
    return states

#nfaTraverse(formalDef,states, symbol) traverses as it would in a nfa
def nfaTraverse(formalDef,states, symbol):
    states = traverseIndefinitely(formalDef,states,'e')
    states = traverseMultipleStates(formalDef,states,symbol)
    states = traverseIndefinitely(formalDef,states,'e')
    return states

#findStateFromStateCombinaton(stateCombinations,combination) is an auxiliar 
#method to build a state string from a combination of states
def findStateFromStateCombinaton(stateCombinations,combination):
    foundCombination = ""
    for comb in stateCombinations:
        if combination == set(comb):
            foundCombination = "_".join(str(state) for state in comb)
            break
    return foundCombination

#getAlphabet(formalDef) get all the symbols of an automata
def getAlphabet(formalDef):
    alphabet = set()
    for state in formalDef[TRANSITIONS]:
        for symbol in formalDef[TRANSITIONS][state]:
            alphabet.add(symbol)
    alphabet.discard('e')
    return alphabet

#nfaToDfa(formalDef) build a dfa from a nfa
def nfaToDfa(formalDef):
    newFormalDef = {STATES: [], INITIAL: '', ACCEPT: [], TRANSITIONS: {}}
    
    #CREATE STATE COMBINATIONS (from each state)
    states = formalDef[STATES]
    stateCombinations = []
    newStates = []
    for i in range(1,len(states)+1):
        combinations = set(itertools.combinations(states,i))
        for comb in combinations:
            stateCombinations.append(comb)

    for states in stateCombinations:
        newStates.append("_".join(str(state) for state in states))
    newFormalDef[STATES] = newStates

    #SET ACCEPTING STATES (for every state accept the ones that has at least one accepting state)
    accepting_states = formalDef[ACCEPT]
    newAccepting_states = []

    for states in stateCombinations:
        for accept_state in accepting_states:
            if accept_state in states:
                newAccepting_states.append("_".join(str(state) for state in states))

    newAccepting_states = set(newAccepting_states)
    newFormalDef[ACCEPT] = newAccepting_states

    #SET INITIAL STATE (from the initial state traverse all 'e' symbols until you can't you get the most states. The initial state is a combination of every single starting state)
    initial = formalDef[INITIAL]
    newInitial = traverseIndefinitely(formalDef,initial,'e')
    newFormalDef[INITIAL] = findStateFromStateCombinaton(stateCombinations,newInitial)
    
    
    #SET TRANSITIONS
    alphabet = getAlphabet(formalDef)
    transitions = formalDef[TRANSITIONS]
    for symbol in alphabet:
        print(symbol)
        for states in stateCombinations:
            newState = '_'.join(str(state) for state in states)
            newResultStates = nfaTraverse(formalDef,states,symbol)
            newResultState = findStateFromStateCombinaton(stateCombinations,newResultStates)
            automataAddTransiton(newFormalDef,newState,symbol,newResultState)    
    return newFormalDef

#automataAddTransiton(formalDef,state,symbol,resultState) adds a 
#transition to an automata even if it doesn't have that key
def automataAddTransiton(formalDef,state,symbol,resultState):
    try:
        if symbol in formalDef[TRANSITIONS][state]:
            formalDef[TRANSITIONS][state][symbol].append(resultState)
        else:
            formalDef[TRANSITIONS][state][symbol] = resultState    
    except KeyError:
        formalDef[TRANSITIONS][state] = {symbol: [resultState]}
    


readInputFile()
print(nfaToDfa(formalDef))