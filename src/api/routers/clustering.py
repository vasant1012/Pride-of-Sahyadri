from fastapi import APIRouter
from src.core.data_loader import load_forts
from src.core.cluster_engine import GeoCluster

router = APIRouter()

# Load dataset
DF = load_forts()

# Initialize clustering engine
clusterer = GeoCluster(n_clusters=8)

try:
    DF = clusterer.fit(DF)
except Exception as e:
    # Fallback: assign cluster 0 if clustering fails
    DF = DF.copy()
    DF['cluster'] = 0
    INIT_ERROR = str(e)
else:
    INIT_ERROR = None


@router.get("/")
def get_clusters():
    """Return size of each cluster.

    Returns:
        dict: {cluster_id: count}
    """
    if INIT_ERROR:
        return {"warning": f"Clustering fallback used: {INIT_ERROR}"}
    return DF.groupby('cluster').size().to_dict()


@router.get("/predict")
def predict_cluster(lat: float, lon: float):
    """Predict which cluster a (lat, lon) coordinate belongs to.

    Args:
        lat (float): latitude
        lon (float): longitude

    Returns:
        dict: {'cluster': int} or {'error': str}
    """
    try:
        cluster_id = clusterer.predict(lat, lon)
        return {"cluster": int(cluster_id)}
    except Exception as e:
        return {"error": str(e)}
