# Workflow Diagram

Complete unified workflow diagram for the Employee Performance Report System.

---

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    EMPLOYEE PERFORMANCE REPORT SYSTEM                                        │
│                                         COMPLETE WORKFLOW DIAGRAM                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        1. USER AUTHENTICATION                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

User Opens Application
         │
         ▼
┌────────────────────┐
│  Login Page        │
│  (Enter Email/Pass) │
└─────────┬──────────┘
          │
          ▼
┌──────────────────────────────┐
│  Authentication Check         │
│  • Supabase Auth (Primary)    │
│  • Local Auth (Fallback)     │
└──────────┬───────────────────┘
           │
      ┌────┴────┐
      │         │
      ▼         ▼
┌─────────┐ ┌──────────────┐
│ Success │ │ Failed       │
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │      ┌──────────────┐
     │      │ Show Error   │
     │      │ Return to    │
     │      │ Login        │
     │      └──────────────┘
     │
     ▼
┌────────────────────┐
│  Set Session      │
│  • authenticated  │
│  • user (role)    │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        2. MAIN DASHBOARD                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────┐
│  Dashboard         │
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
     │     │ View My Data   │
     │     │ • Tasks        │
     │     │ • Goals        │
     │     │ • Performance  │
     │     │ • Feedback     │
     │     └───────┬───────┘
     │             │
     │             └──────────────┐
     │                            │
     ▼                            │
┌────────────────────┐            │
│  Manager Actions   │            │
│  • Projects        │            │
│  • Employees       │            │
│  • Reports         │            │
│  • Goals           │            │
│  • Feedback        │            │
└─────────┬──────────┘            │
          │                        │
          └────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        3. TASK MANAGEMENT                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

User Creates/Updates Task
         │
         ▼
┌────────────────────┐
│  Task Form         │
│  • Title           │
│  • Description     │
│  • Priority        │
│  • Due Date        │
│  • Assignee        │
│  • Project         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Save Task         │
│  (DataManager)     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Publish Event:    │
│  TASK_CREATED/     │
│  TASK_UPDATED      │
└─────────┬──────────┘
          │
          │ Task Status = "completed"?
          ▼
┌────────────────────┐
│  Publish Event:    │
│  TASK_COMPLETED    │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        4. EVENT-DRIVEN PROCESSING                                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────┐
│  Event Bus         │
│  • Receive Event   │
│  • Store History   │
│  • Find Handlers   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Event Handlers    │
│  (AI-Powered)      │
└─────────┬──────────┘
          │
          ├─────────────────────────────────────────────────────────────┐
          │                                                               │
          ▼                                                               ▼
┌────────────────────┐                                        ┌────────────────────┐
│ AI Decision:       │                                        │ AI Decision:        │
│ Update Performance?│                                        │ Send Notification?  │
└─────────┬──────────┘                                        └─────────┬──────────┘
          │                                                              │
          ▼                                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        5. PERFORMANCE EVALUATION                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────┐
