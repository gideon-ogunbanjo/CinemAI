# importing libraires
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# Welcome Page and Page Configuration
st.set_page_config(
    page_title="CinemAI",
    initial_sidebar_state="expanded",
)

# Loading the data and performimg preprocessing as needed
movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')

# Creating a list unique genres from the genres column of the movies DataFrame
genres = []
for genre in movies.genres:
    x = genre.split('|')
    for i in x:
        if i not in genres:
            genres.append(str(i))
genres = str(genres)

# Creating a chart of the top 20 movies with the highest rating
df = pd.merge(ratings, movies, how='left', on='movieId')
df1 = df.groupby(['title'])[['rating']].sum()
high_rated = df1.nlargest(20, 'rating')

# Creating the tfdif vectorizer
model = TfidfVectorizer()
tfidf_matrix = model.fit_transform(movies['genres'])

# Calculating cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a Series for index lookup
indices = pd.Series(movies.index, index=movies['title'])
titles = movies['title']

# Defining recommendations function
def recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

# Streamlit UI
st.title("CinemAI - Movie Recommendation App")
st.write("CinemaAI is an advanced content-based movie recommendation system. Its primary aim is to provide personalized movie recommendations to users based on their movie preferences.")

# Input box for user to enter a movie title
user_input = st.text_input("Enter a movie title")

# Find the closest matching title
closest_title = titles[titles.str.contains(user_input, case=False)].iloc[0]
idx = indices[closest_title]

if st.button("Get Recommendations"):
    recommended_movies = recommendations(closest_title)
    
    st.write("Recommended Movies:")
    for movie in recommended_movies:
        st.write(movie)
        
        
link='Created by [Gideon Ogunbanjo](https://gideonogunbanjo.netlify.app)'
st.markdown(link,unsafe_allow_html=True)                                                                        