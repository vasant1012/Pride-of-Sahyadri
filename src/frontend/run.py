import sys
sys.path.append("/home/vasant/projects/Pride-of-Sahyadri/src")
from frontend import app

if __name__ == "__main__":
    app.run_server(debug=False, port=8050)
