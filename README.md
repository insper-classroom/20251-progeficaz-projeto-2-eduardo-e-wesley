## README - Instruções de Configuração e Execução

Este projeto contém uma API Flask para gerenciamento de imóveis, seguindo uma arquitetura em camadas (controllers, repositories, etc.). Abaixo estão os passos para **inicializar** o projeto localmente e **rodar os testes** em diferentes sistemas operacionais.

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

Se estiver usando Python no Windows e o comando `pip` não funcionar, tente `python -m pip install -r requirements.txt`.

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

Certifique-se de que o projeto está lendo o `.env` adequadamente (usando `python-dotenv`, por exemplo).

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

- A API Flask deve iniciar em modo debug, exibindo algo como:  
  `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

- Acesse no navegador:  
  [http://127.0.0.1:5000/imoveis](http://127.0.0.1:5000/imoveis)

---

## 7. **Rodar os Testes**

Dentro do **diretório raiz** do projeto, execute:

```bash
python -m pytest
```
ou apenas:

```bash
pytest
```

Isso irá procurar pelos arquivos de teste (`test_*.py`) e rodar cada teste, exibindo um resumo dos resultados.

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