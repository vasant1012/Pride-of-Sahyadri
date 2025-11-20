# 🏰 Pride-of-Sahyadri  
### *AI-Powered Maharashtra Forts Explorer & Knowledge Engine*

**Pride-of-Sahyadri** is an AI-driven exploration and intelligence platform built around the historic forts of Maharashtra, India.  
It blends **Machine Learning**, **Semantic Search**, **Geospatial Analysis**, and a clean **FastAPI backend** to create a powerful knowledge hub for trekkers, historians, researchers, and proud Maharashtrians who value the Sahyadri heritage.

This project honors the legacy of the Maratha Empire and the timeless forts that stand as symbols of resilience, strategy, and regional pride.

---

## 📜 Dataset Credits
This project uses the Maharashtra Forts dataset curated by:

> **Tushar B. Kute**  
> Dataset Source (Kaggle): *Maharashtra Forts — 350+ forts with detailed metadata*

A big thanks to the author for compiling such a rich resource.

---

## 🚀 Features

### 🔍 1. **Semantic RAG Search**
Query the fort knowledge base naturally:

- “Forts built by Shivaji Maharaj”
- “Easy monsoon treks near Pune”
- “Sea forts with historical battles”
- “Forts important in Maratha-Nizam conflict”

RAG engine uses **Sentence-Transformers (MiniLM)** to retrieve the most relevant fort entries —  
**no post-processing**, returning raw fort metadata exactly as stored.

---

### 🧠 2. **Clean RAG Engine Architecture**
A minimalistic 3-function design:

| Function        | Description |
|----------------|-------------|
| `load_data(df)` | Load DataFrame & build text corpus |
| `build_index()` | Encode all corpus entries as embeddings |
| `query(text)`   | Return top-k fort records based on semantic similarity |

Optimized for API usage and downstream LLM processing.

---

### 🧭 3. **Recommendation System**
✔ Nearby forts by geodesic distance  
✔ Similar forts via embedding proximity  
✔ Useful for trek route planning and tourism recommendations

---

### 🗺️ 4. **Geospatial Clustering**
K-means clustering across:

- Latitude  
- Longitude  
- Elevation  
- Trek difficulty  

Provides geographic insight into fort groupings.

---

### 📡 5. **FastAPI Backend**
A clean REST API with the following endpoints:

- `GET /forts`  
- `GET /forts/{fort_id}`  
- `GET /search/qa`  
- `GET /clusters`  
- `GET /clusters/predict`  
- `GET /recommend/nearby`  
- `GET /recommend/similar/{fort_id}`  

Interactive documentation:  
👉 http://localhost:8000/docs

---

### 🌐 6. **Dash App UI**
A simple, user-friendly UI for:

- Searching forts  
- Viewing details  
- Finding nearby forts  
- Running NLQ queries via API  

Ideal for explorers and tourism apps.

---

## 📁 Project Structure

├── data/
│ └── maharashtra-forts.csv
├── src/
│ ├── core/
│ │ ├── data_loader.py
│ │ ├── preprocess.py
│ │ ├── rag_engine.py
│ │ ├── cluster_engine.py
│ │ ├── recommender.py
│ │ └── trek_predictor.py
│ └── api/
│ ├── main.py
│ └── routers/
│ ├── forts.py
│ ├── search.py
│ ├── clustering.py
│ └── recommend.py
├── dash_app.py
├── tests/
│ ├── test_data_loader.py
│ └── test_api.py
├── requirements.txt
└── README.md

