from src.core.rag_engine import SimpleRAG
from src.core.data_loader import load_forts

# Test data loading
df = load_forts()

rag = SimpleRAG()
rag.build_index(df, text_column='notes')
print(rag.query(q="sea fort"))