from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "" # apı key kısmı ımbd apı alma yada ombd apı alma kısmından alınabilir

# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']  
    recommended_movies = get_recommended_movies(genre)

    return render_template('recommend.html', movies=recommended_movies)

def get_recommended_movies(genre):
    url = f"http://www.omdbapi.com/?s={genre}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('Response') == 'False':
        return [] 
    
    movies = []
    for movie in data.get('Search', []):
        movies.append({
            'Title': movie['Title'],
            'Poster': movie['Poster'],
            'Link': f"https://www.imdb.com/title/{movie['imdbID']}/"
        })
    return movies

if __name__ == '__main__':
    app.run(debug=True, port=9090)
