# Arena Manager

Arena Manager é uma API para gestão de campeonatos amadores, com foco em futebol, society e futsal.

O backend permite gerenciar times, jogadores, campeonatos, partidas, eventos de jogo, classificação, dashboard e artilharia.

## Status do projeto

Backend em fase avançada, com testes cobrindo:

* Models
* Serializers
* Views/API
* Actions customizadas
* Signals
* Permissões/autenticação
* Fluxo de partidas
* Classificação
* Dashboard
* Artilharia

Atualmente o backend possui **75 testes passando**.

## Tecnologias

* Python
* Django
* Django REST Framework
* Simple JWT
* django-filter
* drf-spectacular
* python-decouple
* SQLite em desenvolvimento

## Estrutura principal

```text
backend/
├── apps/
│   ├── championships/
│   ├── matches/
│   ├── players/
│   ├── teams/
│   └── users/
├── config/
└── manage.py
```

## Configuração do backend

Entre na pasta do backend:

```bash
cd backend
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows/Git Bash:

```bash
source venv/Scripts/activate
```

Instale as dependências:

```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter drf-spectacular python-decouple pillow
```

## Variáveis de ambiente

Crie um arquivo `.env` dentro da pasta `backend/`:

```env
SECRET_KEY=sua-chave-secreta-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Banco de dados

```bash
python manage.py makemigrations
python manage.py migrate
```

## Rodar o servidor

```bash
python manage.py runserver
```

A API ficará disponível em:

```text
http://127.0.0.1:8000/
```

## Documentação da API

```text
/api/docs/
/api/schema/
```

## Autenticação

O projeto usa autenticação JWT.

```text
POST /api/auth/token/
POST /api/auth/token/refresh/
```

## Endpoints principais

### Times

```text
GET    /api/teams/
POST   /api/teams/
GET    /api/teams/{id}/
PATCH  /api/teams/{id}/
DELETE /api/teams/{id}/
```

### Jogadores

```text
GET    /api/players/
POST   /api/players/
GET    /api/players/{id}/
PATCH  /api/players/{id}/
DELETE /api/players/{id}/
```

### Campeonatos

```text
GET    /api/championships/
POST   /api/championships/
GET    /api/championships/{id}/
PATCH  /api/championships/{id}/
DELETE /api/championships/{id}/
```

### Ações de campeonatos

```text
POST /api/championships/{id}/generate-matches/
POST /api/championships/{id}/recalculate/
GET  /api/championships/{id}/dashboard/
GET  /api/championships/{id}/top-scorers/
```

### Partidas

```text
GET    /api/matches/
POST   /api/matches/
GET    /api/matches/{id}/
PATCH  /api/matches/{id}/
DELETE /api/matches/{id}/
```

### Eventos de partida

```text
GET    /api/match-events/
POST   /api/match-events/
GET    /api/match-events/{id}/
PATCH  /api/match-events/{id}/
DELETE /api/match-events/{id}/
```

## Testes

Rodar a suíte atual:

```bash
python manage.py test \
  apps.championships.tests.test_models \
  apps.championships.tests.test_views \
  apps.championships.tests.test_actions \
  apps.championships.tests.test_serializers \
  apps.championships.tests.test_permissions \
  apps.matches.tests.test_signals \
  apps.matches.tests.test_views \
  apps.matches.tests.test_serializers \
  apps.matches.tests.test_permissions \
  apps.players.tests.test_models \
  apps.players.tests.test_views \
  apps.players.tests.test_serializers \
  apps.players.tests.test_permissions \
  apps.teams.tests.test_models \
  apps.teams.tests.test_views \
  apps.teams.tests.test_serializers \
  apps.teams.tests.test_permissions
```

## Funcionalidades

* Cadastro de times
* Cadastro de jogadores
* Criação de campeonatos
* Vinculação de times a campeonatos
* Geração automática de partidas
* Registro de placar
* Registro de eventos de jogo
* Atualização automática de placar por gols
* Recalcular classificação
* Dashboard do campeonato
* Ranking de artilheiros
* Autenticação JWT
* Documentação Swagger

## Próximas melhorias

* Criar `requirements.txt`
* Adicionar GitHub Actions
* Melhorar descoberta automática dos testes
* Adicionar filtros, busca e ordenação nos testes
* Configurar PostgreSQL para produção
* Adicionar Docker

## Licença

Este projeto está licenciado sob a licença. Veja o arquivo [`LICENSE`](LICENSE).
