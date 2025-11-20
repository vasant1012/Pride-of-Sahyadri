from fastapi import APIRouter, HTTPException
from src.core.data_loader import load_forts

router = APIRouter()

# Load once at startup
DF = load_forts()


@router.get("/")
def list_forts(q: str | None = None, district: str | None = None, limit: int = 10):  # NOQA
    """List forts with optional search and district filters.

    Args:
        q: optional text search query (name, notes, key_events)
        district: optional district filter
        limit: number of results to return
    """
    df = DF.copy()

    if q:
        ql = q.lower()
        mask = (
            df["name"].str.lower().str.contains(ql, na=False)
            | df["notes"].str.lower().str.contains(ql, na=False)
            | df["key_events"].str.lower().str.contains(ql, na=False)
        )
        df = df[mask]

    if district:
        df = df[df["district"].str.lower() == district.lower()]

    response = df.head(limit).to_dict(orient="records")
    return response


@router.get("/{fort_id}")
def get_fort(fort_id: int):
    """Retrieve a single fort record by its fort_id."""
    row = DF[DF["fort_id"] == fort_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Fort not found")
    response = row.iloc[0].to_dict()
    return response