│ PerformanceAgent   │
│ .evaluate_employee()│
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Fetch Data         │
│  • Tasks            │
│  • Feedback         │
│  • Goals            │
│  • History          │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Calculate Metrics  │
│  • Completion Rate  │
│  • On-Time Rate     │
│  • Task Quality     │
│  • Workload         │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Performance Score Calculation       │
│                                      │
│  ┌──────────────────────────────┐  │
│  │ Check ML Model Status        │  │
│  └───────┬──────────────────────┘  │
│          │                          │
│      ┌───┴───┐                      │
│      │       │                      │
│      ▼       ▼                      │
│  ┌─────┐ ┌──────────────────┐      │
│  │ Yes │ │ No               │      │
│  └──┬──┘ └───┬───────────────┘      │
│     │        │                      │
│     │        ▼                      │
│     │   ┌──────────────┐            │
│     │   │ Check AI     │            │
│     │   │ Available?   │            │
│     │   └───┬──────────┘            │
│     │       │                       │
│     │   ┌───┴───┐                   │
│     │   │       │                   │
│     │   ▼       ▼                   │
│     │ ┌─────┐ ┌──────────────┐     │
│     │ │ Yes │ │ No            │     │
│     │ └──┬──┘ └───┬───────────┘     │
│     │    │        │                  │
│     │    │        ▼                  │
│     │    │   ┌──────────────┐        │
│     │    │   │ Simple       │        │
│     │    │   │ Formula      │        │
│     │    │   └──────┬───────┘        │
│     │    │          │                │
│     │    ▼          │                │
│     │ ┌──────────┐  │                │
│     │ │ AI API   │  │                │
│     │ │ Call     │  │                │
│     │ └────┬─────┘  │                │
│     │      │        │                │
│     └──────┴────────┘                │
│            │                         │
│            ▼                         │
│  ┌──────────────────────┐           │
│  │ Performance Score     │           │
│  │ (0-100)               │           │
│  └──────────┬────────────┘           │
│             │                        │
│             ▼                        │
│  ┌──────────────────────┐           │
│  │ Calculate Rank &     │           │
│  │ Trend (AI Analysis)   │           │
│  └──────────┬────────────┘           │
│             │                        │
│             ▼                        │
│  ┌──────────────────────┐           │
│  │ Save Performance      │           │
│  │ (DataManager)         │           │
│  └──────────┬────────────┘           │
│             │                        │
│             ▼                        │
│  ┌──────────────────────┐           │
│  │ Publish Event:        │           │
│  │ PERFORMANCE_EVALUATED  │           │
│  └───────────────────────┘           │
└──────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        6. NOTIFICATION SYSTEM                                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────┐
│ NotificationAgent  │
│ (RL Model Check)   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Should Send?      │
│  (RL Decision)     │
└─────────┬──────────┘
          │
      ┌───┴───┐
      │       │
      ▼       ▼
┌─────────┐ ┌──────────────┐
│ Yes     │ │ No (Delay/   │
│         │ │ Skip)        │
└────┬────┘ └──────────────┘
     │
     ▼
┌────────────────────┐
│  AI Generate        │
│  Message            │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Send Notification │
│  • In-app          │
│  • Email (optional)│
└─────────┬──────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        7. GOAL MANAGEMENT                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

User Creates/Updates Goal
         │
         ▼
┌────────────────────┐
│  GoalAgent         │
│  • Save Goal       │
│  • Track Progress  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  AI-Determined      │
│  Goal Status       │
│  • active          │
│  • completed       │
│  • overdue         │
│  • at_risk         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  ML Progress Trend │
│  Analysis          │
│  • Predict         │
│  • Auto-adjust     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Publish Event:    │
│  GOAL_PROGRESS_     │
│  UPDATED/           │
│  GOAL_COMPLETED     │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        8. FEEDBACK SYSTEM                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Manager Creates Feedback
         │
         ▼
┌────────────────────┐
│  FeedbackAgent     │
│  • Save Feedback   │
│  • AI Analysis     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  AI Sentiment       │
│  Analysis           │
│  • Extract Points   │
│  • Generate Summary  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Publish Event:    │
│  FEEDBACK_CREATED   │
└─────────┬──────────┘
          │
          │ Employee Responds
          ▼
┌────────────────────┐
│  Update Thread     │
│  (Conversation)     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Publish Event:    │
│  FEEDBACK_RESPONDED│
└─────────┬──────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        9. REPORT GENERATION                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

User Requests Report
         │
         ▼
┌────────────────────┐
│  Select Employee   │
│  (Role-based)      │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ Preview │ │ Generate PDF  │
│ Report  │ │              │
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │     ┌──────────────────┐
     │     │ Fetch All Data    │
     │     │ • Performance     │
     │     │ • Tasks           │
     │     │ • Goals           │
     │     │ • Feedback        │
     │     └──────────┬────────┘
     │                │
     │                ▼
     │     ┌──────────────────┐
     │     │ Create PDF        │
     │     │ (ReportLab)       │
     │     │ • Header/Footer   │
     │     │ • Charts          │
     │     │ • Summary         │
     │     └──────────┬────────┘
     │                │
     │                ▼
     │     ┌──────────────────┐
     │     │ Save to exports/  │
     │     │ → Download Link   │
     │     └───────────────────┘
     │
     ▼
