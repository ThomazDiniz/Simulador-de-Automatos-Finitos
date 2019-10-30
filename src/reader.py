import sys

ACCEPT      = 'aceita'
STATES      = 'estados'
INITIAL     = 'inicial'
TRANSITIONS = 'transicoes'

# readInputFile() reads a file.txt in the specified format 
# and inserts the data into `formalDef` object.
# required filename passed by argument.
def readInputFile():
    formalDef = {STATES: [], INITIAL: "", ACCEPT: [], TRANSITIONS: {}}
    inputFile = open(sys.argv[2], "r")
    while True:
        line = inputFile.readline()
        if not line: break

        args = line.strip().split(" ", 1)
        if(args[0] in formalDef):
            formalDef[args[0]] = args[1].split(',')
        else:
            currentState, nextState, symbol = line.strip().split(" ")
            if (formalDef[TRANSITIONS].has_key(currentState)):
                if (formalDef[TRANSITIONS].has_key(symbol)):
                    formalDef[TRANSITIONS][currentState][symbol].append(nextState)
                else:
                    formalDef[TRANSITIONS][currentState][symbol] = [nextState]
            else:
                formalDef[TRANSITIONS][currentState] = {symbol: [nextState]}
        
    return formalDef