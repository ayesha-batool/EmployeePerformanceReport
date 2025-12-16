# Frontend-Backend Separation

## Architecture Overview

The application is now separated into:

### Backend (FastAPI)
- **Location**: `api/` directory
- **Main file**: `api/main.py`
- **Purpose**: All business logic, data management, and agent operations
- **Endpoints**: 
  - `/api/dashboard/*` - Dashboard data endpoints
  - `/api/frontend/*` - Frontend-specific endpoints (auth, goals, feedback, reports, etc.)

### Frontend (Streamlit)
- **Location**: `app.py`
- **Purpose**: Pure UI layer that calls backend API
- **API Client**: `components/managers/api_client.py`

## How to Run

### 1. Start Backend
```bash
cd api
uvicorn main:app --reload --port 8003
```

Or:
```bash
python -m api.main
```

### 2. Start Frontend
```bash
streamlit run app.py
```

## API Endpoints

### Authentication
- `POST /api/frontend/auth/login` - Login user

### Dashboard
- `GET /api/dashboard/overview?user_role={role}&user_id={id}` - Get dashboard data

### Goals
- `GET /api/frontend/goals?user_id={id}&user_role={role}` - Get goals
- `POST /api/frontend/goals` - Create goal

### Feedback
- `GET /api/frontend/feedback?employee_id={id}&user_role={role}` - Get feedback
- `POST /api/frontend/feedback` - Create feedback
- `POST /api/frontend/feedback/{id}/respond` - Respond to feedback

### Reports
- `GET /api/frontend/reports/overview` - Get overview report
- `GET /api/frontend/reports/project/{project_id}` - Get project report
- `POST /api/frontend/reports/export?data_type={type}` - Export data

### Employees
- `GET /api/frontend/employees` - Get all employees with performance

### Projects
- `GET /api/frontend/projects?user_id={id}&user_role={role}` - Get projects with tasks

### Tasks
- `POST /api/frontend/tasks/{task_id}/update` - Update task

## Configuration

Set environment variable for API URL:
```bash
export API_BASE_URL=http://localhost:8003
```

Or in `.env`:
```
API_BASE_URL=http://localhost:8003
```

## Benefits

1. **Separation of Concerns**: UI logic separate from business logic
2. **Scalability**: Backend can be scaled independently
3. **Reusability**: API can be used by other clients (mobile, web, etc.)
4. **Testing**: Backend and frontend can be tested independently
5. **Deployment**: Can deploy frontend and backend separately

