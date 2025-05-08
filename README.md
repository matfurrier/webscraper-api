[EN](#english) | [PT](#portugues)

---

<a name="english"></a>
## 🇺🇸 English

# WebScraper API 🕷️📊
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

RESTful API for periodic scraping with Playwright + FastAPI + MongoDB

A modern RESTful API built with FastAPI, capable of collecting web data using Playwright (JavaScript headless rendering), storing it in MongoDB, and displaying it via a dashboard or exportable endpoints (JSON/CSV). Ideal for automated scraping of public portals and generating periodic reports.

## ⚙️ Technologies

*   Python 3.10+
*   FastAPI
*   MongoDB
*   APScheduler
*   Playwright (for scraping, replacing the need for Selenium)
*   BeautifulSoup4 (for parsing HTML post-Playwright)
*   Pandas
*   Jinja2 (for Dashboard)
*   Docker & Docker Compose
*   Uvicorn & Gunicorn

## 📌 Features

*   **Web Scraping:**
    *   Collects data from the [CEPEA/ESALQ Soybean Indicator](https://www.cepea.esalq.usp.br/br/indicador/soja.aspx) (configurable via `TARGET_URL`) using Playwright to render JavaScript.
    *   Runs periodically (configurable via `SCRAPE_INTERVAL_HOURS`).
*   **REST API (FastAPI) & UI:**
    *   `GET /`: Root path.
    *   `GET /dashboard`: Simple HTML dashboard (embedded frontend UI) to view the data.
    *   `GET /api/data`: Returns all collected data.
    *   `GET /api/data/{id}`: Returns a specific item by ID.
    *   `POST /api/scrape`: Triggers a manual scraping process (runs in the background).
    *   `GET /api/export/json`: Downloads all data in JSON format.
    *   `GET /api/export/csv`: Downloads all data in CSV format.
    *   Interactive API documentation (Swagger UI) available at `/docs`.
*   **Database:**
    *   MongoDB for data storage.
    *   Schema: `{ "_id": ObjectId (string in API), "fonte": "string", "dados": {"tabela_completa": List[List[str]] }, "data_coleta": "datetime" }` (The `dados` field now contains the full extracted table).
*   **Scheduling:**
    *   Scraping job runs at a defined interval (default: 12 hours).
*   **Docker:**
    *   Container for the FastAPI application and scheduler (includes Playwright setup).
    *   Container for MongoDB.
    *   Persistent volume for MongoDB data.

## 📁 Folder Structure

```
webscraper-api/
├── app/
│   ├── api.py          # REST API routes (/api/*)
│   ├── db.py           # MongoDB connection and Pydantic schemas
│   ├── export.py       # Export functionalities (CSV/JSON)
│   ├── main.py         # FastAPI app, UI routes, lifecycle
│   ├── scheduler.py    # Scraping scheduler (APScheduler)
│   ├── scraper.py      # Scraping logic (Playwright + BeautifulSoup)
│   └── templates/
│       └── dashboard.html  # Dashboard HTML via Jinja2
├── Dockerfile          # Defines the Docker image for the application
├── docker-compose.yml  # Orchestrates containers (API + MongoDB)
├── requirements.txt    # Python dependencies
└── .env.example        # Environment settings (example)
```

## 🚀 Running the Project

### Prerequisites

*   Docker
*   Docker Compose

### 1. Environment Variables

Copy the `.env.example` file to `.env` in the project root (`webscraper-api/`) and adjust the variables as needed:

```bash
cp .env.example .env
```

Contents of `.env` (example):

```env
SCRAPE_INTERVAL_HOURS=12
TARGET_URL=https://www.cepea.esalq.usp.br/br/indicador/soja.aspx
MONGO_URI=mongodb://mongodb:27017/
MONGO_DB_NAME=scraper_db
PORT=8000
```

**Note:** The `docker-compose.yml` already defines default values for these variables. The local `.env` file allows you to easily override them.

### 2. Build and Run with Docker Compose

In the project root (`webscraper-api/`), run:

```bash
docker compose up --build
```

This will build the application image (including Playwright dependency installation) and start the application and MongoDB containers.

The API will be accessible at `http://localhost:8000`.
The Dashboard will be at `http://localhost:8000/dashboard`.
The interactive documentation (Swagger UI) will be at `http://localhost:8000/docs`.

### 3. Accessing Endpoints

*   **Dashboard:** `GET http://localhost:8000/dashboard`
*   **List all data (API):** `GET http://localhost:8000/api/data`
*   **Fetch by ID (replace `{item_id}`):** `GET http://localhost:8000/api/data/{item_id}`
*   **Trigger manual scraping:** `POST http://localhost:8000/api/scrape`
*   **Export to JSON:** `GET http://localhost:8000/api/export/json`
*   **Export to CSV:** `GET http://localhost:8000/api/export/csv`

### 4. Stopping the Application

To stop the containers:

```bash
docker compose down
```

To stop and remove volumes (including MongoDB data):

```bash
docker compose down -v
```

## 🔧 Local Development (Without Docker, requires Python and MongoDB)

1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Install Playwright dependencies:**
    ```bash
    playwright install --with-deps chromium
    ```
3.  **Set up MongoDB:** Ensure a MongoDB instance is running and accessible.
4.  **Environment Variables:** Create a `.env` file in the project root (`webscraper-api/`) with your settings (especially `MONGO_URI` pointing to your local instance, e.g., `mongodb://localhost:27017/`).
5.  **Run the application:**
    ```bash
    python app/main.py
    ```
    Or using Uvicorn directly for auto-reloading:
    ```bash
    uvicorn app.main:app --reload
    ```

---

<a name="portugues"></a>
## 🇧🇷 Português

# WebScraper API 🕷️📊
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

API RESTful para scraping periódico com Playwright + FastAPI + MongoDB

Uma API RESTful moderna construída com FastAPI, capaz de coletar dados web com Playwright (JavaScript headless rendering), armazenar em MongoDB e exibir via dashboard ou endpoints exportáveis (JSON/CSV). Ideal para scraping automatizado de portais públicos e geração de relatórios periódicos.

## ⚙️ Tecnologias

*   Python 3.10+
*   FastAPI
*   MongoDB
*   APScheduler
*   Playwright (para scraping, substituindo a necessidade de Selenium)
*   BeautifulSoup4 (para parsing HTML pós-Playwright)
*   Pandas
*   Jinja2 (para o Dashboard)
*   Docker & Docker Compose
*   Uvicorn & Gunicorn

## 📌 Funcionalidades

*   **Scraping Web:**
    *   Coleta dados do [Indicador da Soja CEPEA/ESALQ](https://www.cepea.esalq.usp.br/br/indicador/soja.aspx) (configurável via `TARGET_URL`) usando Playwright para renderizar JavaScript.
    *   Roda periodicamente (configurável via `SCRAPE_INTERVAL_HOURS`).
*   **API REST (FastAPI) e UI:**
    *   `GET /`: Página inicial.
    *   `GET /dashboard`: Dashboard HTML simples (UI frontend embutido) para visualização dos dados.
    *   `GET /api/data`: Retorna todos os dados coletados.
    *   `GET /api/data/{id}`: Retorna um item específico pelo ID.
    *   `POST /api/scrape`: Dispara um processo de scraping manualmente (roda em background).
    *   `GET /api/export/json`: Baixa todos os dados em formato JSON.
    *   `GET /api/export/csv`: Baixa todos os dados em formato CSV.
    *   Documentação interativa da API (Swagger UI) disponível em `/docs`.
*   **Banco de Dados:**
    *   MongoDB para armazenamento dos dados.
    *   Schema: `{ "_id": ObjectId (string na API), "fonte": "string", "dados": {"tabela_completa": List[List[str]] }, "data_coleta": "datetime" }` (O campo `dados` agora contém a tabela completa extraída).
*   **Agendamento:**
    *   Job de scraping roda no intervalo definido (padrão: 12 horas).
*   **Docker:**
    *   Contêiner para a aplicação FastAPI e o scheduler (inclui instalação do Playwright).
    *   Contêiner para o MongoDB.
    *   Volume persistente para os dados do MongoDB.

## 📁 Estrutura de Pastas

```
webscraper-api/
├── app/
│   ├── api.py          # Rotas da API REST (/api/*)
│   ├── db.py           # Conexão com MongoDB e schemas Pydantic
│   ├── export.py       # Funcionalidades de exportação (CSV/JSON)
│   ├── main.py         # Aplicação FastAPI, rotas UI, ciclo de vida
│   ├── scheduler.py    # Agendador de scraping (APScheduler)
│   ├── scraper.py      # Lógica de scraping (Playwright + BeautifulSoup)
│   └── templates/
│       └── dashboard.html  # Dashboard HTML via Jinja2
├── Dockerfile          # Define a imagem Docker para a aplicação
├── docker-compose.yml  # Orquestra containers (API + MongoDB)
├── requirements.txt    # Dependências Python
└── .env.example        # Configurações de ambiente (exemplo)
```

## 🚀 Rodando o Projeto

### Pré-requisitos

*   Docker
*   Docker Compose

### 1. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` na raiz do projeto (`webscraper-api/`) e ajuste as variáveis conforme necessário:

```bash
cp .env.example .env
```

Conteúdo do `.env` (exemplo):

```env
SCRAPE_INTERVAL_HOURS=12
TARGET_URL=https://www.cepea.esalq.usp.br/br/indicador/soja.aspx
MONGO_URI=mongodb://mongodb:27017/
MONGO_DB_NAME=scraper_db
PORT=8000
```

**Nota:** O `docker-compose.yml` já define valores padrão para essas variáveis. O arquivo `.env` local permite que você os sobrescreva facilmente.

### 2. Build e Run com Docker Compose

Na raiz do projeto (`webscraper-api/`), execute:

```bash
docker compose up --build
```

Isso irá construir a imagem da aplicação (incluindo a instalação das dependências do Playwright), iniciar os contêineres da aplicação e do MongoDB.

A API estará acessível em `http://localhost:8000`.
O Dashboard estará em `http://localhost:8000/dashboard`.
A documentação interativa (Swagger UI) estará em `http://localhost:8000/docs`.

### 3. Acessando os Endpoints

*   **Dashboard:** `GET http://localhost:8000/dashboard`
*   **Listar todos os dados (API):** `GET http://localhost:8000/api/data`
*   **Buscar por ID (substitua `{item_id}`):** `GET http://localhost:8000/api/data/{item_id}`
*   **Disparar scraping manual:** `POST http://localhost:8000/api/scrape`
*   **Exportar para JSON:** `GET http://localhost:8000/api/export/json`
*   **Exportar para CSV:** `GET http://localhost:8000/api/export/csv`

### 4. Parando a Aplicação

Para parar os contêineres:

```bash
docker compose down
```

Para parar e remover os volumes (incluindo dados do MongoDB):

```bash
docker compose down -v
```

## 🔧 Desenvolvimento Local (Sem Docker, requer Python e MongoDB)

1.  **Instale as dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Instale as dependências do Playwright:**
    ```bash
    playwright install --with-deps chromium
    ```
3.  **Configure o MongoDB:** Certifique-se de que uma instância do MongoDB esteja rodando e acessível.
4.  **Variáveis de Ambiente:** Crie um arquivo `.env` na raiz do projeto (`webscraper-api/`) com as configurações (principalmente `MONGO_URI` apontando para sua instância local, e.g., `mongodb://localhost:27017/`).
5.  **Rode a aplicação:**
    ```bash
    python app/main.py
    ```
    Ou usando Uvicorn diretamente para recarregamento automático:
    ```bash
    uvicorn app.main:app --reload
    ``` 