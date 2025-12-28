from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

# URL безкоштовного API для ігор
FREETOGAME_API = "https://www.freetogame.com/api/games"

# Головна сторінка сайту
@app.route('/')
def index():
    # Отримати популярні ігри для відображення
    response = requests.get(FREETOGAME_API, params={'sort-by': 'popularity'})
    popular_games = []
    if response.status_code == 200:
        popular_games = response.json()[:6]  # Топ 6 популярних
    return render_template('index.html', popular_games=popular_games)

# Маршрути для категорій
@app.route('/category/<category>')
def category(category):
    return redirect(url_for('search', category=category))

# Пошук ігор (для фронтенду)
@app.route('/search')
def search():
    query = request.args.get('q', '')  # Параметр пошуку
    platform = request.args.get('platform', '')  # Фільтр за платформою (pc, browser тощо)
    category = request.args.get('category', '')  # Фільтр за категорією
    sort_by = request.args.get('sort', '')  # Сортування
    
    url = FREETOGAME_API
    params = {}
    if platform:
        params['platform'] = platform
    if category:
        params['category'] = category
    if sort_by:
        params['sort-by'] = sort_by
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        games = response.json()
        if query:
            # Фільтруємо за назвою локально
            games = [game for game in games if query.lower() in game['title'].lower()]
        return render_template('results.html', games=games[:50])  # Обмежуємо до 50 для швидкості
    
    return "Помилка завантаження даних", 500

# Власне API сайту (повертає JSON)
@app.route('/api/games')
def api_games():
    platform = request.args.get('platform', '')
    category = request.args.get('category', '')  # Наприклад, mmorpg, shooter
    
    url = FREETOGAME_API
    params = {}
    if platform:
        params['platform'] = platform
    if category:
        params['category'] = category
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    
    return jsonify({"error": "Не вдалося отримати дані"}), 500

if __name__ == '__main__':
    app.run(debug=True)