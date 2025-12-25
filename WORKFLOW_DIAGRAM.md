# Workflow Diagram

Complete workflow diagrams for the Employee Performance Report System showing all major processes and user flows.

---

## 1. Authentication & Login Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER LOGIN WORKFLOW                       │
└─────────────────────────────────────────────────────────────────┘

User Opens Application
         │
         ▼
┌────────────────────┐
│  Login Page        │
│  (Streamlit UI)    │
└─────────┬──────────┘
          │
          │ User Enters Credentials
          │ (Email + Password)
          ▼
┌─────────────────────────────────────┐
│  Check: USE_API_BACKEND?           │
│  • true  → API Mode                │
│  • false → Direct Mode              │
└─────────┬───────────────────────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────────┐
│ API     │ │ Direct Auth      │
│ Client  │ │ (AuthManager)     │
└────┬────┘ └────────┬──────────┘
     │               │
     │               ▼
     │      ┌──────────────────────┐
     │      │ Try Supabase Auth    │
     │      │ (if configured)      │
     │      └──────────┬───────────┘
     │                 │
     │                 ▼
     │      ┌──────────────────────┐
     │      │ Fallback: Local Auth │
     │      │ (Hash password)      │
     │      └──────────┬───────────┘
     │                 │
     └─────────────────┘
              │
              ▼
    ┌─────────────────────┐
    │ Authentication      │
    │ Result?             │
    └─────┬───────────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ Success │ │ Failed       │
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │      ┌──────────────┐
     │      │ Show Error   │
     │      │ "Invalid     │
     │      │  credentials" │
     │      └──────────────┘
     │
     ▼
┌─────────────────────┐
│ Set Session State   │
│ • authenticated=true│
│ • user={email, role,│
│   name, id}         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Redirect to         │
│ Dashboard           │
└─────────────────────┘
```

---

## 2. Task Management Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      TASK MANAGEMENT WORKFLOW                    │
└─────────────────────────────────────────────────────────────────┘

User Navigates to Projects Page
         │
         ▼
┌────────────────────┐
│  Projects Page     │
│  (View/Create)     │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ View    │ │ Create Task  │
│ Tasks   │ │              │
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ Fill Form:    │
     │     │ • Title       │
     │     │ • Description │
     │     │ • Priority    │
     │     │ • Due Date    │
     │     │ • Assignee    │
     │     │ • Project     │
     │     └───────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ Save Task    │
     │     │ (DataManager)│
     │     └───────┬───────┘
     │             │
     │             ▼
     │     ┌──────────────────────┐
     │     │ Publish Event:       │
     │     │ TASK_CREATED         │
     │     └───────┬──────────────┘
     │             │
     │             ▼
     │     ┌──────────────────────┐
     │     │ Event Bus            │
     │     │ → Event Handlers     │
     │     │ → NotificationAgent  │
     │     │ → PerformanceAgent   │
     │     └──────────────────────┘
     │
     ▼
┌────────────────────┐
│  Task List View    │
│  • Filter by Status│
│  • Filter by User  │
│  • Edit/Delete     │
└─────────┬──────────┘
          │
          │ User Updates Task Status
          ▼
┌────────────────────┐
│  Update Task       │
│  (Status Change)   │
└─────────┬──────────┘
          │
          ▼
┌──────────────────────┐
│ Check: Status =       │
│ "completed"?         │
└─────┬────────────────┘
      │
  ┌───┴───┐
  │       │
  ▼       ▼
┌─────┐ ┌──────────────────┐
│ Yes │ │ No               │
└──┬──┘ └──────────────────┘
   │
   ▼
┌──────────────────────┐
│ Publish Event:        │
│ TASK_COMPLETED        │
└───────────┬───────────┘
            │
            ▼
┌──────────────────────────────┐
│ Event Cascade:                │
│ 1. EventHandlers              │
│    → AI Decision: Update      │
│       Performance?            │
│ 2. PerformanceAgent           │
│    → Re-evaluate Employee     │
│ 3. NotificationAgent          │
│    → RL: Should notify?      │
│    → Send notification         │
│ 4. GoalAgent                  │
│    → Check goal progress      │
└──────────────────────────────┘
```

---

## 3. Performance Evaluation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   PERFORMANCE EVALUATION WORKFLOW                │
└─────────────────────────────────────────────────────────────────┘

Trigger: User Requests Performance Report OR Task Completed
         │
         ▼
┌────────────────────┐
│ PerformanceAgent   │
│ .evaluate_employee()│
└─────────┬──────────┘
          │
          ▼
