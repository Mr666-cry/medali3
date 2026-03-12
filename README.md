# YTapimusic API 🎵

Backend API untuk aplikasi musik berbasis YouTube Music menggunakan Python dan ytmusicapi. Dibuat khusus untuk deployment di Vercel Serverless Functions.

## Fitur

- 🔍 **Search** - Cari lagu, video, dan artis
- 📈 **Trending** - Dapatkan lagu-lagu populer/charts
- 🎵 **Song Details** - Informasi detail tentang lagu tertentu
- 👤 **Artist Info** - Informasi artis dan lagu populer mereka

## API Endpoints

### 1. Search
```
GET /api/search?query={search_query}&limit={limit}
```

**Parameters:**
- `query` (required) - Kata kunci pencarian
- `limit` (optional) - Jumlah maksimal hasil (default: 20)

**Response:**
```json
{
  "status": "success",
  "query": "lagu indonesia",
  "count": 10,
  "data": [
    {
      "videoId": "dQw4w9WgXcQ",
      "title": "Judul Lagu",
      "artist": "Nama Artis",
      "thumbnail": "https://...",
      "duration": "3:45",
      "album": "Nama Album"
    }
  ]
}
```

### 2. Trending/Charts
```
GET /api/trending?country={country_code}&limit={limit}
```

**Parameters:**
- `country` (optional) - Kode negara (default: ID)
- `limit` (optional) - Jumlah maksimal hasil (default: 20)

### 3. Song Details
```
GET /api/song?videoId={video_id}
```

**Parameters:**
- `videoId` (required) - ID video YouTube

### 4. Artist Info
```
GET /api/artist?channelId={channel_id}&limit={limit}
```

**Parameters:**
- `channelId` (required) - ID channel YouTube artis
- `limit` (optional) - Jumlah lagu populer (default: 20)

## Cara Deploy ke Vercel

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login ke Vercel
```bash
vercel login
```

### 3. Deploy
```bash
# Masuk ke folder project
cd ytapimusic

# Deploy ke Vercel
vercel --prod
```

Atau deploy via Git:
1. Push kode ke GitHub/GitLab/Bitbucket
2. Import project di [vercel.com](https://vercel.com)
3. Pilih framework preset: "Other"
4. Deploy!

## Struktur Project

```
ytapimusic/
├── api/
│   ├── search.py      # Endpoint pencarian
│   ├── trending.py    # Endpoint trending/charts
│   ├── song.py        # Endpoint detail lagu
│   └── artist.py      # Endpoint info artis
├── requirements.txt   # Dependencies Python
├── vercel.json       # Konfigurasi Vercel
└── README.md         # Dokumentasi
```

## Dependencies

- `ytmusicapi>=1.5.0` - Library untuk mengakses YouTube Music API
- `requests>=2.31.0` - HTTP library

## Penggunaan di Frontend

Setelah deploy, gunakan URL Vercel Anda di frontend:

```javascript
// Contoh penggunaan
const API_BASE = 'https://your-project.vercel.app';

// Search
const response = await fetch(`${API_BASE}/api/search?query=lagu indonesia`);
const result = await response.json();

if (result.status === 'success') {
    console.log(result.data); // Array of songs
}
```

## Catatan Penting

1. **Rate Limiting**: YouTube Music memiliki batasan request. Jangan spam API.
2. **CORS**: API sudah di-setup dengan CORS headers untuk akses dari domain manapun.
3. **No Authentication**: API ini tidak memerlukan autentikasi YouTube Music.

## Troubleshooting

### Error "Module not found"
Pastikan `requirements.txt` sudah di-push ke repository.

### Error "Function invocation failed"
Cek logs di Vercel Dashboard untuk detail error.

### CORS Error
CORS sudah di-setup di setiap endpoint. Jika masih error, cek browser console.

## License

MIT License - Dibuat oleh SANN404 FORUM
