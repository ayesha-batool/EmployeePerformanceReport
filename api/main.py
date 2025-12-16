"""
ScoreSquad Performance API - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.database import init_db
from api.routes import reviews, goals, feedback, skills, analytics, reports, employees, tasks, projects, performances, notifications
from api.routes import dashboard, frontend

# Initialize FastAPI app
app = FastAPI(
    title="ScoreSquad Performance API",
    description="Performance tracking and assessment API for integration with Atlas AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for Atlas integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

# Include routers
app.include_router(reviews.router)
app.include_router(goals.router)
app.include_router(feedback.router)
app.include_router(skills.router)
app.include_router(analytics.router)
app.include_router(reports.router)
app.include_router(employees.router)
app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(performances.router)
app.include_router(notifications.router)
app.include_router(dashboard.router)
app.include_router(frontend.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ScoreSquad Performance API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)