┌──────────────────────────────┐
│ Fetch Employee Data           │
│ • Tasks (via DataManager)     │
│ • Feedback (via DataManager)  │
│ • Goals (via GoalAgent)       │
│ • Historical Performance      │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Calculate Basic Metrics      │
│ • Total Tasks                 │
│ • Completed Tasks             │
│ • Completion Rate (%)         │
│ • On-Time Rate (%)            │
│ • Active Tasks Count          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Prepare ML Features           │
│ • Task Quality (0-1)          │
│ • Feedback Sentiment (0-1)    │
│ • Workload Balance (0-1)      │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Check ML Model Status         │
│ models/performance_scorer.pkl │
└─────┬─────────────────────────┘
      │
  ┌───┴───┐
  │       │
  ▼       ▼
┌─────┐ ┌──────────────────────────┐
│ Yes │ │ No (Model Not Trained)   │
└──┬──┘ └──────┬───────────────────┘
   │           │
   │           ▼
   │   ┌───────────────────────┐
   │   │ Check AI Availability │
   │   │ (USE_AI flag)         │
   │   └───────┬───────────────┘
   │           │
   │       ┌───┴───┐
   │       │       │
   │       ▼       ▼
   │   ┌─────┐ ┌──────────────────┐
   │   │ Yes │ │ No               │
   │   └──┬──┘ └───┬───────────────┘
   │      │        │
   │      │        ▼
   │      │   ┌──────────────┐
   │      │   │ Simple       │
   │      │   │ Weighted     │
   │      │   │ Formula      │
   │      │   └──────┬───────┘
   │      │          │
   │      ▼          │
   │ ┌──────────┐   │
   │ │ AI API   │   │
   │ │ Call     │   │
   │ │ (OpenAI/ │   │
   │ │ Gemini/  │   │
   │ │ Claude)  │   │
   │ └────┬─────┘   │
   │      │         │
   └──────┴─────────┘
            │
            ▼
┌──────────────────────────────┐
│ Performance Score (0-100)     │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Calculate Rank                │
│ • Get all performance scores  │
│ • Sort descending             │
│ • Find position               │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Calculate Trend               │
│ • Get historical scores       │
│ • AI Analysis:                │
│   - improving                 │
│   - declining                │
│   - stable                   │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Save Performance Data         │
│ (DataManager.save_data)       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Publish Event:                │
│ PERFORMANCE_EVALUATED         │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Event Handlers:               │
│ • NotificationAgent            │
│   (if low performance)        │
│ • ReportingAgent              │
│   (update reports)            │
│ • GoalAgent                   │
│   (check goal progress)       │
└──────────────────────────────┘
```

---

## 4. Report Generation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      REPORT GENERATION WORKFLOW                  │
└─────────────────────────────────────────────────────────────────┘

User Navigates to Reports Page
         │
         ▼
┌────────────────────┐
│  Reports Page      │
│  (Streamlit UI)    │
└─────────┬──────────┘
          │
          │ User Selects Employee
          ▼
┌────────────────────┐
│  Employee Dropdown │
│  (Role-based)      │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ Preview  │ │ Generate PDF  │
│ Report   │ │              │
└────┬─────┘ └──────┬───────┘
     │              │
     │              ▼
     │      ┌──────────────────┐
     │      │ Professional     │
     │      │ Report Generator │
     │      └──────────┬───────┘
     │                 │
     │                 ▼
     │      ┌──────────────────┐
     │      │ Fetch Data:      │
     │      │ • Employee Info   │
     │      │ • Performance     │
     │      │ • Tasks           │
     │      │ • Goals           │
     │      │ • Feedback       │
     │      └──────────┬───────┘
     │                 │
     │                 ▼
     │      ┌──────────────────┐
     │      │ If Performance   │
     │      │ Not Evaluated:    │
     │      │ → Trigger        │
     │      │   PerformanceAgent│
     │      └──────────┬───────┘
     │                 │
     │                 ▼
     │      ┌──────────────────┐
     │      │ Create PDF       │
     │      │ (ReportLab)      │
     │      │ • Header/Footer  │
     │      │ • Employee Info  │
     │      │ • Performance    │
     │      │   Summary        │
     │      │ • Tasks Summary  │
     │      │   (with Chart)   │
     │      │ • Goals Summary  │
     │      │   (with Chart)   │
     │      │ • Feedback       │
     │      │ • Trends         │
     │      └──────────┬───────┘
     │                 │
     │                 ▼
     │      ┌──────────────────┐
     │      │ Save to          │
     │      │ exports/         │
     │      └──────────┬───────┘
     │                 │
     │                 ▼
     │      ┌──────────────────┐
     │      │ Return PDF File   │
     │      │ → Download Link  │
     │      └──────────────────┘
     │
     ▼
┌────────────────────┐
│  Display Metrics   │
│  • Performance     │
│    Score           │
│  • Completion Rate │
│  • On-Time Rate    │
│  • Rank            │
│  • Trend           │
│  • Tasks Summary   │
│  • Goals Summary   │
│  • Feedback        │
└────────────────────┘
```

