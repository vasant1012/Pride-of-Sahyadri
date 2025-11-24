# import sys
# sys.path.append("/home/vasant/projects/Pride-of-Sahyadri/src")
# from src.frontend.app import app

# if __name__ == "__main__":
#     app.run_server(debug=False, port=8050)

import requests
import pandas as pd

BASE = "http://localhost:8000"

def show(x):
    """Pretty print JSON or DataFrame intelligently."""
    if isinstance(x, list):
        if len(x) == 0:
            print("[] (empty list)")
        else:
            print(pd.DataFrame(x).head())
    elif isinstance(x, dict):
        print(x)
    else:
        print(x)


clusters = requests.get(f"{BASE}/clusters")
print(clusters)