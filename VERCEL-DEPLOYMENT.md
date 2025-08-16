# 🚀 Deploy ke Vercel - Python + HTML Biasa

## 📋 **Permintaan Guru:**
> "4. Deploy di Vercel untuk pythonnya (Python + HTML biasa)"

## ✨ **Yang Akan Deploy:**
- ✅ **Python Flask** - Backend sederhana
- ✅ **HTML Templates** - Frontend biasa
- ✅ **Database SQLite** - Data storage
- ✅ **User Authentication** - Login/Register
- ✅ **Room Management** - Buat dan join room
- ❌ **TANPA WebSocket** - Tidak ada real-time multiplayer

## 🛠️ **File yang Dibutuhkan:**

1. **`vercel.json`** - Konfigurasi Vercel
2. **`api/index.py`** - Flask app entry point
3. **`requirements.txt`** - Python dependencies
4. **`templates/`** - HTML files
5. **`static/`** - CSS, JS, images

## 🚀 **Langkah Deployment:**

### **Step 1: Push ke GitHub**
```bash
git add .
git commit -m "Prepare for Vercel deployment - Python + HTML"
git push origin main
```

### **Step 2: Deploy di Vercel Dashboard**

1. **Buka [vercel.com](https://vercel.com)**
2. **Login/Register**
3. **Klik "New Project"**
4. **Import dari GitHub** - pilih repository Anda
5. **Konfigurasi:**
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (kosong)
   - **Build Command**: Kosong
   - **Output Directory**: Kosong
   - **Install Command**: `pip install -r requirements.txt`
6. **Klik "Deploy"**

### **Step 3: Set Environment Variables**
Setelah deploy, di Vercel dashboard:
- **Settings** → **Environment Variables**
- Tambahkan: `FLASK_SECRET_KEY` = `your_secret_key`

## 🎯 **Fitur yang Tersedia:**

### **✅ Bisa:**
- Landing page
- User registration & login
- Dashboard dengan daftar room
- Buat room baru
- Join room
- Basic game interface

### **❌ Tidak Bisa:**
- Real-time multiplayer
- WebSocket updates
- Live game state sync

## 🔧 **Struktur Aplikasi:**

```
Socket-Game/
├── api/
│   └── index.py          ← Flask app (entry point)
├── templates/             ← HTML templates
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── game.html
├── static/                ← CSS & JS
├── requirements.txt       ← Python dependencies
└── vercel.json           ← Vercel config
```

## 📱 **Testing Setelah Deploy:**

1. **Landing Page** - `/` ✅
2. **Register** - `/register` ✅
3. **Login** - `/login` ✅
4. **Dashboard** - `/dashboard` ✅
5. **Create Room** - Form di dashboard ✅
6. **Game Page** - `/game/<room_id>` ✅

## 🆘 **Troubleshooting:**

### **Build Failed:**
- Check `requirements.txt` - pastikan dependencies benar
- Pastikan `api/index.py` ada dan benar

### **Template Not Found:**
- Pastikan folder `templates/` ada
- Pastikan path di `render_template()` benar

### **Database Error:**
- SQLite akan dibuat otomatis
- Check logs di Vercel dashboard

## 🎮 **Cara Kerja Game:**

1. **User register/login**
2. **Buat room** dari dashboard
3. **Join room** yang sudah ada
4. **Game interface** tampil (tanpa real-time)
5. **Game state** disimpan di database

## 🌐 **URL Setelah Deploy:**

App akan tersedia di:
`https://your-project-name.vercel.app`

---

**✅ Sesuai Permintaan Guru: Python + HTML Biasa di Vercel!**
