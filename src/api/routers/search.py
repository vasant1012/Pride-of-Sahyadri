from fastapi import APIRouter
from src.core.data_loader import load_forts
from src.core.rag_engine import RAGEngine

router = APIRouter()

# Load dataset
DF = load_forts()

# Initialize RAG engine
try:
    rag = RAGEngine()
    rag.build_corpus(DF)
    rag.build_index()
except Exception as e:
    rag = None
    INIT_ERROR = str(e)
else:
    INIT_ERROR = None


@router.get("/semantic_search")
def semantic_search(q: str):
    """Semantic search / mini-QA endpoint.

    Args:
        q (str): query text
        top_k (int): number of results

    Returns:
        list of retrieved notes with similarity score
    """
    if rag is None:
        return {"error": f"RAG engine unavailable: {INIT_ERROR}"}

    try:
        results = rag.retrieve(q, top_k=3)
        context = rag.build_context(results)
        response = rag.generate_answer(context, q)
    except Exception as e:
        return {"error": str(e)}

    # format results
    return response
