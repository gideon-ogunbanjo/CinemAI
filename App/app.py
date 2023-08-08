# importing libraires
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

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