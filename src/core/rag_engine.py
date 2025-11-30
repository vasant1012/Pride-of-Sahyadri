import os
import json
import torch
from sentence_transformers import SentenceTransformer, util


class RAGEngine:
    def __init__(self, cache_dir="rag_cache"):
        self.df = None
        self.corpus = []
        self.embeddings = None
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.cache_dir = cache_dir

        # Create directory if missing
        os.makedirs(self.cache_dir, exist_ok=True)

        # Cache file paths
        self.corpus_file = os.path.join(cache_dir, "corpus.json")
        self.emb_file = os.path.join(cache_dir, "embeddings.pt")

    # -------------------------------------------------------
    # 1. LOAD DATA
    # -------------------------------------------------------
    def load_data(self, df):
        self.df = df
        self.corpus = []

        text_columns = [
            "name", "district", "type", "built_by", "era",
            "key_events", "notes", "water_availability",
            "trek_difficulty", "description"
        ]

        for _, row in df.iterrows():
            parts = [str(row.get(col, "")) for col in text_columns]
            combined = " | ".join(parts)
            self.corpus.append(combined)

        # Save corpus locally for future reuse
        with open(self.corpus_file, "w") as f:
            json.dump(self.corpus, f)

        print(f"RAGEngine: Corpus created with {len(self.corpus)} entries.")
        return self

    # -------------------------------------------------------
    # 2. BUILD OR LOAD INDEX
    # -------------------------------------------------------
    def build_index(self):
        # Try loading cached embeddings
        if os.path.exists(self.emb_file):
            print("RAGEngine: Loading cached embeddings...")
            self.embeddings = torch.load(self.emb_file)
            print("RAGEngine: Embeddings loaded from cache.")
            return self

        # Else build embeddings fresh
        print("RAGEngine: Building new embeddings...")
        self.embeddings = self.model.encode(
            self.corpus,
            convert_to_tensor=True
        )

        # Save embeddings to disk
        torch.save(self.embeddings, self.emb_file)
        print("RAGEngine: Embeddings created and cached.")

        return self

    # -------------------------------------------------------
    # 3. QUERY DOCUMENTS
    # -------------------------------------------------------
    def query(self, user_query, k=5):
        if self.embeddings is None:
            raise ValueError("Index not built. Call build_index().")

        q_emb = self.model.encode(user_query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(q_emb, self.embeddings)[0]

        top_idx = torch.topk(scores, k).indices.tolist()

        # Return raw dataframe rows (no formatting)
        return [self.df.iloc[i].to_dict() for i in top_idx]
    

    # -------------------------------------------------------
    # Extra: force rebuild (if needed)
    # -------------------------------------------------------
    def rebuild_index(self):
        """Manually rebuild all embeddings, ignoring cache."""
        print("RAGEngine: Force rebuilding embeddings...")
        self.embeddings = self.model.encode(
            self.corpus, convert_to_tensor=True
        )
        torch.save(self.embeddings, self.emb_file)
        print("RAGEngine: Rebuild complete.")
        return self
