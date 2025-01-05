from sentence_transformers import SentenceTransformer
import faiss

class SimpleVectorStore:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.embeddings_model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []

    def add_texts(self, texts):
        self.texts.extend(texts)
        embeddings = self.embeddings_model.encode(texts, show_progress_bar=True)
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query, top_k=3):
        query_embedding = self.embeddings_model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.texts[i] for i in indices[0]]
        return results

    def save_store(self, path="vectorstore.index"):
        """Sla de FAISS-index op naar disk."""
        if self.index is not None:
            faiss.write_index(self.index, path)
        else:
            raise ValueError("FAISS-index is leeg en kan niet worden opgeslagen.")

    def load_store(self, path="vectorstore.index"):
        """Laad de FAISS-index van disk."""
        try:
            self.index = faiss.read_index(path)
        except Exception as e:
            raise ValueError(f"Fout bij het laden van de FAISS-index: {e}")
