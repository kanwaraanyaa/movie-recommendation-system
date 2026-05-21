print("Model started")
import pandas as pd
import ast
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv('data/movies.csv')
credits = pd.read_csv('data/credits.csv')

# Merge datasets
movies = movies.merge(credits, on='title')

# Keep important columns
movies = movies[['movie_id', 'title', 'overview',
                 'genres', 'keywords',
                 'cast', 'crew']]

# Remove missing values
movies.dropna(inplace=True)

# Convert JSON-like text into lists
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Get top 3 cast members
def convert_cast(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert_cast)

# Get director name
def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

# Convert overview into list
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces
def collapse(L):
    return [i.replace(" ", "") for i in L]

movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)

# Create tags
movies['tags'] = movies['overview'] + movies['genres'] + \
                 movies['keywords'] + movies['cast'] + movies['crew']

# New dataframe
new = movies[['movie_id', 'title', 'tags']]

# Convert list to string
new['tags'] = new['tags'].apply(lambda x: " ".join(x))

# Lowercase
new['tags'] = new['tags'].apply(lambda x: x.lower())

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new['tags']).toarray()

# Similarity matrix
similarity = cosine_similarity(vectors)

# Save files
import pickle

with open('movies.pkl', 'wb') as f:
    pickle.dump(new, f)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)


print("Model files saved successfully!")