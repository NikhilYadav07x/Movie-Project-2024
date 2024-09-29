import pickle
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Load movie data and similarity model
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Flask Route to serve index.html
@app.route('/')
def home():
    return render_template('index.html')

# Flask Route to handle movie recommendations
@app.route('/recommend')
def recommendation_page():
    # Get the movie from the search query parameter
    searched_movie = request.args.get('movie')
    
    if searched_movie and searched_movie in movies['title'].values:
        # Get movie recommendations
        recommended_movie_names, recommended_movie_posters = recommend(searched_movie)
        
        # Return an HTML page with the recommended movies
        return render_template('recommend.html', movie=searched_movie, recommendations=zip(recommended_movie_names, recommended_movie_posters))
    else:
        # Return an error page if the movie is not found
        return f"No movie found with the name '{searched_movie}'"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
