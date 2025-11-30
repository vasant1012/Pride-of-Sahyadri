from fastapi import APIRouter
from src.core.data_loader import load_forts
from src.core.rag_engine import RAGEngine
from src.core.llm_decoder import LLM_Decoder

router = APIRouter()

# Load dataset
DF = load_forts()

# Initialize RAG engine
try:
    rag = RAGEngine()
    rag.load_data(DF)
    rag.build_index()
    analyzer = LLM_Decoder(
            model_name="Qwen/Qwen2-1.5B-Instruct"
        )
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
        result = rag.query(q, k=1)
        response = analyzer.decode_response(result)
    except Exception as e:
        return {"error": str(e)}

    # format results
    return response
