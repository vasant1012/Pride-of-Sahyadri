from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from typing import List
import pickle


class TrekDifficultyModel:
    """Wraps a RandomForestClassifier for predicting trek difficulty.

    The model expects NUMERIC target labels. If your target column is
    textual (e.g., 'Moderate', 'Hard', 'Easy'), encode it first using
    LabelEncoder via the preprocess module.
    """

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=None,
            random_state=42
        )
        self.trained = False

    def fit(self, df: pd.DataFrame, feature_cols: List[str], target_col: str = 'trek_difficulty_le') -> None:
        """Train the RandomForest model.

        Args:
            df (pd.DataFrame): training DataFrame
            feature_cols (List[str]): list of numeric feature columns
            target_col (str): label-encoded trek difficulty column
        """

        # Drop rows where required fields are missing
        clean = df.dropna(subset=feature_cols + [target_col])
        if clean.shape[0] == 0:
            raise ValueError('No valid training rows available after dropping NA.')

        X = clean[feature_cols]
        y = clean[target_col]

        self.model.fit(X, y)
        self.trained = True

    def predict(self, X_df: pd.DataFrame):
        """Predict trek difficulty.

        Args:
            X_df (pd.DataFrame): input features (must match training feature_cols)
        Returns:
            ndarray: predicted numeric labels
        """
        if not self.trained:
            raise RuntimeError('TrekDifficultyModel must be trained or loaded before prediction.')

        return self.model.predict(X_df)

    def save(self, path: str) -> None:
        """Save model to disk using pickle."""
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, path: str) -> None:
        """Load model from disk."""
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
            self.trained = True
