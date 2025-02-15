# Spotivents 🎵📅

Spotivents is a Python-based desktop application that helps users discover upcoming events for their favorite artists on Spotify. The application retrieves top artists from a user's Spotify listening history and finds corresponding events, displaying clickable links for event details.

## Features 🚀
- **Find Events for Your Favorite Artists** 🎤🎫  
  - Uses Spotify's API to fetch top artists from your listening history.
  - Retrieves event information for these artists.
  
- **Customizable Search** 🔄  
  - Adjust the **time range** for top artists (short, medium, or long-term).
  - Change the **number of artists** (Top 5, 10, or 25).

- **Clickable Event Links** 🌍  
  - Click on event links in the output window to open event details in your browser.

- **Dark Themed GUI** 🌑  
  - Uses `tkinter` and `sv_ttk` for a modern dark-themed interface.

## Installation 📝
### Prerequisites
Ensure you have **Python 3.7+** installed. You also need the following dependencies:

```sh
pip install tkinter sv_ttk spotipy
```

### Clone the Repository
```sh
git clone https://github.com/your-username/spotivents.git
cd spotivents
```

### Environment Setup
Create a virtual environment (recommended):
```sh
python -m venv spotipy-env
source spotipy-env/bin/activate  # On Mac/Linux
spotipy-env\Scripts\activate  # On Windows
```

## Usage 🎯
1. **Run the program**  
   ```sh
   python app_view.py
   ```
2. Click **"Start"** to fetch events.
3. Use **"Change Term"** to cycle through time periods (Short, Medium, Long-term).
4. Use **"Change Limit"** to select the number of top artists.
5. Click on event links to view details in your web browser.

## Configuration ⚙️
Edit the following credentials in `app_view.py` to match your **Spotify API credentials**:

```python
client_id = 'your_spotify_client_id'
client_secret = 'your_spotify_client_secret'
redirect_uri = 'https://localhost:8888/callback'
```

To obtain API credentials, visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

## Troubleshooting 🔧
- **Invalid Redirect URI?**  
  - Ensure the redirect URI in `app_view.py` matches the one in your Spotify developer settings.
  
- **Events Not Showing?**  
  - The `EventFinder` class may need adjustments based on your event data source.

## License 📝
This project is licensed under the MIT License.

---

🎵 **Enjoy discovering live events for your favorite artists with Spotivents!** 🎫