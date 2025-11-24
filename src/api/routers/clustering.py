from fastapi import APIRouter
from src.core.cluster_engine import ClusterEngine

router = APIRouter(prefix="/clusters", tags=["Clustering"])

# Build clusters at startup
cluster_engine = ClusterEngine()
cluster_engine.build_clusters()

@router.get("/")
def get_cluster_counts():
    """
    Return {cluster_id: count}
    """
    return cluster_engine.get_cluster_counts()


@router.get("/data")
def get_clustered_forts():
    """
    Returns list of forts with `cluster` label added
    """
    df = cluster_engine.get_clustered_data()
    return df.to_dict(orient="records")


@router.post("/rebuild/{n_clusters}")
def rebuild_clusters(n_clusters: int):
    """
    Recompute clusters with a new number of clusters.
    """
    cluster_engine.n_clusters = n_clusters
    df, counts = cluster_engine.build_clusters()
    return {"clusters": counts, "n_clusters": n_clusters}
