import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = '' #kendi apı numaran steam apı bölümünden alınabilir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games', methods=['POST'])
def get_games():
    category = request.form['category']
    url = f'https://api.rawg.io/api/games?key={API_KEY}&genres={category}'
    
    response = requests.get(url)
    games = response.json().get('results', [])

    # Eğer resim yoksa varsayılan bir görsel ayarla
    for game in games:
        if not game.get('background_image'):
            game['background_image'] = 'https://via.placeholder.com/100'  # Varsayılan görsel URL'si

    # Kategoriyi template'e gönderiyoruz
    return render_template('games.html', games=games, category=category)


if __name__ == '__main__':
    app.run(debug=True, port=7070)
