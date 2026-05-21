import streamlit as st
import pickle
import requests

from auth import add_user, login_user

# ================= LOAD DATA =================

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Netflix Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<h1 style='color:#E50914; font-size:60px; font-weight:900;'>
NETFLIX
</h1>
""", unsafe_allow_html=True)

# ================= SESSION =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= FUNCTIONS =================

def fetch_poster(movie_id):

    api_key = "YOUR_API_KEY"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:

        response = requests.get(url, timeout=10)

        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:

            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

            return full_path

        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except Exception as e:

        print(e)

        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_movies_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_movies_posters

# ================= SIDEBAR =================

menu = ["Login", "Signup"]

choice = st.sidebar.selectbox(
    "Menu",
    menu
)

# ================= AUTH PAGES =================

if not st.session_state.logged_in:

    # ---------- SIGNUP ----------

    if choice == "Signup":

        st.title("Create New Account")

        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):

            add_user(new_user, new_email, new_password)

            st.success("Account created successfully!")
            st.info("Go to Login page")

    # ---------- LOGIN ----------

    elif choice == "Login":

        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(username, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:
                st.error("Invalid username or password")

# ================= HOME PAGE =================

if st.session_state.logged_in:

    st.sidebar.success(f"Welcome {st.session_state.username}")

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    st.title("NETFLIX MOVIE RECOMMENDER")

    st.subheader("Discover movies you'll love 🍿")

    selected_movie = st.selectbox(
        "Choose a movie",
        movies['title'].values
    )

    if st.button("Recommend"):

        names, posters = recommend(selected_movie)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(names[0])
            st.image(posters[0])

        with col2:
            st.text(names[1])
            st.image(posters[1])

        with col3:
            st.text(names[2])
            st.image(posters[2])

        with col4:
            st.text(names[3])
            st.image(posters[3])

        with col5:
            st.text(names[4])
            st.image(posters[4])