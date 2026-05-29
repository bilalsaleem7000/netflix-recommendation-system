# import streamlit as st
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Load data
# df = pd.read_csv('netflix_titles.csv')
#
# # Preprocess
# df['listed_in'] = df['listed_in'].fillna('')
#
# # Vectorization
# cv = CountVectorizer(tokenizer=lambda x: x.split(', '))
# genre_matrix = cv.fit_transform(df['listed_in'])
#
# # Similarity
# similarity = cosine_similarity(genre_matrix)
#
#
# # Recommendation function
# def recommend(title):
#     try:
#         idx = df[df['title'] == title].index[0]
#         scores = list(enumerate(similarity[idx]))
#         scores = sorted(scores, key=lambda x: x[1], reverse=True)
#         scores = scores[1:6]
#
#         results = [df.iloc[i[0]]['title'] for i in scores]
#         return results
#     except:
#         return ["Title not found"]
#
#
# # UI
# st.title("🎬 Netflix Recommendation System")
#
# movie = st.text_input("Enter a movie or show name:")
#
# if st.button("Recommend"):
#     results = recommend(movie)
#
#     st.write("### Recommended for you:")
#     for r in results:
#         st.write(r)







#
#
# import streamlit as st
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Load data
# df = pd.read_csv('netflix_titles.csv')
#
# # Preprocess
# df['listed_in'] = df['listed_in'].fillna('')
#
# # Vectorization
# cv = CountVectorizer(tokenizer=lambda x: x.split(', '))
# genre_matrix = cv.fit_transform(df['listed_in'])
#
# # Similarity
# similarity = cosine_similarity(genre_matrix)
#
#
# # Recommendation function
# def recommend(title):
#     try:
#         idx = df[df['title'] == title].index[0]
#         scores = list(enumerate(similarity[idx]))
#         scores = sorted(scores, key=lambda x: x[1], reverse=True)
#         scores = scores[1:6]
#
#         results = [(df.iloc[i[0]]['title'], df.iloc[i[0]]['listed_in']) for i in scores]
#         return results
#     except:
#         return [("Title not found", "")]
#
#
# # UI
# st.title("🎬 Netflix Recommendation System")
#
# # Step 5: Improved description
# st.write("Find similar Netflix content based on genre 🎯")
#
# # Step 6: Dropdown instead of text input
# movie = st.selectbox("Choose a title:", df['title'].values)
#
# if st.button("Recommend"):
#     results = recommend(movie)
#
#     st.write("### Recommended for you:")
#
#     for title, genre in results:
#         st.write(f"**{title}**")
#         st.write(f"Genre: {genre}")
#         st.write("---")


import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔑 TMDb API Key
API_KEY = "90bcfcce1a0c5795297824414e11f046"

# Load dataset
df = pd.read_csv('netflix_titles.csv')
df['listed_in'] = df['listed_in'].fillna('')

# Vectorization
cv = CountVectorizer(tokenizer=lambda x: x.split(', '))
genre_matrix = cv.fit_transform(df['listed_in'])

# Similarity
similarity = cosine_similarity(genre_matrix)

# 🎬 Fetch data from TMDb
def fetch_movie_data(title):
    try:
        query = quote(title)

        url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"
        data = requests.get(url).json()

        if not data.get('results'):
            return None, "N/A", "No data found"

        # Prefer movie/tv results
        result = None
        for r in data['results']:
            if r.get('media_type') in ['movie', 'tv']:
                result = r
                break
        if result is None:
            result = data['results'][0]

        poster_path = result.get('poster_path')
        rating = result.get('vote_average', "N/A")
        overview = result.get('overview', "No description available")

        if poster_path:
            poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster = None

        return poster, rating, overview

    except:
        return None, "N/A", "Error fetching data"

# Recommendation function
def recommend(title):
    try:
        idx = df[df['title'] == title].index[0]
    except:
        return []

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = scores[1:11]  # top 10

    results = []
    for i in scores:
        movie_title = df.iloc[i[0]]['title']
        genre = df.iloc[i[0]]['listed_in']
        poster, rating, overview = fetch_movie_data(movie_title)

        # Convert rating to numeric for sorting
        try:
            numeric_rating = float(rating)
        except:
            numeric_rating = 0.0

        results.append((movie_title, genre, poster, rating, overview, numeric_rating))

    return results

# 🎨 UI CONFIG
st.set_page_config(page_title="Netflix Recommender", layout="wide")

st.title("🎬 Netflix Recommendation System")
st.write("Find similar Netflix content based on genre 🎯")

# Select movie
movie = st.selectbox("Choose a title:", df['title'].values)

# ⭐ Sort option
sort_option = st.selectbox(
    "Sort by Rating:",
    ["None", "High to Low", "Low to High"]
)

# Button
if st.button("Recommend"):
    results = recommend(movie)

    # Apply sorting
    if sort_option == "High to Low":
        results = sorted(results, key=lambda x: x[5], reverse=True)
    elif sort_option == "Low to High":
        results = sorted(results, key=lambda x: x[5])

    if not results:
        st.warning("No recommendations found.")
    else:
        st.subheader("Recommended for you")

        # Netflix-style grid
        num_cols = 5
        for i in range(0, len(results), num_cols):
            cols = st.columns(num_cols)

            for j, (title, genre, poster, rating, overview, numeric_rating) in enumerate(results[i:i+num_cols]):
                with cols[j]:
                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.write("No Image")

                    st.markdown(f"**{title}**")
                    st.markdown(f"⭐ {rating}")

                    with st.expander("Details"):
                        st.write(f"**Genre:** {genre}")
                        st.write(f"📝 {overview}")