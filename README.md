# Python Example

Este é um projeto de exemplo para organização de projetos Python utilizando o padrão src layout, automação com Makefile e gerenciamento de dependências com [uv](https://docs.astral.sh/uv/).

## Dependências

- [uv](https://docs.astral.sh/uv/)
- [make](https://www.gnu.org/software/make/)

## Instalação

Sincronize as dependências do projeto:

```bash
uv sync
```

Se precisar instalar a versão correta do Python:

```bash
uv python install
```

## Como rodar o projeto

Execute o script principal:

```bash
uv run start
```

## Rodando os testes

Execute todos os testes com:
```bash
make test
```

## Padronização e qualidade de código

Antes de subir alterações, garanta que o código está formatado e segue os padrões:

```bash
make check-all
```

## Contribuição

Veja as ferramentas auxiliares e comandos disponíveis no Makefile.

## Links úteis

- [Documentação do uv](https://docs.astral.sh/uv/)
- [Documentação do Python](https://docs.python.org/pt-br/3/)
