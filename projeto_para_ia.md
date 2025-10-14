# 📋 Análise de Projeto

**Projeto:** `brdk-v1`  
**Caminho:** `C:\Users\user\Documents\BRDK MONITORAMENTO\brdk-v1`

---

## 📊 Estatísticas da Análise

- **Arquivos processados:** 78
- **Arquivos ignorados/pulados:** 12
- **Erros encontrados:** 0
- **Avisos gerados:** 0
- **Data/Hora:** 14/10/2025 18:37:48
- **Tempo de execução:** 0.90s

---

## 📁 Estrutura de Pastas

```
│   └── composer.json
│   └── custom.ini
│   └── docker-compose.yml
│   └── Dockerfile
│   └── nginx.conf
│   └── package.json
│   └── postcss.config.js
│   └── README.md
│   └── tailwind.config.js
├── db/
│   └── SCRIPT_SQL_BRDK.sql
│   └── SCRIPT_SQL_LOOKUP_DATA.sql
│   ├── migrations/
├── docs/
│   └── equipamentos_torres.csv
│   └── torres.csv
├── public/
│   └── .htaccess
│   └── index.php
│   └── openapi.json
│   ├── assets/
│   │   ├── css/
│   │   │   └── tailwind.css
│   │   ├── img/
│   │   ├── js/
│   │   │   └── api.js
│   │   │   └── app.js
│   │   │   └── configuracoes.js
│   │   │   └── dashboard.js
│   │   │   └── mapa.js
│   │   │   └── torres.js
│   │   │   ├── components/
│   │   │   │   └── emptyStateManager.js
│   │   │   │   └── import-modal.js
├── routes/
│   └── api.php
│   └── web.php
├── scripts/
│   └── seed.php
│   └── test_improvements.php
├── src/
│   ├── Controllers/
│   │   ├── Api/
│   │   │   └── AuthController.php
│   │   │   └── DashboardController.php
│   │   │   └── DispositivoController.php
│   │   │   └── EventoController.php
│   │   │   └── ImportController.php
│   │   │   └── LookupController.php
│   │   │   └── MapaController.php
│   │   │   └── TorreController.php
│   │   │   └── UserController.php
│   │   ├── Web/
│   │   │   └── AuthController.php
│   │   │   └── ConfiguracoesController.php
│   │   │   └── DashboardController.php
│   │   │   └── HomeController.php
│   │   │   └── MapaController.php
│   │   │   └── TorresController.php
│   ├── Core/
│   │   └── Core.php
│   │   └── Validator.php
│   │   └── View.php
│   ├── DTO/
│   │   └── DispositivoDTO.php
│   │   └── EventoDTO.php
│   │   └── TorreDTO.php
│   ├── Http/
│   │   └── ApiResponse.php
│   │   └── Request.php
│   │   └── Response.php
│   │   └── Route.php
│   ├── Middleware/
│   │   └── AuthMiddleware.php
│   ├── Models/
│   │   └── Database.php
│   │   └── MotivoFalha.php
│   │   └── StatusTipo.php
│   │   └── TipoDispositivo.php
│   │   └── TipoEvento.php
│   │   └── Usuario.php
│   ├── Repository/
│   │   └── DispositivoRepository.php
│   │   └── EventoRepository.php
│   │   └── TorreRepository.php
│   ├── Services/
│   │   └── AuthService.php
│   │   └── DashboardService.php
│   │   └── DispositivoService.php
│   │   └── EventoService.php
│   │   └── ImportService.php
│   │   └── MapaService.php
│   │   └── TempoService.php
│   │   └── TorreService.php
│   │   └── UserService.php
├── views/
│   ├── auth/
│   │   └── alterar-senha.php
│   │   └── login.php
│   │   └── register.php
│   ├── configuracoes/
│   │   └── index.php
│   ├── dashboard/
│   │   └── index.php
│   ├── layouts/
│   │   └── app.php
│   ├── mapa/
│   │   └── index.php
│   ├── partials/
│   │   └── empty-state.php
│   │   └── _import_modal.php
│   ├── torres/
│   │   └── index.php
```

---

## 💻 Conteúdo dos Arquivos de Código

### `composer.json`

```json
{
    "name": "brdk/monitoramento-api",
    "description": "API para o sistema de monitoramento BRDK.",
    "type": "project",
    "require": {
        "lcobucci/jwt": "^5.0",
        "vlucas/phpdotenv": "^5.5"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

### `custom.ini`

```ini
; Configurações personalizadas do PHP
upload_max_filesize = 20M
post_max_size = 20M
memory_limit = 256M
display_errors = On
error_reporting = E_ALL

[opcache]
opcache.enable=1
opcache.enable_cli=1
opcache.save_comments=1
```

### `docker-compose.yml`

```yml
# Define os serviços (contêineres) que compõem nossa aplicação.
services:
  # Serviço do Banco de Dados PostgreSQL
  db:
    image: postgres:15-alpine  # Usa a imagem oficial e leve do PostgreSQL 15.
    container_name: brdk_db     # Nomeia o contêiner para fácil identificação.
    restart: always             # Reinicia o contêiner automaticamente se ele parar.
    environment:
      # As credenciais são lidas do arquivo .env na raiz do projeto.
      POSTGRES_DB: ${DB_DATABASE}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      # 'pgdata' é um volume nomeado para persistir os dados do banco.
      - pgdata:/var/lib/postgresql/data
      - ./db:/docker-entrypoint-initdb.d
    ports:
      # Mapeia a porta 5432 do seu computador para a porta 5432 do contêiner.
      - "5433:5432"

  # Serviço da Aplicação PHP
  app:
    build: .  # Constrói a imagem a partir do Dockerfile na pasta atual.
    container_name: brdk_app
    restart: always
    env_file: ./.env
    volumes:
      # Mapeia o código-fonte local para dentro do contêiner.
      # Alterações nos arquivos locais são refletidas instantaneamente.
      - .:/var/www/html
    depends_on:
      - db  # Garante que o serviço 'db' inicie antes do serviço 'app'.

  # Serviço do Servidor Web Nginx
  nginx:
    image: nginx:stable-alpine
    container_name: brdk_nginx
    restart: always
    ports:
      # Mapeia a porta 8000 do seu computador para a porta 80 do contêiner.
      # Você acessará a aplicação em http://localhost:8000
      - "8000:80"
    volumes:
      # Mapeia o código-fonte para que o Nginx possa servir os arquivos estáticos.
      - .:/var/www/html
      # Mapeia nosso arquivo de configuração do Nginx.
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app

# Define os volumes nomeados para persistência de dados.
volumes:
  pgdata:
```

### `Dockerfile`

```
# Usa a imagem oficial do PHP 8.2 com FPM
FROM php:8.2-fpm

# Define o diretório de trabalho padrão
WORKDIR /var/www/html

# Instala dependências do sistema, extensões PHP, GIT, ZIP, E AGORA NODE.JS/NPM
RUN apt-get update && apt-get install -y \
    libpq-dev \
    git \
    zip \
    unzip \
    libzip-dev \
    curl \
    # As duas linhas abaixo instalam o Node.js (versão 20) e o NPM
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    # Continua com a instalação das suas extensões PHP
    && docker-php-ext-install pdo pdo_pgsql zip

# Copia o executável do Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copia apenas os arquivos de definição de dependências
COPY composer.json composer.lock ./

# Adiciona o diretório atual como seguro para o Git
RUN git config --global --add safe.directory /var/www/html

# Instala as dependências do PHP
RUN composer install --no-interaction --no-plugins --no-scripts --prefer-dist

# Copia o restante dos arquivos da aplicação
COPY . .

# Copia a sua configuração personalizada do PHP por último
COPY custom.ini /usr/local/etc/php/conf.d/custom.ini
```

### `nginx.conf`

```conf
server {
    # O Nginx vai escutar na porta 80 dentro da rede Docker.
    listen 80;
    server_name localhost;

    # O diretório raiz, onde estão os arquivos públicos da aplicação.
    root /var/www/html/public;
    index index.php index.html;

    # Configuração para logs de erro e acesso.
    error_log /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;

    # Trata as requisições para arquivos estáticos (CSS, JS, imagens).
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # Passa as requisições de arquivos .php para o serviço PHP-FPM.
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        # O 'app:9000' é a chave: 'app' é o nome do nosso serviço PHP no docker-compose.
        fastcgi_pass app:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
}
```

### `package.json`

```json
{
  "devDependencies": {
    "autoprefixer": "^10.4.21",
    "postcss": "^8.5.6",
    "tailwindcss": "^3.4.18"
  },
    "scripts": {
    "dev": "tailwindcss -i ./public/assets/css/tailwind.css -o ./public/dist/output.css --watch"
  }
}
```

### `postcss.config.js`

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### `README.md`

```md
# BRDK Monitoramento - API

## 1. Visão Geral
A **BRDK Monitoramento - API** é o backend responsável por gerenciar e fornecer dados para um sistema de **monitoramento de infraestrutura de rede**.

Desenvolvida em **PHP 8+**, foi projetada para oferecer **performance**, **segurança** e **escalabilidade**, seguindo as melhores práticas RESTful.

O sistema possibilita o cadastro e monitoramento de **torres de transmissão** e seus **dispositivos**, registrando **eventos**, **falhas** e **históricos de status** para análises e dashboards em tempo real.

---

## 2. Funcionalidades Principais
- **Autenticação Segura**: Login e registro com **JWT (JSON Web Tokens)** para proteger os endpoints.
- **Gestão de Infraestrutura (CRUD)**: Criação, leitura, atualização e exclusão de **torres** e **dispositivos**.
- **Registro de Eventos**: Registro e consulta de eventos associados a cada dispositivo.
- **Ambiente Padronizado com Docker**: Configuração de ambiente de desenvolvimento com um único comando.
- **Estrutura Modular**: Código organizado em *Services*, *Models* e *Controllers* para fácil manutenção e expansão.
- **Validação Avançada**: Classe central de validação para garantir a integridade dos dados de entrada.

---

## 3. Tecnologias Utilizadas
- **Linguagem:** PHP 8.2+
- **Banco de Dados:** PostgreSQL 15+
- **Servidor Web:** Nginx
- **Gerenciador de Dependências:** Composer

### Ambiente de Desenvolvimento
- **Docker** e **Docker Compose**

