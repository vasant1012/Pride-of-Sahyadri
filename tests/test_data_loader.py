import sys
sys.path.append("/home/pamya/Python/ML_Projects/maharashtra-forts")
from src.core.data_loader import load_forts


def test_load_exists():
    """Test that the CSV loads and returns a non-empty DataFrame."""
    df = load_forts()
    assert df.shape[0] > 0, "Dataset should not be empty"
    assert 'name' in df.columns, "Column 'name' must exist in dataset"
    assert 'district' in df.columns, "Column 'district' must exist in dataset"
