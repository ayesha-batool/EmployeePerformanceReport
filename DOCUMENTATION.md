# 📊 Employee Performance Report System - Complete Documentation

**Team**: ScoreSquad  
**Project**: Employee Performance Tracking & Manager Assessment Tool

A comprehensive employee performance tracking and analytics system with an agentic framework, built with Streamlit.

---

# Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Authentication](#authentication)
4. [All Pages & Features](#all-pages--features)
5. [Agentic Framework](#agentic-framework)
6. [Atlas Integration](#atlas-integration)
7. [Automation Guide](#automation-guide)
8. [MCP Server](#mcp-server)
9. [API Endpoints](#api-endpoints)
10. [Technical Architecture](#technical-architecture)
11. [Features by Sprint](#features-by-sprint)
12. [Configuration](#configuration)

---

## Overview

This is a comprehensive **Employee Performance Management System** built with Streamlit. It uses an **agentic framework** with specialized agents to automate tasks, track performance, detect risks, and provide analytics.

### Key Features

- ✅ User Authentication (Supabase + Local fallback)
- ✅ Project Management (CRUD operations)
- ✅ Task Management (CRUD operations)
- ✅ Employee Management (CRUD operations)
- ✅ Performance Evaluation (Automated scoring)
- ✅ Advanced Analytics Dashboard
- ✅ Feedback System
- ✅ Goal Tracking
- ✅ Risk Detection
- ✅ Export & Sharing (CSV, PDF)
- ✅ Team Comparison
- ✅ Automation & MCP Server
- ✅ FastAPI Backend for Atlas Integration

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- streamlit
- pandas
- plotly
- numpy
- fastapi
- uvicorn
- sqlalchemy
- pyjwt
- httpx
- mcp
- reportlab
- (and more - see requirements.txt)

### 3. (Optional) Configure Supabase for Authentication

Set environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase API key

### 4. (Optional) Configure SMTP for Email Notifications

Set environment variables:
- `SMTP_HOST`: SMTP server host
- `SMTP_PORT`: SMTP server port (default: 587)
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password

---

## 🚀 How to Run

### Option 1: Run with API Backend (Recommended)

**Run both the API server and Streamlit app for full integration:**

1. **Start the API server** (in one terminal):
```bash
python start_api.py
```
The API will run on `http://localhost:8003`
API documentation: `http://localhost:8003/docs`

2. **Start the Streamlit app** (in another terminal):
```bash
python -m streamlit run app.py
```

3. **Enable API integration** by setting environment variable:
```bash
# Windows PowerShell
$env:USE_API="true"
python -m streamlit run app.py

# Linux/Mac
export USE_API=true
python -m streamlit run app.py
```

The app will automatically use the API backend when available, falling back to JSON files if the API is not running.

### Option 2: Run Streamlit Application Only (JSON Files)

**This is the traditional way using JSON files:**

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

**Default Login Credentials:**
- **Owner/Admin**: `owner@company.com` / `admin123`
- **Employee**: `john@company.com` / `password123`

### Option 2: Run FastAPI Backend (For Atlas Integration)

**Run this if you need the API endpoints for Atlas integration.**

```bash
# Start the API server
uvicorn api.main:app --port 8003 --reload
```

**Access Points:**
- API Base URL: `http://localhost:8003`
- Interactive Docs: `http://localhost:8003/docs` (Swagger UI)
- Alternative Docs: `http://localhost:8003/redoc` (ReDoc)
- Health Check: `http://localhost:8003/health`

### Option 3: Run Both (Streamlit + API)

**Run both services simultaneously for full functionality.**

**Terminal 1 (Streamlit):**
```bash
streamlit run app.py
```

**Terminal 2 (FastAPI):**
```bash
uvicorn api.main:app --port 8003 --reload
```

### Option 4: Run Automation Scripts

**For automated tasks without the UI:**

```bash
# Evaluate all employees
python automate.py evaluate

# Detect all risks
python automate.py risks

# Check overdue tasks
python automate.py overdue-tasks

# Check overdue goals
python automate.py overdue-goals

# Run all daily checks
python automate.py daily
```

### Option 5: Run MCP Server

**For AI assistant integration (Claude Desktop, etc.):**

```bash
# Test the MCP server
python -m mcp_server.example_usage

# Use CLI tool
python -m mcp_server.cli evaluate_all_employees --args '{"save_results": true}'

# Run scheduled daily checks
python -m mcp_server.scheduler
```

---

## 📋 Quick Start Guide

### First Time Setup:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Login:**
   - Use `owner@company.com` / `admin123` for admin access
   - Or `john@company.com` / `password123` for employee access

4. **Start using:**
   - Create employees, projects, and tasks
   - Evaluate performance
   - View analytics and reports

### For Atlas Integration:

1. **Start FastAPI backend:**
   ```bash
   uvicorn api.main:app --port 8003 --reload
   ```

2. **Get Atlas JWT token:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/demo-login
   ```

3. **Test API endpoint:**
   ```bash
   curl -X GET http://localhost:8003/api/v1/analytics/user/1/performance \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

4. **View API documentation:**
   - Open browser: `http://localhost:8003/docs`

---

## Authentication

### Default Login Credentials

- **Owner/Admin**: 
  - Email: `owner@company.com`
  - Password: `admin123`

- **Employee**: 
  - Email: `john@company.com`
  - Password: `password123`

### How Authentication Works

1. System checks Supabase first (if configured)
2. Falls back to local JSON file authentication (`data/users.json`)
3. Users have roles: `owner`, `manager`, or `employee`
4. Role determines access to different features

---

## All Pages & Features

### 1. 📊 Dashboard (Main Overview)

**What it does:**
- Shows system-wide metrics and KPIs
- Displays overall team performance score
- Shows top performer
- Displays average goal completion rate
- Shows feedback score
- Visualizes performance trends with charts
- Shows skills development bar chart
- Displays recent reports

**Who can access:** Everyone (role-based views)

---

### 2. 👤 My Dashboard (Employee Self-Service)

**What it does:**
- Personal performance metrics for logged-in employee
- Shows assigned tasks
- Displays personal goals
- Shows feedback received
- Performance history chart
- Task completion statistics

**Who can access:** All employees (shows their own data)

---

### 3. 📁 Projects (Project Management)

**What it does:**
- **View Projects**: Table view with Edit/Delete actions
- **Create Project**: Add new projects with name, description, status, deadline, manager
- **Project Reports**: Generate detailed project reports including:
  - Project status overview
  - Task breakdown
  - Team performance on project
  - Timeline and milestones

**Who can access:** Managers and Owners (full access), Employees (view only)

---

### 4. ✅ Tasks (Task Management)

**What it does:**
- **View Tasks**: All tasks in table format with Edit/Delete
- **Create Task**: Create and assign tasks with title, description, priority, status, due date, assigned employee
- **My Tasks**: Filtered view of tasks assigned to logged-in user
- TaskAgent automatically validates and sends notifications

**Who can access:** Everyone (role-based permissions)

**Workflow:**
1. Manager creates task → TaskAgent validates
2. Task assigned to employee → Notification sent
3. Employee updates status → Performance tracked
4. Task completed → Performance score updated

---

### 5. 👥 Employees (Employee Management)

**What it does:**
- **View Employees**: Table with all employees (Edit/Delete)
- **Create Employee**: Add new employees with name, email, department, role, hire date
- Employee details and management

**Who can access:** Managers and Owners only

---

### 6. 📈 Performance (Performance Evaluation)

**What it does:**
- **Evaluate Employee Performance**: 
  - Select employee from dropdown
  - Click "Evaluate Performance" button
  - System calculates:
    - **Performance Score** (0-100)
    - **Completion Rate** (%)
    - **On-Time Rate** (%)
    - **Rank** (among all employees)
    - **Trend** (improving/declining/stable)
- Shows performance history chart
- Displays detailed evaluation metrics

**How Performance is Calculated:**
```
Performance Score = 
  (Completion Rate × 40%) +
  (On-Time Rate × 30%) +
  (Speed Score × 20%) +
  (Priority Handling × 10%)
```

**Metrics Explained:**
- **Completion Rate**: (Completed Tasks / Total Tasks) × 100
- **On-Time Rate**: (Tasks completed on/before deadline / Completed Tasks) × 100
- **Average Completion Time**: Average days to complete tasks
- **High Priority Completed**: Number of high-priority tasks completed
- **Rank**: Position among all employees based on performance score

**Who can access:** Managers and Owners

---

### 7. 🔍 Analytics (Advanced Analytics)

**What it does:**
- **Overview**: System-wide statistics
- **Predictive Reports**:
  - **Capacity Forecast**: Predict employee/team workload capacity
  - **Project Risk Forecast**: Predict project risks
- **Correlation Analysis**: Find relationships between performance and training, task completion and feedback, goals and performance
- **Trend Analysis**: Performance trends over time
- **AI Insights**: AI-powered recommendations and insights

**Who can access:** Managers and Owners only

---

### 8. ⚠️ Risks (Risk Detection)

**What it does:**
- **View Risks**: All detected risks with severity levels
- **Risk Categories**:
  - Employee risks (low performance, overload)
  - Project risks (delays, budget overruns)
  - Task risks (overdue, high priority)
  - Performance risks (declining trends)
- **Risk Details**: Description, severity, affected entities
- **Risk History**: Historical risk data

**How Risks are Detected:**
- RiskDetectionAgent automatically scans:
  - Employee performance drops
  - Overdue tasks
  - Project delays
  - Workload imbalances

**Who can access:** Managers and Owners

---

### 9. 🎯 Goals (Goal Management)

**What it does:**
- **View Goals**: All goals with progress tracking
- **Create Goal**: Set goals for employees with title, description, target date, assigned employee
- **Goal Progress**: Visual progress indicators (0-100%)
- **Goal Status**: Active, Completed, Overdue
- **Goal Reports**: Goal completion statistics

**Who can access:** Everyone (role-based)

**Workflow:**
1. Manager creates goal for employee
2. Employee sees goal in "My Dashboard"
3. Progress updated automatically based on related tasks
4. Goal marked complete when target reached

---

### 10. 💬 Feedback (Feedback System)

**What it does:**
- **Manager View**:
  - Create feedback for employees
  - View all feedback given
  - Respond to employee questions
  - Track feedback status
- **Employee View**:
  - View received feedback
  - Ask questions to manager
  - View conversation thread
- **Feedback Categories**: Performance, Behavior, Skills, etc.

**Who can access:** Everyone (role-based views)

**Workflow:**
1. Manager creates feedback → Employee notified
2. Employee views feedback → Can ask questions
3. Manager responds → Two-way communication
4. Feedback tracked in system

---

### 11. 🔔 Notifications (Notification Center)

**What it does:**
- View all notifications
- Filter by type (Task, Feedback, Goal, Risk, etc.)
- Mark as read
- Notification history

**Notification Types:**
- Task assigned/completed
- Feedback received
- Goal created/updated
- Risk detected
- Performance evaluation

**Who can access:** Everyone (their own notifications)

---

### 12. 📤 Export (Data Export)

**What it does:**
- **CSV Export**: Export data in CSV format (Projects, Tasks, Employees, Performance, etc.)
- **PDF Export**: Generate PDF reports (Performance reports, Project reports, Personal performance summary)
- **Email Sharing**: Send reports via email (SMTP config needed)

**Who can access:** Managers and Owners

---

### 13. ⚖️ Comparison (Team Comparison)

**What it does:**
- Compare employee performance
- Team performance comparison
- Department comparison
- Visual comparison charts (bar, line, area)
- Performance rankings

**Who can access:** Managers and Owners

---

## Agentic Framework

The system uses 12 specialized agents for automation:

### 1. TaskAgent
- Validates task creation
- Automatically assigns tasks
- Sends notifications
- Tracks task completion

### 2. EnhancedPerformanceAgent
- Calculates performance scores
- Tracks completion rates
- Monitors on-time delivery
- Ranks employees
- Calculates trends

### 3. ReportingAgent
- Generates project reports
- Creates overview reports
- Analyzes team statistics

### 4. NotificationAgent
- Sends notifications for:
  - Task assignments
  - Feedback
  - Goals
  - Risks
  - Performance updates

### 5. RiskDetectionAgent
- Scans for employee risks
- Detects project risks
- Identifies task risks
- Monitors performance risks

### 6. AssistantAgent
- Natural language queries
- AI-powered assistance

### 7. ExportAgent
- CSV exports
- PDF generation
- Email sharing

### 8. GoalAgent
- Goal creation
- Progress tracking
- Status management

### 9. FeedbackAgent
- Feedback creation
- Communication threads
- Status tracking

### 10. FilteringAgent
- Advanced filtering
- Sorting capabilities

### 11. ComparisonAgent
- Team comparisons
- Performance rankings
- Comparison charts

### 12. EnhancedAIAgent
- Performance predictions
- Growth insights
- AI recommendations

---

## Atlas Integration

### Integration Plan

**Target**: Integration with Atlas AI Scrum Master MCP Server

### What Atlas Has

- **Backend**: Python FastAPI + SQLite (async)
- **Frontend**: React 18 + TypeScript + Vite
- **Database**: SQLite (atlas.db) with 13 tables
- **Authentication**: JWT tokens (7-day expiry)
- **AI**: OpenAI GPT-4o-mini integration
- **MCP Server**: 18 tools for project management
- **Port**: Backend runs on 8000

### What We Provide

#### FastAPI Backend (Port 8003)

**Required Endpoints:**

```http
# Performance Reviews
GET  /api/v1/reviews/user/{user_id}                # Get user's reviews
POST /api/v1/reviews                                # Create review
GET  /api/v1/reviews/pending                        # Pending reviews for manager

# Goal Management
GET  /api/v1/goals/user/{user_id}                   # Get user's goals
POST /api/v1/goals                                   # Create goal
PUT  /api/v1/goals/{goal_id}/progress               # Update goal progress

# Peer Feedback
POST /api/v1/feedback                                # Submit feedback
GET  /api/v1/feedback/user/{user_id}                # Get user's feedback

# Skill Assessments
GET  /api/v1/skills/user/{user_id}                  # Get user's skills
POST /api/v1/skills/assess                          # Create assessment
GET  /api/v1/skills/gaps/{user_id}                  # Identify skill gaps

# Performance Analytics
GET  /api/v1/analytics/user/{user_id}/performance   # Performance trends
GET  /api/v1/analytics/team/{org_id}/performance    # Team performance

# Reports
GET  /api/v1/reports/user/{user_id}/quarterly       # Quarterly report
GET  /api/v1/reports/team/{org_id}/quarterly        # Team report
```

#### Authentication Integration

- Validate JWT tokens from Atlas
- Extract user_id and role from token
- Implement role-based access (employees vs managers)
- No separate login system needed

#### Database Schema (SQLite)

```sql
-- Link to Atlas users
performance_reviews (
    id, employee_id,  -- Link to Atlas user
    reviewer_id, review_period_start, review_period_end,
    overall_rating, strengths, areas_for_improvement,
    status  -- draft, submitted, acknowledged
)

performance_goals (
    id, user_id,  -- Link to Atlas user
    title, description, goal_type,
    target_value, current_value,
    start_date, target_date, status
)

peer_feedback (
    id, employee_id, reviewer_id,
    project_id,  -- Link to Atlas project
    feedback_type, rating, feedback_text,
    is_anonymous
)

skill_assessments (
    id, user_id,
    skill_name, skill_category,
    proficiency_level, proficiency_score,
    assessed_by, assessment_method
)

performance_metrics (
    id, user_id, metric_date,
    tasks_completed, tasks_on_time,
    productivity_score, collaboration_score,
    overall_score
)
```

#### Data Integration

**Pull data from Atlas for performance calculation:**

```python
# You can call Atlas API to get:
- Task completion rate: GET /api/v1/projects/{project_id}/tasks
- Project contributions: GET /api/v1/projects
- Issue resolution: GET /api/v1/issues/project/{project_id}

# Calculate performance score:
performance_score = (
    task_completion_rate * 0.30 +
    task_quality_score * 0.25 +      # From peer feedback
    productivity_score * 0.20 +      # From Code Crafters if integrated
    collaboration_score * 0.15 +     # From peer feedback
    goal_achievement_rate * 0.10     # From your goals
) * 100
```

#### MCP Tools Integration

**Atlas will add these 10-12 tools to their MCP server:**

1. `get_user_performance(user_id, time_period)` → Calls `GET /api/v1/analytics/user/{user_id}/performance`
2. `create_performance_review(employee_id, review_period)` → Calls `POST /api/v1/reviews`
3. `set_performance_goal(user_id, title, goal_type, target)` → Calls `POST /api/v1/goals`
4. `get_team_performance(organization_id)` → Calls `GET /api/v1/analytics/team/{org_id}/performance`
5. `submit_peer_feedback(employee_id, feedback_type, rating, text)` → Calls `POST /api/v1/feedback`
6. `assess_skills(user_id, skill_name, proficiency_level)` → Calls `POST /api/v1/skills/assess`
7. `identify_skill_gaps(user_id, project_id)` → Calls `GET /api/v1/skills/gaps/{user_id}`
8. `track_goal_progress(goal_id, current_value)` → Calls `PUT /api/v1/goals/{goal_id}/progress`
9. `generate_performance_report(user_id, report_type)` → Calls `GET /api/v1/reports/user/{user_id}/quarterly`
10. `predict_performance_trend(user_id, prediction_months)` → Calls `POST /api/v1/analytics/predict`

#### Integration Flow

```
1. User logs into Atlas → Gets JWT token
2. Manager uses Claude Desktop → MCP calls your API
3. Your API pulls task data from Atlas
4. Your API calculates performance metrics
5. MCP shows performance insights in Claude
```

---

## Automation Guide

### Quick Start

#### Option 1: Standalone Script (Simplest)

Use the standalone automation script for quick tasks:

```bash
# Evaluate all employees
python automate.py evaluate

# Detect all risks
python automate.py risks

# Check overdue tasks
python automate.py overdue-tasks

# Check overdue goals
python automate.py overdue-goals

# Run all daily checks
python automate.py daily
```

#### Option 2: MCP Server (Advanced)

Use the MCP server for integration with AI assistants and other tools:

```bash
# Run example usage
python -m mcp_server.example_usage

# Use CLI tool
python -m mcp_server.cli evaluate_all_employees --args '{"save_results": true}'

# Run scheduled daily checks
python -m mcp_server.scheduler
```

### Available Automation Tasks

#### 1. Performance Evaluation
- **Evaluate all employees**: Automatically calculate performance scores for all employees
- **Generate reports**: Create performance reports in JSON, PDF, or CSV format
- **Get employee stats**: Retrieve comprehensive statistics for any employee

#### 2. Risk Detection
- **Detect all risks**: Automatically identify risks in:
  - Employee performance
  - Project status
  - Task completion
  - System health

#### 3. Monitoring & Alerts
- **Check overdue tasks**: Find tasks past their due date and optionally send notifications
- **Check overdue goals**: Find goals past their deadline and optionally send notifications
- **Assess workload**: Identify employees with excessive workload

#### 4. Daily Automation
- **Automated daily check**: Runs all checks at once:
  - Performance evaluation
  - Risk detection
  - Overdue task checking
  - Overdue goal checking

### Scheduling

#### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `automate.py daily`
7. Start in: `C:\path\to\project`

#### Linux/Mac Cron

Add to crontab (`crontab -e`):

```bash
# Run daily checks at 9 AM
0 9 * * * cd /path/to/project && python automate.py daily

# Run every hour
0 * * * * cd /path/to/project && python automate.py overdue-tasks
```

### Integration Examples

#### With CI/CD Pipelines

```yaml
# GitHub Actions example
name: Daily Performance Check
on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run daily checks
        run: python automate.py daily
```

---

## MCP Server

### Overview

The MCP (Model Context Protocol) server provides automation tools for performance evaluation, notifications, reports, and more.

### Setup

#### 1. Install Dependencies

```bash
pip install mcp httpx
```

#### 2. Configure Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "employee-performance-automation": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

#### 3. Available Tools

The MCP server provides 22 tools:

**Original 12 Tools:**
1. `evaluate_all_employees` - Evaluate performance for all employees
2. `detect_all_risks` - Detect all risks in the system
3. `send_notification` - Send a notification to an employee
4. `generate_performance_report` - Generate a performance report
5. `check_overdue_tasks` - Check for overdue tasks
6. `check_overdue_goals` - Check for overdue goals
7. `assess_workload` - Assess workload for all employees
8. `generate_project_report` - Generate a project report
9. `export_data` - Export data to CSV or PDF
10. `record_attendance` - Record employee attendance
11. `get_employee_stats` - Get comprehensive statistics for an employee
12. `automated_daily_check` - Run automated daily checks

**New Atlas Integration Tools (10):**
13. `get_user_performance` - Get comprehensive performance data
14. `create_performance_review` - Create performance review
15. `set_performance_goal` - Set performance goal
16. `get_team_performance` - Get team performance
17. `submit_peer_feedback` - Submit peer feedback
18. `assess_skills` - Assess skills
19. `identify_skill_gaps` - Identify skill gaps
20. `track_goal_progress` - Track goal progress
21. `generate_performance_report_api` - Generate report via API
22. `predict_performance_trend` - Predict performance trend

### Usage

#### With Claude Desktop

Once configured, you can use the tools directly in Claude Desktop conversations:

```
"Evaluate all employees and save the results"
"Check for overdue tasks and send notifications"
"Generate a performance report for employee ID 3"
```

#### Programmatic Usage

```python
from mcp_server.server import server

# List available tools
tools = await server.list_tools()

# Call a tool
result = await server.call_tool("evaluate_all_employees", {"save_results": True})
```

---

## API Endpoints

### Base URL
```
http://localhost:8003
```

### Authentication
All endpoints require Atlas JWT token:
```
Authorization: Bearer <atlas_jwt_token>
```

### Endpoints

#### Performance Reviews
- `GET /api/v1/reviews/user/{user_id}` - Get user's reviews
- `POST /api/v1/reviews` - Create review
- `GET /api/v1/reviews/pending` - Get pending reviews (Manager only)

#### Goal Management
- `GET /api/v1/goals/user/{user_id}` - Get user's goals
- `POST /api/v1/goals` - Create goal
- `PUT /api/v1/goals/{goal_id}/progress` - Update goal progress

#### Peer Feedback
- `POST /api/v1/feedback` - Submit feedback
- `GET /api/v1/feedback/user/{user_id}` - Get user's feedback

#### Skill Assessments
- `GET /api/v1/skills/user/{user_id}` - Get user's skills
- `POST /api/v1/skills/assess` - Create assessment
- `GET /api/v1/skills/gaps/{user_id}` - Identify skill gaps

#### Performance Analytics
- `GET /api/v1/analytics/user/{user_id}/performance` - Get performance data
- `GET /api/v1/analytics/team/{org_id}/performance` - Get team performance (Manager only)
- `POST /api/v1/analytics/predict` - Predict performance trend

#### Reports
- `GET /api/v1/reports/user/{user_id}/quarterly` - Generate quarterly user report
- `GET /api/v1/reports/team/{org_id}/quarterly` - Generate quarterly team report (Manager only)

### Interactive Documentation

Visit `http://localhost:8003/docs` for Swagger UI with:
- All endpoints listed
- Try it out functionality
- Request/response schemas
- Authentication requirements

---

## Technical Architecture

### Project Structure

```
project/
├── app.py                          # Main Streamlit application
├── api/                            # FastAPI backend
│   ├── main.py                    # FastAPI app
│   ├── database.py                # SQLite setup
│   ├── models.py                  # Database models
│   ├── dependencies.py           # JWT validation
│   ├── routes/                    # API routes
│   │   ├── reviews.py
│   │   ├── goals.py
│   │   ├── feedback.py
│   │   ├── skills.py
│   │   ├── analytics.py
│   │   └── reports.py
│   └── services/                  # Services
│       ├── atlas_client.py        # Atlas API client
│       └── performance_calculator.py
├── components/
│   ├── managers/
│   │   ├── data_manager.py         # JSON file persistence
│   │   └── auth_manager.py         # Authentication system
│   └── agents/                     # 12 specialized agents
│       ├── task_agent.py
│       ├── performance_agent.py
│       ├── reporting_agent.py
│       ├── notification_agent.py
│       ├── risk_agent.py
│       ├── assistant_agent.py
│       ├── export_agent.py
│       ├── goal_agent.py
│       ├── feedback_agent.py
│       ├── filtering_agent.py
│       ├── comparison_agent.py
│       └── enhanced_ai_agent.py
├── mcp_server/                     # MCP server
│   ├── server.py                   # MCP server implementation
│   ├── cli.py                      # CLI interface
│   ├── scheduler.py                # Scheduled tasks
│   └── example_usage.py            # Usage examples
├── data/                           # JSON data files (auto-created)
├── exports/                        # Exported files (auto-created)
├── automate.py                     # Standalone automation script
├── requirements.txt                # Python dependencies
└── DOCUMENTATION.md                # This file
```

### Data Storage

All data is stored in JSON files in the `data/` directory:
- `projects.json` - All projects
- `tasks.json` - All tasks
- `employees.json` - All employees
- `performance.json` - Performance evaluations
- `users.json` - User accounts
- `feedback.json` - Feedback data
- `goals.json` - Goals
- `notifications.json` - Notifications
- `risks.json` - Risk data

API data is stored in SQLite database (`performance.db`):
- `performance_reviews` - Performance reviews
- `performance_goals` - Performance goals
- `peer_feedback` - Peer feedback
- `skill_assessments` - Skill assessments
- `performance_metrics` - Performance metrics
- `employees` - Employee data
- `tasks` - Task data
- `projects` - Project data
- `performances` - Performance evaluations
- `notifications` - Notifications

**Hybrid Data Manager**: The system uses a `HybridDataManager` that:
- Uses API backend when `USE_API=true` and API server is running
- Falls back to JSON files if API is unavailable
- Maintains backward compatibility with existing JSON-based workflow

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with agentic framework
- **API**: FastAPI (REST API)
- **Data Storage**: JSON files + SQLite database
- **Authentication**: Supabase (optional) + Local fallback + JWT
- **Charts**: Plotly (interactive visualizations)
- **Agents**: 12 specialized agents for automation
- **MCP Server**: Model Context Protocol for AI integration

---

## Quick Start Workflow

### For Managers/Owners:

1. **Login** → `owner@company.com` / `admin123`
2. **Create Employees** → Employees Page → Create Employee
3. **Create Projects** → Projects Page → Create Project
4. **Create Tasks** → Tasks Page → Create Task → Assign to Employee
5. **Evaluate Performance** → Performance Page → Select Employee → Evaluate
6. **View Analytics** → Analytics Page → See insights and predictions
7. **Monitor Risks** → Risks Page → Check for issues
8. **Give Feedback** → Feedback Page → Create feedback for employees
9. **Set Goals** → Goals Page → Create goals for employees
10. **Export Data** → Export Page → Download reports

### For Employees:

1. **Login** → `john@company.com` / `password123`
2. **View My Dashboard** → See personal metrics
3. **View My Tasks** → Tasks Page → My Tasks tab
4. **Update Task Status** → Edit task → Change status
5. **View Feedback** → Feedback Page → See received feedback
6. **Ask Questions** → Feedback Page → Ask manager questions
7. **View Goals** → My Dashboard → See assigned goals
8. **View Notifications** → Notifications Page → See updates

---

## Performance Calculation Details

### Performance Score Formula:

```
Score = (Completion_Rate × 0.4) + 
        (On_Time_Rate × 0.3) + 
        (Speed_Score × 0.2) + 
        (Priority_Score × 0.1)
```

### Where:
- **Completion Rate** = (Completed Tasks / Total Tasks) × 100
- **On-Time Rate** = (On-Time Tasks / Completed Tasks) × 100
- **Speed Score** = Normalized completion time (faster = higher)
- **Priority Score** = High priority tasks completed ratio

### Performance Rank:
- All employees evaluated
- Sorted by performance score
- Rank = position in sorted list

### Performance Trend:
- Compares last 2 evaluations
- **Improving**: Score increased by >5 points
- **Declining**: Score decreased by >5 points
- **Stable**: Change within ±5 points

---

## Tips for Best Results

1. **Create Complete Data**: Add employees, projects, and tasks before evaluating performance
2. **Update Task Status**: Keep task statuses current for accurate performance tracking
3. **Set Realistic Deadlines**: On-time completion rate depends on realistic due dates
4. **Regular Evaluations**: Run performance evaluations regularly to track trends
5. **Use Feedback**: Give feedback to help employees improve
6. **Set Goals**: Create goals to motivate and track progress
7. **Monitor Risks**: Check risks page regularly to catch issues early
8. **Export Reports**: Export data for external analysis

---

## Troubleshooting

### No Performance Data?
- Ensure tasks are created and assigned
- Update task statuses to "completed"
- Run performance evaluation

### Can't See Certain Pages?
- Check your role (owner/manager/employee)
- Some pages are role-restricted

### Performance Score is 0?
- Employee needs completed tasks
- Check task assignments
- Verify task statuses

### API Not Working?
- Ensure FastAPI server is running on port 8003
- Check JWT token is valid
- Verify database is initialized

---

## Features by Sprint

### ✅ Sprint 1-2: Core Features
- ✅ User Authentication (Supabase + Local fallback)
- ✅ Project Management (CRUD operations)
- ✅ Task Management (CRUD operations)
- ✅ Employee Management (CRUD operations)
- ✅ Performance Evaluation (Automated scoring)
- ✅ Basic Analytics Dashboard
- ✅ Data Persistence (JSON files)

### ✅ Sprint 3: Feedback System
- ✅ Structured feedback creation
- ✅ Employee response to feedback
- ✅ Feedback tracking and status
- ✅ Notification integration

### ✅ Sprint 4: Filtering & Comparison
- ✅ Advanced filtering (status, date, department)
- ✅ Sorting capabilities
- ✅ Team performance comparison
- ✅ Comparison charts (Plotly)

### ✅ Sprint 5: Export & Sharing
- ✅ CSV export
- ✅ PDF export
- ✅ Personal performance report download
- ✅ Email sharing (SMTP-ready, needs configuration)

### ✅ Sprint 6: Goal Tracking
- ✅ Goal creation
- ✅ Goal progress tracking
- ✅ Goal status management (Active, Completed, Overdue)
- ✅ Employee goal management
- ✅ Progress percentage calculation

### ✅ Sprint 7: Enhanced AI Features
- ✅ Performance trend prediction
- ✅ Training correlation analysis (placeholder)
- ✅ Growth insights generation
- ✅ AI-powered recommendations

### ✅ Sprint 8: Risk Detection & Notifications
- ✅ Automated risk detection (Employee, Project, Task, Performance)
- ✅ Risk categorization (High, Medium, Low)
- ✅ Notification system
- ✅ Real-time alerts

---

## Configuration

### Email Sharing
Email sharing is implemented but requires SMTP configuration. Set the following environment variables:
- `SMTP_HOST`
- `SMTP_PORT` (default: 587)
- `SMTP_USER`
- `SMTP_PASSWORD`

### Training Correlation
The training correlation feature is a placeholder implementation. It requires training data integration for accurate correlation analysis.

### Supabase Authentication
Set environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase API key

### Atlas API Integration
Set environment variables:
- `ATLAS_JWT_SECRET`: JWT secret key for Atlas token validation
- `ATLAS_API_URL`: Atlas API base URL (default: http://localhost:8000)
- `PERFORMANCE_DB_URL`: SQLite database URL (default: sqlite:///./performance.db)

---

## MCP Server Setup

### Quick Start

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The MCP package will be installed automatically. If you encounter issues, install it separately:

```bash
pip install mcp
```

#### 2. Test the Server

Run the example usage script to test:

```bash
python -m mcp_server.example_usage
```

#### 3. Use the CLI Tool

Run individual automation tasks:

```bash
# Evaluate all employees
python -m mcp_server.cli evaluate_all_employees --args '{"save_results": true}'

# Check overdue tasks
python -m mcp_server.cli check_overdue_tasks --args '{"send_notifications": true}'

# Run automated daily check
python -m mcp_server.cli automated_daily_check --args '{"evaluate_performance": true, "detect_risks": true, "check_overdue": true}'
```

#### 4. Schedule Daily Checks

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily" at desired time
4. Action: Start a program
5. Program: `python`
6. Arguments: `-m mcp_server.scheduler`
7. Start in: `C:\path\to\project`

**Linux/Mac (Cron):**

Add to crontab (`crontab -e`):

```bash
# Run daily checks at 9 AM every day
0 9 * * * cd /path/to/project && python -m mcp_server.scheduler
```

#### 5. Configure MCP Client (Optional)

If you want to use this with an MCP client (like Claude Desktop):

**Claude Desktop Configuration**

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "employee-performance-automation": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

### MCP Server Tools

#### Performance Management
- `evaluate_all_employees` - Evaluate all employees at once
- `generate_performance_report` - Generate reports (JSON/PDF/CSV)
- `get_employee_stats` - Get comprehensive employee statistics

#### Monitoring
- `detect_all_risks` - Detect all system risks
- `check_overdue_tasks` - Find and notify about overdue tasks
- `check_overdue_goals` - Find and notify about overdue goals
- `assess_workload` - Check employee workload

#### Automation
- `automated_daily_check` - Run all daily checks at once

#### Other Tools
- `send_notification` - Send notifications
- `generate_project_report` - Generate project reports
- `export_data` - Export data to CSV/PDF
- `record_attendance` - Record attendance

#### Atlas Integration Tools (10 new tools)
- `get_user_performance` - Get comprehensive performance data
- `create_performance_review` - Create performance review
- `set_performance_goal` - Set performance goal
- `get_team_performance` - Get team performance
- `submit_peer_feedback` - Submit peer feedback
- `assess_skills` - Assess skills
- `identify_skill_gaps` - Identify skill gaps
- `track_goal_progress` - Track goal progress
- `generate_performance_report_api` - Generate report via API
- `predict_performance_trend` - Predict performance trend

**Total: 22 MCP Tools**

### MCP Server Troubleshooting

#### Import Errors

If you get import errors, make sure you're running from the project root:

```bash
cd /path/to/project
python -m mcp_server.server
```

#### MCP Library Not Found

If the MCP library is not available, the server will still work for CLI usage. Install it with:

```bash
pip install mcp
```

#### Path Issues

Make sure all paths in configuration files use absolute paths, not relative paths.

---

## Support

For issues or questions, check:
- This documentation file
- `components/agents/` - Agent implementations
- `data/` - Data files structure
- `api/` - API implementation
- `mcp_server/` - MCP server documentation

---

## License

This project is part of a Software Project Management course.

---

**Happy Performance Tracking! 🚀**

