from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
from ytmusicapi import YTMusic

# Initialize YTMusic
ytmusic = YTMusic()

class handler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        # Convert query params from list to single values
        params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        
        try:
            if path == '/' or path == '/api':
                response = self.get_api_info()
            elif path == '/api/search':
                response = self.search(params)
            elif path == '/api/trending':
                response = self.trending(params)
            elif path == '/api/song':
                response = self.song_detail(params)
            elif path == '/api/artist':
                response = self.artist_info(params)
            else:
                response = {'status': 'error', 'message': 'Not found'}, 404
                
        except Exception as e:
            response = {'status': 'error', 'message': str(e)}, 500
        
        # Send response
        if isinstance(response, tuple):
            data, status_code = response
        else:
            data, status_code = response, 200
            
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def get_api_info(self):
        return {
            "name": "YTapimusic API",
            "version": "1.0.0",
            "description": "YouTube Music API untuk aplikasi musik",
            "author": "SANN404 FORUM",
            "endpoints": {
                "/api/search": "Cari lagu (query param: ?query=lagu&limit=20)",
                "/api/trending": "Trending songs (query param: ?country=ID&limit=20)",
                "/api/song": "Detail lagu (query param: ?videoId=xxx)",
                "/api/artist": "Info artis (query param: ?channelId=xxx)"
            },
            "status": "running"
        }
    
    def search(self, params):
        query = params.get('query', '')
        limit = int(params.get('limit', 20))
        
        if not query or not query.strip():
            return {'status': 'error', 'message': 'Query parameter is required'}, 400
        
        search_results = ytmusic.search(
            query=query.strip(),
            filter='songs',
            limit=limit
        )
        
        formatted_results = []
        for item in search_results:
            if item.get('resultType') in ['song', 'video']:
                thumbnails = item.get('thumbnails', [])
                thumbnail = thumbnails[-1].get('url', '') if thumbnails else ''
                
                artists = item.get('artists', [])
                artist_name = artists[0].get('name', 'Unknown Artist') if artists else 'Unknown Artist'
                
                formatted_results.append({
                    'videoId': item.get('videoId', ''),
                    'title': item.get('title', 'Unknown Title'),
                    'artist': artist_name,
                    'thumbnail': thumbnail,
                    'duration': item.get('duration', ''),
                    'album': item.get('album', {}).get('name', '') if item.get('album') else ''
                })
        
        return {
            'status': 'success',
            'query': query,
            'count': len(formatted_results),
            'data': formatted_results
        }
    
    def trending(self, params):
        country = params.get('country', 'ID')
        limit = int(params.get('limit', 20))
        
        charts = ytmusic.get_charts(country=country)
        
        formatted_results = []
        if 'songs' in charts and 'items' in charts['songs']:
            items = charts['songs']['items'][:limit]
            for item in items:
                thumbnails = item.get('thumbnails', [])
                thumbnail = thumbnails[-1].get('url', '') if thumbnails else ''
                
                artists = item.get('artists', [])
                artist_name = artists[0].get('name', 'Unknown Artist') if artists else 'Unknown Artist'
                
                formatted_results.append({
                    'videoId': item.get('videoId', ''),
                    'title': item.get('title', 'Unknown Title'),
                    'artist': artist_name,
                    'thumbnail': thumbnail,
                    'duration': item.get('duration', ''),
                    'rank': item.get('rank', ''),
                    'trend': item.get('trend', '')
                })
        
        return {
            'status': 'success',
            'country': country,
            'count': len(formatted_results),
            'data': formatted_results
        }
    
    def song_detail(self, params):
        video_id = params.get('videoId', '')
        
        if not video_id:
            return {'status': 'error', 'message': 'videoId parameter is required'}, 400
        
        song_info = ytmusic.get_song(video_id)
        
        if not song_info or 'videoDetails' not in song_info:
            return {'status': 'error', 'message': 'Song not found'}, 404
        
        video_details = song_info.get('videoDetails', {})
        thumbnails = video_details.get('thumbnail', {}).get('thumbnails', [])
        thumbnail = thumbnails[-1].get('url', '') if thumbnails else ''
        
        return {
            'status': 'success',
            'data': {
                'videoId': video_id,
                'title': video_details.get('title', 'Unknown Title'),
                'artist': video_details.get('author', 'Unknown Artist'),
                'thumbnail': thumbnail,
                'duration': video_details.get('lengthSeconds', ''),
                'keywords': video_details.get('keywords', []),
                'viewCount': video_details.get('viewCount', ''),
                'channelId': video_details.get('channelId', '')
            }
        }
    
    def artist_info(self, params):
        channel_id = params.get('channelId', '')
        limit = int(params.get('limit', 20))
        
        if not channel_id:
            return {'status': 'error', 'message': 'channelId parameter is required'}, 400
        
        artist = ytmusic.get_artist(channel_id)
        
        if not artist:
            return {'status': 'error', 'message': 'Artist not found'}, 404
        
        thumbnails = artist.get('thumbnails', [])
        thumbnail = thumbnails[-1].get('url', '') if thumbnails else ''
        
        top_songs = []
        if 'songs' in artist and 'results' in artist['songs']:
            songs = artist['songs']['results'][:limit]
            for song in songs:
                song_thumbnails = song.get('thumbnails', [])
                song_thumbnail = song_thumbnails[-1].get('url', '') if song_thumbnails else ''
                
                top_songs.append({
                    'videoId': song.get('videoId', ''),
                    'title': song.get('title', 'Unknown Title'),
                    'thumbnail': song_thumbnail,
                    'duration': song.get('duration', '')
                })
        
        return {
            'status': 'success',
            'data': {
                'channelId': channel_id,
                'name': artist.get('name', 'Unknown Artist'),
                'description': artist.get('description', ''),
                'thumbnail': thumbnail,
                'subscribers': artist.get('subscribers', ''),
                'views': artist.get('views', ''),
                'topSongs': top_songs
            }
        }
s.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Vercel handler
if __name__ == '__main__':
    app.run(debug=True)
