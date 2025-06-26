import requests
import json

GRAPHQL_URL = "http://localhost:8000/graphql"

def execute_query(query, variables=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = {"query": query, "variables": variables}
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    return response.json()

# Пример логина
login_query = """
mutation Login($email: String!, $password: String!) {
  login(email: $email, password: $password) {
    token
    user {
      id
      name
      email
      role
    }
  }
}
"""
login_variables = {"email": "admin@example.com", "password": "admin123"}
login_response = execute_query(login_query, login_variables)
print("Login Response:", json.dumps(login_response, indent=2))
token = login_response.get("data", {}).get("login", {}).get("token")

# Пример создания пользователя
create_user_query = """
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
    role
  }
}
"""
create_user_variables = {
    "input": {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "role": "USER"
    }
}
create_response = execute_query(create_user_query, create_user_variables)
print("Create User Response:", json.dumps(create_response, indent=2))

# Пример получения списка пользователей
list_users_query = """
query ListUsers($filter: UserFilter, $limit: Int, $offset: Int) {
  listUsers(filter: $filter, limit: $limit, offset: $offset) {
    id
    name
    email
    role
  }
}
"""
list_users_variables = {"limit": 5, "offset": 0}
list_response = execute_query(list_users_query, list_users_variables, token)
print("List Users Response:", json.dumps(list_response, indent=2))

# Пример обновления пользователя (требуется токен ADMIN)
update_user_query = """
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    email
    role
  }
}
"""
update_user_variables = {
    "id": "1",
    "input": {"name": "Admin Updated"}
}
update_response = execute_query(update_user_query, update_user_variables, token)
print("Update User Response:", json.dumps(update_response, indent=2))

# Пример удаления пользователя (требуется токен ADMIN)
delete_user_query = """
mutation DeleteUser($id: ID!) {
  deleteUser(id: $id)
}
"""
delete_user_variables = {"id": "1"}
delete_response = execute_query(delete_user_query, delete_user_variables, token)
print("Delete User Response:", json.dumps(delete_response, indent=2))