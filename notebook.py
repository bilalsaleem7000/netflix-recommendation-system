import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


#dataset reading part
df = pd.read_csv('netflix_titles.csv')

df.head()


df.shape
df.info()
df.isnull().sum()

#
# #Data cleaning part
# # Remove duplicates
# # Remove duplicates
# df = df.drop_duplicates()
#
# # Fill missing values (correct way)
# df['director'] = df['director'].fillna('Unknown')
# df['cast'] = df['cast'].fillna('Unknown')
# df['country'] = df['country'].fillna('Unknown')
#
# # Clean date column
# df['date_added'] = df['date_added'].str.strip()
# df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
#
# # Drop rows where date is still invalid
# df = df.dropna(subset=['date_added'])
#
# # Extract year
# df['year_added'] = df['date_added'].dt.year
#
# # Clean country
# df['country'] = df['country'].str.split(',').str[0]
#
# # Clean duration
# df['duration'] = df['duration'].str.extract(r'(\d+)').astype(float)
#
#
# #Movies vs TV Shows part
# sns.countplot(x='type', data=df)
# plt.title("Movies vs TV Shows")
# plt.show()
#
#
#
# #Content Growth Over Time
# df['year_added'].value_counts().sort_index().plot(figsize=(10,5))
# plt.title("Content Added Over Time")
# plt.xlabel("Year")
# plt.ylabel("Count")
# plt.show()
#
#
# #Top Countries
# df['country'].value_counts().head(10).plot(kind='bar', figsize=(10,5))
# plt.title("Top 10 Content Producing Countries")
# plt.show()
#
#
# #Most Common Genres
# genres = df['listed_in'].str.split(', ').explode()
# genres.value_counts().head(10).plot(kind='barh')
# plt.title("Top Genres")
# plt.show()
#
#
#
# #Ratings Distribution
# sns.countplot(y='rating', data=df, order=df['rating'].value_counts().index)
# plt.title("Ratings Distribution")
# plt.show()
#
#
# #Movie Duration Analysis
# movies = df[df['type'] == 'Movie']
#
# movies['duration'].hist()
# plt.title("Movie Duration Distribution")
# plt.xlabel("Minutes")
# plt.show()
#
#
#
#
# #Top Directors
# df['director'].value_counts().head(10)
#
#
# #Top Actors
# actors = df['cast'].str.split(', ').explode()
# actors.value_counts().head(10)
#



## NETFLIX RECOMMENDATION SYSTEM

#preparing data
from sklearn.feature_extraction.text import CountVectorizer

# Fill missing genres
df['listed_in'] = df['listed_in'].fillna('')

# Convert text to vectors
cv = CountVectorizer(tokenizer=lambda x: x.split(', '))

genre_matrix = cv.fit_transform(df['listed_in'])


#Compute Similarity
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(genre_matrix)


#Build Recommendation Function
def recommend(title):
    idx = df[df['title'] == title].index[0]

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Top 5 similar
    scores = scores[1:6]

    for i in scores:
        print(df.iloc[i[0]]['title'])



#running
recommend("Narcos")