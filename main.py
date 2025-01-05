from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from pydantic import BaseModel
import os

# Laad het .env-bestand
load_dotenv()

# Initialiseer de app
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiseer de embeddings
class SentenceTransformerWrapper:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, query):
        return self.model.encode([query], show_progress_bar=False)[0]

embeddings_model = SentenceTransformerWrapper()

# Initialiseer vectorstore
vectorstore = FAISS.from_texts(["CKBA vectorstore geinitialiseerd"], embeddings_model)

# Helperfuncties
def retrieve_documents(query, k=3):
    if not vectorstore:
        raise HTTPException(status_code=500, detail="Vectorstore niet beschikbaar.")
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

def generate_answer(question, context):
    prompt = (
        f"Gebruik de onderstaande informatie om de vraag te beantwoorden:\n"
        f"{context}\n\n"
        f"Vraag: {question}\nAntwoord:"
    )
    nlp_pipeline = pipeline("text-generation", model="bigscience/bloomz-1b7")
    result = nlp_pipeline(prompt, max_length=200, truncation=True)
    return result[0]["generated_text"]

# Endpoints
@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to CKBA!"}

@app.post("/upload")
async def upload_documents(files: list[UploadFile]):
    try:
        documents = []
        allowed_types = ["text/plain"]

        for file in files:
            if file.content_type not in allowed_types:
                raise HTTPException(status_code=400, detail=f"Bestandstype {file.content_type} niet toegestaan.")

            content = (await file.read()).decode("utf-8")
            texts = content.split("\n")
            file_documents = [Document(page_content=text.strip(), metadata={"source": file.filename}) for text in texts if text.strip()]
            documents.extend(file_documents)

        vectorstore.add_texts([doc.page_content for doc in documents])
        return {"message": f"{len(documents)} documenten succesvol geupload en verwerkt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fout bij upload: {str(e)}")

class QuestionRequest(BaseModel):
    question: str

@app.post("/answer")
async def answer_question(request: QuestionRequest):
    try:
        context = "\n".join(retrieve_documents(request.question, k=3))
        answer = generate_answer(request.question, context)
        return {"question": request.question, "context": context, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fout bij beantwoording: {str(e)}")