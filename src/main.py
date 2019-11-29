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

# _getNotFinalStates get state that are not final states
def _getNotFinalStates(formalDef):
    notFinalStates = []
    for state in formalDef[STATES]:
        if not state in formalDef[ACCEPT]:
            notFinalStates.append(state)
    return notFinalStates


# _minimalStates calculates the minimal states for the automaton given
def _minimalStates(formalDef):
    formalDef = removeUnreachableStates(formalDef)
    notFinalStates = _getNotFinalStates(formalDef)
    finalStates = formalDef[ACCEPT]
    sets = [notFinalStates, finalStates]
    currentSets = []
    transitios = formalDef[TRANSITIONS]
    alphabet = getAlphabet(formalDef)
    while currentSets == []:
        currentSets = sets
        sets = []
        for subSet in currentSets:
            isDivided = False
            for symbol in alphabet:
                into = []
                outo = []
                for state in subSet:
                    try:
                        if transitios[state][symbol][0] in finalStates: into.append(state)
                        else: outo.append(state)
                    except KeyError:
                        outo.append(state)
                if into != [] and outo != []:
                    sets.append(into)
                    sets.append(outo)
                    isDivided = True
                    break
            if not isDivided:
                sets.append(subSet)
    return list(map(lambda x: ''.join(x), sets))

# _getInitialState calculates the new initial state for the minimal automaton
def _getInitialState(formalDef, minimalStates):
    for state in minimalStates:
        if formalDef[INITIAL] in state:
            return state
    return ''

# _getAcceptStates calculates the new accept state for the minimal automaton
def _getAcceptStates(formalDef, minimalStates):
    accept = []
    for state in minimalStates:
        for finalState in formalDef[ACCEPT]:
            if finalState in state:
                accept.append(state)
    return list(set(accept))

# _getTransitions calculates the transitions for the new automaton
# with its states changes to be the minimal one.
def _getTransitions(formalDef, minimalStates):
    accept = formalDef[ACCEPT]
    transitions = {}
    alphabet = getAlphabet(formalDef)
    for state in minimalStates:
        transitions[state] = {}
        for symbol in alphabet: transitions[symbol] = []
        for symbol in alphabet:
            nextStates = []
            for s in list(state):
                for b in formalDef[TRANSITIONS][s][symbol]:
                    for nextState in minimalStates:
                        if b in nextState: 
                            nextStates.append(nextState)
            transitions[state][symbol] = list(set(nextStates))
    return transitions

# minimization generates a new automaton with the minimal states and transitions
# necessaries to do the same computation as the larger received does
def minimization(formalDef):
    minimal_states = _minimalStates(formalDef)
    initial = _getInitialState(formalDef, minimal_states)
    accept = _getAcceptStates(formalDef, minimal_states)
    transitions = _getTransitions(formalDef, minimal_states)

    minimal_formalDef = {
        STATES: minimal_states,
        INITIAL: initial,
        ACCEPT: accept,
        TRANSITIONS: transitions
    }
    return minimal_formalDef

# handleInput read input commands and redirect to responsible function
def handleInput():
    directories = [d for d in sys.argv[1:] if d not in operations and os.path.isfile(d)]
    operation = next((op for op in sys.argv[1:] if op in operations),'')
    automatas = [readAutomataFile(d) for d in directories]

    result = ''
    if operation == OP_UNION:
        print('Operação de União:')
        result = union(automatas[0], automatas[1])
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
        result = generateComplement(automatas[0])
    elif operation == OP_MINIMIZATION:
        print('Operação Minimização:')
        result = minimization(automatas[0])
    else:
        print('Operação de Simulação:')
        simulate(automatas[0])
        
    if operation != '':
        writeOutputFile(result)


# readAutomataFile reads a text file and specifies the automaton,
# requires the path to file
def readAutomataFile(filePath):
    inputFile = open(filePath, 'r')
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
    
# simulate process the automaton specified,
# when it reads the word given it returns a list
# with the states where the automaton stops at the end of the word
# requires the formal definition of the automaton
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
    showVeredict(formalDef, toProcess)


# showVeredict receives a list with the states the automaton stops
# at the end of a word and verifies if one of them is an accept state
# and shows a message according to it.
# requires the formal definition of the automaton and list of states
def showVeredict(formalDef, states):
    accept = False
    for state in states:
        if (state in formalDef[ACCEPT]): accept = True
    print('\nA palavra %sfoi aceita' % ('nao ' if not accept else ''))


