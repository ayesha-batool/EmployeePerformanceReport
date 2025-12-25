# Architecture Pipeline - Single Diagram

Complete architecture pipeline of the Employee Performance Report System in one comprehensive diagram.

---

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    USER INTERFACE LAYER (Streamlit Frontend)                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Dashboard │ │Projects  │ │Employees │ │  Tasks   │ │  Goals   │ │ Feedback │ │ Reports  │ │  Export  │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
└───────┼────────────┼─────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────┘
        │            │             │            │            │            │            │            │
        └────────────┴─────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              AUTHENTICATION LAYER (AuthManager)                                              │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  • Supabase Auth  • JWT Validation  • Role-based Access (Owner/Manager/Employee)  • Session Mgmt  │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
        ┌──────────────────────┐          ┌──────────────────────────────┐
        │  Direct Mode        │          │   API Mode (USE_API_BACKEND)  │
        │  (Legacy)           │          │                              │
        └──────────┬──────────┘          └──────────────┬───────────────┘
                   │                                     │
                   │                                     ▼
                   │                     ┌─────────────────────────────────────┐
                   │                     │   API CLIENT LAYER                  │
                   │                     │   (APIClient - HTTP/REST)          │
                   │                     └──────────────┬──────────────────────┘
                   │                                     │
                   └─────────────────────┬───────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND API LAYER (FastAPI)                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│  │  Dashboard   │ │  Employees   │ │  Projects    │ │   Tasks     │ │   Reports   │ │   Goals     │    │
│  │  Feedback    │ │  Analytics   │ │  Reviews     │ │ Performances│ │  Skills     │ │Notifications│    │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              AGENTIC FRAMEWORK LAYER                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  1. EnhancedPerformanceAgent  →  ML/AI Performance Scoring, Rankings, Trends                        │  │
│  │  2. ReportingAgent            →  Project Health, Risk Detection, Reports                            │  │
│  │  3. NotificationAgent          →  RL-based Notifications, Personalized Messages                     │  │
│  │  4. GoalAgent                 →  Goal Status (AI-determined), Progress Tracking                     │  │
│  │  5. FeedbackAgent              →  Feedback Analysis, Thread Management                              │  │
│  │  6. ExportAgent                →  CSV/PDF Export, Data Formatting                                    │  │
│  │  7. PromotionAgent             →  Promotion Probability (ML Classification)                          │  │
│  │  8. EventHandlers              →  AI-powered Event Processing (24+ Event Types)                    │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                    EVENT BUS (Event-Driven Architecture)                                │  │
│  │  • Event Publishing  • Event Subscription  • Event History (24+ Types)  • AI-Powered Handlers      │  │
│  │                                                                                                         │  │
│  │  Event Types: TASK_*, PERFORMANCE_*, GOAL_*, FEEDBACK_*, PROJECT_*, RISK_*, NOTIFICATION_*, etc.   │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
        ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
        │   AI CLIENT MANAGER │ │   ML MODELS LAYER    │ │   DATA MANAGER       │
        │   (ai_client.py)    │ │   (components/ml/)   │ │   (data_manager.py)  │
        │                     │ │                     │ │                     │
        │  • OpenAI           │ │  • PerformanceScorer │ │  • CRUD Operations   │
        │  • Gemini           │ │  • NotificationRL    │ │  • Data Validation   │
        │  • Anthropic        │ │  • PredictiveAnalytics│ │  • Query Building   │
        │  • Multi-provider   │ │  • PromotionClassifier│ │  • Transactions      │
        └──────────┬──────────┘ └──────────┬───────────┘ └──────────┬──────────┘
                   │                       │                        │
                   │                       │                        │
                   └───────────────────────┼────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE LAYER (Supabase PostgreSQL)                                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │employees│ │ projects │ │  tasks   │ │performances│ │  goals   │ │ feedback │ │ reviews │ │  skills  │ │
│  │notifications│achievements│metrics  │ │  reports  │ │  (RLS)   │ │  (RLS)   │ │  (RLS)   │ │  (RLS)   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    DATA FLOW & EVENT FLOW

