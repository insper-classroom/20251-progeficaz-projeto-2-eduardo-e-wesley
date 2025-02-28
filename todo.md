
## 1️⃣ Configuração do Ambiente
- [ ] Criar repositório no GitHub e clonar para a máquina local
- [ ] Criar ambiente virtual e instalar dependências:
  ```sh
  python -m venv venv
  source venv/bin/activate  
  # No Windows: venv\Scripts\activate
  pip install flask flask-mysql flask-restful pytest requests pymysql python-dotenv gunicorn
  ```
- [ ] Criar estrutura do projeto:
  ```
  /imobiliaria
  ├── app/
  │   ├── __init__.py
  │   ├── routes.py
  │   ├── models.py
  │   ├── database.py
  │   ├── services.py
  │   ├── controllers.py
  ├── tests/
  │   ├── test_routes.py
  │   ├── test_services.py
  ├── config.py
  ├── run.py
  ├── requirements.txt
  ├── README.md
  ```

## 2️⃣ Banco de Dados (MySQL)
- [ ] Criar instância MySQL
- [ ] Criar arquivo `.env` com credenciais do banco:
  ```
  DB_HOST=<host>
  DB_USER=<user>
  DB_PASSWORD=<password>
  DB_NAME=<dbname>
  ```
- [ ] Criar conexão com o banco em `database.py`
- [ ] Executar o script SQL fornecido:
  ```sh
  mysql -h <host> -u <user> -p <dbname> < /mnt/data/imoveis.sql
  ```

## 3️⃣ Desenvolvimento da API seguindo TDD
- [ ] Criar testes para todas as rotas em `tests/test_routes.py`
- [ ] Rodar os testes e garantir que falhem (`pytest -v`)
- [ ] Implementar rotas em `routes.py`:
  - [ ] `GET /imoveis` - Listar todos os imóveis
  - [ ] `GET /imoveis/<id>` - Buscar um imóvel pelo ID
  - [ ] `POST /imoveis` - Adicionar novo imóvel
  - [ ] `PUT /imoveis/<id>` - Atualizar imóvel existente
  - [ ] `DELETE /imoveis/<id>` - Remover imóvel
  - [ ] `GET /imoveis/tipo/<tipo>` - Listar imóveis por tipo
  - [ ] `GET /imoveis/cidade/<cidade>` - Listar imóveis por cidade
- [ ] Rodar os testes e garantir que todos passem (`pytest -v`)

## 4️⃣ Implementar Nível 3 da Maturidade de Richardson (HATEOAS)
- [ ] Adicionar links de navegação em todas as respostas da API

## 5️⃣ Deploy na AWS EC2
- [ ] Criar instância EC2 na AWS
- [ ] Permitir conexões na porta 5000 no **Security Group**
- [ ] Instalar Python e dependências na instância EC2:
  ```sh
  sudo apt update
  sudo apt install python3 python3-pip
  pip install flask pymysql gunicorn
  ```
- [ ] Clonar repositório na instância EC2 e rodar API:
  ```sh
  git clone <seu-repo>
  cd imobiliaria
  gunicorn --bind 0.0.0.0:5000 run:app
  ```
- [ ] Testar API:
  ```sh
  curl http://<IP-PUBLICO>:5000/imoveis
  ```

## 6️⃣ Checklist Final para A+
- [ ] Banco de dados MySQL na Aiven funcionando
- [ ] Todas as rotas RESTful implementadas corretamente
- [ ] Testes automatizados cobrindo todas as rotas (**TDD**)
- [ ] Implementação do HATEOAS para atingir **Maturidade de Richardson Nível 3**
- [ ] API rodando na AWS EC2 e acessível publicamente
- [ ] API retorna os códigos HTTP corretos e responde com JSON corretamente

---