# generateComplement generate the complement automaton for the
# automaton received in the param.
# it returns a formal definition for the complement automaton.
# requires the formal definition of the automaton
def generateComplement(formalDef):
    complementDef = {}
    complementDef[INITIAL] = formalDef[INITIAL]
    complementDef[TRANSITIONS] = formalDef[TRANSITIONS].copy()
    complementDef[STATES] = formalDef[STATES][:]
    complementDef[ACCEPT] = list(set(formalDef[STATES]) - set(formalDef[ACCEPT]))
    return complementDef


# writeOutputFile writes an automaton to the default output
# requires the formal definition of the automaton 
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


# traverse traverses through the automaton 
# and returns all the states it should be after the input is set
# requires the formal definition of the automaton, state and symbol
def traverse(formalDef, state, symbol):
    if state in formalDef[TRANSITIONS]:
        if symbol in formalDef[TRANSITIONS][state]:
            return formalDef[TRANSITIONS][state][symbol]
    return []


# traverse traverses through the automaton 
# and returns all the states it should be after all the inputs are set
# the difference from this to traverse is that it receives multiple states
# requires the formal definition of the automaton, state and symbol
def traverseMultipleStates(formalDef, states, symbol):
    finalStates = []
    for state in states:
        if state in formalDef[TRANSITIONS]:
            if symbol in formalDef[TRANSITIONS][state]:
                finalStates = finalStates + formalDef[TRANSITIONS][state][symbol]
    return finalStates


# traverseIndefinitely traverse indefinitely using a symbol,
# it only stops when the set of states doesn't change after a traverse.
# requires the formal definition of the automaton, state and symbol
def traverseIndefinitely(formalDef, states, symbol):
    previousStates = []
    while True:
        states = set(states).union(set(traverseMultipleStates(formalDef,states,symbol)))
        if states == previousStates:
            break
        previousStates = states
    return states


# nfaTraverse traverses as it would in a nfa
# requires the formal definition of the automaton, state and symbol
def nfaTraverse(formalDef, states, symbol):
    states = traverseIndefinitely(formalDef,states,'e')
    states = traverseMultipleStates(formalDef,states,symbol)
    states = traverseIndefinitely(formalDef,states,'e')
    return states


# findStateFromStateCombinaton is an auxiliar 
# method to build a state string from a combination of states
# requires a list of state combinations and the combination
def findStateFromStateCombinaton(stateCombinations,combination):
    foundCombination = ""
    for comb in stateCombinations:
        if combination == set(comb):
            foundCombination = "_".join(str(state) for state in comb)
            break
    return foundCombination


# getAlphabet(formalDef) get all the symbols of an automaton
# requires the formal definition of the automaton
def getAlphabet(formalDef):
    alphabet = set()
    for state in formalDef[TRANSITIONS]:
        for symbol in formalDef[TRANSITIONS][state]:
            alphabet.add(symbol)
    alphabet.discard('e')
    return alphabet


# nfaToDfa build a dfa from a nfa
# requires the formal definition of the automaton
def nfaToDfa(formalDef):
    newFormalDef = {STATES: [], INITIAL: '', ACCEPT: [], TRANSITIONS: {}}
    
    for s in formalDef[STATES]:
        if "_" in s:
            print("Não foi possível converter o automato para nfa pois o automato utiliza '_' em sua nomenclatura de estados")
            return formalDef

    # CREATE STATE COMBINATIONS (from each state)
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

    # SET ACCEPTING STATES (for every state accept the ones that has at least one accepting state)
    accepting_states = formalDef[ACCEPT]
    newAccepting_states = []

    for states in stateCombinations:
        for accept_state in accepting_states:
            if accept_state in states:
                newAccepting_states.append("_".join(str(state) for state in states))

    newAccepting_states = set(newAccepting_states)
    newFormalDef[ACCEPT] = newAccepting_states

    # SET INITIAL STATE (from the initial state traverse all 'e' symbols until you can't you 
    # get the most states. The initial state is a combination of every single starting state)
    initial = formalDef[INITIAL]
    newInitial = traverseIndefinitely(formalDef,initial,'e')
    newFormalDef[INITIAL] = findStateFromStateCombinaton(stateCombinations,newInitial)
    
    
    # SET TRANSITIONS
    alphabet = getAlphabet(formalDef)
    transitions = formalDef[TRANSITIONS]
    for symbol in alphabet:
        for states in stateCombinations:
            newState = '_'.join(str(state) for state in states)
            newResultStates = nfaTraverse(formalDef,states,symbol)
            newResultState = findStateFromStateCombinaton(stateCombinations,newResultStates)
            if newResultState == '':
                newResultState = '_'
            automataAddTransiton(newFormalDef,newState,symbol,newResultState)    
    return newFormalDef


