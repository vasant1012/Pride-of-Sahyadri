from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


class GeoCluster:
    """KMeans-based geospatial clustering for forts.

    If there are not enough valid (lat, lon) pairs to form `n_clusters`,
    a fallback cluster assignment of 0 is applied to all rows.
    """

    def __init__(self, n_clusters: int = 8, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = None

    def fit(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fit geospatial clustering and return df with new 'cluster' column.

        Args:
            df (pd.DataFrame): DataFrame with 'latitude' and 'longitude'

        Returns:
            pd.DataFrame: copy of df with cluster labels added.
        """
        coords = df[['latitude', 'longitude']].dropna()

        # If not enough data points, fallback to a single cluster
        if coords.shape[0] < max(1, self.n_clusters):
            df2 = df.copy()
            df2['cluster'] = 0
            self.model = None
            return df2

        # Fit KMeans
        self.model = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)
        self.model.fit(coords)

        # For rows where lat/lon missing, fill with (0,0) safely
        df_filled = df[['latitude', 'longitude']].fillna(0)
        labels = self.model.predict(df_filled)

        df2 = df.copy()
        df2['cluster'] = labels
        return df2

    def predict(self, lat: float, lon: float) -> int:
        """Predict cluster for a single coordinate.

        Args:
            lat (float): latitude
            lon (float): longitude

        Returns:
            int: cluster label
        """
        if self.model is None:
            raise RuntimeError('Model not fitted or insufficient data for clustering.')

        arr = np.array([[lat, lon]])
        label = self.model.predict(arr)[0]
        return int(label)
