Prova de Seleção de Estágio - FastAPI, Pydantic e SQLAlchemy

Objetivo:
Criar uma API simples utilizando FastAPI, Pydantic, SQLAlchemy para cadastrar
empresas e gerenciar obrigações acessórias que a empresa precisa declarar para o
governo.

Requisitos da Prova:
1. Configuração do Ambiente
a. Criar um repositório no GitHub e compartilhar o link (deixar link
público)
b. Para este projeto, colocar todos os arquivos na pasta raiz do
repositório (sem criar subpastas)
c. Criar um ambiente virtual e instalar as dependências necessárias: pip
install fastapi[all] sqlalchemy psycopg2 pydantic
d. Configurar um banco de dados PostgreSQL com SQLAlchemy
2. Modelagem de Dados (SQLAlchemy & Pydantic): Criar os seguintes modelos:
Empresa (Empresa):
id: int (PK)
nome: str
cnpj: str (único)
endereco: str
email: str
telefone: str
Obrigação Acessória (ObrigacaoAcessoria):
id: int (PK)
nome: str
periodicidade: str (mensal, trimestral, anual)
empresa_id: int (FK -> Empresa)

Criar schemas Pydantic para entrada e saída de dados.
3. Implementação de CRUD de Empresa e ObrigacaoAcessoria utilizando o
FastAPI.
4. Banco de Dados e Configuração:

a. Criar um arquivo de configuração .env para armazenar as credenciais
do banco de dados.
b. Criar a conexão com o banco de dados usando SQLAlchemy.
c. Criar um script de migração para gerar as tabelas no banco.
5. Testes e Documentação:
a. Implementar testes unitários para validar os endpoints.
b. Garantir que a documentação da API esteja disponível no Swagger UI
(/docs).
