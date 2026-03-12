# YTapimusic API 🎵

Backend API YouTube Music untuk aplikasi musik. Siap deploy ke Vercel!

## 📁 Struktur Project

```
ytapimusic/
├── api/
│   ├── index.py      # Handler utama + API info
│   ├── search.py     # Endpoint /api/search
│   ├── trending.py   # Endpoint /api/trending
│   ├── song.py       # Endpoint /api/song
│   └── artist.py     # Endpoint /api/artist
├── requirements.txt  # WAJIB ADA!
└── vercel.json       # Konfigurasi routing
```

## 🚀 Deploy ke Vercel

### Cara 1: Deploy via GitHub (Recommended)

1. **Push ke GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/username/ytapimusic.git
   git push -u origin main
   ```

2. **Import di Vercel**
   - Buka [vercel.com](https://vercel.com)
   - Klik "Add New Project"
   - Import dari GitHub
   - Framework Preset: **Other**
   - Klik Deploy

### Cara 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd ytapimusic
vercel --prod
```

## ⚠️ PENTING!

1. **`requirements.txt` WAJIB ADA** - Vercel butuh ini untuk install `ytmusicapi`
2. **Jangan hapus folder `api/`** - Semua endpoint harus di folder ini
3. **Format handler** - Menggunakan `class handler(BaseHTTPRequestHandler)`

## 📡 API Endpoints

| Endpoint | Method | Parameter | Contoh |
|----------|--------|-----------|--------|
| `/` | GET | - | Info API |
| `/api/search` | GET | `query`, `limit` | `/api/search?query=lagu%20indonesia&limit=10` |
| `/api/trending` | GET | `country`, `limit` | `/api/trending?country=ID&limit=10` |
| `/api/song` | GET | `videoId` | `/api/song?videoId=dQw4w9WgXcQ` |
| `/api/artist` | GET | `channelId`, `limit` | `/api/artist?channelId=UC...` |

## 🔌 Integrasi Frontend

Update URL API di `index.html`:

```javascript
const API_BASE = 'https://your-project.vercel.app';

// Search
const response = await fetch(`${API_BASE}/api/search?query=lagu%20indonesia`);
const result = await response.json();
```

## 📋 Response Format

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
      "duration": "3:45"
    }
  ]
}
```

## 🔧 Troubleshooting

### Error "Module not found"
- Pastikan `requirements.txt` ada di root folder
- Isi: `ytmusicapi==1.7.0`

### Error "Handler not found"
- Pastikan semua file di `api/` punya `class handler`
- Jangan ubah nama class `handler`

### Error 404
- Cek `vercel.json` routing
- Pastikan path benar

## 📦 Dependencies

- `ytmusicapi==1.7.0` - YouTube Music API

## 📝 License

MIT - SANN404 FORUM
