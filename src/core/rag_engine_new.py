import os
import torch
from sentence_transformers import SentenceTransformer, util


class RAGEngine:
    def __init__(self, cache_dir="rag_cache"):
        self.df = None
        self.cache_dir = cache_dir

        # Create directory if missing
        os.makedirs(self.cache_dir, exist_ok=True)

        # Cache file paths
        self.corpus_file = os.path.join(cache_dir, "corpus.txt")
        self.emb_file = os.path.join(cache_dir, "embeddings.pt")

        self.corpus = ''
        self.embeddings = None
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def fort_dict_to_paragraph(self, data: dict) -> str:
        return (
            f"{data['name']} is a {data['type']} located in "
            f"{data['taluka']}, {data['district']} district. It was built by "
            f"{data['built_by']} during the {data['era']} around {data['year_of_construction']}. "  # NOQA E501
            f"The fort stands at an elevation of about {data['elevation_m']} meters above sea level "  # NOQA E501
            f"and is currently in a {data['current_condition']} condition. "
            f"Historically, it served as {data['key_events']}. "
            f"The base village for the fort is {data['base_village']}, situated at latitude "  # NOQA E501
            f"{data['latitude']} and longitude {data['longitude']}. "
            f"The trek to the fort is considered {data['trek_difficulty']} and generally takes "  # NOQA E501
            f"around {data['trek_time_hours']} hour(s). The best season to visit the fort is during "  # NOQA E501
            f"{data['best_season']}. Water availability at the fort includes {data['water_availability']}, "  # NOQA E501
            f"and accommodation options are available in {data['accommodation']}. "  # NOQA E501
            f"Additional facts: {data['notes']}"
        )

    # -------------------------------------------------------
    # 1. LOAD DATA
    # -------------------------------------------------------
    def build_corpus(self, df):
        if os.path.exists(self.corpus_file):
            print(f"The file '{self.corpus_file}' does not exist.")
            with open(self.corpus_file, 'r') as file:
                self.corpus = file.read()
        else:
            print(f"The file '{self.corpus_file}' does not exist.")
            self.corpus_list = []

            for _, row in df.iterrows():
                self.corpus_list.append(self.fort_dict_to_paragraph(row))

            self.corpus = "\n".join(line.strip() for line in self.corpus_list)

            # Save corpus locally for future reuse
            with open(self.corpus_file, 'w') as file_object:
                file_object.write(self.corpus)

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
