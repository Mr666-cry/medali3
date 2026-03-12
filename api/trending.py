"""
YTapimusic API - Trending/Popular Songs Endpoint
Returns trending songs from YouTube Music
"""

import json
from ytmusicapi import YTMusic

ytmusic = YTMusic()


def handler(request, response):
    """
    GET /api/trending
    
    Query Parameters:
        country: Country code (default: 'ID' for Indonesia)
        limit: Maximum number of results (default: 20)
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
            country = params.get('country', ['ID'])[0]
            limit = int(params.get('limit', ['20'])[0])
        else:
            country = query_string.get('country', 'ID')
            limit = int(query_string.get('limit', 20))
        
        # Get charts for the country
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
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'country': country,
                'count': len(formatted_results),
                'data': formatted_results
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
