from fastapi.testclient import TestClient
from main import app  # импортируем твой настоящий блог

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Blog" in response.text  # проверяем, что на странице есть заголовок

def test_get_posts_api():
    response = client.get("/api/posts")
    assert response.status_code == 200
    assert "posts" in response.json()  # проверяем, что API вернул список постов

def test_unauthorized_create_post():
    # Пытаемся создать пост БЕЗ токена авторизации
    response = client.post("/api/posts", json={"title": "Test", "content": "Test"})
    assert response.status_code == 401  # Ожидаем отказ (Unauthorized)