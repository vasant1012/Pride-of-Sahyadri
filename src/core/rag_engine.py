from sentence_transformers import SentenceTransformer, util
import torch


class RAGEngine:
    def __init__(self):
        self.df = None
        self.corpus = []
        self.embeddings = None
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # -------------------------------------------------------
    # 1. LOAD DATA
    # -------------------------------------------------------
    def load_data(self, df):
        """
        Loads DataFrame and builds concatenated corpus for embeddings.
        Output of RAG = original df rows (no processing).
        """
        self.df = df
        self.corpus = []

        text_columns = [
            "name", "district", "type", "built_by", "era",
            "key_events", "notes", "water_availability",
            "trek_difficulty", "description"
        ]

        for _, row in df.iterrows():
            # Safe text fusion without modifying text content
            parts = [str(row.get(col, "")) for col in text_columns]
            combined = " | ".join(parts)  # simple join, no formatting

            self.corpus.append(combined)

        print(f"RAGEngine: Loaded corpus with {len(self.corpus)} items.")
        return self

    # -------------------------------------------------------
    # 2. BUILD INDEX
    # -------------------------------------------------------
    def build_index(self):
        if not self.corpus:
            raise ValueError("Data not loaded. Call load_data() first.")

        print("RAGEngine: Generating embeddings...")
        self.embeddings = self.model.encode(self.corpus, convert_to_tensor=True)
        print("RAGEngine: Index built.")
        return self

    # -------------------------------------------------------
    # 3. QUERY (NO POST PROCESSING)
    # -------------------------------------------------------
    def query(self, user_query, k=5):
        """
        RAG search:
        - Uses semantic similarity
        - Returns ORIGINAL dataframe rows (as dictionaries)
        - NO transformations, NO natural language formatting
        """

        if self.embeddings is None:
            raise ValueError("Index not built. Call build_index().")

        # Encode query
        q_emb = self.model.encode(user_query, convert_to_tensor=True)

        # Compute similarity
        scores = util.pytorch_cos_sim(q_emb, self.embeddings)[0]
        top_idx = torch.topk(scores, k).indices.tolist()

        # Return original DataFrame rows EXACTLY as stored
        results = [self.df.iloc[i].to_dict() for i in top_idx]
        return results