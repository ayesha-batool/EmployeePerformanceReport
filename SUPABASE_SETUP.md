# Supabase Setup Guide

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

## 2. Run Database Schema

1. Open Supabase Dashboard → SQL Editor
2. Copy and paste the contents of `supabase_schema.sql`
3. Click "Run" to execute the schema
4. Verify tables are created in the Table Editor

## 3. Configure Environment Variables

✅ **Already configured!** The `.env` file has been created with your Supabase credentials:
- URL: `https://nlrzxohdrohmxmegmvtl.supabase.co`
- Anon Key: Configured

The application will automatically load these credentials when it starts.

**Note:** If you need to change them, edit the `.env` file in the project root.

Or set them in your system (alternative method):

```bash
# Windows PowerShell
$env:SUPABASE_URL="https://your-project-id.supabase.co"
$env:SUPABASE_ANON_KEY="your-anon-key-here"

# Linux/Mac
export SUPABASE_URL="https://your-project-id.supabase.co"
export SUPABASE_ANON_KEY="your-anon-key-here"
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the Application

```bash
python -m streamlit run app.py
```

## Database Schema

The schema includes:
- `employees` - Employee information
- `projects` - Project management
- `tasks` - Task assignments
- `performances` - Performance evaluations
- `performance_goals` - Goals tracking
- `peer_feedback` - Feedback system
- `performance_reviews` - Reviews
- `skill_assessments` - Skills
- `performance_metrics` - Metrics
- `notifications` - Notifications

All tables use UUID primary keys and have proper indexes for performance.

## Row Level Security (RLS)

The schema includes RLS policies that allow all operations for development. For production, you should customize these policies based on your security requirements.