### Principais Bibliotecas
- [`lcobucci/jwt`](https://github.com/lcobucci/jwt): Geração e validação de tokens JWT.
- [`vlucas/phpdotenv`](https://github.com/vlucas/phpdotenv): Gerenciamento de variáveis de ambiente.

---

## 4. Estrutura do Projeto
```text
brdk-monitoramento/
├── db/                     # Scripts de Banco de Dados
│   ├── SCRIPT_SQL_BRDK.sql
│   └── SCRIPT_SQL_LOOKUP_DATA.sql
├── public/                 # Raiz pública do servidor (DocumentRoot)
│   └── index.php           # Ponto de entrada único (Front Controller)
├── src/                    # Código-fonte da aplicação (PHP)
│   ├── Controllers/
│   ├── Core/
│   ├── Http/
│   ├── Middleware/
│   ├── Models/
│   └── Services/
├── vendor/                 # Dependências do Composer
├── .env                    # Variáveis de ambiente (local)
├── .env.example            # Arquivo de exemplo para as variáveis
├── composer.json           # Definições do Composer
├── custom.ini              # Configurações personalizadas do PHP
├── docker-compose.yml      # Orquestrador dos contêineres Docker
├── Dockerfile              # Receita para construir a imagem da aplicação
└── nginx.conf              # Arquivo de configuração do Nginx
```

---

## 5. Ambiente de Desenvolvimento (Docker)

Este é o **método recomendado** para configurar e executar o projeto. Ele garante que toda a equipe utilize um ambiente idêntico e elimina a necessidade de instalar PHP, PostgreSQL ou Composer localmente.

### Pré-requisitos
- **Git** (para clonar o projeto)
- **Docker Desktop** (que já inclui o Docker Compose)
  - [Baixar Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Passo a Passo para Configuração

**1. Clone o Repositório:**
```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd brdk-monitoramento
```

**2. Crie o Arquivo de Variáveis de Ambiente:**
Copie o arquivo de exemplo para criar sua configuração local.
```bash
cp .env.example .env
```
*(Se o arquivo `.env.example` não existir, crie um arquivo chamado `.env` manualmente e cole o conteúdo abaixo nele):*
```dotenv
# BANCO DE DADOS
DB_CONNECTION=pgsql
DB_HOST=db
DB_PORT=5432
DB_DATABASE=brdk_monitoramento
DB_USERNAME=postgres
DB_PASSWORD=root

# JSON WEB TOKEN (JWT)
JWT_SECRET_KEY="28IdxWUjKE2qqM6LV9FO2cIUy5xLpoSFnmQoPvaFuD8="
JWT_ISSUER="brdk-api"
JWT_AUDIENCE="brdk-app"
```
> **Nota:** O `DB_HOST` deve ser `db`, que é o nome do serviço do banco de dados no `docker-compose.yml`.

**3. Inicie os Contêineres:**
Este comando irá construir as imagens necessárias e iniciar todos os serviços (PHP, Nginx, PostgreSQL) em segundo plano.
```bash
docker-compose up -d
```
*Na primeira vez, este processo pode demorar alguns minutos. Nas próximas, será quase instantâneo.*

Ao iniciar pela primeira vez, o Docker irá **automaticamente criar o banco de dados** e **executar todos os scripts `.sql`** da pasta `db/`.

**4. Crie o Usuário Administrador (Seed):**
Para finalizar, execute o script que cria o usuário padrão do sistema.
```bash
docker-compose exec app php scripts/seed.php
```

**Pronto! O ambiente está 100% configurado.**

---

## 6. Acessando e Gerenciando o Ambiente

### Acesso à Aplicação
- **URL da Aplicação:** **[http://localhost:8000](http://localhost:8000)**
- **Email do Admin:** `admin@brdk.com.br`
- **Senha do Admin:** `admin123`

### Comandos Úteis do Docker
- **Parar todos os contêineres:**
  ```bash
  docker-compose down
  ```

- **Ver os logs de um serviço em tempo real (ótimo para depurar):**
  ```bash
  # Ver logs do PHP
  docker-compose logs -f app

  # Ver logs do Banco de Dados
  docker-compose logs -f db
  ```
  *(Pressione `Ctrl + C` para sair dos logs)*

- **Executar um comando dentro de um contêiner (ex: Composer):**
  ```bash
  docker-compose exec app composer update
  ```

- **Recriar os contêineres (se você alterar o `Dockerfile` ou `docker-compose.yml`):**
  ```bash
  docker-compose up -d --build --force-recreate
  ```

---

## 7. Documentação da API (Endpoints)

> **Obs:** Todos os endpoints, exceto `/login` e `/register`, exigem o cabeçalho de autorização:
> ```http
> Authorization: Bearer <seu_token_jwt>
> ```

### 7.1 Autenticação
- **POST /api/v1/login**
  Autentica um usuário e retorna um token JWT.
  **Body:** `{"email": "user@example.com", "senha": "password123"}`

- **POST /api/v1/register**
  Registra um novo usuário.
  **Body:** `{"nome": "Novo Usuario", "email": "novo@example.com", "senha": "password123"}`

### 7.2 Torres
- **GET /api/v1/torres** – Lista todas as torres.
- **GET /api/v1/torres/{id}** – Busca uma torre específica.
- **POST /api/v1/torres** – Cria uma nova torre.
  **Body:** `{"nome": "Torre Sul", "localizacao": "Zona Sul"}`
- **PUT /api/v1/torres/{id}** – Atualiza dados de uma torre.
  **Body:** `{"nome": "Torre Sul Atualizada", "localizacao": "Nova Localização"}`

### 7.3 Dispositivos
- **GET /api/v1/dispositivos** – Lista todos os dispositivos.
- **GET /api/v1/dispositivos/{id}** – Busca um dispositivo específico.
- **POST /api/v1/dispositivos** – Cria um novo dispositivo.
  **Body:** `{"torre_id": 1, "tipo_dispositivo_id": 2, "identificador": "SWA-01-SUL", "ip": "192.168.1.10"}`
- **PUT /api/v1/dispositivos/{id}** – Atualiza dados de um dispositivo.
  **Body:** `{"identificador": "SWA-01-SUL-ALT", "ip": "192.168.1.11"}`

### 7.4 Eventos
- **GET /api/v1/dispositivos/{id}/eventos** – Lista eventos de um dispositivo.
- **POST /api/v1/dispositivos/{id}/eventos** – Registra um novo evento.
  **Body:** `{"tipo_evento_id": 1, "status_evento_id": 2, "mensagem_original": "Device rebooted unexpectedly"}`

### 7.5 Rotas de Apoio (Lookup)
- **GET /api/v1/tipos-dispositivo** – Lista tipos de dispositivo.
- **GET /api/v1/status-tipos** – Lista tipos de status.
- **GET /api/v1/tipos-evento** – Lista tipos de evento.
- **GET /api/v1/motivos-falha** – Lista motivos de falha.

---

## 8. Licença
Este projeto é disponibilizado sob a licença **MIT**.
```

### `tailwind.config.js`

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', 
  content: [
    "./views/**/*.php",
    "./public/assets/js/**/*.js"  
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### `db\SCRIPT_SQL_BRDK.sql`

```sql
-- ===================================================================
-- SCRIPT COMPLETO DE CRIAÇÃO DO BANCO DE DADOS DO BRDK (VERSÃO CORRIGIDA)
-- ===================================================================

-- 1. TIPOS CUSTOMIZADOS
CREATE TYPE criticidade_enum AS ENUM ('baixa', 'media', 'alta', 'critica');

-- 2. TABELAS DE CONFIGURAÇÃO (LOOKUP TABLES)

CREATE TABLE status_tipos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    is_erro BOOLEAN DEFAULT FALSE,
    criticidade criticidade_enum,
    cor_hex VARCHAR(7) DEFAULT '#000000',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tipos_evento (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(30) UNIQUE NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    categoria VARCHAR(50),
    automatico BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tipos_dispositivo (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(30) UNIQUE NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE motivos_falha (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(30) UNIQUE NOT NULL,
    descricao TEXT NOT NULL,
    categoria VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. TABELAS PRINCIPAIS E RELACIONAMENTOS

CREATE TABLE torres (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    localizacao VARCHAR(200),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    status_geral INTEGER REFERENCES status_tipos(id),
    uptime_percentage DECIMAL(5,2) DEFAULT 100.00,
    last_check TIMESTAMPTZ DEFAULT NOW(),
    observacoes TEXT,
    depende_de_torre_id BIGINT REFERENCES torres(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE dispositivos (
    id BIGSERIAL PRIMARY KEY,
    torre_id BIGINT NOT NULL REFERENCES torres(id) ON DELETE CASCADE,
    tipo_dispositivo_id INTEGER REFERENCES tipos_dispositivo(id),
    nome VARCHAR(100) NOT NULL,
    ip INET NOT NULL UNIQUE,
    mac_address MACADDR,
    observacoes TEXT,
    status VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    localizacao VARCHAR(100)
);

CREATE TABLE subtipos_dispositivos (
    id SERIAL PRIMARY KEY,
    tipo_dispositivo_id INTEGER NOT NULL REFERENCES tipos_dispositivo(id) ON DELETE CASCADE,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50),
    fabricante VARCHAR(100),
    modelo VARCHAR(100),
    capacidade_portas INTEGER,
    gerenciavel BOOLEAN DEFAULT TRUE,
    porta_padrao_gerencia INTEGER DEFAULT 80,
    ativo BOOLEAN DEFAULT TRUE,
    localizacao VARCHAR(100)
);

CREATE TABLE monitoramento (
    dispositivo_id BIGINT PRIMARY KEY REFERENCES dispositivos(id) ON DELETE CASCADE,
    status_atual INTEGER NOT NULL REFERENCES status_tipos(id),
    ultima_atualizacao TIMESTAMPTZ DEFAULT NOW(),
    uptime_percentage DECIMAL(5,2) DEFAULT 100.00,
    tempo_offline_minutos INTEGER DEFAULT 0,
    intervalo_ping INTEGER DEFAULT 60,
    timeout_ping INTEGER DEFAULT 5,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CHECK(uptime_percentage >= 0 AND uptime_percentage <= 100)
);

CREATE TABLE janelas_manutencao (
    id BIGSERIAL PRIMARY KEY,
    torre_id BIGINT REFERENCES torres(id) ON DELETE CASCADE,
    dispositivo_id BIGINT REFERENCES dispositivos(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    data_inicio TIMESTAMPTZ NOT NULL,
    data_fim TIMESTAMPTZ NOT NULL,
    agendado_por VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CHECK(num_nonnulls(torre_id, dispositivo_id) = 1),
    CHECK(data_fim > data_inicio)
);

CREATE TABLE eventos (
    id BIGSERIAL PRIMARY KEY,
    dispositivo_id BIGINT NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    tipo_evento_id INTEGER NOT NULL REFERENCES tipos_evento(id),
    status_evento_id INTEGER NOT NULL REFERENCES status_tipos(id),
    motivo_falha_id INTEGER REFERENCES motivos_falha(id),
    horario TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    response_time_ms INTEGER,
    packet_loss_percent DECIMAL(5,2),
    status_http INTEGER,
    bytes_transferidos BIGINT,
    jitter_ms DECIMAL(6,2),
    latency_ms DECIMAL(8,2),
    mensagem_original TEXT,
    duracao_estado INTEGER,
    origem VARCHAR(50) DEFAULT 'sistema',
    raw_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE dispositivo_historicos (
    id BIGSERIAL PRIMARY KEY,
    dispositivo_id BIGINT NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    status_historico_id INTEGER NOT NULL REFERENCES status_tipos(id),
    data_inicio TIMESTAMPTZ NOT NULL,
    data_fim TIMESTAMPTZ,
    duracao_minutos INTEGER,
    CHECK(data_fim IS NULL OR data_fim >= data_inicio)
);

CREATE TABLE usuarios (
    id BIGSERIAL PRIMARY KEY,
    primeiro_nome VARCHAR(100) NOT NULL,
    ultimo_nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    celular VARCHAR(20) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. ÍNDICES OTIMIZADOS

CREATE INDEX idx_status_tipos_criticidade ON status_tipos(criticidade) WHERE is_erro = TRUE;

CREATE INDEX idx_torres_status ON torres(status_geral);
CREATE INDEX idx_torres_location ON torres(latitude, longitude) WHERE latitude IS NOT NULL;

CREATE INDEX idx_dispositivos_torre_status ON dispositivos(torre_id, status);

CREATE INDEX idx_janelas_manutencao_periodo ON janelas_manutencao(data_inicio, data_fim);

CREATE INDEX idx_eventos_dispositivo_horario ON eventos(dispositivo_id, horario DESC);
CREATE INDEX idx_eventos_horario ON eventos(horario DESC);

CREATE INDEX idx_historico_dispositivo_periodo ON dispositivo_historicos(dispositivo_id, data_inicio DESC);

CREATE INDEX idx_usuarios_email ON usuarios(email);

-- FIM DO SCRIPT
```

### `db\SCRIPT_SQL_LOOKUP_DATA.sql`

```sql
-- SCRIPT DE INSERÇÃO DE DADOS INICIAIS (LOOKUP TABLES)

INSERT INTO status_tipos (codigo, descricao, is_erro, criticidade, cor_hex) VALUES
('ONLINE', 'Online', false, 'baixa', '#10b981'),
('OFFLINE', 'Offline', true, 'alta', '#ef4444'),
('MANUTENCAO', 'Manutenção', false, 'media', '#f59e0b'),
('WARNING', 'Atenção', true, 'media', '#f97316');

-- DADOS PARA A TABELA tipos_dispositivo
INSERT INTO tipos_dispositivo (codigo, descricao, categoria) VALUES
('DEFAULT', 'Tipo padrão', 'geral'),
('EQUIPAMENTO', 'Equipamento', 'auto');
```

### `public\index.php`

```php
<?php
require_once __DIR__ . '/../vendor/autoload.php';

define('APP_VERSION', '1.0.0');

// Carrega variáveis de ambiente
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/..');
$dotenv->load();

// Inicializar array de rotas
$routes = [];

// Carrega definições de rotas
require_once __DIR__ . '/../routes/web.php';
require_once __DIR__ . '/../routes/api.php';

// Processar requisição
App\Core\Core::dispatch($routes);
?>
```

### `public\openapi.json`

```json
{
    "openapi": "3.0.0"
}
```

### `public\assets\css\tailwind.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### `public\assets\js\api.js`

```js
/**
 * Módulo central para todas as requisições à API.
 * Inclui tratamento global de erros de autenticação (401).
 */

/**
 * @param {string} endpoint - O endpoint da API a ser chamado.
 * @param {object} options - Opções da requisição fetch (method, body, etc.).
 * @param {boolean} [isFile=false] - Se verdadeiro, trata a resposta como um ficheiro.
 */
async function apiFetch(endpoint, options = {}, isFile = false) {
    const token = localStorage.getItem('jwt_token');
    const defaultHeaders = {};

    if (!isFile) {
        defaultHeaders['Accept'] = 'application/json';
        if (!(options.body instanceof FormData)) {
            defaultHeaders['Content-Type'] = 'application/json';
        }
    }

    if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const finalOptions = { ...options, headers: { ...defaultHeaders, ...options.headers } };

    try {
        const response = await fetch(endpoint, finalOptions);

        // Se o token for inválido ou expirado, o servidor retorna 401.
        if (response.status === 401) {
            // Chama a função de logout global do app.js
            logoutUser();
            // Lança um erro para interromper a execução do código que fez a chamada.
            throw new Error("Sessão expirada. Por favor, faça login novamente.");
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({})); // Tenta ler o erro como JSON
            const errorMessage = errorData.error?.message || `Erro HTTP ${response.status}`;
            const error = new Error(errorMessage);
            error.responseJSON = errorData;
            throw error;
        }

        // Se for um ficheiro, trata de forma diferente
        if (isFile) {
            const contentDisposition = response.headers.get('content-disposition');
            let filename = 'template.csv';
            if (contentDisposition?.includes('attachment')) {
                const filenameMatch = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
                if (filenameMatch?.[1]) {
                    filename = filenameMatch[1].replace(/['"]/g, '');
                }
            }
            const blob = await response.blob();
            return { blob, filename };
        }

        // Se for JSON
        return await response.json();

    } catch (error) {
        // Não redireciona aqui, apenas propaga o erro para a função que chamou.
        // O redirecionamento já foi tratado se o erro for 401.
        console.error(`API Error on ${endpoint}:`, error.message);
        throw error;
    }
}

const api = {
    //DASHBOARD
    fetchKpis: () => apiFetch('/api/v1/dashboard/kpis'),
    fetchCurrentUser: () => apiFetch('/api/v1/user/me'),
    fetchDispositivosStatus: () => apiFetch('/api/v1/dashboard/dispositivos-status'),
    fetchDispositivosTipos: () => apiFetch('/api/v1/dashboard/dispositivos-tipos'),
    fetchTorresCriticas: () => apiFetch('/api/v1/dashboard/torres-criticas'),
    fetchVisaoGeralTorres: () => apiFetch('/api/v1/dashboard/visao-geral-torres'),


    //IMPORTAÇÃO CSV
    importCSV: (type, formData) => {
        const endpoint = type === 'torres' ? '/api/v1/import/torres' : '/api/v1/import/equipamentos';
        return apiFetch(endpoint, { method: 'POST', body: formData });
    },
    downloadTemplate: async (type) => {
        const endpoint = `/api/v1/import/${type}/template`;
        const { blob, filename } = await apiFetch(endpoint, {}, true); // O terceiro parâmetro 'true' indica que é um ficheiro

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    },


    //MAPA
    fetchTorresParaMapa: () => apiFetch('/api/v1/mapa/torres'),
    fetchTorreDetails: (id) => apiFetch(`/api/v1/mapa/torre/${id}`),
    fetchRegioesParaMapa: () => apiFetch('/api/v1/mapa/regioes'),
    fetchTempoTorre: (id) => apiFetch(`/api/v1/torres/${id}/tempo`),


    //CONFIGURAÇÕES
    updateUser: (data) => apiFetch('/api/v1/user/me', { method: 'PUT', body: JSON.stringify(data) }),
    updatePassword: (data) => apiFetch('/api/v1/user/me/senha', { method: 'PUT', body: JSON.stringify(data) }),


    // TORRES (CRUD)
    fetchTorres: () => apiFetch('/api/v1/torres?per_page=1000'),
    createTorre: (data) => apiFetch('/api/v1/torres', { method: 'POST', body: JSON.stringify(data) }),
    updateTorre: (id, data) => apiFetch(`/api/v1/torres/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteTorre: (id) => apiFetch(`/api/v1/torres/${id}`, { method: 'DELETE' }),
    fetchDispositivosDaTorre: (id) => apiFetch(`/api/v1/torres/${id}/dispositivos`),


    // DISPOSITIVOS (CRUD)
    fetchTiposDispositivo: () => apiFetch('/api/v1/lookup/tipos-dispositivo'),
    createDispositivo: (data) => apiFetch('/api/v1/dispositivos', { method: 'POST', body: JSON.stringify(data) }),
    updateDispositivo: (id, data) => apiFetch(`/api/v1/dispositivos/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteDispositivo: (id) => apiFetch(`/api/v1/dispositivos/${id}`, { method: 'DELETE' }),

};
```

### `public\assets\js\app.js`

```js
/**
 * Lógica global da aplicação, executada em todas as páginas.
 */

/**
 * Função central para encerrar a sessão do usuário.
 */
function logoutUser() {
    console.log("Sessão encerrada. Limpando token...");
    localStorage.removeItem('jwt_token');
    setTimeout(() => {
        window.location.href = '/login';
    }, 100);
}

/**
 * Carrega e exibe as informações do usuário no cabeçalho.
 */
async function loadAndDisplayUser() {
    try {
        const response = await api.fetchCurrentUser();
        if (response && response.success) {
            const user = response.data;
            const avatarEl = document.getElementById('user-avatar');
            const nameEl = document.getElementById('user-name');

            if (avatarEl && nameEl) {
                const nomeCompleto = user.nome || '';
                const partesDoNome = nomeCompleto.split(' ');
                const primeiroNome = partesDoNome[0] || '';
                const ultimoNome = partesDoNome.length > 1 ? partesDoNome[partesDoNome.length - 1] : '';
                const iniciais = (primeiroNome.charAt(0) + ultimoNome.charAt(0)).toUpperCase();

                avatarEl.textContent = iniciais;
                nameEl.textContent = nomeCompleto;

                avatarEl.classList.remove('bg-gray-200', 'dark:bg-gray-700');
                avatarEl.classList.add('bg-blue-100', 'text-blue-700', 'dark:bg-blue-900/50', 'dark:text-blue-400');
            }
        }
    } catch (error) {
        // O api.js já trata o logout em caso de 401.
        console.error("Não foi possível carregar os dados do usuário.", error.message);
        const nameEl = document.getElementById('user-name');
        if (nameEl) nameEl.textContent = "Sessão inválida";
    }
}

/**
 * Configura o modal de confirmação para o botão de logout.
 */
function setupLogoutConfirmation() {
    const logoutButton = document.getElementById('logout-button');
    const modal = document.getElementById('logout-confirmation-modal');
    const confirmBtn = document.getElementById('btn-logout-confirm');
    const cancelBtn = document.getElementById('btn-logout-cancel');

    if (logoutButton && modal && confirmBtn && cancelBtn) {
        // Abre o modal ao clicar em "Sair"
        logoutButton.addEventListener('click', (e) => {
            e.preventDefault(); // Previne qualquer comportamento padrão
            modal.classList.remove('hidden');
        });

        // O botão de confirmação no modal é quem realmente faz o logout
        confirmBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
            logoutUser();
        });

        // O botão de cancelar apenas fecha o modal
        cancelBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
        });
    }
}

/**
 * Função de inicialização principal da aplicação.
 */
function initApp() {
    console.log("🚀 Lógica global (app.js) iniciada.");
    loadAndDisplayUser();
    setupLogoutConfirmation(); // Configura o modal de logout

    const importButton = document.getElementById('open-import-modal');
    if (importButton && typeof showImportModal === 'function') {
        importButton.addEventListener('click', () => showImportModal());
    }
}

// Inicia a aplicação quando o DOM estiver pronto.
document.addEventListener('DOMContentLoaded', initApp);
```

### `public\assets\js\configuracoes.js`

```js
// ===================================================================================
// LÓGICA DA PÁGINA DE CONFIGURAÇÕES (VERSÃO CORRIGIDA E MELHORADA)
// ===================================================================================

document.addEventListener('DOMContentLoaded', () => {
    initPerfilForm();
    initSenhaForm();
});

// ===================================================================================
// FORMULÁRIO DE DADOS PESSOAIS
// ===================================================================================

let originalUserData = {};

function initPerfilForm() {
    // Adiciona os event listeners de forma segura
    document.getElementById('perfil-form').addEventListener('submit', salvarPerfil);
    document.getElementById('btn-editar-perfil').addEventListener('click', () => toggleEditMode(true));
    document.getElementById('btn-cancelar-perfil').addEventListener('click', () => {
        toggleEditMode(false);
        document.getElementById('nome').value = originalUserData.nome || '';
        document.getElementById('email').value = originalUserData.email || '';
    });
    
    loadUserData();
}

async function loadUserData() {
    try {
        const response = await api.fetchCurrentUser();
        if (response.success && response.data) {
            originalUserData = response.data;
            document.getElementById('nome').value = originalUserData.nome || '';
            document.getElementById('email').value = originalUserData.email || '';
        } else {
            throw new Error('Resposta da API inválida ao carregar usuário.');
        }
    } catch (error) {
        showNotification('Erro ao carregar dados do usuário.', 'error');
        console.error(error);
    }
}

function toggleEditMode(enable = true) {
    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    document.getElementById('btn-editar-perfil').classList.toggle('hidden', enable);
    document.getElementById('acoes-edicao-perfil').classList.toggle('hidden', !enable);

    [nomeInput, emailInput].forEach(input => {
        input.disabled = !enable;
        input.classList.toggle('bg-gray-100', !enable);
        input.classList.toggle('cursor-not-allowed', !enable);
    });
}

async function salvarPerfil(event) {
    event.preventDefault();
    const nomeCompleto = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();

    const partesNome = nomeCompleto.split(' ');
    const data = {
        primeiro_nome: partesNome.shift() || '',
        ultimo_nome: partesNome.join(' ') || '',
        email: email,
        celular: originalUserData.celular || '00000000000'
    };

    try {
        const response = await api.updateUser(data);
        if (response.success) {
            showNotification('Perfil atualizado com sucesso!', 'success');
            toggleEditMode(false);
            const userNameEl = document.getElementById('user-name');
            if (userNameEl) userNameEl.textContent = nomeCompleto;
            loadUserData();
        }
    } catch (error) {
        showNotification(error.message || 'Erro ao atualizar perfil.', 'error');
    }
}

// ===================================================================================
// FORMULÁRIO DE ALTERAÇÃO DE SENHA (COM VALIDAÇÃO EM TEMPO REAL)
// ===================================================================================

function initSenhaForm() {
    document.getElementById('senha-form').addEventListener('submit', salvarSenha);
    
    const novaSenhaInput = document.getElementById('nova_senha');
    novaSenhaInput.addEventListener('input', validatePasswordRealtime);
}

function validatePasswordRealtime() {
    const password = document.getElementById('nova_senha').value;

    // Função auxiliar para atualizar cada requisito na UI
    const updateRequirement = (id, isValid) => {
        const el = document.getElementById(id);
        const icon = el.querySelector('i');
        if (isValid) {
            el.classList.remove('text-gray-500');
            el.classList.add('text-green-600');
            icon.className = 'fas fa-check-circle text-green-500';
        } else {
            el.classList.remove('text-green-600');
            el.classList.add('text-gray-500');
            icon.className = 'fas fa-times-circle text-red-400';
        }
    };

    // 1. Mínimo 8 caracteres
    updateRequirement('req-length', password.length >= 8);
    // 2. Pelo menos 1 letra maiúscula
    updateRequirement('req-uppercase', /[A-Z]/.test(password));
    // 3. Pelo menos 1 número
    updateRequirement('req-number', /[0-9]/.test(password));
    // 4. Pelo menos 1 caractere especial
    updateRequirement('req-special', /[\W_]/.test(password)); // \W é "não-palavra", inclui especiais
}

async function salvarSenha(event) {
    event.preventDefault();
    const form = document.getElementById('senha-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Validações no frontend antes de enviar
    if (data.nova_senha !== data.confirmacao_nova_senha) {
        showNotification('A nova senha e a confirmação não coincidem.', 'error');
        return;
    }

    try {
        const response = await api.updatePassword(data);
        if (response.success) {
            showNotification('Senha alterada com sucesso! Por favor, faça login novamente.', 'success');
            form.reset();
            validatePasswordRealtime(); // Reseta a UI de requisitos
            setTimeout(() => {
                logoutUser(); // Força o logout por segurança
            }, 2000);
        }
    } catch (error) {
        showNotification(error.responseJSON?.error?.message || error.message || 'Erro ao alterar a senha.', 'error');
    }
}

// ===================================================================================
// FUNÇÃO AUXILIAR DE NOTIFICAÇÃO (TOAST)
// ===================================================================================

function showNotification(message, type = 'success') {
    const toast = document.getElementById('notification-toast');
    if (!toast) return;
    toast.textContent = message;
    
    toast.className = `fixed top-5 right-5 p-4 rounded-md shadow-lg text-white transition-all duration-300 z-50 ${type === 'success' ? 'bg-green-600' : 'bg-red-600'}`;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 4000);
}
```

### `public\assets\js\dashboard.js`

```js
/**
 * Orquestra o carregamento do dashboard com foco na experiência do utilizador,
 * utilizando o componente global EmptyStateManager para estados de boas-vindas.
 */
async function initializeDashboard() {
    try {
        // ✅ ALTERAÇÃO DE PERFORMANCE: Executa as verificações essenciais em paralelo.
        const [torresResponse, equipamentosResponse] = await Promise.all([
            api.fetchVisaoGeralTorres(),
            api.fetchDispositivosStatus()
        ]);

        // Define os estados com base nas respostas paralelas
        const hasTorres = torresResponse && torresResponse.success && Array.isArray(torresResponse.data) && torresResponse.data.length > 0;
        const hasEquipamentos = equipamentosResponse && equipamentosResponse.success && (equipamentosResponse.data.online > 0 || equipamentosResponse.data.offline > 0);

        document.body.dataset.hasTorres = hasTorres;
        document.body.dataset.hasEquipamentos = hasEquipamentos;

        // Agora, toma a decisão com base nos estados já conhecidos.
        if (!hasTorres) {
            // --- CENÁRIO 1: Não existem torres ---
            const torreIcon = `<svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"></path></svg>`;
            EmptyStateManager.show({
                containerId: 'dashboard-main-content',
                icon: torreIcon,
                title: 'Bem-vindo ao seu Dashboard!',
                message: 'Para começar a monitorizar, o primeiro passo é importar as suas torres a partir de um ficheiro CSV.',
                buttonText: '+ Importar Torres (CSV)',
                buttonAction: "showImportModal('torres')" // ✅ ALTERAÇÃO: Passa o contexto 'torres'
            });
        } else if (!hasEquipamentos) {
            // --- CENÁRIO 2: Existem torres, mas não equipamentos ---
            const equipamentoIcon = `<svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"></path></svg>`;
            EmptyStateManager.show({
                containerId: 'dashboard-main-content',
                icon: equipamentoIcon,
                title: 'Próximo Passo: Cadastre seus Equipamentos!',
                message: 'Excelente! Suas torres já estão no sistema. Agora, importe os equipamentos para começar a ver os dados de monitorização.',
                buttonText: '+ Importar Equipamentos (CSV)',
                buttonAction: "showImportModal('equipamentos')" // ✅ ALTERAÇÃO: Passa o contexto 'equipamentos'
            });
        } else {
            // --- CENÁRIO 3: Existem torres e equipamentos ---
            loadFullDashboard(torresResponse.data);
        }

        // Carrega os KPIs em paralelo com o resto da lógica
        carregarKpis();

    } catch (error) {
        console.error("❌ Erro ao inicializar o dashboard:", error);
        document.body.dataset.hasTorres = 'false';
        document.body.dataset.hasEquipamentos = 'false';
        document.getElementById('dashboard-main-content').innerHTML = `<div class="text-center p-8 text-red-500">Não foi possível carregar o dashboard. Verifique a sua conexão.</div>`;
    }
}

/**
 * Agrupa as chamadas para carregar todos os componentes do dashboard.
 * @param {Array} visaoGeralData - Os dados da visão geral, já buscados.
 */
function loadFullDashboard(visaoGeralData) {
    renderVisaoGeralTorres(visaoGeralData); // Reutiliza os dados já buscados
    carregarGraficoDispositivos();
    carregarGraficoInventario();
    carregarTorresCriticas();
}

// Função auxiliar para estados vazios DENTRO dos cards, caso necessário
function createLocalEmptyState(message) {
    return `<div class="flex items-center justify-center h-full text-sm text-gray-500 p-4">${message}</div>`;
}

async function carregarKpis() {
    try {
        const response = await api.fetchKpis();
        if (response && response.success) {
            const kpis = response.data;
            document.getElementById('kpi-total-torres').textContent = kpis.total_torres || 0;
            document.getElementById('kpi-torres-online').textContent = kpis.torres_online || 0;
            document.getElementById('kpi-torres-offline').textContent = kpis.torres_offline || 0;
            document.getElementById('kpi-uptime-medio').innerHTML = `${kpis.uptime_medio || 0}<span class="text-lg">%</span>`;
        }
    } catch (error) {
        console.error("Erro ao carregar KPIs:", error);
    }
}

async function carregarGraficoDispositivos() {
    const container = document.getElementById('status-chart-container');
    try {
        const response = await api.fetchDispositivosStatus();
        if (response && response.success) {
            const stats = response.data;
            if (stats.online === 0 && stats.offline === 0) {
                container.innerHTML = createLocalEmptyState('Não há dispositivos para exibir status.');
                return;
            }
            container.innerHTML = '<canvas id="dispositivosStatusChart"></canvas>';
            const ctx = document.getElementById('dispositivosStatusChart').getContext('2d');
            new Chart(ctx, { type: 'doughnut', data: { labels: ['Online', 'Offline'], datasets: [{ label: 'Dispositivos', data: [stats.online, stats.offline], backgroundColor: ['#10B981', '#EF4444'], borderColor: '#ffffff', borderWidth: 2 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } } });
        }
    } catch (error) {
        console.error("Erro ao carregar gráfico de dispositivos:", error);
        container.innerHTML = createLocalEmptyState('Falha ao carregar dados.');
    }
}

async function carregarGraficoInventario() {
    const container = document.getElementById('tipos-chart-container');
    try {
        const response = await api.fetchDispositivosTipos();
        if (response && response.success) {
            const inventario = response.data;
            if (!inventario || inventario.length === 0) {
                container.innerHTML = createLocalEmptyState('Não há inventário para exibir.');
                return;
            }
            const labels = inventario.map(item => item.tipo);
            const data = inventario.map(item => item.total);
            container.innerHTML = '<canvas id="inventarioTiposChart"></canvas>';
            const ctx = document.getElementById('inventarioTiposChart').getContext('2d');
            new Chart(ctx, { type: 'bar', data: { labels, datasets: [{ label: 'Quantidade', data, backgroundColor: '#3b82f6' }] }, options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { precision: 0 } } } } });
        }
    } catch (error) {
        console.error("Erro ao carregar gráfico de inventário:", error);
        container.innerHTML = createLocalEmptyState('Falha ao carregar dados.');
    }
}

async function carregarTorresCriticas() {
    const listContainer = document.getElementById('torres-criticas-list');
    try {
        const response = await api.fetchTorresCriticas();
        if (response && response.success && response.data.length > 0) {
            const torres = response.data;
            listContainer.innerHTML = torres.map(torre => {
                const dispositivosHtml = torre.dispositivos_offline.map(d => `<li class="text-sm text-gray-600 pl-4">- ${d.nome}</li>`).join('');
                return `<div class="border border-gray-200 rounded-lg"><button onclick="toggleTorreCritica(this)" class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50"><span class="font-medium text-gray-800">${torre.nome}</span><div class="flex items-center gap-3"><span class="bg-red-100 text-red-700 text-sm font-semibold px-3 py-1 rounded-full">${torre.offline_count} offline</span><i class="fas fa-chevron-down text-gray-500 transition-transform"></i></div></button><div class="hidden px-4 pb-3 border-t border-gray-200"><ul class="mt-2 space-y-1">${dispositivosHtml}</ul></div></div>`;
            }).join('');
        } else {
            listContainer.innerHTML = createLocalEmptyState('🎉 Nenhuma torre com dispositivos offline!');
        }
    } catch (error) {
        console.error("Erro ao carregar torres críticas:", error);
        listContainer.innerHTML = createLocalEmptyState('Falha ao carregar dados.');
    }
}

function toggleTorreCritica(buttonElement) {
    const detailsDiv = buttonElement.nextElementSibling;
    const icon = buttonElement.querySelector('i');
    detailsDiv.classList.toggle('hidden');
    icon.classList.toggle('rotate-180');
}

function renderVisaoGeralTorres(torres) {
    const tableBody = document.getElementById('visao-geral-torres-body');
    if (!torres || torres.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="p-8 text-center text-gray-500">Nenhuma torre encontrada.</td></tr>';
        return;
    }
    tableBody.innerHTML = torres.map(torre => `
        <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap"><div class="text-sm font-medium text-gray-900">${torre.nome}</div><div class="text-sm text-gray-500">${torre.localizacao || ''}</div></td>
            <td class="px-6 py-4 whitespace-nowrap"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" style="background-color:${torre.status_cor}20; color:${torre.status_cor};">${torre.status_descricao}</span></td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"><span class="font-bold text-gray-800">${torre.total_dispositivos}</span> T / <span class="font-bold text-green-600">${torre.dispositivos_online}</span> On / <span class="font-bold text-red-600">${torre.dispositivos_offline}</span> Off</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">${torre.uptime_percentage}%</td>
        </tr>
    `).join('');
}

document.addEventListener('DOMContentLoaded', initializeDashboard);
```

### `public\assets\js\mapa.js`

```js
/**
 * Script da Página do Mapa - BRDK v1
 * Implementa um mapa de satélite interativo com filtros automáticos,
 * marcadores inteligentes e um painel de detalhes lateral com meteorologia.
 * Otimizado para carregar o Empty State instantaneamente.
 */

// Variáveis globais
let mapa;
let todasAsTorres = []; // Armazena os dados brutos das torres
let todosOsMarcadores = []; // Armazena os objetos de marcadores do Leaflet
let clusterGroup;

// ===================================================================================
// INICIALIZAÇÃO PRINCIPAL (NOVA LÓGICA OTIMIZADA)
// ===================================================================================

async function initMapa() {
    try {
        // 1. FAZEMOS A VERIFICAÇÃO MAIS IMPORTANTE PRIMEIRO
        const response = await api.fetchTorresParaMapa();
        todasAsTorres = response.data.filter(t => t.latitude && t.longitude);

        // 2. DECIDIMOS O QUE FAZER COM BASE NO RESULTADO
        if (todasAsTorres.length === 0) {
            // Se NÃO houver torres, mostramos o Empty State IMEDIATAMENTE.
            // O mapa pesado nem chega a ser carregado.
            mostrarEmptyState();
        } else {
            // Se HOUVER torres, então prosseguimos com o carregamento do mapa.
            inicializarMapaCompleto();
            renderizarTorresEConfigurarFiltros();
        }
    } catch (error) {
        console.error("Erro crítico ao inicializar o mapa:", error);
        mostrarEmptyState("Falha ao carregar dados", "Não foi possível conectar à API. Verifique a sua conexão e tente novamente.");
    }
}

document.addEventListener('DOMContentLoaded', initMapa);


// ===================================================================================
// FUNÇÕES DE LÓGICA E RENDERIZAÇÃO
// ===================================================================================

/** Mostra a tela de boas-vindas quando não há torres. */
function mostrarEmptyState(titulo, mensagem) {
    const emptyStateContainer = document.getElementById('map-empty-state-container');
    emptyStateContainer.style.display = 'flex';
    emptyStateContainer.classList.remove('pointer-events-none');

    const torreIcon = `<svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"></path></svg>`;

    EmptyStateManager.show({
        containerId: 'map-empty-state-container',
        icon: torreIcon,
        title: titulo || 'Nenhuma torre para exibir no mapa',
        message: mensagem || 'Para visualizar a sua infraestrutura, primeiro adicione torres com geolocalização através de um ficheiro CSV.',
        buttonText: '+ Importar Torres (CSV)',
        buttonAction: "showImportModal('torres')"
    });
    atualizarResumo([]); // Zera o widget de resumo
}

/** Inicializa o objeto do mapa, tiles e clusters. */
function inicializarMapaCompleto() {
    const emptyStateContainer = document.getElementById('map-empty-state-container');
    emptyStateContainer.style.display = 'none'; // Garante que o empty state está escondido

    mapa = L.map('mapa', { zoomControl: false }).setView([-15.7801, -47.9292], 4);
    L.control.zoom({ position: 'topright' }).addTo(mapa);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}').addTo(mapa);

    clusterGroup = L.markerClusterGroup();
    mapa.addLayer(clusterGroup);
}

/** Popula os filtros e desenha as torres no mapa. */
async function renderizarTorresEConfigurarFiltros() {
    // Popula o filtro de regiões (localizações)
    const filtroRegiao = document.getElementById('filtro-regiao');
    const regioes = [...new Set(todasAsTorres.map(t => t.localizacao).filter(Boolean))];
    regioes.sort();
    regioes.forEach(regiao => filtroRegiao.add(new Option(regiao, regiao)));

    // Adiciona os event listeners aos filtros
    document.getElementById('filtro-status').addEventListener('change', aplicarFiltros);
    document.getElementById('filtro-regiao').addEventListener('change', aplicarFiltros);

    // Renderiza as torres no mapa pela primeira vez (sem filtros)
    aplicarFiltros();
}

/** Filtra as torres e (re)desenha os marcadores no mapa. */
function aplicarFiltros() {
    clusterGroup.clearLayers();
    todosOsMarcadores = [];

    const filtroStatus = document.getElementById('filtro-status').value;
    const filtroRegiao = document.getElementById('filtro-regiao').value;

    let torresFiltradas = todasAsTorres;

    if (filtroStatus !== 'todos') {
        torresFiltradas = torresFiltradas.filter(t => (t.status.id === 1 && filtroStatus === 'online') || (t.status.id !== 1 && filtroStatus === 'offline'));
    }
    if (filtroRegiao !== 'todas') {
        torresFiltradas = torresFiltradas.filter(t => t.localizacao === filtroRegiao);
    }

    torresFiltradas.forEach(torre => {
        const marcador = L.marker([torre.latitude, torre.longitude], { icon: criarMarcadorPersonalizado(torre) });
        marcador.on('click', () => showDetalhesPainel(torre.id));
        todosOsMarcadores.push(marcador);
    });

    clusterGroup.addLayers(todosOsMarcadores);
    atualizarResumo(torresFiltradas);

    // Centraliza o mapa nos marcadores filtrados, se houver algum
    if (todosOsMarcadores.length > 0) {
        const groupBounds = L.featureGroup(todosOsMarcadores).getBounds();
        mapa.fitBounds(groupBounds.pad(0.1)); // pad(0.1) adiciona uma pequena margem
    }
}


// ===================================================================================
// FUNÇÕES DE UI E HELPERS (sem grandes alterações)
// ===================================================================================

/** Exibe o painel de detalhes da torre, busca os dados e os renderiza. */
async function showDetalhesPainel(torreId) {
    const painel = document.getElementById('detalhes-torre-painel');
    if (!painel) return;

    painel.classList.remove('-translate-x-full');
    painel.innerHTML = `<div class="p-6 text-center text-gray-500"><i class="fas fa-spinner fa-spin mr-2"></i> A carregar detalhes...</div>`;

    try {
        const [detalhesResponse, tempoResponse] = await Promise.all([
            api.fetchTorreDetails(torreId),
            api.fetchTempoTorre(torreId)
        ]);
        renderDetalhesNoPainel(detalhesResponse.data, tempoResponse.data);
    } catch (error) {
        console.error("Erro ao buscar detalhes da torre:", error);
        painel.innerHTML = `<div class="p-6 text-center text-red-500">Falha ao carregar detalhes. <button onclick="closeDetalhesPainel()" class="text-blue-600 underline font-semibold">Fechar</button></div>`;
    }
}

/** Esconde o painel de detalhes. */
function closeDetalhesPainel() {
    const painel = document.getElementById('detalhes-torre-painel');
    if (painel) painel.classList.add('-translate-x-full');
}

/** Constrói o painel de detalhes clonando e preenchendo os templates. */
function renderDetalhesNoPainel(detalhes, tempo) {
    const painel = document.getElementById('detalhes-torre-painel');
    const template = document.getElementById('detalhes-torre-template');
    const clone = template.content.cloneNode(true);

    const torre = detalhes.torre;
    const equipamentos = detalhes.dispositivos || [];

    // Preenche dados da Torre
    clone.querySelector('[data-template-id="nome-torre"]').textContent = torre.nome;
    clone.querySelector('[data-template-id="nome-torre"]').title = torre.nome;
    clone.querySelector('[data-template-id="localizacao-torre"]').textContent = torre.localizacao || 'N/A';
    clone.querySelector('[data-template-id="link-gerenciar"]').href = `/torres?torreId=${torre.id}`;
    clone.querySelector('[data-template-id="btn-fechar"]').onclick = closeDetalhesPainel;

    const statusEl = clone.querySelector('[data-template-id="status-torre"]');
    statusEl.textContent = torre.status.descricao || 'Desconhecido';
    statusEl.style.backgroundColor = `${torre.status.cor}20`;
    statusEl.style.color = torre.status.cor;

    // Preenche dados de Meteorologia
    const blocoTempo = clone.querySelector('[data-template-id="bloco-tempo"]');
    const semTempoMsg = clone.querySelector('[data-template-id="sem-tempo"]');

    if (tempo && tempo.agora) {
        blocoTempo.style.display = 'block';
        semTempoMsg.style.display = 'none';
        clone.querySelector('[data-template-id="icone-tempo"]').src = `https://openweathermap.org/img/wn/${tempo.agora.icone}@2x.png`;
        clone.querySelector('[data-template-id="temperatura-tempo"]').textContent = `${tempo.agora.temperatura}°C`;
        clone.querySelector('[data-template-id="condicao-tempo"]').textContent = tempo.agora.condicao;
        clone.querySelector('[data-template-id="umidade-tempo"]').textContent = `${tempo.agora.umidade}%`;

        const previsaoContainer = clone.querySelector('[data-template-id="lista-previsao"]');
        const previsaoTemplate = document.getElementById('detalhes-previsao-template');
        if (tempo.previsao_proximos_dias && tempo.previsao_proximos_dias.length > 0) {
            tempo.previsao_proximos_dias.forEach(dia => {
                const prevClone = previsaoTemplate.content.cloneNode(true);
                prevClone.querySelector('[data-template-id="previsao-dia"]').textContent = dia.dia_semana;
                prevClone.querySelector('[data-template-id="previsao-icone"]').src = `https://openweathermap.org/img/wn/${dia.icone}.png`;
                prevClone.querySelector('[data-template-id="previsao-temp"]').textContent = `${dia.temp_max}°/${dia.temp_min}°`;
                previsaoContainer.appendChild(prevClone);
            });
        }
    } else {
        blocoTempo.style.display = 'none';
        semTempoMsg.style.display = 'block';
    }

    // Preenche lista de Equipamentos
    clone.querySelector('[data-template-id="total-equipamentos"]').textContent = equipamentos.length;
    const listaEquipamentosEl = clone.querySelector('[data-template-id="lista-equipamentos"]');
    const semEquipamentosMsg = clone.querySelector('[data-template-id="sem-equipamentos"]');

    if (equipamentos.length > 0) {
        const equipamentoTemplate = document.getElementById('detalhes-equipamento-template');
        equipamentos.forEach(eq => {
            const eqClone = equipamentoTemplate.content.cloneNode(true);
            const eqIsOnline = eq.status.id === 1;
            eqClone.querySelector('[data-template-id="nome-equipamento"]').textContent = eq.nome;
            eqClone.querySelector('[data-template-id="ip-equipamento"]').textContent = eq.ip;
            eqClone.querySelector('[data-template-id="status-led"]').classList.add(eqIsOnline ? 'bg-green-500' : 'bg-red-500');
            const statusEqEl = eqClone.querySelector('[data-template-id="status-texto"]');
            statusEqEl.textContent = eqIsOnline ? 'Online' : 'Offline';
            statusEqEl.classList.add(eqIsOnline ? 'text-green-700' : 'text-red-700');
            listaEquipamentosEl.appendChild(eqClone);
        });
        semEquipamentosMsg.style.display = 'none';
    } else {
        semEquipamentosMsg.style.display = 'block';
    }

    painel.innerHTML = '';
    painel.appendChild(clone);
}

/** * Cria o HTML para o marcador personalizado no mapa, com o texto sempre visível.
 * Utiliza Template Literals para melhor legibilidade do código.
 */
function criarMarcadorPersonalizado(torre) {
    const isOnline = torre.status.id === 1;
    const onlineCount = torre.dispositivos_stats.online;
    const offlineCount = torre.dispositivos_stats.offline;

    // A estrutura HTML volta a ser a original, mas escrita com Template Literals (` `).
    const html = `
        <div class="flex flex-col items-center cursor-pointer">
            <div class="w-5 h-5 ${isOnline ? 'bg-green-500' : 'bg-red-500 animate-pulse'} rounded-full border-2 border-white shadow-lg"></div>
            <div class="bg-gray-800 bg-opacity-75 text-white text-xs font-semibold px-2 py-1 rounded-md shadow-lg mt-2 text-center whitespace-nowrap">
                <p>${torre.nome}</p>
                <div class="flex justify-center items-center gap-2 mt-1">
                    <span class="text-green-400 flex items-center gap-1"><i class="fas fa-arrow-up fa-xs"></i> ${onlineCount}</span>
                    <span class="text-red-400 flex items-center gap-1"><i class="fas fa-arrow-down fa-xs"></i> ${offlineCount}</span>
                </div>
            </div>
        </div>`;

    return L.divIcon({
        className: 'custom-map-marker', // Classe vazia para evitar estilos padrão do Leaflet
        html: html,
        iconAnchor: [10, 10] // Define que o ponto de ancoragem é o centro da bolinha colorida
    });
}

/** Atualiza o widget de resumo com as contagens atuais. */
function atualizarResumo(torresVisiveis) {
    const online = torresVisiveis.filter(t => t.status.id === 1).length;
    const offline = torresVisiveis.length - online;
    document.getElementById('summary-total').textContent = torresVisiveis.length;
    document.getElementById('summary-online').textContent = online;
    document.getElementById('summary-offline').textContent = offline;
}
```

### `public\assets\js\torres.js`

```js
/**
 * Lógica da Página de Gestão de Torres
 * Foco no "básico bem feito": CRUD de Torres e Paginação.
 */

// ===================================================================================
// ESTADO E CONSTANTES
// ===================================================================================
let allTorres = [];
let filteredTorres = [];
let currentPage = 1;
let tiposDeDispositivo = []; // Guarda os tipos para não buscar toda hora
const itemsPerPage = 12;

// ===================================================================================
// INICIALIZAÇÃO
// ===================================================================================
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadInitialData();
});

async function loadInitialData() {
    try {
        const responseTipos = await api.fetchTiposDispositivo();
        if (responseTipos.success) {
            tiposDeDispositivo = responseTipos.data;
        }
    } catch (e) {
        console.error("Falha ao carregar tipos de dispositivo.");
    }

    // Carrega as torres como antes
    await loadTorresFromAPI();
    // Após carregar todas as torres, verifica se um ID veio na URL
    const params = new URLSearchParams(window.location.search);
    const torreIdFromUrl = params.get('torreId');

    if (torreIdFromUrl) {
        // Se encontrámos um ID, procuramos a torre correspondente na nossa lista
        const torreEncontrada = allTorres.find(t => t.id == torreIdFromUrl);

        if (torreEncontrada) {
            // Se a torre existir, abrimos o painel de detalhes para ela!
            // Adicionamos um pequeno atraso para dar tempo à interface de renderizar.
            setTimeout(() => {
                openTorreDetails(torreEncontrada.id);
            }, 250); // Atraso de 250ms
        } else {
            console.warn(`Torre com ID ${torreIdFromUrl} não encontrada.`);
        }
    }
}

function setupEventListeners() {
    document.getElementById('search-torres').addEventListener('input', applyFilters);
    document.getElementById('status-filter').addEventListener('change', applyFilters);
    document.getElementById('location-filter').addEventListener('change', applyFilters);
    document.getElementById('btn-limpar-filtros').addEventListener('click', clearFilters);
    document.getElementById('btn-nova-torre').addEventListener('click', () => openTorreModal());
    document.getElementById('btn-fechar-modal').addEventListener('click', closeTorreModal);
    document.getElementById('btn-cancelar-modal').addEventListener('click', closeTorreModal);
    document.getElementById('torre-form').addEventListener('submit', saveTorre);
    document.addEventListener('click', () => closeAllDropdowns(), true); // Usar capture para fechar dropdowns

    document.querySelectorAll('.numeric-input').forEach(input => {
        input.addEventListener('input', (e) => {
            // Remove qualquer caractere que não seja um número, ponto ou o sinal de menos no início.
            e.target.value = e.target.value.replace(/[^0-9.-]/g, '').replace(/(\..*)\./g, '$1');
        });
    });

    document.getElementById('btn-fechar-dispositivo-modal').addEventListener('click', closeDispositivoModal);
    document.getElementById('btn-cancelar-dispositivo-modal').addEventListener('click', closeDispositivoModal);
    document.getElementById('dispositivo-form').addEventListener('submit', saveDispositivo);
    document.addEventListener('click', () => closeAllDropdowns(), true);
}

// ===================================================================================
// LÓGICA DE DADOS (API)
// ===================================================================================
async function loadTorresFromAPI() {
    showLoadingState();
    try {
        const response = await api.fetchTorresParaMapa(); // Endpoint que já retorna os dados completos
        if (response.success && Array.isArray(response.data)) {
            allTorres = response.data;
            populateLocationFilter();
            applyFilters();
        } else {
            allTorres = [];
            applyFilters();
        }
    } catch (error) {
        console.error('❌ Erro ao carregar torres:', error);
        showErrorState(error.message);
    }
}

// ===================================================================================
// LÓGICA DE CRUD (CRIAR, EDITAR, EXCLUIR TORRES)
// ===================================================================================
function openTorreModal(torre = null) {
    const modal = document.getElementById('torre-modal');
    const form = document.getElementById('torre-form');
    const title = document.getElementById('modal-title');
    form.reset();
    if (torre) {
        title.textContent = `Editar Torre: ${torre.nome}`;
        document.getElementById('torre-id').value = torre.id;
        document.getElementById('nome-torre').value = torre.nome;
        document.getElementById('status-torre').value = torre.status.id;
        document.getElementById('localizacao-torre').value = torre.localizacao;
        document.getElementById('latitude-torre').value = torre.latitude;
        document.getElementById('longitude-torre').value = torre.longitude;
        document.getElementById('observacoes-torre').value = torre.observacoes;
    } else {
        title.textContent = 'Adicionar Nova Torre';
        document.getElementById('torre-id').value = '';
    }
    modal.classList.remove('hidden');
}

function closeTorreModal() {
    document.getElementById('torre-modal').classList.add('hidden');
}

async function saveTorre(event) {
    event.preventDefault();
    const id = document.getElementById('torre-id').value;
    const form = document.getElementById('torre-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    data.latitude = data.latitude ? parseFloat(data.latitude) : null;
    data.longitude = data.longitude ? parseFloat(data.longitude) : null;
    data.status_geral = parseInt(data.status_geral);

    try {
        if (id) {
            await api.updateTorre(id, data);
            showNotification('Torre atualizada com sucesso!', 'success');
        } else {
            await api.createTorre(data);
            showNotification('Torre criada com sucesso!', 'success');
        }
        closeTorreModal();
        await loadTorresFromAPI();
    } catch (error) {
        showNotification(error.message || 'Erro ao salvar torre.', 'error');
    }
}

function deleteTorre(id, nome) {
    showConfirmationModal({
        title: `Excluir Torre`,
        message: `Tem a certeza que deseja excluir a torre "${nome}"? Esta ação não pode ser desfeita.`,
        onConfirm: async () => {
            try {
                await api.deleteTorre(id);
                showNotification('Torre excluída com sucesso!', 'success');
                await loadTorresFromAPI();
            } catch (error) {
                showNotification(error.message || 'Erro ao excluir torre.', 'error');
            }
        }
    });
}

// ===================================================================================
// PAINEL DE DETALHES LATERAL
// ===================================================================================
async function openTorreDetails(torreId) {
    const painel = document.getElementById('detalhe-torre-painel');
    painel.classList.remove('translate-x-full');
    painel.innerHTML = `<div class="p-6 text-center text-gray-500"><i class="fas fa-spinner fa-spin mr-2"></i> A carregar detalhes...</div>`;

    try {
        const [torreResponse, dispositivosResponse] = await Promise.all([
            api.fetchTorreDetails(torreId),
            api.fetchDispositivosDaTorre(torreId)
        ]);
        if (torreResponse.success && dispositivosResponse.success) {
            renderTorreDetails(torreResponse.data.torre, dispositivosResponse.data);
        } else {
            throw new Error('Falha ao carregar todos os detalhes da torre.');
        }
    } catch (error) {
        painel.innerHTML = `<div class="p-6 text-red-500">Erro ao carregar detalhes. <button onclick="closeTorreDetails()" class="underline">Fechar</button></div>`;
        console.error(error);
    }
}

function closeTorreDetails() {
    document.getElementById('detalhe-torre-painel').classList.add('translate-x-full');
}

function renderTorreDetails(torre, dispositivos, torreId) {
    const painel = document.getElementById('detalhe-torre-painel');
    const template = document.getElementById('detalhe-torre-template');
    const clone = template.content.cloneNode(true);

    clone.querySelector('[data-template-id="detalhe-nome-torre"]').textContent = torre.nome;
    const [statusText, statusColor] = getStatusInfo(torre.status.id);
    const statusEl = clone.querySelector('[data-template-id="detalhe-status-torre"]');
    statusEl.textContent = statusText;
    statusEl.className = `font-semibold px-2 py-0.5 rounded-full text-xs bg-${statusColor}-100 text-${statusColor}-800`;
    clone.querySelector('[data-template-id="detalhe-localizacao-torre"]').textContent = torre.localizacao;
    clone.querySelector('[data-template-id="detalhe-uptime-torre"]').textContent = `${parseFloat(torre.uptime || 0).toFixed(1)}%`;
    clone.querySelector('[data-template-id="btn-fechar-detalhes"]').onclick = closeTorreDetails;

    clone.querySelector('[data-template-id="detalhe-total-dispositivos"]').textContent = dispositivos.length;
    const listaContainer = clone.querySelector('[data-template-id="detalhe-lista-dispositivos"]');
    const semDispositivosMsg = clone.querySelector('[data-template-id="detalhe-sem-dispositivos"]');
    const itemTemplate = document.getElementById('detalhe-dispositivo-item-template');

    if (dispositivos.length > 0) {
        dispositivos.forEach(disp => {
            const itemClone = itemTemplate.content.cloneNode(true);
            // Corrigido para usar a chave correta da API
            const [dispStatusText, dispStatusColor] = getStatusInfo(disp.status_id);
            itemClone.querySelector('[data-template-id="dispositivo-status-led"]').classList.add(`bg-${dispStatusColor}-500`);
            itemClone.querySelector('[data-template-id="dispositivo-nome"]').textContent = disp.nome;
            itemClone.querySelector('[data-template-id="dispositivo-ip"]').textContent = disp.ip;

            // LIGAÇÃO DAS AÇÕES
            itemClone.querySelector('[data-template-id="btn-editar-dispositivo"]').onclick = () => openDispositivoModal(disp, torreId);
            itemClone.querySelector('[data-template-id="btn-excluir-dispositivo"]').onclick = () => deleteDispositivo(disp, torreId);

            listaContainer.appendChild(itemClone);
        });
    } else {
        semDispositivosMsg.classList.remove('hidden');
    }

    painel.innerHTML = '';
    painel.appendChild(clone);
}

// ===================================================================================
// FUNÇÕES DE UI (RENDERIZAÇÃO, FILTROS, PAGINAÇÃO)
// ===================================================================================
function updateUI() {
    hideStates();
    updateQuickStats();
    renderTorresGrid();
    setupPagination();
}

function applyFilters() {
    const statusFilter = document.getElementById('status-filter').value;
    const locationFilter = document.getElementById('location-filter').value;
    const searchTerm = document.getElementById('search-torres').value.toLowerCase().trim();

    filteredTorres = allTorres.filter(torre => {
        const matchStatus = !statusFilter || torre.status.id == statusFilter;
        const matchLocation = !locationFilter || torre.localizacao === locationFilter;
        const matchSearch = !searchTerm ||
            (torre.nome && torre.nome.toLowerCase().includes(searchTerm)) ||
            (torre.localizacao && torre.localizacao.toLowerCase().includes(searchTerm));
        return matchStatus && matchLocation && matchSearch;
    });
    currentPage = 1;
    if (allTorres.length === 0) {
        showEmptyState();
    } else if (filteredTorres.length === 0) {
        updateQuickStats();
        showEmptyState('Nenhuma torre encontrada', 'Nenhuma torre corresponde aos filtros aplicados.');
        setupPagination();
    } else {
        updateUI();
    }
}

function clearFilters() {
    document.getElementById('status-filter').value = '';
    document.getElementById('location-filter').value = '';
    document.getElementById('search-torres').value = '';
    applyFilters();
}

function renderTorresGrid() {
    const gridContainer = document.getElementById('torres-container');
    const template = document.getElementById('torre-card-template');

    const startIndex = (currentPage - 1) * itemsPerPage;
    const paginatedTorres = filteredTorres.slice(startIndex, startIndex + itemsPerPage);

    gridContainer.innerHTML = '';
    const grid = document.createElement('div');
    grid.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6';

    paginatedTorres.forEach(torre => {
        const clone = template.content.cloneNode(true);
        const [statusText, statusColor] = getStatusInfo(torre.status.id);

        const statusBadge = clone.querySelector('[data-template-id="status-badge"]');
        statusBadge.textContent = statusText;
        statusBadge.className = `px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-${statusColor}-100 text-${statusColor}-800`;

        clone.querySelector('[data-template-id="nome"]').textContent = torre.nome;
        clone.querySelector('[data-template-id="localizacao"]').textContent = torre.localizacao || 'Sem localização';
        clone.querySelector('[data-template-id="uptime"]').textContent = `${parseFloat(torre.uptime_percentage || 0).toFixed(1)}%`;
        clone.querySelector('[data-template-id="dispositivos"]').textContent = `${torre.dispositivos_stats.online}/${torre.dispositivos_stats.total}`;

        clone.querySelector('[data-template-id="card-body"]').onclick = () => openTorreDetails(torre.id);
        clone.querySelector('[data-template-id="btn-detalhes"]').onclick = (e) => { e.preventDefault(); e.stopPropagation(); openTorreDetails(torre.id); };
        clone.querySelector('[data-template-id="btn-editar"]').onclick = (e) => { e.preventDefault(); e.stopPropagation(); openTorreModal(torre); };
        clone.querySelector('[data-template-id="btn-excluir"]').onclick = (e) => { e.preventDefault(); e.stopPropagation(); deleteTorre(torre.id, torre.nome); };

        const dropdown = clone.querySelector('[data-template-id="actions-dropdown"]');
        const dropdownButton = dropdown.querySelector('button');
        const dropdownMenu = dropdown.querySelector('div');
        dropdownButton.addEventListener('click', (e) => {
            e.stopPropagation();
            closeAllDropdowns(dropdownMenu);
            dropdownMenu.classList.toggle('hidden');
        });
        grid.appendChild(clone);
    });
    gridContainer.appendChild(grid);
}

function setupPagination() {
    const paginationContainer = document.getElementById('torres-pagination');
    const template = document.getElementById('pagination-template');
    const totalRecords = filteredTorres.length;
    const totalPages = Math.ceil(totalRecords / itemsPerPage);

    paginationContainer.innerHTML = '';
    if (totalPages <= 1) return;

    const clone = template.content.cloneNode(true);
    const showingFrom = totalRecords > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0;
    const showingTo = Math.min(currentPage * itemsPerPage, totalRecords);

    clone.querySelector('[data-template-id="showing-from"]').textContent = showingFrom;
    clone.querySelector('[data-template-id="showing-to"]').textContent = showingTo;
    clone.querySelector('[data-template-id="total-records"]').textContent = totalRecords;

    const prevBtn = clone.querySelector('[data-template-id="prev-page"]');
    const nextBtn = clone.querySelector('[data-template-id="next-page"]');

    prevBtn.onclick = () => changePage(currentPage - 1);
    nextBtn.onclick = () => changePage(currentPage + 1);

    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;

    paginationContainer.appendChild(clone);
}

function changePage(page) {
    const totalPages = Math.ceil(filteredTorres.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderTorresGrid();
    setupPagination();
    document.querySelector('.torres-header').scrollIntoView({ behavior: 'smooth' });
}

// ===================================================================================
// FUNÇÕES DE UI E ESTADO
// ===================================================================================
function updateQuickStats() {
    const total = allTorres.length;
    const online = allTorres.filter(t => t.status.id === 1).length;
    const offline = allTorres.filter(t => t.status.id !== 1).length;
    const uptimes = allTorres.map(t => parseFloat(t.uptime_percentage)).filter(u => !isNaN(u));
    const avgUptime = uptimes.length > 0 ? (uptimes.reduce((a, b) => a + b, 0) / uptimes.length) : 0;

    document.getElementById('total-torres').textContent = total;
    document.getElementById('torres-online').textContent = online;
    document.getElementById('torres-offline').textContent = offline;
    document.getElementById('uptime-medio').textContent = `${avgUptime.toFixed(1)}%`;
}

function populateLocationFilter() {
    const locationFilter = document.getElementById('location-filter');
    const locations = [...new Set(allTorres.map(t => t.localizacao).filter(Boolean))];
    locations.sort();
    while (locationFilter.options.length > 1) locationFilter.remove(1);
    locations.forEach(loc => locationFilter.add(new Option(loc, loc)));
}

function showLoadingState() {
    const container = document.getElementById('torres-container');
    container.innerHTML = `<div class="text-center p-8 text-gray-500"><i class="fas fa-spinner fa-spin fa-2x"></i><p class="mt-2">A carregar torres...</p></div>`;
}

function showEmptyState(title, message) {
    const container = document.getElementById('torres-container');

    // CORREÇÃO: Usar um ícone Font Awesome para consistência e centralização perfeita.
    const icon = `<i class="fas fa-broadcast-tower fa-3x text-gray-300"></i>`;

    container.innerHTML = `
        <div class="bg-white p-8 rounded-lg shadow-md text-center mt-8 flex flex-col items-center">
            <div class="mb-4">
                ${icon}
            </div>
            <h3 class="mt-2 text-xl font-semibold text-gray-800">${title || 'Nenhuma torre cadastrada'}</h3>
            <p class="mt-1 text-gray-500">${message || 'Adicione torres para começar a monitorizar.'}</p>
            <button onclick="document.getElementById('btn-nova-torre').click()" class="mt-6 inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700">
                <i class="fas fa-plus"></i> Adicionar Primeira Torre
            </button>
        </div>
    `;
}

function showErrorState(message) {
    const container = document.getElementById('torres-container');
    container.innerHTML = `<div class="bg-red-50 text-red-700 p-6 rounded-lg shadow-md text-center">
        <h3 class="font-semibold">Ocorreu um erro</h3><p class="text-sm">${message}</p>
    </div>`;
}

function hideStates() {
    document.getElementById('torres-container').innerHTML = '';
}

// ===================================================================================
// FUNÇÕES AUXILIARES
// ===================================================================================
function getStatusInfo(statusId) {
    // Lógica simplificada conforme pedido
    switch (Number(statusId)) {
        case 1: return ['Online', 'green'];
        default: return ['Offline', 'red'];
    }
}

function showNotification(message, type = 'success') {
    const toast = document.getElementById('notification-toast');
    if (!toast) { console.log(`Notification (${type}): ${message}`); return; }
    toast.textContent = message;
    toast.className = `fixed top-5 right-5 p-4 rounded-md shadow-lg text-white transition-all duration-300 z-50 ${type === 'success' ? 'bg-green-600' : 'bg-red-600'}`;
    toast.classList.remove('hidden');
    setTimeout(() => { toast.classList.add('hidden'); }, 4000);
}

function closeAllDropdowns(exceptThisOne = null) {
    document.querySelectorAll('[data-template-id="actions-dropdown"] > div').forEach(menu => {
        if (menu !== exceptThisOne) {
            menu.classList.add('hidden');
        }
    });
}

function showConfirmationModal({ title, message, onConfirm }) {
    const modal = document.getElementById('confirmation-modal');
    document.getElementById('confirmation-title').textContent = title;
    document.getElementById('confirmation-message').textContent = message;

    const confirmBtn = document.getElementById('btn-confirm-action');
    const cancelBtn = document.getElementById('btn-confirm-cancel');

    // Remove event listeners antigos para evitar chamadas múltiplas
    confirmBtn.replaceWith(confirmBtn.cloneNode(true));
    cancelBtn.replaceWith(cancelBtn.cloneNode(true));

    // Pega as novas referências dos botões
    const newConfirmBtn = document.getElementById('btn-confirm-action');
    const newCancelBtn = document.getElementById('btn-confirm-cancel');

    const closeModal = () => modal.classList.add('hidden');

    newConfirmBtn.onclick = () => {
        onConfirm();
        closeModal();
    };
    newCancelBtn.onclick = closeModal;

    modal.classList.remove('hidden');
}

// ===================================================================================
// LÓGICA DE CRUD DE DISPOSITIVOS
// ===================================================================================
function openDispositivoModal(dispositivo = null, torreId) {
    const modal = document.getElementById('dispositivo-modal');
    const form = document.getElementById('dispositivo-form');
    const title = document.getElementById('dispositivo-modal-title');
    form.reset();

    const tipoSelect = document.getElementById('dispositivo-tipo');
    tipoSelect.innerHTML = '<option value="">Selecione um tipo...</option>';
    tiposDeDispositivo.forEach(tipo => {
        tipoSelect.add(new Option(tipo.descricao, tipo.id));
    });

    if (dispositivo) { // Modo Edição
        title.textContent = `Editar Dispositivo: ${dispositivo.nome}`;
        document.getElementById('dispositivo-id').value = dispositivo.id;
        document.getElementById('dispositivo-torre-id').value = torreId;
        document.getElementById('dispositivo-nome').value = dispositivo.nome;
        document.getElementById('dispositivo-ip').value = dispositivo.ip;
        document.getElementById('dispositivo-tipo').value = dispositivo.tipo_dispositivo_id;
        document.getElementById('dispositivo-status').value = dispositivo.status_id;
    } else { // Modo Criação
        title.textContent = 'Adicionar Novo Dispositivo';
        document.getElementById('dispositivo-id').value = '';
        document.getElementById('dispositivo-torre-id').value = torreId;
    }
    modal.classList.remove('hidden');
}

function closeDispositivoModal() {
    document.getElementById('dispositivo-modal').classList.add('hidden');
}

async function saveDispositivo(event) {
    event.preventDefault();

    // Leitura explícita de cada campo para garantir os dados corretos
    const id = document.getElementById('dispositivo-id').value;
    const torreId = document.getElementById('dispositivo-torre-id').value;
    const nome = document.getElementById('dispositivo-nome').value;
    const ip = document.getElementById('dispositivo-ip').value;
    const tipo_dispositivo_id = document.getElementById('dispositivo-tipo').value;
    const status = document.getElementById('dispositivo-status').value;

    // Construção manual do objeto de dados
    const data = {
        nome: nome,
        ip: ip,
        tipo_dispositivo_id: parseInt(tipo_dispositivo_id),
        status: status, // A coluna no BD é VARCHAR, então enviamos como string '1' ou '2'
        torre_id: parseInt(torreId) // Garantimos que o torre_id está aqui!
    };

    try {
        if (id) {
            // Requisição para ATUALIZAR
            await api.updateDispositivo(id, data);
            showNotification('Dispositivo atualizado com sucesso!', 'success');
        } else {
            // Requisição para CRIAR
            await api.createDispositivo(data);
            showNotification('Dispositivo criado com sucesso!', 'success');
        }

        closeDispositivoModal();

        // ATUALIZAÇÃO DINÂMICA (sem reload da página inteira)
        // Usamos Promise.all para fazer as duas atualizações em paralelo
        await Promise.all([
            openTorreDetails(torreId), // Recarrega o painel de detalhes para mostrar a alteração
            loadTorresFromAPI()      // Recarrega a lista principal de torres para atualizar os KPIs
        ]);

    } catch (error) {
        showNotification(error.message || 'Erro ao salvar dispositivo.', 'error');
    }
}

function deleteDispositivo(dispositivo, torreId) {
    showConfirmationModal({
        title: 'Excluir Dispositivo',
        message: `Tem a certeza que deseja excluir o dispositivo "${dispositivo.nome}"?`,
        onConfirm: async () => {
            try {
                await api.deleteDispositivo(dispositivo.id);
                showNotification('Dispositivo excluído com sucesso!', 'success');

                // Ação de Reload!
                setTimeout(() => {
                    window.location.reload();
                }, 1000); // Espera 1 segundo para o usuário ver a notificação

            } catch (error) {
                showNotification(error.message || 'Erro ao excluir dispositivo.', 'error');
            }
        }
    });
}

function showConfirmationModal({ title, message, onConfirm }) {
    const modal = document.getElementById('confirmation-modal');
    document.getElementById('confirmation-title').textContent = title;
    document.getElementById('confirmation-message').textContent = message;

    const confirmBtn = document.getElementById('btn-confirm-action');
    const cancelBtn = document.getElementById('btn-confirm-cancel');

    // Remove event listeners antigos para evitar chamadas múltiplas
    confirmBtn.replaceWith(confirmBtn.cloneNode(true));
    cancelBtn.replaceWith(cancelBtn.cloneNode(true));

    const newConfirmBtn = document.getElementById('btn-confirm-action');
    const newCancelBtn = document.getElementById('btn-confirm-cancel');

    const closeModal = () => modal.classList.add('hidden');

    newConfirmBtn.onclick = () => {
        onConfirm();
        closeModal();
    };
    newCancelBtn.onclick = closeModal;

    modal.classList.remove('hidden');
}
```

### `public\assets\js\components\emptyStateManager.js`

```js
/**
 * Fornece uma maneira reutilizável de exibir painéis de "estado vazio" ou
 * "boas-vindas", preenchendo o conteúdo de um container alvo.
 */
const EmptyStateManager = {
    /**
     * Exibe um painel de estado vazio, preenchendo o conteúdo de um container.
     * @param {object} options - As opções para personalizar o painel.
     * @param {string} options.containerId - O ID do elemento a ser preenchido.
     * @param {string} [options.icon] - O SVG completo para o ícone.
     * @param {string} options.title - O título principal do painel.
     * @param {string} options.message - A mensagem de parágrafo.
     * @param {string} [options.buttonText] - O texto para o botão de ação.
     * @param {string} [options.buttonAction] - A função a ser chamada pelo onclick do botão.
     */
    show(options) {
        const { containerId, icon, title, message, buttonText, buttonAction } = options;

        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`[EmptyStateManager] Erro: Container com ID "${containerId}" não foi encontrado.`);
            return;
        }

        // Constrói o HTML do ícone e do botão de forma condicional
        const iconHtml = icon ? `<div class="bg-indigo-100 text-indigo-600 rounded-full p-4 mb-6">${icon}</div>` : '';
        
        const buttonHtml = (buttonText && buttonAction) ?
            `<button
                onclick="${buttonAction}"
                class="mt-8 px-6 py-3 bg-indigo-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-transform transform hover:scale-105 pointer-events-auto">
                ${buttonText}
            </button>` : '';

        // Monta o HTML final do painel
        const panelHTML = `
            <div class="bg-white p-8 rounded-lg shadow-xl text-center flex flex-col items-center border border-gray-200 max-w-lg mx-auto">
                ${iconHtml}
                <h2 class="text-2xl font-bold text-gray-800">${title}</h2>
                <p class="mt-2 text-gray-600 max-w-md">${message}</p>
                ${buttonHtml}
            </div>
        `;

        // **A MUDANÇA ESTÁ AQUI:**
        // Agora injetamos o HTML diretamente dentro do container especificado.
        container.innerHTML = panelHTML;
        // E garantimos que o container está visível.
        container.style.display = 'flex';
    }
};
```

### `public\assets\js\components\import-modal.js`

```js
let importType = '';

function showImportModal(contexto) {
    const modal = document.getElementById('importModal');
    if (!modal) return;
    const hasTorres = document.body.dataset.hasTorres === 'true';
    const torresButton = document.getElementById('import-torres-btn');
    const equipamentosButton = document.getElementById('import-equipamentos-btn');
    const setButtonState = (button, enable, title) => {
        if (!button) return;
        if (enable) {
            button.classList.remove('opacity-50', 'cursor-not-allowed');
            button.setAttribute('onclick', `selectImportType('${button.id.includes('torres') ? 'torres' : 'equipamentos'}')`);
            button.title = title;
        } else {
            button.classList.add('opacity-50', 'cursor-not-allowed');
            button.removeAttribute('onclick');
            button.title = title;
        }
    };
    if (contexto === 'torres') {
        setButtonState(torresButton, true, 'Importar ou atualizar a lista de torres');
        setButtonState(equipamentosButton, false, 'É necessário importar torres primeiro.');
    } else if (contexto === 'equipamentos') {
        setButtonState(torresButton, false, 'O foco atual é a importação de equipamentos.');
        setButtonState(equipamentosButton, true, 'Importar ou atualizar os dispositivos das torres.');
    } else {
        setButtonState(torresButton, true, 'Importar ou atualizar a lista de torres');
        setButtonState(equipamentosButton, hasTorres, hasTorres ? 'Importar ou atualizar os dispositivos' : 'É necessário importar torres primeiro.');
    }
    modal.classList.remove('hidden');
    backToTypeSelection();
}

function closeImportModal() {
    document.getElementById('importModal')?.classList.add('hidden');
}

// NOVA FUNÇÃO: Fecha o modal e recarrega a página para ver os dados atualizados.
function closeImportModalAndRefresh() {
    closeImportModal();
    window.location.reload();
}

function selectImportType(type) {
    // Esta função não precisa de verificação, pois o 'onclick' é removido do elemento desativado.
    importType = type;
    document.getElementById('importTypeSelection').style.display = 'none';
    document.getElementById('importUploadArea').style.display = 'block';
    document.getElementById('uploadTitle').textContent = `Importar ${type === 'torres' ? 'Torres' : 'Equipamentos'}`;
}

function backToTypeSelection() {
    importType = '';
    document.getElementById('importTypeSelection').style.display = 'block';
    document.getElementById('importUploadArea').style.display = 'none';
    document.getElementById('importResultsArea').style.display = 'none';
    document.getElementById('finalResults').style.display = 'none';
    document.getElementById('uploadProgress').style.display = 'block';
    document.getElementById('progressFill').style.width = '0%';
}

function setupImportModalEventListeners() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('csvFileInput');
    const downloadLink = document.getElementById('downloadTemplateLink');

    if (!uploadZone || !fileInput || !downloadLink) return;

    uploadZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files));

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => uploadZone.classList.add('border-blue-500', 'bg-blue-50'), false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => uploadZone.classList.remove('border-blue-500', 'bg-blue-50'), false);
    });

    uploadZone.addEventListener('drop', (e) => handleFileSelect(e.dataTransfer.files), false);

    downloadLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (importType) {
            window.location.href = `/api/v1/import/${importType}/template`;
        }
    });
}

