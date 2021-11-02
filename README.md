# tomasulo-simulator
Este é um simulador para instruções RISCV32I.

## Instalando as dependências
Execute o seguinte comando para instalar as depedências do projeto:

```sh
    $ pip install -r requirements.txt
```

## Configurando o simulador
Caso você queira definir alguma configuração específica do simulador, modifique o arquivo `config.json`.

## Arquivo de entrada
O simulador vai precisar de um arquivo assembly sem preambulos com instruções RISCV32I. O formato do arquivo deverá ser semelhante ao arquivo é o `dump.txt`.

## Executando o simulador
Para executar o simulador, basta executar o seguinte comando:

```sh
    $ python tomasulo.py <arquivo_assembly>
```