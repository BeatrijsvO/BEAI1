from sentence_transformers import SentenceTransformer

class SentenceTransformerWrapper:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, query):
        return self.model.encode([query], show_progress_bar=False)[0]