┌────────────────────┐
│  Display Metrics   │
│  • Performance     │
│  • Trends          │
│  • Charts          │
└────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    EVENT CASCADE FLOW

Any Action (Task/Goal/Feedback/Performance)
         │
         ▼
┌────────────────────┐
│  Event Published   │
│  to Event Bus      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Event Handlers     │
│  (AI-Powered)      │
│  • Make Decisions  │
│  • Trigger Actions  │
└─────────┬──────────┘
          │
          ├──────────────┬──────────────┬──────────────┬──────────────┐
          │              │              │              │              │
          ▼              ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Performance  │ │ Notification │ │ Goal         │ │ Reporting    │ │ Export       │
│ Agent        │ │ Agent        │ │ Agent        │ │ Agent        │ │ Agent        │
│              │ │              │ │              │ │              │ │              │
│ • Re-evaluate│ │ • RL Check   │ │ • Check      │ │ • Update     │ │ • Generate   │
│ • Update     │ │ • Generate   │ │   Progress   │ │   Reports    │ │   CSV/PDF    │
│ • Rank       │ │   Message    │ │ • Update     │ │ • Health     │ │              │
│              │ │ • Send       │ │   Status     │ │   Score      │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                 │                │                │
       │                │                 │                │                │
       └────────────────┴─────────────────┴────────────────┴────────────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │  New Events        │
                          │  Published         │
                          │  (Cascade)         │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │  Cycle Continues   │
                          │  (Event-Driven)    │
                          └────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    DATA FLOW SUMMARY

User Action
    │
    ▼
Frontend (Streamlit)
    │
    ▼
[API Mode] → FastAPI Backend → Agents
[Direct Mode] → Agents Directly
    │
    ▼
Event Bus → Event Handlers (AI-Powered)
    │
    ├─→ PerformanceAgent → ML/AI → Performance Score
    ├─→ NotificationAgent → RL Model → Notifications
    ├─→ GoalAgent → AI Status → Goal Updates
    ├─→ FeedbackAgent → AI Analysis → Feedback Processing
    ├─→ ReportingAgent → Reports & Analytics
    └─→ ExportAgent → CSV/PDF Generation
    │
    ▼
DataManager → Supabase Database
    │
    ▼
Response → Frontend → User

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    KEY WORKFLOW FEATURES

✓ Authentication: Supabase + Local Fallback
✓ Role-Based Access: Owner/Manager/Employee
✓ Event-Driven: All actions trigger events
✓ AI-Powered: Decisions made by AI, not rules
✓ ML Integration: Performance scoring with ML models
✓ Real-Time: Notifications and updates
✓ Automated: Performance tracking, goal monitoring
✓ Comprehensive: Full CRUD operations
✓ Reporting: PDF generation with charts
✓ Analytics: Performance trends and insights

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## Workflow Summary

**Main Flow:**
1. **Authentication** → User logs in (Supabase/Local)
2. **Dashboard** → Role-based view of data
3. **Task Management** → Create/Update/Complete tasks
4. **Event Processing** → Events trigger AI-powered handlers
5. **Performance Evaluation** → ML/AI calculates performance scores
6. **Notifications** → RL model decides when to notify
7. **Goal Management** → AI determines goal status
8. **Feedback System** → AI analyzes feedback sentiment
9. **Report Generation** → PDF reports with charts

**Event Cascade:**
- Every action publishes events
- Events trigger multiple AI-powered handlers
- Handlers make intelligent decisions
- New events cascade to other handlers
- Complete automation and real-time updates

**Technology Integration:**
- **ML Models**: Performance scoring, trend analysis
- **AI APIs**: Decision making, message generation
- **RL Model**: Notification optimization
- **Event Bus**: Decoupled architecture
- **Supabase**: Data persistence
