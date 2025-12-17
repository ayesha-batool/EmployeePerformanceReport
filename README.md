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
9. [Employee Performance Reports](#employee-performance-reports)
10. [Agentic Framework](#agentic-framework)
11. [AI Integration & Performance Calculation](#ai-integration--performance-calculation)
12. [ML Models & Training](#ml-models--training)
13. [Event-Driven Architecture](#event-driven-architecture)
14. [API Endpoints](#api-endpoints)
15. [Frontend-Backend Separation](#frontend-backend-separation)
16. [MCP Server](#mcp-server)
17. [Technical Architecture](#technical-architecture)
18. [Troubleshooting](#troubleshooting)

---

## Overview

This is a comprehensive **Employee Performance Management System** built with Streamlit. It uses an **agentic framework** with specialized agents, AI-powered automation, event-driven architecture, and ML models for intelligent decision-making.

### Key Features

- ✅ User Authentication (Supabase)
- ✅ Project Management (CRUD operations)
- ✅ Task Management (CRUD operations)
- ✅ Employee Management (CRUD operations - Add, Edit, Delete)
- ✅ Performance Evaluation (AI-powered scoring)
- ✅ Employee Performance Reports (PDF generation)
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

6. **Add Employees (for Owners/Managers):**
   - Go to **👥 Employees** page
   - Click **➕ Add Employee** tab
   - Fill in employee details and save
   - Return to **📊 Reports** to generate performance reports

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
- reportlab (for PDF generation)

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

### 2. 📁 Projects (Project Management)

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

### 3. ✅ Tasks (Task Management)

**Tasks are now integrated into the Projects page as sub-items.**

**What it does:**
- Tasks displayed within their parent projects
- **Create Task**: Create and assign tasks with title, description, priority, status, due date, assigned employee
- **My Tasks**: Filtered view of tasks assigned to logged-in user
- Task updates trigger event-driven notifications

**Who can access:** Everyone (role-based permissions)

---

### 4. 👥 Employees (Employee Management)

**What it does:**
- **View Employees**: List of all employees with performance metrics
- **Add Employee**: Create new employees with:
  - Name (required)
  - Email (required)
  - Position (optional)
  - Hire Date (optional)
  - Skills (optional, JSON format)
- **Edit Employee**: Update employee information
- **Delete Employee**: Remove employee from system (with confirmation)
- Employee details and performance tracking

**Who can access:** Managers and Owners only

---

### 5. 🎯 Goals

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

### 6. 💬 Feedback (Feedback System)

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

### 7. 📊 Reports (Employee Performance Reports)

**What it does:**
- **Employee Performance Report**: Generate professional PDF reports based on performance metrics
- **Preview Report**: View detailed performance metrics before generating PDF:
  - Key Performance Metrics (Performance Score, Completion Rate, On-Time Rate, Rank)
  - Tasks Summary (Total, Completed, In Progress, Pending)
  - Goals Summary (Total, Achieved, Active)
  - Feedback Summary (Total Feedback, Average Rating)
  - Performance Trend (Improving/Declining/Stable)
- **Generate PDF Report**: Download professional PDF document with:
  - Employee Information
  - Performance Summary
  - Tasks Summary
  - Goals Summary
  - Recent Feedback
  - Performance Trends

**Who can access:** 
- Employees: Can generate their own reports
- Managers/Owners: Can generate reports for any employee

**How to Use:**
1. Select an employee from the dropdown
2. Click "📊 Preview Report" to see detailed metrics
3. Click "📥 Generate PDF Report" to download PDF

**Note:** If you see "No employees available", you need to add employees first through the Employees page.

---

### 8. 📤 Export (Data Export)

**What it does:**
- **CSV Export**: Export data in CSV format (Projects, Tasks, Employees, Performance, etc.)
- **PDF Export**: Generate PDF reports (Performance reports, Project reports, Personal performance summary)

**Who can access:** Managers and Owners

---

## Employee Performance Reports

### Overview

The Reports page allows you to generate professional Employee Performance Reports based on performance metrics. The system uses a hybrid approach combining ML models and AI APIs for intelligent performance calculation.

### How to Generate Reports

1. **Navigate to Reports Page**: Click "📊 Reports" in the sidebar
2. **Select Employee**: Choose an employee from the dropdown (employees see only themselves)
3. **Preview Report**: Click "📊 Preview Report" to see detailed metrics
4. **Generate PDF**: Click "📥 Generate PDF Report" to download a professional PDF

### Report Contents

The performance report includes:
- **Employee Information**: Name, Email, Position, Report Date
- **Performance Summary**: 
  - Overall Performance Score (0-100%)
  - Task Completion Rate
  - On-Time Delivery Rate
  - Rank among employees
  - Performance Trend
- **Tasks Summary**: Breakdown by status (Completed, In Progress, Pending)
- **Goals Summary**: Total goals, achieved goals, active goals
- **Recent Feedback**: Average rating and feedback count

### If No Employees Available

If you see "No employees available":
- **For Owners/Managers**: Click "➡️ Go to Employees Page" button to add employees
- **For Employees**: Contact your administrator to add your employee record

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

## AI Integration & Performance Calculation

### Overview

The system uses a **hybrid approach** combining:
1. **ML Models** (Random Forest/XGBoost) - Primary method
2. **AI API** (OpenAI/Anthropic/Gemini) - Fallback and intelligent analysis
3. **Rule-based calculations** - Basic metrics

### Architecture Flow

```
Employee Data → Performance Agent → ML Scorer → AI Fallback (if needed) → Performance Score
```

### Performance Calculation Process

#### Step 1: Calculate Basic Metrics (Rule-based)
- Total tasks
- Completed tasks
- Completion rate
- On-time completion rate

#### Step 2: Prepare Data for ML Model
```python
employee_data = {
    "tasks": employee_tasks,
    "feedbacks": self._get_feedbacks(employee_id),
    "attendance": [],
    "workload": active_tasks_count
}
```

#### Step 3: ML Model Prediction
- Uses Random Forest or XGBoost model
- Extracts 4 key features:
  1. **Task Quality (0-1)**: On-time completion bonus (+0.3), High priority completion (+0.2)
  2. **Feedback Sentiment (0-1)**: Positive vs negative feedback ratio
  3. **Attendance Trend (0-1)**: Recent attendance rate (last 30 days)
  4. **Workload Balance (0-1)**: Optimal is 5-10 active tasks (0.5)
- Outputs performance score (0-100)

#### Step 4: AI Fallback (if ML not trained)
If ML model is not trained, the system uses AI API to calculate score:
```python
# Sends data to AI API
response = ai_client.chat(
    [{"role": "user", "content": f"Calculate performance score (0-100): {data}"}],
    system_prompt="Return only a number 0-100",
    temperature=0.3,
    max_tokens=50
)
```

#### Step 5: AI Trend Analysis
AI determines if performance is improving, declining, or stable:
```python
# Analyzes historical vs current performance
response = ai_client.chat(
    [{"role": "user", "content": f"Trend: current={score}, history={historical}"}],
    system_prompt="Return one word: improving/declining/stable",
    temperature=0.2,
    max_tokens=10
)
```

### Supported AI Providers

1. **OpenAI** (GPT-3.5, GPT-4)
   - Models: GPT-4, GPT-3.5-turbo
   - Get API Key: https://platform.openai.com/api-keys

2. **Google Gemini** (Free tier available)
   - Models: gemini-pro, gemini-pro-vision
   - Get API Key: https://makersuite.google.com/app/apikey

3. **Anthropic Claude**
   - Models: Claude 3 Opus, Sonnet, Haiku
   - Get API Key: https://console.anthropic.com/

### AI Configuration

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
- **Performance Trend Analysis**: AI determines if performance is improving/declining/stable

### Example API Calls

#### Fallback Score Calculation
```python
messages = [
    {"role": "system", "content": "Return only a number 0-100"},
    {"role": "user", "content": "Calculate performance score (0-100): {\"completion_rate\": 85, \"on_time_rate\": 90}"}
]

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.3,
    max_tokens=50
)
# Response: "87.5"
```

#### Trend Analysis
```python
messages = [
    {"role": "system", "content": "Return one word"},
    {"role": "user", "content": "Trend: current=85, history=[80, 82, 83, 84]. Return: improving/declining/stable"}
]

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.2,
    max_tokens=10
)
# Response: "improving"
```

---

## ML Models & Training

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

### 2. Training the Performance Model

#### Quick Start

```bash
# Install ML dependencies
pip install scikit-learn numpy pandas xgboost

# Train with historical data (if you have performance records)
python train_performance_model.py

# Train with synthetic data (if you don't have enough historical data)
python train_performance_model.py --use-synthetic --num-synthetic 100
```

#### Prerequisites

1. **Install ML Dependencies**:
   ```bash
   pip install -r requirements_ml.txt
   ```
   Or individually:
   ```bash
   pip install scikit-learn numpy pandas xgboost
   ```

2. **Ensure You Have Training Data**:
   - At least 10 performance records in the `performances` table
   - Each record should have a `performance_score` (0-100)
   - Associated tasks, feedbacks, and attendance data

#### Training Methods

**Method 1: Train with Historical Data (Recommended)**
```bash
python train_performance_model.py --model-type random_forest
```

Or with XGBoost:
```bash
python train_performance_model.py --model-type xgboost
```

**Method 2: Train with Synthetic Data**
```bash
python train_performance_model.py --model-type random_forest --use-synthetic --num-synthetic 100
```

This will:
- Use any existing historical data
- Generate 100 synthetic samples based on realistic patterns
- Train the model on the combined dataset

#### How Training Works

1. **Data Collection**: Script collects data from Supabase (employees, tasks, feedbacks, performances, attendance)
2. **Feature Extraction**: For each historical performance record, extracts:
   - Task quality metrics
   - Feedback sentiment
   - Attendance trends
   - Workload balance
3. **Model Training**:
   - Feature Scaling using StandardScaler
   - Train/Test Split (80% training, 20% testing)
   - Model Training (Random Forest or XGBoost)
   - Evaluation (MSE and R² score)
   - Model Saving to `models/performance_scorer.pkl`
4. **Model Usage**: Once trained, the model is automatically loaded by `PerformanceAgent`

#### Training Output

After training, you'll see:
```
✅ Model trained. MSE: 45.23, R²: 0.87
✅ Model saved to models/performance_scorer.pkl
```

**Metrics Explained:**
- **MSE (Mean Squared Error)**: Lower is better (measures prediction error)
- **R² (R-squared)**: Higher is better (0-1, measures model fit)
  - 0.8+ = Excellent
  - 0.6-0.8 = Good
  - <0.6 = Needs improvement

#### Model Configuration

**Random Forest (Default)**:
- n_estimators: 100 trees
- max_depth: 10 levels
- Pros: Fast, interpretable, handles non-linear relationships
- Cons: Can overfit with small datasets

**XGBoost**:
- n_estimators: 100 trees
- max_depth: 6 levels
- learning_rate: 0.1
- Pros: Often more accurate, handles complex patterns
- Cons: Slower training, requires more data

#### Verifying Model Training

```python
import os
if os.path.exists("models/performance_scorer.pkl"):
    print("✅ Model is trained and ready!")
else:
    print("❌ Model not found. Run training script first.")
```

#### Retraining the Model

To retrain with new data:
1. Delete old model (optional): `rm models/performance_scorer.pkl`
2. Run training again: `python train_performance_model.py --model-type random_forest`

The model will be retrained with all available data, including new records.

#### Troubleshooting Training

**Error: "scikit-learn not available"**
```bash
pip install scikit-learn
```

**Error: "Insufficient training data"**
- Solution 1: Add more performance records to Supabase
- Solution 2: Use synthetic data: `python train_performance_model.py --use-synthetic --num-synthetic 200`

**Error: "XGBoost not available"**
```bash
pip install xgboost
```
Or use Random Forest instead: `python train_performance_model.py --model-type random_forest`

**Low R² Score (<0.6)**
- Collect more historical data (need 50+ samples)
- Use synthetic data to supplement
- Try XGBoost instead of Random Forest
- Check data quality in Supabase

### 3. Notification RL Agent

**File**: `components/ml/notification_rl.py`

**Learning**:
- Learns when notifications are effective
- Stops spamming automatically
- Adapts to user response patterns

**Actions**: `send`, `delay`, `skip`

### 4. Predictive Analytics

**File**: `components/ml/predictive_analytics.py`

**Predictions**:
- Future Performance (30-day forecast)
- Burnout Risk (0-1 score)
- Promotion Readiness (0-1 score)

**Models**: Prophet (time-series) or LSTM

### 5. Promotion Classifier

**File**: `components/ml/promotion_classifier.py`

**Inputs**:
- Performance (0-1)
- Consistency (0-1)
- Skills (0-1)
- Leadership (0-1)

**Output**: Promotion probability (0-1)

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

#### Employees
- `GET /api/v1/employees` - Get all employees
- `POST /api/v1/employees` - Create employee (Manager only)
- `PUT /api/v1/employees/{employee_id}` - Update employee (Manager only)
- `DELETE /api/v1/employees/{employee_id}` - Delete employee (Manager only)

### Interactive Documentation

Visit `http://localhost:8003/docs` for Swagger UI with:
- All endpoints listed
- Try it out functionality
- Request/response schemas
- Authentication requirements

---

## Frontend-Backend Separation

### Architecture Overview

The application is separated into:

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

### How to Run

#### 1. Start Backend
```bash
cd api
uvicorn main:app --reload --port 8003
```

Or:
```bash
python -m api.main
```

#### 2. Start Frontend
```bash
streamlit run app.py
```

### Configuration

Set environment variable for API URL:
```bash
export API_BASE_URL=http://localhost:8003
```

Or in `.env`:
```
API_BASE_URL=http://localhost:8003
```

### Benefits

1. **Separation of Concerns**: UI logic separate from business logic
2. **Scalability**: Backend can be scaled independently
3. **Reusability**: API can be used by other clients (mobile, web, etc.)
4. **Testing**: Backend and frontend can be tested independently
5. **Deployment**: Can deploy frontend and backend separately

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
├── train_performance_model.py     # ML model training script
├── api/                            # FastAPI backend
│   ├── main.py                    # FastAPI app
│   ├── database.py                # Database setup
│   ├── models.py                  # Database models
│   ├── dependencies.py           # JWT validation
│   ├── routes/                    # API routes
│   │   ├── dashboard.py
│   │   ├── employees.py
│   │   ├── frontend.py
│   │   ├── reports.py
│   │   └── ...
│   └── services/                  # Services
├── components/
│   ├── managers/
│   │   ├── data_manager.py         # Supabase data manager
│   │   ├── supabase_client.py      # Supabase client
│   │   ├── auth_manager.py         # Authentication system
│   │   ├── ai_client.py            # AI client
│   │   ├── api_client.py           # API client
│   │   └── event_bus.py            # Event bus
│   ├── agents/                     # 8 essential agents
│   │   ├── performance_agent.py
│   │   ├── reporting_agent.py
│   │   ├── notification_agent.py
│   │   ├── export_agent.py
│   │   ├── goal_agent.py
│   │   ├── feedback_agent.py
│   │   ├── promotion_agent.py
│   │   ├── event_handlers.py
│   │   └── professional_report_generator.py
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
- **PDF Generation**: ReportLab

---

## Troubleshooting

### No Employees Available?
- Go to **👥 Employees** page
- Click **➕ Add Employee** tab
- Add at least one employee
- Return to Reports page to generate reports

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

### ML Model Not Working?
- Train the model first: `python train_performance_model.py`
- Check if model exists: `models/performance_scorer.pkl`
- If not trained, system will use AI fallback or weighted average

### MCP Server Not Working?
- Ensure MCP package is installed: `pip install mcp`
- Check paths in configuration are absolute
- Verify you're running from project root

### Report Generation Fails?
- Ensure ReportLab is installed: `pip install reportlab`
- Check if employee exists in database
- Verify employee has performance data (tasks, goals, etc.)

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
