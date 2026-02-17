# AI-Based Social Media Post & Creative Generator (Django)

Backend-powered Python tool that accepts business details, generates structured social media content with Gemini, stores outputs in SQLite, and renders a premium UI.

## Tech Stack
- Python
- Django
- Gemini API (`google-genai`)
- SQLite

## Setup
1. Create and activate virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `.env`:
   ```env
   DEBUG=True
   SECRET_KEY=replace-with-a-secure-secret-key
   ALLOWED_HOSTS=127.0.0.1,localhost
   CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost

   GEMINI_API_KEY=replace-with-your-gemini-api-key
   GEMINI_MODEL=gemini-2.0-flash-lite
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```
6. Open `http://127.0.0.1:8000/`


## Loom Demo

<div style="position: relative; padding-bottom: 41.875%; height: 0;"><iframe src="https://www.loom.com/embed/fed2f6bde020414ab7dcd90425564b84" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>