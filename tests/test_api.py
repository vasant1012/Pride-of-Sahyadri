from fastapi.testclient import TestClient
import sys
sys.path.append("/home/pamya/Python/ML_Projects/maharashtra-forts")
sys.path.append("/home/pamya/Python/ML_Projects/maharashtra-forts/src")
from api.main import app

client = TestClient(app)


def test_root():
    """Root endpoint should respond with running status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "up" in data.get("msg", "").lower()


def test_list_forts():
    """Listing forts should return a list of records."""
    response = client.get("/forts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "name" in data[0], "Each fort record should contain a name field"
        assert "district" in data[0], "Each fort record should contain a district field"