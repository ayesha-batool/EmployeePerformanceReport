"""
Event Handlers - AI-powered event handlers for event-driven architecture
All handlers use AI for decision-making instead of rules
"""
from typing import Dict, Any
from components.managers.event_bus import Event, EventType, get_event_bus
from components.managers.ai_client import AIClient
from components.managers.data_manager import DataManager
from components.agents.notification_agent import NotificationAgent
from components.agents.performance_agent import EnhancedPerformanceAgent
from components.agents.goal_agent import GoalAgent
from components.agents.feedback_agent import FeedbackAgent
import json


class EventHandlers:
    """AI-powered event handlers"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.ai_client = AIClient()
        self.notification_agent = NotificationAgent(data_manager)
        self.performance_agent = EnhancedPerformanceAgent(data_manager)
        self.goal_agent = GoalAgent(data_manager, self.notification_agent)
        self.feedback_agent = FeedbackAgent(data_manager, self.notification_agent)
        self.event_bus = get_event_bus()
        
        # Register all handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all event handlers"""
        # Task events
        self.event_bus.subscribe(EventType.TASK_CREATED, self.handle_task_created)
        self.event_bus.subscribe(EventType.TASK_UPDATED, self.handle_task_updated)
        self.event_bus.subscribe(EventType.TASK_COMPLETED, self.handle_task_completed)
        self.event_bus.subscribe(EventType.TASK_OVERDUE, self.handle_task_overdue)
        self.event_bus.subscribe(EventType.TASK_ASSIGNED, self.handle_task_assigned)
        
        # Performance events
        self.event_bus.subscribe(EventType.PERFORMANCE_EVALUATED, self.handle_performance_evaluated)
        self.event_bus.subscribe(EventType.PERFORMANCE_LOW, self.handle_performance_low)
        self.event_bus.subscribe(EventType.PERFORMANCE_HIGH, self.handle_performance_high)
        self.event_bus.subscribe(EventType.PERFORMANCE_TREND_CHANGED, self.handle_performance_trend_changed)
        
        # Goal events
        self.event_bus.subscribe(EventType.GOAL_CREATED, self.handle_goal_created)
        self.event_bus.subscribe(EventType.GOAL_UPDATED, self.handle_goal_updated)
        self.event_bus.subscribe(EventType.GOAL_COMPLETED, self.handle_goal_completed)
        self.event_bus.subscribe(EventType.GOAL_OVERDUE, self.handle_goal_overdue)
        self.event_bus.subscribe(EventType.GOAL_PROGRESS_UPDATED, self.handle_goal_progress_updated)
        
        # Feedback events
        self.event_bus.subscribe(EventType.FEEDBACK_CREATED, self.handle_feedback_created)
        self.event_bus.subscribe(EventType.FEEDBACK_RESPONDED, self.handle_feedback_responded)
        
        # Project events
        self.event_bus.subscribe(EventType.PROJECT_CREATED, self.handle_project_created)
        self.event_bus.subscribe(EventType.PROJECT_HEALTH_CHANGED, self.handle_project_health_changed)
        
        # Risk events
        self.event_bus.subscribe(EventType.RISK_DETECTED, self.handle_risk_detected)
        
        print("✅ All event handlers registered")
    
    # Task Event Handlers
    def handle_task_created(self, event: Event):
        """Handle task created event - AI decides what to do"""
        if not self.ai_client.enabled:
            return
        
        task = event.data.get("task", {})
        
        # Use AI to determine if notification is needed
        prompt = f"""A new task was created:
{json.dumps(task, indent=2, default=str)}

Should a notification be sent? Consider: task priority, deadline proximity, assignee workload.

Return JSON: {{"should_notify": true/false, "urgency": "low/medium/high", "message": "personalized message"}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a task management assistant. Decide if notifications are needed.",
                temperature=0.3,
                max_tokens=200
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                if decision.get("should_notify", False):
                    assignee_id = task.get("assigned_to")
                    if assignee_id:
                        self.notification_agent.send_notification(
                            recipient=assignee_id,
                            title="New Task Assigned",
                            message=decision.get("message", f"New task: {task.get('title')}"),
                            notification_type="task_assignment",
                            priority=decision.get("urgency", "medium")
                        )
        except Exception as e:
            print(f"Error in handle_task_created: {e}")
    
    def handle_task_updated(self, event: Event):
        """Handle task updated event - AI analyzes changes"""
        if not self.ai_client.enabled:
            return
        
        task = event.data.get("task", {})
        changes = event.data.get("changes", {})
        
        # Use AI to determine if update is significant
        prompt = f"""Task was updated:
