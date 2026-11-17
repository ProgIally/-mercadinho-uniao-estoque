# Mercadinho União — Sistema de Controle de Estoque

Sistema web desenvolvido em Python, Flask e SQLite para gerenciar o estoque de um pequeno estabelecimento comercial.

## 1. Objetivo

O projeto tem como objetivo facilitar o controle de produtos, registrar entradas e saídas de mercadorias e identificar produtos que precisam de reposição.

O sistema foi desenvolvido como projeto acadêmico, aplicando conceitos de programação, banco de dados, desenvolvimento web e testes automatizados.

## 2. Tecnologias utilizadas

- Python — linguagem de programação principal
- Flask — framework para desenvolvimento web
- SQLite — banco de dados relacional
- HTML e CSS — estrutura e apresentação das páginas
- Pytest — execução de testes automatizados
- Git e GitHub — versionamento do projeto
- GitHub Actions — automação dos testes

## 3. Funcionalidades

### Consulta de estoque

- Listagem dos produtos cadastrados
- Visualização das quantidades disponíveis
- Consulta do estoque mínimo
- Identificação da situação de cada produto

### Cadastro de produtos

- Cadastro de novos produtos
- Definição da quantidade inicial
- Configuração do estoque mínimo
- Validação dos dados informados

### Movimentação de estoque

- Registro de entradas de mercadorias
- Registro de saídas de mercadorias
- Atualização das quantidades disponíveis
- Bloqueio de saídas superiores ao estoque disponível
- Registro das movimentações no banco de dados

### Alertas de estoque

- Identificação de produtos com estoque baixo
- Identificação de produtos que atingiram o estoque mínimo
- Exibição dos produtos que precisam de reposição

## 4. Estrutura do projeto

```text
mercadinho-uniao-estoque/
├── .github/
│   └── workflows/
│       └── tests.yml
├── static/
├── templates/
│   ├── alertas.html
│   ├── base.html
│   ├── cadastro.html
│   ├── estoque.html
│   ├── login.html
│   └── movimentacao.html
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_models.py
│   ├── test_movimentacoes.py
│   └── test_produtos.py
├── .gitignore
├── app.py
├── config.py
├── database.py
├── models.py
├── requirements.txt
└── README.md
```

## 5. Banco de dados

O sistema utiliza SQLite para armazenar as informações.

### Tabela produto

Armazena:

- ID do produto
- Nome
- Quantidade disponível
- Estoque mínimo

### Tabela movimentacao

Armazena:

- ID da movimentação
- ID do produto
- Tipo de movimentação (entrada ou saída)
- Quantidade movimentada
- Data da movimentação

As tabelas possuem restrições de integridade para evitar quantidades inválidas e manter o relacionamento entre produtos e movimentações.

## 6. Como executar o projeto

### Requisitos

- Python instalado
- Git (para clonar o repositório)
- Navegador web

### Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd mercadinho-uniao-estoque
```

Substitua `URL_DO_REPOSITORIO` pelo endereço real do projeto no GitHub.

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar o ambiente virtual

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=substitua_por_uma_chave_aleatoria_segura
```

O arquivo `.env` não deve ser enviado ao GitHub.

### Inicializar o banco de dados

```bash
python database.py
```

### Iniciar a aplicação

```bash
python app.py
```

Acesse no navegador:

http://127.0.0.1:5000

## 7. Testes automatizados

O projeto utiliza Pytest para validar as principais regras de negócio e funcionalidades.

Os testes contemplam:

- Validação de nomes de produtos
- Validação de quantidades
- Cadastro de produtos
- Entrada de mercadorias
- Saída de mercadorias
- Bloqueio de estoque insuficiente
- Registro de movimentações
- Alertas de estoque mínimo
- Alertas de estoque abaixo do mínimo
- Operações realizadas pelas rotas da aplicação

### Executar os testes

```bash
python -m pytest tests/ -v
```

### Resultado da última execução local

**19 testes executados e aprovados.**

Os testes utilizam um banco temporário para evitar alterações nos dados reais da aplicação.

## 8. Integração contínua

O projeto possui um workflow do GitHub Actions em:

`.github/workflows/tests.yml`

O workflow configura o ambiente Python, instala as dependências e executa os testes automatizados.

## 9. Segurança

O projeto utiliza algumas práticas básicas de segurança:

- Chave secreta configurada por variável de ambiente
- Arquivo `.env` ignorado pelo Git
- Banco de dados local ignorado pelo Git
- Validação das entradas de dados
- Consultas SQL parametrizadas
- Restrições de integridade no banco de dados

## 10. Considerações finais

O Mercadinho União demonstra a aplicação prática de conceitos de desenvolvimento de software na construção de um sistema de controle de estoque.

A solução integra interface web, regras de negócio, persistência de dados, validações e testes automatizados.

O projeto pode ser expandido futuramente com autenticação de usuários, relatórios gerenciais e novas funcionalidades administrativas.

## Revisão técnica do MVP

### Arquitetura e organização

O Mercadinho União utiliza Python, Flask e SQLite para implementar o controle de estoque. A aplicação está organizada em arquivos responsáveis pelas rotas HTTP (`app.py`), regras de negócio (`models.py`) e acesso ao banco de dados (`database.py`).

Essa separação facilita a manutenção, a identificação de responsabilidades e a execução de testes automatizados.

### Qualidade e segurança

O sistema possui validações para impedir o cadastro de produtos com nomes inválidos, quantidades negativas e nomes superiores a 100 caracteres.

As movimentações de estoque verificam a disponibilidade dos produtos antes de permitir uma saída. As consultas SQL utilizam parâmetros para os valores fornecidos à aplicação.

O projeto também utiliza testes automatizados com pytest e integração contínua pelo GitHub Actions.
