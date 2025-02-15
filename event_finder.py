import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import pickle
import os

class EventFinder:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIRECT_URI = redirect_uri
        self.scope = "user-top-read,user-read-private"
        self.auth_manager = SpotifyOAuth(scope=self.scope)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        self.cache_file = 'cache.pkl'

        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                self.cache = pickle.load(f)
        else:
            self.cache = {}

    def __del__(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)

    def get_cached_response(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            return None

    def cache_response(self, url, response):
        self.cache[url] = response

    def get_artist_id(self, artist_name):
        api_key = 'CHFAxfcH8bKAPrXNXM9XO3G69eXivGvX'
        url = f'https://app.ticketmaster.com/discovery/v2/attractions.json?keyword={artist_name}&apikey={api_key}'
        cached_response = self.get_cached_response(url)
        if cached_response:
            return cached_response
        else:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['page']['totalElements'] > 0:
                    self.cache_response(url, data['_embedded']['attractions'][0]['id'])
                    return data['_embedded']['attractions'][0]['id']
        return None

    def get_upcoming_events(self, artist_name, location):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            api_key = 'CHFAxfcH8bKAPrXNXM9XO3G69eXivGvX'
            url = f'https://app.ticketmaster.com/discovery/v2/events.json?attractionId={artist_id}&apikey={api_key}&countryCode={location}&classificationName=music&dmaId=324'
            cached_response = self.get_cached_response(url)
            if cached_response:
                return cached_response
            else:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data['page']['totalElements'] > 0:
                        self.cache_response(url, data['_embedded']['events'])
                        return data['_embedded']['events']
        return None
    
    def get_lowest_prices(self, event_id, num_prices):
        api_key = 'CHFAxfcH8bKAPrXNXM9XO3G69eXivGvX'
        url = f'https://app.ticketmaster.com/commerce/v2/events/{event_id}/offers?apikey={api_key}'
        cached_response = self.get_cached_response(url)
        if cached_response:
            return cached_response
        else:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'offers' in data and data['offers']:
                    prices = [offer['attributes']['total'] for offer in data['offers'] if 'attributes' in offer and 'total' in offer['attributes']]
                    if prices:
                        sorted_prices = sorted(prices)[:num_prices]
                        self.cache_response(url, sorted_prices)
                        return sorted_prices
        return None

    def get_user_top_artists(self, limit, term):
        return self.sp.current_user_top_artists(limit=limit, time_range=term)

    def get_user_country(self):
        user_profile = self.sp.me()
        return user_profile['country']

    def find_events_for_top_artists(self, limit, term):
        top_artists = self.get_user_top_artists(limit=limit, term=term)
        user_country = self.get_user_country()
        top_artist_names = [artist['name'] for artist in top_artists['items']]
        events_info = []
        for i, artist_name in enumerate(top_artist_names):
            artist_events_info = f"Upcoming events for {artist_name}:\n"
            if i != 0:
                artist_events_info = "\n" + artist_events_info
            events = self.get_upcoming_events(artist_name, user_country)
            if events:
                for event in events:
                    venue_name = event['_embedded']['venues'][0]['name']
                    city = event['_embedded']['venues'][0]['city']['name']
                    date = event['dates']['start']['localDate']
                    event_name = event['name']
                    event_url = event['url'] if 'url' in event else "No URL available"
                    event_info = f"- {event_name} at {venue_name}, {city} - {date}\n{event_url}"
                    artist_events_info += event_info + '\n'
            else:
                artist_events_info += "No upcoming events found.\n"
            events_info.append(artist_events_info)
        return events_info


if __name__ == "__main__":
    event_finder = EventFinder(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    event_finder.find_events_for_top_artists()
