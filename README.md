# Employee Performance Report System

A comprehensive employee performance tracking and analytics system with an agentic framework, built with Streamlit.

## Features

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

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure Supabase for authentication:
   - Set environment variables:
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_KEY`: Your Supabase API key

4. (Optional) Configure SMTP for email notifications:
   - Set environment variables:
     - `SMTP_HOST`: SMTP server host
     - `SMTP_PORT`: SMTP server port (default: 587)
     - `SMTP_USER`: SMTP username
     - `SMTP_PASSWORD`: SMTP password

## Running the Application

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Default Login Credentials

- **Owner**: 
  - Email: `owner@company.com`
  - Password: `admin123`

- **Employee**: 
  - Email: `john@company.com`
  - Password: `password123`

## Project Structure

```
project/
├── app.py                          # Main Streamlit application
├── components/
│   ├── managers/
│   │   ├── data_manager.py         # JSON file persistence
│   │   └── auth_manager.py         # Authentication system
│   └── agents/
│       ├── task_agent.py           # Task management agent
│       ├── performance_agent.py    # Performance evaluation agent
│       ├── reporting_agent.py      # Reporting and analytics agent
│       ├── notification_agent.py   # Notification system agent
│       ├── risk_agent.py           # Risk detection agent
│       ├── assistant_agent.py      # AI assistant agent
│       ├── export_agent.py         # Export functionality agent
│       ├── goal_agent.py          # Goal tracking agent
│       ├── feedback_agent.py       # Feedback management agent
│       ├── filtering_agent.py     # Filtering and sorting agent
│       ├── comparison_agent.py    # Team comparison agent
│       └── enhanced_ai_agent.py    # Enhanced AI features agent
├── data/                           # JSON data files (auto-created)
├── exports/                        # Exported files (auto-created)
├── requirements.txt                # Python dependencies
└── README.md                      # This file
```

## All 12 Agents

1. **TaskAgent** - Autonomous task creation, validation, assignment, and notification
2. **EnhancedPerformanceAgent** - Multi-metric performance evaluation
3. **ReportingAgent** - Comprehensive project reports and analytics
4. **NotificationAgent** - Multi-channel notification system
5. **RiskDetectionAgent** - Proactive risk identification
6. **AssistantAgent** - AI-powered natural language query processing
7. **ExportAgent** - Data export in multiple formats (CSV, PDF)
8. **GoalAgent** - Goal setting, tracking, and progress management
9. **FeedbackAgent** - Structured feedback management
10. **FilteringAgent** - Advanced filtering and sorting
11. **ComparisonAgent** - Team performance comparison
12. **EnhancedAIAgent** - AI-powered predictions, insights, and correlations

## Data Storage

All data is stored in JSON files in the `data/` directory:
- `projects.json` - Project data
- `tasks.json` - Task data
- `employees.json` - Employee data
- `performance.json` - Performance evaluations
- `users.json` - User authentication data
- `feedback.json` - Feedback data
- `goals.json` - Goal data
- `notifications.json` - Notification data
- `risks.json` - Risk data

## Features Overview

### Dashboard
- System overview metrics
- Project status charts
- Task completion rate gauge

### Projects
- View all projects
- Create new projects
- Generate project reports

### Tasks
- View all tasks
- Create and assign tasks
- View assigned tasks

### Employees
- View all employees
- Create new employees
- Employee management

### Performance
- Evaluate employee performance
- View performance history
- Performance trend charts

### Analytics
- System overview analytics
- AI-powered insights
- Performance predictions

### Risks
- Automated risk detection
- Risk categorization
- Risk details and recommendations

### Goals
- Create and track goals
- Goal progress visualization
- Goal status management

### Feedback
- Create structured feedback
- Employee responses
- Feedback tracking

### Notifications
- View notifications
- Mark as read
- Notification management

### Export
- Export data to CSV/PDF
- Generate performance reports
- Download reports

### Comparison
- Compare team performance
- Generate comparison charts
- Team analytics

## Configuration

### Email Sharing
Email sharing is implemented but requires SMTP configuration. Set the following environment variables:
- `SMTP_HOST`
- `SMTP_PORT` (default: 587)
- `SMTP_USER`
- `SMTP_PASSWORD`

### Training Correlation
The training correlation feature is a placeholder implementation. It requires training data integration for accurate correlation analysis.

## License

This project is part of a Software Project Management course.

## Support

For issues or questions, please refer to the project documentation or contact the development team.

