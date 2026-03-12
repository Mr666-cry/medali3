"""
YTapimusic API - YouTube Music Search Endpoint
Compatible with Vercel Serverless Functions
"""

import json
import os
from urllib.parse import parse_qs
from ytmusicapi import YTMusic

# Initialize YTMusic client
# Using default credentials (no auth required for search)
ytmusic = YTMusic()


def handler(request, response):
    """
    Vercel serverless function handler for /api/search
    
    Query Parameters:
        query: Search query string
        limit: Maximum number of results (default: 20)
    
    Returns:
        JSON response with search results
    """
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight requests
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Parse query parameters
        query_string = request.get('query', {})
        
        # Handle both dict and string query formats
        if isinstance(query_string, str):
            params = parse_qs(query_string)
            query = params.get('query', [''])[0]
            limit = int(params.get('limit', ['20'])[0])
        else:
            query = query_string.get('query', '')
            limit = int(query_string.get('limit', 20))
        
        # Validate query
        if not query or not query.strip():
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Query parameter is required'
                })
            }
        
        # Search using ytmusicapi
        search_results = ytmusic.search(
            query=query.strip(),
            filter='songs',
            limit=limit
        )
        
        # Format results
        formatted_results = []
        for item in search_results:
            if item.get('resultType') in ['song', 'video']:
                # Extract thumbnail (prefer highest quality)
                thumbnails = item.get('thumbnails', [])
                thumbnail = ''
                if thumbnails:
                    # Get the highest resolution thumbnail
                    thumbnail = thumbnails[-1].get('url', '')
                
                # Extract artist name
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
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'query': query,
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


# Vercel serverless function entry point
def main(request, response):
    return handler(request, response)
