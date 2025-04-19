# 🎬 Personal Movie App

A feature-rich personal movie database you can use via command line **or** a dynamic web interface. Save, update, and explore your favorite movies — powered by API integration and personalized notes.

## 💡 Features

- **User Accounts** with password protection and personalized data storage (CSV or JSON)
- **OMDb API Integration** for automatic movie info retrieval
- **Add Notes**: Add your own comments to each movie
- **Poster Display**: Movies shown with posters and hover-over comments
- **Ratings**: Display movie ratings with star icons ⭐
- **Web Version**: Auto-generated dynamic HTML overview with an individual header, year, 
  poster, rating & note
- **Statistics & Random Movie**: Bonus CLI features
- **Clean OOP Design** 

## 🚀 Quick Start

### 1. Clone this repo:

```bash
git clone https://github.com/yourusername/movie-app.git
cd movie-app
```

### 2. Install requirements:

```bash
pip install flask python-dotenv
```

### 3. Add your OMDb API Key:

Create a `.env` file in the root folder and add:

```env
OMDB_API_KEY=your_api_key_here
```

### 4. Run the command line app:

```bash
python main.py
```

### 5. Run the web app:

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🛠 Technologies Used

- Python 3
- Flask
- OMDb API
- JSON & CSV
- SHA256 for password hashing
- HTML/CSS (Google Fonts, responsive layout)

---

## 📁 Project Structure

```
movie-app/
├── app.py               # Web interface with Flask
├── main.py              # CLI entry point
├── movie_app.py         # Core logic & menu
├── user_manager.py      # User creation/login
├── storage/
│   ├── istorage.py      # Storage interface
│   ├── storage_csv.py
│   └── storage_json.py
├── templates/
│   └── index.html       # HTML template
├── static/
│   └── index.html       # Generated movie overview
├── data/
│   └── users.json       # User accounts
│   └── username.json    # Movie data (per user)
└── .env
```

---

## 📝 Notes

- All data is saved locally and per user.
- Notes are optional and can be updated anytime.
- The CLI and web interface use the same storage files.

---

## ✨ Author

Created by **Martha** for educational purpose during studies at Masterschool– 2025

---

## ✨ License

This project is under MIT Licence. Feel free to contribute or contacting me.
