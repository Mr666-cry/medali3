"""
YTapimusic API - Root Endpoint
Returns API information and available endpoints
"""

import json


def handler(request, response):
    """
    GET /
    Returns API documentation
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
    
    api_info = {
        "name": "YTapimusic API",
        "version": "1.0.0",
        "description": "YouTube Music API untuk aplikasi musik",
        "author": "SANN404 FORUM",
        "endpoints": {
            "/api/search": {
                "method": "GET",
                "description": "Cari lagu, video, dan artis",
                "parameters": {
                    "query": "string (required) - Kata kunci pencarian",
                    "limit": "integer (optional) - Jumlah maksimal hasil (default: 20)"
                },
                "example": "/api/search?query=lagu%20indonesia&limit=10"
            },
            "/api/trending": {
                "method": "GET",
                "description": "Dapatkan lagu-lagu trending/charts",
                "parameters": {
                    "country": "string (optional) - Kode negara (default: ID)",
                    "limit": "integer (optional) - Jumlah maksimal hasil (default: 20)"
                },
                "example": "/api/trending?country=ID&limit=10"
            },
            "/api/song": {
                "method": "GET",
                "description": "Dapatkan detail lagu tertentu",
                "parameters": {
                    "videoId": "string (required) - ID video YouTube"
                },
                "example": "/api/song?videoId=dQw4w9WgXcQ"
            },
            "/api/artist": {
                "method": "GET",
                "description": "Dapatkan info artis dan lagu populer",
                "parameters": {
                    "channelId": "string (required) - ID channel YouTube artis",
                    "limit": "integer (optional) - Jumlah lagu populer (default: 20)"
                },
                "example": "/api/artist?channelId=UC..."
            }
        },
        "status": "running"
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(api_info, indent=2)
    }


def main(request, response):
    return handler(request, response)
