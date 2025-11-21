import requests

API_BASE = "http://localhost:8000"     # change in production

def get_forts(params=None):
    """Fetch list of forts with optional filters."""
    return requests.get(f"{API_BASE}/forts", params=params).json()

def get_fort(fort_id):
    """Fetch a single fort by ID."""
    return requests.get(f"{API_BASE}/forts/{fort_id}").json()

def rag_query(q):
    """Semantic search using RAG engine."""
    return requests.get(f"{API_BASE}/search/qa", params={"q": q}).json()

def get_clusters():
    return requests.get(f"{API_BASE}/clusters").json()

def predict_cluster(lat, lon):
    return requests.get(
        f"{API_BASE}/clusters/predict",
        params={"lat": lat, "lon": lon}
    ).json()

def get_nearby(lat, lon, k=5):
    return requests.get(
        f"{API_BASE}/recommend/nearby",
        params={"lat": lat, "lon": lon, "k": k}
    ).json()

def get_similar(fort_id, k=5):
    return requests.get(
        f"{API_BASE}/recommend/similar/{fort_id}",
        params={"k": k}
    ).json()