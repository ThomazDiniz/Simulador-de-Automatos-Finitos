# Simulador de Automatos Finitos

Simulador de autômatos finitos com interface de linha de comando desenvolvido em Python 3.

### Operações

As seguintes operações são suportadas:

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

`py main.py path_to_automata -s`

#### Operação Complemento (-c)

`py main.py path_to_automata -s`

#### Operação Minimização (-m)

`py main.py path_to_automata -m`

#### União (-u)

`py main.py path_to_automata1 path_to_automata2 -u`

#### Intersecção (-i)

`py main.py path_to_automata1 path_to_automata2 -i`

### Como funcionam as operações?

#### Conversão de NFA para DFA

Um DFA é um autômato determinístico, um NFA é não-determinístico. Um DFA, dada uma entrada, toma apenas um caminho através dos seus estados. Um NFA toma todos os caminhos possíveis para aquela entrada, e aceita entrada se pelo menos um caminho termina em um estado final. DFAs, NFAs e expressões regulares todos expressam a mesma classe de conjunto de símbolos. Isso quer dizer que podemos converter de um para outro.

#### Complemento

Operação na qual se inverte as condições de aceitação e não aceitação do autômato transformando os estados finais em não finais e vice-versa. Além disso, é necessário garantir que o autômato só irá parar ao terminar de ler toda a entrada. Para isso, deve-se introduzir um novo estado que será destino de todas as transições anteriormente indefinidas.

#### Estrela (Fecho de Kleene)

Operação na qual é criado um novo estado inicial. O novo estado se torna o estado inicial e aceitação. Transições que aceitam a cadeia vazia são criadas entre os estados de aceitação e o antigo estado inicial.

#### Minimização

Um AFD é mínimo para a linguagem se nenhum AFD para essa linguagem contém menor número de estados. Para isso, elimina-se os estados não alcançáveis a partir do estado inicial. Por fim, substitui-se cada grupo de estados equivalentes por um único estado.

#### União

Operação realizada através do produto de dois autômatos, que nada mais é do que a execução de dois autômatos em paralelo. É criado um novo estado inicial com transições que aceitam a cadeia vazia para a junção dos dois autômatos. Após isso é calculado o produto.

#### Intersecção

Operação realizada através da combinação de todos os estados do autômato incluindo os de aceitação. Após isso, adiconam-se transições entre os estados transversos dos dois autômatos.
