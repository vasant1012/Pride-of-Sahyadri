from fastapi import APIRouter, HTTPException
from src.core.data_loader import load_forts
from src.core.recommender import recommend_by_proximity, recommend_similar

router = APIRouter()

# Load dataset once
DF = load_forts()


@router.get("/nearby")
def nearby(lat: float, lon: float, k: int = 10):
    """Return the k nearest forts to a given coordinate.

    Args:
        lat (float): latitude
        lon (float): longitude
        k (int): number of results

    Returns:
        list: forts sorted by distance_km ascending
    """
    results = recommend_by_proximity(DF, lat, lon, k=k)
    return results.to_dict(orient="records")


@router.get("/similar/{fort_id}")
def similar(fort_id: int, k: int = 5):
    """Return forts similar to the provided fort_id.

    Similarity uses:
    - Same type (strongly weighted)
    - Elevation closeness

    Args:
        fort_id (int)
        k (int): number of results
    """
    results = recommend_similar(DF, fort_id, k=k)

    if results.empty:
        raise HTTPException(status_code=404, detail="Fort not found or insufficient data for similarity.")

    return results.to_dict(orient="records")