function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

function handleFileSelect(files) {
    const file = files[0];
    if (file && (file.type === 'text/csv' || file.name.endsWith('.csv'))) {
        startImport(file, importType);
    } else {
        alert('Por favor, selecione um ficheiro CSV válido.');
    }
}

async function startImport(file, type) {
    document.getElementById('importUploadArea').style.display = 'none';
    document.getElementById('importResultsArea').style.display = 'block';

    const formData = new FormData();
    formData.append('csv_file', file);

    const progressFill = document.getElementById('progressFill');
    progressFill.style.width = '50%';
    document.getElementById('progressText').textContent = 'A processar no servidor...';

    try {
        const response = await api.importCSV(type, formData);
        progressFill.style.width = '100%';
        setTimeout(() => showResults(response, true), 300);
    } catch (error) {
        progressFill.style.width = '100%';
        setTimeout(() => showResults(error.responseJSON || error, false), 300);
    }
}

function showResults(response, isSuccess) {
    document.getElementById('uploadProgress').style.display = 'none';
    document.getElementById('finalResults').style.display = 'block';

    const iconEl = document.getElementById('resultsIcon');
    const titleEl = document.getElementById('resultsTitle');
    const summaryEl = document.getElementById('resultsSummary');
    const detailsEl = document.getElementById('resultsDetails');
    const detailsBtn = document.getElementById('showDetailsBtn');

    if (isSuccess) {
        iconEl.innerHTML = `<i class="fas fa-check-circle fa-3x"></i>`;
        iconEl.className = 'mx-auto w-16 h-16 flex items-center justify-center rounded-full mb-4 text-green-600 bg-green-100';
        titleEl.textContent = 'Importação Concluída!';
        summaryEl.textContent = response.message || 'Dados processados com sucesso.';
        detailsEl.style.display = 'none';
        detailsBtn.style.display = 'none';
    } else {
        const errors = response.data?.detalhes_erros || response.details?.detalhes_erros || [];

        iconEl.innerHTML = `<i class="fas fa-times-circle fa-3x"></i>`;
        iconEl.className = 'mx-auto w-16 h-16 flex items-center justify-center rounded-full mb-4 text-red-600 bg-red-100';
        titleEl.textContent = 'Falha na Importação';
        summaryEl.textContent = response.message || 'Ocorreram erros durante a importação.';

        if (errors.length > 0) {
            detailsEl.innerHTML = errors.map(err =>
                `<div class="text-sm p-2 bg-red-50 border-l-4 border-red-400">
                    <strong>Linha ${err.linha}:</strong> ${err.erro}
                 </div>`
            ).join('');
            detailsBtn.style.display = 'inline-block';
        } else {
            detailsEl.innerHTML = `<div class="text-sm p-2 bg-red-50 border-l-4 border-red-400"><strong>Erro:</strong> ${response.message || 'Erro desconhecido'}</div>`;
            detailsBtn.style.display = 'none';
        }
    }
}

function toggleErrorDetails() {
    const detailsEl = document.getElementById('resultsDetails');
    detailsEl.style.display = detailsEl.style.display === 'none' ? 'block' : 'none';
}

