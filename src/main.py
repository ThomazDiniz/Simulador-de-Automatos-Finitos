import sys, itertools, os
from collections import deque

ACCEPT      = 'aceita'
STATES      = 'estados'
INITIAL     = 'inicial'
TRANSITIONS = 'transicoes'

operations = ['-u','-i','-d','-s','-c','-m']
OP_UNION = operations[0]
OP_INTERSECTION = operations[1]
OP_DFACONVERSION = operations[2]
OP_STAR = operations[3]
OP_COMPLEMENT = operations[4]
OP_MINIMIZATION = operations[5]


formalDef = {STATES: [], INITIAL: '', ACCEPT: [], TRANSITIONS: {}}
automatas = [] 

def readInputFile():
    directories = [d for d in sys.argv[1:] if d not in operations and os.path.isfile(d)]
    operation = next((op for op in sys.argv[1:] if op in operations),'')
    word = next((w for w in sys.argv[1:] if w not in directories and w not in operations),'')
    automatas = [readAutomataFile(d) for d in directories]

    result = ''
    if operation == OP_UNION:
        print('Operação de União:')
        result = union(automatas[0],automatas[1])
    elif operation == OP_INTERSECTION:
        print('Operação de Intersecção:')
        result = intersection(automatas[0],automatas[1])
    elif operation == OP_DFACONVERSION:
        print('Operação conversão NFA para DFA:')
        result = nfaToDfa(automatas[0])
    elif operation == OP_STAR:
        print('Operação Estrela:')
        result = starOperation(automatas[0])
    elif operation == OP_COMPLEMENT:
        print('Operação Complemento:')
        generateComplement(automatas[0])
    elif operation == OP_MINIMIZATION:
        print('Operação Minimização:')
        print("Not implemented YET")
    else:
        print('Operação de Simulação:')
        simulate(automatas[0])
        
    if operation != '':
        writeOutputFile(result)


# readInputFile() reads a file.txt in the specified format 
# and inserts the data into `formalDef` object.
# required filename passed by argument.
def readAutomataFile(directory):
    inputFile = open(directory, 'r')
    formalDef = {STATES: [], INITIAL: '', ACCEPT: [], TRANSITIONS: {}}
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
    inputFile.close()
    return formalDef
    
# simulate() simulate the automaton specified in the formatDef object
# when it reads the word given in the sys argument and returns a list
# with the states where the automaton stops at the end of the word.
def simulate(formalDef):
    word = sys.argv[2]
    toProcess = deque([])
    toProcess.append(formalDef[INITIAL])

    print('ESTADO', '\t', 'PALAVRA')
    print(formalDef[INITIAL], '\t', word)
    while(len(word) > 0 and len(toProcess) > 0):
        currentState = toProcess.popleft()
        symbol = word[0]
        word = word[1:len(word)]
        if (symbol in formalDef[TRANSITIONS][currentState]):
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
    
    for s in formalDef[STATES]:
        if "_" in s:
            print("Não foi possível converter o automato para nfa pois o automato utiliza '_' em sua nomenclatura de estados")
            return formalDef

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

    newStates.append("_")
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


# union(formalDefA, formalDefB) constructs an automata recognizing the union 
# of the languages of two given automatas.
def union(formalDefA, formalDefB):
    newFormalDef = {
        STATES: formalDefA[STATES] + formalDefB[STATES],
        INITIAL: 'NEW_STATE',
        ACCEPT: formalDefA[ACCEPT] + formalDefB[ACCEPT],
        TRANSITIONS: formalDefA[TRANSITIONS]
    }

    newFormalDef[STATES].append(newFormalDef[INITIAL])

    newFormalDef[TRANSITIONS].update(formalDefB[TRANSITIONS])
    newFormalDef[TRANSITIONS][newFormalDef[INITIAL]] = {
        'e': [formalDefA[INITIAL], formalDefB[INITIAL]]
    }

    return newFormalDef

