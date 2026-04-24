import sys
sys.path.append("/home/vasant/projects/Pride-of-Sahyadri/")
from src.frontend.app import app  # noqa: E402 (import after path setup)


if __name__ == "__main__":
    app.run_server(debug=False)
