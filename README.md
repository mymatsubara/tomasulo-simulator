# tomasulo-simulator
Este é um simulador para instruções RISCV32I escrito em python.

## Instalando as dependências
Execute o seguinte comando para instalar as depedências do projeto (lista de dependências no arquivo `requirements.txt`):

```sh
    $ pip install -r requirements.txt
```

## Configurando o simulador
Caso você queira definir alguma configuração específica do simulador, modifique o arquivo `config.json`.

## Arquivo de entrada
O simulador vai precisar de um arquivo assembly sem preambulos com instruções RISCV32I. O formato do arquivo deverá ser semelhante ao arquivo `test_files/dump.txt`.

## Executando o simulador
Para executar o simulador, basta executar o seguinte comando:

```sh
    $ python tomasulo.py <arquivo_assembly>
```

## Implementação
Foi considerado que o pipeline tem 4 estágios: decode, emission, execution e write. A implementação de cada um deles está presente na pasta `stages`.

O arquivo `tomasulo.py` contém a implementação do loop principal do algoritmo, carregamento das configurações do simulador e é lá onde são instanciadas todas as tabelas utilizadas durante o algoritmo.

Além disso, o arquivo `Instruction.py` possui a implementação da classe `Instruction` e do enum `InstructionFormat`, ambos utilizados para facilitar a interpretação de instruções durante o ciclo de vida do algoritmo.