---

## 5. Goal Management Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        GOAL MANAGEMENT WORKFLOW                  │
└─────────────────────────────────────────────────────────────────┘

User Navigates to Goals Page
         │
         ▼
┌────────────────────┐
│  Goals Page        │
│  (View/Create)     │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ View    │ │ Create Goal  │
│ Goals   │ │              │
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ Fill Form:    │
     │     │ • Title       │
     │     │ • Description │
     │     │ • Target Date │
     │     │ • Employee    │
     │     │ • Progress %  │
     │     └───────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ Save Goal     │
     │     │ (GoalAgent)   │
     │     └───────┬───────┘
     │             │
     │             ▼
     │     ┌──────────────────┐
     │     │ Publish Event:    │
     │     │ GOAL_CREATED      │
     │     └───────┬───────────┘
     │             │
     │             ▼
     │     ┌──────────────────┐
     │     │ Event Handlers   │
     │     │ → Notification   │
     │     └──────────────────┘
     │
     │ User Updates Goal Progress
     ▼
┌────────────────────┐
│  Update Progress   │
│  (0-100%)          │
└─────────┬──────────┘
          │
          ▼
┌──────────────────────┐
│ GoalAgent            │
│ .update_progress()   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│ AI-Determined Goal Status    │
│ • active                      │
│ • completed                   │
│ • overdue                     │
│ • at_risk                     │
│ • on_hold                     │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ ML-Based Progress Trend      │
│ Analysis                      │
│ • Analyze progress pattern    │
│ • Predict completion date     │
│ • Auto-adjust if needed       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Publish Event:                │
│ GOAL_PROGRESS_UPDATED         │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Check: Progress = 100%?      │
└─────┬────────────────────────┘
      │
  ┌───┴───┐
  │       │
  ▼       ▼
┌─────┐ ┌──────┐
│ Yes │ │ No   │
└──┬──┘ └──────┘
   │
   ▼
┌──────────────────────────────┐
│ Publish Event:                │
│ GOAL_COMPLETED                │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Event Handlers:               │
│ • NotificationAgent            │
│   (congratulate employee)     │
│ • PerformanceAgent            │
│   (update performance)        │
│ • ReportingAgent              │
│   (update reports)            │
└──────────────────────────────┘
```

---

## 6. Feedback Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         FEEDBACK WORKFLOW                       │
└─────────────────────────────────────────────────────────────────┘

User Navigates to Feedback Page
         │
         ▼
┌────────────────────┐
│  Feedback Page     │
│  (Role-based View) │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ Manager │ │ Employee     │
│ View    │ │ View         │
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ View Received │
     │     │ Feedback      │
     │     │ • Ask Question│
     │     │ • View Thread │
     │     └───────────────┘
     │
     ▼
┌────────────────────┐
│  Create Feedback   │
│  (Manager Only)    │
└─────────┬──────────┘
          │
          ▼
┌──────────────────────────────┐
│ Fill Form:                   │
│ • Employee                   │
│ • Category                   │
│ • Rating (1-5)               │
│ • Message                    │
│ • Type (positive/negative)  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ FeedbackAgent                 │
│ .create_feedback()            │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ AI-Powered Analysis          │
│ • Sentiment Analysis          │
│ • Extract Key Points         │
│ • Generate Summary           │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Save Feedback                 │
│ (DataManager)                 │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Publish Event:                │
│ FEEDBACK_CREATED               │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Event Handlers:               │
│ • NotificationAgent            │
│   (notify employee)           │
│ • PerformanceAgent            │
│   (update sentiment score)    │
└──────────────────────────────┘
           │
           │ Employee Responds
           ▼
┌──────────────────────────────┐
│ FeedbackAgent                 │
│ .respond_to_feedback()        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Update Thread                 │
│ (Conversation History)        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Publish Event:                │
│ FEEDBACK_RESPONDED            │
└──────────────────────────────┘
```

---

## 7. Event-Driven Workflow (Complete Cascade)

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN WORKFLOW CASCADE                 │
└─────────────────────────────────────────────────────────────────┘

Action Occurs (e.g., Task Completed)
         │
         ▼
┌────────────────────┐
│ Agent Publishes    │
│ Event to Event Bus │
└─────────┬──────────┘
          │
          ▼
