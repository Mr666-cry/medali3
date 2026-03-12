"""
YTapimusic API - Artist Details Endpoint
Get artist information and top songs
"""

import json
from ytmusicapi import YTMusic

ytmusic = YTMusic()


def handler(request, response):
    """
    GET /api/artist?channelId={channelId}
    
    Query Parameters:
        channelId: YouTube channel ID (required)
        limit: Maximum number of songs (default: 20)
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        query_string = request.get('query', {})
        
        if isinstance(query_string, str):
            from urllib.parse import parse_qs
            params = parse_qs(query_string)
            channel_id = params.get('channelId', [''])[0]
            limit = int(params.get('limit', ['20'])[0])
        else:
            channel_id = query_string.get('channelId', '')
            limit = int(query_string.get('limit', 20))
        
        if not channel_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'channelId parameter is required'
                })
            }
        
        # Get artist details
        artist = ytmusic.get_artist(channel_id)
        
        if not artist:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Artist not found'
                })
            }
        
        # Extract thumbnails
        thumbnails = artist.get('thumbnails', [])
        thumbnail = thumbnails[-1].get('url', '') if thumbnails else ''
        
        # Get top songs if available
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
        
        # Format response
        result = {
            'channelId': channel_id,
            'name': artist.get('name', 'Unknown Artist'),
            'description': artist.get('description', ''),
            'thumbnail': thumbnail,
            'subscribers': artist.get('subscribers', ''),
            'views': artist.get('views', ''),
            'topSongs': top_songs
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'data': result
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'status': 'error',
                'message': str(e)
            })
        }


def main(request, response):
    return handler(request, response)
