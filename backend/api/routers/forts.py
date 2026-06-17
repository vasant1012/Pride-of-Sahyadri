from fastapi import APIRouter, HTTPException
from backend.core.data_loader import load_forts

router = APIRouter()

# Load once at startup
DF = load_forts()


def normalize_fort_type(value: str | None) -> str:
    if not value:
        return "Unknown"
    lower = value.lower()
    if "sea" in lower:
        return "Sea Fort"
    if "hill" in lower or "giri" in lower or "durg" in lower:
        return "Hill Fort"
    if "land" in lower:
        return "Land Fort"
    if "plateau" in lower:
        return "Hill Fort"
    return value


def normalize_seasons(value: str | None) -> list[str]:
    if not value:
        return []
    return [s.strip() for s in value.split(",") if s.strip()]


@router.get("/")
def list_forts(
    q: str | None = None,
    district: str | None = None,
    type: str | None = None,
    difficulty: str | None = None,
    season: str | None = None,
    water: str | None = None,
    minElev: int | None = None,
    maxElev: int | None = None,
    limit: int | None = None,
):  # NOQA
    """List forts with optional search and filter parameters."""
    df = DF.copy()
    df["type"] = df["type"].apply(normalize_fort_type)

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

    if type and type.lower() != "all":
        df = df[df["type"].str.lower() == type.lower()]

    if difficulty and difficulty.lower() != "all":
        df = df[df["trek_difficulty"].str.lower() == difficulty.lower()]

    if season and season.lower() != "all":
        df = df[df["best_season"].str.lower().str.contains(season.lower(), na=False)]

    if water and water.lower() != "all":
        df = df[df["water_availability"].str.lower() == water.lower()]

    if minElev is not None:
        df = df[df["elevation_m"] >= minElev]

    if maxElev is not None:
        df = df[df["elevation_m"] <= maxElev]

    if limit is not None and limit > 0:
        df = df.head(limit)

    response = df.to_dict(orient="records")
    return response


@router.get("/meta")
def get_meta():
    districts = sorted(DF["district"].dropna().astype(str).unique().tolist())
    types = sorted({normalize_fort_type(v) for v in DF["type"].fillna("")})
    difficulties = sorted(DF["trek_difficulty"].dropna().astype(str).unique().tolist())
    seasons = sorted({season for value in DF["best_season"].fillna("").tolist() for season in normalize_seasons(value)})
    water_options = sorted(DF["water_availability"].dropna().astype(str).unique().tolist())

    return {
        "districts": districts,
        "types": types,
        "difficulties": difficulties,
        "seasons": seasons,
        "waterOptions": water_options,
        "totalForts": len(DF),
    }


@router.get("/stats")
def get_stats():
    df = DF.copy()
    df["type"] = df["type"].apply(normalize_fort_type)

    by_type = df["type"].value_counts().to_dict()
    by_difficulty = df["trek_difficulty"].value_counts().to_dict()
    by_district = df["district"].value_counts().to_dict()
    elevations = (
        df[["name", "elevation_m"]]
        .sort_values("elevation_m", ascending=False)
        .head(12)
        .rename(columns={"elevation_m": "elevation"})
        .to_dict(orient="records")
    )

    return {
        "totals": {
            "totalForts": len(df),
            "districtsCovered": len(by_district),
            "trekRoutes": int(df[df["elevation_m"] > 0].shape[0]),
            "heritageSites": len(df),
        },
        "byType": [{"name": name, "value": value} for name, value in by_type.items()],
        "byDifficulty": [{"name": name, "value": value} for name, value in by_difficulty.items()],
        "byDistrict": [{"name": name, "value": value} for name, value in by_district.items()],
        "elevations": elevations,
    }


@router.get("/{fort_id}")
def get_fort(fort_id: int):
    """Retrieve a single fort record by its fort_id."""
    row = DF[DF["fort_id"] == fort_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Fort not found")
    response = row.iloc[0].to_dict()
    response["type"] = normalize_fort_type(response.get("type"))
    return response
