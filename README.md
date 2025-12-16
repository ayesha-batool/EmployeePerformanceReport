# 📊 Employee Performance Report System

**Team**: ScoreSquad  
**Project**: Employee Performance Tracking & Manager Assessment Tool

A comprehensive employee performance tracking and analytics system with an agentic framework, built with Streamlit, Supabase, and AI-powered automation.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Installation & Setup](#installation--setup)
4. [Environment Configuration](#environment-configuration)
5. [Supabase Setup](#supabase-setup)
6. [How to Run](#how-to-run)
7. [Authentication](#authentication)
8. [All Pages & Features](#all-pages--features)
9. [Agentic Framework](#agentic-framework)
10. [AI Integration](#ai-integration)
11. [Event-Driven Architecture](#event-driven-architecture)
12. [ML Models](#ml-models)
13. [API Endpoints](#api-endpoints)
14. [MCP Server](#mcp-server)
15. [Technical Architecture](#technical-architecture)
16. [Troubleshooting](#troubleshooting)

---

## Overview

This is a comprehensive **Employee Performance Management System** built with Streamlit. It uses an **agentic framework** with specialized agents, AI-powered automation, event-driven architecture, and ML models for intelligent decision-making.

### Key Features

- ✅ User Authentication (Supabase)
- ✅ Project Management (CRUD operations)
- ✅ Task Management (CRUD operations)
- ✅ Employee Management (CRUD operations)
- ✅ Performance Evaluation (AI-powered scoring)
- ✅ Advanced Analytics Dashboard
- ✅ Feedback System
- ✅ Goal Tracking
- ✅ Export & Sharing (CSV, PDF)
- ✅ AI-Powered Automation
- ✅ Event-Driven Architecture
- ✅ ML Models for Intelligent Decisions
- ✅ Supabase PostgreSQL Database

---

## Quick Start

### First Time Setup:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements_ml.txt  # For ML features
   ```

2. **Configure environment:**
   - Create `.env` file (see [Environment Configuration](#environment-configuration))
   - Add Supabase credentials
   - Add AI API keys (optional but recommended)

3. **Set up Supabase:**
   - Run `supabase_schema.sql` in Supabase SQL Editor
   - (See [Supabase Setup](#supabase-setup) for details)

4. **Run the application:**
   ```bash
   python -m streamlit run app.py
   ```

5. **Login:**
   - Use `owner@company.com` / `admin123` for admin access
   - Or `john@company.com` / `password123` for employee access

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
pip install -r requirements_ml.txt  # For ML features
```

**Required packages:**
- streamlit
- pandas
- plotly
- numpy
- supabase
- python-dotenv
- openai (for AI features)
- anthropic (optional)
- google-generativeai (optional)
- scikit-learn (for ML)
- xgboost (for ML)
- prophet (for time-series forecasting)

### 3. Configure Environment Variables

See [Environment Configuration](#environment-configuration) section below.

---

## Environment Configuration

### Create .env File

Create a `.env` file in the project root with your credentials:

```bash
# Supabase (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# AI Configuration (Optional but Recommended)
USE_AI=true
AI_PROVIDER=openai  # or gemini or anthropic
AI_MODEL=gpt-3.5-turbo  # or gemini-pro, etc.

# AI API Keys (Add ONE of these)
OPENAI_API_KEY=sk-your-key-here
# OR
GEMINI_API_KEY=your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional: Atlas Integration
ATLAS_JWT_SECRET=your-secret-key
ATLAS_API_URL=http://localhost:8000
ALLOW_LOCAL_AUTH_BYPASS=true
```

### Steps

1. **Create `.env` file** in the project root directory
2. **Add the credentials** above
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run the schema**: Copy `supabase_schema.sql` to Supabase SQL Editor and execute
5. **Run the app**: `python -m streamlit run app.py`

---

## Supabase Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### 2. Run Database Schema

1. Open Supabase Dashboard → SQL Editor
2. Copy and paste the contents of `supabase_schema.sql`
3. Click "Run" to execute the schema
4. Verify tables are created in the Table Editor

### 3. Configure Environment Variables

Add your Supabase credentials to `.env`:
- URL: `https://your-project-id.supabase.co`
- Anon Key: Your anon key from Supabase dashboard

### 4. Database Schema

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
- `achievements` - Employee achievements

All tables use UUID primary keys and have proper indexes for performance.

---

## How to Run

### Option 1: Run Streamlit Application

```bash
python -m streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

**Default Login Credentials:**
- **Owner/Admin**: `owner@company.com` / `admin123`
- **Employee**: `john@company.com` / `password123`

### Option 2: Run FastAPI Backend (For Atlas Integration)

```bash
uvicorn api.main:app --port 8003 --reload
```

**Access Points:**
- API Base URL: `http://localhost:8003`
- Interactive Docs: `http://localhost:8003/docs` (Swagger UI)
- Alternative Docs: `http://localhost:8003/redoc` (ReDoc)
- Health Check: `http://localhost:8003/health`

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

1. System checks Supabase for user authentication
2. Users have roles: `owner`, `manager`, or `employee`
3. Role determines access to different features

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
- Achievement logging and tracking

**Who can access:** All employees (shows their own data)

---

### 3. 📁 Projects (Project Management)

**What it does:**
- **View Projects**: Table view with Edit/Delete actions
- **Create Project**: Add new projects with name, description, status, deadline, manager
- **Project Tasks**: View tasks as sub-items within each project
- **Project Reports**: Generate detailed project reports including:
  - Project status overview
  - Task breakdown
  - Team performance on project
  - Timeline and milestones

**Who can access:** Managers and Owners (full access), Employees (view only)

---

### 4. ✅ Tasks (Task Management)

**Tasks are now integrated into the Projects page as sub-items.**

**What it does:**
- Tasks displayed within their parent projects
- **Create Task**: Create and assign tasks with title, description, priority, status, due date, assigned employee
- **My Tasks**: Filtered view of tasks assigned to logged-in user
- Task updates trigger event-driven notifications

**Who can access:** Everyone (role-based permissions)

---

### 5. 👥 Employees (Employee Management)

**What it does:**
- **View Employees**: Table with all employees (Edit/Delete)
- **Create Employee**: Add new employees with name, email, position, hire date
- Employee details and management

**Who can access:** Managers and Owners only

---

### 6. 📈 Performance & Development (Merged Page)

**What it does:**
- **Performance Evaluation**: 
  - Select employee from dropdown
  - Click "Evaluate Performance" button
  - System calculates (AI-powered):
    - **Performance Score** (0-100) using ML model
    - **Completion Rate** (%)
    - **On-Time Rate** (%)
    - **Rank** (among all employees)
    - **Trend** (improving/declining/stable)
- Shows performance history chart
- Displays detailed evaluation metrics
- AI-powered insights and predictions
- **13 Tabs**: Performance, Goals, Feedback, Skills, Development Plans, Achievements, Analytics, Reports, Trends, Comparisons, Predictions, Recommendations, Export

**Who can access:** Managers and Owners

---

### 7. 🎯 Goals

**What it does:**
- **Goals Tab**: 
  - View all goals with progress tracking
  - Create goal for employees with title, description, target date, assigned employee
  - Goal progress visual indicators (0-100%)
  - Goal status: Active, Completed, Overdue (AI-determined)
  - Goal reports: Goal completion statistics
  - ML-based progress trend analysis and auto-adjustment

**Who can access:** Everyone (role-based)

---

### 8. 💬 Feedback (Feedback System)

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
- AI-powered feedback analysis

**Who can access:** Everyone (role-based views)

---

### 9. 📤 Export (Data Export)

**What it does:**
- **CSV Export**: Export data in CSV format (Projects, Tasks, Employees, Performance, etc.)
- **PDF Export**: Generate PDF reports (Performance reports, Project reports, Personal performance summary)
- **Email Sharing**: Send reports via email (SMTP config needed)

**Who can access:** Managers and Owners

---

## Agentic Framework

The system uses **8 essential agents** for automation:

### 1. EnhancedPerformanceAgent
- AI-powered performance score calculation (0-100)
- ML model integration (Random Forest/XGBoost)
- AI-determined employee rankings
- AI-analyzed performance trends (improving/declining/stable)
- Multi-metric evaluation
- Performance history tracking
- Publishes `PERFORMANCE_EVALUATED` and `PERFORMANCE_TREND_CHANGED` events

### 2. ReportingAgent
- AI-calculated project health scores
- AI-identified project risks with severity assessment
- System overview reports
- Resource allocation analysis
- Completion date estimation
- Publishes `PROJECT_HEALTH_CHANGED` and `RISK_DETECTED` events

### 3. NotificationAgent
- AI-determined notification timing
- Reinforcement Learning (Q-Learning) for spam prevention
- AI-generated personalized messages
- Multi-channel delivery (in-app, email)
- Notification management (read/unread)
- Priority-based notifications

### 4. GoalAgent
- AI-determined goal status (active, completed, overdue, at_risk, on_hold)
- ML-based progress trend analysis
- Auto-adjusts goals based on employee capacity
- Progress tracking and updates
- Goal creation and management
- Publishes `GOAL_CREATED`, `GOAL_PROGRESS_UPDATED`, `GOAL_COMPLETED`, `GOAL_OVERDUE` events

### 5. FeedbackAgent
- AI-powered feedback analysis
- Structured feedback creation
- Employee response handling
- Communication threads
- Feedback status management
- Publishes `FEEDBACK_CREATED` and `FEEDBACK_RESPONDED` events

### 6. ExportAgent
- CSV exports with metadata
- PDF report generation
- Data formatting and presentation
- Export scheduling support

### 7. PromotionAgent
- ML classification model (Random Forest/XGBoost)
- Promotion probability prediction (0-1)
- Analyzes: Performance, Consistency, Skills, Leadership
- Candidate recommendations
- Multi-candidate comparison

### 8. EventHandlers
- AI-powered event handlers for event-driven architecture
- Handles 24+ event types
- Replaces all rule-based logic with AI decisions
- Context-aware event processing

---

## AI Integration

### Overview

The system uses **AI APIs exclusively** for all intelligent decision-making. All rule-based logic has been removed and replaced with AI-powered analysis.

### Supported Providers

1. **OpenAI** (ChatGPT)
   - Models: GPT-4, GPT-3.5-turbo
   - Get API Key: https://platform.openai.com/api-keys

2. **Google Gemini** (Free tier available)
   - Models: gemini-pro, gemini-pro-vision
   - Get API Key: https://makersuite.google.com/app/apikey

3. **Anthropic Claude**
   - Models: Claude 3 Opus, Sonnet, Haiku
   - Get API Key: https://console.anthropic.com/

### Configuration

Add to `.env`:
```env
USE_AI=true
AI_PROVIDER=openai  # or gemini or anthropic
AI_MODEL=gpt-3.5-turbo  # or gemini-pro, etc.

# Add ONE of these:
OPENAI_API_KEY=sk-your-key-here
# OR
GEMINI_API_KEY=your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### AI Features

- **Intelligent Task Assignment**: AI analyzes task requirements, employee skills, workload, and performance
- **AI-Powered Risk Analysis**: AI determines severity, impact, mitigation strategies
- **Natural Language Query Processing**: AI understands complex questions
- **AI-Generated Recommendations**: Performance improvement suggestions
- **Intelligent Performance Alerts**: AI generates actionable recommendations

---

## Event-Driven Architecture

### Overview

The system uses **100% event-driven architecture**. All decisions and actions are triggered by events, with AI-powered event handlers making intelligent decisions instead of following fixed rules.

### Event Bus

Central event distribution system (`components/managers/event_bus.py`):
- Event publishing and subscription
- Event history tracking
- Handler registration
- Event filtering

### Event Types (24+)

- **Task Events**: `TASK_CREATED`, `TASK_UPDATED`, `TASK_COMPLETED`, `TASK_OVERDUE`, `TASK_ASSIGNED`
- **Performance Events**: `PERFORMANCE_EVALUATED`, `PERFORMANCE_LOW`, `PERFORMANCE_HIGH`, `PERFORMANCE_TREND_CHANGED`
- **Goal Events**: `GOAL_CREATED`, `GOAL_UPDATED`, `GOAL_COMPLETED`, `GOAL_OVERDUE`, `GOAL_PROGRESS_UPDATED`
- **Feedback Events**: `FEEDBACK_CREATED`, `FEEDBACK_RESPONDED`, `FEEDBACK_UPDATED`
- **Project Events**: `PROJECT_CREATED`, `PROJECT_UPDATED`, `PROJECT_COMPLETED`, `PROJECT_HEALTH_CHANGED`
- **Risk Events**: `RISK_DETECTED`, `RISK_RESOLVED`, `RISK_SEVERITY_CHANGED`
- **System Events**: `SYSTEM_STARTED`, `SYSTEM_SHUTDOWN`

### Event Handlers

AI-powered event handlers (`components/agents/event_handlers.py`):
- All handlers use AI for decision-making
- No fixed rules or thresholds
- Context-aware processing
- 20+ handlers for different event types

### Benefits

1. **Decoupled Architecture**: Agents don't need to know about each other
2. **AI-Powered Decisions**: Every event handler uses AI
3. **Extensibility**: Easy to add new event types and handlers
4. **Traceability**: Full event history for debugging
5. **Flexibility**: Change behavior by updating handlers

---

## ML Models

### Overview

The system uses **Machine Learning models** instead of rule-based logic for intelligent decision-making:

1. **Performance Scoring** - Random Forest/XGBoost
2. **Notification Optimization** - Reinforcement Learning (Q-Learning)
3. **Predictive Analytics** - Time-series Forecasting (LSTM/Prophet)
4. **Goal Management** - Progress Trend Analysis
5. **Promotion Classification** - Random Forest/XGBoost

### 1. Performance Scoring Model

**File**: `components/ml/performance_scorer.py`

**Inputs**:
- Task Quality (0-1)
- Feedback Sentiment (0-1)
- Attendance Trend (0-1)
- Workload Balance (0-1)

**Output**: Performance score (0-100)

**Usage**:
```python
from components.ml.performance_scorer import PerformanceScorer

scorer = PerformanceScorer(model_type="random_forest")
score = scorer.predict(employee_data)
```

### 2. Notification RL Agent

**File**: `components/ml/notification_rl.py`

**Learning**:
- Learns when notifications are effective
- Stops spamming automatically
- Adapts to user response patterns

**Actions**: `send`, `delay`, `skip`

**Usage**:
```python
from components.ml.notification_rl import NotificationRL

rl_agent = NotificationRL()
decision = rl_agent.should_send_notification(notification_data)
```

### 3. Predictive Analytics

**File**: `components/ml/predictive_analytics.py`

**Predictions**:
- Future Performance (30-day forecast)
- Burnout Risk (0-1 score)
- Promotion Readiness (0-1 score)

**Models**: Prophet (time-series) or LSTM

### 4. Promotion Classifier

**File**: `components/ml/promotion_classifier.py`

**Inputs**:
- Performance (0-1)
- Consistency (0-1)
- Skills (0-1)
- Leadership (0-1)

**Output**: Promotion probability (0-1)

**Usage**:
```python
from components.agents.promotion_agent import PromotionAgent

promotion_agent = PromotionAgent(data_manager)
analysis = promotion_agent.analyze_promotion_eligibility(employee_id)
```

### Installation

```bash
pip install -r requirements_ml.txt
```

**Dependencies**:
- scikit-learn
- xgboost
- prophet
- tensorflow (optional, for LSTM)
- stable-baselines3 (optional, for advanced RL)

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

The MCP server provides 22+ tools:

**Performance Management:**
- `evaluate_all_employees` - Evaluate all employees at once
- `generate_performance_report` - Generate reports (JSON/PDF/CSV)
- `get_employee_stats` - Get comprehensive employee statistics
- `get_user_performance` - Get comprehensive performance data
- `create_performance_review` - Create performance review
- `predict_performance_trend` - Predict performance trend

**Goal Management:**
- `set_performance_goal` - Set performance goal
- `track_goal_progress` - Track goal progress
- `check_overdue_goals` - Find and notify about overdue goals

**Feedback & Skills:**
- `submit_peer_feedback` - Submit peer feedback
- `assess_skills` - Assess skills
- `identify_skill_gaps` - Identify skill gaps

**Monitoring:**
- `detect_all_risks` - Detect all system risks
- `check_overdue_tasks` - Find and notify about overdue tasks
- `assess_workload` - Check employee workload

**Team Management:**
- `get_team_performance` - Get team performance

**Automation:**
- `automated_daily_check` - Run all daily checks at once

### Usage

#### With Claude Desktop

Once configured, you can use the tools directly in Claude Desktop conversations:

```
"Evaluate all employees and save the results"
"Check for overdue tasks and send notifications"
"Generate a performance report for employee ID 3"
```

---

## Technical Architecture

### Project Structure

```
project/
├── app.py                          # Main Streamlit application
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── requirements_ml.txt            # ML dependencies
├── supabase_schema.sql            # Database schema
├── api/                            # FastAPI backend
│   ├── main.py                    # FastAPI app
│   ├── database.py                # Database setup
│   ├── models.py                  # Database models
│   ├── dependencies.py           # JWT validation
│   ├── routes/                    # API routes
│   └── services/                  # Services
├── components/
│   ├── managers/
│   │   ├── data_manager.py         # Supabase data manager
│   │   ├── supabase_client.py      # Supabase client
│   │   ├── auth_manager.py         # Authentication system
│   │   ├── ai_client.py            # AI client
│   │   └── event_bus.py            # Event bus
│   ├── agents/                     # 8 essential agents
│   │   ├── performance_agent.py
│   │   ├── reporting_agent.py
│   │   ├── notification_agent.py
│   │   ├── export_agent.py
│   │   ├── goal_agent.py
│   │   ├── feedback_agent.py
│   │   ├── promotion_agent.py
│   │   └── event_handlers.py
│   └── ml/                         # ML models
│       ├── performance_scorer.py
│       ├── notification_rl.py
│       ├── predictive_analytics.py
│       └── promotion_classifier.py
├── mcp_server/                     # MCP server
│   ├── server.py                   # MCP server implementation
│   ├── cli.py                      # CLI interface
│   ├── scheduler.py               # Scheduled tasks
│   └── example_usage.py            # Usage examples
└── exports/                        # Exported files (auto-created)
```

### Data Storage

**Primary Storage**: Supabase PostgreSQL
- All data stored in Supabase PostgreSQL database
- Tables defined in `supabase_schema.sql`
- UUID primary keys for all tables
- Row Level Security (RLS) enabled

**Data Manager**: The system uses `DataManager` that:
- Uses Supabase as primary storage
- Direct SupabaseClient usage
- No fallbacks, just Supabase

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with agentic framework
- **API**: FastAPI (REST API)
- **Database**: Supabase PostgreSQL
- **Authentication**: Supabase
- **Charts**: Plotly (interactive visualizations)
- **Agents**: 8 essential agents for automation
- **AI**: OpenAI, Anthropic, Google Gemini
- **ML**: scikit-learn, XGBoost, Prophet, TensorFlow
- **MCP Server**: Model Context Protocol for AI integration

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

### Supabase Connection Issues?
- Check `.env` file has correct credentials
- Verify Supabase project is active
- Check network connectivity
- Verify schema has been run in Supabase SQL Editor

### AI Not Working?
- Check `USE_AI=true` in `.env`
- Verify API key is set correctly
- Make sure library is installed (`pip install openai` or `google-generativeai`)
- Check API key has credits/quota

### MCP Server Not Working?
- Ensure MCP package is installed: `pip install mcp`
- Check paths in configuration are absolute
- Verify you're running from project root

---

## Support

For issues or questions, check:
- This README file
- `components/agents/` - Agent implementations
- `api/` - API implementation
- `mcp_server/` - MCP server documentation
- Supabase Dashboard - Database management

---

## License

This project is part of a Software Project Management course.

---

**Happy Performance Tracking! 🚀**
