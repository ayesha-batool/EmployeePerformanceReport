# 📊 Employee Performance Report System - Complete Guide

## 🎯 Overview

This is a comprehensive **Employee Performance Management System** built with Streamlit. It uses an **agentic framework** with 12 specialized agents to automate tasks, track performance, detect risks, and provide analytics.

---

## 🔐 Authentication & Getting Started

### Default Login Credentials:
- **Owner/Admin**: `owner@company.com` / `admin123`
- **Employee**: `john@company.com` / `password123`

### How Authentication Works:
1. System checks Supabase first (if configured)
2. Falls back to local JSON file authentication (`data/users.json`)
3. Users have roles: `owner`, `manager`, or `employee`
4. Role determines access to different features

---

## 📑 All Pages & Their Functions

### 1. 📊 **Dashboard** (Main Overview)
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

### 2. 👤 **My Dashboard** (Employee Self-Service)
**What it does:**
- Personal performance metrics for logged-in employee
- Shows assigned tasks
- Displays personal goals
- Shows feedback received
- Performance history chart
- Task completion statistics

**Who can access:** All employees (shows their own data)

---

### 3. 📁 **Projects** (Project Management)
**What it does:**
- **View Projects**: Table view with Edit/Delete actions
- **Create Project**: Add new projects with:
  - Name, description, status, deadline, manager
- **Project Reports**: Generate detailed project reports
  - Project status overview
  - Task breakdown
  - Team performance on project
  - Timeline and milestones

**Who can access:** Managers and Owners (full access), Employees (view only)

---

### 4. ✅ **Tasks** (Task Management)
**What it does:**
- **View Tasks**: All tasks in table format with Edit/Delete
- **Create Task**: Create and assign tasks with:
  - Title, description, priority, status, due date, assigned employee
  - TaskAgent automatically validates and sends notifications
- **My Tasks**: Filtered view of tasks assigned to logged-in user

**Who can access:** Everyone (role-based permissions)

**Workflow:**
1. Manager creates task → TaskAgent validates
2. Task assigned to employee → Notification sent
3. Employee updates status → Performance tracked
4. Task completed → Performance score updated

---

### 5. 👥 **Employees** (Employee Management)
**What it does:**
- **View Employees**: Table with all employees (Edit/Delete)
- **Create Employee**: Add new employees with:
  - Name, email, department, role, hire date
- Employee details and management

**Who can access:** Managers and Owners only

---

### 6. 📈 **Performance** (Performance Evaluation)
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

### 7. 🔍 **Analytics** (Advanced Analytics)
**What it does:**
- **Overview**: System-wide statistics
- **Predictive Reports**:
  - **Capacity Forecast**: Predict employee/team workload capacity
    - Individual employee capacity forecasting
    - Team capacity forecasting
    - Utilization rate analysis
  - **Project Risk Forecast**: Predict project risks
    - Risk level (High/Medium/Low)
    - Risk factors analysis
    - Recommendations
- **Correlation Analysis**: Find relationships between:
  - Performance and training
  - Task completion and feedback
  - Goals and performance
- **Trend Analysis**: Performance trends over time
- **AI Insights**: AI-powered recommendations and insights

**Who can access:** Managers and Owners only

---

### 8. ⚠️ **Risks** (Risk Detection)
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

### 9. 🎯 **Goals** (Goal Management)
**What it does:**
- **View Goals**: All goals with progress tracking
- **Create Goal**: Set goals for employees with:
  - Title, description, target date, assigned employee
  - Progress tracking (0-100%)
  - Status (Active, Completed, Overdue)
- **Goal Progress**: Visual progress indicators
- **Goal Reports**: Goal completion statistics

**Who can access:** Everyone (role-based)

**Workflow:**
1. Manager creates goal for employee
2. Employee sees goal in "My Dashboard"
3. Progress updated automatically based on related tasks
4. Goal marked complete when target reached

---

### 10. 💬 **Feedback** (Feedback System)
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

### 11. 🔔 **Notifications** (Notification Center)
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

### 12. 🚨 **Alerts** (Alert System)
**What it does:**
- View critical alerts
- Alert categories:
  - Performance alerts
  - Risk alerts
  - Deadline alerts
  - Overload alerts
- Alert history and resolution

**Who can access:** Managers and Owners

---

### 13. 📤 **Export** (Data Export)
**What it does:**
- **CSV Export**: Export data in CSV format
  - Projects, Tasks, Employees, Performance, etc.
- **PDF Export**: Generate PDF reports
  - Performance reports
  - Project reports
  - Personal performance summary
- **Email Sharing**: Send reports via email (SMTP config needed)

**Who can access:** Managers and Owners

