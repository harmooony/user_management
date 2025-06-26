from ariadne import make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from server.resolvers import (
    resolve_list_users,
    resolve_get_user,
    resolve_me,
    resolve_create_user,
    resolve_update_user,
    resolve_delete_user,
    resolve_login
)
from server.database import Base, engine
from server.models import User
import uvicorn

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Загружаем схему
type_defs = load_schema_from_path("schema/schema.graphql")

# Настраиваем резолверы
query = {
    "listUsers": resolve_list_users,
    "getUser": resolve_get_user,
    "me": resolve_me
}

mutation = {
    "createUser": resolve_create_user,
    "updateUser": resolve_update_user,
    "deleteUser": resolve_delete_user,
    "login": resolve_login
}

# Создаем исполняемую схему
schema = make_executable_schema(
    type_defs,
    [query, mutation],
    snake_case_fallback_resolvers
)

# Создаем ASGI приложение
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)