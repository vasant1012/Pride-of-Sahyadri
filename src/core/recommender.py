from geopy.distance import geodesic
import pandas as pd


def recommend_by_proximity(df: pd.DataFrame, lat: float, lon: float, k: int = 10) -> pd.DataFrame:
    """Return k nearest forts to the given (lat, lon) location.

    Args:
        df (pd.DataFrame): fort dataset
        lat (float): latitude of query location
        lon (float): longitude of query location
        k (int): number of results to return

    Returns:
        pd.DataFrame: sorted by ascending distance_km
    """
    df_coords = df.copy()

    def compute_distance(row):
        try:
            if pd.isna(row['latitude']) or pd.isna(row['longitude']):
                return float('inf')
            return geodesic((lat, lon), (row['latitude'], row['longitude'])).km
        except Exception:
            return float('inf')

    df_coords['distance_km'] = df_coords.apply(compute_distance, axis=1)
    return df_coords.sort_values('distance_km').head(k)


def recommend_similar(df: pd.DataFrame, fort_id: int, k: int = 5) -> pd.DataFrame:
    """Recommend similar forts to the given fort_id.

    Similarity heuristic:
        - Same type = +1
        - Elevation closeness improves score

    Args:
        df (pd.DataFrame): fort dataset
        fort_id (int): fort to find similar forts for
        k (int): number of results

    Returns:
        pd.DataFrame: top-k similar forts
    """
    base = df[df['fort_id'] == fort_id]
    if base.empty:
        return pd.DataFrame()

    base = base.iloc[0]
    df2 = df.copy()

    # Type similarity
    df2['type_score'] = (df2['type'] == base['type']).astype(int)

    # Elevation difference (smaller is better)
    base_elev = base['elevation_m'] if pd.notna(base['elevation_m']) else 0
    df2['elev_diff'] = (df2['elevation_m'].fillna(0) - base_elev).abs()

    # Combined score
    df2['score'] = df2['type_score'] - 0.001 * df2['elev_diff']

    return df2.sort_values('score', ascending=False).head(k)
