from sentence_transformers import SentenceTransformer
from backend.core.logger import logger
import numpy as np
import requests
import torch
import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"


class RAGEngine:
    def __init__(self, cache_dir="rag_cache"):
        self.df = None
        self.cache_dir = cache_dir

        # Create directory if missing
        os.makedirs(self.cache_dir, exist_ok=True)

        # Cache file paths
        self.corpus_file = os.path.join(cache_dir, "corpus.txt")
        self.emb_file = os.path.join(cache_dir, "embeddings.pt")

        self.corpus = ""
        self.embeddings = None
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

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
            logger.info(f"The file '{self.corpus_file}' exists.")
            with open(self.corpus_file, "r") as file:
                self.corpus = file.read()
        else:
            logger.info(f"The file '{self.corpus_file}' does not exist.")
            self.corpus_list = []

            for _, row in df.iterrows():
                self.corpus_list.append(self.fort_dict_to_paragraph(row))

            self.corpus = "\n".join(line.strip() for line in self.corpus_list)

            # Save corpus locally for future reuse
            with open(self.corpus_file, "w") as file_object:
                file_object.write(self.corpus)

        logger.info(f"RAGEngine: Corpus created with {len(self.corpus)} entries.")  # NOQA E501
        return self

    # -------------------------------------------------------
    # 2. CHUNKING THE TEXT
    # -------------------------------------------------------
    def chunk_by_sentences(self, text, chunk_size=5, overlap=2):
        sentences = text.split("\n")
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        start = 0

        while start < len(sentences):
            end = start + chunk_size
            chunk = " ".join(sentences[start:end])
            chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    # -------------------------------------------------------
    # 3. BUILD OR LOAD INDEX
    # -------------------------------------------------------
    def build_index(self):
        self.chunks = self.chunk_by_sentences(self.corpus)
        # Try loading cached embeddings
        if os.path.exists(self.emb_file):
            logger.info("RAGEngine: Loading cached embeddings...")
            self.embeddings = torch.load(self.emb_file)
            logger.info("RAGEngine: Embeddings loaded from cache.")
            return self

        # Else build embeddings fresh
        logger.info("RAGEngine: Building new embeddings...")
        self.embeddings = self.embed_model.encode(
            self.chunks, convert_to_tensor=True, show_progress_bar=True
        )
        logger.info(f"Embedding shape: {self.embeddings.shape}")

        # Save embeddings to disk
        torch.save(self.embeddings, self.emb_file)
        logger.info("RAGEngine: Embeddings created and cached.")

        return self

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # -------------------------------------------------------
    # 3. QUERY DOCUMENTS
    # -------------------------------------------------------
    def retrieve(self, query, top_k=3):
        query_vec = self.embed_model.encode([query])[0]

        scores = np.dot(self.embeddings, query_vec) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec)
        )

        top_indices = np.argsort(scores)[-top_k:][::-1]

        return [(self.chunks[i], scores[i]) for i in top_indices]

    # -------------------------------------------------------
    # 3. BUILD CONTEXT
    # -------------------------------------------------------
    def build_context(self, results):
        return "\n\n".join([chunk for chunk, _ in results])

    def generate_answer(self, context, query):
        prompt = (
            "You are a precise assistant. Answer ONLY from the context. "
            "If the answer is not in the context, reply exactly: Not found. "
            "Keep the answer to 1-3 short sentences.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "qwen2:1.5b-instruct",
                  "prompt": prompt, "stream": False},
        )

        return response.json()["response"]
