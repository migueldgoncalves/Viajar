## Criar novo meio de transporte

Este tutorial descreve como acrescentar um novo meio de transporte ao projecto Viajar.

### Requisitos

Conhecimentos de programação são recomendados.

### Passos

1. Aceder ao ficheiro [viajar.py](https://github.com/migueldgoncalves/Viajar/blob/master/src/viajar/viajar.py).
2. Nas constantes referentes às opções do menu, acrescentar uma constante para o novo meio de transporte. O nome da constante deverá ter o formato `<meio_transporte>_STRING`, em maiúsculas e sem acentos. Por exemplo, para o avião a string é `AVIAO_STRING`.
3. Nas constantes referentes aos meios de transporte, acrescentar uma constante para o novo meio de transporte.
4. No método `mudar_modo`, no if do método, acrescentar um elif para o novo meio de transporte. A string a imprimir deverá ter um `\n` no início.
5. No método `realizar_viagem`, no bloco de código das opções de mudança de modo, acrescentar um elif para o novo meio de transporte. O print a colocar dentro do elif deverá ter o formato `print(iterador, SEPARADOR_MODO, <meio_transporte_string>)`, onde `<meio_transporte_string>` é a constante criada no passo 2.

O novo meio de transporte já pode ser usado no projecto.

Boa viagem!