User Action → Frontend → Auth → [Direct/API] → Backend → Agent → Event Bus → [AI/ML/DataManager] → Database
                                                                      │
                                                                      ▼
                                                              Event Handlers
                                                                      │
                                                              Cascade Events
                                                                      │
                                                              Notifications
                                                                      │
                                                              Performance Updates
                                                                      │
                                                              Goal Progress
                                                                      │
                                                                      ▼
                                                              Response → Frontend → User

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    PERFORMANCE EVALUATION PIPELINE

User Request → PerformanceAgent → [Fetch Tasks/Feedback] → [ML Model Check]
                                                                    │
                                    ┌───────────────────────────────┼───────────────────────────────┐
                                    │                               │                               │
                                    ▼                               ▼                               ▼
                            ML Model Trained?              AI Enabled?                    Simple Fallback
                                    │                               │                               │
                                    ▼                               ▼                               ▼
                            PerformanceScorer              AI API Call                    Weighted Formula
                            (Random Forest/XGBoost)        (OpenAI/Gemini/Anthropic)      (Rule-based)
                                    │                               │                               │
                                    └───────────────────────────────┼───────────────────────────────┘
                                                                    │
                                                                    ▼
                                                            Performance Score (0-100)
                                                                    │
                                                                    ▼
                                                            Calculate Rank & Trend
                                                                    │
                                                                    ▼
                                                            Publish PERFORMANCE_EVALUATED Event
                                                                    │
                                                                    ▼
                                                            Event Handlers → Notifications → Reports

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    EVENT-DRIVEN CASCADE EXAMPLE

Task Completed → Event Bus.publish(TASK_COMPLETED)
                            │
                            ├─→ EventHandlers.handle_task_completed()
                            │       │
                            │       ├─→ AI Decision: Update Performance? → PerformanceAgent.evaluate()
                            │       ├─→ AI Decision: Notify Manager? → NotificationAgent.send()
                            │       └─→ AI Decision: Check Goals? → GoalAgent.check_progress()
                            │
                            ├─→ NotificationAgent (RL Model: Should send now?)
                            │       │
                            │       ├─→ AI: Generate personalized message
                            │       └─→ Send notification (in-app/email)
                            │
                            └─→ PerformanceAgent (if triggered)
                                    │
                                    └─→ Re-evaluate → PERFORMANCE_EVALUATED event
                                            │
                                            └─→ Cascade continues...

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    TECHNOLOGY STACK

Frontend:     Streamlit | Plotly | ReportLab
Backend:      FastAPI | Python 3.x | Pydantic
AI/ML:        OpenAI | Gemini | Anthropic | scikit-learn | XGBoost | Prophet
Database:     Supabase PostgreSQL | Row Level Security (RLS)
Auth:         Supabase Auth | JWT Tokens
Architecture: Event-Driven | Agentic Framework | Layered Architecture | Microservices-Ready

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                    KEY FEATURES

✓ 8 Specialized Agents for Automation
✓ 24+ Event Types with AI-Powered Handlers
✓ Hybrid ML/AI Performance Calculation
✓ Event-Driven Architecture (100% Event-Based)
✓ Frontend-Backend Separation (Optional API Mode)
✓ Role-based Access Control (Owner/Manager/Employee)
✓ Real-time Notifications with RL Optimization
✓ Professional PDF Report Generation
✓ Predictive Analytics & Forecasting
✓ MCP Server for External Automation

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## Architecture Summary

**Flow Direction**: Top to Bottom (User → Database)

**Key Layers**:
1. **UI Layer** - Streamlit frontend with 8 pages
2. **Auth Layer** - Supabase authentication with role-based access
3. **API Layer** (Optional) - FastAPI backend with REST endpoints
4. **Agentic Framework** - 8 agents + Event Bus for automation
5. **AI/ML Layer** - Multi-provider AI + ML models
6. **Data Layer** - DataManager for CRUD operations
7. **Database Layer** - Supabase PostgreSQL with RLS

**Architecture Patterns**:
- **Layered Architecture** - Clear separation of concerns
- **Event-Driven** - Decoupled components via Event Bus
- **Agentic Framework** - Specialized autonomous agents
- **Hybrid AI/ML** - ML primary, AI fallback, rules last resort
- **Microservices-Ready** - Scalable and deployable independently
