import requests

API_BASE = "http://localhost:8000"
TIMEOUT = 8  # seconds


class APIClient:
    """A clean wrapper around the FastAPI backend endpoints."""

    def __init__(self, base_url: str = API_BASE):
        self.base = base_url.rstrip("/")

    # --------------------------------------------------
    # Internal HTTP GET helper
    # --------------------------------------------------
    def _get(self, path: str, params=None, expect_list=False):
        url = f"{self.base}{path}"
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()

        except Exception as e:
            print(f"[API ERROR] GET {url} params={params} -> {e}")
            return [] if expect_list else {}

    # --------------------------------------------------
    # Public API Methods
    # --------------------------------------------------

    def get_forts(self, params=None):
        return self._get("/forts", params=params, expect_list=True)

    def get_fort(self, fort_id):
        return self._get(f"/forts/{fort_id}")

    def get_nearby(self, lat, lon, k=5):
        return self._get(
            "/recommend/nearby",
            params={"lat": lat, "lon": lon, "k": k},
            expect_list=True,
        )

    def get_similar(self, fort_id, k=5):
        return self._get(
            f"/recommend/similar/{fort_id}",
            params={"k": k},
            expect_list=True,
        )

    def get_clusters(self):
        return self._get("/clusters")

    def get_clustered_forts(self):
        return self._get("/clusters/data", expect_list=True)

    def rag_query(self, query: str):
        return self._get(
            "/search/qa",
            params={"q": query},
            expect_list=True,
        )


# Global instance used across the app
api = APIClient()
