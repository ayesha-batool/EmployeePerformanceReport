"""
Reinforcement Learning for Notification Agent
Learns when and how often notifications are effective
Stops spamming automatically
"""
import numpy as np
from typing import Dict, Any, Optional, List
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import gym
    from stable_baselines3 import PPO, DQN
    from stable_baselines3.common.env_util import make_vec_env
    RL_AVAILABLE = True
except ImportError:
    RL_AVAILABLE = False
    print("⚠️ stable-baselines3 not available. Using simple Q-learning. Install with: pip install stable-baselines3")


class NotificationRL:
    """Reinforcement Learning agent for notification optimization"""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95):
        """
        Initialize RL agent
        
        Args:
            learning_rate: Learning rate for Q-learning
            discount_factor: Discount factor for future rewards
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        
        # Q-table: state -> action -> Q-value
        # State: (notification_type, time_since_last, urgency_level, user_response_rate)
        # Action: (send, don't_send, delay)
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # Track notification history
        self.notification_history = []
        self.user_responses = defaultdict(list)  # user_id -> list of (notification_id, responded, time)
        
        # Statistics
        self.stats = {
            "total_notifications": 0,
            "effective_notifications": 0,
            "ignored_notifications": 0,
            "spam_prevented": 0
        }
    
    def get_state(self, notification_data: Dict[str, Any]) -> tuple:
        """
        Get state representation
        
        State features:
        1. Notification type (encoded)
        2. Time since last notification to this user (hours)
        3. Urgency level (0=low, 1=medium, 2=high)
        4. User response rate (0-1)
        """
        user_id = notification_data.get("recipient", "")
        notification_type = notification_data.get("type", "general")
        urgency = notification_data.get("priority", "medium")
        
        # Time since last notification
        user_notifications = [n for n in self.notification_history 
                            if n.get("recipient") == user_id]
        if user_notifications:
            last_notification = user_notifications[-1]
            last_time = datetime.fromisoformat(last_notification.get("timestamp", datetime.now().isoformat()))
            hours_since = (datetime.now() - last_time).total_seconds() / 3600
        else:
            hours_since = 24.0  # Default: 24 hours
        
        # User response rate
        user_responses = self.user_responses.get(user_id, [])
        if user_responses:
            responded_count = sum(1 for r in user_responses if r.get("responded", False))
            response_rate = responded_count / len(user_responses)
        else:
            response_rate = 0.5  # Default: 50%
        
        # Encode notification type
        type_encoding = {
            "task_assignment": 0,
            "task_update": 1,
            "deadline_reminder": 2,
            "warning": 3,
            "achievement": 4,
            "feedback": 5,
            "general": 6
        }.get(notification_type, 6)
        
        # Encode urgency
        urgency_encoding = {"low": 0, "medium": 1, "high": 2, "critical": 3}.get(urgency, 1)
        
        # Discretize hours_since (0-6 hours = 0, 6-12 = 1, 12-24 = 2, >24 = 3)
        if hours_since <= 6:
            hours_bucket = 0
        elif hours_since <= 12:
            hours_bucket = 1
        elif hours_since <= 24:
            hours_bucket = 2
        else:
            hours_bucket = 3
        
        # Discretize response rate (0-0.3 = 0, 0.3-0.6 = 1, 0.6-1.0 = 2)
        if response_rate <= 0.3:
            response_bucket = 0
        elif response_rate <= 0.6:
            response_bucket = 1
        else:
            response_bucket = 2
        
        return (type_encoding, hours_bucket, urgency_encoding, response_bucket)
    
    def get_action(self, state: tuple, epsilon: float = 0.1) -> str:
        """
        Get action using epsilon-greedy policy
        
        Actions:
        - "send": Send notification immediately
        - "delay": Delay notification (send later)
        - "skip": Don't send notification
        """
        # Epsilon-greedy: explore with probability epsilon
        if np.random.random() < epsilon:
            return np.random.choice(["send", "delay", "skip"])
        
        # Get Q-values for this state
        q_values = {
            "send": self.q_table[state]["send"],
            "delay": self.q_table[state]["delay"],
            "skip": self.q_table[state]["skip"]
        }
        
        # Return action with highest Q-value
        return max(q_values, key=q_values.get)
    
    def update_q_value(self, state: tuple, action: str, reward: float, next_state: Optional[tuple] = None):
        """
        Update Q-value using Q-learning
        
        Q(s,a) = Q(s,a) + α[r + γ * max(Q(s',a')) - Q(s,a)]
        """
        current_q = self.q_table[state][action]
        
        if next_state:
            # Get max Q-value for next state
            next_q_values = [
                self.q_table[next_state]["send"],
                self.q_table[next_state]["delay"],
                self.q_table[next_state]["skip"]
            ]
            max_next_q = max(next_q_values)
        else:
            max_next_q = 0
        
        # Update Q-value
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def should_send_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide if notification should be sent
        
        Returns:
            {
                "should_send": bool,
                "action": "send" | "delay" | "skip",
                "reason": str,
                "confidence": float
            }
        """
        state = self.get_state(notification_data)
        action = self.get_action(state, epsilon=0.1)  # Low epsilon for exploitation
        
        # Get Q-values for confidence
        q_values = {
            "send": self.q_table[state]["send"],
            "delay": self.q_table[state]["delay"],
            "skip": self.q_table[state]["skip"]
        }
        max_q = max(q_values.values())
        min_q = min(q_values.values())
        confidence = (max_q - min_q) / (max_q - min_q + 1e-6) if max_q != min_q else 0.5
        
        # Check for spam prevention
        user_id = notification_data.get("recipient", "")
        recent_notifications = [
            n for n in self.notification_history[-10:]
            if n.get("recipient") == user_id
            and (datetime.now() - datetime.fromisoformat(n.get("timestamp", datetime.now().isoformat()))).total_seconds() < 3600
        ]
        
        if len(recent_notifications) >= 3 and action == "send":
            # Too many recent notifications - prevent spam
            action = "delay"
            self.stats["spam_prevented"] += 1
        
        reasons = {
            "send": "Notification is likely to be effective",
            "delay": "Too many recent notifications or low response rate",
            "skip": "Notification unlikely to be effective"
        }
        
        return {
            "should_send": action == "send",
            "action": action,
            "reason": reasons.get(action, "Unknown"),
            "confidence": confidence
        }
    
    def record_notification(self, notification_data: Dict[str, Any], sent: bool):
        """Record that a notification was sent"""
        if sent:
            notification_data["timestamp"] = datetime.now().isoformat()
            self.notification_history.append(notification_data)
            self.stats["total_notifications"] += 1
    
    def record_response(self, user_id: str, notification_id: str, responded: bool, response_time: float):
        """
        Record user response to notification
        
        Args:
            user_id: User who received notification
            notification_id: Notification ID
            responded: Whether user responded/acted on notification
            response_time: Time to respond in seconds
        """
        self.user_responses[user_id].append({
            "notification_id": notification_id,
            "responded": responded,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
        
        if responded:
            self.stats["effective_notifications"] += 1
        else:
            self.stats["ignored_notifications"] += 1
    
    def calculate_reward(self, notification_data: Dict[str, Any], responded: bool, response_time: float) -> float:
        """
        Calculate reward for RL learning
        
        Reward:
        - +1.0 if user responded quickly (< 1 hour)
        - +0.5 if user responded slowly (> 1 hour)
        - -0.5 if user didn't respond but notification was important
        - -1.0 if user didn't respond and notification was spam
        """
        if responded:
            if response_time < 3600:  # < 1 hour
                return 1.0
            else:
                return 0.5
        else:
            urgency = notification_data.get("priority", "medium")
            if urgency in ["high", "critical"]:
                return -0.5  # Important but ignored
            else:
                return -1.0  # Spam
    
    def learn_from_feedback(self, notification_data: Dict[str, Any], responded: bool, response_time: float):
        """Learn from user feedback"""
        state = self.get_state(notification_data)
        action = "send"  # Assume we sent it (could track actual action)
        
        reward = self.calculate_reward(notification_data, responded, response_time)
        
        # Update Q-value
        self.update_q_value(state, action, reward)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        total = self.stats["total_notifications"]
        if total > 0:
            effectiveness = self.stats["effective_notifications"] / total
        else:
            effectiveness = 0.0
        
        return {
            **self.stats,
            "effectiveness_rate": effectiveness,
            "q_table_size": len(self.q_table),
            "users_tracked": len(self.user_responses)
        }
    
    def save_model(self, path: str = "models/notification_rl.pkl"):
        """Save Q-table and statistics"""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        
        model_data = {
            "q_table": dict(self.q_table),
            "stats": self.stats,
            "user_responses": dict(self.user_responses)
        }
        
        with open(path, "wb") as f:
            import pickle
            pickle.dump(model_data, f)
    
    def load_model(self, path: str = "models/notification_rl.pkl"):
        """Load Q-table and statistics"""
        try:
            with open(path, "rb") as f:
                import pickle
                model_data = pickle.load(f)
            
            self.q_table = defaultdict(lambda: defaultdict(float), model_data.get("q_table", {}))
            self.stats = model_data.get("stats", self.stats)
            self.user_responses = defaultdict(list, model_data.get("user_responses", {}))
        except Exception as e:
            print(f"❌ Error loading RL model: {e}")