---

### 14. ⚖️ **Comparison** (Team Comparison)
**What it does:**
- Compare employee performance
- Team performance comparison
- Department comparison
- Visual comparison charts (bar, line, area)
- Performance rankings

**Who can access:** Managers and Owners

---

## 🔄 Complete Workflow: How to Get Performance Data

### Step-by-Step Process:

#### **1. Setup Data (One-Time)**
```
Projects Page → Create Projects
Employees Page → Create Employees
Tasks Page → Create Tasks and Assign to Employees
```

#### **2. Track Work Progress**
```
Tasks Page → Employees update task status
- Status: pending → in_progress → completed
- System tracks completion dates automatically
```

#### **3. Generate Performance Evaluations**
```
Performance Page → 
  1. Select Employee from dropdown
  2. Click "Evaluate Performance"
  3. System calculates:
     - Performance Score
     - Completion Rate
     - On-Time Rate
     - Rank
     - Trend
  4. View performance history chart
  5. Data saved to performance.json
```

#### **4. View Performance Data**
```
Dashboard → Overall team performance
My Dashboard → Personal performance (for employees)
Analytics → Advanced performance analytics
Comparison → Compare team members
```

#### **5. Monitor & Improve**
```
Risks Page → Check for performance risks
Alerts Page → View critical alerts
Feedback Page → Give feedback to improve performance
Goals Page → Set performance goals
```

---

## 🤖 Agentic Framework (12 Agents)

### 1. **TaskAgent**
- Validates task creation
- Automatically assigns tasks
- Sends notifications
- Tracks task completion

### 2. **EnhancedPerformanceAgent**
- Calculates performance scores
- Tracks completion rates
- Monitors on-time delivery
- Ranks employees
- Calculates trends

### 3. **ReportingAgent**
- Generates project reports
- Creates overview reports
- Analyzes team statistics

### 4. **NotificationAgent**
- Sends notifications for:
  - Task assignments
  - Feedback
  - Goals
  - Risks
  - Performance updates

### 5. **RiskDetectionAgent**
- Scans for employee risks
- Detects project risks
- Identifies task risks
- Monitors performance risks

### 6. **AssistantAgent**
- Natural language queries
- AI-powered assistance

### 7. **ExportAgent**
- CSV exports
- PDF generation
- Email sharing

### 8. **GoalAgent**
- Goal creation
- Progress tracking
- Status management

### 9. **FeedbackAgent**
- Feedback creation
- Communication threads
- Status tracking

### 10. **FilteringAgent**
- Advanced filtering
- Sorting capabilities

### 11. **ComparisonAgent**
- Team comparisons
- Performance rankings
- Comparison charts

### 12. **EnhancedAIAgent**
- Performance predictions
- Growth insights
- AI recommendations

---

## 💾 Data Storage

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

---

## 🎨 Theme & Styling

- **Background**: Dark blue (`#0a0e27`)
- **Accent Color**: Teal/Cyan (`#00CED1`)
- **Text**: White/Light gray
- **Cards**: Dark blue with teal borders
- **Charts**: Teal color scheme
- **Modern, professional design**

---

## 🚀 Quick Start Workflow

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

## 📊 Performance Calculation Details

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

## 🔧 Technical Architecture

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with agentic framework
- **Data Storage**: JSON files (can be migrated to database)
- **Authentication**: Supabase (optional) + Local fallback
- **Charts**: Plotly (interactive visualizations)
- **Agents**: 12 specialized agents for automation

---

## 📝 Tips for Best Results

1. **Create Complete Data**: Add employees, projects, and tasks before evaluating performance

2. **Update Task Status**: Keep task statuses current for accurate performance tracking

3. **Set Realistic Deadlines**: On-time completion rate depends on realistic due dates

4. **Regular Evaluations**: Run performance evaluations regularly to track trends

5. **Use Feedback**: Give feedback to help employees improve

6. **Set Goals**: Create goals to motivate and track progress

7. **Monitor Risks**: Check risks page regularly to catch issues early

8. **Export Reports**: Export data for external analysis

---

## 🆘 Troubleshooting

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

---

## 📞 Support

For issues or questions, check:
- `README.md` - Installation and setup
- `components/agents/` - Agent implementations
- `data/` - Data files structure

---

**Happy Performance Tracking! 🚀**


👩‍💻 3. Employee

How many? All other users (could be dozens, hundreds)

Features they can access:
✅ My Dashboard (personal metrics)
✅ Tasks (view assigned only)
✅ Performance (view own performance only)
✅ Feedback (view + ask questions)
✅ Goals (view + update progress if allowed)
✅ Notifications (their own)
✅ Alerts (personal alerts)