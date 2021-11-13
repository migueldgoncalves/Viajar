# Viajar

Viajar de carro, barco, comboio e avião, pelo Baixo Guadiana e mais além, unicamente com recurso a código

Desenvolvido em Python 3.9

## Apresentação

Este projecto está dividido em 2 partes: a viagem propriamente dita pelo Baixo Guadiana, e uma simulação de carro

As 2 partes do projecto podem ser executadas de forma independente ou interligada.

### Viagem pelo Baixo Guadiana

Esta parte do projecto inclui um conjunto de locais pelos quais é possível viajar.
Esses locais podem ser povoações, estradas ou pontos de interesse, e na sua maioria estão localizados no Baixo Guadiana.

A viagem começa num local determinado por uma constante no ficheiro [viajar.py](https://github.com/migueldgoncalves/Viajar/blob/master/src/viajar/viajar.py).
O programa mostra então os locais adjacentes, e permite que se escolha um deles para se viajar para o mesmo.
Ao chegar-se a esse local são mostrados os locais adjacentes ao mesmo e para os quais se podem viajar, e assim sucessivamente.

A área coberta pelo mapa corresponde, aproximadamente, a um triângulo formado pelas cidades de Beja, Faro e Sevilha, com ênfase no Baixo Guadiana.

A lista de locais disponíveis não é exaustiva, mesmo dentro do Baixo Guadiana.

A viagem engloba diversos modos de transporte.
O carro é o modo predominante, e está disponível em praticamente todos os locais.
Corresponde sempre a estradas reais, e é o único modo de transporte para o qual se contabilizam as distâncias.

Os restantes modos de transporte servem de atalhos entre locais, em maior ou menor medida, e podem ou não corresponder a rotas existentes:

- Barco - Permite percorrer o Rio Guadiana entre Mértola e Vila Real de Santo António, assim como aceder à Ria Formosa;
- Comboio - Disponível entre Faro e Vila Real de Santo António, na zona do Pomarão e entre Ayamonte e Sevilha;
- Avião - Permite viajar de forma instantânea entre os extremos do mapa, que são as cidades de Faro, Beja e Sevilha
- Metro - Disponível dentro de Sevilha, permite atravessar a cidade passando por menos locais

### Simulação de carro

Esta parte do projecto permite realizar as acções base de um veículo motorizado: acelerar, travar e mudar de mudança.

Podem ser ajustados alguns parâmetros do carro através das constantes do ficheiro [carro.py](https://github.com/migueldgoncalves/Viajar/blob/master/src/carro/carro.py).
Estes incluem o número de mudanças disponíveis, a velocidade máxima e a aceleração em cada mudança.

A simulação de carro começa por simular uma aceleração durante um certo número de segundos, definido numa constante do mesmo ficheiro.
Durante esse tempo é necessário que o utilizador mantenha premida a tecla ENTER.
Isto é necessário para medir o número de inputs que o computador consegue ler por segundo, número que será usado em cálculos futuros.

Em seguida, é possível conduzir-se livremente o carro simulado.
Alcançar e permanecer na redline não tem consequências para a simulação.

### Executar os scripts

Para executar a viagem pelo Baixo Guadiana, correr o script [main_viagem.py](https://github.com/migueldgoncalves/Viajar/blob/master/src/main_viagem.py).
No início da execução será pedido se se quer incluir ou não a simulação de carro.

Em caso afirmativo, será necessário conduzir de um local para outro quando a viagem se faça por estrada.
Viagens realizadas noutro modo de transporte serão instantâneas.

Em caso negativo, todas as viagens entre locais serão instantâneas.
Para calcular o tempo de viagem, será obtida uma velocidade média aleatória entre dois valores definidos no ficheiro [viajar.py](https://github.com/migueldgoncalves/Viajar/blob/master/src/viajar/viajar.py).

Para executar a simulação de carro, correr o script [main_carro.py](https://github.com/migueldgoncalves/Viajar/blob/master/src/main_carro.py).
A simulação irá correr por tempo e distância indefinidos até ser interrompida pelos utilizadores.

**NOTA**

É necessário correr a simulação de carro num terminal normal do Windows ou equivalente.
Quer se execute por si mesma, quer esteja incluída na viagem pelo Baixo Guadiana.

Isso deve-se ao uso da biblioteca msvcrt para detectar e ler teclas pressionadas

O comando Run do IDE PyCharm apenas irá funcionar se em Run > Edit Configurations se seleccione a opção Emulate terminal in output console.
Porém, com esse comando todos os caracteres não-ASCII irão aparecer desformatados

## Links úteis

* [Criar novo meio de transporte](https://github.com/migueldgoncalves/Viajar/blob/master/docs/criar_novo_meio_transporte.md)