"""
Event Bus - Event-driven architecture for the system
Replaces rule-based logic with event-driven patterns
"""
from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from datetime import datetime
import json


class EventType(str, Enum):
    """System event types"""
    # Task Events
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_OVERDUE = "task.overdue"
    TASK_ASSIGNED = "task.assigned"
    
    # Performance Events
    PERFORMANCE_EVALUATED = "performance.evaluated"
    PERFORMANCE_LOW = "performance.low"
    PERFORMANCE_HIGH = "performance.high"
    PERFORMANCE_TREND_CHANGED = "performance.trend_changed"
    
    # Goal Events
    GOAL_CREATED = "goal.created"
    GOAL_UPDATED = "goal.updated"
    GOAL_COMPLETED = "goal.completed"
    GOAL_OVERDUE = "goal.overdue"
    GOAL_PROGRESS_UPDATED = "goal.progress_updated"
    
    # Feedback Events
    FEEDBACK_CREATED = "feedback.created"
    FEEDBACK_RESPONDED = "feedback.responded"
    FEEDBACK_UPDATED = "feedback.updated"
    
    # Project Events
    PROJECT_CREATED = "project.created"
    PROJECT_UPDATED = "project.updated"
    PROJECT_COMPLETED = "project.completed"
    PROJECT_HEALTH_CHANGED = "project.health_changed"
    
    # Risk Events
    RISK_DETECTED = "risk.detected"
    RISK_RESOLVED = "risk.resolved"
    RISK_SEVERITY_CHANGED = "risk.severity_changed"
    
    # Notification Events
    NOTIFICATION_SENT = "notification.sent"
    NOTIFICATION_READ = "notification.read"
    
    # Achievement Events
    ACHIEVEMENT_LOGGED = "achievement.logged"
    ACHIEVEMENT_UPDATED = "achievement.updated"
    
    # System Events
    EMPLOYEE_CREATED = "employee.created"
    EMPLOYEE_UPDATED = "employee.updated"
    SYSTEM_STARTED = "system.started"
    SYSTEM_SHUTDOWN = "system.shutdown"


class Event:
    """Event object"""
    
    def __init__(self, event_type: EventType, data: Dict[str, Any], 
                 source: str = "system", timestamp: Optional[datetime] = None):
        self.event_type = event_type
        self.data = data
        self.source = source
        self.timestamp = timestamp or datetime.now()
        self.id = f"{event_type.value}_{self.timestamp.isoformat()}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            "id": self.id,
            "type": self.event_type.value,
            "data": self.data,
            "source": self.source,
            "timestamp": self.timestamp.isoformat()
        }
    
    def __repr__(self):
        return f"Event({self.event_type.value}, {self.data})"


class EventBus:
    """Central event bus for event-driven architecture"""
    
    def __init__(self):
        self.handlers: Dict[EventType, List[Callable]] = {}
        self.event_history: List[Event] = []
        self.max_history = 1000  # Keep last 1000 events
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Subscribe a handler to an event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        print(f"✅ Subscribed handler to {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Unsubscribe a handler from an event type"""
        if event_type in self.handlers:
            try:
                self.handlers[event_type].remove(handler)
            except ValueError:
                pass
    
    def publish(self, event: Event):
        """Publish an event to all subscribed handlers"""
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        # Notify all handlers for this event type
        handlers = self.handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"❌ Error in event handler for {event.event_type.value}: {e}")
    
    def publish_event(self, event_type: EventType, data: Dict[str, Any], 
                     source: str = "system"):
        """Convenience method to create and publish an event"""
        event = Event(event_type, data, source)
        self.publish(event)
        return event
    
    def get_event_history(self, event_type: Optional[EventType] = None, 
                         limit: int = 100) -> List[Event]:
        """Get event history, optionally filtered by type"""
        history = self.event_history.copy()
        if event_type:
            history = [e for e in history if e.event_type == event_type]
        return history[-limit:]
    
    def clear_history(self):
        """Clear event history"""
        self.event_history.clear()


# Global event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get or create global event bus instance"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


def set_event_bus(event_bus: EventBus):
    """Set global event bus instance"""
    global _event_bus
    _event_bus = event_bus