# automataAddTransiton(formalDef,state,symbol,resultState) adds a 
# transition to an automata even if it doesn't have that key
# requires the formal definition of the automaton, the state, symbol and the result state
def automataAddTransiton(formalDef,state,symbol,resultState):
    try:
        if symbol in formalDef[TRANSITIONS][state]:
            formalDef[TRANSITIONS][state][symbol].append(resultState)
        else:
            formalDef[TRANSITIONS][state][symbol] = [resultState]    
    except KeyError:
        formalDef[TRANSITIONS][state] = {symbol: [resultState]}


# union constructs an automata recognizing the union of the languages of two given automata.
# requires two formal definitions of automata
def union(formalDefA, formalDefB):
    newFormalDef = {
        STATES: ['NEW_STATE'],
        INITIAL: 'NEW_STATE',
        ACCEPT: [],
        TRANSITIONS: {}
    }

    # RENAME STATES
    newFormalDef[STATES] = newFormalDef[STATES] + list(map(lambda oldState: '1_' + oldState, formalDefA[STATES]))
    newFormalDef[STATES] = newFormalDef[STATES] + list(map(lambda oldState: '2_' + oldState, formalDefB[STATES]))

    # RENAME ACCEPT
    newFormalDef[ACCEPT] = newFormalDef[ACCEPT] + list(map(lambda oldState: '1_' + oldState, formalDefA[ACCEPT]))
    newFormalDef[ACCEPT] = newFormalDef[ACCEPT] + list(map(lambda oldState: '2_' + oldState, formalDefB[ACCEPT]))

    # RENAME TRANSITIONS
    for state in formalDefA[TRANSITIONS].keys():
        newFormalDef[TRANSITIONS]['1_' + state] = {}
        for symbol in formalDefA[TRANSITIONS][state]:
            newFormalDef[TRANSITIONS]['1_' + state][symbol] = list(map(lambda oldState: '1_' + oldState, formalDefA[TRANSITIONS][state][symbol]))

    for state in formalDefB[TRANSITIONS].keys():
        newFormalDef[TRANSITIONS]['2_' + state] = {}
        for symbol in formalDefB[TRANSITIONS][state]:
            newFormalDef[TRANSITIONS]['2_' + state][symbol] = list(map(lambda oldState: '2_' + oldState, formalDefB[TRANSITIONS][state][symbol]))

    # ADD NEW STATE TRASITION
    newFormalDef[TRANSITIONS][newFormalDef[INITIAL]] = {
        'e': ['1_' + formalDefA[INITIAL], '2_' + formalDefB[INITIAL]]
    }

    return newFormalDef

# intersection constructs an automata recognizing the intersection of the languages of two given automata.
# requires two formal definitions of automata
def intersection(formalDefA, formalDefB):
    newFormalDef = newFormalDef = {STATES: [], INITIAL: '', ACCEPT: [], TRANSITIONS: {}}
    stateCombinations = list(itertools.product(formalDefA[STATES], formalDefB[STATES]))
    states = []
    # states
    for combinations in stateCombinations:
        states.append("_".join(str(state) for state in combinations))
    newFormalDef[STATES] = states
    # initial
    newFormalDef[INITIAL] = formalDefA[INITIAL] + "_" +  formalDefB[INITIAL]
    # accept
    acceptCombination = list(itertools.product(formalDefA[ACCEPT], formalDefB[ACCEPT]))
    acceptStates = []
    for combinations in acceptCombination:
        acceptStates.append("_".join(str(state) for state in combinations))
    newFormalDef[ACCEPT] = acceptStates
    # transitions
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

# starOperation builds the star operation for the given automaton
# requires the formal definition of automaton
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

 
#transform to dfa   
#dfa = nfaToDfa(formalDef)

def removeUnreachableStates(formalDef):
    reachableStates = findReachableStates(formalDef)
    unreachableStates = set([s for s in formalDef[STATES] if s not in reachableStates])
    formalDef[STATES] = [s for s in formalDef[STATES] if s in reachableStates]
    formalDef[ACCEPT] = [s for s in formalDef[ACCEPT] if s in reachableStates]
    for s in unreachableStates:
        formalDef[TRANSITIONS].pop(s, None)
    return formalDef

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

handleInput()