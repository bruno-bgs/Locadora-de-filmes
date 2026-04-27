# Locadora de Filmes

Aplicação web para cadastro de filmes e clientes, controle de aluguéis e devoluções.

O projeto foi feito para praticar integração entre frontend, backend e banco de dados em um fluxo simples de locadora.

## Funcionalidades

- Cadastro de filmes
- Cadastro de clientes
- Listagem de filmes
- Controle de disponibilidade dos filmes
- Registro de aluguéis
- Registro de devoluções
- Visualização de aluguéis em andamento e devolvidos

## Tecnologias

### Frontend

- React
- Vite
- CSS

### Backend

- Python
- Flask
- mysql-connector-python

### Banco de dados

- MySQL

## Estrutura do projeto

```text
locadora-filmes/
├── backend/
│   ├── app.py
│   ├── clientes.py
│   ├── conexao.py
│   ├── filmes.py
│   └── inserir.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Como executar

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd locadora-filmes
```

### 2. Configure o banco de dados

O backend usa MySQL local. A conexão atual está em `backend/conexao.py`.

Verifique se:

- o MySQL está em execução
- o banco `locadora` existe
- o usuário e a senha configurados em `conexao.py` estão corretos

Exemplo atual:

```python
host="localhost"
user="root"
password="root"
database="locadora"
```

### 3. Instale as dependências do backend

Na pasta `backend`:

```bash
pip install flask mysql-connector-python
```

### 4. Inicie o backend

```bash
cd backend
python app.py
```

O backend ficará disponível em:

- `http://localhost:5000/`

### 5. Instale as dependências do frontend

Em outro terminal:

```bash
cd frontend
npm install
```

### 6. Inicie o frontend

```bash
npm run dev
```

O frontend ficará disponível em:

- `http://localhost:5173/`

## Rotas principais da API

- `GET /filmes`
- `POST /filmes`
- `GET /clientes`
- `POST /clientes`
- `GET /alugueis`
- `POST /alugueis`
- `POST /devolucoes`

## Observações

- O frontend consome a API local em `http://localhost:5000`
- Para o cadastro funcionar no navegador, o backend já está configurado para aceitar requisições do frontend local
- O projeto ainda é voltado para ambiente local de estudo

## Melhorias futuras

- Separar melhor os componentes do frontend
- Padronizar respostas da API
- Adicionar variáveis de ambiente para configuração
- Melhorar validações de formulário
- Publicar uma versão online para demonstração

## Autor

Bruno Borges
https://github.com/bruno-bgs
