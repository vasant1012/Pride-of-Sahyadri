import sys
sys.path.append("/home/pamya/Python/ML_Projects/Pride-of-Sahyadri")
from src.frontend.app import app  # noqa: E402 (import after path setup)


if __name__ == "__main__":
    app.run_server(debug=False)
