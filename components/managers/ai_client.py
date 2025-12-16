"""
AI Client for integrating with AI model APIs
Supports OpenAI, Anthropic Claude, Google Gemini, and other providers
"""
import os
import json
from typing import Dict, Any, Optional, List
from enum import Enum

# Try to import AI libraries
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AIProvider(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    NONE = "none"


class AIClient:
    """Client for AI model APIs"""
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize AI client
        
        Args:
            provider: AI provider name ('openai', 'anthropic', 'gemini', or None for auto-detect)
            model: Model name (e.g., 'gpt-4', 'gpt-3.5-turbo', 'claude-3-opus-20240229', 'gemini-pro')
        """
        self.provider = provider or os.getenv("AI_PROVIDER", "openai").lower()
        self.model = model or os.getenv("AI_MODEL", "gpt-3.5-turbo")
        self.api_key = None
        self.client = None
        self.enabled = os.getenv("USE_AI", "false").lower() == "true"
        
        if not self.enabled:
            return
        
        # Initialize provider-specific client
        if self.provider == AIProvider.OPENAI:
            self._init_openai()
        elif self.provider == AIProvider.ANTHROPIC:
            self._init_anthropic()
        elif self.provider == AIProvider.GEMINI:
            self._init_gemini()
        else:
            # Auto-detect based on available libraries and API keys
            if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
                self.provider = AIProvider.OPENAI
                self._init_openai()
            elif ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
                self.provider = AIProvider.ANTHROPIC
                self._init_anthropic()
            elif GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
                self.provider = AIProvider.GEMINI
                self._init_gemini()
            else:
                self.enabled = False
                print("Warning: No AI provider configured. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY in .env")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        if not OPENAI_AVAILABLE:
            self.enabled = False
            print("Warning: openai library not installed. Install with: pip install openai")
            return
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.enabled = False
            print("Warning: OPENAI_API_KEY not set in environment")
            return
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.provider = AIProvider.OPENAI
    
    def _init_anthropic(self):
        """Initialize Anthropic client"""
        if not ANTHROPIC_AVAILABLE:
            self.enabled = False
            print("Warning: anthropic library not installed. Install with: pip install anthropic")
            return
        
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            self.enabled = False
            print("Warning: ANTHROPIC_API_KEY not set in environment")
            return
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.provider = AIProvider.ANTHROPIC
    
    def _init_gemini(self):
        """Initialize Google Gemini client"""
        if not GEMINI_AVAILABLE:
            self.enabled = False
            print("Warning: google-generativeai library not installed. Install with: pip install google-generativeai")
            return
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self.enabled = False
            print("Warning: GEMINI_API_KEY not set in environment")
            return
        
        genai.configure(api_key=self.api_key)
        self.client = genai
        self.provider = AIProvider.GEMINI
    
    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None, 
             temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        """
        Send chat messages to AI model
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
        
        Returns:
            AI response text or None if error
        """
        if not self.enabled or not self.client:
            return None
        
        try:
            if self.provider == AIProvider.OPENAI:
                return self._chat_openai(messages, system_prompt, temperature, max_tokens)
            elif self.provider == AIProvider.ANTHROPIC:
                return self._chat_anthropic(messages, system_prompt, temperature, max_tokens)
            elif self.provider == AIProvider.GEMINI:
                return self._chat_gemini(messages, system_prompt, temperature, max_tokens)
        except Exception as e:
            print(f"AI API error: {e}")
            return None
    
    def _chat_openai(self, messages: List[Dict[str, str]], system_prompt: Optional[str], 
                     temperature: float, max_tokens: int) -> str:
        """Chat with OpenAI"""
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def _chat_anthropic(self, messages: List[Dict[str, str]], system_prompt: Optional[str],
                       temperature: float, max_tokens: int) -> str:
        """Chat with Anthropic"""
        # Convert messages format for Anthropic
        system_msg = system_prompt or ""
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "user":
                user_messages.append(msg["content"])
            elif msg["role"] == "assistant":
                # Anthropic doesn't support assistant messages in the same way
                # We'll append them as part of the conversation
                pass
        
        message = anthropic.Anthropic().messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_msg if system_msg else None,
            messages=[{"role": "user", "content": "\n".join(user_messages)}]
        )
        return message.content[0].text
    
    def _chat_gemini(self, messages: List[Dict[str, str]], system_prompt: Optional[str],
                     temperature: float, max_tokens: int) -> str:
        """Chat with Google Gemini"""
        # Combine system prompt and messages
        full_prompt = ""
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n"
        
        # Convert messages to text format for Gemini
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                full_prompt += f"User: {content}\n"
            elif role == "assistant":
                full_prompt += f"Assistant: {content}\n"
        
        # Configure generation settings
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        
        # Get the model
        model = self.client.GenerativeModel(
            model_name=self.model,
            generation_config=generation_config
        )
        
        # Generate response
        response = model.generate_content(full_prompt)
        return response.text
    
    def generate_insights(self, data: Dict[str, Any], context: str = "performance") -> Optional[str]:
        """
        Generate AI-powered insights from data
        
        Args:
            data: Data dictionary to analyze
            context: Context for analysis (performance, tasks, risks, etc.)
        
        Returns:
            Generated insights text
        """
        if not self.enabled:
            return None
        
        system_prompts = {
            "performance": "You are an expert HR analyst. Analyze performance data and provide actionable insights.",
            "tasks": "You are a project management expert. Analyze task data and provide recommendations.",
            "risks": "You are a risk management expert. Analyze risk data and provide mitigation strategies.",
            "goals": "You are a goal-setting expert. Analyze goal data and provide guidance.",
            "workload": "You are a workload management expert. Analyze workload data and provide recommendations."
        }
        
        system_prompt = system_prompts.get(context, "You are a business analyst. Analyze the data and provide insights.")
        
        user_prompt = f"Analyze this {context} data and provide key insights and recommendations:\n\n{json.dumps(data, indent=2)}"
        
        messages = [{"role": "user", "content": user_prompt}]
        return self.chat(messages, system_prompt=system_prompt, temperature=0.5, max_tokens=500)
    
    def intelligent_task_assignment(self, task: Dict[str, Any], employees: List[Dict[str, Any]], 
                                   tasks: List[Dict[str, Any]]) -> Optional[str]:
        """
        Use AI to intelligently assign a task to the best employee
        
        Args:
            task: Task to assign
            employees: List of available employees
            tasks: List of all tasks (for workload analysis)
        
        Returns:
            Employee ID of best match, or None
        """
        if not self.enabled:
            return None
        
        # Prepare employee data (skills, workload, performance)
        employee_data = []
        for emp in employees:
            emp_tasks = [t for t in tasks if t.get("assigned_to") == emp.get("id") and t.get("status") != "completed"]
            employee_data.append({
                "id": emp.get("id"),
                "name": emp.get("name"),
                "skills": emp.get("skills", {}),
                "workload": len(emp_tasks),
                "performance_score": self._get_latest_performance(emp.get("id"))
            })
        
        system_prompt = """You are an intelligent task assignment system. Analyze the task requirements and employee capabilities to recommend the best employee for the task. Consider:
1. Employee skills matching task requirements
2. Current workload (prefer employees with lower workload)
3. Performance scores (prefer higher performers)
4. Task priority and deadline

Return ONLY the employee ID of your recommendation, nothing else."""
        
        user_prompt = f"""Task to assign:
{json.dumps(task, indent=2)}

Available employees:
{json.dumps(employee_data, indent=2)}

Recommend the best employee ID for this task."""
        
        messages = [{"role": "user", "content": user_prompt}]
        response = self.chat(messages, system_prompt=system_prompt, temperature=0.3, max_tokens=50)
        
        if response:
            # Extract employee ID from response
            response = response.strip()
            # Try to find employee ID in response
            for emp in employees:
                if emp.get("id") in response or emp.get("name").lower() in response.lower():
                    return emp.get("id")
        
        return None
    
    def _get_latest_performance(self, employee_id: str) -> float:
        """Get latest performance score for employee"""
        # This would typically query the data manager
        # For now, return a default
        return 75.0
    
    def analyze_risk(self, risk_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Use AI to analyze and provide risk mitigation strategies
        
        Args:
            risk_data: Risk data dictionary
        
        Returns:
            Dictionary with analysis and recommendations
        """
        if not self.enabled:
            return None
        
        system_prompt = """You are a risk management expert. Analyze risks and provide:
1. Severity assessment (low/medium/high/critical)
2. Impact analysis
3. Mitigation strategies
4. Recommended actions

Return your analysis as JSON with keys: severity, impact, mitigation_strategies (list), recommended_actions (list)."""
        
        user_prompt = f"Analyze this risk:\n\n{json.dumps(risk_data, indent=2)}"
        
        messages = [{"role": "user", "content": user_prompt}]
        response = self.chat(messages, system_prompt=system_prompt, temperature=0.4, max_tokens=300)
        
        if response:
            try:
                # Try to parse JSON from response
                # AI might return JSON wrapped in markdown code blocks
                if "```json" in response:
                    response = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0].strip()
                
                return json.loads(response)
            except:
                # If JSON parsing fails, return structured text
                return {
                    "analysis": response,
                    "severity": "medium",
                    "mitigation_strategies": [response]
                }
        
        return None
    
    def natural_language_query(self, query: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process natural language query using AI
        
        Args:
            query: User's natural language query
            context: Context data (employees, tasks, projects, etc.)
        
        Returns:
            Dictionary with response and action
        """
        if not self.enabled:
            return None
        
        system_prompt = """You are an AI assistant for an Employee Performance Management System. 
You can help users with:
- Performance queries (scores, evaluations, rankings)
- Task management (assignments, status, deadlines)
- Project information (status, progress, teams)
- Risk detection and mitigation
- Goal tracking and recommendations
- Analytics and reporting

Understand the user's query and provide helpful, accurate responses based on the available data."""
        
        context_str = f"""Available data context:
{json.dumps(context, indent=2)}"""
        
        user_prompt = f"{context_str}\n\nUser query: {query}\n\nProvide a helpful response."
        
        messages = [{"role": "user", "content": user_prompt}]
        response = self.chat(messages, system_prompt=system_prompt, temperature=0.7, max_tokens=500)
        
        if response:
            return {
                "response": response,
                "confidence": 0.8,
                "source": "ai"
            }
        
        return None
    
    def generate_recommendations(self, data_type: str, data: Dict[str, Any]) -> Optional[List[str]]:
        """
        Generate AI-powered recommendations
        
        Args:
            data_type: Type of data (performance, tasks, risks, goals)
            data: Data to analyze
        
        Returns:
            List of recommendation strings
        """
        if not self.enabled:
            return None
        
        system_prompts = {
            "performance": "You are an HR expert. Analyze performance data and provide actionable recommendations for improvement.",
            "tasks": "You are a project management expert. Analyze task data and provide recommendations for better task management.",
            "risks": "You are a risk management expert. Analyze risks and provide mitigation recommendations.",
            "goals": "You are a goal-setting expert. Analyze goals and provide recommendations for goal achievement."
        }
        
        system_prompt = system_prompts.get(data_type, "Analyze the data and provide recommendations.")
        
        user_prompt = f"Analyze this {data_type} data and provide 3-5 specific, actionable recommendations:\n\n{json.dumps(data, indent=2)}"
        
        messages = [{"role": "user", "content": user_prompt}]
        response = self.chat(messages, system_prompt=system_prompt, temperature=0.6, max_tokens=400)
        
        if response:
            # Parse recommendations (usually numbered or bulleted list)
            recommendations = []
            for line in response.split("\n"):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith("-") or line.startswith("*")):
                    # Remove numbering/bullets
                    rec = line.lstrip("0123456789.-* ").strip()
                    if rec:
                        recommendations.append(rec)
            
            return recommendations if recommendations else [response]
        
        return None

