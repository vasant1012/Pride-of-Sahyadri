from pathlib import Path
from typing import Optional
import pandas as pd

# Default path: project_root/data/maharashtra-forts.csv
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "maharashtra-forts.csv"


def load_forts(path: Optional[str] = None) -> pd.DataFrame:
    """Load forts CSV into a pandas DataFrame.

    - Normalizes column names to lowercase
    - Ensures numeric columns are converted
    - Fills NA for certain text columns with empty strings

    Args:
        path: optional path to CSV. If None, uses package DATA_PATH.

    Returns:
        pd.DataFrame: cleaned DataFrame

    Raises:
        FileNotFoundError: if CSV is not found at the resolved path.
    """
    p = Path(path) if path else DATA_PATH
    if not p.exists():
        raise FileNotFoundError(f"CSV not found at: {p}")

    df = pd.read_csv(p._str)

    # normalize columns
    df.columns = [c.strip().lower() for c in df.columns]

    # optional: ensure fort_id is int if present
    if "fort_id" in df.columns:
        try:
            df["fort_id"] = df["fort_id"].astype(int)
        except Exception:
            # coerce and fill with index if conversion fails
            df["fort_id"] = pd.to_numeric(df["fort_id"], errors="coerce")
            df["fort_id"] = df["fort_id"].fillna(range(1, len(df) + 1)).astype(int)

    # fill NA textual cols with empty strings
    text_cols = [
        "notes",
        "key_events",
        "alternate_names",
        "best_season",
        "trek_difficulty",
        "type",
        "district",
        "taluka",
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")

    # numeric conversions
    num_cols = ["latitude", "longitude", "elevation_m", "trek_time_hours"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
