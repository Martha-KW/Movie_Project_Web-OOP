import requests
import os
from dotenv import load_dotenv
from utils import safe_str, safe_float

load_dotenv()  # Loads the .env file that protects the api key

class OmdbClient:
    def __init__(self):
        self.api_key = os.getenv("OMDB_API_KEY")
        self.base_url = "http://www.omdbapi.com/"

    def fetch_movie(self, title):
        params = {
            "apikey": self.api_key,
            "t": title
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "False":
                print(f"Movie '{title}' not found in OMDb.")
                return None

            year_raw = data.get("Year", "")
            try:
                year = int(year_raw[:4]) if year_raw and year_raw[:4].isdigit() else None
            except ValueError:
                year = None

            return {
                "title": safe_str(data.get("Title")),
                "year": year,
                "rating": safe_float(data.get("imdbRating")),
                "poster": safe_str(data.get("Poster"))
            }
        except requests.exceptions.ConnectionError:
            print("🌐 Could not connect to OMDb API. Please check your internet connection.")
        except requests.exceptions.HTTPError:
            print("🚨 There was a problem with the OMDb server response.")
        except requests.RequestException:
            print("⚠️ An unexpected error occurred while trying to fetch the movie data.")

        return None
