import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHROMA_PATH = str(PROJECT_ROOT / "chroma_db")
COLLECTION_NAME = "jira_knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"

_client = None
_collection = None
_model = None


def get_collection():

    global _client
    global _collection

    if _collection is None:

        _client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    return _collection


def get_model():

    global _model

    if _model is None:

        _model = SentenceTransformer(
            MODEL_NAME,
            local_files_only=True
        )

    return _model


def search_knowledge_base(query):

    if not query or not query.strip():

        return ""

    try:

        collection = get_collection()

        if collection.count() == 0:

            return ""

        model = get_model()

        query_embedding = model.encode(
            query
        ).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        return "\n".join(documents)

    except Exception as error:

        print(f"Knowledge base search skipped: {error}")

        return ""
