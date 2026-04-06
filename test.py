from sentence_transformers import SentenceTransformer, util
import torch
import textwrap


class LocalRAG:
    def __init__(self, corpus_text, chunk_size=200, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        corpus_text: large input text
        chunk_size: number of words per chunk for retrieval
        """
        self.model = SentenceTransformer(model_name)
        self.chunks = self.create_chunks(corpus_text, chunk_size)
        self.embeddings = self.model.encode(
            self.chunks, convert_to_tensor=True)

    def create_chunks(self, text, size):
        """Split corpus into equal-sized word chunks."""
        words = text.split()
        return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

    def ask(self, question, top_k=2):
        """
        Retrieve most similar chunks and generate answer from them.
        """
        q_emb = self.model.encode(question, convert_to_tensor=True)
        scores = util.cos_sim(q_emb, self.embeddings)[0]
        top_idx = torch.topk(scores, top_k).indices.tolist()

        # Join top relevant text pieces → generate answer
        context = " ".join([self.chunks[i] for i in top_idx])

        answer = self.generate_answer(question, context)
        return answer

    def generate_answer(self, question, context):
        """
        Simple extractive response – summarises context around query.
        (You can replace with LLM later)
        """
        wrapped = textwrap.fill(context, width=90)
        return f"Answer based on corpus:\n{wrapped}"
