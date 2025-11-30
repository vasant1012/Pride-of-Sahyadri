from fastapi import APIRouter
from src.core.data_loader import load_forts
from src.core.rag_engine import RAGEngine

router = APIRouter()

# Load dataset
DF = load_forts()

# Initialize RAG engine
try:
    rag = RAGEngine()
    rag.load_data(DF)
    rag.build_index()
except Exception as e:
    rag = None
    INIT_ERROR = str(e)
else:
    INIT_ERROR = None


@router.get("/semantic_search")
def semantic_search(q: str, top_k: int = 3):
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
        result = rag.query(q, k=top_k)
    except Exception as e:
        return {"error": str(e)}

    # format results
    return result
