import pickle
import streamlit as st
import pandas as pd
import requests
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

movies_data = pickle.load(open("movies.pkl", "rb"))

if isinstance(movies_data, dict):
    movies = pd.DataFrame(movies_data)
else:
    movies = movies_data

similarity = pickle.load(open("similarity.pkl", "rb"))


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": st.secrets["TMDB_API_KEY"],
        "language": "en-US"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return None

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]["movie_id"]
        movie_title = movies.iloc[i[0]]["title"]

        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------------- UI ----------------

st.markdown(
    """
    <h1 style="text-align: center;">
        🎬 Movie Recommendation System
    </h1>

    <p style="text-align: center; font-size: 18px; color: gray;">
        Find movies similar to your favorites
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

selected_movie = st.selectbox(
    "🎥 Select a movie",
    movies["title"].values
)

if st.button("🍿 Recommend Movies", use_container_width=True):

    recommended_movies, recommended_posters = recommend(selected_movie)

    st.markdown("## Recommended for you")

    columns = st.columns(5)

    for i in range(5):
        with columns[i]:

            if recommended_posters[i]:
                st.image(
                    recommended_posters[i],
                    use_container_width=True
                )

            st.markdown(
                f"""
                <h4 style="text-align: center;">
                    {recommended_movies[i]}
                </h4>
                """,
                unsafe_allow_html=True
            )

st.divider()

st.markdown(
    """
    <p style="text-align: center; color: gray;">
        Built with Python • Machine Learning • Streamlit
    </p>
    """,
    unsafe_allow_html=True
)