import requests
import json

# URL вашего GraphQL сервера
GRAPHQL_URL = "http://localhost:8000"


def execute_query(query, variables=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = {"query": query}
    if variables:
        data["variables"] = variables

    response = requests.post(GRAPHQL_URL, headers=headers, json=data)
    return response.json()


# Примеры запросов
def test_operations():
    # Создание пользователя
    create_user_mutation = """
    mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) {
            id
            name
            email
            role
        }
    }
    """

    variables = {
        "input": {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "securepassword",
            "role": "admin"
        }
    }

    result = execute_query(create_user_mutation, variables)
    print("Create User Result:", json.dumps(result, indent=2))

    # Логин
    login_mutation = """
    mutation Login($email: String!, $password: String!) {
        login(email: $email, password: $password) {
            token
            user {
                id
                name
                email
            }
        }
    }
    """

    variables = {
        "email": "admin@example.com",
        "password": "securepassword"
    }

    result = execute_query(login_mutation, variables)
    print("Login Result:", json.dumps(result, indent=2))
    token = result["data"]["login"]["token"]

    # Получение списка пользователей
    list_users_query = """
    query ListUsers {
        listUsers {
            id
            name
            email
            role
        }
    }
    """

    result = execute_query(list_users_query, token=token)
    print("List Users Result:", json.dumps(result, indent=2))

    # Получение текущего пользователя
    me_query = """
    query Me {
        me {
            id
            name
            email
            role
        }
    }
    """

    result = execute_query(me_query, token=token)
    print("Me Query Result:", json.dumps(result, indent=2))


if __name__ == "__main__":
    test_operations()