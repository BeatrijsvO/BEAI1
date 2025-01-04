from langchain_community.vectorstores import FAISS

class FAISSManager:
    def __init__(self, embeddings_model, storage_path):
        self.embeddings_model = embeddings_model
        self.storage_path = storage_path
        self.vectorstore = None

    def load_or_create(self):
        if self.storage_path.exists():
            self.vectorstore = FAISS.load_local(str(self.storage_path), self.embeddings_model, allow_dangerous_deserialization=True)
        else:
            raise ValueError("FAISS-bestand niet gevonden. Upload eerst documenten.")
        return self.vectorstore

    def save(self):
        if self.vectorstore:
            self.vectorstore.save_local(str(self.storage_path))

    def add_texts(self, texts):
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_texts(texts, self.embeddings_model)
        else:
            self.vectorstore.add_texts(texts)
        self.save()