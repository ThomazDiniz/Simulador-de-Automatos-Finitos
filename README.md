# Simulador de Automatos Finitos

### Operações 
- Simulação
- Conversão de NFA para DFA
- Complemento
- Estrela
- Minimização
- União
- Intersecção

### Como rodar
Vá até o diretório do src do projeto e execute com python 3 utilizando os parâmetros:


`cd "path_to_src"`

`py main.py "path_to_automata1" "path_to_automata2" "operation"`

As operações possíveis são: 

`'-u','-i','-d','-s','-c','-m'`

### Exemplos de execução
#### Simulação 
`py main.py path_to_automata word`
#### Conversão NFA para DFA (-d)
`py main.py path_to_automata -d`
#### Operação Estrela (-s)
`py main.py path_to_automata -s``
#### Operação Complemento (-c)
`py main.py path_to_automata -s``
#### Operação Minimização (-m)
`py main.py path_to_automata -m`
#### União (-u)
`py main.py path_to_automata1 path_to_automata2 -u
#### Intersecção (-i)
`py main.py path_to_automata1 path_to_automata2 -i`
