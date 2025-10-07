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

Rode as migrations existentes:
```bash
make migrate-head
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

## Mudanças no BD

Mudanças no esquema do banco de dados PostgreSQL, através de atualizações dos models, devem gerar novas migrations e atualizar o estado de migrations do alembic. Para isso rode:

```bash
make migrate "nome da migration"
make migrate-head
```

Não se esqueça de revisar a migration criada em alembic/versions

## Links úteis

- [Documentação do uv](https://docs.astral.sh/uv/)
- [Documentação do Python](https://docs.python.org/pt-br/3/)
- [Documentação do make](https://www.gnu.org/software/make/manual/)
- [Tutorial de Makefile](https://makefiletutorial.com/)

## Troubleshooting
Você pode enfrentar alguns erros relacionados a instalação do driver para PostgreSQL psicopg2. Caso seja um erro de compilação da biblioteca use o comando abaixo:
```bash
sudo apt update
sudo apt install -y libpq-dev gcc python3-dev
```