import requests
import pandas as pd

class Genius:
    """
    A class to interact with the Genius API for retrieving artist information.
    """

    def __init__(self, access_token: str):
        """
        Initialize the Genius class with an access token.
        """
        self.access_token = access_token

    def get_artist(self, search_term: str) -> dict:
        """
        Retrieve artist information from Genius API using a search term.
        """
        search_url = "https://api.genius.com/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"q": search_term}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        json_data = response.json()

        hits = json_data.get("response", {}).get("hits", [])
        if not hits:
            raise ValueError(f"No results found for '{search_term}'.")

        artist_id = hits[0]["result"]["primary_artist"]["id"]

        artist_url = f"https://api.genius.com/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=headers)
        artist_response.raise_for_status()
        artist_data = artist_response.json()

        return artist_data
        
        def get_artists(self, search_terms: list) -> pd.DataFrame:
        """
        Retrieve artist information for a list of search terms and return as a DataFrame.
        """
        data = []

        for term in search_terms:
            try:
                artist_data = self.get_artist(term)
                artist_info = artist_data.get("response", {}).get("artist", {})

                data.append({
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count", None)
                })
            except Exception:
                data.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(data)


