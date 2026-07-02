# Catálogo de Livros — Projeto Final (Engenharia de Software II)

API REST em FastAPI para cadastro de livros, organizada em camadas
(rotas → service → repository), com regra de negócio própria e
integração com a API pública da [Open Library](https://openlibrary.org/dev/docs/api/books).

## Estrutura

> **Atenção:** todo o código do projeto vive dentro da pasta
> `projeto-final-es-main/` (não na raiz do repositório).

```
projeto-final-es-main/
├── app/
│   ├── main.py            # rotas FastAPI
│   ├── models.py          # schemas Pydantic
│   ├── repository.py      # RepositorioLivros (interface + implementação em memória)
│   ├── services/livro.py  # regras de negócio (ISBN duplicado, ano futuro, Open Library)
│   └── clients/open_library.py  # cliente HTTP da Open Library
├── tests/                 # testes unitários e de integração (pytest)
├── Dockerfile
├── infra.yml              # CloudFormation (não editar)
└── .github/workflows/     # CI (pylint + pytest) e deploy (AWS Academy)
```

## Rodando localmente

```bash
cd projeto-final-es-main
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API disponível em `http://localhost:8000`, documentação Swagger em
`http://localhost:8000/docs`.

## Rodando os testes

```bash
cd projeto-final-es-main
pip install -r requirements.txt
pytest --cov=app --cov-report=term-missing
```

Os testes **não dependem de rede**: toda chamada à Open Library é
mockada (`unittest.mock.patch`).

## Regras de negócio

- Não é permitido cadastrar dois livros com o mesmo ISBN (`409 Conflict`).
- Não é permitido cadastrar um livro com ano de publicação futuro (`400 Bad Request`).
- Ao cadastrar um livro, o título e o autor são complementados/validados
  consultando a Open Library pelo ISBN (se a consulta falhar ou não
  retornar dados, o cadastro segue com os dados enviados pelo cliente).

## CI

Todo Pull Request dispara o workflow `.github/workflows/ci.yml`, que roda:

- `pylint app --fail-under=7.0`
- `pytest --cov=app --cov-fail-under=70`

PRs com o pipeline vermelho não devem ser mesclados (configure isso em
Settings → Branches → Branch protection rules → *Require status checks
to pass before merging*).

## Deploy (AWS Academy)

O deploy usa o `infra.yml` (CloudFormation) já existente, **sem
alterações**. O workflow `.github/workflows/deploy.yml` sobe a stack,
apontando para este mesmo repositório (`RepoSubdir=projeto-final-es-main`).

Secrets necessários (Settings → Secrets and variables → Actions):

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`

Após o deploy, a URL da API fica disponível na aba *Actions* (output
`ApiUrl`) ou via:

```bash
aws cloudformation describe-stacks --stack-name catalogo-livros \
  --query "Stacks[0].Outputs" --output table
```
