from flask import Flask, request, jsonify
from flasgger import Swagger
import pickle
from flask_cors import CORS
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # <-- ici
swagger = Swagger(app)

# Chargement des fichiers nécessaires
with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

user_item_matrix = pd.read_pickle('user_item_matrix.pkl')
metadata = pd.read_pickle('metadata.pkl')
df_grouped = pd.read_pickle('df_grouped.pkl')

with open('id_to_index.pkl', 'rb') as f:
    id_to_index = pickle.load(f)

similarity_matrix_bert = np.load('similarity_matrix_bert.npy')
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Charger la vraie DataFrame des reviews (adapté à ton fichier)
# Exemple pickle :
all_reviews2 = pd.read_pickle('df_grouped.pkl')
# ou CSV si tu préfères :
# all_reviews2 = pd.read_csv('all_reviews_final.csv')

def recommander_hybride_par_titre(titre_saisi, top_n=5, alpha=0.5, beta=0.5):
    titre_embedding = bert_model.encode([titre_saisi])
    titres = df_grouped["title"].fillna("").tolist()
    titres_embeddings = bert_model.encode(titres)

    similarities = cosine_similarity(titre_embedding, titres_embeddings)[0]
    idx_best = similarities.argmax()

    logement_ref = df_grouped.iloc[idx_best]
    id_listing_ref = logement_ref["id_listing"]

    users_ayant_note = user_item_matrix[user_item_matrix[id_listing_ref].notna()].index.tolist()
    if not users_ayant_note:
        return {"error": "Aucun utilisateur trouvé ayant noté ce logement."}

    user_vector_moyen = user_item_matrix.loc[users_ayant_note].mean()

    distances, indices = knn_model.kneighbors([user_vector_moyen.fillna(0)], n_neighbors=10)
    similar_users = user_item_matrix.index[indices.flatten()[1:]]

    logements_candidats = user_item_matrix.loc[similar_users].mean().dropna()
    logements_candidats = logements_candidats.drop(id_listing_ref, errors='ignore')

    results = []
    idx_ref = id_to_index.get(id_listing_ref)

    for id_logement, note_estimee in logements_candidats.items():
        idx_candidat = id_to_index.get(id_logement)
        if idx_candidat is None or idx_ref is None:
            continue

        sim_bert = similarity_matrix_bert[idx_ref, idx_candidat]
        score_final = alpha * float(sim_bert) + beta * (float(note_estimee) / 5.0)

        meta = metadata[metadata["id_listing"] == id_logement]
        rating = meta["rating_review_moyen"].values[0] if not meta.empty else None
        accuracy = meta["accuracy_moyen"].values[0] if not meta.empty else None

        subset = all_reviews2[all_reviews2["id_listing"] == id_logement]
        if not subset.empty:
            infos = subset.iloc[0].to_dict()
        else:
            infos = {}

        reviews_pos = all_reviews2[
            (all_reviews2["id_listing"] == id_logement) & 
            (all_reviews2["sentiment_bert"] == "positive")
        ]["localizedText"].dropna().tolist()

        results.append({
            "id_listing": int(id_logement),
            "score": float(score_final),
            "similarity_bert": float(sim_bert),
            "note_estimée_knn": float(note_estimee),
            "rating": float(rating) if rating is not None else None,
            "accuracy": float(accuracy) if accuracy is not None else None,
            "title": infos.get("title", None),
            "city_listing": infos.get("city_listing", None),
            "description": (infos.get("description", "")[:300] + "...") if infos.get("description") else None,
            "sentiment_moyen": float(infos.get("sentiment_moyen", 0)) if "sentiment_moyen" in infos else None,
            "reviews_positives": reviews_pos[:3]
        })

    top_results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]

    return {"recommendations": top_results}

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Obtenir des recommandations hybrides à partir d’un titre
    ---
    tags:
      - Recommandation
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: "Appartement moderne avec vue sur mer"
    responses:
      200:
        description: Résultats de recommandation
        schema:
          type: object
          properties:
            recommendations:
              type: array
              items:
                type: object
                properties:
                  id_listing:
                    type: integer
                  score:
                    type: number
                  similarity_bert:
                    type: number
                  note_estimée_knn:
                    type: number
                  rating:
                    type: number
                  accuracy:
                    type: number
                  title:
                    type: string
                  city_listing:
                    type: string
                  description:
                    type: string
                  sentiment_moyen:
                    type: number
                  reviews_positives:
                    type: array
                    items:
                      type: string
    """
    data = request.json
    titre = data.get('title', '')
    if not titre:
        return jsonify({"error": "Title is required"}), 400

    recommendations = recommander_hybride_par_titre(titre)
    return jsonify(recommendations)

@app.route('/')
def index():
    return "Bienvenue dans le système de recommandation. Accédez à la documentation Swagger via /apidocs/."

if __name__ == '__main__':
    app.run(debug=True)

