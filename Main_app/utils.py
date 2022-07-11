import requests, pandas as pd, pickle
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity




movies_data = pd.read_csv('Application/Main_app/data/Processed_data.csv')
genres = pickle.load(open('Application/Main_app/data/genres.pkl', 'rb'))
cast = pickle.load(open('Application/Main_app/data/cast.pkl', 'rb'))
directors = pickle.load(open('Application/Main_app/data/directors.pkl', 'rb'))


def stem(text):
    ps = PorterStemmer()
    x = []
    for i in text.split():
        x.append(ps.stem(i))
    return " ".join(x)



def get_details(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=58be5aa37f4b049afa12aa16b671e947&language=en-US')
    except:
        return {"movie_name": "ServerTimedOut"}
    details = {}
    data = response.json()
    details['id'] = movie_id
    details['movie_name'] = movies_data[movies_data['id'] == movie_id]['title'].values[0]
    details['movie_overview'] = movies_data[movies_data['id'] == movie_id]['overview'].values[0]

    try:
        details['movie_poster'] = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    except:
        details['movie_poster'] = "Picture"
    try:
        details['movie_release'] = data['release_date']
    except:
        details['movie_release'] = "Unknown Release"
    return details


def get_recommendations(movie):
    try:
        movie_index = movies_data[movies_data['title'] == movie].index[0]
    except:
        return [{"movie_name": "unexpected error has occured saurav"}]
    cv = CountVectorizer()
    vectors = cv.fit_transform(movies_data['tags'])
    similarity = cosine_similarity(vectors)
    distances = similarity[movie_index]
    sorted_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:13]
    movie_list = []
    for i in sorted_movies:
        movie_id = movies_data.iloc[i[0]].id
        movie_list.append(get_details(movie_id))
    return movie_list



def get_names():
    return genres.tolist() + cast.tolist() + directors.tolist()



def get_discovered_movies(input_data):
    indexes = movies_data[movies_data['tags'].str.contains(stem((input_data).lower()))].sort_values(by=['popularity'], ascending=False).head(12).index.values
    if indexes.shape[0] == 0:
        return [{"movie_name": "unexpected error has occured saurav"}]
    movie_list = []
    for i in indexes:
        movie_id = movies_data.iloc[i].id
        movie_list.append(get_details(movie_id))
    return movie_list



def get_default_movies():
    indexes = movies_data.sort_values(by=['popularity'], ascending=False).head(12).index.values    
    if movies_data.shape[0] == 0:
        return [{"movie_name": "unexpected error has occured saurav"}]
    movie_list = []
    for i in indexes:
        movie_id = movies_data.iloc[i].id
        movie_list.append(get_details(movie_id))
    return movie_list