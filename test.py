from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app=app)

print(
    client.get(
        "/search/semantic_search", params={"q": "Which forts are difficult treks?"}
    ).json()
)