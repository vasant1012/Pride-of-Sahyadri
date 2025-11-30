import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path

CSV_PATH = Path("data/maharashtra-forts.csv")   # your dataset path


class ClusterEngine:
    def __init__(self, n_clusters=6):
        self.n_clusters = n_clusters
        self.df = None
        self.cluster_counts = None
        self.scaler = None
        self.kmeans = None

    # -----------------------------
    # Load + Preprocess
    # -----------------------------
    def load_data(self):
        df = pd.read_csv(CSV_PATH)
        df = df.copy()
        df = df.fillna(value='Information Not Available')

        # Standardize latitude/longitude column names
        df["latitude"] = pd.to_numeric(
            df.get("latitude", df.get("lat")), errors="coerce"
        )
        df["longitude"] = pd.to_numeric(
            df.get("longitude", df.get("lng")), errors="coerce"
        )

        df["elevation_m"] = pd.to_numeric(df["elevation_m"], errors="coerce")
        df["trek_time_hours"] = pd.to_numeric(
            df["trek_time_hours"], errors="coerce")

        # Difficulty → numeric
        df["difficulty_num"] = df["trek_difficulty"].apply(self.map_difficulty)

        # Impute missing values
        df["latitude"].fillna(df["latitude"].median(), inplace=True)
        df["longitude"].fillna(df["longitude"].median(), inplace=True)
        df["elevation_m"].fillna(df["elevation_m"].median(), inplace=True)
        df["trek_time_hours"].fillna(
            df["trek_time_hours"].median(), inplace=True)
        df["difficulty_num"].fillna(
            df["difficulty_num"].median(), inplace=True)

        self.df = df
        return df

    @staticmethod
    def map_difficulty(val):
        if pd.isna(val):
            return np.nan
        s = str(val).lower()
        if "easy" in s:
            return 1
        if "medium" in s:
            return 2
        if "hard" in s:
            return 3
        try:
            return float(val)
        except:  # NOQA E722
            return np.nan

    # -----------------------------
    # Build Clusters
    # -----------------------------
    def build_clusters(self):
        if self.df is None:
            self.load_data()

        features = self.df[
            ["latitude", "longitude", "elevation_m",
                "trek_time_hours", "difficulty_num"]
        ]

        # Scale features
        self.scaler = StandardScaler()
        X = self.scaler.fit_transform(features)

        # Train KMeans
        self.kmeans = KMeans(
            n_clusters=self.n_clusters, random_state=42, n_init=10
        )
        labels = self.kmeans.fit_predict(X)

        # Add cluster column
        self.df["cluster"] = labels.astype(int)

        # Build cluster counts
        self.cluster_counts = (
            self.df["cluster"].value_counts().sort_index().to_dict()
        )

        return self.df, self.cluster_counts

    # -----------------------------
    # Get Results
    # -----------------------------
    def get_clustered_data(self):
        if self.df is None:
            self.build_clusters()
        return self.df

    def get_cluster_counts(self):
        if self.cluster_counts is None:
            self.build_clusters()
        return self.cluster_counts