def intersection(formalDefA,formalDefB):
    newFormalDef = newFormalDef = {STATES: [], INITIAL: '', ACCEPT: [], TRANSITIONS: {}}
    stateCombinations = list(itertools.product(formalDefA[STATES], formalDefB[STATES]))
    states = []
    #States
    for combinations in stateCombinations:
        states.append("_".join(str(state) for state in combinations))
    newFormalDef[STATES] = states
    #initial
    newFormalDef[INITIAL] = formalDefA[INITIAL] + "_" +  formalDefB[INITIAL]
    #ACCEPT:
    acceptCombination = list(itertools.product(formalDefA[ACCEPT], formalDefB[ACCEPT]))
    acceptStates = []
    for combinations in acceptCombination:
        acceptStates.append("_".join(str(state) for state in combinations))
    newFormalDef[ACCEPT] = acceptStates
    #transitions
    alphabetA = set(getAlphabet(formalDefA))
    alphabetB = set(getAlphabet(formalDefB))
    alphabet = alphabetA | alphabetB
    for symbol in alphabet:
        for state in newFormalDef[STATES]:
            stateA,stateB = state.split("_")
            resultA = nfaTraverse(formalDefA,stateA,symbol)
            resultB = nfaTraverse(formalDefB,stateB,symbol)
            for a in resultA:
                for b in resultB:
                    myState = stateA + "_" + stateB
                    resultState = a + "_" + b
                    automataAddTransiton(newFormalDef,myState,symbol,resultState)
    
    return newFormalDef

def starOperation(formalDef):
    newFormalDef = formalDef

    # A new state is added
    newFormalDef[STATES].append('NEW_STATE')

    oldInitial = newFormalDef[INITIAL]
    oldAccepts = newFormalDef[ACCEPT]
    
    # New state is setted to initial and accept states
    newFormalDef[INITIAL] = 'NEW_STATE'
    newFormalDef[ACCEPT].append('NEW_STATE')
    
    # Empty transiton from new initial to old initial
    newFormalDef[TRANSITIONS]['NEW_STATE'] = { 'e' : [oldInitial] } 

    # Empty transitions created from old accept states to old initial state
    for oldAccept in oldAccepts:
        newFormalDef[TRANSITIONS][oldAccept]['e'] = [oldInitial]

    return newFormalDef

def minimize(formalDef):  
    #remove all unreachable states
    reachableStates = findReachableStates(formalDef)
    formalDef[STATES] = [s for s in formalDef[STATES] if s in reachableStates]
    formalDef[ACCEPT] = [s for s in formalDef[ACCEPT] if s in reachableStates]
    
    return formalDef
 
#transform to dfa   
#dfa = nfaToDfa(formalDef)


def findReachableStates(formalDef):
    alphabet = getAlphabet(formalDef)
    initial = formalDef[INITIAL]
    reachableStates = [initial]
    previousReachableStates = []
    while True:
        for symbol in alphabet:
            reachableStates = set(reachableStates).union(set(traverseMultipleStates(formalDef,reachableStates,symbol)))
        if reachableStates == previousReachableStates:
            break
        previousReachableStates = reachableStates
    return reachableStates


fa = {'estados': ['A', 'B'], 'inicial': 'A', 'aceita': ['B'], 'transicoes': {'A': {'0': ['B'], '1': ['A']}, 'B': {'0': ['A'], '1': ['B']}}}
fb = {'estados': ['A', 'B', 'C', 'D', 'Z'], 'inicial': 'A', 'aceita': ['D','A','Z'], 'transicoes': {'Z':{'0':['Z','A']},'A': {'0': ['B'], '1': ['C']}, 'B': {'1': ['C'], '0': ['D']}, 'C': {'0': ['B'], '1': ['D']}, 'D': {'0': ['D'], '1': ['D']}}}

# intersection(fa,fb)
print(fb)
print(minimize(fb))
#readInputFile()
# print(formalDef)
# print(nfaToDfa(formalDef))
