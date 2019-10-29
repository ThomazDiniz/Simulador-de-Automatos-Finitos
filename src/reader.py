import sys

# readInputFile() reads a file.txt in the specified format 
# and inserts the data into `formalDef` object.
# required filename passed by argument.
def readInputFile():
    formalDef = {"estados": [], "inicial": "", "aceita": [], "transicoes": []}
    inputFile = open(sys.argv[2], "r")
    while True:
        line = inputFile.readline()
        if not line: break

        args = line.strip().split(" ", 1)
        if(args[0] in formalDef):
            formalDef[args[0]] = args[1].split(',')
        else:
            args = line.strip().split(" ")
            formalDef["transicoes"].append(args)
        
    return formalDef