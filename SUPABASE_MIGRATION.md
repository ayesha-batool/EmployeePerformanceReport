# Supabase Migration Guide

## What Changed

### ✅ Removed
- Local JSON file storage (`data/*.json`)
- API client fallback mechanism
- Complex hybrid data manager logic

### ✅ Added
- Direct Supabase PostgreSQL integration
- Simple Supabase client wrapper
- Clean database schema with proper relationships

## Architecture

```
Streamlit Frontend (app.py)
    ↓
HybridDataManager (simplified)
    ↓
SupabaseClient
    ↓
Supabase PostgreSQL Database
```

## Setup Steps

1. **Create Supabase Project**
   - Go to supabase.com
   - Create new project
   - Get URL and anon key

2. **Run Schema**
   - Copy `supabase_schema.sql`
   - Paste in Supabase SQL Editor
   - Execute

3. **Set Environment Variables**
   ```bash
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   ```

4. **Run Application**
   ```bash
   python -m streamlit run app.py
   ```

## Data Flow

### Creating Data
```python
# Frontend
data_manager.create_task({...})
    ↓
# HybridDataManager
supabase_client.create_task(data)
    ↓
# SupabaseClient
client.table("tasks").insert(data).execute()
    ↓
# Supabase Database
INSERT INTO tasks ...
```

### Reading Data
```python
# Frontend
data_manager.load_data("tasks")
    ↓
# HybridDataManager
supabase_client.get_tasks()
    ↓
# SupabaseClient
client.table("tasks").select("*").execute()
    ↓
# Returns data from PostgreSQL
```

## Benefits

1. **No Local Files**: All data in cloud database
2. **Real-time**: Supabase supports real-time subscriptions
3. **Scalable**: PostgreSQL handles large datasets
4. **Secure**: Row Level Security (RLS) policies
5. **Simple**: Direct database access, no API layer needed

## Notes

- All IDs are UUIDs (not integers)
- Foreign keys use UUID references
- JSONB fields for flexible data (skills, etc.)
- Timestamps are automatically managed

