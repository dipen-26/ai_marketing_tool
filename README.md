# AI-Based Social Media Post & Creative Generator (Django)

Backend-powered Python tool that accepts business details, generates structured social media content with Gemini, stores outputs in SQLite, and renders a premium UI.

## Features
- Input form with required fields:
  - Business Name
  - Industry
  - Target Audience
  - Location
  - Business Goal (`Leads`, `Branding`, `Sales`, `Engagement`)
  - Tone (`Professional`, `Friendly`, `Bold`, `Educational`)
  - Number of Posts (default `5`, range `1-10`)
- AI generation for each post:
  - Post Topic
  - Platform-neutral Caption
  - Instagram Version
  - LinkedIn Version
  - Facebook Version
  - Hashtags
  - CTA
  - Image Prompt (structured only; no actual image generation required)
  - Creative Type (`Carousel` / `Reel` / `Static Post`)
  - Text Overlay Suggestion
  - Color Theme Suggestion
- Database storage with `Project` and `GeneratedPost` tables
- Results page with structured output cards
- Bonus:
  - Export generated project posts as `.txt`
  - Basic scheduling (`publish_at` auto-staggered per post)
  - Temperature control input

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

## Export
From results page click **Export as TXT** to download `project_<id>_posts.txt`.

## Notes
- The app is configured for Gemini-only generation in runtime logic.
- If the AI call fails (except quota/rate-limit), a structured fallback generator is used to keep flow working.

## Loom Demo
Record a 5-7 minute demo showing:
1. Form input submission
2. AI-generated output cards
3. Database entries in Django admin
4. TXT export flow
