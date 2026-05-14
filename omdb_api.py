import requests
import random
from config import OMDB_API_KEY

BASE_URL = "http://www.omdbapi.com/"

def get_random_movie(year: str, genre: str):
    try:
        params = {
            "apikey": OMDB_API_KEY,
            "s": genre,
            "y": year,
            "type": "movie"
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

    except requests.exceptions.Timeout:
        print("Ошибка: превышено время ожидания API")
        return None

    except requests.exceptions.ConnectionError:
        print("Ошибка: нет соединения с API")
        return None
        
    if data.get("Response") == "False":
        return None

    movies = data.get("Search", [])
    if not movies:
        return None

    movie = random.choice(movies)

    # Получаем подробную информацию
    movie_id = movie.get("imdbID")
    details_params = {
        "apikey": OMDB_API_KEY,
        "i": movie_id
    }

    details_response = requests.get(BASE_URL, params=details_params)
    return details_response.json()