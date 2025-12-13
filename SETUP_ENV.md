# Environment Setup

## Create .env File

Create a `.env` file in the project root with your Supabase credentials:

```bash
SUPABASE_URL=https://nlrzxohdrohmxmegmvtl.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5scnp4b2hkcm9obXhtZWdtdnRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE0NzgzNjQsImV4cCI6MjA3NzA1NDM2NH0._ZKqwN2i7werUHzpmvq0q8Qk528_lrzywewtiegKCAU
```

## Steps

1. **Create `.env` file** in the project root directory
2. **Add the credentials** above
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run the schema**: Copy `supabase_schema.sql` to Supabase SQL Editor and execute
5. **Run the app**: `python -m streamlit run app.py`

## Verify Setup

The app will automatically load the `.env` file when it starts. If credentials are missing, you'll see an error message with instructions.

