# API Integration Guide

## Overview

The project now supports **unified data access** through the FastAPI backend. The Streamlit frontend can use either:
1. **API Backend** (SQLite database) - Recommended for production
2. **JSON Files** - Fallback for local development

## Architecture

### Components

1. **FastAPI Backend** (`api/`)
   - RESTful API endpoints
   - SQLite database storage
   - JWT authentication (optional for local dev)

2. **API Client** (`components/managers/api_client.py`)
   - Synchronous HTTP client
   - Handles all API requests

3. **Hybrid Data Manager** (`components/managers/hybrid_data_manager.py`)
   - Uses API when available
   - Falls back to JSON files
   - Drop-in replacement for DataManager

4. **API Data Manager** (`components/managers/api_data_manager.py`)
   - Pure API-backed data manager
   - Implements same interface as DataManager

## API Endpoints

### New Endpoints Added

- **Employees**: `/api/v1/employees` (GET, POST, PUT, DELETE)
- **Tasks**: `/api/v1/tasks` (GET, POST, PUT, DELETE)
- **Projects**: `/api/v1/projects` (GET, POST, PUT, DELETE)
- **Performances**: `/api/v1/performances` (GET, POST)
- **Notifications**: `/api/v1/notifications` (GET, POST, PUT)

### Existing Endpoints

- **Reviews**: `/api/v1/reviews`
- **Goals**: `/api/v1/goals`
- **Feedback**: `/api/v1/feedback`
- **Skills**: `/api/v1/skills`
- **Analytics**: `/api/v1/analytics`
- **Reports**: `/api/v1/reports`

## How to Use

### 1. Start the API Server

```bash
python start_api.py
```

Or manually:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8003 --reload
```

The API will be available at:
- Base URL: `http://localhost:8003`
- Documentation: `http://localhost:8003/docs`
- Health Check: `http://localhost:8003/health`

### 2. Enable API Integration in Streamlit

Set environment variable before running Streamlit:

**Windows PowerShell:**
```powershell
$env:USE_API="true"
python -m streamlit run app.py
```

**Linux/Mac:**
```bash
export USE_API=true
python -m streamlit run app.py
```

**Or set in code:**
```python
import os
os.environ["USE_API"] = "true"
```

### 3. Authentication

For local development, authentication is bypassed by default. The API accepts requests without JWT tokens when `ALLOW_LOCAL_AUTH_BYPASS=true` (default).

For production, set:
```bash
ALLOW_LOCAL_AUTH_BYPASS=false
ATLAS_JWT_SECRET=your-secret-key
```

## Data Flow

### With API Enabled

```
Streamlit App
    ↓
HybridDataManager
    ↓
SyncAPIClient
    ↓
FastAPI Backend
    ↓
SQLite Database
```

### Without API (Fallback)

```
Streamlit App
    ↓
HybridDataManager
    ↓
DataManager (JSON files)
    ↓
data/*.json files
```

## Migration from JSON to API

The system automatically:
1. Tries to load from API first
2. Falls back to JSON if API unavailable
3. Saves to both API and JSON (when API enabled)

This ensures:
- **Backward compatibility**: Existing JSON data still works
- **Gradual migration**: No data loss during transition
- **Resilience**: System works even if API is down

## Database Schema

### New Tables

- `employees` - Employee information
- `tasks` - Task assignments
- `projects` - Project management
- `performances` - Performance evaluations
- `notifications` - User notifications

### Existing Tables

- `performance_reviews` - Performance reviews
- `performance_goals` - Goals
- `peer_feedback` - Feedback
- `skill_assessments` - Skills
- `performance_metrics` - Metrics

## Configuration

### Environment Variables

```bash
# Enable API integration
USE_API=true

# API server URL
API_BASE_URL=http://localhost:8003

# API authentication token (optional for local)
API_TOKEN=local

# Allow bypassing auth for local dev
ALLOW_LOCAL_AUTH_BYPASS=true

# JWT secret for production
ATLAS_JWT_SECRET=your-secret-key
```

## Benefits

1. **Unified Data Access**: Single source of truth
2. **Scalability**: SQLite can be replaced with PostgreSQL/MySQL
3. **API-First**: Ready for external integrations (Atlas, etc.)
4. **Backward Compatible**: JSON files still work
5. **Resilient**: Falls back gracefully if API unavailable

## Testing

### Test API Endpoints

```bash
# Health check
curl http://localhost:8003/health

# Get employees
curl http://localhost:8003/api/v1/employees

# Get tasks
curl http://localhost:8003/api/v1/tasks
```

### Test from Streamlit

1. Start API server
2. Set `USE_API=true`
3. Run Streamlit app
4. Check browser console for API calls
5. Verify data loads from API

## Troubleshooting

### API Not Connecting

1. Check if API server is running: `curl http://localhost:8003/health`
2. Verify `USE_API=true` is set
3. Check `API_BASE_URL` matches server URL
4. Check firewall/port settings

### Data Not Syncing

1. API saves to database, JSON saves to files
2. Both are saved when API is enabled
3. Check database: `sqlite3 performance.db`
4. Check JSON files in `data/` directory

### Authentication Errors

1. For local dev, set `ALLOW_LOCAL_AUTH_BYPASS=true`
2. For production, provide valid JWT token
3. Check `ATLAS_JWT_SECRET` matches

## Next Steps

1. **Data Migration**: Migrate existing JSON data to database
2. **Production Setup**: Configure proper authentication
3. **Database Upgrade**: Consider PostgreSQL for production
4. **API Enhancements**: Add more endpoints as needed
5. **Monitoring**: Add logging and monitoring

