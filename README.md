## README - Instruções de Configuração e Execução

Este projeto contém uma API Flask para gerenciamento de imóveis, seguindo uma arquitetura em camadas (controllers, repositories, etc.). Abaixo estão os passos para **inicializar** o projeto localmente, **rodar os testes** em diferentes sistemas operacionais e os detalhes das rotas disponíveis na aplicação.

---

## 1. **Pré-requisitos**

- **Python** instalado:
  - No macOS e Linux, verifique com `python3 --version`.
  - No Windows, verifique com `python --version` ou `py --version`.

---

## 2. **Clonar o Repositório**

Caso ainda não tenha o projeto localmente, clone via Git:

```bash
git clone git@github.com:insper-classroom/20251-progeficaz-projeto-2-eduardo-e-wesley.git
cd SEU_REPOSITORIO
```

Se já tiver o projeto baixado de outra forma (ex.: ZIP), basta entrar no diretório principal do projeto.

---

## 3. **Criar e Ativar Ambiente Virtual**

Recomendamos o uso de um **ambiente virtual** para isolar as dependências do projeto. O comando varia conforme o sistema operacional.

### **macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **Windows (CMD)**

```bash
python -m venv venv
venv\Scripts\activate
```

### **Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 4. **Instalar Dependências**

Com o ambiente virtual **ativado**, instale as dependências listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

Se estiver usando Python no Windows e o comando `pip` não funcionar, tente:

```bash
python -m pip install -r requirements.txt
```

---

## 5. **Configurar Variáveis de Ambiente (opcional)**

Se o projeto utiliza um arquivo `.env` com variáveis como `DB_HOST`, `DB_USER`, etc., crie/edite seu `.env` na raiz do projeto. Exemplo:

```
DB_CONNECTION=
DB_HOST=
DB_PORT=
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=
SSL_CA_PATH=
```

Certifique-se de que o projeto está lendo o `.env` adequadamente (usando, por exemplo, `python-dotenv`).

---

## 6. **Executar a API**

No diretório raiz do projeto (onde está o `main.py` ou o script principal), rode:

```bash
python app/main.py
```

ou, se você tiver uma função `create_app()`, pode ser algo como:

```bash
cd app
python main.py
```

- A API Flask iniciará em modo debug, exibindo algo como:  
  `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

- Acesse no navegador:  
  [http://127.0.0.1:5000/imoveis](http://127.0.0.1:5000/imoveis)

---

## 7. **Rodar os Testes**

Dentro do **diretório raiz** do projeto, execute:

```bash
python -m pytest
```

ou simplesmente:

```bash
pytest
```

Isso irá procurar pelos arquivos de teste (`test_*.py`) e executar os testes, exibindo um resumo dos resultados.

> Se estiver em Windows, você pode precisar do comando `py -m pytest`.

---

## 8. **Estrutura Geral do Projeto (Exemplo)**

```
SEU_REPOSITORIO/
├─ app/
│  ├─ __init__.py
│  ├─ main.py                 # Script principal Flask
│  ├─ controllers/
│  │  └─ imoveis.py           # Rotas da API
│  ├─ repositories/
│  │  └─ imoveis_repo.py      # Funções de acesso ao DB
│  ├─ database/
│  │  └─ connection.py        # Função connect_db()
│  ├─ services/
│  │  └─ links.py             # Funções de geração de links HATEOAS
│  └─ tests/
│     └─ test_api.py          # Arquivo de testes
├─ requirements.txt
└─ README.md
```

---

## 9. **Rotas da API**

As rotas disponíveis na aplicação estão configuradas para o IP `50.16.164.251` e estão descritas a seguir conforme o export do Postman:

### **Listar Todos os Imóveis**
- **Método:** GET  
- **URL:** `http://50.16.164.251/imoveis`  
- **Descrição:** Retorna uma lista de todos os imóveis cadastrados, com detalhes como `id`, `bairro`, `cep`, `cidade`, `data_aquisicao`, `logradouro`, `tipo`, `tipo_logradouro` e `valor`.

### **Listar um Imóvel Específico pelo ID**
- **Método:** GET  
- **URL:** `http://50.16.164.251/imoveis/{id}`  
- **Exemplo:** `http://50.16.164.251/imoveis/1000`  
- **Descrição:** Retorna os detalhes de um imóvel específico com base no ID fornecido.

### **Adicionar um Novo Imóvel**
- **Método:** POST  
- **URL:** `http://50.16.164.251/imoveis`  
- **Exemplo de Body (JSON):**

```json
{
    "logradouro": "av. Europa",
    "tipo_logradouro": "Avenidaaa",
    "bairro": "Jd. Europa",
    "cidade": "São Paulo",
    "cep": "01449000",
    "tipo": "casa",
    "valor": 20000000,
    "data_aquisicao": "2019-12-12"
}
```

- **Descrição:** Insere um novo imóvel na base de dados com as informações enviadas.

### **Atualizar um Imóvel Existente**
- **Método:** PUT  
- **URL:** `http://50.16.164.251/imoveis/{id}`  
- **Exemplo:** `http://50.16.164.251/imoveis/1004`  
- **Exemplo de Body (JSON):**

```json
{
    "logradouro": "av. Europa",
    "tipo_logradouro": "Avenida88",
    "bairro": "Jd. Europaaaa",
    "cidade": "São Paulo",
    "cep": "01449000",
    "tipo": "casa",
    "valor": 20000000,
    "data_aquisicao": "2019-12-12"
}
```

- **Descrição:** Atualiza os dados de um imóvel existente identificado pelo ID informado.

### **Remover um Imóvel Existente**
- **Método:** DELETE  
- **URL:** `http://50.16.164.251/imoveis/{id}`  
- **Exemplo:** `http://50.16.164.251/imoveis/1004`  
- **Descrição:** Remove o imóvel com o ID especificado da base de dados.

### **Listar Imóveis por Tipo**
- **Método:** GET  
- **URL:** `http://50.16.164.251/imoveis/tipo/{tipo}`  
- **Exemplo:** `http://50.16.164.251/imoveis/tipo/casa`  
- **Descrição:** Retorna uma lista de imóveis filtrados pelo tipo (por exemplo, "casa").

### **Listar Imóveis por Cidade**
- **Método:** GET  
- **URL:** `http://50.16.164.251/imoveis/cidade/{cidade}`  
- **Exemplo:** `http://50.16.164.251/imoveis/cidade/North Garyville`  
- **Descrição:** Retorna uma lista de imóveis filtrados pela cidade especificada.

---