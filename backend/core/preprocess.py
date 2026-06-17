from typing import Tuple, Dict
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_for_model(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    """Encode categorical columns and fill numeric NAs.

    For each categorical column, this function creates a new column
    named `{col}_le` which contains the label-encoded integers.

    Args:
        df (pd.DataFrame): raw fort dataset

    Returns:
        Tuple[pd.DataFrame, dict]: (processed_df, encoders_dict)
    """
    encoders: Dict[str, LabelEncoder] = {}
    out = df.copy()

    # Categorical columns to encode
    cat_cols = [
        'type',
        'district',
        'taluka',
        'trek_difficulty',
        'best_season'
    ]

    for col in cat_cols:
        if col in out.columns:
            le = LabelEncoder()
            out[col] = out[col].fillna('Unknown').astype(str)
            out[col + '_le'] = le.fit_transform(out[col])
            encoders[col] = le

    # Numeric columns to fill
    numeric_cols = ['elevation_m', 'trek_time_hours']
    for col in numeric_cols:
        if col in out.columns:
            median_val = out[col].median()
            out[col] = out[col].fillna(median_val)

    return out, encoders
