from pathlib import Path
from knowledge_base.vector_store import get_collection, get_model

# ==========================================
# CONFIG
# ==========================================

# Jira status names that mean "done" — adjust to match your workflow
RESOLVED_STATUSES = {"done", "closed", "resolved", "complete", "completed"}

DOCS_PATH = Path(__file__).resolve().parent / "docs"


def is_ticket_resolved(fields: dict) -> bool:
    """Returns True if the ticket status means it's closed/done."""

    status_name = (
        fields
        .get("status", {})
        .get("name", "")
        .lower()
        .strip()
    )

    print(f"\nTICKET STATUS: '{status_name}'")

    return status_name in RESOLVED_STATUSES


def save_ticket_to_knowledge_base(
    issue_key: str,
    title: str,
    description: str,
    comments: str,
    root_cause: str,
    sentiment: str
) -> bool:
    """
    Saves a resolved ticket as a KB entry in ChromaDB.
    Uses the issue_key as the document ID so re-saves are safe (upsert).
    Also writes a .txt snapshot to knowledge_base/docs/ for visibility.
    Returns True if saved, False if skipped.
    """

    doc_id = f"resolved/{issue_key}"

    # ==========================================
    # BUILD KB DOCUMENT
    # ==========================================

    kb_entry = f"""========================================
TITLE: {title}
TICKET: {issue_key}
========================================

Description:
{description}

Root Cause:
{root_cause}

Customer Sentiment:
{sentiment}
"""

    if comments.strip():
        kb_entry += f"""
Comments Summary:
{comments}
"""

    kb_entry += f"""
Keywords:
{_extract_keywords(title, description)}
"""

    # ==========================================
    # SAVE TO CHROMADB
    # ==========================================

    try:

        collection = get_collection()

        model = get_model()

        embedding = model.encode(kb_entry).tolist()

        collection.upsert(
            documents=[kb_entry],
            embeddings=[embedding],
            ids=[doc_id]
        )

        print(f"\nKB SAVED: {issue_key} → ChromaDB ({doc_id})")

    except Exception as error:

        print(f"\nKB SAVE FAILED (ChromaDB): {error}")

        return False

    # ==========================================
    # WRITE SNAPSHOT .TXT (optional, for review)
    # ==========================================

    try:

        DOCS_PATH.mkdir(parents=True, exist_ok=True)

        snapshot_path = DOCS_PATH / f"{issue_key}.txt"

        with open(snapshot_path, "w", encoding="utf-8") as f:

            f.write(kb_entry)

        print(f"KB SNAPSHOT: Written to docs/{issue_key}.txt")

    except Exception as error:

        # Non-fatal — ChromaDB save already succeeded
        print(f"KB snapshot write failed (non-fatal): {error}")

    return True


def _extract_keywords(title: str, description: str) -> str:
    """
    Simple keyword extraction — pulls meaningful words from title + description.
    For production, replace with a proper NLP approach if needed.
    """

    stop_words = {
        "the", "a", "an", "is", "in", "on", "at", "to", "for",
        "of", "and", "or", "but", "not", "with", "this", "that",
        "it", "was", "are", "be", "by", "from", "as", "has", "have",
        "had", "i", "we", "you", "they", "he", "she", "its"
    }

    words = (title + " " + description).lower().split()

    keywords = list(dict.fromkeys(
        w.strip(".,!?;:()[]") for w in words
        if len(w) > 3 and w not in stop_words
    ))

    return ", ".join(keywords[:15])