function setupImportModalEventListeners() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('csvFileInput');
    const downloadLink = document.getElementById('downloadTemplateLink');

    if (!uploadZone || !fileInput || !downloadLink) return;

    uploadZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files));

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => { /* ... */ });
    ['dragenter', 'dragover'].forEach(eventName => { /* ... */ });
    ['dragleave', 'drop'].forEach(eventName => { /* ... */ });
    uploadZone.addEventListener('drop', (e) => handleFileSelect(e.dataTransfer.files), false);


    downloadLink.addEventListener('click', async (e) => {
        e.preventDefault();
        if (importType) {
            const originalText = downloadLink.textContent;
            downloadLink.textContent = 'A baixar...'; // Feedback para o utilizador
            downloadLink.style.pointerEvents = 'none'; // Previne cliques múltiplos

            try {
                await api.downloadTemplate(importType);
            } catch (error) {
                // Aqui você pode usar uma função de toast de erro, se tiver uma
                alert(`Falha ao baixar o template: ${error.message}`);
            } finally {
                // Restaura o link ao estado original
                downloadLink.textContent = originalText;
                downloadLink.style.pointerEvents = 'auto';
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', setupImportModalEventListeners);
console.log("Componente 'import-modal.js' carregado e pronto.");
```

### `routes\api.php`

```php
<?php
use App\Http\Route;

// ===================================================================
// ROTAS PÚBLICAS
// ===================================================================
Route::post('/api/v1/register', 'Api\AuthController@register');
Route::post('/api/v1/login', 'Api\AuthController@login');
Route::post('/api/v1/user/recuperar-senha', 'Api\UserController@recuperarSenhaPublica');

// ===================================================================
// ROTAS AUTENTICADAS
// ===================================================================

// -- Usuário --
Route::get('/api/v1/user/me', 'Api\UserController@me');
Route::put('/api/v1/user/me', 'Api\UserController@update');
Route::put('/api/v1/user/me/senha', 'Api\UserController@alterarSenha');

// -- Torres --
Route::get('/api/v1/torres', 'Api\TorreController@index');
Route::post('/api/v1/torres', 'Api\TorreController@store');
Route::get('/api/v1/torres/{id}', 'Api\TorreController@show');
Route::put('/api/v1/torres/{id}', 'Api\TorreController@update');
Route::delete('/api/v1/torres/{id}', 'Api\TorreController@destroy');
Route::get('/api/v1/torres/{id}/tempo', 'Api\TorreController@getTempo');
Route::get('/api/v1/torres/{id}/dispositivos', 'Api\TorreController@getDispositivos');

// -- Mapa -- (ESTE BLOCO ESTAVA EM FALTA)
Route::get('/api/v1/mapa/torres', 'Api\MapaController@getTorresForMap');
Route::get('/api/v1/mapa/torre/{id}', 'Api\MapaController@getTorreDetails');
Route::get('/api/v1/mapa/regioes', 'Api\MapaController@getRegioes');

// -- Dispositivos --
Route::get('/api/v1/dispositivos', 'Api\DispositivoController@index');
Route::post('/api/v1/dispositivos', 'Api\DispositivoController@store');
Route::get('/api/v1/dispositivos/{id}', 'Api\DispositivoController@show');
Route::put('/api/v1/dispositivos/{id}', 'Api\DispositivoController@update');
Route::delete('/api/v1/dispositivos/{id}', 'Api\DispositivoController@destroy');

// -- Eventos --
Route::get('/api/v1/dispositivos/{id}/eventos', 'Api\EventoController@index');
Route::post('/api/v1/dispositivos/{id}/eventos', 'Api\EventoController@store');

// -- Lookups (dados auxiliares) --
Route::get('/api/v1/lookup/tipos-dispositivo', 'Api\LookupController@getTiposDispositivo');
Route::get('/api/v1/lookup/status-tipos', 'Api\LookupController@getStatusTipos');
Route::get('/api/v1/lookup/tipos-evento', 'Api\LookupController@getTiposEvento');
Route::get('/api/v1/lookup/motivos-falha', 'Api\LookupController@getMotivosFalha');

// -- Dashboard --
Route::get('/api/v1/dashboard/kpis', 'Api\DashboardController@getKpis');
Route::get('/api/v1/dashboard/dispositivos-status', 'Api\DashboardController@getDispositivosStatus');
Route::get('/api/v1/dashboard/dispositivos-tipos', 'Api\DashboardController@getDispositivosTipos');
Route::get('/api/v1/dashboard/torres-criticas', 'Api\DashboardController@getTorresCriticas');
Route::get('/api/v1/dashboard/visao-geral-torres', 'Api\DashboardController@getVisaoGeralTorres');

// -- Importação --
Route::post('/api/v1/import/torres', 'Api\ImportController@importTorres');
Route::post('/api/v1/import/equipamentos', 'Api\ImportController@importEquipamentos');
Route::get('/api/v1/import/torres/template', 'Api\ImportController@downloadTorresTemplate');
Route::get('/api/v1/import/equipamentos/template', 'Api\ImportController@downloadEquipamentosTemplate');
```

### `routes\web.php`

```php
<?php
use App\Http\Route;

// =================================================
// ROTAS PÚBLICAS (NÃO EXIGEM LOGIN)
// =================================================
Route::get('/', 'Web\HomeController@index');
Route::get('/login', 'Web\AuthController@showLoginForm');
Route::get('/register', 'Web\AuthController@showRegisterForm');

// =================================================
// ROTAS DO PAINEL (EXIGEM LOGIN)
// =================================================
Route::get('/dashboard', 'Web\DashboardController@index');
Route::get('/mapa', 'Web\MapaController@index'); 
Route::get('/torres', 'Web\TorresController@index');
Route::get('/configuracoes', 'Web\ConfiguracoesController@index');
```

### `scripts\seed.php`

```php
<?php

// Garante que o script seja executado a partir da raiz do projeto
if (file_exists('vendor/autoload.php')) {
    require 'vendor/autoload.php';
} else {
    // Se executado de dentro da pasta scripts/
    require __DIR__ . '/../vendor/autoload.php';
}

use App\Models\Usuario;
use App\Services\AuthService;
use Dotenv\Dotenv;

// Carrega as variáveis de ambiente
$dotenv = Dotenv::createImmutable(__DIR__ . '/..');
$dotenv->load();

echo "========================================\n";
echo "==      INICIANDO SEED DO BANCO       ==\n";
echo "========================================\n";

// Dados do usuário administrador (CORRIGIDO)
$adminData = [
    'primeiro_nome' => 'Administrador',
    'ultimo_nome' => 'Sistema',
    'celular' => '00000000000', // Campo obrigatório
    'email' => 'admin@brdk.com.br',
    'senha' => 'admin123'
];

try {
    echo "Verificando se o usuário administrador já existe...\n";
    $user = Usuario::findByEmail($adminData['email']);

    if ($user) {
        echo "Usuário administrador já existe. Nenhum usuário foi criado.\n";
    } else {
        echo "Criando usuário administrador...\n";
        $authService = new AuthService();
        $result = $authService->register($adminData);

        // Lógica de tratamento de erro (CORRIGIDA)
        if (isset($result['error'])) {
            echo "ERRO AO CRIAR USUÁRIO:\n";
            $errorMessage = $result['error'];
            if (isset($result['details'])) {
                $validationErrors = [];
                foreach ($result['details'] as $field => $msg) {
                    $validationErrors[] = "{$field}: {$msg}";
                }
                $errorMessage .= " (" . implode(', ', $validationErrors) . ")";
            }
            echo $errorMessage . "\n";
        } else {
            // Este bloco só é executado em caso de sucesso
            echo "Usuário administrador criado com sucesso!\n";
        }
    }
} catch (Exception $e) {
    echo "ERRO CRÍTICO NO PROCESSO DE SEED: " . $e->getMessage() . "\n";
}

echo "\nProcesso de seed finalizado.\n";
```

### `scripts\test_improvements.php`

```php
<?php
require_once __DIR__ . '/../vendor/autoload.php';

echo "🧪 TESTANDO MELHORIAS NA API\n";
echo "==============================\n\n";

// Teste 1: Login com dados válidos  
echo "📝 Teste 1: Login válido\n";
$response = file_get_contents('http://localhost:8000/api/v1/login', false, stream_context_create([
    'http' => [
        'method' => 'POST',
        'header' => [
            'Content-Type: application/json',
            'Accept: application/json'
        ],
        'content' => json_encode([
            'email' => 'admin@brdk.com.br',
            'senha' => 'admin123'
        ])
    ]
]));

echo "Resposta: " . $response . "\n\n";

// Teste 2: Validação de campos obrigatórios
echo "📝 Teste 2: Validação (campos vazios)\n";
$response = file_get_contents('http://localhost:8000/api/v1/login', false, stream_context_create([
    'http' => [
        'method' => 'POST',
        'header' => [
            'Content-Type: application/json',
            'Accept: application/json'
        ],
        'content' => json_encode([
            'email' => '',
            'senha' => ''
        ])
    ]
]));

echo "Resposta: " . $response . "\n\n";

echo "✅ Testes concluídos!\n";
?>
```

### `src\Controllers\Api\AuthController.php`

```php
<?php
namespace App\Controllers\Api;

use App\Http\Request;
use App\Http\Response;
use App\Services\AuthService;
use Exception;

class AuthController
{
    /** @var AuthService */
    private AuthService $authService;

    public function __construct()
    {
        $this->authService = new AuthService();
    }

    /**
     * Endpoint para registar um novo usuário.
     * Recebe os dados via POST e passa para o AuthService.
     */
    public function register(): void
    {
        try {
            $body = Request::body();
            $result = $this->authService->register($body);

            if (isset($result['error'])) {
                Response::error($result['error'], $result['status'], $result['details'] ?? []);
            } else {
                Response::success($result['data'], $result['message'], $result['status']);
            }
        } catch (Exception $e) {
            // Log de erro real para o servidor, não para o usuário.
            error_log("Erro crítico no AuthController@register: " . $e->getMessage());
            Response::error('Erro interno do servidor', 500);
        }
    }

    /**
     * Endpoint para autenticar um usuário.
     * Recebe as credenciais via POST e retorna um token JWT.
     */
    public function login(): void
    {
        try {
            $body = Request::body();
            $result = $this->authService->login($body);

            if (isset($result['error'])) {
                if ($result['status'] === 422) {
                    Response::validationError($result['details']);
                } else {
                    Response::error($result['error'], $result['status']);
                }
            } else {
                Response::success(['token' => $result['token']], 'Login realizado com sucesso', $result['status']);
            }
        } catch (Exception $e) {
            error_log("Erro crítico no AuthController@login: " . $e->getMessage());
            Response::error('Erro interno do servidor', 500);
        }
    }
}
```

### `src\Controllers\Api\DashboardController.php`

```php
<?php
namespace App\Controllers\Api;

use App\Http\Response;
use App\Services\DashboardService;
use Exception;

class DashboardController
{
    private DashboardService $dashboardService;

    public function __construct()
    {
        // NOTA: A autenticação (AuthMiddleware::handle()) foi removida daqui
        // e colocada em cada método para seguir o padrão dos outros controllers.
        $this->dashboardService = new DashboardService();
    }

    /**
     * Endpoint para buscar os dados dos KPIs.
     * @return void
     */
    public function getKpis(): void
    {
        \App\Middleware\AuthMiddleware::handle();
        try {
            $kpis = $this->dashboardService->getKpiStatistics();
            Response::success($kpis, 'KPIs do dashboard carregados com sucesso.');
        } catch (Exception $e) {
            Response::error('Erro interno ao buscar os KPIs do dashboard.', 500);
        }
    }

    /**
     * Endpoint para buscar o status dos dispositivos (online/offline).
     * @return void
     */
    public function getDispositivosStatus(): void
    {
        \App\Middleware\AuthMiddleware::handle();
        try {
            $stats = $this->dashboardService->getStatusDispositivos();
            Response::success($stats, 'Status de dispositivos carregado com sucesso.');
        } catch (Exception $e) {
            Response::error('Erro interno ao buscar status de dispositivos.', 500);
        }
    }

    /**
     * Endpoint para buscar o inventário de dispositivos por tipo.
     * @return void
     */
    public function getDispositivosTipos(): void
    {
        \App\Middleware\AuthMiddleware::handle();
        try {
            $stats = $this->dashboardService->getTiposDispositivosCount();
            Response::success($stats, 'Inventário de dispositivos carregado com sucesso.');
        } catch (Exception $e) {
            Response::error('Erro interno ao buscar inventário de dispositivos.', 500);
        }
    }

    /**
     * Endpoint para buscar a lista de torres mais críticas.
     * @return void
     */
    public function getTorresCriticas(): void
    {
        \App\Middleware\AuthMiddleware::handle();
        try {
            $torres = $this->dashboardService->getTorresCriticas();
            Response::success($torres, 'Torres críticas carregadas com sucesso.');
        } catch (Exception $e) {
            Response::error('Erro interno ao buscar torres críticas.', 500);
        }
    }

    /**
     * Endpoint para buscar dados da tabela de visão geral de torres.
     * @return void
     */
    public function getVisaoGeralTorres(): void
    {
        \App\Middleware\AuthMiddleware::handle();
        try {
            $torres = $this->dashboardService->getVisaoGeralTorres();
            Response::success($torres, 'Visão geral das torres carregada com sucesso.');
        } catch (Exception $e) {
            Response::error('Erro interno ao buscar visão geral das torres.', 500);
        }
    }
}
```

### `src\Controllers\Api\DispositivoController.php`

```php
<?php

namespace App\Controllers\Api;

use App\Http\Request;
use App\Http\Response;
use App\Services\DispositivoService;
use Exception;

/**
 * Controller para gerir a interação HTTP com o recurso de Dispositivos.
 */
class DispositivoController
{
    private DispositivoService $dispositivoService;

    public function __construct(DispositivoService $dispositivoService)
    {
        $this->dispositivoService = $dispositivoService;
    }

    public function index(): void
    {
        try {
            $dispositivos = $this->dispositivoService->getAll();
            Response::success($dispositivos, 'Dispositivos listados com sucesso.');
        } catch (Exception $e) {
            Response::error('Erro ao buscar dispositivos.', 500);
        }
    }

    public function show(int $id): void
    {
        try {
            $dispositivo = $this->dispositivoService->getById($id);
            if (!$dispositivo) {
                Response::error('Dispositivo não encontrado.', 404);
                return;
            }
            Response::success($dispositivo, 'Dispositivo encontrado com sucesso.');
        } catch (Exception $e) {
            Response::error('Erro ao buscar dispositivo.', 500);
        }
    }

    public function store(): void
    {
        try {
            $body = Request::body();
            $novoDispositivo = $this->dispositivoService->create($body);
            Response::success($novoDispositivo, 'Dispositivo criado com sucesso.', 201);
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            $errors = json_decode($e->getMessage(), true);
            if (json_last_error() === JSON_ERROR_NONE) {
                 Response::error('Erro de validação', 422, $errors);
            } else {
                 Response::error($e->getMessage(), $code);
            }
        }
    }

    public function update(int $id): void
    {
        try {
            $body = Request::body();
            $dispositivoAtualizado = $this->dispositivoService->update($id, $body);
            Response::success($dispositivoAtualizado, 'Dispositivo atualizado com sucesso.');
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            Response::error($e->getMessage(), $code);
        }
    }

    public function destroy(int $id): void
    {
        try {
            $this->dispositivoService->delete($id);
            Response::success(null, 'Dispositivo removido com sucesso.', 204);
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            Response::error($e->getMessage(), $code);
        }
    }
}
```

### `src\Controllers\Api\EventoController.php`

```php
<?php

namespace App\Controllers\Api;

use App\Http\Request;
use App\Http\Response;
use App\Services\EventoService;
use Exception;

/**
 * Controller para gerir a interação HTTP com o recurso de Eventos.
 */
class EventoController
{
    private EventoService $eventoService;

    public function __construct(EventoService $eventoService)
    {
        $this->eventoService = $eventoService;
    }

    /**
     * Lista todos os eventos de um dispositivo específico.
     * GET /api/v1/dispositivos/{id}/eventos
     */
    public function index(int $dispositivoId): void
    {
        try {
            $eventos = $this->eventoService->getEventosByDispositivoId($dispositivoId);
            Response::success($eventos, 'Eventos carregados com sucesso.');
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            Response::error($e->getMessage(), $code);
        }
    }

    /**
     * Regista um novo evento para um dispositivo específico.
     * POST /api/v1/dispositivos/{id}/eventos
     */
    public function store(int $dispositivoId): void
    {
        try {
            $body = Request::body();
            $novoEvento = $this->eventoService->createEvento($dispositivoId, $body);
            Response::success($novoEvento, 'Evento registado com sucesso.', 201);
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            $errors = json_decode($e->getMessage(), true);
            if (json_last_error() === JSON_ERROR_NONE) {
                 Response::error('Erro de validação', 422, $errors);
            } else {
                 Response::error($e->getMessage(), $code);
            }
        }
    }
}
```

### `src\Controllers\Api\ImportController.php`

```php
<?php
namespace App\Controllers\Api;

use App\Http\Request;
use App\Http\Response;
use App\Middleware\AuthMiddleware;
use App\Services\ImportService;

class ImportController
{
    private ImportService $importService;

    public function __construct()
    {
        $this->importService = new ImportService();
    }

    /**
     * Importar torres via CSV
     * POST /api/v1/import/torres
     */
    public function importTorres(): void
    {
        AuthMiddleware::handle();

        try {
            // Verificar se arquivo foi enviado
            if (!isset($_FILES['csv_file']) || $_FILES['csv_file']['error'] !== UPLOAD_ERR_OK) {
                Response::error('Arquivo CSV não foi enviado corretamente', 400);
                return;
            }

            $uploadedFile = $_FILES['csv_file'];

            // Validações básicas do arquivo
            $validationErrors = $this->validateUploadedFile($uploadedFile, 'torres');
            if (!empty($validationErrors)) {
                Response::error('Arquivo inválido', 400, $validationErrors);
                return;
            }

            // Ler conteúdo do arquivo
            $csvContent = file_get_contents($uploadedFile['tmp_name']);
            if ($csvContent === false) {
                Response::error('Erro ao ler arquivo CSV', 500);
                return;
            }

            // Processar CSV
            try {
                $csvData = $this->importService->processCSV($csvContent);
            } catch (\Exception $e) {
                Response::error('Erro ao processar CSV: ' . $e->getMessage(), 400);
                return;
            }

            // Validar estrutura do CSV
            $structureErrors = $this->importService->validateTorresCSV($csvData);
            if (!empty($structureErrors)) {
                Response::error('Estrutura do CSV inválida', 400, $structureErrors);
                return;
            }

            // Executar importação
            $results = $this->importService->importTorres($csvData);

            // Preparar resposta detalhada
            $message = $this->buildImportMessage($results, 'torres');

            if ($results['success']) {
                Response::success($results, $message, 200);
            } else {
                Response::error($message, 422, $results);
            }

        } catch (\Exception $e) {
            error_log("Erro na importação de torres: " . $e->getMessage());
            Response::error('Erro interno durante a importação', 500);
        }
    }

    /**
     * Importar equipamentos via CSV
     * POST /api/v1/import/equipamentos
     */
    public function importEquipamentos(): void
    {
        AuthMiddleware::handle();

        try {
            // Verificar se arquivo foi enviado
            if (!isset($_FILES['csv_file']) || $_FILES['csv_file']['error'] !== UPLOAD_ERR_OK) {
                Response::error('Arquivo CSV não foi enviado corretamente', 400);
                return;
            }

            $uploadedFile = $_FILES['csv_file'];

            // Validações básicas do arquivo
            $validationErrors = $this->validateUploadedFile($uploadedFile, 'equipamentos');
            if (!empty($validationErrors)) {
                Response::error('Arquivo inválido', 400, $validationErrors);
                return;
            }

            // Ler conteúdo do arquivo
            $csvContent = file_get_contents($uploadedFile['tmp_name']);
            if ($csvContent === false) {
                Response::error('Erro ao ler arquivo CSV', 500);
                return;
            }

            // Processar CSV
            try {
                $csvData = $this->importService->processCSV($csvContent);
            } catch (\Exception $e) {
                Response::error('Erro ao processar CSV: ' . $e->getMessage(), 400);
                return;
            }

            // Validar estrutura do CSV
            $structureErrors = $this->importService->validateEquipamentosCSV($csvData);
            if (!empty($structureErrors)) {
                Response::error('Estrutura do CSV inválida', 400, $structureErrors);
                return;
            }

            // Executar importação
            $results = $this->importService->importEquipamentos($csvData);

            // Preparar resposta detalhada
            $message = $this->buildImportMessage($results, 'equipamentos');

            if ($results['success']) {
                Response::success($results, $message, 200);
            } else {
                Response::error($message, 422, $results);
            }

        } catch (\Exception $e) {
            error_log("Erro na importação de equipamentos: " . $e->getMessage());
            Response::error('Erro interno durante a importação', 500);
        }
    }

    /**
     * Validar arquivo enviado
     */
    private function validateUploadedFile(array $file, string $type): array
    {
        $errors = [];

        // Verificar tamanho do arquivo (máximo 5MB)
        $maxSize = 5 * 1024 * 1024; // 5MB
        if ($file['size'] > $maxSize) {
            $errors[] = 'Arquivo muito grande. Tamanho máximo: 5MB';
        }

        // Verificar tipo MIME
        $allowedMimes = ['text/csv', 'text/plain', 'application/csv', 'application/excel'];
        $fileMime = mime_content_type($file['tmp_name']);

        if (!in_array($fileMime, $allowedMimes)) {
            // Verificar também pela extensão como fallback
            $fileName = $file['name'];
            $extension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

            if ($extension !== 'csv') {
                $errors[] = 'Apenas arquivos CSV são aceitos';
            }
        }

        // Verificar se o arquivo não está vazio
        if ($file['size'] == 0) {
            $errors[] = 'Arquivo está vazio';
        }

        return $errors;
    }

    /**
     * Construir mensagem detalhada de resultado da importação
     */
    private function buildImportMessage(array $results, string $type): string
    {
        if (!$results['success']) {
            return "Falha na importação de $type";
        }

        $parts = [];

        if ($type === 'torres') {
            if ($results['adicionadas'] > 0) {
                $parts[] = "{$results['adicionadas']} torres adicionadas";
            }
            if ($results['atualizadas'] > 0) {
                $parts[] = "{$results['atualizadas']} torres atualizadas";
            }
        } else {
            if ($results['adicionadas'] > 0) {
                $parts[] = "{$results['adicionadas']} equipamentos adicionados";
            }
            if ($results['atualizadas'] > 0) {
                $parts[] = "{$results['atualizadas']} equipamentos atualizados";
            }
            if ($results['torres_criadas'] > 0) {
                $parts[] = "{$results['torres_criadas']} torres criadas automaticamente";
            }
            if ($results['tipos_criados'] > 0) {
                $parts[] = "{$results['tipos_criados']} tipos de equipamento criados";
            }
        }

        if ($results['erros'] > 0) {
            $parts[] = "{$results['erros']} erros encontrados";
        }

        $message = "Importação concluída: " . implode(', ', $parts);

        return $message;
    }

    /**
     * Download de template CSV para torres
     * GET /api/v1/import/torres/template
     */
    public function downloadTorresTemplate(): void
    {
        AuthMiddleware::handle();

        $csvContent = "nome;localizacao;latitude;longitude;observacoes;depende_de_torre_id\n";
        $csvContent .= "Torre Matriz SP;São Paulo - Centro;-23.550520;-46.633308;Torre principal do escritório de SP;\n"; // depende_de_torre_id vazio
        $csvContent .= "Torre Filial RJ;Rio de Janeiro - Copacabana;-22.969778;-43.186859;Torre da filial com link de backup;1\n"; // Exemplo: depende da Torre Matriz (ID 1)

        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename="template_torres.csv"');
        header('Cache-Control: no-cache, must-revalidate');

        echo $csvContent;
        exit;
    }

    /**
     * Download de template CSV para equipamentos
     * GET /api/v1/import/equipamentos/template
     */
    public function downloadEquipamentosTemplate(): void
    {
        AuthMiddleware::handle();

        $csvContent = "torre;nome;ip\n";
        $csvContent .= "Torre Matriz SP;SWITCH-CORE-01;192.168.1.1\n";
        $csvContent .= "Torre Matriz SP;ROUTER-BORDA-01;192.168.1.254\n";
        $csvContent .= "Torre Filial RJ;PTP-RJ-SP-LADO-B;10.10.20.2\n";

        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename="template_equipamentos.csv"');

        echo $csvContent;
        exit;
    }
}
?>
```

### `src\Controllers\Api\LookupController.php`

```php
<?php
namespace App\Controllers\Api;

use App\Http\Response;
use App\Middleware\AuthMiddleware;
use App\Models\MotivoFalha;
use App\Models\StatusTipo;
use App\Models\TipoDispositivo;
use App\Models\TipoEvento;

class LookupController
{
    /**
     * Retorna a lista de todos os tipos de dispositivo.
     * @return void
     */
    public function getTiposDispositivo(): void
    {
        AuthMiddleware::handle();
        $data = TipoDispositivo::findAll();
        Response::success($data, 'Tipos de dispositivo carregados com sucesso.');
    }

    /**
     * Retorna a lista de todos os tipos de status.
     * @return void
     */
    public function getStatusTipos(): void
    {
        AuthMiddleware::handle();
        $data = StatusTipo::findAll();
        Response::success($data, 'Tipos de status carregados com sucesso.');
    }

    /**
     * Retorna a lista de todos os tipos de evento.
     * @return void
     */
    public function getTiposEvento(): void
    {
        AuthMiddleware::handle();
        $data = TipoEvento::findAll();
        Response::success($data, 'Tipos de evento carregados com sucesso.');
    }

    /**
     * Retorna a lista de todos os motivos de falha.
     * @return void
     */
    public function getMotivosFalha(): void
    {
        AuthMiddleware::handle();
        $data = MotivoFalha::findAll();
        Response::success($data, 'Motivos de falha carregados com sucesso.');
    }
}
```

### `src\Controllers\Api\MapaController.php`

```php
<?php
namespace App\Controllers\Api;

use App\Services\MapaService;
use App\Http\Response;
use App\Http\Request;
use App\Middleware\AuthMiddleware;

class MapaController
{
    private MapaService $mapaService;

    public function __construct()
    {
        $this->mapaService = new MapaService();
    }

    // GET /api/v1/mapa/torres
    public function getTorresForMap(): void
    {
        AuthMiddleware::handle();

        try {
            $torres = $this->mapaService->getTorresComCoordenadas();
            Response::success($torres, "Torres para o mapa carregadas");
        } catch (\Exception $e) {
            error_log("Erro ao carregar torres para mapa: " . $e->getMessage());
            Response::error("Erro ao carregar dados do mapa", 500);
        }
    }

    // GET /api/v1/mapa/torre/{id}
    public function getTorreDetails(int $id): void
    {
        AuthMiddleware::handle();

        try {
            $detalhes = $this->mapaService->getDetalhesTorre($id);

            if (isset($detalhes['error'])) {
                Response::error($detalhes['error'], $detalhes['status']);
                return;
            }

            // CORREÇÃO: remover ['data'] se existir
            Response::success($detalhes, "Detalhes da torre carregados");
        } catch (\Exception $e) {
            error_log("Erro ao carregar detalhes da torre: " . $e->getMessage());
            Response::error("Erro ao carregar detalhes", 500);
        }
    }

    /**
     * Retorna a lista de regiões para os filtros.
     * GET /api/v1/mapa/regioes
     */
    public function getRegioes(): void
    {
        AuthMiddleware::handle();
        try {
            $regioes = $this->mapaService->getRegioesDisponiveis();
            Response::success($regioes, "Regiões carregadas");
        } catch (\Exception $e) {
            Response::error("Erro ao carregar regiões", 500);
        }
    }
}
```

### `src\Controllers\Api\TorreController.php`

```php
<?php

namespace App\Controllers\Api;

use App\Services\TorreService;
use App\Http\Request;
use App\Http\Response;
use App\Middleware\AuthMiddleware;
use Exception;

/**
 * Controller para gerir a interação HTTP com o recurso de Torres.
 *
 * É a camada mais externa, responsável por:
 * - Receber a requisição.
 * - Chamar a camada de Serviço.
 * - Formatar a resposta HTTP (sucesso ou erro).
 * - Capturar exceções da camada de serviço.
 *
 * NÃO contém lógica de negócio.
 */
class TorreController
{
    private TorreService $torreService;

    /**
     * O construtor recebe a dependência do TorreService.
     */
    public function __construct(TorreService $torreService)
    {
        $this->torreService = $torreService;
        // O AuthMiddleware será chamado no roteador, antes de chegar ao controller.
    }

    /**
     * Lista todas as torres.
     * GET /api/v1/torres
     */
    public function index(): void
    {
        try {
            $torres = $this->torreService->getAllTorres();
            Response::success($torres, count($torres) . ' torres encontradas');
        } catch (Exception $e) {
            error_log("Erro em TorreController::index(): " . $e->getMessage());
            Response::error('Erro ao buscar torres.', 500);
        }
    }

    /**
     * Busca uma torre específica pelo seu ID.
     * GET /api/v1/torres/{id}
     */
    public function show(int $id): void
    {
        try {
            $torre = $this->torreService->getTorreById($id);
            if (!$torre) {
                Response::error('Torre não encontrada', 404);
                return;
            }
            Response::success($torre, 'Torre encontrada');
        } catch (Exception $e) {
            error_log("Erro em TorreController::show($id): " . $e->getMessage());
            Response::error('Erro ao buscar torre.', 500);
        }
    }

    /**
     * Cria uma nova torre.
     * POST /api/v1/torres
     */
    public function store(): void
    {
        try {
            $body = Request::body();
            $novaTorre = $this->torreService->createTorre($body);
            Response::success($novaTorre, 'Torre criada com sucesso', 201);
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            // Tenta decodificar a mensagem de erro, caso seja um JSON de validação
            $errors = json_decode($e->getMessage(), true);
            if (json_last_error() === JSON_ERROR_NONE) {
                 Response::error('Erro de validação', 422, $errors);
            } else {
                 Response::error($e->getMessage(), $code);
            }
        }
    }

    /**
     * Atualiza uma torre existente.
     * PUT /api/v1/torres/{id}
     */
    public function update(int $id): void
    {
        try {
            $body = Request::body();
            $torreAtualizada = $this->torreService->updateTorre($id, $body);
            Response::success($torreAtualizada, 'Torre atualizada com sucesso');
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            Response::error($e->getMessage(), $code);
        }
    }

    /**
     * Remove uma torre.
     * DELETE /api/v1/torres/{id}
     */
    public function destroy(int $id): void
    {
        try {
            $this->torreService->deleteTorre($id);
            Response::success(null, 'Torre removida com sucesso', 204);
        } catch (Exception $e) {
            $code = $e->getCode() >= 400 ? $e->getCode() : 500;
            Response::error($e->getMessage(), $code);
        }
    }
}
```

### `src\Controllers\Api\UserController.php`

```php
<?php
namespace App\Controllers\Api;

use App\Http\Request;
use App\Http\Response;
use App\Middleware\AuthMiddleware;
use App\Models\Usuario;
use App\Services\UserService;

class UserController
{
    private UserService $userService;

    public function __construct()
    {
        $this->userService = new UserService();
    }

    public function me(): void
    {
        AuthMiddleware::handle();
        $userId = AuthMiddleware::getUserId();
        if (!$userId) { Response::unauthorized(); return; }

        $user = Usuario::findById($userId);
        if (!$user) { Response::notFound('Usuário'); return; }

        $userData = [
            'id' => (int) $user['id'],
            'nome' => trim(($user['primeiro_nome'] ?? '') . ' ' . ($user['ultimo_nome'] ?? '')),
            'email' => $user['email'] ?? '',
            'celular' => $user['celular'] ?? ''
        ];
        Response::success($userData, 'Dados carregados');
    }

    public function update(): void
    {
        AuthMiddleware::handle();
        $userId = AuthMiddleware::getUserId();
        if (!$userId) { Response::unauthorized(); return; }
        
        $data = Request::body();
        if (empty($data)) { Response::error('Nenhum dado fornecido', 400); return; }

        $result = $this->userService->update($userId, $data);

        if (isset($result['error'])) {
             Response::error($result['error'], $result['status'] ?? 422, $result['details'] ?? []);
        } else {
             Response::success([], $result['message'] ?? 'Usuário atualizado com sucesso');
        }
    }

    public function alterarSenha(): void
    {

        // 1. Valida o token da requisição primeiro
        AuthMiddleware::handle();

        // 2. Só depois de validar, pega o ID do usuário
        $userId = AuthMiddleware::getUserId();
        
        if (!$userId) {
            Response::unauthorized();
            return;
        }

        $body = Request::body();
        $result = $this->userService->alterarSenha($userId, $body);

        if (isset($result['error'])) {
            Response::error($result['error'], $result['status'], $result['details'] ?? []);
        } else {
            Response::success([], $result['message'], $result['status']);
        }
    }

    public function recuperarSenhaPublica(): void
    {
        $body = Request::body();
        $result = $this->userService->recuperarSenhaPublica($body);

        if (isset($result['error'])) {
            Response::error($result['error'], $result['status'], $result['details'] ?? []);
        } else {
            Response::success([], $result['message'], $result['status']);
        }
    }
}
```

### `src\Controllers\Web\AuthController.php`

```php
<?php

namespace App\Controllers\Web;

use App\Core\View;

class AuthController
{
    /**
     * Mostra a página com o formulário de login.
     */
    public function showLoginForm(): void
    {
        // Define o layout como null para não usar o layout do dashboard
        View::$layout = null; 
        View::make('auth/login', ['title' => 'Login - BRDK Monitor']);
    }

    /**
     * Mostra a página com o formulário de registo.
     */
    public function showRegisterForm(): void
    {
        View::$layout = null;
        View::make('auth/register', ['title' => 'Registo - BRDK Monitor']);
    }
}
```

### `src\Controllers\Web\ConfiguracoesController.php`

```php
<?php
namespace App\Controllers\Web;

use App\Core\View;

class ConfiguracoesController
{
    public function index(): void
    {
        $data = [
            'title' => 'Configurações - BRDK Monitoramento',
            'page' => 'configuracoes',
            'pageScript' => '/assets/js/configuracoes.js'
        ];

        View::make('configuracoes/index', $data);
    }
}
```

### `src\Controllers\Web\DashboardController.php`

```php
<?php
namespace App\Controllers\Web;

use App\Core\View;

class DashboardController
{
    /**
     * Exibe a página principal do dashboard.
     *
     * @return void
     */
    public function index(): void
    {
        $data = [
            'title' => 'Dashboard',
            'page' => 'dashboard', // Usado para destacar o item no menu lateral
            'pageScript' => '/assets/js/dashboard.js' // Script JS específico da página
        ];

        View::make('dashboard/index', $data);
    }
}
```

### `src\Controllers\Web\HomeController.php`

```php
<?php

namespace App\Controllers\Web;

class HomeController
{
    /**
     * Redireciona o utilizador da página raiz para a página de login.
     */
    public function index(): void
    {
        header('Location: /login');
        exit;
    }
}
```

### `src\Controllers\Web\MapaController.php`

```php
<?php
namespace App\Controllers\Web;

use App\Core\View;

class MapaController
{
    /**
     * Exibe a página do mapa de torres.
     *
     * @return void
     */
    public function index(): void
    {
        $data = [
            'title' => 'Mapa de Torres',
            'page' => 'mapa',
            'pageScript' => '/assets/js/mapa.js'
        ];

        View::make('mapa/index', $data);
    }
}
```

### `src\Controllers\Web\TorresController.php`

```php
<?php
namespace App\Controllers\Web;

use App\Core\View;

class TorresController
{
    /**
     * Exibe a página de gestão de torres.
     *
     * @return void
     */
    public function index(): void
    {
        $data = [
            'title' => 'Gestão de Torres',
            'page' => 'torres',
            'pageScript' => '/assets/js/torres.js'
        ];

        View::make('torres/index', $data);
    }
}
```

### `src\Core\Core.php`

```php
<?php
namespace App\Core;

class Core
{
    public static function dispatch(array $routes): void
    {
        $method = $_SERVER['REQUEST_METHOD'];
        $uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

        foreach ($routes as $route) {
            if ($route['method'] !== $method) {
                continue;
            }

            // A lógica de 'type' => 'web' foi removida.
            // Agora, TODAS as rotas chamam um Controller.
            if (self::matchRoute($route['path'], $uri, $params)) {
                self::executeAction($route['action'], $params);
                return;
            }
        }

        http_response_code(404);
        echo "<h1>404 - Página Não Encontrada</h1>";
        error_log("❌ Rota não encontrada: $method $uri");
    }

    private static function matchRoute(string $routePath, string $requestPath, &$params): bool
    {
        $params = [];

        error_log("🔍 Comparando: '$routePath' com '$requestPath'");

        // Rota exata
        if ($routePath === $requestPath) {
            error_log("✅ Match exato!");
            return true;
        }

        // Rota com parâmetros {id}
        $routePattern = preg_replace('/\{([^}]+)\}/', '([^/]+)', $routePath);
        $routePattern = '#^' . $routePattern . '$#';

        error_log("🔍 Pattern gerado: $routePattern");

        if (preg_match($routePattern, $requestPath, $matches)) {
            array_shift($matches); // Remove match completo

            // Extrair nomes dos parâmetros
            preg_match_all('/\{([^}]+)\}/', $routePath, $paramNames);

            foreach ($matches as $index => $value) {
                $paramName = $paramNames[1][$index] ?? $index;
                $params[$paramName] = $value;
                error_log("📋 Parâmetro capturado: $paramName = $value");
            }

            error_log("✅ Match com parâmetros!");
            return true;
        }

        return false;
    }

    private static function executeAction(string $action, array $params): void
    {
        try {
            error_log("🚀 Executando action: $action");
            error_log("🚀 Parâmetros: " . json_encode($params));

            // Parse Controller@method
            [$controllerName, $method] = explode('@', $action);

            // Namespace correto (SEM duplo escape)
            $controllerClass = "App\\Controllers\\$controllerName";

            error_log("🎯 Controller class: $controllerClass");
            error_log("🎯 Method: $method");

            if (!class_exists($controllerClass)) {
                throw new \Exception("Controller $controllerClass não encontrado");
            }

            // ================= INJEÇÃO DE DEPENDÊNCIA =================
            $controller = self::buildController($controllerClass);
            // ========================================================

            if (!method_exists($controller, $method)) {
                throw new \Exception("Método $method não encontrado no controller $controllerClass");
            }

            // Executar método com parâmetros
            if (!empty($params)) {
                // Se há parâmetro 'id', converter para int
                if (isset($params['id']) && is_numeric($params['id'])) {
                    error_log("📋 Passando ID como int: {$params['id']}");
                    $controller->$method((int) $params['id']);
                } else {
                    error_log("📋 Passando parâmetros: " . implode(', ', $params));
                    $controller->$method(...array_values($params));
                }
            } else {
                error_log("📋 Executando sem parâmetros");
                $controller->$method();
            }

            error_log("✅ Action executada com sucesso");

        } catch (\Throwable $e) {
            error_log("❌ Erro ao executar action: " . $e->getMessage());
            error_log("❌ Stack trace: " . $e->getTraceAsString());

            http_response_code(500);
            header('Content-Type: application/json');
            echo json_encode([
                'success' => false,
                'message' => 'Erro interno do servidor',
                'error' => $e->getMessage(),
                'controller' => $controllerClass ?? 'N/A',
                'method' => $method ?? 'N/A'
            ], JSON_PRETTY_PRINT);
        }
    }

    private static function renderView(string $viewPath, array $data = []): void
    {
        // A CORREÇÃO ESTÁ NA LINHA ABAIXO
        $filePath = __DIR__ . '/../../views/' . $viewPath . '.php';

        if (file_exists($filePath)) {
            extract($data);

            ob_start();
            require_once $filePath;
            $content = ob_get_clean();

            require_once __DIR__ . '/../../views/layouts/app.php';
        } else {
            http_response_code(404);
            // Adicionamos o caminho para ajudar a depurar no futuro
            echo "Página não encontrada (view file missing at: {$filePath})";
        }
    }

    /**
     * Constrói o controller com suas dependências (Container de DI simples).
     *
     * @param string $controllerClass O nome da classe do controller.
     * @return object A instância do controller.
     */
    private static function buildController(string $controllerClass): object
    {
        // Dependência base
        $pdo = \App\Models\Database::getInstance();

        // Extrai o nome base do controller (ex: 'TorreController')
        $baseName = substr($controllerClass, strrpos($controllerClass, '\\') + 1);
        $entityName = str_replace('Controller', '', $baseName); // ex: 'Torre'

        // Nomes das classes de Repository e Service
        $repoClass = "App\\Repositories\\{$entityName}Repository";
        $serviceClass = "App\\Services\\{$entityName}Service";

        // Verifica se as classes de dependência existem
        if (class_exists($repoClass) && class_exists($serviceClass)) {
            // "Fiação" das dependências
            $repository = new $repoClass($pdo);
            $service = new $serviceClass($repository);
            return new $controllerClass($service);
        }

        // Fallback para controllers sem a arquitetura completa (ex: AuthController)
        // Tenta instanciar com o service se ele existir
        if (class_exists($serviceClass)) {
             $service = new $serviceClass(); // Assumindo que o service pode não ter repo
             return new $controllerClass($service);
        }
        
        // Fallback para controllers sem dependências
        return new $controllerClass();
    }
}
```

### `src\Core\Validator.php`

```php
<?php

namespace App\Core;

class Validator
{
    private static array $errors = [];

    /**
     * Valida um conjunto de dados com base num conjunto de regras.
     * @param array $data Os dados a serem validados (ex: ['email' => 'teste@email.com'])
     * @param array $rules As regras de validação (ex: ['email' => 'required|email'])
     * @return bool True se a validação passar, false caso contrário.
     */
    public static function validate(array $data, array $rules): bool
    {
        self::$errors = []; // Limpa os erros de validações anteriores

        foreach ($rules as $field => $ruleString) {
            $rulesForField = explode('|', $ruleString);
            $value = $data[$field] ?? null;

            foreach ($rulesForField as $rule) {
                $ruleName = $rule;
                $ruleParam = null;

                if (str_contains($rule, ':')) {
                    [$ruleName, $ruleParam] = explode(':', $rule, 2);
                }

                self::applyRule($field, $value, $ruleName, $ruleParam);
            }
        }

        return empty(self::$errors);
    }

    /**
     * Retorna os erros de validação encontrados.
     * @return array
     */
    public static function getErrors(): array
    {
        return self::$errors;
    }

    private static function applyRule(string $field, mixed $value, string $ruleName, ?string $param): void
    {
        switch ($ruleName) {
            case 'required':
                if (empty(trim((string)$value))) {
                    self::$errors[$field][] = "O campo {$field} é obrigatório.";
                }
                break;
            case 'email':
                if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
                    self::$errors[$field][] = "O campo {$field} deve ser um e-mail válido.";
                }
                break;
            case 'ip':
                if (!filter_var($value, FILTER_VALIDATE_IP)) {
                    self::$errors[$field][] = "O campo {$field} deve ser um endereço de IP válido.";
                }
                break;
            case 'min':
                if (strlen(trim((string)$value)) < (int)$param) {
                    self::$errors[$field][] = "O campo {$field} deve ter no mínimo {$param} caracteres.";
                }
                break;
            case 'integer':
                if (!filter_var($value, FILTER_VALIDATE_INT)) {
                    self::$errors[$field][] = "O campo {$field} deve ser um número inteiro.";
                }
                break;
        }
    }
}
```

### `src\Core\View.php`

```php
<?php
namespace App\Core;

class View
{
    private static string $viewsPath = __DIR__ . '/../../views/';
    public static ?string $layout = 'layouts/app';
    private static array $data = [];

    /**
     * Renderiza uma view com template
     */
    public static function render(string $view, array $data = []): string
    {
        $viewData = array_merge(self::$data, $data);
        extract($viewData);
        
        // Capturar conteúdo da view
        ob_start();
        $viewFile = self::$viewsPath . $view . '.php';
        
        if (!file_exists($viewFile)) {
            throw new \Exception("View file not found: {$viewFile}");
        }
        
        include $viewFile;
        $content = ob_get_clean();
        
        // Renderizar com template
        if (self::$layout) {
            ob_start();
            $templateFile = self::$viewsPath . self::$layout . '.php';
            
            if (!file_exists($templateFile)) {
                throw new \Exception("Template file not found: {$templateFile}");
            }
            
            include $templateFile;
            $content = ob_get_clean();
        }
        
        return $content;
    }

    /**
     * Renderiza e exibe uma view
     */
    public static function make(string $view, array $data = []): void
    {
        echo self::render($view, $data);
    }
}
```

### `src\DTO\DispositivoDTO.php`

```php
<?php

namespace App\DTO;

/**
 * Data Transfer Object para a entidade Dispositivo.
 */
class DispositivoDTO
{
    public function __construct(
        public readonly int $id,
        public readonly string $nome,
        public readonly string $ip,
        public readonly int $torre_id,
        public readonly int $tipo_dispositivo_id,
        public readonly int $status,
        public readonly ?string $mac_address,
        public readonly ?string $observacoes,
        public readonly ?string $localizacao,
        public readonly string $created_at,
        public readonly string $updated_at,
        // Propriedades que podem vir de JOINs
        public readonly ?string $torre_nome = null,
        public readonly ?string $tipo_dispositivo_nome = null,
        public readonly ?string $status_descricao = null
    ) {
    }
}
```

### `src\DTO\EventoDTO.php`

```php
<?php

namespace App\DTO;

/**
 * Data Transfer Object para a entidade Evento.
 */
class EventoDTO
{
    public function __construct(
        public readonly int $id,
        public readonly int $dispositivo_id,
        public readonly int $tipo_evento_id,
        public readonly int $status_evento_id,
        public readonly ?int $response_time_ms,
        public readonly ?string $mensagem_original,
        public readonly string $horario,
        // Propriedades que podem vir de JOINs
        public readonly ?string $tipo_evento_descricao = null,
        public readonly ?string $status_evento_descricao = null
    ) {
    }
}
```

### `src\DTO\TorreDTO.php`

```php
<?php

namespace App\DTO;

/**
 * Data Transfer Object para a entidade Torre.
 *
 * Esta classe serve como um contrato de dados fortemente tipado para a comunicação
 * entre as camadas, primariamente entre o Repositório e o Serviço.
 * É uma classe "burra", não contém métodos de negócio ou de acesso a dados.
 * As propriedades são públicas e somente leitura para garantir a imutabilidade
 * dos dados após a sua criação.
 */
class TorreDTO
{
    public function __construct(
        public readonly int $id,
        public readonly string $nome,
        public readonly ?string $localizacao,
        public readonly ?float $latitude,
        public readonly ?float $longitude,
        public readonly int $status_geral,
        public readonly float $uptime_percentage,
        public readonly ?string $last_check,
        public readonly ?string $observacoes,
        public readonly string $created_at,
        public readonly string $updated_at,
        public readonly ?string $status_descricao = null
    ) {
    }
}
```

### `src\Http\Request.php`

```php
<?php
namespace App\Http;

class Request
{
    /**
     * Retorna o corpo (body) de uma requisição JSON como um array associativo.
     * @return array
     */
    public static function body(): array
    {
        return json_decode(file_get_contents('php://input'), true) ?? [];
    }
    
    /**
     * Detecta se a requisição espera JSON
     */
    public static function expectsJson(): bool
    {
        $accept = $_SERVER['HTTP_ACCEPT'] ?? '';
        $xRequestedWith = $_SERVER['HTTP_X_REQUESTED_WITH'] ?? '';
        
        return strpos($accept, 'application/json') !== false ||
               $xRequestedWith === 'XMLHttpRequest';
    }

    /**
     * Obtém parâmetro GET
     */
    public static function get(string $key, $default = null)
    {
        return $_GET[$key] ?? $default;
    }

    /**
     * Obtém parâmetros de paginação
     */
    public static function getPagination(): array
    {
        return [
            'page' => max(1, (int)(self::get('page') ?? 1)),
            'per_page' => min(100, max(1, (int)(self::get('per_page') ?? 10)))
        ];
    }

    /**
     * Validação básica de campos obrigatórios
     */
    public static function validateRequired(array $required): array
    {
        $data = self::body();
        $errors = [];
        
        foreach ($required as $field) {
            if (!isset($data[$field]) || empty(trim($data[$field]))) {
                $errors[$field] = "O campo {$field} é obrigatório";
            }
        }
        
        return $errors;
    }
}
?>
```

### `src\Http\Response.php`

```php
<?php
namespace App\Http;

class Response
{
    /**
     * Envia uma resposta JSON para o cliente com o status code apropriado.
     * @param array $data O conteúdo a ser enviado.
     * @param int $status O código de status HTTP (padrão 200).
     */
    public static function json(array $data = [], int $status = 200): void
    {
        http_response_code($status);
        echo json_encode($data);
    }
    
    /**
     * Resposta de sucesso padronizada
     */
    public static function success($data = [], string $message = '', int $status = 200): void
    {
        self::json([
            'success' => true,
            'data' => $data,
            'message' => $message,
            'meta' => [
                'timestamp' => date('c'),
                'version' => 'v1'
            ]
        ], $status);
    }

    /**
     * Resposta de erro padronizada  
     */
    public static function error(string $message, int $status = 400, array $errors = []): void
    {
        self::json([
            'success' => false,
            'error' => [
                'message' => $message,
                'details' => $errors
            ],
            'meta' => [
                'timestamp' => date('c'),
                'version' => 'v1'
            ]
        ], $status);
    }

    /**
     * Resposta paginada
     */
    public static function paginated(array $data, int $total, int $page = 1, int $perPage = 10): void
    {
        $totalPages = ceil($total / $perPage);
        
        self::success([
            'items' => $data,
            'pagination' => [
                'current_page' => $page,
                'per_page' => $perPage,
                'total' => $total,
                'total_pages' => $totalPages,
                'has_next' => $page < $totalPages,
                'has_prev' => $page > 1
            ]
        ]);
    }

    /**
     * Atalhos para respostas comuns
     */
    public static function notFound(string $resource = 'Resource'): void
    {
        self::error("{$resource} não encontrado", 404);
    }

    public static function unauthorized(string $message = 'Token inválido ou expirado'): void
    {
        self::error($message, 401);
    }

    public static function validationError(array $errors): void
    {
        self::error('Dados inválidos fornecidos', 422, $errors);
    }
}
?>
```

### `src\Http\Route.php`

```php
<?php
// src/Http/Route.php - VERSÃO FINAL LIMPA
namespace App\Http;

class Route
{
    public static function get(string $path, string $action): void
    {
        global $routes;
        
        $routes[] = [
            'method' => 'GET',
            'path' => $path,
            'action' => $action
        ];
    }

    public static function post(string $path, string $action): void
    {
        global $routes;
        
        $routes[] = [
            'method' => 'POST',
            'path' => $path,
            'action' => $action
        ];
    }

    public static function put(string $path, string $action): void
    {
        global $routes;
        
        $routes[] = [
            'method' => 'PUT',
            'path' => $path,
            'action' => $action
        ];
    }

    public static function delete(string $path, string $action): void
    {
        global $routes;
        
        $routes[] = [
            'method' => 'DELETE',
            'path' => $path,
            'action' => $action
        ];
    }
}
```

### `src\Middleware\AuthMiddleware.php`

```php
<?php
namespace App\Middleware;

use App\Http\Request;
use App\Http\Response;
use App\Services\AuthService;
use Exception;

class AuthMiddleware
{
    private static ?array $decodedToken = null;

    /**
     * Verifica o token JWT da requisição
     * CORRIGIDO: Nunca redirecionar em API, sempre retornar JSON
     */
    public static function handle(): bool
    {

        error_log('--- INICIANDO AUTH MIDDLEWARE ---'); // <-- ADICIONA ESTA LINHA
        error_log('Authorization Header Recebido (via $_SERVER): ' . ($_SERVER['HTTP_AUTHORIZATION'] ?? 'NAO ENCONTRADO')); // <-- E ESTA

        try {
            // Obter o cabeçalho de autorização
            $authHeader = $_SERVER['HTTP_AUTHORIZATION'] ??
                ($_SERVER['HTTP_X_AUTHORIZATION'] ?? '');

            // Se não há cabeçalho Authorization, tenta nos headers alternativos
            if (empty($authHeader)) {
                $allHeaders = getallheaders();
                $authHeader = $allHeaders['Authorization'] ??
                    ($allHeaders['authorization'] ?? '');
            }

            // ===================================================================
            // CORREÇÃO: Verificar se é requisição de API
            // ===================================================================
            $isApiRequest = strpos($_SERVER['REQUEST_URI'] ?? '', '/api/') !== false;

            if (empty($authHeader)) {
                error_log("⚠️ AuthMiddleware: Token não fornecido");
                error_log("⚠️ URI: " . ($_SERVER['REQUEST_URI'] ?? 'N/A'));
                error_log("⚠️ É API? " . ($isApiRequest ? 'Sim' : 'Não'));

                if ($isApiRequest) {
                    // Para API, retornar JSON 401
                    header('Content-Type: application/json');
                    http_response_code(401);
                    echo json_encode([
                        'success' => false,
                        'error' => [
                            'message' => 'Token de autorização não fornecido',
                            'code' => 'NO_TOKEN'
                        ]
                    ]);
                    exit;
                } else {
                    // Para páginas web, redirecionar
                    header('Location: /login');
                    exit;
                }
            }

            // Verificar se está no formato Bearer token
            if (!preg_match('/Bearer\s+(\S+)/', $authHeader, $matches)) {
                error_log("⚠️ AuthMiddleware: Formato de token inválido");

                if ($isApiRequest) {
                    header('Content-Type: application/json');
                    http_response_code(401);
                    echo json_encode([
                        'success' => false,
                        'error' => [
                            'message' => 'Formato de token inválido. Use: Bearer <token>',
                            'code' => 'INVALID_FORMAT'
                        ]
                    ]);
                    exit;
                } else {
                    header('Location: /login');
                    exit;
                }
            }

            $token = $matches[1];

            // Validar token
            if (!self::validateTokenSimple($token)) {
                error_log("⚠️ AuthMiddleware: Token inválido ou expirado");

                if ($isApiRequest) {
                    header('Content-Type: application/json');
                    http_response_code(401);
                    echo json_encode([
                        'success' => false,
                        'error' => [
                            'message' => 'Token inválido ou expirado',
                            'code' => 'INVALID_TOKEN'
                        ]
                    ]);
                    exit;
                } else {
                    header('Location: /login');
                    exit;
                }
            }

            error_log("✅ AuthMiddleware: Token validado com sucesso");
            return true;

        } catch (Exception $e) {
            error_log("❌ Erro no middleware de auth: " . $e->getMessage());

            $isApiRequest = strpos($_SERVER['REQUEST_URI'] ?? '', '/api/') !== false;

            if ($isApiRequest) {
                header('Content-Type: application/json');
                http_response_code(500);
                echo json_encode([
                    'success' => false,
                    'error' => [
                        'message' => 'Erro de autenticação',
                        'code' => 'AUTH_ERROR'
                    ]
                ]);
                exit;
            } else {
                header('Location: /login');
                exit;
            }
        }
    }

    /**
     * Validação simples de token JWT
     */
    private static function validateTokenSimple(string $token): bool
    {
        try {
            // Verificação básica da estrutura JWT
            $parts = explode('.', $token);
            if (count($parts) !== 3) {
                error_log("⚠️ Token não tem 3 partes");
                return false;
            }

            // Decodifica o payload
            $payload = json_decode(base64_decode($parts[1]), true);

            if (!$payload) {
                error_log("⚠️ Payload inválido");
                return false;
            }

            // Verifica se o token não expirou
            if (isset($payload['exp']) && $payload['exp'] < time()) {
                error_log("⚠️ Token expirado");
                return false;
            }

            // Verifica issuer se definido
            if (isset($payload['iss']) && $payload['iss'] !== $_ENV['JWT_ISSUER']) {
                error_log("⚠️ Issuer inválido");
                return false;
            }

            // Salva os dados do token
            self::$decodedToken = $payload;

            error_log("✅ Token válido para user_id: " . ($payload['uid'] ?? 'N/A'));
            return true;

        } catch (Exception $e) {
            error_log("❌ Erro ao validar token: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Retorna os dados do token que foi decodificado
     */
    public static function getPayload(): ?array
    {
        return self::$decodedToken;
    }

    /**
     * Retorna o ID do usuário do token decodificado
     */
    public static function getUserId(): ?int
    {
        return self::$decodedToken['uid'] ?? null;
    }
}
```

### `src\Models\Database.php`

```php
<?php

namespace App\Models;

use PDO;
use PDOException;

class Database
{
    private static $instance = null;

    /**
     * Impede a instanciação direta da classe (padrão Singleton).
     */
    private function __construct()
    {
    }

    /**
     * Impede a clonagem da instância (padrão Singleton).
     */
    private function __clone()
    {
    }

    /**
     * Retorna uma instância única de conexão PDO (Singleton).
     * @return PDO
     */
    public static function getInstance(): PDO
    {
        if (self::$instance === null) {
            try {
                $dsn = sprintf(
                    '%s:host=%s;port=%s;dbname=%s', // MANTEMOS O DSN LIMPO
                    $_ENV['DB_CONNECTION'],
                    $_ENV['DB_HOST'],
                    $_ENV['DB_PORT'],
                    $_ENV['DB_DATABASE']
                );

                self::$instance = new PDO(
                    $dsn,
                    $_ENV['DB_USERNAME'],
                    $_ENV['DB_PASSWORD'],
                    [
                        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                        // REMOVEMOS A LINHA: PDO::ATTR_PERSISTENT => true 
                    ]
                );

                // A forma correta de definir o encoding para PostgreSQL
                self::$instance->exec("SET NAMES 'UTF8'");

            } catch (PDOException $e) {
                http_response_code(500);
                die(json_encode(['error' => 'Database connection failed: ' . $e->getMessage()]));
            }
        }

        return self::$instance;
    }
}
```

### `src\Models\MotivoFalha.php`

```php
<?php

namespace App\Models;

class MotivoFalha
{
    /**
     * Busca todos os motivos de falha no banco de dados.
     * @return array
     */
    public static function findAll(): array
    {
        $pdo = Database::getInstance();
        $stmt = $pdo->query("SELECT id, codigo, descricao, categoria FROM motivos_falha ORDER BY descricao ASC");
        return $stmt->fetchAll();
    }
}
```

### `src\Models\StatusTipo.php`

```php
<?php

namespace App\Models;

class StatusTipo
{
    /**
     * Busca todos os tipos de status no banco de dados.
     * @return array
     */
    public static function findAll(): array
    {
        $pdo = Database::getInstance();
        $stmt = $pdo->query("SELECT id, codigo, descricao, is_erro, criticidade, cor_hex FROM status_tipos ORDER BY descricao ASC");
        return $stmt->fetchAll();
    }
}
```

### `src\Models\TipoDispositivo.php`

```php
<?php
namespace App\Models;

use PDO;

class TipoDispositivo
{
    /**
     * Busca um tipo de dispositivo pelo nome. Se não existir, cria um novo de forma atómica.
     * Retorna o ID do tipo existente ou do recém-criado.
     * @param string $nome O nome descritivo do tipo (ex: "Rádio - PTP")
     * @return int|null O ID do tipo de dispositivo ou null em caso de erro.
     */
    public static function findOrCreate(string $nome): ?int
    {
        $nomeLimpo = trim($nome);
        if (empty($nomeLimpo)) {
            // Usa 'Dispositivo Desconhecido' como padrão se o nome for vazio
            return self::findOrCreate('Dispositivo Desconhecido');
        }

        try {
            // CORRIGIDO: Chamada direta para Database::getInstance()
            $db = Database::getInstance();
            $codigo = strtoupper(preg_replace('/[^a-zA-Z0-9]+/', '_', $nomeLimpo));

            // Query "Upsert" para PostgreSQL
            $query = "
                INSERT INTO tipos_dispositivo (codigo, descricao, categoria)
                VALUES (:codigo, :descricao, 'auto')
                ON CONFLICT (codigo) 
                DO UPDATE SET descricao = :descricao -- Ação segura para garantir que o RETURNING id funcione
                RETURNING id;
            ";
            
            $stmt = $db->prepare($query);
            $stmt->bindValue(':codigo', $codigo);
            $stmt->bindValue(':descricao', $nomeLimpo);
            $stmt->execute();
            
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            return $result['id'] ? (int)$result['id'] : null;

        } catch (\Exception $e) {
            error_log("❌ Erro em TipoDispositivo::findOrCreate('$nomeLimpo'): " . $e->getMessage());
            return null;
        }
    }
    
    /**
     * Busca todos os tipos de dispositivo no banco de dados.
     */
    public static function findAll(): array
    {
        // CORRIGIDO: Chamada direta para Database::getInstance()
        $pdo = Database::getInstance();
        $stmt = $pdo->query("SELECT id, codigo, descricao, categoria FROM tipos_dispositivo ORDER BY descricao ASC");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Busca um tipo de dispositivo pelo nome (usado internamente).
     */
    public static function findByName(string $nome): ?array
    {
        try {
            // CORRIGIDO: Chamada direta para Database::getInstance()
            $pdo = Database::getInstance();
            $query = "
                SELECT id, codigo, descricao
                FROM tipos_dispositivo 
                WHERE LOWER(codigo) = LOWER(:nome) OR LOWER(descricao) = LOWER(:nome)
                LIMIT 1
            ";
            $stmt = $pdo->prepare($query);
            $stmt->bindValue(':nome', trim($nome), PDO::PARAM_STR);
            $stmt->execute();
            $tipo = $stmt->fetch(PDO::FETCH_ASSOC);
            return $tipo ?: null;
        } catch (\Exception $e) {
            error_log("Erro em TipoDispositivo::findByName($nome): " . $e->getMessage());
            return null;
        }
    }
}
```

### `src\Models\TipoEvento.php`

```php
<?php

namespace App\Models;

class TipoEvento
{
    /**
     * Busca todos os tipos de evento no banco de dados.
     * @return array
     */
    public static function findAll(): array
    {
        $pdo = Database::getInstance();
        $stmt = $pdo->query("SELECT id, codigo, descricao, categoria FROM tipos_evento ORDER BY descricao ASC");
        return $stmt->fetchAll();
    }
}
```

### `src\Models\Usuario.php`

```php
<?php

namespace App\Models;

use PDO;

class Usuario
{

    public static function findByEmail(string $email): array|false
    {
        $pdo = Database::getInstance();
        $stmt = $pdo->prepare("SELECT * FROM usuarios WHERE email = ?");
        $stmt->execute([$email]);
        return $stmt->fetch();
    }


    public static function save(array $data): int|false
    {
        $pdo = Database::getInstance();
        $stmt = $pdo->prepare(
            "INSERT INTO usuarios (primeiro_nome, ultimo_nome, email, celular, senha) VALUES (?, ?, ?, ?, ?)"
        );

        $success = $stmt->execute([
            $data['primeiro_nome'],
            $data['ultimo_nome'],
            $data['email'],
            $data['celular'],
            $data['senha']
        ]);

        return $success ? (int) $pdo->lastInsertId() : false;
    }

    public static function findById(int $id): array|false
    {
        $pdo = Database::getInstance();
        $stmt = $pdo->prepare("SELECT id, primeiro_nome, ultimo_nome, email, celular, created_at, updated_at FROM usuarios WHERE id = ?");
        $stmt->execute([$id]);
        return $stmt->fetch();
    }


    public static function update(int $id, array $data): bool
    {
        $pdo = Database::getInstance();

        $usuario = self::findById($id);
        if ($usuario === false) {
            return false;
        }
        $camposPermitidos = ['primeiro_nome', 'ultimo_nome', 'email', 'senha', 'celular'];

        $camposAtualizar = [];
        $valores = [];

        foreach ($camposPermitidos as $campo) {
            if (isset($data[$campo])) {
                $camposAtualizar[] = "$campo = ?";
                $valores[] = $data[$campo];
            }
        }

        if (empty($camposAtualizar)) {
            return false;
        }

        $valores[] = $id;

        $sql = "UPDATE usuarios SET " . implode(', ', $camposAtualizar) . " WHERE id = ?";
        $stmt = $pdo->prepare($sql);

        return $stmt->execute($valores);
    }

}
```

### `src\Repository\DispositivoRepository.php`

```php
<?php

namespace App\Repositories;

use App\DTO\DispositivoDTO;
use PDO;

/**
 * Repository para a entidade Dispositivo.
 */
class DispositivoRepository
{
    private PDO $db;

    public function __construct(PDO $db)
    {
        $this->db = $db;
    }

    private function toDTO(array $data): DispositivoDTO
    {
        return new DispositivoDTO(
            id: (int) $data['id'],
            nome: $data['nome'],
            ip: $data['ip'],
            torre_id: (int) $data['torre_id'],
            tipo_dispositivo_id: (int) $data['tipo_dispositivo_id'],
            status: (int) $data['status'],
            mac_address: $data['mac_address'],
            observacoes: $data['observacoes'],
            localizacao: $data['localizacao'],
            created_at: $data['created_at'],
            updated_at: $data['updated_at'],
            torre_nome: $data['torre_nome'] ?? null,
            tipo_dispositivo_nome: $data['tipo_dispositivo_nome'] ?? null,
            status_descricao: $data['status_descricao'] ?? null
        );
    }

    /**
     * @return DispositivoDTO[]
     */
    public function findAll(): array
    {
        $query = "
            SELECT 
                d.*,
                t.nome as torre_nome,
                td.nome as tipo_dispositivo_nome,
                st.descricao as status_descricao
            FROM dispositivos d
            LEFT JOIN torres t ON d.torre_id = t.id
            LEFT JOIN tipos_dispositivo td ON d.tipo_dispositivo_id = td.id
            LEFT JOIN status_tipos st ON d.status = st.id
            ORDER BY d.nome ASC
        ";
        $stmt = $this->db->query($query);
        $dispositivosData = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $dispositivos = [];
        foreach ($dispositivosData as $data) {
            $dispositivos[] = $this->toDTO($data);
        }
        return $dispositivos;
    }

    public function findById(int $id): ?DispositivoDTO
    {
        $query = "
            SELECT 
                d.*,
                t.nome as torre_nome,
                td.nome as tipo_dispositivo_nome,
                st.descricao as status_descricao
            FROM dispositivos d
            LEFT JOIN torres t ON d.torre_id = t.id
            LEFT JOIN tipos_dispositivo td ON d.tipo_dispositivo_id = td.id
            LEFT JOIN status_tipos st ON d.status = st.id
            WHERE d.id = :id
        ";
        $stmt = $this->db->prepare($query);
        $stmt->bindValue(':id', $id, PDO::PARAM_INT);
        $stmt->execute();
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        return $data ? $this->toDTO($data) : null;
    }

    public function save(array $data): ?int
    {
        $query = "
            INSERT INTO dispositivos (nome, ip, torre_id, tipo_dispositivo_id, status, mac_address, observacoes, localizacao, created_at, updated_at) 
            VALUES (:nome, :ip, :torre_id, :tipo_dispositivo_id, :status, :mac_address, :observacoes, :localizacao, NOW(), NOW())
        ";
        $stmt = $this->db->prepare($query);

        $stmt->bindValue(':nome', $data['nome']);
        $stmt->bindValue(':ip', $data['ip']);
        $stmt->bindValue(':torre_id', $data['torre_id'], PDO::PARAM_INT);
        $stmt->bindValue(':tipo_dispositivo_id', $data['tipo_dispositivo_id'], PDO::PARAM_INT);
        $stmt->bindValue(':status', $data['status'] ?? 1, PDO::PARAM_INT);
        $stmt->bindValue(':mac_address', $data['mac_address'] ?? null);
        $stmt->bindValue(':observacoes', $data['observacoes'] ?? null);
        $stmt->bindValue(':localizacao', $data['localizacao'] ?? null);

        $stmt->execute();
        return (int) $this->db->lastInsertId();
    }

    public function update(int $id, array $data): bool
    {
        $query = "
            UPDATE dispositivos 
            SET nome = :nome, ip = :ip, torre_id = :torre_id, tipo_dispositivo_id = :tipo_dispositivo_id, status = :status, 
                mac_address = :mac_address, observacoes = :observacoes, localizacao = :localizacao, updated_at = NOW()
            WHERE id = :id
        ";
        $stmt = $this->db->prepare($query);

        $stmt->bindValue(':id', $id, PDO::PARAM_INT);
        $stmt->bindValue(':nome', $data['nome']);
        $stmt->bindValue(':ip', $data['ip']);
        $stmt->bindValue(':torre_id', $data['torre_id'], PDO::PARAM_INT);
        $stmt->bindValue(':tipo_dispositivo_id', $data['tipo_dispositivo_id'], PDO::PARAM_INT);
        $stmt->bindValue(':status', $data['status'] ?? 1, PDO::PARAM_INT);
        $stmt->bindValue(':mac_address', $data['mac_address'] ?? null);
        $stmt->bindValue(':observacoes', $data['observacoes'] ?? null);
        $stmt->bindValue(':localizacao', $data['localizacao'] ?? null);

        return $stmt->execute();
    }

    public function delete(int $id): bool
    {
        $stmt = $this->db->prepare("DELETE FROM dispositivos WHERE id = :id");
        $stmt->bindValue(':id', $id, PDO::PARAM_INT);
        return $stmt->execute();
    }
    
    public function findByTorreAndName(int $torreId, string $nome): ?DispositivoDTO
    {
        $query = "
            SELECT d.*, t.nome as torre_nome, td.nome as tipo_dispositivo_nome, st.descricao as status_descricao
            FROM dispositivos d
            LEFT JOIN torres t ON d.torre_id = t.id
            LEFT JOIN tipos_dispositivo td ON d.tipo_dispositivo_id = td.id
            LEFT JOIN status_tipos st ON d.status = st.id
            WHERE d.torre_id = :torre_id AND LOWER(d.nome) = LOWER(:nome)
            LIMIT 1
        ";
        $stmt = $this->db->prepare($query);
        $stmt->bindValue(':torre_id', $torreId, PDO::PARAM_INT);
        $stmt->bindValue(':nome', trim($nome), PDO::PARAM_STR);
        $stmt->execute();
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        return $data ? $this->toDTO($data) : null;
    }
}
```

### `src\Repository\EventoRepository.php`

```php
<?php

namespace App\Repositories;

use App\DTO\EventoDTO;
use PDO;

/**
 * Repository para a entidade Evento.
 */
class EventoRepository
{
    private PDO $db;

    public function __construct(PDO $db)
    {
        $this->db = $db;
    }

    private function toDTO(array $data): EventoDTO
    {
        return new EventoDTO(
            id: (int) $data['id'],
            dispositivo_id: (int) $data['dispositivo_id'],
            tipo_evento_id: (int) $data['tipo_evento_id'],
            status_evento_id: (int) $data['status_evento_id'],
            response_time_ms: isset($data['response_time_ms']) ? (int) $data['response_time_ms'] : null,
            mensagem_original: $data['mensagem_original'],
            horario: $data['horario'],
            tipo_evento_descricao: $data['tipo_evento_descricao'] ?? null,
            status_evento_descricao: $data['status_evento_descricao'] ?? null
        );
    }

    /**
     * @return EventoDTO[]
     */
    public function findByDispositivoId(int $dispositivoId): array
    {
        $query = "
            SELECT 
                e.*,
                te.descricao as tipo_evento_descricao,
                st.descricao as status_evento_descricao
            FROM eventos e
            LEFT JOIN tipos_evento te ON e.tipo_evento_id = te.id
            LEFT JOIN status_tipos st ON e.status_evento_id = st.id
            WHERE e.dispositivo_id = :dispositivo_id 
            ORDER BY e.horario DESC
        ";
        $stmt = $this->db->prepare($query);
        $stmt->bindValue(':dispositivo_id', $dispositivoId, PDO::PARAM_INT);
        $stmt->execute();
        
        $eventosData = $stmt->fetchAll(PDO::FETCH_ASSOC);
        $eventos = [];
        foreach ($eventosData as $data) {
            $eventos[] = $this->toDTO($data);
        }
        return $eventos;
    }

    public function save(array $data): ?int
    {
        $query = "
            INSERT INTO eventos (dispositivo_id, tipo_evento_id, status_evento_id, response_time_ms, mensagem_original) 
            VALUES (:dispositivo_id, :tipo_evento_id, :status_evento_id, :response_time_ms, :mensagem_original)
        ";
        $stmt = $this->db->prepare($query);

        $stmt->bindValue(':dispositivo_id', $data['dispositivo_id'], PDO::PARAM_INT);
        $stmt->bindValue(':tipo_evento_id', $data['tipo_evento_id'], PDO::PARAM_INT);
        $stmt->bindValue(':status_evento_id', $data['status_evento_id'], PDO::PARAM_INT);
        $stmt->bindValue(':response_time_ms', $data['response_time_ms'] ?? null, PDO::PARAM_INT);
        $stmt->bindValue(':mensagem_original', $data['mensagem_original'] ?? null);

        $stmt->execute();
        return (int) $this->db->lastInsertId();
    }
}
```

### `src\Repository\TorreRepository.php`

```php
<?php

namespace App\Repositories;

use App\DTO\TorreDTO;
use PDO;
use PDOException;

/**
 * Repository para a entidade Torre.
 *
 * É o único intermediário entre a aplicação e a fonte de dados (tabela 'torres').
 * Contém todo o código SQL e converte os dados brutos do banco de dados em DTOs.
 * Usa exclusivamente prepared statements para máxima segurança.
 */
class TorreRepository
{
    private PDO $db;

    /**
     * O construtor recebe a dependência da conexão PDO.
     */
    public function __construct(PDO $db)
    {
        $this->db = $db;
    }

    /**
     * Converte um array de dados do banco de dados em um TorreDTO.
     *
     * @param array $data O array associativo vindo do fetch.
     * @return TorreDTO O objeto de transferência de dados.
     */
    private function toDTO(array $data): TorreDTO
    {
        return new TorreDTO(
            id: (int) $data['id'],
            nome: $data['nome'],
            localizacao: $data['localizacao'],
            latitude: (float) $data['latitude'],
            longitude: (float) $data['longitude'],
            status_geral: (int) $data['status_geral'],
            uptime_percentage: (float) $data['uptime_percentage'],
            last_check: $data['last_check'],
            observacoes: $data['observacoes'],
            created_at: $data['created_at'],
            updated_at: $data['updated_at'],
            status_descricao: $data['status_descricao'] ?? null
        );
    }

    /**
     * Buscar todas as torres.
     *
     * @return TorreDTO[]
     */
    public function findAll(): array
    {
        $query = "
            SELECT 
                t.id, t.nome, t.localizacao, t.latitude, t.longitude, 
                t.status_geral, t.uptime_percentage, t.last_check, t.observacoes,
                t.created_at, t.updated_at,
                st.descricao as status_descricao
            FROM torres t
            LEFT JOIN status_tipos st ON t.status_geral = st.id
            ORDER BY t.nome ASC
        ";
        $stmt = $this->db->query($query);
        $torresData = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $torres = [];
        foreach ($torresData as $torreData) {
            $torres[] = $this->toDTO($torreData);
        }
        return $torres;
    }

    /**
     * Buscar torre por ID.
     */
    public function findById(int $id): ?TorreDTO
    {
        $query = "
            SELECT 
                t.id, t.nome, t.localizacao, t.latitude, t.longitude,
                t.status_geral, t.uptime_percentage, t.last_check, t.observacoes,
                t.created_at, t.updated_at,
                st.descricao as status_descricao
            FROM torres t
            LEFT JOIN status_tipos st ON t.status_geral = st.id
            WHERE t.id = :id
        ";
        $stmt = $this->db->prepare($query);
        $stmt->bindValue(':id', $id, PDO::PARAM_INT);
        $stmt->execute();
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        return $data ? $this->toDTO($data) : null;
    }

    /**
     * Criar nova torre.
     *
     * @param array $data Dados da torre a ser criada.
     * @return int|null O ID da torre inserida ou null em caso de falha.
     */
    public function save(array $data): ?int
    {
        $query = "
            INSERT INTO torres (
                nome, localizacao, latitude, longitude, status_geral, 
                uptime_percentage, observacoes, depende_de_torre_id, 
                created_at, updated_at
            ) VALUES (
                :nome, :localizacao, :latitude, :longitude, :status, 
                :uptime, :observacoes, :depende_de_torre_id, NOW(), NOW()
            ) RETURNING id
        ";

        $stmt = $this->db->prepare($query);
        $stmt->bindValue(':nome', $data['nome']);
        $stmt->bindValue(':localizacao', $data['localizacao'] ?? null);
        $stmt->bindValue(':latitude', $data['latitude'] ?? null);
        $stmt->bindValue(':longitude', $data['longitude'] ?? null);
        $stmt->bindValue(':status', $data['status_geral'] ?? 1, PDO::PARAM_INT);
        $stmt->bindValue(':uptime', $data['uptime_percentage'] ?? 100.0);
        $stmt->bindValue(':observacoes', $data['observacoes'] ?? null);
        $stmt->bindValue(':depende_de_torre_id', $data['depende_de_torre_id'] ?? null, PDO::PARAM_INT);

        $stmt->execute();
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        return $result['id'] ? (int) $result['id'] : null;
    }

    /**
     * Atualizar torre.
     *
     * @param int $id O ID da torre a ser atualizada.
     * @param array $data Os dados a serem atualizados.
     * @return bool True se a atualização foi bem-sucedida, false caso contrário.
     */
    public function update(int $id, array $data): bool
    {
        $setClauses = [];
        $params = ['id' => $id];

        $allowedFields = ['nome', 'localizacao', 'latitude', 'longitude', 'uptime_percentage', 'observacoes', 'depende_de_torre_id', 'status_geral'];

        foreach ($data as $field => $value) {
            if (in_array($field, $allowedFields)) {
                $setClauses[] = "$field = :$field";
                $params[$field] = $value;
            }
        }

        if (empty($setClauses)) {
            return false;
        }

        $setClauses[] = "updated_at = NOW()";
        $setClause = implode(', ', $setClauses);
        $query = "UPDATE torres SET $setClause WHERE id = :id";

        $stmt = $this->db->prepare($query);
        foreach ($params as $key => &$val) { // Passar por referência para bindValue
            $stmt->bindValue(":$key", $val);
        }
        return $stmt->execute();
    }

    /**
     * Deletar torre.
     */
    public function delete(int $id): bool
    {
        $query = "DELETE FROM torres WHERE id = :id";
        $stmt = $this->db->prepare($query);
        $stmt->bindValue(':id', $id, PDO::PARAM_INT);
        return $stmt->execute();
    }
    
    /**
     * Buscar torre por nome.
     */
    public function findByName(string $nome): ?TorreDTO
    {
        $query = "
            SELECT 
                t.*,
                st.descricao as status_descricao
            FROM torres t
            LEFT JOIN status_tipos st ON t.status_geral = st.id
            WHERE LOWER(t.nome) = LOWER(:nome) 
            LIMIT 1
        ";
        $stmt = $this->db->prepare($query);
        $stmt->bindValue(':nome', trim($nome), PDO::PARAM_STR);
        $stmt->execute();
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        return $data ? $this->toDTO($data) : null;
    }
}
```

### `src\Services\AuthService.php`

```php
<?php
namespace App\Services;

use App\Core\Validator;
use App\Models\Usuario;
use Lcobucci\JWT\Configuration;
use Lcobucci\JWT\Signer\Hmac\Sha256;
use Lcobucci\JWT\Signer\Key\InMemory;
use DateTimeImmutable;

class AuthService
{
    /** @var Configuration Configuração do JWT. */
    private Configuration $jwtConfig;

    /**
     * Construtor do AuthService.
     * Configura a biblioteca JWT.
     */
    public function __construct()
    {
        $secret = getenv('JWT_SECRET_KEY') ?: $_ENV['JWT_SECRET_KEY'] ?? null;
        if (!$secret) {
            throw new \RuntimeException('JWT_SECRET_KEY não está definido no ambiente.');
        }
        $this->jwtConfig = Configuration::forSymmetricSigner(
            new Sha256(),
            InMemory::plainText($secret)
        );
    }

    /**
     * Valida e regista um novo usuário no sistema.
     *
     * @param array $data Dados do usuário (primeiro_nome, ultimo_nome, celular, email, senha).
     * @return array Retorna um array com o resultado da operação.
     */
    public function register(array $data): array
    {
        $rules = [
            'primeiro_nome' => 'required',
            'ultimo_nome' => 'required',
            'celular' => 'required',
            'email' => 'required|email',
            'senha' => 'required|min:8'
        ];

        if (!Validator::validate($data, $rules)) {
            return ['error' => 'Dados de registo inválidos.', 'details' => Validator::getErrors(), 'status' => 422];
        }

        if (Usuario::findByEmail($data['email'])) {
            return ['error' => 'Este e-mail já está em uso.', 'status' => 409];
        }

        $data['senha'] = password_hash($data['senha'], PASSWORD_ARGON2ID);
        $userId = Usuario::save($data);

        if (!$userId) {
            return ['error' => 'Falha ao criar o usuário no banco de dados.', 'status' => 500];
        }

        return [
            'message' => 'Usuário criado com sucesso!',
            'data' => ['userId' => $userId],
            'status' => 201
        ];
    }

    /**
     * Autentica um usuário e retorna um token JWT.
     *
     * @param array $data Credenciais do usuário (email, senha).
     * @return array Retorna um array com o token ou um erro.
     */
    public function login(array $data): array
    {
        $rules = [
            'email' => 'required|email',
            'senha' => 'required'
        ];

        if (!Validator::validate($data, $rules)) {
            return ['error' => 'Dados de login inválidos', 'details' => Validator::getErrors(), 'status' => 422];
        }

        $user = Usuario::findByEmail($data['email']);

        if (!$user || !password_verify($data['senha'], $user['senha'])) {
            return ['error' => 'Credenciais inválidas.', 'status' => 401];
        }

        $now = new DateTimeImmutable();
        $token = $this->jwtConfig->builder()
            ->issuedBy($_ENV['JWT_ISSUER'])
            ->permittedFor($_ENV['JWT_AUDIENCE'])
            ->issuedAt($now)
            ->expiresAt($now->modify('+1 hour'))
            ->withClaim('uid', $user['id'])
            ->getToken($this->jwtConfig->signer(), $this->jwtConfig->signingKey());

        return ['token' => $token->toString(), 'status' => 200];
    }
}
```

### `src\Services\DashboardService.php`

```php
<?php
namespace App\Services;

use App\Models\Database;
use PDO;

class DashboardService
{
    private PDO $db;

    public function __construct()
    {
        $this->db = Database::getInstance();
    }

    /**
     * Buscar torres online (status = 1)
     */
    public function getTorresUp(): int
    {
        try {
            $query = "SELECT COUNT(*) as total FROM torres WHERE status_geral = 1";
            $stmt = $this->db->prepare($query);
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            return (int) $result['total'];
        } catch (\Exception $e) {
            error_log("Erro ao contar torres UP: " . $e->getMessage());
            return 0;
        }
    }

    /**
     * Buscar torres offline (status = 2)
     */
    public function getTorresDown(): int
    {
        try {
            $query = "SELECT COUNT(*) as total FROM torres WHERE status_geral = 2";
            $stmt = $this->db->prepare($query);
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            return (int) $result['total'];
        } catch (\Exception $e) {
            error_log("Erro ao contar torres DOWN: " . $e->getMessage());
            return 0;
        }
    }

    /**
     * Calcular disponibilidade média
     */
    public function getDisponibilidadeMedia(): float
    {
        try {
            $query = "SELECT AVG(uptime_percentage) as media FROM torres WHERE uptime_percentage IS NOT NULL";
            $stmt = $this->db->prepare($query);
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            return round($result['media'] ?? 0, 1);
        } catch (\Exception $e) {
            error_log("Erro ao calcular disponibilidade: " . $e->getMessage());
            return 0.0;
        }
    }

    /**
     * Delta torres UP (simulado)
     */
    public function getDeltaTorresUp(): int
    {
        return 2; // +2 desde ontem (mock)
    }

    /**
     * Delta torres DOWN (simulado) 
     */
    public function getDeltaTorresDown(): int
    {
        return -1; // -1 desde ontem (mock)
    }

    /**
     * Delta disponibilidade (simulado)
     */
    public function getDeltaDisponibilidade(): float
    {
        return 1.2; // +1.2% desde ontem (mock)
    }

    /**
     * Falhas por criticidade (dados reais)
     */
    public function getFalhasPorCriticidade(): array
    {
        try {
            $query = "
                SELECT 
                    COALESCE(st.criticidade, 'baixa') as criticidade,
                    COUNT(e.id) as total
                FROM eventos e
                LEFT JOIN status_tipos st ON e.status_evento_id = st.id
                WHERE e.horario >= NOW() - INTERVAL '7 days'
                GROUP BY st.criticidade
                ORDER BY total DESC
            ";

            $stmt = $this->db->prepare($query);
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (\Exception $e) {
            error_log("Erro ao buscar falhas por criticidade: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Eventos recentes
     */
    public function getEventosRecentes(int $limit = 5): array
    {
        try {
            $query = "
                SELECT 
                    e.horario,
                    e.mensagem_original,
                    t.nome as torre,
                    d.nome as dispositivo,
                    CASE 
                        WHEN e.horario >= NOW() - INTERVAL '1 hour' THEN 'há poucos minutos'
                        WHEN e.horario >= NOW() - INTERVAL '1 day' THEN CONCAT(EXTRACT(HOUR FROM (NOW() - e.horario))::int, 'h atrás')
                        ELSE CONCAT(EXTRACT(DAY FROM (NOW() - e.horario))::int, 'd atrás')
                    END as tempo_atras,
                    'alta' as criticidade
                FROM eventos e
                JOIN dispositivos d ON e.dispositivo_id = d.id
                JOIN torres t ON d.torre_id = t.id
                ORDER BY e.horario DESC
                LIMIT :limit
            ";

            $stmt = $this->db->prepare($query);
            $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (\Exception $e) {
            error_log("Erro ao buscar eventos recentes: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Torres para visão geral
     */
    public function getTorresVisaoGeral(): array
    {
        try {
            $query = "
                SELECT 
                    t.nome as torre,
                    ROUND(t.uptime_percentage, 1) || '%' as uptime,
                    t.localizacao,
                    CASE 
                        WHEN t.last_check >= NOW() - INTERVAL '10 minutes' THEN 'Online'
                        WHEN t.last_check >= NOW() - INTERVAL '1 hour' THEN 'há ' || EXTRACT(MINUTE FROM (NOW() - t.last_check))::int || 'min'
                        ELSE 'há ' || EXTRACT(HOUR FROM (NOW() - t.last_check))::int || 'h'
                    END as ultimo_check,
                    CASE t.status_geral
                        WHEN 1 THEN 'up'
                        WHEN 2 THEN 'down'  
                        WHEN 3 THEN 'maintenance'
                        WHEN 4 THEN 'warning'
                        ELSE 'unknown'
                    END as status
                FROM torres t
                ORDER BY t.nome ASC
                LIMIT 5;
            ";

            $stmt = $this->db->prepare($query);
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (\Exception $e) {
            error_log("Erro ao buscar torres visão geral: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Busca as estatísticas principais (KPIs) para os cards do dashboard.
     * Utiliza uma única query otimizada para performance.
     * @return array
     */
    public function getKpiStatistics(): array
    {
        try {
            // IDs de status baseados no script de lookup (1=Online, 2=Offline)
            $onlineStatusId = 1;
            $offlineStatusId = 2;

            $query = "
                SELECT
                    COUNT(*) AS total_torres,
                    COUNT(CASE WHEN status_geral = :online_status_id THEN 1 END) AS torres_online,
                    COUNT(CASE WHEN status_geral = :offline_status_id THEN 1 END) AS torres_offline,
                    AVG(uptime_percentage) AS uptime_medio
                FROM torres;
            ";

            $stmt = $this->db->prepare($query);
            $stmt->bindValue(':online_status_id', $onlineStatusId, PDO::PARAM_INT);
            $stmt->bindValue(':offline_status_id', $offlineStatusId, PDO::PARAM_INT);
            $stmt->execute();

            $result = $stmt->fetch(PDO::FETCH_ASSOC);

            // Retorna os dados com um formato limpo e padronizado
            return [
                'total_torres' => (int) ($result['total_torres'] ?? 0),
                'torres_online' => (int) ($result['torres_online'] ?? 0),
                'torres_offline' => (int) ($result['torres_offline'] ?? 0),
                'uptime_medio' => round((float) ($result['uptime_medio'] ?? 0), 2)
            ];

        } catch (\PDOException $e) {
            error_log("❌ Erro em DashboardService::getKpiStatistics(): " . $e->getMessage());
            // Retorna uma estrutura zerada em caso de erro, para não quebrar o frontend.
            return [
                'total_torres' => 0,
                'torres_online' => 0,
                'torres_offline' => 0,
                'uptime_medio' => 0.0
            ];
        }
    }

    /**
     * Busca a contagem de dispositivos online e offline.
     * @return array
     */
    public function getStatusDispositivos(): array
    {
        try {
            // No CSV e no banco, o status dos dispositivos é '1' (online) ou '2' (offline)
            $query = "
                SELECT
                    COUNT(CASE WHEN status = '1' THEN 1 END) AS online,
                    COUNT(CASE WHEN status = '2' THEN 1 END) AS offline
                FROM dispositivos;
            ";

            $stmt = $this->db->query($query);
            $result = $stmt->fetch(PDO::FETCH_ASSOC);

            return [
                'online' => (int) ($result['online'] ?? 0),
                'offline' => (int) ($result['offline'] ?? 0)
            ];

        } catch (\PDOException $e) {
            error_log("❌ Erro em DashboardService::getStatusDispositivos(): " . $e->getMessage());
            return ['online' => 0, 'offline' => 0];
        }
    }

    /**
     * Busca a contagem de dispositivos agrupados por tipo para o gráfico de inventário.
     * @return array
     */
    public function getTiposDispositivosCount(): array
    {
        try {
            $query = "
                SELECT
                    td.descricao AS tipo,
                    COUNT(d.id) AS total
                FROM
                    dispositivos d
                JOIN
                    tipos_dispositivo td ON d.tipo_dispositivo_id = td.id
                GROUP BY
                    td.descricao
                ORDER BY
                    total DESC;
            ";

            $stmt = $this->db->query($query);
            $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

            // O resultado já vem no formato [ ['tipo' => 'Antena', 'total' => 10], ... ]
            // Apenas garantimos que os totais são números inteiros.
            return array_map(function ($row) {
                $row['total'] = (int) $row['total'];
                return $row;
            }, $results);

        } catch (\PDOException $e) {
            error_log("❌ Erro em DashboardService::getTiposDispositivosCount(): " . $e->getMessage());
            return [];
        }
    }

    /**
     * Busca as 5 torres com a maior contagem de dispositivos offline,
     * incluindo a lista de nomes desses dispositivos.
     * @return array
     */
    public function getTorresCriticas(): array
    {
        try {
            $offlineStatus = '2'; // Status '2' para Offline

            // Passo 1: Encontrar as 5 torres mais críticas (pelo ID)
            $queryTorres = "
                SELECT t.id, t.nome, COUNT(d.id) AS offline_count
                FROM torres t
                JOIN dispositivos d ON t.id = d.torre_id
                WHERE d.status = :offline_status
                GROUP BY t.id, t.nome
                ORDER BY offline_count DESC
                LIMIT 5;
            ";
            $stmtTorres = $this->db->prepare($queryTorres);
            $stmtTorres->bindValue(':offline_status', $offlineStatus);
            $stmtTorres->execute();
            $torresCriticas = $stmtTorres->fetchAll(PDO::FETCH_ASSOC);

            if (empty($torresCriticas)) {
                return [];
            }

            // Passo 2: Buscar todos os dispositivos offline APENAS dessas torres
            $torreIds = array_column($torresCriticas, 'id');
            $placeholders = implode(',', array_fill(0, count($torreIds), '?'));

            $queryDispositivos = "
                SELECT torre_id, nome FROM dispositivos 
                WHERE status = ? AND torre_id IN ($placeholders)
            ";
            $params = array_merge([$offlineStatus], $torreIds);

            $stmtDispositivos = $this->db->prepare($queryDispositivos);
            $stmtDispositivos->execute($params);
            $dispositivosOffline = $stmtDispositivos->fetchAll(PDO::FETCH_ASSOC);

            // Passo 3: Juntar os dados em PHP
            $resultado = [];
            foreach ($torresCriticas as $torre) {
                $dispositivosDaTorre = [];
                foreach ($dispositivosOffline as $dispositivo) {
                    if ($dispositivo['torre_id'] == $torre['id']) {
                        $dispositivosDaTorre[] = ['nome' => $dispositivo['nome']];
                    }
                }
                $resultado[] = [
                    'nome' => $torre['nome'],
                    'offline_count' => (int) $torre['offline_count'],
                    'dispositivos_offline' => $dispositivosDaTorre
                ];
            }

            return $resultado;

        } catch (\PDOException $e) {
            error_log("❌ Erro em DashboardService::getTorresCriticas(): " . $e->getMessage());
            return [];
        }
    }

    /**
     * Busca uma lista completa de torres com contagem de dispositivos para a visão geral.
     * @return array
     */
    public function getVisaoGeralTorres(): array
    {
        try {
            $query = "
                SELECT
                    t.id,
                    t.nome,
                    t.localizacao,
                    t.uptime_percentage,
                    st.descricao AS status_descricao,
                    st.cor_hex AS status_cor,
                    COUNT(d.id) AS total_dispositivos,
                    COUNT(CASE WHEN d.status = '1' THEN 1 END) AS dispositivos_online,
                    COUNT(CASE WHEN d.status = '2' THEN 1 END) AS dispositivos_offline
                FROM
                    torres t
                LEFT JOIN
                    status_tipos st ON t.status_geral = st.id
                LEFT JOIN
                    dispositivos d ON t.id = d.torre_id
                GROUP BY
                    t.id, t.nome, t.localizacao, t.uptime_percentage, st.descricao, st.cor_hex
                ORDER BY
                    t.nome ASC
                    LIMIT 3;
            ";

            $stmt = $this->db->query($query);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);

        } catch (\PDOException $e) {
            error_log("❌ Erro em DashboardService::getVisaoGeralTorres(): " . $e->getMessage());
            return [];
        }
    }
}
```

### `src\Services\DispositivoService.php`

```php
<?php

namespace App\Services;

use App\Repositories\DispositivoRepository;
use App\DTO\DispositivoDTO;
use App\Core\Validator;
use Exception;
use PDOException;

/**
 * Service para a entidade Dispositivo.
 */
class DispositivoService
{
    private DispositivoRepository $dispositivoRepository;

    public function __construct(DispositivoRepository $dispositivoRepository)
    {
        $this->dispositivoRepository = $dispositivoRepository;
    }

    /**
     * @return DispositivoDTO[]
     */
    public function getAll(): array
    {
        return $this->dispositivoRepository->findAll();
    }

    public function getById(int $id): ?DispositivoDTO
    {
        return $this->dispositivoRepository->findById($id);
    }

    /**
     * @throws Exception
     */
    public function create(array $data): DispositivoDTO
    {
        $rules = [
            'nome' => 'required',
            'ip' => 'required|ip',
            'torre_id' => 'required|integer',
            'tipo_dispositivo_id' => 'required|integer'
        ];

        if (!Validator::validate($data, $rules)) {
            throw new Exception(json_encode(Validator::getErrors()), 422);
        }
        
        try {
            // Lógica de negócio: verificar se já existe um dispositivo com o mesmo nome na mesma torre
            $existing = $this->dispositivoRepository->findByTorreAndName($data['torre_id'], $data['nome']);
            if ($existing) {
                throw new Exception("Já existe um dispositivo com o nome '{$data['nome']}' nesta torre.", 409);
            }

            $dispositivoId = $this->dispositivoRepository->save($data);
            if (!$dispositivoId) {
                throw new Exception('Falha ao criar o dispositivo.', 500);
            }
            
            $novoDispositivo = $this->getById($dispositivoId);
            if (!$novoDispositivo) {
                throw new Exception('Não foi possível encontrar o dispositivo recém-criado.', 500);
            }
            return $novoDispositivo;

        } catch (PDOException $e) {
            if ($e->getCode() == '23505') { // Unique violation
                throw new Exception('Este endereço IP já está em uso.', 409);
            }
            throw new Exception('Erro de banco de dados ao criar dispositivo.', 500);
        }
    }

    /**
     * @throws Exception
     */
    public function update(int $id, array $data): DispositivoDTO
    {
        $dispositivo = $this->dispositivoRepository->findById($id);
        if (!$dispositivo) {
            throw new Exception('Dispositivo não encontrado.', 404);
        }

        // Valida o IP se ele for fornecido
        if (isset($data['ip']) && !filter_var($data['ip'], FILTER_VALIDATE_IP)) {
            throw new Exception('O formato do endereço IP é inválido.', 422);
        }

        try {
            if (!$this->dispositivoRepository->update($id, $data)) {
                 throw new Exception('Nenhum dado foi alterado ou falha ao atualizar.', 500);
            }
            
            $dispositivoAtualizado = $this->getById($id);
            if (!$dispositivoAtualizado) {
                throw new Exception('Não foi possível encontrar o dispositivo recém-atualizado.', 500);
            }
            return $dispositivoAtualizado;

        } catch (PDOException $e) {
            if ($e->getCode() == '23505') {
                throw new Exception('Este endereço IP já está em uso por outro dispositivo.', 409);
            }
            throw new Exception('Erro de banco de dados ao atualizar dispositivo.', 500);
        }
    }

    /**
     * @throws Exception
     */
    public function delete(int $id): bool
    {
        $dispositivo = $this->dispositivoRepository->findById($id);
        if (!$dispositivo) {
            throw new Exception('Dispositivo não encontrado.', 404);
        }
        
        if (!$this->dispositivoRepository->delete($id)) {
            throw new Exception('Falha ao apagar o dispositivo.', 500);
        }
        
        return true;
    }
}
```

### `src\Services\EventoService.php`

```php
<?php

namespace App\Services;

use App\Repositories\EventoRepository;
use App\Repositories\DispositivoRepository;
use App\DTO\EventoDTO;
use App\Core\Validator;
use Exception;

/**
 * Service para a entidade Evento.
 */
class EventoService
{
    private EventoRepository $eventoRepository;
    private DispositivoRepository $dispositivoRepository;

    public function __construct(EventoRepository $eventoRepository, DispositivoRepository $dispositivoRepository)
    {
        $this->eventoRepository = $eventoRepository;
        $this->dispositivoRepository = $dispositivoRepository;
    }

    /**
     * @return EventoDTO[]
     * @throws Exception
     */
    public function getEventosByDispositivoId(int $dispositivoId): array
    {
        if (!$this->dispositivoRepository->findById($dispositivoId)) {
            throw new Exception('Dispositivo não encontrado.', 404);
        }
        return $this->eventoRepository->findByDispositivoId($dispositivoId);
    }

    /**
     * @throws Exception
     */
    public function createEvento(int $dispositivoId, array $data): EventoDTO
    {
        if (!$this->dispositivoRepository->findById($dispositivoId)) {
            throw new Exception('Dispositivo não encontrado.', 404);
        }

        $data['dispositivo_id'] = $dispositivoId;

        $rules = [
            'dispositivo_id' => 'required|integer',
            'tipo_evento_id' => 'required|integer',
            'status_evento_id' => 'required|integer'
        ];

        if (!Validator::validate($data, $rules)) {
            throw new Exception(json_encode(Validator::getErrors()), 422);
        }

        $eventoId = $this->eventoRepository->save($data);
        if (!$eventoId) {
            throw new Exception('Falha ao registar o evento.', 500);
        }
        
        // Embora o repositório não tenha um findById, podemos construir o DTO com os dados que temos
        // para uma resposta mais completa, ou simplesmente retornar o ID.
        // Por consistência, vamos assumir que o controller só precisa do ID por enquanto.
        // Para uma API RESTful completa, um método findById no repo seria ideal.
        return new EventoDTO(
            id: $eventoId,
            dispositivo_id: $data['dispositivo_id'],
            tipo_evento_id: $data['tipo_evento_id'],
            status_evento_id: $data['status_evento_id'],
            response_time_ms: $data['response_time_ms'] ?? null,
            mensagem_original: $data['mensagem_original'] ?? null,
            horario: date('Y-m-d H:i:s') // Aproximação do horário
        );
    }
}
```

### `src\Services\ImportService.php`

```php
<?php
namespace App\Services;

use App\Models\Database;
use App\Models\Torre;
use App\Models\Dispositivo;
use App\Models\TipoDispositivo;
use PDO;

class ImportService
{
    private PDO $db;

    private const REGRAS_TIPO_DISPOSITIVO = [
        'SWITCH' => 'Switch',
        'ROUTER' => 'Roteador',
        'RB' => 'Roteador',
        'OLT' => 'OLT',
        'PTP' => 'Rádio - PTP',
        'PMP' => 'Rádio - PMP',
        'MIKROTIK' => 'Rádio - Ubiquiti/Mikrotik',
        'UBNT' => 'Rádio - Ubiquiti/Mikrotik',
        'UBIQUITI' => 'Rádio - Ubiquiti/Mikrotik',
        'CAMBIUM' => 'Antena - Cambium',
        'NET.S' => 'Antena - NET.S',
        'ANTENA' => 'Antena',
        'ONU' => 'ONU',
        'SERVIDOR' => 'Servidor',
        'SERVER' => 'Servidor',
        'PC' => 'Servidor',
        'NOBREAK' => 'Nobreak',
        'UPS' => 'Nobreak'
    ];

    public function __construct()
    {
        $this->db = Database::getInstance();
    }

    /**
     * Converte uma string de coordenada em formato DMS (Graus, Minutos, Segundos)
     * para o formato DD (Graus Decimais).
     * Ex: " 23°34'49.47""S" -> -23.58040833
     */
    private function convertDMSToDD($dms_string): ?float
    {
        $dms_string = trim($dms_string);
        if (empty($dms_string)) {
            return null;
        }

        // Limpa a string, mantendo apenas números, pontos e as letras de direção
        $dms_string = preg_replace('/[^\d\.NSEWO]/i', ' ', $dms_string);
        $parts = preg_split('/\s+/', $dms_string, -1, PREG_SPLIT_NO_EMPTY);

        if (count($parts) < 3) {
            return null; // Formato inválido
        }

        $degrees = (float) ($parts[0] ?? 0);
        $minutes = (float) ($parts[1] ?? 0);
        $seconds = (float) ($parts[2] ?? 0);

        $decimal = $degrees + ($minutes / 60) + ($seconds / 3600);

        // Verifica a última parte para a direção (Sul/Oeste são negativos)
        $direction = strtoupper(end($parts));
        if ($direction === 'S' || $direction === 'O' || $direction === 'W') {
            $decimal *= -1;
        }

        return $decimal;
    }

    private function getStatusId(string $statusDescricao, int $defaultId = 1): int
    {
        try {
            $stmt = $this->db->prepare("SELECT id FROM status_tipos WHERE LOWER(TRIM(descricao)) = LOWER(TRIM(:descricao)) LIMIT 1");
            $stmt->bindValue(':descricao', $statusDescricao);
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);

            if (is_array($result) && isset($result['id'])) {
                return (int) $result['id'];
            }
            return $defaultId;

        } catch (\Exception $e) {
            error_log("Erro ao buscar ID do status '{$statusDescricao}': " . $e->getMessage());
            return $defaultId;
        }
    }

    /**
     * Importar torres do CSV (VERSÃO FINAL com conversão de coordenadas DMS)
     */
    public function importTorres(array $csvData): array
    {
        $results = [
            'total_processadas' => count($csvData),
            'adicionadas' => 0,
            'atualizadas' => 0,
            'dependencias_criadas' => 0,
            'erros' => 0,
            'detalhes_erros' => [],
            'success' => true
        ];
        $torreMap = []; // Mapeia nome da torre -> novo ID no banco

        try {
            $this->db->beginTransaction();

            // FASE 1: Inserir ou atualizar todas as torres, mas sem as dependências.
            foreach ($csvData as $linha => $dados) {
                try {
                    $nomeDaTorre = trim($dados['nome_equipamento'] ?? $dados['nome_torre'] ?? $dados['nome'] ?? '');
                    if (empty($nomeDaTorre))
                        throw new \Exception("Nome da torre em branco");

                    $statusId = $this->getStatusId(trim($dados['status_geral'] ?? 'Ativo') === 'Ativo' ? 'Online' : trim($dados['status_geral']), 1);

                    $torreData = [
                        'nome' => $nomeDaTorre,
                        'localizacao' => trim($dados['localizacao'] ?? '') ?: null,
                        'latitude' => $this->convertDMSToDD($dados['latitude'] ?? null),
                        'longitude' => $this->convertDMSToDD($dados['longitude'] ?? null),
                        'status_geral' => $statusId,
                        'uptime_percentage' => !empty($dados['uptime_percentage']) ? (float) $dados['uptime_percentage'] : 100.0,
                        'observacoes' => trim($dados['observacoes'] ?? '') ?: null,
                        'depende_de_torre_id' => null // Força a dependência como nula na primeira fase
                    ];

                    $existingTorre = Torre::findByName($torreData['nome']);
                    if ($existingTorre) {
                        Torre::update($existingTorre['id'], $torreData);
                        $results['atualizadas']++;
                        $torreMap[$nomeDaTorre] = $existingTorre['id'];
                    } else {
                        $newId = Torre::save($torreData);
                        if (!$newId)
                            throw new \Exception("Falha ao salvar a torre");
                        $results['adicionadas']++;
                        $torreMap[$nomeDaTorre] = $newId;
                    }
                } catch (\Exception $e) {
                    $results['erros']++;
                    $results['detalhes_erros'][] = ['linha' => $linha + 2, 'torre' => $nomeDaTorre ?? 'N/A', 'erro' => "Fase 1: " . $e->getMessage()];
                }
            }

            // FASE 2: Atualizar as dependências, agora que todas as torres existem.
            foreach ($csvData as $linha => $dados) {
                try {
                    $nomeDaTorre = trim($dados['nome_equipamento'] ?? $dados['nome_torre'] ?? $dados['nome'] ?? '');
                    $dependeDeTorreNome = trim($dados['depende_de_torre_id'] ?? '');

                    if (!empty($nomeDaTorre) && !empty($dependeDeTorreNome)) {
                        $torreId = $torreMap[$nomeDaTorre] ?? null;
                        $torrePaiId = $torreMap[$dependeDeTorreNome] ?? null;

                        if ($torreId && $torrePaiId) {
                            Torre::update($torreId, ['depende_de_torre_id' => $torrePaiId]);
                            $results['dependencias_criadas']++;
                        } else if (!$torrePaiId) {
                            throw new \Exception("Torre pai '{$dependeDeTorreNome}' não encontrada no CSV.");
                        }
                    }
                } catch (\Exception $e) {
                    $results['erros']++;
                    $results['detalhes_erros'][] = ['linha' => $linha + 2, 'torre' => $nomeDaTorre ?? 'N/A', 'erro' => "Fase 2: " . $e->getMessage()];
                }
            }

            if ($results['erros'] > 0) {
                $results['success'] = false;
                $this->db->rollBack();
            } else {
                $this->db->commit();
            }

        } catch (\Exception $e) {
            $this->db->rollBack();
            $results['success'] = false;
            $results['erro_geral'] = 'Erro fatal na transação: ' . $e->getMessage();
        }
        return $results;
    }


    /**
     * Importar equipamentos do CSV
     * VERSÃO FINAL com inicialização correta de resultados.
     */
    public function importEquipamentos(array $csvData): array
    {
        // CORREÇÃO: Inicializamos o array $results com todas as chaves necessárias.
        $results = [
            'total_processadas' => 0,
            'adicionadas' => 0,
            'atualizadas' => 0,
            'erros' => 0,
            'torres_criadas' => 0,
            'tipos_criados' => 0, // Adicionando esta métrica para o 'findOrCreate'
            'detalhes_erros' => [],
            'success' => true
        ];

        try {
            $this->db->beginTransaction();

            foreach ($csvData as $linha => $dados) {
                $results['total_processadas']++;
                $nomeDaTorre = null;
                $nomeDoEquipamento = null;

                try {
                    $nomeDaTorre = trim($dados['nome_torre'] ?? '');
                    $nomeDoEquipamento = trim($dados['nome_equipamento'] ?? '');
                    $ip = trim($dados['ip'] ?? '');

                    if (empty($nomeDaTorre) || empty($nomeDoEquipamento) || empty($ip)) {
                        throw new \Exception("Colunas obrigatórias (Torre, Nome, IP) em branco.");
                    }

                    $torre = Torre::findByName($nomeDaTorre);
                    if (!$torre) {
                        $torreId = Torre::save(['nome' => $nomeDaTorre, 'status_geral' => 1]);
                        if (!$torreId) throw new \Exception("Falha ao criar torre automaticamente: " . $nomeDaTorre);
                        $results['torres_criadas']++;
                        $torre = ['id' => $torreId]; 
                    }

                    $tipoNomeInferido = $this->inferirTipoDeDispositivo($nomeDoEquipamento);
                    
                    $tipoId = TipoDispositivo::findOrCreate($tipoNomeInferido);
                    if (!$tipoId) throw new \Exception("Falha ao buscar/criar tipo de dispositivo: " . $tipoNomeInferido);

                    $dispositivoData = [
                        'torre_id' => $torre['id'],
                        'tipo_dispositivo_id' => $tipoId,
                        'nome' => $nomeDoEquipamento,
                        'ip' => $ip,
                        'status' => '1' 
                    ];

                    $existingDispositivo = Dispositivo::findByTorreAndName($torre['id'], $nomeDoEquipamento);

                    if ($existingDispositivo) {
                        if (!Dispositivo::update($existingDispositivo['id'], $dispositivoData)) throw new \Exception("Falha ao atualizar dispositivo");
                        $results['atualizadas']++;
                    } else {
                        $dispositivoId = Dispositivo::save($dispositivoData);
                        if (!$dispositivoId) throw new \Exception("Falha ao criar novo dispositivo");
                        $results['adicionadas']++;
                    }

                } catch (\Exception $e) {
                    $results['erros']++;
                    $results['detalhes_erros'][] = [
                        'linha' => $linha + 2,
                        'torre' => $nomeDaTorre ?? 'N/A',
                        'equipamento' => $nomeDoEquipamento ?? 'N/A',
                        'erro' => $e->getMessage()
                    ];
                    continue;
                }
            }

            if ($results['erros'] > 0) { $results['success'] = false; }

            if ($results['success']) { 
                $this->db->commit();
            } else { 
                $this->db->rollBack();
            }

        } catch (\Exception $e) {
            $this->db->rollBack();
            $results['success'] = false;
            $results['erro_geral'] = 'Erro fatal na transação: ' . $e->getMessage();
        }

        return $results;
    }

    /**
     * Nova função privada para aplicar as regras de inferência de tipo.
     */
    private function inferirTipoDeDispositivo(string $nomeDoEquipamento): string
    {
        $nomeUpper = strtoupper($nomeDoEquipamento);

        foreach (self::REGRAS_TIPO_DISPOSITIVO as $palavraChave => $tipoResultante) {
            if (strpos($nomeUpper, $palavraChave) !== false) {
                // Se a palavra-chave for a categoria, retorna só a categoria (ex: SWITCH -> Switch)
                if (strtoupper($palavraChave) === strtoupper($tipoResultante)) {
                    return $tipoResultante;
                }
                // Retorna a combinação (ex: PTP -> Rádio - PTP)
                return $tipoResultante;
            }
        }

        // Se nenhuma regra corresponder, retorna o tipo padrão.
        return 'Dispositivo Desconhecido';
    }

    /**
     * Criar entrada na tabela de monitoramento para novo dispositivo
     */
    private function createMonitoramento(int $dispositivoId, int $statusInicial = 1): bool
    {
        try {
            $query = "
                INSERT INTO monitoramento (dispositivo_id, status_atual, ultima_atualizacao, uptime_percentage, created_at, updated_at)
                VALUES (:dispositivo_id, :status_atual, NOW(), 100.0, NOW(), NOW())
            ";

            $stmt = $this->db->prepare($query);
            $stmt->bindValue(':dispositivo_id', $dispositivoId, PDO::PARAM_INT);
            $stmt->bindValue(':status_atual', $statusInicial, PDO::PARAM_INT);

            return $stmt->execute();

        } catch (\Exception $e) {
            error_log("Erro ao criar monitoramento: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Atualizar entrada na tabela de monitoramento
     */
    private function updateMonitoramento(int $dispositivoId, int $novoStatus): bool
    {
        try {
            $query = "
                UPDATE monitoramento 
                SET status_atual = :status_atual, ultima_atualizacao = NOW(), updated_at = NOW()
                WHERE dispositivo_id = :dispositivo_id
            ";

            $stmt = $this->db->prepare($query);
            $stmt->bindValue(':dispositivo_id', $dispositivoId, PDO::PARAM_INT);
            $stmt->bindValue(':status_atual', $novoStatus, PDO::PARAM_INT);

            return $stmt->execute();

        } catch (\Exception $e) {
            error_log("Erro ao atualizar monitoramento: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Processa o conteúdo de um arquivo CSV, convertendo-o em um array associativo.
     * ESTA É A VERSÃO FINAL CORRIGIDA, que silencia os avisos do fgetcsv.
     */
    public function processCSV(string $csvContent): array
    {
        // Remove o BOM (caractere invisível) do início do arquivo, se existir
        if (substr($csvContent, 0, 3) === "\xEF\xBB\xBF") {
            $csvContent = substr($csvContent, 3);
        }

        $data = [];
        $tempFile = fopen('php://memory', 'r+');
        fwrite($tempFile, $csvContent);
        rewind($tempFile); // Volta o ponteiro para o início do "arquivo"

        // Lê a primeira linha para pegar os cabeçalhos
        // CORREÇÃO APLICADA: Adicionados os parâmetros '"' (enclosure) e '\\' (escape)
        $headers = fgetcsv($tempFile, 0, ';', '"', '\\');

        if ($headers === false) {
            fclose($tempFile);
            throw new \Exception('Não foi possível ler os cabeçalhos do arquivo CSV.');
        }

        $normalizedHeaders = array_map([$this, 'normalizeHeader'], $headers);
        $headerCount = count($normalizedHeaders);

        // Lê o restante do arquivo, linha por linha
        while (($row = fgetcsv($tempFile, 0, ';', '"', '\\')) !== false) { // <-- CORREÇÃO APLICADA AQUI TAMBÉM

            if (empty(array_filter($row, fn($value) => $value !== null && $value !== ''))) {
                continue; // Pula a linha se estiver completamente vazia
            }

            if (count($row) !== $headerCount) {
                $row = array_pad($row, $headerCount, '');
            }

            // Garante que o array combinado não tenha erros se as contagens divergirem
            if (count($normalizedHeaders) == count($row)) {
                $data[] = array_combine($normalizedHeaders, $row);
            }
        }

        fclose($tempFile);
        return $data;
    }

    /**
     * Normalizar cabeçalho do CSV
     */
    private function normalizeHeader(string $header): string
    {
        // Mapeamento de cabeçalhos comuns
        $headerMap = [
            'torre' => 'nome_torre',
            'nome torre' => 'nome_torre',
            'nome_torre' => 'nome_torre',
            'nome' => 'nome_equipamento',
            'equipamento' => 'nome_equipamento',
            'nome equipamento' => 'nome_equipamento',
            'nome_equipamento' => 'nome_equipamento',
            'ip' => 'ip',
            'endereco ip' => 'ip',
            'endereco_ip' => 'ip',
            'tipo' => 'tipo_equipamento',
            'tipo equipamento' => 'tipo_equipamento',
            'tipo_equipamento' => 'tipo_equipamento',
            'localizacao' => 'localizacao',
            'localização' => 'localizacao',
            'endereco' => 'endereco',
            'endereço' => 'endereco',
            'latitude' => 'latitude',
            'longitude' => 'longitude',
            'status' => 'status',
            'uptime' => 'uptime',
            'observacoes' => 'observacoes',
            'observações' => 'observacoes',
            'mac' => 'mac',
            'mac address' => 'mac',
            'mac_address' => 'mac'
        ];

        $normalized = trim(strtolower($header));
        $normalized = preg_replace('/[^a-z0-9_\s]/', '', $normalized);
        $normalized = trim($normalized);

        return $headerMap[$normalized] ?? $normalized;
    }

    /**
     * Validar estrutura do CSV para torres
     */
    public function validateTorresCSV(array $data): array
    {
        $errors = [];

        if (empty($data)) {
            $errors[] = 'Arquivo CSV não contém dados válidos';
            return $errors;
        }

        $firstRow = $data[0];

        // CORREÇÃO APLICADA AQUI:
        // Verifica se existe QUALQUER UMA das chaves possíveis para o nome da torre
        // após a normalização do cabeçalho.
        $nomeKeyFound = array_key_exists('nome', $firstRow) ||
            array_key_exists('nome_torre', $firstRow) ||
            array_key_exists('nome_equipamento', $firstRow);

        if (!$nomeKeyFound) {
            $errors[] = "Campo obrigatório não encontrado: nome";
        }

        return $errors;
    }

    /**
     * Validar estrutura do CSV para equipamentos  
     */
    public function validateEquipamentosCSV(array $data): array
    {
        $errors = [];
        $requiredFields = ['nome_torre', 'nome_equipamento', 'ip'];

        if (empty($data)) {
            $errors[] = 'Arquivo CSV não contém dados válidos';
            return $errors;
        }

        // Verificar se tem campos obrigatórios
        $firstRow = $data[0];
        foreach ($requiredFields as $field) {
            if (!array_key_exists($field, $firstRow)) {
                $errors[] = "Campo obrigatório não encontrado: $field";
            }
        }

        return $errors;
    }
}
?>
```

### `src\Services\MapaService.php`

```php
<?php
namespace App\Services;

use App\Models\Database;
use PDO;

class MapaService
{
    private PDO $db;

    public function __construct()
    {
        $this->db = Database::getInstance();
    }

    /**
     * Buscar torres com coordenadas válidas para exibir no mapa
     */
    public function getTorresComCoordenadas(): array
    {
        try {
            // CORREÇÃO: A query foi padronizada para usar apenas 't.status_geral'.
            $query = "
                SELECT 
                    t.id, t.nome, t.localizacao, t.latitude, t.longitude, 
                    t.status_geral, -- Usando o nome correto da coluna
                    t.uptime_percentage, t.last_check,
                    st.descricao as status_descricao,
                    st.cor_hex as status_cor
                FROM torres t
                LEFT JOIN status_tipos st ON t.status_geral = st.id -- JOIN corrigido
                WHERE t.latitude IS NOT NULL 
                  AND t.longitude IS NOT NULL
                  AND t.latitude != 0 
                  AND t.longitude != 0
                ORDER BY t.nome ASC
            ";

            $stmt = $this->db->prepare($query);
            $stmt->execute();
            $torres = $stmt->fetchAll(PDO::FETCH_ASSOC);

            if (empty($torres)) {
                error_log("⚠️ MapaService: Nenhuma torre com coordenadas encontrada");
                return [];
            }

            error_log("🗺️ MapaService: " . count($torres) . " torres encontradas com coordenadas");

            $torreIds = array_column($torres, 'id');
            if (empty($torreIds))
                return []; // Segurança para evitar query IN () vazia

            $placeholders = implode(',', array_fill(0, count($torreIds), '?'));

            $deviceQuery = "
                SELECT 
                    d.torre_id,
                    COUNT(*) as total,
                    COUNT(CASE WHEN d.status = '1' THEN 1 END) as online,
                    COUNT(CASE WHEN d.status = '2' THEN 1 END) as offline
                FROM dispositivos d
                WHERE d.torre_id IN ($placeholders)
                GROUP BY d.torre_id
            ";

            $deviceStmt = $this->db->prepare($deviceQuery);
            $deviceStmt->execute($torreIds);

            $deviceResults = $deviceStmt->fetchAll(PDO::FETCH_ASSOC);
            $deviceCounts = [];
            foreach ($deviceResults as $row) {
                $deviceCounts[$row['torre_id']] = $row;
            }

            $result = array_map(function ($torre) use ($deviceCounts) {
                $dispositivos = $deviceCounts[$torre['id']] ?? ['total' => 0, 'online' => 0, 'offline' => 0];

                return [
                    'id' => (int) $torre['id'],
                    'nome' => $torre['nome'],
                    'localizacao' => $torre['localizacao'],
                    'latitude' => (float) $torre['latitude'],
                    'longitude' => (float) $torre['longitude'],
                    'status' => [
                        // CORREÇÃO: Ajustado para ler 'status_geral'
                        'id' => (int) $torre['status_geral'],
                        'descricao' => $torre['status_descricao'] ?? 'Desconhecido',
                        'cor' => $torre['status_cor'] ?? '#999999'
                    ],
                    'uptime' => (float) ($torre['uptime_percentage'] ?? 0),
                    'lastcheck' => $torre['last_check'] ?? null,
                    'dispositivos' => [],
                    'dispositivos_stats' => [
                        'total' => (int) $dispositivos['total'],
                        'online' => (int) $dispositivos['online'],
                        'offline' => (int) $dispositivos['offline']
                    ]
                ];
            }, $torres);

            error_log("✅ MapaService: Dados processados com sucesso");
            return $result;

        } catch (\Exception $e) {
            error_log("❌ Erro em getTorresComCoordenadas: " . $e->getMessage());
            error_log("Stack trace: " . $e->getTraceAsString());
            return [];
        }
    }

    /**
     * Buscar dispositivos detalhados de uma torre específica (NÃO FOI ALTERADO)
     */
    private function getDispositivosDaTorre(int $torreId): array
    {
        try {
            $query = "
                SELECT 
                    d.id, d.nome, d.ip, d.localizacao,
                    d.status as status_atual,
                    st.descricao as status_descricao,
                    st.cor_hex as status_cor
                FROM dispositivos d
                LEFT JOIN status_tipos st ON CAST(d.status AS INTEGER) = st.id
                WHERE d.torre_id = :torreId
                ORDER BY d.nome
            ";
            $stmt = $this->db->prepare($query);
            $stmt->bindValue(':torreId', $torreId, PDO::PARAM_INT);
            $stmt->execute();
            $dispositivos = $stmt->fetchAll(PDO::FETCH_ASSOC);

            return array_map(function ($dispositivo) {
                return [
                    'id' => (int) $dispositivo['id'],
                    'nome' => $dispositivo['nome'],
                    'ip' => $dispositivo['ip'],
                    'localizacao' => $dispositivo['localizacao'] ?? 'N/A',
                    'status' => [
                        'id' => (int) ($dispositivo['status_atual'] ?? 0),
                        'descricao' => $dispositivo['status_descricao'] ?? 'Desconhecido',
                        'cor' => $dispositivo['status_cor'] ?? '#808080'
                    ]
                ];
            }, $dispositivos);

        } catch (\Exception $e) {
            error_log("Erro em getDispositivosDaTorre: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Buscar detalhes completos de uma torre
     */
    public function getDetalhesTorre(int $id): array
    {
        try {
            error_log("🔍 MapaService: Buscando detalhes da torre ID: $id");

            // CORREÇÃO: A query foi padronizada para usar apenas 't.status_geral'.
            $queryTorre = "
                SELECT 
                    t.id, t.nome, t.localizacao, t.latitude, t.longitude,
                    t.status_geral, -- Usando o nome correto da coluna
                    t.uptime_percentage, t.last_check, t.observacoes,
                    st.descricao as status_descricao,
                    st.cor_hex as status_cor,
                    st.criticidade
                FROM torres t
                LEFT JOIN status_tipos st ON t.status_geral = st.id -- JOIN corrigido
                WHERE t.id = :id
            ";

            $stmtTorre = $this->db->prepare($queryTorre);
            $stmtTorre->bindValue(':id', $id, PDO::PARAM_INT);
            $stmtTorre->execute();

            $torre = $stmtTorre->fetch(PDO::FETCH_ASSOC);
            if (!$torre) {
                error_log("❌ MapaService: Torre ID $id não encontrada");
                return ['error' => 'Torre não encontrada', 'status' => 404];
            }

            error_log("✅ MapaService: Torre encontrada: " . $torre['nome']);

            $dispositivos = $this->getDispositivosDaTorre($id);

            return [
                'torre' => [
                    'id' => (int) $torre['id'],
                    'nome' => $torre['nome'],
                    'localizacao' => $torre['localizacao'],
                    'latitude' => (float) $torre['latitude'],
                    'longitude' => (float) $torre['longitude'],
                    'status' => [
                        // CORREÇÃO: Ajustado para ler 'status_geral'
                        'id' => (int) $torre['status_geral'],
                        'descricao' => $torre['status_descricao'],
                        'cor' => $torre['status_cor'],
                        'criticidade' => $torre['criticidade']
                    ],
                    'uptime' => (float) $torre['uptime_percentage'],
                    'last_check' => $torre['last_check'],
                    'observacoes' => $torre['observacoes'] ?? '',
                ],
                'dispositivos' => $dispositivos,
            ];
        } catch (\Exception $e) {
            error_log("❌ Erro em getDetalhesTorre: " . $e->getMessage());
            return ['error' => 'Erro ao buscar detalhes da torre', 'status' => 500];
        }
    }

    /**
     * busca todas as localizações (regiões) distintas das torres.
     * Usada para popular o dropdown de filtro no frontend.
     */
    public function getRegioesDisponiveis(): array
    {
        try {
            $query = "SELECT DISTINCT localizacao FROM torres WHERE localizacao IS NOT NULL AND localizacao != '' ORDER BY localizacao ASC";
            $stmt = $this->db->query($query);
            return $stmt->fetchAll(PDO::FETCH_COLUMN);
        } catch (\Exception $e) {
            error_log("❌ Erro em getRegioesDisponiveis: " . $e->getMessage());
            return [];
        }
    }
}
```

### `src\Services\TempoService.php`

```php
<?php
namespace App\Services;

class TempoService
{
    private const API_URL = 'https://api.open-meteo.com/v1/forecast';

    public function getTempoPorCoordenadas(float $lat, float $lon): array
    {
        $url = sprintf(
            "%s?latitude=%s&longitude=%s&current=temperature_2m,relativehumidity_2m,weathercode&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto",
            self::API_URL, $lat, $lon
        );

        $data = $this->fetch($url);

        if (empty($data) || isset($data['error'])) {
            throw new \Exception($data['reason'] ?? 'Falha ao buscar dados do tempo.');
        }

        return $this->formatarResposta($data);
    }

    private function fetch(string $url): array
    {
        $response = @file_get_contents($url);
        return json_decode($response, true) ?? [];
    }

    private function formatarResposta(array $data): array
    {
        $previsaoDiaria = [];
        $times = $data['daily']['time'] ?? [];

        // Mapa para traduzir a abreviação do dia da semana de inglês para português
        $diasSemana = [
            'Mon' => 'Seg',
            'Tue' => 'Ter',
            'Wed' => 'Qua',
            'Thu' => 'Qui',
            'Fri' => 'Sex',
            'Sat' => 'Sáb',
            'Sun' => 'Dom',
        ];

        // A linha setlocale() não é mais necessária e pode ser removida ou comentada
        // setlocale(LC_TIME, 'pt_BR.utf8', 'pt_BR', 'portuguese');

        for ($i = 1; $i < count($times) && $i <= 4; $i++) {
            // Usamos a classe DateTime para uma abordagem moderna
            $date = new \DateTime($times[$i]);
            $diaAbreviado = $date->format('D'); // Obtém 'Mon', 'Tue', etc.
            
            $weatherInfo = $this->mapWeatherCode($data['daily']['weathercode'][$i] ?? 0);

            $previsaoDiaria[] = [
                // Traduzimos para português usando o nosso mapa
                'dia_semana' => $diasSemana[$diaAbreviado] ?? $diaAbreviado,
                'temp_max' => round($data['daily']['temperature_2m_max'][$i] ?? 0),
                'temp_min' => round($data['daily']['temperature_2m_min'][$i] ?? 0),
                'condicao' => $weatherInfo['description'],
                'icone' => $weatherInfo['icon']
            ];
        }

        return [
            'agora' => [
                'temperatura' => round($data['current']['temperature_2m'] ?? 0),
                'umidade' => $data['current']['relativehumidity_2m'] ?? 0,
                'condicao' => $this->mapWeatherCode($data['current']['weathercode'] ?? 0)['description'],
                'icone' => $this->mapWeatherCode($data['current']['weathercode'] ?? 0)['icon']
            ],
            'previsao_proximos_dias' => $previsaoDiaria
        ];
    }

    private function mapWeatherCode(int $code): array
    {
        // Mapa simplificado dos códigos WMO
        $map = [
            0 => ['description' => 'Céu limpo', 'icon' => '01d'], 1 => ['description' => 'Quase limpo', 'icon' => '02d'],
            2 => ['description' => 'Parcialmente nublado', 'icon' => '03d'], 3 => ['description' => 'Nublado', 'icon' => '04d'],
            45 => ['description' => 'Nevoeiro', 'icon' => '50d'], 48 => ['description' => 'Nevoeiro gelado', 'icon' => '50d'],
            51 => ['description' => 'Chuvisco leve', 'icon' => '09d'], 53 => ['description' => 'Chuvisco', 'icon' => '09d'],
            55 => ['description' => 'Chuvisco forte', 'icon' => '09d'], 61 => ['description' => 'Chuva leve', 'icon' => '10d'],
            63 => ['description' => 'Chuva', 'icon' => '10d'], 65 => ['description' => 'Chuva forte', 'icon' => '10d'],
            71 => ['description' => 'Neve leve', 'icon' => '13d'], 73 => ['description' => 'Neve', 'icon' => '13d'],
            75 => ['description' => 'Neve forte', 'icon' => '13d'], 80 => ['description' => 'Pancadas de chuva', 'icon' => '09d'],
            81 => ['description' => 'Pancadas de chuva', 'icon' => '09d'], 82 => ['description' => 'Pancadas de chuva', 'icon' => '09d'],
            95 => ['description' => 'Trovoada', 'icon' => '11d'], 96 => ['description' => 'Trovoada', 'icon' => '11d'],
            99 => ['description' => 'Trovoada', 'icon' => '11d'],
        ];
        return $map[$code] ?? ['description' => 'Desconhecido', 'icon' => '01d'];
    }
}
```

### `src\Services\TorreService.php`

```php
<?php

namespace App\Services;

use App\Repositories\TorreRepository;
use App\DTO\TorreDTO;
use App\Core\Validator;
use Exception;

/**
 * Service para a entidade Torre.
 *
 * Contém toda a lógica de negócio da aplicação relacionada a torres.
 * Orquestra as operações, chamando o repositório para persistência de dados.
 * NÃO sabe SQL ou como os dados são armazenados.
 */
class TorreService
{
    private TorreRepository $torreRepository;

    /**
     * O construtor recebe a dependência do TorreRepository.
     */
    public function __construct(TorreRepository $torreRepository)
    {
        $this->torreRepository = $torreRepository;
    }

    /**
     * Busca todas as torres.
     *
     * @return TorreDTO[]
     */
    public function getAllTorres(): array
    {
        return $this->torreRepository->findAll();
    }

    /**
     * Busca uma torre específica pelo seu ID.
     *
     * @param int $id O ID da torre.
     * @return TorreDTO|null Retorna o DTO da torre ou null se não encontrada.
     */
    public function getTorreById(int $id): ?TorreDTO
    {
        return $this->torreRepository->findById($id);
    }

    /**
     * Cria uma nova torre após validar os dados.
     *
     * @param array $data Dados da nova torre.
     * @return TorreDTO O DTO da torre criada.
     * @throws Exception Se a validação falhar ou ocorrer um erro na criação.
     */
    public function createTorre(array $data): TorreDTO
    {
        $rules = [
            'nome' => 'required',
            'status_geral' => 'required|integer',
            'localizacao' => 'required',
            'latitude' => 'required|numeric',
            'longitude' => 'required|numeric'
        ];

        if (!Validator::validate($data, $rules)) {
            // Lança uma exceção com os erros de validação
            throw new Exception(json_encode(Validator::getErrors()));
        }
        
        // Lógica de negócio: verificar se já existe uma torre com o mesmo nome
        if ($this->torreRepository->findByName($data['nome'])) {
            throw new Exception("O nome '{$data['nome']}' já está em uso.", 409); // 409 Conflict
        }

        $torreId = $this->torreRepository->save($data);
        if (!$torreId) {
            throw new Exception("Falha ao salvar a torre no banco de dados.", 500);
        }

        $novaTorre = $this->getTorreById($torreId);
        if (!$novaTorre) {
            // Isso seria um estado inconsistente, mas é bom verificar
            throw new Exception("Não foi possível encontrar a torre recém-criada.", 500);
        }
        
        return $novaTorre;
    }

    /**
     * Atualiza uma torre existente.
     *
     * @param int $id O ID da torre a ser atualizada.
     * @param array $data Os novos dados da torre.
     * @return TorreDTO O DTO da torre atualizada.
     * @throws Exception Se a torre não for encontrada ou ocorrer um erro.
     */
    public function updateTorre(int $id, array $data): TorreDTO
    {
        $torre = $this->torreRepository->findById($id);
        if (!$torre) {
            throw new Exception('Torre não encontrada', 404);
        }

        // Lógica de negócio: se o nome está sendo alterado, verificar se já não existe
        if (isset($data['nome']) && $data['nome'] !== $torre->nome) {
            if ($this->torreRepository->findByName($data['nome'])) {
                throw new Exception("O nome '{$data['nome']}' já está em uso por outra torre.", 409);
            }
        }

        if (!$this->torreRepository->update($id, $data)) {
            throw new Exception("Falha ao atualizar a torre no banco de dados.", 500);
        }

        $torreAtualizada = $this->getTorreById($id);
         if (!$torreAtualizada) {
            throw new Exception("Não foi possível encontrar a torre recém-atualizada.", 500);
        }

        return $torreAtualizada;
    }

    /**
     * Remove uma torre do sistema.
     *
     * @param int $id O ID da torre a ser removida.
     * @return bool True em caso de sucesso.
     * @throws Exception Se a torre não for encontrada ou ocorrer um erro.
     */
    public function deleteTorre(int $id): bool
    {
        $torre = $this->torreRepository->findById($id);
        if (!$torre) {
            throw new Exception('Torre não encontrada', 404);
        }

        if (!$this->torreRepository->delete($id)) {
            throw new Exception("Falha ao remover a torre do banco de dados.", 500);
        }

        return true;
    }
}
```

### `src\Services\UserService.php`

```php
<?php
namespace App\Services;

use App\Core\Validator;
use App\Models\Usuario;

class UserService
{
    // O construtor e o método update estão corretos e podem ser mantidos como estavam antes.
    public function __construct()
    {
        // O construtor do JWT pode ser removido se não for usado em mais nenhum método aqui.
    }
    
    public function update(int $id, array $data): array
    {
        // Esta validação deve ser mais robusta, vamos melhorá-la no futuro
        if (isset($data['senha'])) {
            $data['senha'] = password_hash($data['senha'], PASSWORD_ARGON2ID);
        }
        if (!Usuario::update($id, $data)) {
            return ['error' => 'Erro ao atualizar usuário', 'status' => 500];
        }
        $user = Usuario::findById($id);
        $username = trim(($user['primeiro_nome'] ?? '') . ' ' . ($user['ultimo_nome'] ?? 'Usuário'));
        return ['message' => "Dados de {$username} atualizados com sucesso"];
    }

    /**
     * Valida a força de uma senha de acordo com as regras de segurança.
     */
    private function validarForcaDaSenha(string $senha): bool
    {
        return
            strlen($senha) >= 8 &&
            preg_match('/[A-Z]/', $senha) &&
            preg_match('/[a-z]/', $senha) &&
            preg_match('/[0-9]/', $senha) &&
            preg_match('/[\W_]/', $senha);
    }

    /**
     * Altera a senha de um usuário autenticado.
     * Recebe o ID do usuário e os dados vindos do Controller.
     */
    public function alterarSenha(int $userId, array $data): array
    {
        $rules = ['senha_atual' => 'required', 'nova_senha' => 'required', 'confirmacao_nova_senha' => 'required'];
        if (!Validator::validate($data, $rules)) {
            return ['error' => 'Dados inválidos', 'details' => Validator::getErrors(), 'status' => 422];
        }
        if (!$this->validarForcaDaSenha($data['nova_senha'])) {
            return ['error' => 'A nova senha não cumpre os requisitos de segurança.', 'status' => 422];
        }
        if ($data['nova_senha'] !== $data['confirmacao_nova_senha']) {
            return ['error' => 'A nova senha e a confirmação não coincidem.', 'status' => 422];
        }
        
        $user = Usuario::findById($userId);
        if (!$user) {
             return ['error' => 'Usuário não encontrado.', 'status' => 404];
        }
        
        $fullUser = Usuario::findByEmail($user['email']);
        if (!$fullUser || !password_verify($data['senha_atual'], $fullUser['senha'])) {
            return ['error' => 'A senha atual está incorreta.', 'status' => 403];
        }
        
        $novaSenhaHash = password_hash($data['nova_senha'], PASSWORD_ARGON2ID);
        
        if (!Usuario::update($userId, ['senha' => $novaSenhaHash])) {
            return ['error' => 'Falha ao atualizar a senha no banco de dados.', 'status' => 500];
        }

        return ['message' => 'Senha alterada com sucesso!', 'status' => 200];
    }

    /**
     * Prepara a lógica para a recuperação de senha pública.
     */
    public function recuperarSenhaPublica(array $data): array
    {
        // A lógica correta para esta função será implementada no futuro.
        return ['error' => 'Funcionalidade de recuperação de senha ainda não implementada.', 'status' => 501];
    }
}
```

### `views\auth\login.php`

```php
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?? 'Login' ?></title>
    <link rel="stylesheet" href="/assets/css/app.css">
    <style>
        /* Estilos específicos para a página de autenticação */
        body { background-color: #f5f7fa; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .auth-container { width: 100%; max-width: 400px; }
        .auth-card { background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .auth-title { font-size: 1.75rem; font-weight: 700; text-align: center; margin-bottom: 0.5rem; color: #1f2937; }
        .auth-subtitle { text-align: center; color: #6b7280; margin-bottom: 2rem; }
        .auth-form .form-group { margin-bottom: 1.5rem; }
        .auth-form label { display: block; font-weight: 500; margin-bottom: 0.5rem; font-size: 0.875rem; color: #374151; }
        .auth-form input { width: 100%; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; }
        .btn-full { width: 100%; justify-content: center; }
        .auth-link { text-align: center; margin-top: 1.5rem; font-size: 0.875rem; color: #6b7280; }
        .auth-link a { color: #3b82f6; text-decoration: none; font-weight: 500; }
        .error-box, .success-box { padding: 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.875rem; }
        .error-box { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
        .success-box { background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="auth-card">
            <h1 class="auth-title">Bem-vindo de volta!</h1>
            <p class="auth-subtitle">Faça login para aceder ao painel.</p>
            
            <form id="login-form" class="auth-form">
                <div id="message-box" style="display: none;"></div>

                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required placeholder="seu@email.com">
                </div>
                <div class="form-group">
                    <label for="senha">Senha</label>
                    <input type="password" id="senha" name="senha" required>
                </div>
                <button type="submit" class="btn btn-primary btn-full">Entrar</button>
            </form>
            
            <p class="auth-link">Não tem uma conta? <a href="/register">Registe-se</a></p>
        </div>
    </div>

    <script>
    document.getElementById('login-form').addEventListener('submit', async function(event) {
        event.preventDefault();

        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const messageBox = document.getElementById('message-box');
        
        messageBox.style.display = 'none';
        messageBox.textContent = '';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Aguarde...';

        try {
            const response = await fetch('/api/v1/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.success) {
                // O PASSO MAIS IMPORTANTE: Guardar o token no navegador
                localStorage.setItem('jwt_token', result.data.token);
                
                // Mostrar mensagem de sucesso e redirecionar
                messageBox.className = 'success-box';
                messageBox.textContent = 'Login bem-sucedido! A redirecionar...';
                messageBox.style.display = 'block';

                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                // Mostrar mensagem de erro
                const errorMessage = result.error?.details ? JSON.stringify(result.error.details) : result.error.message;
                throw new Error(errorMessage || 'Ocorreu um erro.');
            }
        } catch (error) {
            messageBox.className = 'error-box';
            messageBox.textContent = error.message;
            messageBox.style.display = 'block';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Entrar';
        }
    });

    // Verifica se há uma mensagem de sucesso na URL (vindo do registo)
    document.addEventListener('DOMContentLoaded', () => {
        const params = new URLSearchParams(window.location.search);
        if (params.get('status') === 'success') {
            const messageBox = document.getElementById('message-box');
            messageBox.className = 'success-box';
            messageBox.textContent = 'Registo efetuado com sucesso! Por favor, faça login.';
            messageBox.style.display = 'block';
        }
    });
    </script>
</body>
</html>
```

### `views\auth\register.php`

```php
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?? 'Registo' ?></title>
    <link rel="stylesheet" href="/assets/css/app.css">
    <style>
        /* Estilos específicos para a página de autenticação (reutilizados) */
        body {
            background-color: #f5f7fa;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        .auth-container {
            width: 100%;
            max-width: 400px;
        }

        .auth-card {
            background: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .auth-title {
            font-size: 1.75rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5rem;
            color: #1f2937;
        }

        .auth-subtitle {
            text-align: center;
            color: #6b7280;
            margin-bottom: 2rem;
        }

        .auth-form .form-group {
            margin-bottom: 1.5rem;
        }

        .auth-form label {
            display: block;
            font-weight: 500;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
            color: #374151;
        }

        .auth-form input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
        }

        .btn-full {
            width: 100%;
            justify-content: center;
        }

        .auth-link {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.875rem;
            color: #6b7280;
        }

        .auth-link a {
            color: #3b82f6;
            text-decoration: none;
            font-weight: 500;
        }

        .error-box {
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            font-size: 0.875rem;
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }
    </style>
</head>

<body>
    <div class="auth-container">
        <div class="auth-card">
            <h1 class="auth-title">Crie a sua Conta</h1>
            <p class="auth-subtitle">Registo rápido e fácil.</p>

            <form id="register-form" class="auth-form">
                <div id="error-message" class="error-box" style="display: none;"></div>

                <div class="form-group">
                    <label for="primeiro_nome">Primeiro Nome</label>
                    <input type="text" id="primeiro_nome" name="primeiro_nome" required>
                </div>

                <div class="form-group">
                    <label for="ultimo_nome">Último Nome</label>
                    <input type="text" id="ultimo_nome" name="ultimo_nome" required>
                </div>

                <div class="form-group">
                    <label for="celular">Celular</label>
                    <input type="tel" id="celular" name="celular" placeholder="(XX) XXXXX-XXXX" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="senha">Senha (mínimo 8 caracteres)</label>
                    <input type="password" id="senha" name="senha" required>
                </div>
                <button type="submit" class="btn btn-primary btn-full">Criar Conta</button>
            </form>

            <p class="auth-link">Já tem uma conta? <a href="/login">Faça login</a></p>
        </div>
    </div>

    <script>
        document.getElementById('register-form').addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const submitBtn = form.querySelector('button[type="submit"]');
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            const errorBox = document.getElementById('error-message');

            errorBox.style.display = 'none';
            submitBtn.disabled = true;
            submitBtn.textContent = 'A processar...';

            try {
                const response = await fetch('/api/v1/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                    body: JSON.stringify(data),
                });

                const result = await response.json();

                if (result.success) {
                    // Redireciona para a página de login com uma mensagem de sucesso
                    window.location.href = '/login?status=success';
                } else {
                    // A nossa API de registo agora retorna um objeto 'errors'
                    const errorDetails = result.error.details;
                    let errorMessage = result.error.message;

                    // Se houver detalhes, formata-os
                    if (errorDetails && typeof errorDetails === 'object') {
                        errorMessage = Object.values(errorDetails).flat().join('<br>');
                    }

                    throw new Error(errorMessage);

                }
            } catch (error) {
                errorBox.innerHTML = error.message; // Usamos innerHTML para permitir <br>
                errorBox.style.display = 'block';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Criar Conta';
            }
        });
    </script>
</body>

</html>
```

### `views\configuracoes\index.php`

```php
<?php
$title = 'Configurações';
$pageScript = '/assets/js/configuracoes.js';
?>

<div class="max-w-4xl mx-auto space-y-8">

    <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex items-center pb-4 mb-6">
            <div class="bg-blue-100 text-blue-600 rounded-lg p-2 mr-4">
                <i class="fas fa-user w-5 h-5 text-center"></i>
            </div>
            <h3 class="text-xl font-semibold text-gray-800">Dados Pessoais</h3>
        </div>
        
        <form id="perfil-form" onsubmit="salvarPerfil(event)">
            <div class="space-y-6">
                <div>
                    <label for="nome" class="block text-sm font-medium text-gray-500 mb-1">Nome Completo</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fas fa-user text-gray-400"></i>
                        </div>
                        <input type="text" id="nome" name="nome" class="block w-full pl-10 p-3 border-none rounded-md bg-gray-100 text-gray-900 cursor-not-allowed focus:ring-2 focus:ring-blue-500" disabled>
                    </div>
                </div>
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-500 mb-1">Email</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fas fa-envelope text-gray-400"></i>
                        </div>
                        <input type="email" id="email" name="email" class="block w-full pl-10 p-3 border-none rounded-md bg-gray-100 text-gray-900 cursor-not-allowed focus:ring-2 focus:ring-blue-500" disabled>
                    </div>
                </div>
            </div>
            <div class="mt-6 text-right">
                <button type="button" id="btn-editar-perfil" class="inline-flex items-center gap-2 justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"><i class="fas fa-pencil-alt"></i>Editar</button>
                <div id="acoes-edicao-perfil" class="hidden space-x-3">
                    <button type="button" id="btn-cancelar-perfil" class="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">Cancelar</button>
                    <button type="submit" id="btn-salvar-perfil" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700">Salvar Alterações</button>
                </div>
            </div>
        </form>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex items-center pb-4 mb-6">
             <div class="bg-orange-100 text-orange-600 rounded-lg p-2 mr-4">
                <i class="fas fa-lock w-5 h-5 text-center"></i>
            </div>
            <h3 class="text-xl font-semibold text-gray-800">Alterar Senha</h3>
        </div>
        <form id="senha-form" onsubmit="salvarSenha(event)">
            <div class="space-y-6">
                <div>
                    <label for="senha_atual" class="block text-sm font-medium text-gray-500 mb-1">Senha Atual</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i class="fas fa-key text-gray-400"></i></div>
                        <input type="password" id="senha_atual" name="senha_atual" placeholder="••••••••" required class="block w-full pl-10 p-3 border-none rounded-md bg-gray-100 text-gray-900 focus:ring-2 focus:ring-blue-500">
                    </div>
                </div>
                <div>
                    <label for="nova_senha" class="block text-sm font-medium text-gray-500 mb-1">Nova Senha</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i class="fas fa-lock text-gray-400"></i></div>
                        <input type="password" id="nova_senha" name="nova_senha" placeholder="Digite sua nova senha" required class="block w-full pl-10 p-3 border-none rounded-md bg-gray-100 text-gray-900 focus:ring-2 focus:ring-blue-500">
                    </div>
                </div>
                
                <div id="password-requirements" class="text-sm text-gray-500 space-y-1 pl-2 pt-2">
                    <div id="req-length" class="flex items-center gap-2"><i class="fas fa-times-circle text-red-400"></i> Mínimo 8 caracteres</div>
                    <div id="req-uppercase" class="flex items-center gap-2"><i class="fas fa-times-circle text-red-400"></i> Pelo menos 1 letra maiúscula</div>
                    <div id="req-number" class="flex items-center gap-2"><i class="fas fa-times-circle text-red-400"></i> Pelo menos 1 número</div>
                    <div id="req-special" class="flex items-center gap-2"><i class="fas fa-times-circle text-red-400"></i> Pelo menos 1 caractere especial</div>
                </div>

                <div>
                    <label for="confirmacao_nova_senha" class="block text-sm font-medium text-gray-500 mb-1">Confirmar Nova Senha</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i class="fas fa-check-circle text-gray-400"></i></div>
                        <input type="password" id="confirmacao_nova_senha" name="confirmacao_nova_senha" placeholder="Confirme a nova senha" required class="block w-full pl-10 p-3 border-none rounded-md bg-gray-100 text-gray-900 focus:ring-2 focus:ring-blue-500">
                    </div>
                </div>
            </div>
            <div class="mt-6 text-right">
                <button type="submit" class="inline-flex items-center gap-2 justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"><i class="fas fa-save"></i>Alterar Senha</button>
            </div>
        </form>
    </div>
</div>

<div id="notification-toast" class="hidden fixed top-5 right-5 p-4 rounded-md shadow-lg text-white transition-all duration-300 z-50"></div>
```

### `views\dashboard\index.php`

```php
<?php
$title = 'Dashboard';
$pageScript = '/assets/js/dashboard.js';
?>

<section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
            <p class="text-sm font-medium text-gray-500">Total de Torres</p>
            <p class="text-3xl font-bold text-gray-800" id="kpi-total-torres">...</p>
        </div>
        <div class="bg-indigo-100 text-indigo-600 rounded-full p-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"></path></svg>
        </div>
    </div>
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
            <p class="text-sm font-medium text-gray-500">Torres Online</p>
            <p class="text-3xl font-bold text-green-600" id="kpi-torres-online">...</p>
        </div>
        <div class="bg-green-100 text-green-600 rounded-full p-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
    </div>
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
            <p class="text-sm font-medium text-gray-500">Torres Offline</p>
            <p class="text-3xl font-bold text-red-600" id="kpi-torres-offline">...</p>
        </div>
        <div class="bg-red-100 text-red-600 rounded-full p-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
    </div>
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
            <p class="text-sm font-medium text-gray-500">Uptime Médio</p>
            <p class="text-3xl font-bold text-gray-800" id="kpi-uptime-medio">...<span class="text-lg">%</span></p>
        </div>
        <div class="bg-blue-100 text-blue-600 rounded-full p-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
        </div>
    </div>
</section>

<main id="dashboard-main-content">
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md flex flex-col min-h-[350px]">
            <h3 class="text-lg font-medium text-gray-800 mb-4">Dispositivos por Status</h3>
            <div id="status-chart-container" class="flex-grow flex items-center justify-center text-gray-400">
                <p>A carregar...</p>
            </div>
        </div>
        <div class="lg:col-span-2 bg-white p-6 rounded-lg shadow-md flex flex-col min-h-[350px]">
            <h3 class="text-lg font-medium text-gray-800 mb-4">Inventário por Tipo de Dispositivo</h3>
            <div id="tipos-chart-container" class="flex-grow flex items-center justify-center text-gray-400">
                <p>A carregar...</p>
            </div>
        </div>
    </section>

    <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <div class="bg-white p-6 rounded-lg shadow-md min-h-[300px]">
            <h3 class="text-lg font-medium text-gray-800 mb-4">Top 5 Torres Críticas</h3>
            <div id="torres-criticas-list" class="space-y-4">
                 <p class="text-center text-gray-500 py-8">A carregar...</p>
            </div>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md min-h-[300px]">
            <h3 class="text-lg font-medium text-gray-800 mb-4">Visão Geral das Torres</h3>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Torre</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Dispositivos</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uptime</th>
                        </tr>
                    </thead>
                    <tbody id="visao-geral-torres-body" class="bg-white divide-y divide-gray-200">
                        <tr>
                            <td colspan="4" class="p-8 text-center text-gray-500">A carregar...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</main>

<div id="welcome-panel-container"></div>
```

### `views\layouts\app.php`

```php
<!DOCTYPE html>
<html lang="pt-BR" class="h-full">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $title ?? 'BRDK Monitoramento'; ?></title>
    <link rel="stylesheet" href="/dist/output.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
</head>

<body class="h-full font-sans bg-gray-100 dark:bg-gray-900">

    <div class="flex h-screen">
        <aside
            class="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col flex-shrink-0">
            <div class="h-20 flex items-center justify-center p-4 border-b border-gray-200 dark:border-gray-700">
                <a href="/dashboard"><img src="/assets/img/logo-brdk.png" alt="Logo BRDK Monitoramento"
                        class="h-12"></a>
            </div>

            <nav class="flex-grow px-4 py-4">
                <?php $current_page = $_SERVER['REQUEST_URI']; ?>
                <a href="/dashboard"
                    class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors duration-200 <?php echo (str_starts_with($current_page, '/dashboard')) ? 'bg-blue-50 dark:bg-gray-700/50 text-blue-600 dark:text-blue-400 font-semibold' : 'font-medium'; ?>"><i
                        class="fas fa-tachometer-alt w-5 h-5 mr-3 text-center"></i><span>Dashboard</span></a>
                <a href="/mapa"
                    class="mt-2 flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors duration-200 <?php echo (str_starts_with($current_page, '/mapa')) ? 'bg-blue-50 dark:bg-gray-700/50 text-blue-600 dark:text-blue-400 font-semibold' : 'font-medium'; ?>"><i
                        class="fas fa-map-marked-alt w-5 h-5 mr-3 text-center"></i><span>Mapa</span></a>
                <a href="/torres"
                    class="mt-2 flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors duration-200 <?php echo (str_starts_with($current_page, '/torres')) ? 'bg-blue-50 dark:bg-gray-700/50 text-blue-600 dark:text-blue-400 font-semibold' : 'font-medium'; ?>"><i
                        class="fas fa-broadcast-tower w-5 h-5 mr-3 text-center"></i><span>Torres</span></a>
                <a href="/configuracoes"
                    class="mt-2 flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors duration-200 <?php echo (str_starts_with($current_page, '/configuracoes')) ? 'bg-blue-50 dark:bg-gray-700/50 text-blue-600 dark:text-blue-400 font-semibold' : 'font-medium'; ?>"><i
                        class="fas fa-cog w-5 h-5 mr-3 text-center"></i><span>Configurações</span></a>
            </nav>

            <div class="mt-auto text-center px-4 pb-2">
                <span class="text-xs text-gray-400 dark:text-gray-500">Versão <?= APP_VERSION ?? '1.0.0' ?></span>
            </div>
            <div class="p-4 border-t border-gray-200 dark:border-gray-700">
                <button id="logout-button" class="w-full flex items-center justify-center ...">
                    <i class="fas fa-sign-out-alt w-5 h-5 mr-3"></i>
                    Sair
                </button>
            </div>
        </aside>

        <div class="flex-1 flex flex-col overflow-hidden">
            <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
                <div class="flex items-center justify-between px-6 h-20">
                    <h1 class="text-xl font-semibold text-gray-800 dark:text-gray-100"><?php echo $title ?? 'Página'; ?>
                    </h1>
                    <div class="flex items-center gap-4">
                        <button id="open-import-modal"
                            class="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"><i
                                class="fas fa-upload"></i> <span class="hidden sm:inline">Importar CSV</span></button>
                        <div class="w-px h-6 bg-gray-200 dark:bg-gray-600"></div>
                        <div id="user-info" class="user-profile flex items-center gap-3">
                            <div id="user-avatar"
                                class="w-9 h-9 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center font-bold text-gray-600 dark:text-gray-300 text-xs">
                                --</div>
                            <div class="hidden md:block"><span id="user-name"
                                    class="block font-medium text-gray-700 dark:text-gray-300 text-sm">Carregando...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>
            <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
                <?php if (isset($content)) {
                    echo $content;
                } ?>
            </main>
        </div>
    </div>

    <?php
    $modalPath = __DIR__ . '/../partials/_import_modal.php';
    if (file_exists($modalPath)) {
        include $modalPath;
    }
    ?>

    <div id="logout-confirmation-modal"
        class="hidden fixed inset-0 bg-gray-900 bg-opacity-60 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-2xl w-full max-w-sm transform transition-all p-6 text-center">
            <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100">
                <i class="fas fa-exclamation-triangle text-yellow-600 fa-lg"></i>
            </div>
            <h3 class="mt-4 text-lg font-semibold text-gray-800">Encerrar Sessão</h3>
            <p class="mt-2 text-sm text-gray-600">Tem a certeza que deseja sair da sua conta?</p>
            <div class="mt-6 flex justify-center gap-3">
                <button id="btn-logout-cancel"
                    class="py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">Cancelar</button>
                <button id="btn-logout-confirm"
                    class="py-2 px-4 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">Sim,
                    Sair</button>
            </div>
        </div>
    </div>

    <script src="/assets/js/api.js"></script>
    <script src="/assets/js/app.js"></script>
    <script src="/assets/js/components/import-modal.js"></script>
    <script src="/assets/js/components/emptyStateManager.js"></script>
    <?php if (!empty($pageScript)): ?>
        <script src="<?= htmlspecialchars($pageScript) ?>"></script>
    <?php endif; ?>
</body>

</html>
```

### `views\mapa\index.php`

```php
<?php
$title = 'Mapa de Torres';
$pageScript = '/assets/js/mapa.js';
?>

<div class="relative h-full w-full rounded-lg shadow-md overflow-hidden">

    <div id="mapa" class="w-full h-full z-0"></div>

    <div id="map-empty-state-container"
        class="absolute inset-0 z-30 bg-white/70 backdrop-blur-sm flex items-center justify-center pointer-events-none"
        style="display: none;">
    </div>

    <aside id="detalhes-torre-painel"
        class="absolute top-0 left-0 h-full w-full max-w-sm bg-white shadow-2xl z-20 transform -translate-x-full transition-transform duration-300 ease-in-out flex flex-col">
    </aside>

    <div class="absolute top-0 left-0 right-0 p-4 z-10 pointer-events-none">
        <div class="flex flex-col md:flex-row items-start justify-between gap-4">

            <div class="bg-white p-4 rounded-lg shadow-lg flex items-center gap-4 pointer-events-auto">
                <div class="flex-1">
                    <label for="filtro-status" class="block text-xs font-medium text-gray-600">Status</label>
                    <select id="filtro-status"
                        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                        <option value="todos">Todos</option>
                        <option value="online">Online</option>
                        <option value="offline">Offline</option>
                    </select>
                </div>
                <div class="flex-1">
                    <label for="filtro-regiao" class="block text-xs font-medium text-gray-600">Localização</label>
                    <select id="filtro-regiao"
                        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                        <option value="todas">Todas as Regiões</option>
                    </select>
                </div>
            </div>

            <div id="mapa-summary-widget" class="bg-white p-4 rounded-lg shadow-lg pointer-events-auto block">
                <h3 class="font-semibold text-gray-700 text-sm mb-2">Torres Visíveis</h3>
                <div class="flex items-center justify-between gap-6">
                    <div class="text-center">
                        <p id="summary-total" class="text-2xl font-bold text-gray-800">0</p>
                        <p class="text-xs text-gray-500">Total</p>
                    </div>
                    <div class="text-center">
                        <p id="summary-online" class="text-2xl font-bold text-green-600">0</p>
                        <p class="text-xs text-gray-500">Online</p>
                    </div>
                    <div class="text-center">
                        <p id="summary-offline" class="text-2xl font-bold text-red-600">0</p>
                        <p class="text-xs text-gray-500">Offline</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<template id="detalhes-torre-template">
    <div class="flex flex-col h-full">
        <div class="flex-shrink-0 p-4 border-b border-gray-200 flex items-center justify-between">
            <h2 data-template-id="nome-torre" class="font-semibold text-gray-800 text-lg truncate"
                title="Nome da Torre">A carregar...</h2>
            <button data-template-id="btn-fechar"
                class="text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
        </div>

        <div class="flex-grow overflow-y-auto p-4 space-y-4">
            <div class="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                <div class="flex justify-between items-center">
                    <strong class="font-medium text-gray-600">Status:</strong>
                    <span data-template-id="status-torre"
                        class="font-semibold px-2 py-0.5 rounded-full text-xs">--</span>
                </div>
                <div class="flex justify-between items-start">
                    <strong class="font-medium text-gray-600">Localização:</strong>
                    <span data-template-id="localizacao-torre" class="text-gray-800 text-right">N/A</span>
                </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 space-y-4">
                <div data-template-id="bloco-tempo">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <img data-template-id="icone-tempo" src="" alt="Condição do tempo" class="w-10 h-10">
                            <div>
                                <span data-template-id="temperatura-tempo"
                                    class="font-bold text-2xl text-gray-800">--°C</span>
                                <span data-template-id="condicao-tempo" class="block text-sm text-gray-600">--</span>
                            </div>
                        </div>
                        <div class="text-right">
                            <span data-template-id="umidade-tempo"
                                class="font-semibold text-blue-600 text-lg">--%</span>
                            <span class="block text-xs text-gray-500">Umidade</span>
                        </div>
                    </div>
                    <div class="border-t border-gray-200 mt-4 pt-3">
                        <div data-template-id="lista-previsao" class="flex justify-around text-center">
                        </div>
                    </div>
                </div>
                <p data-template-id="sem-tempo" class="text-xs text-gray-500 hidden">Informação do tempo indisponível.
                </p>
            </div>

            <div>
                <h3 class="font-semibold text-gray-700 mb-2">Equipamentos (<span
                        data-template-id="total-equipamentos">0</span>)</h3>
                <div data-template-id="lista-equipamentos" class="space-y-1"></div>
                <p data-template-id="sem-equipamentos" class="text-sm text-gray-500 px-3 py-4 hidden">Nenhum equipamento
                    cadastrado.</p>
            </div>
        </div>

        <div class="flex-shrink-0 p-4 border-t border-gray-200">
            <a data-template-id="link-gerenciar" href="#"
                class="w-full text-center block px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">Gerir
                Torre</a>
        </div>
    </div>
</template>

<template id="detalhes-equipamento-template">
    <div class="flex items-center justify-between p-3 hover:bg-gray-50 rounded-md">
        <div class="flex items-center gap-3"><span data-template-id="status-led"
                class="w-2.5 h-2.5 rounded-full"></span>
            <div>
                <p data-template-id="nome-equipamento" class="font-medium text-gray-800 text-sm">--</p>
                <p data-template-id="ip-equipamento" class="text-xs text-gray-500">--</p>
            </div>
        </div><span data-template-id="status-texto" class="text-xs font-semibold">--</span>
    </div>
</template>

<template id="detalhes-previsao-template">
    <div class="flex flex-col items-center">
        <span data-template-id="previsao-dia" class="text-xs font-bold text-gray-600">--</span>
        <img data-template-id="previsao-icone" src="" alt="previsão" class="w-8 h-8">
        <span data-template-id="previsao-temp" class="text-xs text-gray-500">--°/--°</span>
    </div>
</template>
```

### `views\partials\empty-state.php`

```php
<?php
/**
 * Componente de "Estado Vazio" Reutilizável.
 *
 * @param array $options {
 * Opcional. Um array de opções para personalizar o componente.
 *
 * @type string $icon      O SVG do ícone a ser exibido.
 * @type string $message   A mensagem a ser exibida.
 * @type string|null $button_text O texto para o botão de ação.
 * @type string|null $button_action A ação JavaScript a ser executada pelo botão.
 * }
 */
$default_icon = '<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1"><path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" /></svg>';

$icon = $options['icon'] ?? $default_icon;
$message = $options['message'] ?? 'Não há dados para exibir no momento.';
$button_text = $options['button_text'] ?? null;
$button_action = $options['button_action'] ?? null;
?>
<div
    class="flex flex-col items-center justify-center text-center h-full p-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
    <div>
        <?php echo $icon; ?>
    </div>
    <p class="mt-4 text-sm font-medium text-gray-500">
        <?php echo htmlspecialchars($message); ?>
    </p>
    <?php if ($button_text && $button_action): ?>
        <button onclick="<?php echo htmlspecialchars($button_action); ?>"
            class="mt-6 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors">
            <?php echo htmlspecialchars($button_text); ?>
        </button>
    <?php endif; ?>
</div>
```

### `views\partials\_import_modal.php`

```php
<div id="importModal" class="fixed inset-0 bg-gray-900 bg-opacity-60 flex items-center justify-center z-50 hidden" style="backdrop-filter: blur(4px);">
    <div id="modal-container" class="bg-white rounded-xl shadow-2xl w-full max-w-2xl transform transition-all" role="dialog">
        
        <div class="flex items-center justify-between p-5 border-b border-gray-200">
            <h3 id="modal-title" class="text-lg font-semibold text-gray-800">Importar Dados via CSV</h3>
            <button onclick="closeImportModal()" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
        </div>

        <div class="p-6">
            <div id="importTypeSelection">
                <p class="text-center text-gray-600 mb-6">Escolha o tipo de dados que deseja importar:</p>
                <div class="space-y-4">
                    
                    <div id="import-torres-btn" onclick="selectImportType('torres')" class="group flex items-center p-5 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all">
                        <div class="bg-gray-100 group-hover:bg-blue-500 group-hover:text-white text-blue-500 rounded-lg p-3 mr-4"><i class="fas fa-broadcast-tower fa-lg"></i></div>
                        <div class="flex-1"><h4 class="font-semibold text-gray-800">Importar Torres</h4><p class="text-sm text-gray-500">Adicionar ou atualizar a lista de torres.</p></div>
                        <i class="fas fa-chevron-right text-gray-300 group-hover:text-blue-500"></i>
                    </div>

                    <div id="import-equipamentos-btn" onclick="selectImportType('equipamentos')" class="group flex items-center p-5 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all">
                        <div class="bg-gray-100 group-hover:bg-blue-500 group-hover:text-white text-blue-500 rounded-lg p-3 mr-4"><i class="fas fa-server fa-lg"></i></div>
                        <div class="flex-1"><h4 class="font-semibold text-gray-800">Importar Equipamentos</h4><p class="text-sm text-gray-500">Adicionar ou atualizar os dispositivos das torres.</p></div>
                        <i class="fas fa-chevron-right text-gray-300 group-hover:text-blue-500"></i>
                    </div>

                </div>
            </div>

            <div id="importUploadArea" class="hidden">
                <div class="flex items-center gap-4 mb-4">
                    <button onclick="backToTypeSelection()" class="text-sm text-blue-600 hover:underline">&larr; Voltar</button>
                    <h4 id="uploadTitle" class="text-md font-semibold text-gray-700"></h4>
                </div>
                <div id="uploadZone" class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 hover:bg-gray-50 transition-all">
                    <div class="text-gray-400 pointer-events-none">
                        <i class="fas fa-cloud-upload-alt fa-3x"></i>
                        <p class="mt-4 font-semibold text-gray-700">Arraste e solte seu ficheiro CSV aqui</p>
                        <p class="text-sm">ou <span class="text-blue-600 font-semibold">clique para selecionar</span></p>
                    </div>
                    <input type="file" id="csvFileInput" class="hidden" accept=".csv, text/csv">
                </div>
                <div class="mt-4 text-center">
                    <a href="#" id="downloadTemplateLink" class="text-sm text-blue-600 hover:underline">Baixar ficheiro de exemplo</a>
                </div>
            </div>

             <div id="importResultsArea" class="hidden text-center">
                 <div id="uploadProgress" class="space-y-2">
                     <p id="progressText" class="font-semibold text-gray-700">A enviar ficheiro...</p>
                     <div class="w-full bg-gray-200 rounded-full h-2.5">
                         <div id="progressFill" class="bg-blue-600 h-2.5 rounded-full transition-all duration-300" style="width: 0%"></div>
                     </div>
                 </div>
                 <div id="finalResults" class="hidden">
                     <div id="resultsIcon" class="mx-auto w-16 h-16 flex items-center justify-center rounded-full mb-4"></div>
                     <h4 id="resultsTitle" class="text-xl font-semibold mb-2"></h4>
                     <p id="resultsSummary" class="text-gray-600 mb-4"></p>
                     <div id="resultsDetails" class="hidden max-h-40 overflow-y-auto text-left bg-gray-50 p-3 rounded-lg border border-gray-200 space-y-2"></div>
                     <div class="mt-6 flex justify-center gap-4">
                         <button id="showDetailsBtn" onclick="toggleErrorDetails()" class="hidden text-sm text-blue-600 hover:underline">Ver detalhes dos erros</button>
                         <button onclick="backToTypeSelection()" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">Importar Outro</button>
                         <button onclick="closeImportModalAndRefresh()" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md shadow-sm hover:bg-blue-700">Concluir</button>
                     </div>
                 </div>
             </div>
        </div>
    </div>
</div>
```

### `views\torres\index.php`

```php
<?php
$title = 'Gestão de Torres';
$pageScript = '/assets/js/torres.js';
?>

<div class="torres-header flex flex-col md:flex-row justify-between items-start mb-8 gap-4">
    <div>
        <h1 class="text-2xl font-bold text-gray-800">Gerenciamento de Torres</h1>
        <p class="text-gray-500">Visualize, filtre e gerencie todas as suas torres de conectividade.</p>
    </div>
    <button id="btn-nova-torre"
        class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700">
        <i class="fas fa-plus"></i>
        <span>Nova Torre</span>
    </button>
</div>

<section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center gap-4">
        <div class="bg-indigo-100 text-indigo-600 rounded-full p-3"><i class="fas fa-broadcast-tower fa-lg"></i></div>
        <div>
            <p class="text-sm font-medium text-gray-500">Total de Torres</p>
            <p class="text-2xl font-bold text-gray-800" id="total-torres">0</p>
        </div>
    </div>
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center gap-4">
        <div class="bg-green-100 text-green-600 rounded-full p-3"><i class="fas fa-check-circle fa-lg"></i></div>
        <div>
            <p class="text-sm font-medium text-gray-500">Online</p>
            <p class="text-2xl font-bold text-green-600" id="torres-online">0</p>
        </div>
    </div>
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center gap-4">
        <div class="bg-red-100 text-red-600 rounded-full p-3"><i class="fas fa-times-circle fa-lg"></i></div>
        <div>
            <p class="text-sm font-medium text-gray-500">Offline</p>
            <p class="text-2xl font-bold text-red-600" id="torres-offline">0</p>
        </div>
    </div>
    <div class="bg-white p-6 rounded-lg shadow-md flex items-center gap-4">
        <div class="bg-blue-100 text-blue-600 rounded-full p-3"><i class="fas fa-chart-line fa-lg"></i></div>
        <div>
            <p class="text-sm font-medium text-gray-500">Uptime Médio</p>
            <p class="text-2xl font-bold text-gray-800" id="uptime-medio">0%</p>
        </div>
    </div>
</section>

<div class="bg-white p-4 rounded-lg shadow-md mb-8">
    <div class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div class="md:col-span-2 lg:col-span-3">
            <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i
                        class="fas fa-search text-gray-400"></i></div><input type="text" id="search-torres"
                    class="block w-full pl-10 p-2 border-gray-300 rounded-md"
                    placeholder="Buscar por nome ou localização...">
            </div>
        </div>
        <div><select id="status-filter" class="block w-full p-2 border-gray-300 rounded-md">
                <option value="">Todos os Status</option>
                <option value="1">Online</option>
                <option value="2">Offline</option>
                <option value="3">Manutenção</option>
            </select></div>
        <div><select id="location-filter" class="block w-full p-2 border-gray-300 rounded-md">
                <option value="">Todas as Localizações</option>
            </select></div>
        <div class="lg:col-span-1 flex justify-end"><button id="btn-limpar-filtros"
                class="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">Limpar</button>
        </div>
    </div>
</div>

<div id="torres-container"></div>

<div id="torres-pagination" class="mt-8 flex items-center justify-between"></div>

<template id="torre-card-template">
    <div
        class="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-200">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center">
            <span data-template-id="status-badge"
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"></span>
            <div class="relative" data-template-id="actions-dropdown">
                <button
                    class="text-gray-500 hover:text-gray-700 focus:outline-none h-6 w-6 flex items-center justify-center"><i
                        class="fas fa-ellipsis-v"></i></button>
                <div class="hidden absolute right-0 mt-2 w-48 bg-white rounded-md shadow-xl z-10">
                    <a href="#" data-template-id="btn-detalhes"
                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Ver Detalhes</a>
                    <a href="#" data-template-id="btn-editar"
                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Editar</a>
                    <a href="#" data-template-id="btn-excluir"
                        class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50">Excluir</a>
                </div>
            </div>
        </div>
        <div data-template-id="card-body" class="p-5 text-center cursor-pointer">
            <h3 data-template-id="nome" class="text-lg font-semibold text-gray-800 truncate"></h3>
            <p data-template-id="localizacao" class="text-sm text-gray-500 truncate"></p>
        </div>
        <div
            class="px-5 py-3 bg-gray-50 border-t border-gray-200 grid grid-cols-2 divide-x divide-gray-200 text-center">
            <div>
                <p class="text-sm font-bold text-gray-800" data-template-id="uptime"></p>
                <p class="text-xs text-gray-500">Uptime</p>
            </div>
            <div>
                <p class="text-sm font-bold text-gray-800" data-template-id="dispositivos"></p>
                <p class="text-xs text-gray-500">Dispositivos</p>
            </div>
        </div>
    </div>
</template>

<template id="pagination-template">
    <div>
        <p class="text-sm text-gray-700">
            A exibir <span class="font-medium" data-template-id="showing-from"></span>
            a <span class="font-medium" data-template-id="showing-to"></span>
            de <span class="font-medium" data-template-id="total-records"></span> resultados
        </p>
    </div>
    <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
            <button data-template-id="prev-page"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">Anterior</button>
            <div data-template-id="pagination-numbers" class="flex"></div>
            <button data-template-id="next-page"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">Próximo</button>
        </nav>
    </div>
</template>

<div id="torre-modal" class="hidden fixed inset-0 bg-gray-900 bg-opacity-60 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-2xl w-full max-w-lg transform transition-all">
        <div class="p-5 border-b border-gray-200 flex justify-between items-center">
            <h3 id="modal-title" class="text-lg font-semibold text-gray-800"></h3>
            <button id="btn-fechar-modal" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
        </div>
        <form id="torre-form">
            <input type="hidden" name="id" id="torre-id">
            <div class="p-6 space-y-6 max-h-[70vh] overflow-y-auto">

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label for="nome-torre" class="block text-sm font-medium text-gray-700">Nome da Torre *</label>
                        <input type="text" name="nome" id="nome-torre" required
                            class="mt-1 block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                            placeholder="Ex: POP Principal SP">
                    </div>
                    <div>
                        <label for="status-torre" class="block text-sm font-medium text-gray-700">Status *</label>
                        <select name="status_geral" id="status-torre" required
                            class="mt-1 block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                            <option value="1">Online</option>
                            <option value="2">Offline</option>
                            <option value="3">Manutenção</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label for="localizacao-torre" class="block text-sm font-medium text-gray-700">Localização *</label>
                    <div class="mt-1 relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fas fa-map-marker-alt text-gray-400"></i>
                        </div>
                        <input type="text" name="localizacao" id="localizacao-torre" required
                            class="block w-full pl-10 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                            placeholder="Rua, Número, Bairro, Cidade - UF, CEP">
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label for="latitude-torre" class="block text-sm font-medium text-gray-700">Latitude *</label>
                        <div class="mt-1 relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <i class="fas fa-location-arrow text-gray-400"></i>
                            </div>
                            <input type="text" name="latitude" id="latitude-torre" required
                                class="numeric-input block w-full pl-10 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                                placeholder="-23.550520">
                        </div>
                    </div>
                    <div>
                        <label for="longitude-torre" class="block text-sm font-medium text-gray-700">Longitude *</label>
                        <div class="mt-1 relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <i class="fas fa-location-arrow text-gray-400"></i>
                            </div>
                            <input type="text" name="longitude" id="longitude-torre" required
                                class="numeric-input block w-full pl-10 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                                placeholder="-46.633308">
                        </div>
                    </div>
                </div>

                <div>
                    <label for="observacoes-torre" class="block text-sm font-medium text-gray-700">Observações</label>
                    <textarea name="observacoes" id="observacoes-torre" rows="3"
                        class="mt-1 block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Adicione observações sobre esta torre..."></textarea>
                </div>
            </div>
            <div class="px-6 py-4 bg-gray-50 text-right space-x-3">
                <button type="button" id="btn-cancelar-modal"
                    class="py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">Cancelar</button>
                <button type="submit" id="btn-salvar-modal"
                    class="py-2 px-4 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">Salvar</button>
            </div>
        </form>
    </div>
</div>

<aside id="detalhe-torre-painel"
    class="fixed top-0 right-0 h-full w-full max-w-md bg-white shadow-2xl z-40 transform translate-x-full transition-transform duration-300 ease-in-out">
</aside>

<template id="detalhe-torre-template">
    <div class="flex flex-col h-full">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center">
            <div>
                <p class="text-xs text-gray-500">Detalhes da Torre</p>
                <h2 data-template-id="detalhe-nome-torre" class="font-semibold text-gray-800 text-lg"></h2>
            </div>
            <button data-template-id="btn-fechar-detalhes"
                class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
        </div>
        <div class="flex-grow overflow-y-auto p-4 space-y-6">
            <div class="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                <div class="flex justify-between"><strong class="font-medium text-gray-600">Status:</strong> <span
                        data-template-id="detalhe-status-torre"></span></div>
                <div class="flex justify-between"><strong class="font-medium text-gray-600">Localização:</strong> <span
                        data-template-id="detalhe-localizacao-torre" class="text-gray-800 text-right"></span></div>
                <div class="flex justify-between"><strong class="font-medium text-gray-600">Uptime:</strong> <span
                        data-template-id="detalhe-uptime-torre" class="text-gray-800 font-semibold"></span></div>
            </div>
            <div>
                <h3 class="font-semibold text-gray-700 mb-2">Dispositivos (<span
                        data-template-id="detalhe-total-dispositivos">0</span>)</h3>
                <div data-template-id="detalhe-lista-dispositivos" class="border border-gray-200 rounded-md"></div>
                <p data-template-id="detalhe-sem-dispositivos" class="text-sm text-gray-500 p-4 hidden">Nenhum
                    dispositivo cadastrado para esta torre.</p>
            </div>
        </div>
    </div>
</template>

<template id="detalhe-dispositivo-item-template">
    <div class="flex items-center justify-between p-3 hover:bg-gray-50 not-last:border-b not-last:border-gray-100">
        <div class="flex items-center gap-3">
            <span data-template-id="dispositivo-status-led" class="w-2.5 h-2.5 rounded-full"></span>
            <div>
                <p data-template-id="dispositivo-nome" class="font-medium text-gray-800 text-sm"></p>
                <p data-template-id="dispositivo-ip" class="text-xs text-gray-500"></p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <button data-template-id="btn-editar-dispositivo" class="text-gray-400 hover:text-blue-600 w-6 h-6"><i
                    class="fas fa-pencil-alt fa-xs"></i></button>
            <button data-template-id="btn-excluir-dispositivo" class="text-gray-400 hover:text-red-600 w-6 h-6"><i
                    class="fas fa-trash-alt fa-xs"></i></button>
        </div>
    </div>
</template>

<div id="confirmation-modal"
    class="hidden fixed inset-0 bg-gray-900 bg-opacity-60 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-2xl w-full max-w-sm transform transition-all p-6">
        <h3 id="confirmation-title" class="text-lg font-semibold text-gray-800"></h3>
        <p id="confirmation-message" class="mt-2 text-sm text-gray-600"></p>
        <div class="mt-6 flex justify-end gap-3">
            <button id="btn-confirm-cancel"
                class="py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">Cancelar</button>
            <button id="btn-confirm-action"
                class="py-2 px-4 border border-transparent rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700">Confirmar</button>
        </div>
    </div>
</div>

<div id="dispositivo-modal"
    class="hidden fixed inset-0 bg-gray-900 bg-opacity-60 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-2xl w-full max-w-lg transform transition-all">
        <div class="p-5 border-b border-gray-200 flex justify-between items-center">
            <h3 id="dispositivo-modal-title" class="text-lg font-semibold text-gray-800"></h3>
            <button id="btn-fechar-dispositivo-modal"
                class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
        </div>
        <form id="dispositivo-form">
            <input type="hidden" name="id" id="dispositivo-id">
            <input type="hidden" name="torre_id" id="dispositivo-torre-id">
            <div class="p-6 space-y-4">
                <div>
                    <label for="dispositivo-nome" class="block text-sm font-medium text-gray-700">Nome do Dispositivo
                        *</label>
                    <input type="text" name="nome" id="dispositivo-nome" required
                        class="mt-1 block w-full border-gray-300 rounded-md">
                </div>
                <div>
                    <label for="dispositivo-ip" class="block text-sm font-medium text-gray-700">Endereço IP *</label>
                    <input type="text" name="ip" id="dispositivo-ip" required
                        class="mt-1 block w-full border-gray-300 rounded-md" placeholder="192.168.0.1">
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label for="dispositivo-tipo" class="block text-sm font-medium text-gray-700">Tipo *</label>
                        <select name="tipo_dispositivo_id" id="dispositivo-tipo" required
                            class="mt-1 block w-full border-gray-300 rounded-md">
                            <option value="">A carregar tipos...</option>
                        </select>
                    </div>
                    <div>
                        <label for="dispositivo-status" class="block text-sm font-medium text-gray-700">Status *</label>
                        <select name="status" id="dispositivo-status" required
                            class="mt-1 block w-full border-gray-300 rounded-md">
                            <option value="1">Online</option>
                            <option value="2">Offline</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="px-6 py-4 bg-gray-50 text-right space-x-3">
                <button type="button" id="btn-cancelar-dispositivo-modal"
                    class="py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">Cancelar</button>
                <button type="submit"
                    class="py-2 px-4 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">Salvar
                    Dispositivo</button>
            </div>
        </form>
    </div>
</div>
```


---

_Relatório gerado automaticamente pelo ProjectAnalyzer_
