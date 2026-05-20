import os
import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_base.vector_store import (
    CHROMA_PATH,
    COLLECTION_NAME,
    MODEL_NAME,
    get_collection
)

# ==========================================
# CONFIG
# ==========================================

DOCS_PATH = Path(__file__).resolve().parent / "docs"
KB_FILE = Path(__file__).resolve().parent / "jira_kb.txt"


def load_documents():

    documents = []

    ids = []

    print("\nReading knowledge base files...\n")

    for filename in os.listdir(DOCS_PATH):

        filepath = os.path.join(
            DOCS_PATH,
            filename
        )

        if not filename.endswith(".txt"):

            continue

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read().strip()

                if not content:

                    print(f"Skipping empty file: {filename}")

                    continue

                documents.append(content)

                ids.append(f"docs/{filename}")

                print(f"Loaded: {filename}")

        except Exception as error:

            print(f"Failed reading {filename}")

            print(str(error))

    if KB_FILE.exists():

        with open(
            KB_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        chunks = content.split("\n\n")

        for index, chunk in enumerate(chunks):

            chunk = chunk.strip()

            if not chunk:

                continue

            documents.append(chunk)

            ids.append(f"jira_kb/{index}")

        print(f"Loaded: {KB_FILE.name}")

    return documents, ids


def main():

    collection = get_collection()

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME,
        local_files_only=True
    )

    print("Model loaded successfully")

    documents, ids = load_documents()

    if not documents:

        print("\nNo documents found.")

        return

    print("\nGenerating embeddings...")

    embeddings = model.encode(
        documents
    ).tolist()

    print("Embeddings generated")

    existing_ids = collection.get().get("ids", [])

    if existing_ids:

        print("\nRemoving old embeddings...")

        collection.delete(
            ids=existing_ids
        )

    print("\nSaving to ChromaDB...")

    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    print("\n===================================")
    print("Knowledge Base Ingested Successfully")
    print(f"Database Path: {CHROMA_PATH}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Total Documents: {len(documents)}")
    print("===================================\n")


if __name__ == "__main__":

    main()
