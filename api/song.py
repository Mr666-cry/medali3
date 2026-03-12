"""
YTapimusic API - Song Details Endpoint
Get detailed information about a specific song
"""

import json
from ytmusicapi import YTMusic

ytmusic = YTMusic()


def handler(request, response):
    """
    GET /api/song?videoId={videoId}
    
    Query Parameters:
        videoId: YouTube video ID (required)
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
            video_id = params.get('videoId', [''])[0]
        else:
            video_id = query_string.get('videoId', '')
        
        if not video_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'videoId parameter is required'
                })
            }
        
        # Get song details
        song_info = ytmusic.get_song(video_id)
        
        if not song_info or 'videoDetails' not in song_info:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Song not found'
                })
            }
        
        video_details = song_info.get('videoDetails', {})
        
        # Extract thumbnails
        thumbnails = video_details.get('thumbnail', {}).get('thumbnails', [])
        thumbnail = thumbnails[-1].get('url', '') if thumbnails else ''
        
        # Format response
        result = {
            'videoId': video_id,
            'title': video_details.get('title', 'Unknown Title'),
            'artist': video_details.get('author', 'Unknown Artist'),
            'thumbnail': thumbnail,
            'duration': video_details.get('lengthSeconds', ''),
            'keywords': video_details.get('keywords', []),
            'viewCount': video_details.get('viewCount', ''),
            'channelId': video_details.get('channelId', '')
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
