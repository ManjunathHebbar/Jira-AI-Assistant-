from knowledge_base.vector_store import (
    search_knowledge_base
)


def build_rag_context(
    title,
    description
):

    query = f"""
    {title}

    {description}
    """

    knowledge = search_knowledge_base(
        query
    )

    return knowledge