┌──────────────────────────────┐
│ Event Bus Processing         │
│ • Store in Event History      │
│ • Find Subscribed Handlers    │
│ • Dispatch to All Handlers    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ EventHandlers                 │
│ .handle_[event_type]()        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ AI Decision Making            │
│ • Should notify?             │
│ • Should update performance?  │
│ • Should check goals?         │
│ • Should send alert?          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Execute Actions Based on      │
│ AI Decisions                  │
└──────────┬───────────────────┘
           │
           ├─────────────────────────────────┐
           │                                 │
           ▼                                 ▼
┌──────────────────────┐        ┌──────────────────────┐
│ NotificationAgent    │        │ PerformanceAgent    │
│ • RL Model:          │        │ • Re-evaluate       │
│   Should send now?   │        │ • Update score      │
│ • AI: Generate       │        │ • Publish           │
│   message            │        │   PERFORMANCE_      │
│ • Send notification  │        │   EVALUATED          │
└──────────┬───────────┘        └──────────┬─────────┘
           │                                │
           │                                │
           ▼                                ▼
┌──────────────────────┐        ┌──────────────────────┐
│ GoalAgent            │        │ ReportingAgent       │
│ • Check progress     │        │ • Update reports      │
│ • Update status      │        │ • Calculate health    │
│ • Publish            │        │ • Detect risks        │
│   GOAL_PROGRESS_     │        │ • Publish             │
│   UPDATED            │        │   PROJECT_HEALTH_    │
└──────────┬───────────┘        │   CHANGED             │
           │                    └───────────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Cascade Continues...          │
│ New Events → New Handlers      │
│ → More Actions                 │
└──────────────────────────────┘
```

---

## 8. Complete User Journey Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      COMPLETE USER JOURNEY                       │
└─────────────────────────────────────────────────────────────────┘

Start: User Opens Application
         │
         ▼
┌────────────────────┐
│  Login Page        │
│  → Authenticate    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Dashboard         │
│  → View Metrics    │
│  → View Charts     │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ Manager │ │ Employee     │
│ Flow    │ │ Flow         │
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ View My Tasks │
     │     │ → Update      │
     │     │   Status      │
     │     └───────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ View My Goals │
     │     │ → Update      │
     │     │   Progress    │
     │     └───────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ View Feedback │
     │     │ → Respond     │
     │     └───────┬───────┘
     │             │
     │             ▼
     │     ┌───────────────┐
     │     │ Generate      │
     │     │ Performance   │
     │     │ Report        │
     │     └───────┬───────┘
     │             │
     │             └──────────────┐
     │                            │
     ▼                            │
┌───────────────┐                │
│ Create Project│                │
│ → Add Tasks   │                │
│ → Assign      │                │
└───────┬───────┘                │
        │                         │
        ▼                         │
┌───────────────┐                │
│ Manage        │                │
│ Employees     │                │
│ → Add/Edit    │                │
│ → Delete      │                │
└───────┬───────┘                │
        │                         │
        ▼                         │
┌───────────────┐                │
│ Create Goals  │                │
│ → Track       │                │
│ → Update      │                │
└───────┬───────┘                │
        │                         │
        ▼                         │
┌───────────────┐                │
│ Give Feedback │                │
│ → Respond     │                │
│ → Track       │                │
└───────┬───────┘                │
        │                         │
        ▼                         │
┌───────────────┐                │
│ Generate      │                │
│ Reports       │                │
│ → PDF Export  │                │
│ → Analytics   │                │
└───────┬───────┘                │
        │                         │
        └─────────────────────────┘
                    │
                    ▼
        ┌──────────────────────┐
        │  Event-Driven        │
        │  Processing          │
        │  → Notifications     │
        │  → Performance       │
        │    Updates           │
        │  → Goal Tracking     │
        │  → Reports           │
        └──────────────────────┘
```

---

## Summary

**Key Workflow Characteristics:**

1. **Authentication Flow**: Secure login with Supabase + local fallback
2. **Task Management**: Create → Update → Complete → Event Cascade
3. **Performance Evaluation**: Data Collection → ML/AI Calculation → Storage → Events
4. **Report Generation**: Data Fetch → PDF Creation → Download
5. **Goal Management**: Create → Track → Update → AI Status → Events
6. **Feedback System**: Create → AI Analysis → Respond → Thread Management
7. **Event-Driven**: Action → Event → AI Decision → Multiple Handlers → Cascade
8. **User Journey**: Role-based flows with different capabilities

**Workflow Features:**
- ✅ Role-based access control
- ✅ Event-driven architecture
- ✅ AI-powered decision making
- ✅ ML model integration
- ✅ Real-time notifications
- ✅ Automated performance tracking
- ✅ Comprehensive reporting