Task: {json.dumps(task, indent=2, default=str)}
Changes: {json.dumps(changes, indent=2, default=str)}

Is this update significant enough to notify? Return JSON: {{"should_notify": true/false, "message": "..."}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a task management assistant. Determine if updates need notifications.",
                temperature=0.3,
                max_tokens=150
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                if decision.get("should_notify", False):
                    assignee_id = task.get("assigned_to")
                    if assignee_id:
                        self.notification_agent.send_notification(
                            recipient=assignee_id,
                            title="Task Updated",
                            message=decision.get("message", "Your task has been updated"),
                            notification_type="task_update"
                        )
        except Exception as e:
            print(f"Error in handle_task_updated: {e}")
    
    def handle_task_completed(self, event: Event):
        """Handle task completed event - AI determines next actions"""
        if not self.ai_client.enabled:
            return
        
        task = event.data.get("task", {})
        employee_id = task.get("assigned_to")
        
        # Use AI to determine if performance should be re-evaluated
        prompt = f"""Task completed:
{json.dumps(task, indent=2, default=str)}

Should performance be re-evaluated? Consider: task importance, completion time, quality.

Return JSON: {{"should_evaluate": true/false, "reason": "..."}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a performance management assistant.",
                temperature=0.3,
                max_tokens=150
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                if decision.get("should_evaluate", False) and employee_id:
                    # Trigger performance evaluation event
                    self.event_bus.publish_event(
                        EventType.PERFORMANCE_EVALUATED,
                        {"employee_id": employee_id, "trigger": "task_completed", "task_id": task.get("id")}
                    )
        except Exception as e:
            print(f"Error in handle_task_completed: {e}")
    
    def handle_task_overdue(self, event: Event):
        """Handle task overdue event - AI determines urgency and actions"""
        if not self.ai_client.enabled:
            return
        
        task = event.data.get("task", {})
        
        # Use AI to determine urgency and actions
        prompt = f"""Task is overdue:
{json.dumps(task, indent=2, default=str)}

Determine urgency and required actions. Return JSON: {{"urgency": "low/medium/high/critical", "actions": ["action1", "action2"], "notify_manager": true/false}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a task management assistant. Determine overdue task urgency.",
                temperature=0.3,
                max_tokens=200
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                assignee_id = task.get("assigned_to")
                
                if assignee_id:
                    self.notification_agent.send_notification(
                        recipient=assignee_id,
                        title=f"⚠️ Overdue Task ({decision.get('urgency', 'medium').upper()})",
                        message=f"Task '{task.get('title')}' is overdue. Actions: {', '.join(decision.get('actions', []))}",
                        notification_type="warning",
                        priority=decision.get("urgency", "medium")
                    )
                
                if decision.get("notify_manager", False):
                    # Notify managers
                    employees = self.data_manager.load_data("employees") or []
                    managers = [e for e in employees if e.get("role") in ["manager", "owner"]]
                    for manager in managers:
                        self.notification_agent.send_notification(
                            recipient=manager.get("id"),
                            title="Overdue Task Alert",
                            message=f"Task '{task.get('title')}' assigned to employee is overdue",
                            notification_type="risk"
                        )
        except Exception as e:
            print(f"Error in handle_task_overdue: {e}")
    
    def handle_task_assigned(self, event: Event):
        """Handle task assigned event"""
        task = event.data.get("task", {})
        assignee_id = task.get("assigned_to")
        
        if assignee_id:
            self.notification_agent.send_notification(
                recipient=assignee_id,
                title="New Task Assigned",
                message=f"Task '{task.get('title')}' has been assigned to you",
                notification_type="task_assignment"
            )
    
    # Performance Event Handlers
    def handle_performance_evaluated(self, event: Event):
        """Handle performance evaluated event - AI determines if alerts needed"""
        if not self.ai_client.enabled:
            return
        
        employee_id = event.data.get("employee_id")
        performance = event.data.get("performance", {})
        score = performance.get("performance_score", 0)
        
        # Use AI to determine if this triggers low/high performance events
        prompt = f"""Performance evaluated:
Employee ID: {employee_id}
Score: {score}
Performance Data: {json.dumps(performance, indent=2, default=str)}

Should this trigger alerts? Return JSON: {{"trigger_low": true/false, "trigger_high": true/false, "reason": "..."}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a performance management assistant. Determine if performance needs attention.",
                temperature=0.3,
                max_tokens=150
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                
                if decision.get("trigger_low", False):
                    self.event_bus.publish_event(
                        EventType.PERFORMANCE_LOW,
                        {"employee_id": employee_id, "performance": performance, "reason": decision.get("reason", "")}
                    )
                
                if decision.get("trigger_high", False):
                    self.event_bus.publish_event(
                        EventType.PERFORMANCE_HIGH,
                        {"employee_id": employee_id, "performance": performance}
                    )
        except Exception as e:
            print(f"Error in handle_performance_evaluated: {e}")
    
    def handle_performance_low(self, event: Event):
        """Handle low performance event - AI generates recommendations"""
        if not self.ai_client.enabled:
            return
        
        employee_id = event.data.get("employee_id")
        performance = event.data.get("performance", {})
        
        # Use AI to generate recommendations
        recommendations = self.ai_client.generate_recommendations("performance", {
            "employee_id": employee_id,
            "performance": performance
        })
        
        if recommendations:
            employees = self.data_manager.load_data("employees") or []
            employee = next((e for e in employees if e.get("id") == employee_id), None)
            managers = [e for e in employees if e.get("role") in ["manager", "owner"]]
            
            message = f"Employee {employee.get('name') if employee else employee_id} has low performance.\n\n"
            message += "AI Recommendations:\n" + "\n".join(f"- {r}" for r in recommendations[:5])
            
            for manager in managers:
                self.notification_agent.send_notification(
                    recipient=manager.get("id"),
                    title="⚠️ Low Performance Alert",
                    message=message,
                    notification_type="warning"
                )
    
    def handle_performance_high(self, event: Event):
        """Handle high performance event - AI determines recognition"""
        if not self.ai_client.enabled:
            return
        
        employee_id = event.data.get("employee_id")
        performance = event.data.get("performance", {})
        
        # Use AI to determine if recognition is needed
        prompt = f"""High performance detected:
Employee ID: {employee_id}
Performance: {json.dumps(performance, indent=2, default=str)}

Should this employee be recognized? Return JSON: {{"should_recognize": true/false, "recognition_type": "..."}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a recognition system. Determine if high performers should be recognized.",
                temperature=0.4,
                max_tokens=150
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                if decision.get("should_recognize", False):
                    # Send recognition notification
                    self.notification_agent.send_notification(
                        recipient=employee_id,
                        title="🌟 Outstanding Performance!",
                        message=f"Your excellent performance has been recognized! {decision.get('recognition_type', '')}",
                        notification_type="achievement"
                    )
        except Exception as e:
            print(f"Error in handle_performance_high: {e}")
    
    def handle_performance_trend_changed(self, event: Event):
        """Handle performance trend changed event"""
        employee_id = event.data.get("employee_id")
        trend = event.data.get("trend", "")
        
        if trend == "declining":
            # Use AI to determine actions
            prompt = f"""Performance trend is declining for employee {employee_id}.
What actions should be taken? Return JSON: {{"actions": ["action1", "action2"], "notify": true/false}}"""
            
            try:
                response = self.ai_client.chat(
                    [{"role": "user", "content": prompt}],
                    system_prompt="You are a performance management assistant.",
                    temperature=0.3,
                    max_tokens=200
                )
                
                if response:
                    decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                    if decision.get("notify", False):
                        employees = self.data_manager.load_data("employees") or []
                        managers = [e for e in employees if e.get("role") in ["manager", "owner"]]
                        for manager in managers:
                            self.notification_agent.send_notification(
                                recipient=manager.get("id"),
                                title="Performance Trend Alert",
                                message=f"Employee performance trend is declining. Actions: {', '.join(decision.get('actions', []))}",
                                notification_type="warning"
                            )
            except Exception as e:
                print(f"Error in handle_performance_trend_changed: {e}")
    
    # Goal Event Handlers
    def handle_goal_created(self, event: Event):
        """Handle goal created event"""
        goal = event.data.get("goal", {})
        employee_id = goal.get("employee_id") or goal.get("user_id")
        
        if employee_id:
            self.notification_agent.send_notification(
                recipient=employee_id,
                title="New Goal Assigned",
                message=f"Goal '{goal.get('title')}' has been assigned to you",
                notification_type="goal_assignment"
            )
    
    def handle_goal_updated(self, event: Event):
        """Handle goal updated event"""
        goal = event.data.get("goal", {})
        # AI can determine if update needs notification
        pass
    
    def handle_goal_completed(self, event: Event):
        """Handle goal completed event - AI determines recognition"""
        if not self.ai_client.enabled:
            return
        
        goal = event.data.get("goal", {})
        employee_id = goal.get("employee_id") or goal.get("user_id")
        
        # Use AI to determine if completion deserves recognition
        prompt = f"""Goal completed:
{json.dumps(goal, indent=2, default=str)}

Should this be recognized? Return JSON: {{"should_recognize": true/false, "message": "..."}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a recognition system.",
                temperature=0.4,
                max_tokens=150
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                if decision.get("should_recognize", False) and employee_id:
                    self.notification_agent.send_notification(
                        recipient=employee_id,
                        title="🎉 Goal Completed!",
                        message=decision.get("message", f"Congratulations on completing '{goal.get('title')}'!"),
                        notification_type="achievement"
                    )
        except Exception as e:
            print(f"Error in handle_goal_completed: {e}")
    
    def handle_goal_overdue(self, event: Event):
        """Handle goal overdue event - AI determines urgency"""
        if not self.ai_client.enabled:
            return
        
        goal = event.data.get("goal", {})
        employee_id = goal.get("employee_id") or goal.get("user_id")
        
        # Use AI to determine urgency and message
        prompt = f"""Goal is overdue:
{json.dumps(goal, indent=2, default=str)}

Determine urgency and create encouraging message. Return JSON: {{"urgency": "low/medium/high", "message": "encouraging message"}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a goal management assistant. Create encouraging messages for overdue goals.",
                temperature=0.5,
                max_tokens=200
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                if employee_id:
                    self.notification_agent.send_notification(
                        recipient=employee_id,
                        title=f"⚠️ Overdue Goal: {goal.get('title')}",
                        message=decision.get("message", f"Goal '{goal.get('title')}' is overdue"),
                        notification_type="warning",
                        priority=decision.get("urgency", "medium")
                    )
        except Exception as e:
            print(f"Error in handle_goal_overdue: {e}")
    
    def handle_goal_progress_updated(self, event: Event):
        """Handle goal progress updated event"""
        goal = event.data.get("goal", {})
        # AI can determine if significant progress update needs notification
        pass
    
    # Feedback Event Handlers
    def handle_feedback_created(self, event: Event):
        """Handle feedback created event"""
        feedback = event.data.get("feedback", {})
        employee_id = feedback.get("employee_id")
        
        if employee_id:
            self.notification_agent.send_notification(
                recipient=employee_id,
                title="New Feedback Received",
                message=f"You have received new feedback: {feedback.get('title', 'Feedback')}",
                notification_type="feedback"
            )
    
    def handle_feedback_responded(self, event: Event):
        """Handle feedback responded event"""
        feedback = event.data.get("feedback", {})
        given_by = feedback.get("given_by") or feedback.get("reviewer_id")
        
        if given_by:
            self.notification_agent.send_notification(
                recipient=given_by,
                title="Feedback Response Received",
                message=f"Employee has responded to your feedback: {feedback.get('title', 'Feedback')}",
                notification_type="feedback_response"
            )
    
    # Project Event Handlers
    def handle_project_created(self, event: Event):
        """Handle project created event"""
        project = event.data.get("project", {})
        # AI can determine if project creation needs notifications
        pass
    
    def handle_project_health_changed(self, event: Event):
        """Handle project health changed event - AI determines if action needed"""
        if not self.ai_client.enabled:
            return
        
        project = event.data.get("project", {})
        health_score = event.data.get("health_score", 100)
        previous_score = event.data.get("previous_score", 100)
        
        # Use AI to determine if health change is concerning
        prompt = f"""Project health changed:
Project: {project.get('name', '')}
Previous Health: {previous_score}
Current Health: {health_score}
Change: {health_score - previous_score}

Is this concerning? Return JSON: {{"is_concerning": true/false, "severity": "low/medium/high", "actions": ["action1"]}}"""
        
        try:
            response = self.ai_client.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are a project management assistant.",
                temperature=0.3,
                max_tokens=200
            )
            
            if response:
                decision = json.loads(response.split("```json")[1].split("```")[0] if "```json" in response else response)
                if decision.get("is_concerning", False):
                    employees = self.data_manager.load_data("employees") or []
                    managers = [e for e in employees if e.get("role") in ["manager", "owner"]]
                    for manager in managers:
                        self.notification_agent.send_notification(
                            recipient=manager.get("id"),
                            title=f"⚠️ Project Health Alert: {project.get('name')}",
                            message=f"Project health changed from {previous_score} to {health_score}. Actions: {', '.join(decision.get('actions', []))}",
                            notification_type="risk",
                            priority=decision.get("severity", "medium")
                        )
        except Exception as e:
            print(f"Error in handle_project_health_changed: {e}")
    
    # Risk Event Handlers
    def handle_risk_detected(self, event: Event):
        """Handle risk detected event - AI analyzes and determines actions"""
        if not self.ai_client.enabled:
            return
        
        risk = event.data.get("risk", {})
        
        # Use AI to analyze risk
        analysis = self.ai_client.analyze_risk(risk)
        
        if analysis:
            employees = self.data_manager.load_data("employees") or []
            managers = [e for e in employees if e.get("role") in ["manager", "owner"]]
            
            message = risk.get("description", "")
            if analysis.get("analysis"):
                message += f"\n\n🤖 AI Analysis:\n{analysis.get('analysis')}"
            if analysis.get("mitigation_strategies"):
                message += f"\n\n💡 Mitigation:\n" + "\n".join(f"- {s}" for s in analysis.get("mitigation_strategies", [])[:3])
            
            for manager in managers:
                self.notification_agent.send_notification(
                    recipient=manager.get("id"),
                    title=f"⚠️ Risk Detected: {risk.get('type', 'Unknown')}",
                    message=message,
                    notification_type="risk",
                    priority=analysis.get("severity", "medium")
                )

