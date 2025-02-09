# Backend - API Gerenciador de Posts

Este é o backend do **Gerenciador de Posts**, desenvolvido com **Django**. Ele gerencia usuários e posts através de uma API REST protegida por autenticação do próprio Django.

## 🚀 Tecnologias Utilizadas
- **Django** - Framework web backend.
- **PostgreSQL** - Banco de dados relacional.
- **Docker + Docker Compose** - Para containerização.


## 🔧 Configuração e Execução
### 1️⃣ Instale as dependências:
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure as variáveis de ambiente:
Crie um arquivo .env e adicione:

```ini
SECRET_KEY=suachavesecreta
DEBUG=True
DATABASE_URL=postgres://usuario:senha@localhost:5432/seubanco
```

### 3️⃣ Rode as migrações e inicie o servidor:
```bash
python manage.py migrate
python manage.py runserver
```

O backend estará rodando em http://localhost:8000.

## 🏗 Funcionalidades Implementadas
✅ Autenticação: Registro, login e proteção de endpoints.  
✅ CRUD de Posts: Criar, editar e excluir posts com controle de permissões.  
✅ Banco de Dados PostgreSQL: Armazena usuários e posts.  
✅ Validações e Serialização: Uso do Django REST Framework.

## 📌 Endpoints da API
| Método | Endpoint            | Descrição                     |
|--------|---------------------|-------------------------------|
| POST   | /api/auth/login/    | Autenticação do usuário       |
| POST   | /api/auth/register/ | Criação de um novo usuário    |
| GET    | /api/posts/         | Lista todos os posts          |
| POST   | /api/posts/         | Cria um novo post (admin)     |
| PUT    | /api/posts/{id}/    | Edita um post (admin)         |
| DELETE | /api/posts/{id}/    | Exclui um post (admin)        |

feito com 💜 por [MA](https://github.com/MonicaAlvesP).