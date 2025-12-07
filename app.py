"""
Employee Performance Report System - Streamlit Application
Comprehensive employee performance tracking with agentic framework
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

# Import all managers and agents
from components.managers.data_manager import DataManager
from components.managers.auth_manager import AuthManager
from components.agents.task_agent import TaskAgent
from components.agents.performance_agent import EnhancedPerformanceAgent
from components.agents.reporting_agent import ReportingAgent
from components.agents.notification_agent import NotificationAgent
from components.agents.risk_agent import RiskDetectionAgent
from components.agents.assistant_agent import AssistantAgent
from components.agents.export_agent import ExportAgent
from components.agents.goal_agent import GoalAgent
from components.agents.feedback_agent import FeedbackAgent
from components.agents.filtering_agent import FilteringAgent
from components.agents.comparison_agent import ComparisonAgent
from components.agents.enhanced_ai_agent import EnhancedAIAgent
from components.agents.achievement_agent import AchievementAgent
from components.agents.predictive_analytics_agent import PredictiveAnalyticsAgent
from components.agents.correlation_agent import CorrelationAgent
from components.agents.skill_agent import SkillAgent
from components.agents.workload_agent import WorkloadAgent
from components.agents.attendance_agent import AttendanceAgent
from components.agents.engagement_agent import EngagementAgent
from components.agents.promotion_agent import PromotionAgent
from components.agents.badge_agent import BadgeAgent
from components.agents.review_360_agent import Review360Agent

# Page configuration
st.set_page_config(
    page_title="Employee Performance Report System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Neo-Dark Analytics Dashboard Theme
st.markdown("""
    <script>
    (function() {
        function forceDarkInputs() {
            const inputs = document.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                // Always force the dark background, regardless of current style
                input.style.setProperty('background-color', 'rgb(25, 18, 24)', 'important');
                input.style.setProperty('background', 'rgb(25, 18, 24)', 'important');
                input.style.setProperty('color', '#FFFFFF', 'important');
                
                // Also check computed style and override if needed
                const computedStyle = window.getComputedStyle(input);
                const bgColor = computedStyle.backgroundColor;
                if (bgColor && (bgColor.includes('255') || bgColor === 'transparent' || bgColor === 'rgba(0, 0, 0, 0)')) {
                    input.style.setProperty('background-color', 'rgb(25, 18, 24)', 'important');
                    input.style.setProperty('background', 'rgb(25, 18, 24)', 'important');
                }
            });
        }
        
        // Run immediately
        forceDarkInputs();
        
        // Run on interval (more frequent)
        setInterval(forceDarkInputs, 50);
        
        // Run on DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', forceDarkInputs);
        } else {
            forceDarkInputs();
        }
        
        // Watch for DOM changes
        const observer = new MutationObserver(function(mutations) {
            forceDarkInputs();
        });
        observer.observe(document.body, { 
            childList: true, 
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class']
        });
        
        // Also run on input focus/blur events
        document.addEventListener('focusin', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
                forceDarkInputs();
            }
        });
        
        // Prevent text input in selectboxes - make them selection-only
        function disableSelectboxTextInput() {
            // Find all selectbox input fields (Streamlit uses input for searchable selectboxes)
            const selectboxInputs = document.querySelectorAll('[data-baseweb="select"] input, .stSelectbox input');
            selectboxInputs.forEach(input => {
                // Make it read-only and prevent typing
                input.setAttribute('readonly', 'readonly');
                input.setAttribute('autocomplete', 'off');
                input.style.cursor = 'pointer';
                
                // Prevent keydown events that would allow typing
                input.addEventListener('keydown', function(e) {
                    // Allow only arrow keys, Enter, Escape, Tab
                    if (!['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Enter', 'Escape', 'Tab'].includes(e.key)) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                });
                
                // Prevent paste
                input.addEventListener('paste', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                });
                
                // Prevent text input
                input.addEventListener('input', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                });
            });
            
            // Also ensure select elements themselves are not editable
            const selectElements = document.querySelectorAll('select');
            selectElements.forEach(select => {
                select.setAttribute('readonly', 'readonly');
                select.style.cursor = 'pointer';
            });
        }
        
        // Run disable function
        disableSelectboxTextInput();
        setInterval(disableSelectboxTextInput, 100);
        
        // Watch for new selectboxes
        const selectObserver = new MutationObserver(function(mutations) {
            disableSelectboxTextInput();
        });
        selectObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    })();
    </script>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* ===== GLOBAL STYLES ===== */
    * {
        font-family: 'Inter', 'Poppins', sans-serif !important;
        letter-spacing: 0.2px;
        line-height: 1.4;
    }
    
    /* Override Streamlit's default light background (rgb(240, 242, 246)) */
    .st-bs,
    [class*="st-bs"],
    [data-baseweb="base"],
    [class*="base"],
    div[class*="st-bs"],
    section[class*="st-bs"],
    [style*="rgb(240, 242, 246)"],
    [style*="background-color: rgb(240, 242, 246)"] {
        background-color: #0A0F1F !important;
        background: #0A0F1F !important;
    }
    
    /* Override any element with light gray background */
    *[style*="240, 242, 246"],
    *[style*="rgb(240, 242, 246)"] {
        background-color: #0A0F1F !important;
        background: #0A0F1F !important;
    }
    
    /* ===== MAIN APP BACKGROUND ===== */
    .stApp {
        background-color: #0A0F1F !important;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 224, 255, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.03) 0%, transparent 50%);
        color: #FFFFFF !important;
    }
    
    /* ===== HEADER & NAVBAR ===== */
    [data-testid="stHeader"] {
        background-color: #0D1324 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(14px);
        box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);
    }
    
    [data-testid="stToolbar"] {
        background-color: #0D1324 !important;
    }
    
    [data-testid="stDecoration"] {
        background-color: #0D1324 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: #0D1324 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #94A3B8 !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Navigation Buttons */
    .stSidebar .stButton > button {
        background-color: rgba(255, 255, 255, 0.06) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        width: 100%;
        margin: 5px 0;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        text-transform: none !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
        letter-spacing: 0.2px;
    }
    
    .stSidebar .stButton > button:hover {
        background-color: rgba(0, 224, 255, 0.1) !important;
        border-color: #00E0FF !important;
        color: #00E0FF !important;
        box-shadow: 0 0 12px rgba(0, 224, 255, 0.3) !important;
        transform: translateX(5px) scale(1.02) !important;
    }
    
    /* Active sidebar button */
    .stSidebar .stButton > button:focus,
    .stSidebar .stButton > button:active {
        background-color: rgba(0, 224, 255, 0.15) !important;
        border-color: #00E0FF !important;
        color: #00E0FF !important;
    }
    
    /* ===== MAIN CONTENT ===== */
    .main .block-container {
        background-color: transparent !important;
        color: #FFFFFF !important;
        padding: 24px !important;
        max-width: 1400px !important;
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        line-height: 1.4 !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid rgba(0, 224, 255, 0.2) !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
    }
    
    /* Remove any orange/red borders from headers and tabs */
    h1, h2, h3, h4, h5, h6 {
        border-color: rgba(0, 224, 255, 0.2) !important;
    }
    
    /* Remove any default Streamlit orange/red borders */
    [data-baseweb="tab-list"]::before,
    [data-baseweb="tab-list"]::after,
    .stTabs::before,
    .stTabs::after {
        display: none !important;
    }
    
    /* Ensure only blue line shows on tabs */
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #00E0FF !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
    }
    
    h2 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    p, span, div, li {
        color: #94A3B8 !important;
        font-weight: 400 !important;
    }
    
    /* ===== INPUT FIELDS ===== */
    /* Override ALL possible input field backgrounds - highest priority */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    input[type="text"],
    input[type="email"],
    input[type="password"],
    input[type="number"],
    input[type="date"],
    input[type="time"],
    textarea,
    select,
    /* Target Streamlit's nested divs that might have background */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select,
    .stNumberInput input,
    .stDateInput input {
        background-color: rgb(25, 18, 24) !important;
        background: rgb(25, 18, 24) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        caret-color: #00E0FF !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    /* Force override any rgba(255, 255, 255, 0.04) backgrounds */
    input[style*="rgba(255, 255, 255, 0.04)"],
    textarea[style*="rgba(255, 255, 255, 0.04)"],
    select[style*="rgba(255, 255, 255, 0.04)"],
    input[style*="rgba(255,255,255,0.04)"],
    textarea[style*="rgba(255,255,255,0.04)"],
    select[style*="rgba(255,255,255,0.04)"] {
        background-color: rgb(25, 18, 24) !important;
        background: rgb(25, 18, 24) !important;
    }
    
    /* Force dark background on ALL input elements - most aggressive override */
    input,
    textarea,
    select {
        background-color: rgb(25, 18, 24) !important;
        background: rgb(25, 18, 24) !important;
    }
    
    /* Override any white or light backgrounds with inline styles */
    input[style*="background-color: white"],
    input[style*="background-color: rgb(255"],
    input[style*="background-color: rgba(255"],
    input[style*="background: white"],
    input[style*="background: rgb(255"],
    input[style*="background: rgba(255"],
    textarea[style*="background-color: white"],
    textarea[style*="background-color: rgb(255"],
    textarea[style*="background-color: rgba(255"],
    textarea[style*="background: white"],
    textarea[style*="background: rgb(255"],
    textarea[style*="background: rgba(255"],
    select[style*="background-color: white"],
    select[style*="background-color: rgb(255"],
    select[style*="background-color: rgba(255"],
    select[style*="background: white"],
    select[style*="background: rgb(255"],
    select[style*="background: rgba(255"] {
        background-color: rgb(25, 18, 24) !important;
        background: rgb(25, 18, 24) !important;
    }
    
    /* Override any white backgrounds on inputs */
    input[style*="background"],
    textarea[style*="background"],
    select[style*="background"] {
        background-color: rgb(25, 18, 24) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    input[type="text"]:focus,
    input[type="email"]:focus,
    input[type="password"]:focus,
    input[type="number"]:focus,
    textarea:focus,
    select:focus {
        border-color: #00E0FF !important;
        outline: none !important;
        box-shadow: 0 0 10px rgba(0, 224, 255, 0.4) !important;
        background-color: rgb(25, 18, 24) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder,
    .stNumberInput > div > div > input::placeholder,
    .stDateInput > div > div > input::placeholder {
        color: #94A3B8 !important;
        opacity: 0.8 !important;
    }
    
    /* Hide ALL Material Icons text completely - use manual arrows instead */
    [class*="material-icons"],
    [class*="MaterialIcons"],
    .material-icons,
    span[class*="material"],
    i[class*="material"],
    div[class*="material"],
    [data-testid="stIconMaterial"],
    svg[class*="material"],
    *[class*="keyboard"],
    *[title*="keyboard"],
    *[data-icon*="keyboard"] {
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        text-indent: -9999px !important;
        line-height: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }
    
    /* Hide any text containing "keyboard_arrow" - use JavaScript for this */
    *[class*="keyboard"],
    *[title*="keyboard_arrow"],
    *[data-icon*="keyboard"] {
        font-size: 0 !important;
        line-height: 0 !important;
        overflow: hidden !important;
        display: none !important;
    }
    
    /* Hide Material Icons pseudo-elements */
    [class*="material-icons"]::before,
    [class*="MaterialIcons"]::before,
    .material-icons::before,
    [class*="material-icons"]::after,
    [class*="MaterialIcons"]::after,
    .material-icons::after {
        content: "" !important;
        display: none !important;
    }
    
    /* Specifically target Streamlit's icon rendering and sidebar icons */
    [data-baseweb="icon"],
    svg[class*="material"],
    button[aria-label*="sidebar"] span,
    button[aria-label*="sidebar"]::before,
    button[aria-label*="sidebar"]::after,
    /* Hide any text content that might be Material Icons */
    span[title*="keyboard"],
    div[title*="keyboard"],
    /* Hide Streamlit sidebar toggle icon text */
    [data-testid="collapsedControl"] span,
    [data-testid="collapsedControl"]::before,
    [data-testid="collapsedControl"]::after {
        display: none !important;
        visibility: hidden !important;
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        content: "" !important;
    }
    
    /* Hide any visible Material Icons text using font-face trick */
    @font-face {
        font-family: 'Material Icons Hidden';
        src: local('Arial');
        unicode-range: U+E000-EFFF;
    }
    
    /* Force hide any remaining icon text */
    body * {
        font-variant: normal !important;
    }
    
    /* Additional hiding for common Material Icons patterns in Streamlit */
    .stSidebar button span,
    .stSidebar [class*="icon"] span,
    header button span,
    header [class*="icon"] span {
        font-size: 0 !important;
        line-height: 0 !important;
        overflow: hidden !important;
    }
    
    /* Hide selectbox dropdown arrow text */
    .stSelectbox svg,
    .stSelectbox [class*="icon"],
    .stSelectbox [data-baseweb="select"] svg {
        display: none !important;
    }
    
    /* Custom selectbox arrow using CSS */
    .stSelectbox > div > div > select {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2300E0FF' d='M6 9L1 4h10z'/%3E%3C/svg%3E") !important;
        background-repeat: no-repeat !important;
        background-position: right 10px center !important;
        padding-right: 35px !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        appearance: none !important;
    }
    
    /* Prevent text input in selectboxes - make them read-only for selection only */
    .stSelectbox > div > div > select,
    select {
        pointer-events: auto !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
    }
    
    /* Disable any input-like behavior in selectboxes */
    .stSelectbox input,
    .stSelectbox input[type="text"],
    .stSelectbox input[type="search"] {
        display: none !important;
    }
    
    /* Ensure select elements are not editable */
    select:focus {
        outline: 2px solid #00E0FF !important;
        outline-offset: 2px !important;
    }
    
    /* Prevent autocomplete dropdown from showing text input */
    [data-baseweb="select"] input {
        pointer-events: none !important;
        cursor: pointer !important;
    }
    
    /* Make sure selectbox container only allows selection */
    [data-baseweb="select"] {
        cursor: pointer !important;
    }
    
    input, textarea, select {
        color: #FFFFFF !important;
        caret-color: #00E0FF !important;
        background-color: rgb(25, 18, 24) !important;
    }
    
    /* Force dark background on all input elements, even if they have inline styles */
    input[type="text"],
    input[type="email"],
    input[type="password"],
    input[type="number"],
    input[type="date"],
    input[type="time"],
    textarea,
    select {
        background-color: rgb(25, 18, 24) !important;
        background: rgb(25, 18, 24) !important;
    }
    
    /* Override any white or light backgrounds */
    input[style*="white"],
    input[style*="rgb(255"],
    input[style*="rgba(255"],
    textarea[style*="white"],
    textarea[style*="rgb(255"],
    textarea[style*="rgba(255"],
    select[style*="white"],
    select[style*="rgb(255"],
    select[style*="rgba(255"] {
        background-color: rgb(25, 18, 24) !important;
        background: rgb(25, 18, 24) !important;
    }
    
    /* ===== BUTTONS ===== */
    /* Primary Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00D1FF, #00FFA6) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        font-weight: 600 !important;
        text-transform: none !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
        letter-spacing: 0.2px;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 18px rgba(0, 224, 255, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 24px rgba(0, 224, 255, 0.6) !important;
        background: linear-gradient(90deg, #14F1FF, #00FFA6) !important;
    }
    
    /* Secondary Buttons */
    button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.06) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        font-weight: 500 !important;
        text-transform: none !important;
        transition: all 0.3s ease !important;
    }
    
    /* Ensure button content (icon + text) displays in a row */
    .stButton > button,
    button[kind="secondary"],
    button[kind="primary"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-direction: row !important;
        gap: 6px !important;
        white-space: nowrap !important;
    }
    
    /* Ensure emoji and text are inline */
    .stButton > button *,
    button[kind="secondary"] *,
    button[kind="primary"] * {
        display: inline !important;
        vertical-align: middle !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: #00E0FF !important;
        color: #00E0FF !important;
        box-shadow: 0 0 12px rgba(0, 224, 255, 0.3) !important;
        transform: scale(1.01) !important;
    }
    
    /* Form Submit Buttons */
    .stForm button[type="submit"],
    .stForm .stButton > button {
        background: linear-gradient(90deg, #00D1FF, #00FFA6) !important;
        color: #000000 !important;
        border: none !important;
    }
    
    .stForm button[type="submit"]:hover,
    .stForm .stButton > button:hover {
        background: linear-gradient(90deg, #14F1FF, #00FFA6) !important;
        box-shadow: 0 0 24px rgba(0, 224, 255, 0.6) !important;
    }
    
    /* Force dark background on form inputs - override any inline styles */
    .stForm input[type="text"],
    .stForm input[type="email"],
    .stForm input[type="password"],
    .stForm input[type="number"],
    .stForm textarea,
    .stForm select {
        background-color: rgb(25, 18, 24) !important;
        background: rgb(25, 18, 24) !important;
        color: #FFFFFF !important;
    }
    
    
    /* ===== CARDS & CONTAINERS ===== */
    .dashboard-card, .content-card, .achievement-card {
        background-color: #111729 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(14px);
    }
    
    .dashboard-card:hover, .content-card:hover, .achievement-card:hover {
        box-shadow: 0 0 12px rgba(0, 224, 255, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
        border-color: rgba(0, 224, 255, 0.3) !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetricContainer"] {
        background-color: #111729 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stMetricContainer"]:hover {
        box-shadow: 0 0 12px rgba(0, 224, 255, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
        border-color: rgba(0, 224, 255, 0.3) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #00E0FF !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* ===== TABLES & DATAFRAMES ===== */
    .dataframe {
        background-color: #111729 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        overflow-x: auto !important;
        box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05) !important;
    }
    
    .dataframe th {
        background-color: #1A2337 !important;
        color: #00E0FF !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    .dataframe td {
        background-color: #111729 !important;
        color: #FFFFFF !important;
        padding: 10px 12px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(0, 224, 255, 0.05) !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #111729 !important;
    }
    
    .dataframe tbody tr:nth-child(odd) {
        background-color: #0D1324 !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: #111729 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05) !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: none !important;
        gap: 0.5rem !important;
        padding: 0.5rem 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        color: #94A3B8 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        margin-right: 0.5rem !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #111729 !important;
        color: #00E0FF !important;
        font-weight: 600 !important;
        border-bottom: none !important;
    }
    
    .stTabs [aria-selected="false"]:hover {
        background-color: rgba(0, 224, 255, 0.1) !important;
        color: #00E0FF !important;
    }
    
    /* Tab highlight indicator - primary blue background */
    [data-baseweb="tab-highlight"] {
        background-color: #00E0FF !important;
        border-radius: 10px !important;
        opacity: 1 !important;
    }
    
    /* ===== FORMS ===== */
    .stForm {
        background-color: #111729 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05) !important;
    }
    
    label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
    }
    
    /* ===== ALERTS & MESSAGES ===== */
    .stInfo {
        background-color: rgba(59, 130, 246, 0.1) !important;
        border-left: 4px solid #3B82F6 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    .stSuccess {
        background-color: rgba(61, 223, 133, 0.1) !important;
        border-left: 4px solid #3DDF85 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background-color: rgba(255, 82, 119, 0.1) !important;
        border-left: 4px solid #FF5277 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background-color: rgba(250, 204, 21, 0.1) !important;
        border-left: 4px solid #FACC15 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    /* ===== SCROLLBARS ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0A0F1F;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00E0FF;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #14F1FF;
    }
    
    /* ===== PROGRESS BARS ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00D1FF, #00FFA6) !important;
    }
    
    .stProgress > div {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border-radius: 10px !important;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background-color: #111729 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        position: relative !important;
    }
    
    /* Hide Streamlit's default expander icon */
    .streamlit-expanderHeader [class*="material-icons"],
    .streamlit-expanderHeader [data-testid="stIconMaterial"],
    .streamlit-expanderHeader svg[class*="material"],
    .streamlit-expanderHeader span[class*="material"] {
        display: none !important;
        visibility: hidden !important;
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
    }
    
    /* Add custom arrow to expander header */
    .streamlit-expanderHeader::before {
        content: '>' !important;
        color: #00E0FF !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        margin-right: 8px !important;
        display: inline-block !important;
        transition: transform 0.3s ease !important;
    }
    
    /* Rotate arrow when expanded */
    [data-testid="stExpander"][aria-expanded="true"] .streamlit-expanderHeader::before {
        transform: rotate(90deg) !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0D1324 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 20px !important;
    }
    
    /* ===== CODE BLOCKS ===== */
    code {
        background-color: #111729 !important;
        color: #00E0FF !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        font-family: 'Courier New', monospace !important;
    }
    
    pre {
        background-color: #111729 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 16px !important;
        overflow-x: auto;
    }
    
    /* ===== LINKS ===== */
    a {
        color: #00E0FF !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
    }
    
    a:hover {
        color: #14F1FF !important;
        text-decoration: underline !important;
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin: 24px 0 !important;
    }
    
    /* ===== SELECTBOX DROPDOWN ===== */
    [data-baseweb="popover"] {
        background-color: #111729 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.1) !important;
    }
    
    [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
    }
    
    /* ===== CHECKBOXES & RADIO ===== */
    .stCheckbox, .stRadio {
        color: #FFFFFF !important;
    }
    
    /* ===== SLIDERS ===== */
    .stSlider > div > div > div {
        background-color: rgba(255, 255, 255, 0.04) !important;
    }
    
    /* ===== SIDEBAR TOGGLE BUTTON ===== */
    .css-1d391kg,
    [class*="css-"] button[aria-label*="sidebar"],
    button[kind="header"] {
        visibility: visible !important;
        display: inline-flex !important;
        opacity: 1 !important;
        background-color: rgba(255, 255, 255, 0.06) !important;
        color: #00E0FF !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
    }
    
    /* ===== HIDE STREAMLIT MENU ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 16px !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .dashboard-card, .content-card {
            padding: 16px !important;
        }
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Show header but style it */
    header {
        visibility: visible !important;
    }
    
    /* Top header/decorator area */
    .stDeployButton {
        display: none;
    }
    
    /* Style header but keep sidebar toggle visible - Neo Dark Theme */
    [data-testid="stHeader"] {
        background-color: #0D1324 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        visibility: visible !important;
        backdrop-filter: blur(14px);
    }
    
    /* Ensure sidebar toggle button is visible */
    [data-testid="stSidebar"] + * button[aria-label*="sidebar"],
    button[data-testid="baseButton-header"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
    }
    </style>
    <script>
    (function() {
        // Replace Material Icons text with arrow symbols (except keyboard_double_arrow_left)
        function replaceMaterialIconsWithArrows() {
            const iconReplacements = {
                'keyboard_double_arrow_right': '>>',
                'keyboard_arrow_right': '>',
                'keyboard_arrow_left': '<',
                'keyboard_arrow_down': '↓',
                'keyboard_arrow_up': '↑',
                'keyboard_double_arrow_down': '↓↓',
                'keyboard_double_arrow_up': '↑↑'
            };
            
            // Hide keyboard_double_arrow_left instead of replacing
            const hideIcon = 'keyboard_double_arrow_left';
            
            // Function to replace text in a string
            function replaceTextInString(text) {
                if (!text || typeof text !== 'string') return text;
                
                let newText = text;
                
                // Hide keyboard_double_arrow_left
                if (newText.includes(hideIcon)) {
                    return ''; // Return empty string to hide
                }
                
                // Replace all keyboard_arrow patterns
                for (const [iconName, replacement] of Object.entries(iconReplacements)) {
                    // Match exact icon name or with spaces/underscores
                    const patterns = [
                        iconName,
                        iconName.replace(/_/g, ' '),
                        iconName.replace(/_/g, '-'),
                        iconName.replace(/_/g, '')
                    ];
                    
                    patterns.forEach(pattern => {
                        const regex = new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
                        newText = newText.replace(regex, replacement);
                    });
                }
                
                return newText;
            }
            
            // Find and replace in ALL text nodes - more comprehensive
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                {
                    acceptNode: function(node) {
                        // Skip script and style content
                        const parent = node.parentElement;
                        if (parent && (parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE')) {
                            return NodeFilter.FILTER_REJECT;
                        }
                        return NodeFilter.FILTER_ACCEPT;
                    }
                },
                false
            );
            
            const nodesToUpdate = [];
            let node;
            while (node = walker.nextNode()) {
                const originalText = node.textContent;
                // Check for any keyboard_arrow pattern (with or without underscores, case insensitive)
                if (originalText && /keyboard[\s_-]*arrow/i.test(originalText)) {
                    nodesToUpdate.push(node);
                }
            }
            
            // Update all found nodes
            nodesToUpdate.forEach(node => {
                try {
                    const originalText = node.textContent;
                    const newText = replaceTextInString(originalText);
                    
                    if (newText === '') {
                        // Hide the parent element if it's keyboard_double_arrow_left
                        if (node.parentElement) {
                            node.parentElement.style.display = 'none';
                            node.parentElement.style.visibility = 'hidden';
                            node.parentElement.style.fontSize = '0';
                            node.parentElement.style.width = '0';
                            node.parentElement.style.height = '0';
                            node.parentElement.style.opacity = '0';
                        }
                    } else if (newText !== originalText) {
                        node.textContent = newText;
                    }
                } catch (e) {
                    // Silently ignore errors
                }
            });
            
            // Also check innerHTML for any elements that might have the text
            document.querySelectorAll('*').forEach(el => {
                try {
                    // Skip script, style, and already processed elements
                    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
                    if (el.hasAttribute('data-arrow-replaced')) return;
                    
                    const innerHTML = el.innerHTML || '';
                    if (/keyboard[\s_-]*arrow/i.test(innerHTML)) {
                        const newHTML = innerHTML
                            .replace(/keyboard_double_arrow_left/gi, '')
                            .replace(/keyboard_double_arrow_right/gi, '>>')
                            .replace(/keyboard_arrow_right/gi, '>')
                            .replace(/keyboard_arrow_left/gi, '<')
                            .replace(/keyboard_arrow_down/gi, '↓')
                            .replace(/keyboard_arrow_up/gi, '↑')
                            .replace(/keyboard_double_arrow_down/gi, '↓↓')
                            .replace(/keyboard_double_arrow_up/gi, '↑↑');
                        
                        if (newHTML !== innerHTML) {
                            el.innerHTML = newHTML;
                            el.setAttribute('data-arrow-replaced', 'true');
                        }
                    }
                } catch (e) {
                    // Silently ignore errors
                }
            });
            
            // Also check all elements for text content
            document.querySelectorAll('*').forEach(el => {
                // Skip script, style, and already processed elements
                if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
                if (el.hasAttribute('data-arrow-replaced')) return;
                
                // Check if element has direct text content (not in child nodes)
                const children = Array.from(el.childNodes);
                const hasOnlyText = children.length === 1 && children[0].nodeType === Node.TEXT_NODE;
                
                if (hasOnlyText) {
                    const originalText = el.textContent || '';
                    if (originalText.includes('keyboard_arrow') || originalText.includes('keyboard arrow')) {
                        const newText = replaceTextInString(originalText);
                        if (newText === '') {
                            el.style.display = 'none';
                            el.style.visibility = 'hidden';
                            el.style.fontSize = '0';
                            el.style.width = '0';
                            el.style.height = '0';
                            el.style.opacity = '0';
                        } else if (newText !== originalText) {
                            el.textContent = newText;
                        }
                        el.setAttribute('data-arrow-replaced', 'true');
                    }
                }
            });
        }
        
        // Run on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', replaceMaterialIconsWithArrows);
        } else {
            replaceMaterialIconsWithArrows();
        }
        
        // Run after Streamlit renders (with multiple delays to catch all content)
        setTimeout(replaceMaterialIconsWithArrows, 50);
        setTimeout(replaceMaterialIconsWithArrows, 100);
        setTimeout(replaceMaterialIconsWithArrows, 200);
        setTimeout(replaceMaterialIconsWithArrows, 500);
        setTimeout(replaceMaterialIconsWithArrows, 1000);
        setTimeout(replaceMaterialIconsWithArrows, 2000);
        setTimeout(replaceMaterialIconsWithArrows, 3000);
        
        // Use MutationObserver to catch dynamically added content (more aggressive)
        const observer = new MutationObserver(function(mutations) {
            // Debounce to avoid too many calls
            clearTimeout(window.arrowReplacementTimeout);
            window.arrowReplacementTimeout = setTimeout(replaceMaterialIconsWithArrows, 50);
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: false
        });
        
        // Also listen for Streamlit's custom events
        if (window.parent) {
            window.parent.addEventListener('message', function(event) {
                if (event.data && (event.data.type === 'streamlit:render' || event.data.type === 'streamlit:rerun')) {
                    setTimeout(replaceMaterialIconsWithArrows, 100);
                    setTimeout(replaceMaterialIconsWithArrows, 500);
                }
            });
        }
        
        // Also run on any user interaction (clicks, etc.) to catch late-rendered content
        document.addEventListener('click', function() {
            setTimeout(replaceMaterialIconsWithArrows, 100);
        }, true);
        
        // Run continuously every 2 seconds for the first 10 seconds, then every 5 seconds
        let continuousInterval = setInterval(replaceMaterialIconsWithArrows, 2000);
        setTimeout(function() {
            clearInterval(continuousInterval);
            // Then run every 5 seconds
            setInterval(replaceMaterialIconsWithArrows, 5000);
        }, 10000);
    })();
    </script>
""", unsafe_allow_html=True)

# Helper function to display data in a table format with action buttons
def display_table_with_actions(data_list, columns_config, edit_callback, delete_callback, edit_form_callback=None):
    """
    Display data in a table format with Edit/Delete action buttons
    
    Args:
        data_list: List of dictionaries containing the data
        columns_config: Dict mapping column names to display functions or field names
        edit_callback: Function(item) called when Edit is clicked
        delete_callback: Function(item) called when Delete is clicked
        edit_form_callback: Optional function(item) to render edit form
    """
    if not data_list:
        st.info("No data found")
        return
    
    # Handle edit forms first
    if edit_form_callback:
        for item in data_list:
            item_id = item.get('id')
            if st.session_state.get(f"editing_{item_id}", False):
                edit_form_callback(item)
    
    # Prepare table data
    table_data = []
    for item in data_list:
        row = {}
        for col_name, col_config in columns_config.items():
            if callable(col_config):
                row[col_name] = col_config(item)
            else:
                value = item.get(col_config, 'N/A')
                # Truncate long descriptions
                if col_name == "Description" and isinstance(value, str) and len(value) > 50:
                    value = value[:50] + '...'
                row[col_name] = value
        table_data.append(row)
    
    # Display table
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Action buttons for each row
    st.markdown("### Actions")
    for item in data_list:
        item_id = item.get('id')
        # Create columns matching table structure
        num_cols = len(columns_config)
        cols = st.columns([2] * (num_cols - 1) + [1.5])  # Last column for actions
        
        # Display data in columns
        col_idx = 0
        for col_name, col_config in list(columns_config.items())[:-1]:  # All except last
            with cols[col_idx]:
                if callable(col_config):
                    st.write(col_config(item))
                else:
                    value = item.get(col_config, 'N/A')
                    if col_name == "Name" or col_name == "Title":
                        st.write(f"**{value}**")
                    else:
                        st.write(value)
            col_idx += 1
        
        # Action buttons in last column
        with cols[-1]:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("✏️ Edit", key=f"edit_btn_{item_id}", use_container_width=True):
                    edit_callback(item)
            with btn_col2:
                if st.button("🗑️ Del", key=f"delete_btn_{item_id}", use_container_width=True, type="secondary"):
                    delete_callback(item)

# Helper function to convert JSON/dict to table
def display_as_table(data):
    """Convert JSON/dict data to a readable table format"""
    if not data:
        st.info("No data to display")
        return
    
    if isinstance(data, dict):
        # Flatten nested dictionaries
        flattened = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # For nested structures, convert to string representation
                flattened.append({"Key": str(key), "Value": json.dumps(value, indent=2, default=str)})
            else:
                flattened.append({"Key": str(key), "Value": str(value)})
        
        df = pd.DataFrame(flattened)
        st.dataframe(df, use_container_width=True, hide_index=True)
    elif isinstance(data, list):
        if data and isinstance(data[0], dict):
            # List of dictionaries - display as table
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            # Simple list
            df = pd.DataFrame({"Value": data})
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        # Simple value
        df = pd.DataFrame({"Key": ["Value"], "Value": [str(data)]})
        st.dataframe(df, use_container_width=True, hide_index=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "data_manager" not in st.session_state:
    st.session_state.data_manager = DataManager()
if "auth_manager" not in st.session_state:
    st.session_state.auth_manager = AuthManager(st.session_state.data_manager)

# Initialize agents
def initialize_agents():
    """Initialize all agents"""
    data_manager = st.session_state.data_manager
    notification_agent = NotificationAgent(data_manager)
    performance_agent = EnhancedPerformanceAgent(data_manager)
    reporting_agent = ReportingAgent(data_manager)
    risk_agent = RiskDetectionAgent(data_manager, performance_agent, reporting_agent)
    comparison_agent = ComparisonAgent(data_manager, performance_agent)
    enhanced_ai_agent = EnhancedAIAgent(data_manager, performance_agent)
    achievement_agent = AchievementAgent(data_manager, notification_agent)
    predictive_analytics_agent = PredictiveAnalyticsAgent(data_manager, performance_agent, reporting_agent)
    correlation_agent = CorrelationAgent(data_manager, performance_agent)
    
    return {
        "task_agent": TaskAgent(data_manager, notification_agent),
        "performance_agent": performance_agent,
        "reporting_agent": reporting_agent,
        "notification_agent": notification_agent,
        "risk_agent": risk_agent,
        "assistant_agent": AssistantAgent(data_manager, performance_agent, reporting_agent),
        "export_agent": ExportAgent(data_manager),
        "goal_agent": GoalAgent(data_manager, notification_agent),
        "feedback_agent": FeedbackAgent(data_manager, notification_agent),
        "filtering_agent": FilteringAgent(),
        "comparison_agent": comparison_agent,
        "enhanced_ai_agent": enhanced_ai_agent,
        "achievement_agent": achievement_agent,
        "predictive_analytics_agent": predictive_analytics_agent,
        "correlation_agent": correlation_agent,
        "skill_agent": SkillAgent(data_manager),
        "workload_agent": WorkloadAgent(data_manager),
        "attendance_agent": AttendanceAgent(data_manager),
        "engagement_agent": EngagementAgent(data_manager),
        "promotion_agent": PromotionAgent(data_manager),
        "badge_agent": BadgeAgent(data_manager),
        "review_360_agent": Review360Agent(data_manager)
    }

# Login page
def login_page():
    """Login page"""
    st.title("🔐 Login")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            
            # Password field with show/hide toggle
            if "show_password" not in st.session_state:
                st.session_state.show_password = False
            
            # Styled password toggle - hide checkbox label text, show only icon
            st.markdown("""
                <style>
                /* Hide checkbox label text, keep only icon */
                div[data-testid="stCheckbox"] label > div:last-child {
                    font-size: 0 !important;
                    width: 0 !important;
                    height: 0 !important;
                    overflow: hidden !important;
                }
                /* Style the checkbox container */
                div[data-testid="stCheckbox"] {
                    margin-top: 0 !important;
                }
                div[data-testid="stCheckbox"] label {
                    cursor: pointer;
                    padding: 4px 8px;
                }
                div[data-testid="stCheckbox"] label > div:first-child {
                    font-size: 1.4em !important;
                    color: #94A3B8 !important;
                    transition: color 0.3s ease;
                    margin-right: 0 !important;
                }
                div[data-testid="stCheckbox"] label:hover > div:first-child {
                    color: #00E0FF !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Password input and toggle in same row
            pass_col1, pass_col2 = st.columns([11, 1])
            with pass_col1:
                password = st.text_input(
                    "Password", 
                    type="password" if not st.session_state.show_password else "text",
                    placeholder="Enter your password",
                    key="password_input"
                )
            with pass_col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Align with input
                toggle_icon = "👁️" if not st.session_state.show_password else "🙈"
                show_password = st.checkbox(
                    toggle_icon, 
                    value=st.session_state.show_password, 
                    key="show_password_checkbox",
                    label_visibility="visible"
                )
                if show_password != st.session_state.show_password:
                    st.session_state.show_password = show_password
                    st.rerun()
            
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if email and password:
                    result = st.session_state.auth_manager.authenticate(email, password)
                    if result:
                        st.session_state.authenticated = True
                        st.session_state.user = result
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.error("Please enter both email and password")
        
        st.markdown("---")
        st.markdown("**Default Users:**")
        st.code("Owner: owner@company.com / admin123")
        st.code("Employee: john@company.com / password123")

# Main dashboard
def dashboard():
    """Main dashboard with enhanced styling - Team Performance Dashboard for Managers"""
    user_role = st.session_state.user.get("role", "employee")
    
    st.markdown("""
        <style>
        .performance-overview {
            font-size: 2.5rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.5rem;
        }
        .performance-description {
            color: #94A3B8;
            opacity: 0.9;
            margin-bottom: 2rem;
        }
        </style>
        <div class="performance-overview">Team Performance Dashboard</div>
        <div class="performance-description">Monitor and track your team's performance metrics, KPIs, and analytics</div>
    """, unsafe_allow_html=True)
    
    agents = initialize_agents()
    performance_agent = agents["performance_agent"]
    task_agent = agents["task_agent"]
    goal_agent = agents["goal_agent"]
    
    # Overview metrics
    overview = agents["reporting_agent"].generate_overview_report()
    
    # Get all employees and their performance
    employees = st.session_state.data_manager.load_data("employees") or []
    tasks = task_agent.get_tasks()
    goals = goal_agent.get_all_goals()
    performance_data = st.session_state.data_manager.load_data("performances") or []
    
    # Calculate team KPIs
    team_employees = employees  # For now, all employees (can filter by department later)
    team_performance_scores = []
    team_completion_rates = []
    team_on_time_rates = []
    
    for emp in team_employees:
        emp_id = emp.get("id")
        eval_data = performance_agent.evaluate_employee(emp_id, save=False)
        if eval_data:
            team_performance_scores.append(eval_data.get('performance_score', 0))
            team_completion_rates.append(eval_data.get('completion_rate', 0))
            team_on_time_rates.append(eval_data.get('on_time_rate', 0))
    
    avg_team_performance = sum(team_performance_scores) / len(team_performance_scores) if team_performance_scores else 0
    avg_completion_rate = sum(team_completion_rates) / len(team_completion_rates) if team_completion_rates else 0
    avg_on_time_rate = sum(team_on_time_rates) / len(team_on_time_rates) if team_on_time_rates else 0
    
    # Team KPI Cards
    st.markdown("### 📊 Team KPIs")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Average Team Performance</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{avg_team_performance:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Average Completion Rate</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{avg_completion_rate:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Average On-Time Rate</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{avg_on_time_rate:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Team Size</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{len(team_employees)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Employee Ranking Section
    st.markdown("### 🏆 Employee Performance Ranking")
    employee_rankings = []
    for emp in team_employees:
        emp_id = emp.get("id")
        eval_data = performance_agent.evaluate_employee(emp_id, save=False)
        if eval_data:
            employee_rankings.append({
                "name": emp.get("name", "Unknown"),
                "employee_id": emp_id,
                "performance_score": eval_data.get('performance_score', 0),
                "completion_rate": eval_data.get('completion_rate', 0),
                "on_time_rate": eval_data.get('on_time_rate', 0),
                "rank": eval_data.get('rank', 'N/A')
            })
    
    # Sort by performance score
    employee_rankings.sort(key=lambda x: x['performance_score'], reverse=True)
    
    if employee_rankings:
        # Assign ranks based on sorted order
        for idx, emp in enumerate(employee_rankings):
            emp['rank'] = idx + 1
        
        # Create visual charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Bar Chart - Performance Scores
            ranking_df = pd.DataFrame(employee_rankings)
            ranking_df = ranking_df.sort_values('performance_score', ascending=True)  # Ascending for better bar chart
            
            fig_bar = px.bar(
                ranking_df,
                x='performance_score',
                y='name',
                orientation='h',
                title='Performance Scores Comparison',
                color='performance_score',
                color_continuous_scale='Viridis',
                text='performance_score',
                labels={'performance_score': 'Performance Score', 'name': 'Employee'}
            )
            fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF',
                title_font_color='#00E0FF',
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with chart_col2:
            # Radar/Spider Chart for Top 3 Employees
            top_3 = employee_rankings[:3]
            if len(top_3) > 0:
                categories = ['Performance', 'Completion', 'On-Time']
                
                fig_radar = go.Figure()
                
                colors = ['#00E0FF', '#14F1FF', '#3B82F6']
                for idx, emp in enumerate(top_3):
                    values = [
                        emp['performance_score'],
                        emp['completion_rate'],
                        emp['on_time_rate']
                    ]
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values + [values[0]],  # Close the loop
                        theta=categories + [categories[0]],
                        fill='toself',
                        name=emp['name'],
                        line=dict(color=colors[idx % len(colors)], width=2)
                    ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            gridcolor='rgba(255,255,255,0.2)',
                            tickfont=dict(color='#94A3B8')
                        ),
                        angularaxis=dict(
                            gridcolor='rgba(255,255,255,0.2)',
                            tickfont=dict(color='#94A3B8')
                        ),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#FFFFFF',
                    title='Top 3 Employees - Multi-Metric Comparison',
                    title_font_color='#00E0FF',
                    height=400,
                    legend=dict(font=dict(color='#FFFFFF'))
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("Need at least 3 employees for radar chart")
        
        # Horizontal Bar Chart for Completion and On-Time Rates
        st.markdown("---")
        st.markdown("#### 📊 Detailed Metrics Comparison")
        
        metrics_df = pd.DataFrame([
            {
                'Employee': emp['name'],
                'Completion Rate': emp['completion_rate'],
                'On-Time Rate': emp['on_time_rate']
            }
            for emp in employee_rankings
        ])
        
        fig_grouped = go.Figure()
        
        fig_grouped.add_trace(go.Bar(
            name='Completion Rate',
            x=metrics_df['Employee'],
            y=metrics_df['Completion Rate'],
            marker_color='#00E0FF',
            text=metrics_df['Completion Rate'].round(1),
            textposition='outside'
        ))
        
        fig_grouped.add_trace(go.Bar(
            name='On-Time Rate',
            x=metrics_df['Employee'],
            y=metrics_df['On-Time Rate'],
            marker_color='#14F1FF',
            text=metrics_df['On-Time Rate'].round(1),
            textposition='outside'
        ))
        
        fig_grouped.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF',
            title='Completion Rate vs On-Time Rate',
            title_font_color='#00E0FF',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
            legend=dict(font=dict(color='#FFFFFF')),
            height=400
        )
        st.plotly_chart(fig_grouped, use_container_width=True)
        
        # Compact ranking table with badges
        st.markdown("---")
        st.markdown("#### 📋 Ranking Summary")
        
        # Create a more visual ranking display
        for idx, emp in enumerate(employee_rankings[:10]):  # Show top 10
            rank = idx + 1
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
            
            col1, col2, col3, col4, col5 = st.columns([0.5, 2, 1.5, 1.5, 1.5])
            with col1:
                st.markdown(f"### {medal}")
            with col2:
                st.markdown(f"**{emp['name']}**")
            with col3:
                # Performance score with color indicator
                score = emp['performance_score']
                color = "#3DDF85" if score >= 80 else "#FACC15" if score >= 60 else "#FF5277"
                st.markdown(f"<span style='color: {color}; font-size: 1.2em; font-weight: bold;'>{score:.1f}</span>", unsafe_allow_html=True)
            with col4:
                st.write(f"{emp['completion_rate']:.1f}%")
            with col5:
                st.write(f"{emp['on_time_rate']:.1f}%")
            
            if idx < len(employee_rankings) - 1:
                st.markdown("---")
    else:
        st.info("No performance data available yet. Evaluate employees to see rankings.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Calculate percentages for circular progress
    total_projects = overview["projects"]["total"]
    total_tasks = overview["tasks"]["total"]
    completed_tasks = overview["tasks"].get("completed", 0)
    task_completion = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    avg_performance = overview['performance']['average_score']
    
    # Create metric cards with enhanced styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem; opacity: 0.9;">Overall Team Score</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{avg_performance:.0f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Get top performer
        employees = st.session_state.data_manager.load_data("employees") or []
        performance_data = st.session_state.data_manager.load_data("performances") or []
        top_performer = None
        if performance_data:
            sorted_perf = sorted(performance_data, key=lambda x: x.get('performance_score', 0), reverse=True)
            if sorted_perf:
                top_emp_id = sorted_perf[0].get('employee_id')
                top_performer = next((e for e in employees if e.get('id') == top_emp_id), None)
        
        top_name = top_performer.get('name', 'N/A') if top_performer else 'N/A'
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem; opacity: 0.9;">Top Performer</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #00E0FF;">{top_name}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem; opacity: 0.9;">Average Goal Completion</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{task_completion:.0f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate feedback score (mock for now)
        feedback_score = 4.5
        st.markdown(f"""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem; opacity: 0.9;">Feedback Score</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{feedback_score}/5</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts section with card styling
    st.markdown("""
        <style>
        .chart-card {
            background-color: #111729;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("#### Individual Performance Trend")
        performance_data = st.session_state.data_manager.load_data("performances") or []
        if performance_data:
            # Get recent performance data for trend
            recent_perf = sorted(performance_data, key=lambda x: x.get('evaluated_at', ''), reverse=True)[:10]
            if recent_perf:
                dates = [p.get('evaluated_at', '')[:10] for p in reversed(recent_perf)]
                scores = [p.get('performance_score', 0) for p in reversed(recent_perf)]
                
                fig = px.line(
                    x=dates,
                    y=scores,
                    title="",
                    labels={'x': 'Date', 'y': 'Performance Score'},
                    color_discrete_sequence=['#00E0FF']
                )
                fig.update_layout(
                    plot_bgcolor='#111729',
                    paper_bgcolor='#111729',
                    font_color='#FFFFFF',
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=8, color='#00E0FF'))
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("#### Skills Development")
        # Skills data
        skills_data = {
            'Communication': 85,
            'Technical Skills': 75,
            'Leadership': 65,
            'Problem Solving': 80
        }
        
        fig = px.bar(
            x=list(skills_data.keys()),
            y=list(skills_data.values()),
            title="",
            labels={'x': 'Skill', 'y': 'Score'},
            color_discrete_sequence=['#00E0FF']
        )
        fig.update_layout(
            plot_bgcolor='#111729',
            paper_bgcolor='#111729',
            font_color='#FFFFFF',
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
        )
        fig.update_traces(marker_color='#00E0FF')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Reports section
    st.markdown("#### Recent Reports")
    reports_col1, reports_col2, reports_col3 = st.columns(3)
    with reports_col1:
        st.markdown("""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="color: #00E0FF; font-weight: 600; margin-bottom: 0.5rem;">Performance Report</div>
                <div style="color: #94A3B8; opacity: 0.7; font-size: 0.9rem;">Last updated: Today</div>
            </div>
        """, unsafe_allow_html=True)
    with reports_col2:
        st.markdown("""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="color: #00E0FF; font-weight: 600; margin-bottom: 0.5rem;">Team Analysis</div>
                <div style="color: #94A3B8; opacity: 0.7; font-size: 0.9rem;">Last updated: Yesterday</div>
            </div>
        """, unsafe_allow_html=True)
    with reports_col3:
        st.markdown("""
            <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                <div style="color: #00E0FF; font-weight: 600; margin-bottom: 0.5rem;">Monthly Summary</div>
                <div style="color: #94A3B8; opacity: 0.7; font-size: 0.9rem;">Last updated: This week</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Development & Training Suggestions Section
    st.markdown("### 🎓 Development & Training Suggestions")
    employees_list = st.session_state.data_manager.load_data("employees") or []
    development_suggestions = []
    
    for emp in employees_list:
        emp_id = emp.get("id")
        eval_data = performance_agent.evaluate_employee(emp_id, save=False)
        if eval_data:
            score = eval_data.get('performance_score', 0)
            completion_rate = eval_data.get('completion_rate', 0)
            on_time_rate = eval_data.get('on_time_rate', 0)
            
            suggestions = []
            if score < 70:
                suggestions.append("Performance improvement training recommended")
            if completion_rate < 80:
                suggestions.append("Time management and task prioritization training")
            if on_time_rate < 75:
                suggestions.append("Deadline management and planning skills development")
            if score < 60:
                suggestions.append("Consider 1-on-1 coaching sessions")
            
            if suggestions:
                development_suggestions.append({
                    "employee": emp.get("name", "Unknown"),
                    "employee_id": emp_id,
                    "current_score": score,
                    "suggestions": suggestions
                })
    
    if development_suggestions:
        for suggestion in development_suggestions:
            with st.expander(f"> {suggestion['employee']} - Score: {suggestion['current_score']:.1f}%"):
                st.write(f"**Current Performance Score:** {suggestion['current_score']:.1f}%")
                st.markdown("**Recommended Development Actions:**")
                for sug in suggestion['suggestions']:
                    st.write(f"• {sug}")
                st.markdown("---")
                st.info("💡 Consider scheduling a 1-on-1 meeting to discuss development plan")
    else:
        st.success("✅ All team members are performing well! No immediate training needs identified.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions for Managers
    st.markdown("### ⚡ Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        if st.button("📊 View Full Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()
    with action_col2:
        if st.button("⚖️ Compare Team Members", use_container_width=True):
            st.session_state.current_page = "Comparison"
            st.rerun()
    with action_col3:
        if st.button("📈 Evaluate Performance", use_container_width=True):
            st.session_state.current_page = "Performance"
            st.rerun()

# Projects page
def projects_page():
    """Projects management page"""
    st.title("📁 Projects")
    st.markdown("---")
    
    # Role-based access control
    user_role = st.session_state.user.get("role", "employee")
    if user_role == "employee":
        st.error("❌ Access Denied: You don't have permission to access this page.")
        st.info("💡 Employees can view project information through their assigned tasks only.")
        return
    
    data_manager = st.session_state.data_manager
    projects = data_manager.load_data("projects") or []
    
    # Check if we should show view after creation
    show_view_after_create = st.session_state.get("show_projects_view", False)
    
    if show_view_after_create:
        st.session_state.show_projects_view = False
        st.success("✅ Project created successfully! Viewing all projects below.")
        st.markdown("---")
        # Show view content immediately
        projects = data_manager.load_data("projects") or []
        if projects:
            df = pd.DataFrame(projects)
            st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.markdown("### Or use tabs below to navigate")
    
    # Role-based tabs
    if user_role in ["owner", "manager"]:
        tab1, tab2, tab3 = st.tabs(["View Projects", "Create Project", "Project Reports"])
    else:
        # Employees can only view projects
        tab1, tab3 = st.tabs(["View Projects", "Project Reports"])
        tab2 = None
    
    with tab1:
        if projects:
            # Handle edit forms first - only for managers/owners
            if user_role in ["owner", "manager"]:
                for edit_idx, project in enumerate(projects):
                    project_id = project.get('id')
                    if st.session_state.get(f"editing_project_{project_id}", False):
                        with st.expander(f"✏️ Editing: {project.get('name', 'Untitled')}", expanded=True):
                            with st.form(f"edit_project_form_{edit_idx}_{project_id}"):
                                edit_name = st.text_input("Project Name", value=project.get('name', ''), key=f"edit_name_{edit_idx}_{project_id}")
                                edit_description = st.text_area("Description", value=project.get('description', ''), key=f"edit_desc_{edit_idx}_{project_id}")
                                edit_status = st.selectbox("Status", ["active", "completed", "on_hold"], 
                                                          index=["active", "completed", "on_hold"].index(project.get('status', 'active')),
                                                          key=f"edit_project_status_{edit_idx}_{project_id}")
                                edit_deadline = st.date_input("Deadline", 
                                                             value=datetime.fromisoformat(project.get('deadline')) if project.get('deadline') else None,
                                                             key=f"edit_deadline_{edit_idx}_{project_id}")
                                # Show current manager (read-only) - manager is set when project is created
                                st.info(f"**Manager:** {project.get('manager', 'N/A')} (assigned at creation)")
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Save Changes", key=f"save_btn_{edit_idx}_{project_id}"):
                                        project['name'] = edit_name
                                        project['description'] = edit_description
                                        project['status'] = edit_status
                                        project['deadline'] = edit_deadline.isoformat() if edit_deadline else None
                                        # Manager remains unchanged (set at creation)
                                        project['updated_at'] = datetime.now().isoformat()
                                        data_manager.save_data("projects", projects)
                                        st.session_state[f"editing_project_{project_id}"] = False
                                        st.success("Project updated!")
                                        st.rerun()
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel", key=f"cancel_btn_{edit_idx}_{project_id}"):
                                        st.session_state[f"editing_project_{project_id}"] = False
                                        st.rerun()
            
            # Create beautiful table with action buttons
            st.markdown("""
                <style>
                .table-row-container {
                    background-color: #111729;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 16px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);
                    transition: all 0.3s ease;
                }
                .table-row-container:hover {
                    box-shadow: 0 0 12px rgba(0, 224, 255, 0.3);
                    transform: translateY(-2px) scale(1.01);
                    border-color: rgba(0, 224, 255, 0.3);
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Table header
            header_cols = st.columns([2, 1, 1, 2, 1.5])
            with header_cols[0]:
                st.markdown("**Name**")
            with header_cols[1]:
                st.markdown("**Status**")
            with header_cols[2]:
                st.markdown("**Deadline**")
            with header_cols[3]:
                st.markdown("**Description**")
            with header_cols[4]:
                st.markdown("**Actions**")
            
            st.markdown("---")
            
            # Table rows with action buttons
            for idx, project in enumerate(projects):
                project_id = project.get('id')
                name = project.get('name', 'Untitled')
                status = project.get('status', 'N/A')
                deadline = project.get('deadline', 'N/A')[:10] if project.get('deadline') else 'N/A'
                description = (project.get('description', '')[:50] + '...') if len(project.get('description', '')) > 50 else (project.get('description', '') or 'N/A')
                
                # Create row with columns
                row_cols = st.columns([2, 1, 1, 2, 1.5])
                with row_cols[0]:
                    st.write(f"**{name}**")
                with row_cols[1]:
                    st.write(status)
                with row_cols[2]:
                    st.write(deadline)
                with row_cols[3]:
                    st.write(description)
                with row_cols[4]:
                    # Only managers and owners can edit/delete
                    if user_role in ["owner", "manager"]:
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("✏️ Edit", key=f"view_projects_edit_{idx}_{project_id}", use_container_width=True):
                                st.session_state[f"editing_project_{project_id}"] = True
                                st.rerun()
                        with btn_col2:
                            if st.button("🗑️ Del", key=f"view_projects_delete_{idx}_{project_id}", use_container_width=True, type="secondary"):
                                projects = [p for p in projects if p.get("id") != project_id]
                                data_manager.save_data("projects", projects)
                                st.success("Project deleted!")
                                st.rerun()
                    else:
                        st.write("View Only")
        else:
            st.info("No projects found")
    
    if tab2:
        with tab2:
            with st.form("create_project"):
                name = st.text_input("Project Name *")
                description = st.text_area("Description")
                status = st.selectbox("Status", ["active", "completed", "on_hold"], key="create_project_status")
                deadline = st.date_input("Deadline")
                # Manager is auto-set to the logged-in user's email
                user_email = st.session_state.user.get("email", "")
                
                if st.form_submit_button("Create Project"):
                    if name:
                        new_project = {
                            "id": str(len(projects) + 1),
                            "name": name,
                            "description": description,
                            "status": status,
                            "deadline": deadline.isoformat() if deadline else None,
                            "manager": user_email,  # Auto-assign to logged-in user
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat()
                        }
                        projects.append(new_project)
                        data_manager.save_data("projects", projects)
                        st.session_state.show_projects_view = True
                        st.rerun()
    
    with tab3:
        if projects:
            selected_project = st.selectbox("Select Project", ["-- Choose project --"] + [p.get("name") for p in projects], key="project_report_select")
            if selected_project and selected_project != "-- Choose project --":
                project = next((p for p in projects if p.get("name") == selected_project), None)
                if project:
                    agents = initialize_agents()
                    report = agents["reporting_agent"].generate_project_report(project["id"])
                    
                    if report.get("error"):
                        st.error(report.get("error"))
                    else:
                        # Project Header
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, rgba(0, 224, 255, 0.1), rgba(59, 130, 246, 0.1)); 
                                        border: 1px solid rgba(0, 224, 255, 0.2); border-radius: 16px; padding: 24px; margin-bottom: 24px;">
                                <h2 style="color: #00E0FF; margin: 0 0 8px 0;">📁 {report.get('project_name', 'N/A')}</h2>
                                <p style="color: #94A3B8; margin: 0;">
                                    Status: <span style="color: #3DDF85;">{report.get('status', 'N/A').title()}</span> | 
                                    Project ID: {report.get('project_id', 'N/A')}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Key Metrics Cards
                        st.markdown("### 📊 Project Metrics")
                        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                        
                        with metric_col1:
                            st.markdown(f"""
                                <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                            border-radius: 16px; padding: 20px; text-align: center; 
                                            box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                                    <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Total Tasks</div>
                                    <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{report.get('total_tasks', 0)}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with metric_col2:
                            st.markdown(f"""
                                <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                            border-radius: 16px; padding: 20px; text-align: center; 
                                            box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                                    <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Completed</div>
                                    <div style="font-size: 2.5rem; font-weight: 700; color: #3DDF85;">{report.get('completed_tasks', 0)}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with metric_col3:
                            st.markdown(f"""
                                <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                            border-radius: 16px; padding: 20px; text-align: center; 
                                            box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                                    <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Completion Rate</div>
                                    <div style="font-size: 2.5rem; font-weight: 700; color: #00E0FF;">{report.get('completion_rate', 0):.1f}%</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with metric_col4:
                            health_score = report.get('health_score', 0)
                            health_color = "#3DDF85" if health_score >= 70 else "#FACC15" if health_score >= 50 else "#FF5277"
                            st.markdown(f"""
                                <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                            border-radius: 16px; padding: 20px; text-align: center; 
                                            box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                                    <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">Health Score</div>
                                    <div style="font-size: 2.5rem; font-weight: 700; color: {health_color};">{health_score:.0f}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Task Status Breakdown Chart
                        chart_col1, chart_col2 = st.columns(2)
                        
                        with chart_col1:
                            st.markdown("### 📈 Task Status Breakdown")
                            task_data = {
                                "Completed": report.get('completed_tasks', 0),
                                "In Progress": report.get('in_progress_tasks', 0),
                                "Pending": report.get('pending_tasks', 0)
                            }
                            
                            # Create pie chart
                            fig_pie = px.pie(
                                values=list(task_data.values()),
                                names=list(task_data.keys()),
                                color_discrete_map={
                                    "Completed": "#3DDF85",
                                    "In Progress": "#00E0FF",
                                    "Pending": "#FACC15"
                                },
                                hole=0.4
                            )
                            fig_pie.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#FFFFFF',
                                title_font_color='#00E0FF',
                                showlegend=True,
                                legend=dict(font=dict(color='#FFFFFF')),
                                height=350
                            )
                            fig_pie.update_traces(textfont_color='#FFFFFF', textposition='inside')
                            st.plotly_chart(fig_pie, use_container_width=True)
                        
                        with chart_col2:
                            st.markdown("### 📊 Completion Progress")
                            completion_rate = report.get('completion_rate', 0)
                            
                            # Progress bar visualization
                            st.markdown(f"""
                                <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                            border-radius: 16px; padding: 24px;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                                        <span style="color: #94A3B8;">Progress</span>
                                        <span style="color: #00E0FF; font-weight: 600;">{completion_rate:.1f}%</span>
                                    </div>
                                    <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; height: 30px; overflow: hidden;">
                                        <div style="background: linear-gradient(90deg, #00D1FF, #00FFA6); 
                                                    height: 100%; width: {completion_rate}%; 
                                                    transition: width 0.5s ease; border-radius: 10px;"></div>
                                    </div>
                                    <div style="margin-top: 20px; color: #94A3B8; font-size: 0.9rem;">
                                        <div>✅ Completed: {report.get('completed_tasks', 0)} tasks</div>
                                        <div>🔄 In Progress: {report.get('in_progress_tasks', 0)} tasks</div>
                                        <div>⏳ Pending: {report.get('pending_tasks', 0)} tasks</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Health Score Indicator
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("### 💚 Project Health")
                            health_score = report.get('health_score', 0)
                            health_status = "Excellent" if health_score >= 70 else "Good" if health_score >= 50 else "Needs Attention"
                            health_emoji = "🟢" if health_score >= 70 else "🟡" if health_score >= 50 else "🔴"
                            
                            st.markdown(f"""
                                <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                            border-radius: 16px; padding: 20px; text-align: center;">
                                    <div style="font-size: 3rem; margin-bottom: 10px;">{health_emoji}</div>
                                    <div style="font-size: 1.5rem; font-weight: 600; color: {health_color}; margin-bottom: 5px;">
                                        {health_score:.0f}/100
                                    </div>
                                    <div style="color: #94A3B8;">{health_status}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Risks Section
                        risks = report.get('risks', [])
                        if risks:
                            st.markdown("### ⚠️ Project Risks")
                            for risk in risks:
                                risk_severity = risk.get('severity', 'medium')
                                risk_color = "#FF5277" if risk_severity == "high" else "#FACC15" if risk_severity == "medium" else "#00E0FF"
                                st.markdown(f"""
                                    <div style="background-color: #111729; border-left: 4px solid {risk_color}; 
                                                border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                                        <div style="color: {risk_color}; font-weight: 600; margin-bottom: 8px;">
                                            {risk.get('type', 'Risk').title()} - {risk_severity.title()}
                                        </div>
                                        <div style="color: #94A3B8;">{risk.get('description', 'N/A')}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown("### ⚠️ Project Risks")
                            st.success("✅ No risks identified. Project is on track!")
                        
                        # Resource Allocation
                        resource_allocation = report.get('resource_allocation', {})
                        if resource_allocation:
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("### 👥 Resource Allocation")
                            
                            if isinstance(resource_allocation, dict) and resource_allocation:
                                # Create a bar chart for resource allocation
                                # resource_allocation is a dict where values are dicts with "name" and "task_count"
                                resource_df = pd.DataFrame([
                                    {"Employee": v.get("name", k) if isinstance(v, dict) else k, "Tasks": v.get("task_count", v) if isinstance(v, dict) else v} 
                                    for k, v in resource_allocation.items()
                                ])
                                
                                fig_resource = px.bar(
                                    resource_df,
                                    x="Employee",
                                    y="Tasks",
                                    title="Tasks per Employee",
                                    color="Tasks",
                                    color_continuous_scale="Viridis"
                                )
                                fig_resource.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font_color='#FFFFFF',
                                    title_font_color='#00E0FF',
                                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                                    height=350
                                )
                                st.plotly_chart(fig_resource, use_container_width=True)
                        
                        # Estimated Completion Date
                        estimated_completion = report.get('estimated_completion_date')
                        if estimated_completion:
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("### 📅 Estimated Completion")
                            st.info(f"**Estimated Completion Date:** {estimated_completion}")

# Tasks page
def tasks_page():
    """Tasks management page"""
    st.title("✅ Tasks")
    st.markdown("---")
    
    # Role-based access control
    user_role = st.session_state.user.get("role", "employee")
    user_email = st.session_state.user.get("email")
    
    agents = initialize_agents()
    task_agent = agents["task_agent"]
    
    # Check if we should show view after creation
    show_view_after_create = st.session_state.get("show_tasks_view", False)
    
    if show_view_after_create:
        st.session_state.show_tasks_view = False
        st.success("✅ Task created successfully! Viewing all tasks below.")
        st.markdown("---")
        # Show view content immediately
        if user_role in ["owner", "manager"]:
            tasks = task_agent.get_tasks()
        else:
            # Get employee ID from email for employees
            employees = st.session_state.data_manager.load_data("employees") or []
            employee = next((e for e in employees if e.get("email") == user_email), None)
            if employee:
                employee_id = employee.get("id")
                tasks = task_agent.get_tasks({"assigned_to": employee_id})
            else:
                tasks = []
        if tasks:
            df = pd.DataFrame(tasks)
            st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.markdown("### Or use tabs below to navigate")
    
    # Role-based tabs
    if user_role in ["owner", "manager"]:
        tab1, tab2 = st.tabs(["View Tasks", "Create Task"])
        tab3 = None
    else:
        # Employees don't use tabs - show tasks directly
        tab1 = None
        tab2 = None
        tab3 = None
    
    # For employees, show tasks directly without tabs
    if user_role == "employee":
        # Employees only see their own tasks - need to get employee ID first
        employees = st.session_state.data_manager.load_data("employees") or []
        employee = next((e for e in employees if e.get("email") == user_email), None)
        if employee:
            employee_id = employee.get("id")
            tasks = task_agent.get_tasks({"assigned_to": employee_id})
            st.info("👤 Showing only your assigned tasks")
        else:
            st.error("❌ Employee record not found.")
            tasks = []
        
        if tasks:
            # Handle status update forms first
            for task in tasks:
                task_id = task.get('id')
                if st.session_state.get(f"updating_status_{task_id}", False):
                    with st.expander(f"✏️ Update Status: {task.get('title', 'Untitled')}", expanded=True):
                        with st.form(f"update_status_form_{task_id}"):
                            current_status = task.get('status', 'pending')
                            status_options = ["pending", "in_progress", "completed"]
                            current_index = status_options.index(current_status) if current_status in status_options else 0
                            
                            new_status = st.selectbox("Status", status_options, index=current_index, key=f"status_select_{task_id}")
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Update Status"):
                                    # Update task status
                                    all_tasks = task_agent.get_tasks()
                                    updated_task = None
                                    old_status = task.get('status', 'pending')  # Get old status before update
                                    
                                    for t in all_tasks:
                                        if t.get('id') == task_id:
                                            t['status'] = new_status
                                            t['updated_at'] = datetime.now().isoformat()
                                            # If marking as completed, add completed_at timestamp
                                            if new_status == "completed" and not t.get('completed_at'):
                                                t['completed_at'] = datetime.now().isoformat()
                                            updated_task = t
                                            break
                                    task_agent.data_manager.save_data("tasks", all_tasks)
                                    
                                    # Send notifications
                                    notification_agent = agents.get("notification_agent")
                                    if notification_agent and updated_task:
                                        # Get employee name for notification
                                        employees_list = st.session_state.data_manager.load_data("employees") or []
                                        employee = next((e for e in employees_list if e.get("id") == employee_id), None)
                                        employee_name = employee.get('name', 'Employee') if employee else 'Employee'
                                        
                                        # Notify the employee (confirmation)
                                        notification_agent.send_notification(
                                            recipient=employee_id,
                                            title="Task Status Updated",
                                            message=f"Your task '{updated_task.get('title', 'Untitled')}' status has been updated from '{old_status}' to '{new_status}'.",
                                            notification_type="task_status_update",
                                            priority="normal"
                                        )
                                        
                                        # Notify managers/owners about the status change
                                        managers = [e for e in employees_list if e.get("role") in ["manager", "owner"]]
                                        for manager in managers:
                                            manager_id = manager.get("id")
                                            notification_agent.send_notification(
                                                recipient=manager_id,
                                                title=f"Task Status Changed by {employee_name}",
                                                message=f"Employee {employee_name} updated task '{updated_task.get('title', 'Untitled')}' status from '{old_status}' to '{new_status}'.",
                                                notification_type="task_status_update",
                                                priority="normal"
                                            )
                                    
                                    st.session_state[f"updating_status_{task_id}"] = False
                                    st.success(f"✅ Task status updated to '{new_status}'! Notifications sent.")
                                    st.rerun()
                            with col_cancel:
                                if st.form_submit_button("❌ Cancel"):
                                    st.session_state[f"updating_status_{task_id}"] = False
                                    st.rerun()
            
            # Table header - with Actions column for status update
            header_cols = st.columns([3, 1, 1, 1, 1.5])
            with header_cols[0]:
                st.markdown("**Title**")
            with header_cols[1]:
                st.markdown("**Status**")
            with header_cols[2]:
                st.markdown("**Priority**")
            with header_cols[3]:
                st.markdown("**Due Date**")
            with header_cols[4]:
                st.markdown("**Action**")
            
            st.markdown("---")
            
            # Table rows - with Update Status button
            for task in tasks:
                task_id = task.get('id')
                title = task.get('title', 'Untitled')
                status = task.get('status', 'N/A')
                priority = task.get('priority', 'N/A')
                due_date = task.get('due_date', 'N/A')[:10] if task.get('due_date') else 'N/A'
                
                row_cols = st.columns([3, 1, 1, 1, 1.5])
                with row_cols[0]:
                    st.write(f"**{title}**")
                with row_cols[1]:
                    # Show status with color indicator
                    status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
                    emoji = status_emoji.get(status, "📋")
                    st.write(f"{emoji} {status}")
                with row_cols[2]:
                    st.write(priority)
                with row_cols[3]:
                    st.write(due_date)
                with row_cols[4]:
                    if st.button("✏️ Update Status", key=f"update_status_btn_{task_id}", use_container_width=True):
                        st.session_state[f"updating_status_{task_id}"] = True
                        st.rerun()
        else:
            st.info("No tasks found")
    else:
        # Managers and owners use tabs
        with tab1:
            # Managers and owners see all tasks
            tasks = task_agent.get_tasks()
            
            # Debug: Check if tasks are loaded
            if not tasks:
                st.warning(f"⚠️ Debug: task_agent.get_tasks() returned {len(tasks) if tasks else 0} tasks. Data manager loaded: {len(st.session_state.data_manager.load_data('tasks') or [])} tasks from file.")
            
            if tasks:
                # Load employees for name lookup
                employees = st.session_state.data_manager.load_data("employees") or []
                employee_lookup = {e.get("id"): e.get("name", "Unknown") for e in employees}
                
                # Handle edit forms first - only for managers/owners
                for edit_idx, task in enumerate(tasks):
                    task_id = task.get('id')
                    if st.session_state.get(f"editing_task_{task_id}", False):
                        with st.expander(f"✏️ Editing: {task.get('title', 'Untitled')}", expanded=True):
                            with st.form(f"edit_task_form_{edit_idx}_{task_id}"):
                                edit_title = st.text_input("Task Title", value=task.get('title', ''), key=f"edit_task_title_{edit_idx}_{task_id}")
                                edit_description = st.text_area("Description", value=task.get('description', ''), key=f"edit_task_desc_{edit_idx}_{task_id}")
                                edit_priority = st.selectbox("Priority", ["low", "medium", "high"],
                                                            index=["low", "medium", "high"].index(task.get('priority', 'medium')),
                                                            key=f"edit_task_priority_{edit_idx}_{task_id}")
                                edit_status = st.selectbox("Status", ["pending", "in_progress", "completed"],
                                                          index=["pending", "in_progress", "completed"].index(task.get('status', 'pending')),
                                                          key=f"edit_task_status_{edit_idx}_{task_id}")
                                
                                # Managers/owners can edit all fields
                                edit_due_date = st.date_input("Due Date",
                                                             value=datetime.fromisoformat(task.get('due_date')) if task.get('due_date') else None,
                                                             key=f"edit_task_due_{edit_idx}_{task_id}")
                                current_assigned = task.get('assigned_to', '')
                                # Show names instead of IDs in dropdown
                                assigned_options = {f"{e.get('name')} ({e.get('id')})": e.get("id") for e in employees}
                                selected_assigned_name = st.selectbox("Assign To", ["-- Choose employee --"] + list(assigned_options.keys()),
                                                            index=0 if not current_assigned else (list(assigned_options.values()).index(current_assigned) + 1 if current_assigned in assigned_options.values() else 0),
                                                            key=f"edit_task_assigned_{edit_idx}_{task_id}")
                                edit_assigned = assigned_options.get(selected_assigned_name) if selected_assigned_name and selected_assigned_name != "-- Choose employee --" else ""
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Save Changes", key=f"save_task_btn_{edit_idx}_{task_id}"):
                                        # Role-based update restrictions
                                        if user_role in ["owner", "manager"]:
                                            # Managers/owners can update all fields
                                            task['title'] = edit_title
                                            task['description'] = edit_description
                                            task['priority'] = edit_priority
                                            task['status'] = edit_status
                                            task['due_date'] = edit_due_date.isoformat() if edit_due_date else None
                                            task['assigned_to'] = edit_assigned if edit_assigned else None
                                        else:
                                            # Employees can only update status
                                            if task.get("assigned_to") == user_email:
                                                task['status'] = edit_status
                                            else:
                                                st.error("❌ You can only update tasks assigned to you.")
                                                st.rerun()
                                                return
                                        
                                        task['updated_at'] = datetime.now().isoformat()
                                        task_agent.data_manager.save_data("tasks", task_agent.data_manager.load_data("tasks") or [])
                                        st.session_state[f"editing_task_{task_id}"] = False
                                        st.success("Task updated!")
                                        st.rerun()
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel", key=f"cancel_task_btn_{edit_idx}_{task_id}"):
                                        st.session_state[f"editing_task_{task_id}"] = False
                                        st.rerun()
            
                # Table header
                header_cols = st.columns([0.5, 2, 1, 1, 1, 2, 1.5])
                with header_cols[0]:
                    st.markdown("**#**")
                with header_cols[1]:
                    st.markdown("**Title**")
                with header_cols[2]:
                    st.markdown("**Status**")
                with header_cols[3]:
                    st.markdown("**Priority**")
                with header_cols[4]:
                    st.markdown("**Due Date**")
                with header_cols[5]:
                    st.markdown("**Assigned To**")
                with header_cols[6]:
                    st.markdown("**Actions**")
                
                st.markdown("---")
                
                # Table rows with action buttons
                for idx, task in enumerate(tasks):
                    task_id = task.get('id')
                    title = task.get('title', 'Untitled')
                    status = task.get('status', 'N/A')
                    priority = task.get('priority', 'N/A')
                    due_date = task.get('due_date', 'N/A')[:10] if task.get('due_date') else 'N/A'
                    assigned_to_id = task.get('assigned_to', '')
                    # Show employee name instead of ID
                    assigned_to = employee_lookup.get(assigned_to_id, assigned_to_id if assigned_to_id else 'Unassigned')
                    
                    row_cols = st.columns([0.5, 2, 1, 1, 1, 2, 1.5])
                    with row_cols[0]:
                        st.write(f"**{idx + 1}**")
                    with row_cols[1]:
                        st.write(f"**{title}**")
                    with row_cols[2]:
                        st.write(status)
                    with row_cols[3]:
                        st.write(priority)
                    with row_cols[4]:
                        st.write(due_date)
                    with row_cols[5]:
                        st.write(assigned_to)
                    with row_cols[6]:
                        if user_role in ["owner", "manager"]:
                            # Managers and owners can edit/delete
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                if st.button("✏️ Edit", key=f"view_tasks_edit_{idx}_{task_id}", use_container_width=True):
                                    st.session_state[f"editing_task_{task_id}"] = True
                                    st.rerun()
                            with btn_col2:
                                if st.button("🗑️ Del", key=f"view_tasks_delete_{idx}_{task_id}", use_container_width=True, type="secondary"):
                                    if task_agent.delete_task(task_id):
                                        st.success("Task deleted!")
                                    st.rerun()
            else:
                st.info("No tasks found")
    
    if tab2:
        with tab2:
            # Only managers and owners can create tasks
            if user_role not in ["owner", "manager"]:
                st.warning("⚠️ Only managers and owners can create tasks.")
            else:
                with st.form("create_task"):
                    title = st.text_input("Task Title *")
                    description = st.text_area("Description")
                    priority = st.selectbox("Priority", ["low", "medium", "high"], key="create_task_priority")
                    status = st.selectbox("Status", ["pending", "in_progress", "completed"], key="create_task_status")
                    due_date = st.date_input("Due Date")
                    
                    # Add project selection
                    projects = st.session_state.data_manager.load_data("projects") or []
                    project_options = {f"{p.get('name')} ({p.get('id')})": p.get("id") for p in projects}
                    selected_project_name = st.selectbox("Project (Optional)", ["-- Choose from projects --"] + list(project_options.keys()), key="create_task_project", help="Link this task to a project")
                    project_id = project_options.get(selected_project_name) if selected_project_name and selected_project_name != "-- Choose from projects --" else None
                    
                    employees = st.session_state.data_manager.load_data("employees") or []
                    # Show names instead of IDs in dropdown
                    assigned_options = {e.get('name', f"Employee {e.get('id')}"): e.get("id") for e in employees}
                    selected_assigned_name = st.selectbox("Assign To", ["-- Choose employee --"] + list(assigned_options.keys()), key="create_task_assigned")
                    assigned_to = assigned_options.get(selected_assigned_name) if selected_assigned_name and selected_assigned_name != "-- Choose employee --" else ""
                    
                    if st.form_submit_button("Create Task"):
                        if title:
                            result = task_agent.create_task({
                                "title": title,
                                "description": description,
                                "priority": priority,
                                "due_date": due_date.isoformat() if due_date else None,
                                "assigned_to": assigned_to if assigned_to else None,
                                "project_id": project_id
                            })
                            if result.get("success"):
                                st.session_state.show_tasks_view = True
                                st.rerun()
                            else:
                                st.error(result.get("error"))
    
# Employees page
def employees_page():
    """Employees management page"""
    st.title("👥 Employees")
    st.markdown("---")
    
    # Role-based access control - Employees cannot access
    user_role = st.session_state.user.get("role", "employee")
    if user_role == "employee":
        st.error("❌ Access Denied: You don't have permission to access this page.")
        st.info("💡 Employees cannot view or manage the employee list.")
        return
    
    data_manager = st.session_state.data_manager
    employees = data_manager.load_data("employees") or []
    
    # Check if we should show view after creation
    show_view_after_create = st.session_state.get("show_employees_view", False)
    
    if show_view_after_create:
        st.session_state.show_employees_view = False
        st.success("✅ Employee created successfully! Viewing all employees below.")
        st.markdown("---")
        # Show view content immediately
        employees = data_manager.load_data("employees") or []
        if employees:
            df = pd.DataFrame(employees)
            st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.markdown("### Or use tabs below to navigate")
    
    tab1, tab2 = st.tabs(["View Employees", "Create Employee"])
    
    with tab1:
        if employees:
            for employee in employees:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"### {employee.get('name', 'Unknown')}")
                        st.write(f"**Email:** {employee.get('email', 'N/A')} | **Position:** {employee.get('position', 'N/A')}")
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_employee_{employee.get('id')}", use_container_width=True):
                            st.session_state[f"editing_employee_{employee.get('id')}"] = True
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️ Del", key=f"delete_employee_{employee.get('id')}", use_container_width=True, type="secondary"):
                            employees = [e for e in employees if e.get("id") != employee.get("id")]
                            data_manager.save_data("employees", employees)
                            st.success("Employee deleted!")
                            st.rerun()
        
                    # Edit form
                    if st.session_state.get(f"editing_employee_{employee.get('id')}", False):
                        with st.form(f"edit_employee_form_{employee.get('id')}"):
                            edit_name = st.text_input("Name", value=employee.get('name', ''))
                            edit_email = st.text_input("Email", value=employee.get('email', ''))
                            edit_position = st.text_input("Position", value=employee.get('position', ''))
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Save Changes"):
                                    employee['name'] = edit_name
                                    employee['email'] = edit_email
                                    employee['position'] = edit_position
                                    employee['updated_at'] = datetime.now().isoformat()
                                    data_manager.save_data("employees", employees)
                                    st.session_state[f"editing_employee_{employee.get('id')}"] = False
                                    st.success("Employee updated!")
                                    st.rerun()
                            with col_cancel:
                                if st.form_submit_button("❌ Cancel"):
                                    st.session_state[f"editing_employee_{employee.get('id')}"] = False
                                    st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No employees found")
    
    if tab2:
        with tab2:
            # Only managers and owners can create employees
            if user_role not in ["owner", "manager"]:
                st.warning("⚠️ Only managers and owners can create employees.")
            else:
                with st.form("create_employee"):
                    name = st.text_input("Name *")
                    email = st.text_input("Email *")
                    position = st.text_input("Position")
                    
                    if st.form_submit_button("Create Employee"):
                        if name and email:
                            new_employee = {
                                "id": str(len(employees) + 1),
                                "name": name,
                                "email": email,
                                "position": position,
                                "created_at": datetime.now().isoformat(),
                                "updated_at": datetime.now().isoformat()
                            }
                            employees.append(new_employee)
                            data_manager.save_data("employees", employees)
                            st.session_state.show_employees_view = True
                            st.rerun()

# Performance page
def performance_page():
    """Performance evaluation page"""
    st.title("📈 Performance")
    st.markdown("---")
    
    # Role-based access control
    user_role = st.session_state.user.get("role", "employee")
    user_email = st.session_state.user.get("email")
    
    agents = initialize_agents()
    performance_agent = agents["performance_agent"]
    
    employees = st.session_state.data_manager.load_data("employees") or []
    
    # Role-based employee selection
    if user_role == "employee":
        # Employees can only view their own performance
        employee = next((e for e in employees if e.get("email") == user_email), None)
        if employee:
            selected_employee = f"{employee.get('name')} ({employee.get('id')})"
            st.info("👤 Viewing your own performance")
        else:
            st.error("❌ Employee record not found.")
            return
    else:
        # Managers and owners can select any employee
        selected_employee = st.selectbox("Select Employee", ["-- Choose employee --"] + [f"{e.get('name')} ({e.get('id')})" for e in employees], key="performance_employee_select")
    
    if selected_employee and selected_employee != "-- Choose employee --" and "(" in selected_employee:
        employee_id = selected_employee.split("(")[1].split(")")[0]
        
        # Role-based evaluation button
        if user_role == "employee":
            # Employees can view but not evaluate
            st.info("💡 Performance evaluation is done by managers. You can view your performance history below and add your self-assessment.")
            
            # Automatically load and display performance data for employees
            evaluation = performance_agent.evaluate_employee(employee_id, save=False)
            
            # Self-Assessment Section for Employees
            st.markdown("---")
            st.subheader("📝 Self-Assessment / Self Review")
            st.write("Evaluate your own performance and add remarks supporting your achievements.")
            
            with st.expander("➕ Add Self-Assessment", expanded=False):
                with st.form("self_assessment_form"):
                    assessment_period = st.selectbox("Assessment Period", 
                        ["Current Month", "Last Month", "Last Quarter", "Last 6 Months", "This Year"],
                        key="self_assessment_period")
                    
                    strengths = st.text_area("Your Strengths & Achievements *", 
                        placeholder="Describe your key strengths, achievements, and what you've done well...",
                        help="Highlight your accomplishments and areas where you excel")
                    
                    areas_for_improvement = st.text_area("Areas for Improvement", 
                        placeholder="What areas would you like to improve? What challenges are you facing?",
                        help="Identify areas where you want to grow or need support")
                    
                    goals_progress = st.text_area("Goals & Progress Notes", 
                        placeholder="How are you progressing on your goals? Any milestones reached?",
                        help="Share updates on your goal progress and milestones")
                    
                    additional_remarks = st.text_area("Additional Remarks", 
                        placeholder="Any other comments, feedback, or insights about your performance...",
                        help="Add any additional thoughts or context about your performance")
                    
                    if st.form_submit_button("💾 Submit Self-Assessment"):
                        if strengths and strengths.strip():
                            # Save self-assessment
                            self_assessments = st.session_state.data_manager.load_data("self_assessments") or []
                            
                            assessment = {
                                "id": f"self_assessment_{len(self_assessments) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "employee_id": employee_id,
                                "employee_email": user_email,
                                "assessment_period": assessment_period,
                                "strengths": strengths.strip(),
                                "areas_for_improvement": areas_for_improvement.strip() if areas_for_improvement else "",
                                "goals_progress": goals_progress.strip() if goals_progress else "",
                                "additional_remarks": additional_remarks.strip() if additional_remarks else "",
                                "created_at": datetime.now().isoformat(),
                                "status": "submitted"
                            }
                            
                            self_assessments.append(assessment)
                            st.session_state.data_manager.save_data("self_assessments", self_assessments)
                            st.success("✅ Self-assessment submitted successfully! Your manager will be able to review it.")
                            st.rerun()
                        else:
                            st.error("❌ Please provide at least your strengths and achievements.")
            
            # Show previous self-assessments
            self_assessments = st.session_state.data_manager.load_data("self_assessments") or []
            employee_assessments = [a for a in self_assessments if a.get("employee_id") == employee_id]
            employee_assessments.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            if employee_assessments:
                st.markdown("---")
                st.subheader("📋 Your Previous Self-Assessments")
                for assessment in employee_assessments[:5]:  # Show last 5
                    with st.expander(f"> {assessment.get('assessment_period')} - {assessment.get('created_at', '')[:10]}"):
                        st.write(f"**Period:** {assessment.get('assessment_period')}")
                        st.write(f"**Submitted:** {assessment.get('created_at', 'N/A')[:19]}")
                        st.markdown("---")
                        st.write("**Strengths & Achievements:**")
                        st.write(assessment.get('strengths', 'N/A'))
                        if assessment.get('areas_for_improvement'):
                            st.markdown("---")
                            st.write("**Areas for Improvement:**")
                            st.write(assessment.get('areas_for_improvement'))
                        if assessment.get('goals_progress'):
                            st.markdown("---")
                            st.write("**Goals & Progress:**")
                            st.write(assessment.get('goals_progress'))
                        if assessment.get('additional_remarks'):
                            st.markdown("---")
                            st.write("**Additional Remarks:**")
                            st.write(assessment.get('additional_remarks'))
            else:
                st.info("📝 No self-assessments submitted yet. Add your first self-assessment above.")
        else:
            # Managers and owners can evaluate
            if st.button("Evaluate Performance"):
                with st.spinner("Evaluating performance..."):
                    evaluation = performance_agent.evaluate_employee(employee_id, save=True)
                    st.success("✅ Performance evaluated successfully!")
            else:
                # Show existing evaluation if available
                evaluation = performance_agent.evaluate_employee(employee_id, save=False)
        
        # Display performance metrics (for both employees and managers)
        if evaluation:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Performance Score", f"{evaluation.get('performance_score', 0):.1f}")
            with col2:
                st.metric("Completion Rate", f"{evaluation.get('completion_rate', 0):.1f}%")
            with col3:
                st.metric("On-Time Rate", f"{evaluation.get('on_time_rate', 0):.1f}%")
            with col4:
                st.metric("Rank", f"#{evaluation.get('rank', 'N/A')}")
            
            st.markdown("---")
            st.subheader("Performance Details")
            display_as_table(evaluation)
            
            # Performance history chart
            history = performance_agent.get_employee_performance_history(employee_id)
            if len(history) > 1:
                df_history = pd.DataFrame(history)
                df_history['evaluated_at'] = pd.to_datetime(df_history['evaluated_at'])
                
                fig = px.line(df_history, x="evaluated_at", y="performance_score",
                            title="Performance Trend Over Time",
                            labels={"evaluated_at": "Date", "performance_score": "Performance Score"},
                            color_discrete_sequence=['#00E0FF'])
                fig.update_traces(mode='lines+markers', line=dict(width=3, color='#00E0FF'), marker=dict(size=8, color='#14F1FF'))
                fig.update_layout(
                    plot_bgcolor='#111729',
                    paper_bgcolor='#111729',
                    font_color='#FFFFFF',
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Additional metrics charts
                col1, col2 = st.columns(2)
                with col1:
                    fig2 = px.bar(df_history, x="evaluated_at", y="completion_rate",
                                title="Completion Rate Trend",
                                color_discrete_sequence=['#00E0FF'])
                    fig2.update_layout(
                        plot_bgcolor='#111729',
                        paper_bgcolor='#111729',
                        font_color='#FFFFFF',
                        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                with col2:
                    fig3 = px.bar(df_history, x="evaluated_at", y="on_time_rate",
                                title="On-Time Rate Trend",
                                color_discrete_sequence=['#00E0FF'])
                    fig3.update_layout(
                        plot_bgcolor='#111729',
                        paper_bgcolor='#111729',
                        font_color='#FFFFFF',
                        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                    )
                    st.plotly_chart(fig3, use_container_width=True)
            elif len(history) == 1:
                st.info("📊 Only one performance evaluation available. More data will be shown as evaluations are added.")
            else:
                st.info("📊 No performance history available yet. Performance will be tracked as you complete tasks.")

# Employee Dashboard page
def employee_dashboard_page():
    """Employee self-service dashboard"""
    st.title("👤 My Dashboard")
    st.markdown("---")
    
    if not st.session_state.user:
        st.warning("Please log in to view your dashboard")
        return
    
    user_email = st.session_state.user.get("email")
    user_role = st.session_state.user.get("role", "employee")
    
    # Get employee record by email to get employee ID
    employees = st.session_state.data_manager.load_data("employees") or []
    employee = next((e for e in employees if e.get("email") == user_email), None)
    
    # If no employee record found, check if user is Owner/Manager
    if not employee:
        if user_role in ["owner", "manager"]:
            # Owners/Managers can view a system overview dashboard
            st.info("ℹ️ You don't have an employee record. Showing system overview instead.")
            st.markdown("---")
            
            agents = initialize_agents()
            task_agent = agents["task_agent"]
            performance_agent = agents["performance_agent"]
            
            # System-wide metrics for Owners/Managers
            all_tasks = task_agent.get_tasks()
            all_employees = st.session_state.data_manager.load_data("employees") or []
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Employees", len(all_employees))
            with col2:
                total_tasks = len(all_tasks)
                completed_tasks = len([t for t in all_tasks if t.get("status") == "completed"])
                st.metric("Tasks Completed", f"{completed_tasks}/{total_tasks}")
            with col3:
                active_tasks = len([t for t in all_tasks if t.get("status") == "in_progress"])
                st.metric("Active Tasks", active_tasks)
            with col4:
                pending_tasks = len([t for t in all_tasks if t.get("status") == "pending"])
                st.metric("Pending Tasks", pending_tasks)
            
            st.markdown("---")
            st.subheader("📊 System Overview")
            st.write("As an Owner/Manager, you can view detailed analytics and reports from the main Dashboard page.")
            st.write("To view personal metrics, please ensure you have an employee record created.")
            return
        else:
            # Regular employees must have an employee record
            st.error("❌ Employee record not found. Please contact your administrator.")
            return
    
    employee_id = employee.get("id")
    user_id = employee_id  # Use employee ID for performance evaluation
    
    agents = initialize_agents()
    achievement_agent = agents["achievement_agent"]
    performance_agent = agents["performance_agent"]
    task_agent = agents["task_agent"]
    
    tab1, tab2, tab3 = st.tabs(["Overview", "Achievements", "Performance History"])
    
    with tab1:
        st.subheader("Performance Overview")
        
        # Get current performance - DON'T save, just read existing data
        evaluation = performance_agent.evaluate_employee(employee_id, save=False)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Performance Score", f"{evaluation.get('performance_score', 0):.1f}")
        with col2:
            st.metric("Completion Rate", f"{evaluation.get('completion_rate', 0):.1f}%")
        with col3:
            st.metric("On-Time Rate", f"{evaluation.get('on_time_rate', 0):.1f}%")
        with col4:
            st.metric("Rank", f"#{evaluation.get('rank', 'N/A')}")
        
        st.markdown("---")
        
        # Recent tasks - use employee ID, not email
        st.subheader("Recent Tasks")
        my_tasks = task_agent.get_tasks({"assigned_to": employee_id})
        if my_tasks:
            recent_tasks = sorted(my_tasks, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
            for task in recent_tasks:
                status_emoji = {"completed": "✅", "in_progress": "🔄", "pending": "⏳"}
                st.write(f"{status_emoji.get(task.get('status'), '📋')} **{task.get('title')}** - {task.get('status', 'N/A')}")
                if task.get('due_date'):
                    st.write(f"   *Due: {task.get('due_date')}*")
        else:
            st.info("No tasks assigned")
        
    st.markdown("---")
    
    # Achievement summary
    st.subheader("Achievement Summary")
    achievement_stats = achievement_agent.get_achievement_statistics(employee_id)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Achievements", achievement_stats.get("total_achievements", 0))
    with col2:
        st.metric("Verified", achievement_stats.get("verified_achievements", 0))
    with col3:
        st.metric("Recent (30 days)", achievement_stats.get("recent_achievements", 0))
    
    with tab2:
        st.subheader("Log Achievements")
        
        with st.form("log_achievement_form"):
            achievement_title = st.text_input("Achievement Title *")
            achievement_desc = st.text_area("Description")
            achievement_category = st.selectbox("Category", 
                                               ["task_completion", "project_milestone", "skill_development", "general"],
                                               key="create_achievement_category")
            achievement_impact = st.selectbox("Impact", ["low", "medium", "high"], key="create_achievement_impact")
            
            # Task completion shortcut
            my_tasks = task_agent.get_tasks({"assigned_to": employee_id})
            if my_tasks:
                completed_tasks = [t for t in my_tasks if t.get("status") == "completed"]
                if completed_tasks:
                    st.markdown("**Or log task completion:**")
                    task_to_log = st.selectbox("Select Completed Task", 
                                              ["-- Choose task --"] + [f"{t.get('title')} (ID: {t.get('id')})" for t in completed_tasks],
                                              key="log_task_completion_select")
                    if task_to_log and task_to_log != "-- Choose task --":
                        task_id = task_to_log.split("ID: ")[1].split(")")[0]
                        completion_notes = st.text_area("Completion Notes", key="task_completion_notes")
            
            if st.form_submit_button("📝 Log Achievement"):
                if achievement_title:
                    result = achievement_agent.log_achievement(employee_id, {
                        "title": achievement_title,
                        "description": achievement_desc,
                        "category": achievement_category,
                        "impact": achievement_impact
                    })
                    if result.get("success"):
                        st.success("✅ Achievement logged successfully!")
                        st.rerun()
                elif task_to_log:
                    result = achievement_agent.log_task_completion(employee_id, task_id, completion_notes)
                    if result.get("success"):
                        st.success("✅ Task completion logged as achievement!")
                st.rerun()
        
        st.markdown("---")
        st.subheader("My Achievements")
        
        achievement_category_filter = st.selectbox("Filter by Category", 
                                                   ["All"] + ["task_completion", "project_milestone", "skill_development", "general"],
                                                   key="ach_filter")
        
        achievements = achievement_agent.get_employee_achievements(
            user_id, 
            category=achievement_category_filter if achievement_category_filter != "All" else None
        )
        
        if achievements:
            for achievement in achievements:
                verified_badge = "✅ Verified" if achievement.get("verified") else "⏳ Pending"
                impact_emoji = {"high": "🔥", "medium": "⭐", "low": "📌"}
                
                # Create styled achievement card
                achievement_html = f"""
                <div class="achievement-item">
                    <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{impact_emoji.get(achievement.get('impact'), '📌')}</span>
                        <h3 style="color: #FFFFFF; margin: 0; flex: 1;">{achievement.get('title')}</h3>
                        <span style="color: #00E0FF; font-weight: 500;">{verified_badge}</span>
                    </div>
                    <div style="color: #94A3B8; margin-bottom: 0.5rem; font-size: 0.95rem;">
                        <strong>Category:</strong> {achievement.get('category', 'N/A')} | 
                        <strong>Impact:</strong> {achievement.get('impact', 'N/A')}
                    </div>
                    {f'<div style="color: #94A3B8; opacity: 0.9; margin-bottom: 0.5rem; font-style: italic;">{achievement.get("description")}</div>' if achievement.get('description') else ''}
                    <div style="color: #94A3B8; opacity: 0.7; font-size: 0.85rem;">
                        <strong>Date:</strong> {achievement.get('created_at', 'N/A')}
                    </div>
                </div>
                """
                st.markdown(achievement_html, unsafe_allow_html=True)
        else:
            st.info("No achievements logged yet")
    
    with tab3:
        st.subheader("Performance History & Trends")
        
        # Performance history chart
        history = performance_agent.get_employee_performance_history(user_id)
        if len(history) > 1:
            df_history = pd.DataFrame(history)
            df_history['evaluated_at'] = pd.to_datetime(df_history['evaluated_at'])
            
            # Interactive trend chart
            fig = px.line(df_history, x="evaluated_at", y="performance_score",
                         title="Performance Score Trend Over Time",
                         labels={"evaluated_at": "Date", "performance_score": "Performance Score"},
                         color_discrete_sequence=['#00E0FF'])
            fig.update_traces(mode='lines+markers', line=dict(width=3, color='#00E0FF'), marker=dict(size=8, color='#14F1FF'))
            fig.update_layout(
                hovermode='x unified',
                plot_bgcolor='#111729',
                paper_bgcolor='#111729',
                font_color='#FFFFFF',
                xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional metrics
            col1, col2 = st.columns(2)
            with col1:
                fig2 = px.bar(df_history, x="evaluated_at", y="completion_rate",
                            title="Completion Rate Trend",
                            color_discrete_sequence=['#00E0FF'])
                fig2.update_layout(
                    plot_bgcolor='#111729',
                    paper_bgcolor='#111729',
                    font_color='#FFFFFF',
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                fig3 = px.bar(df_history, x="evaluated_at", y="on_time_rate",
                            title="On-Time Rate Trend",
                            color_discrete_sequence=['#00E0FF'])
                fig3.update_layout(
                    plot_bgcolor='#111729',
                    paper_bgcolor='#111729',
                    font_color='#FFFFFF',
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                )
                st.plotly_chart(fig3, use_container_width=True)
            
            # Historical comparison
            st.subheader("Historical Comparison")
            if len(history) >= 2:
                latest = history[0]
                previous = history[1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    perf_change = latest.get("performance_score", 0) - previous.get("performance_score", 0)
                    st.metric("Performance Score", 
                            f"{latest.get('performance_score', 0):.1f}",
                            delta=f"{perf_change:+.1f}")
                with col2:
                    comp_change = latest.get("completion_rate", 0) - previous.get("completion_rate", 0)
                    st.metric("Completion Rate",
                            f"{latest.get('completion_rate', 0):.1f}%",
                            delta=f"{comp_change:+.1f}%")
                with col3:
                    ontime_change = latest.get("on_time_rate", 0) - previous.get("on_time_rate", 0)
                    st.metric("On-Time Rate",
                            f"{latest.get('on_time_rate', 0):.1f}%",
                            delta=f"{ontime_change:+.1f}%")
            else:
                st.info("Not enough performance history data. Complete more tasks to see trends!")
                
# Analytics page
def analytics_page():
    """Analytics and insights page with predictive reports and correlation analysis"""
    st.title("🔍 Analytics & Insights")
    st.markdown("---")
    
    agents = initialize_agents()
    user_role = st.session_state.user.get("role", "employee")
    
    # Only managers and owners can access advanced analytics
    if user_role not in ["owner", "manager"]:
        st.warning("⚠️ Advanced analytics are only available to managers and owners.")
        return
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Predictive Reports", "Correlation Analysis", "Trend Analysis", "AI Insights"])
    
    with tab1:
        overview = agents["reporting_agent"].generate_overview_report()
        st.subheader("System Overview")
        display_as_table(overview)
    
    with tab2:
        st.subheader("Predictive Reports - Capacity & Risk Forecasting")
        
        sub_tab1, sub_tab2 = st.tabs(["Capacity Forecast", "Project Risk Forecast"])
        
        with sub_tab1:
            st.markdown("#### Employee/Team Capacity Forecasting")
            
            forecast_type = st.radio("Forecast Type", ["Individual Employee", "Team"], horizontal=True, key="forecast_type_radio")
            weeks = st.slider("Forecast Period (weeks)", 1, 12, 4, key="forecast_weeks_slider")
            
            if forecast_type == "Individual Employee":
                employees = st.session_state.data_manager.load_data("employees") or []
                selected_employee = st.selectbox("Select Employee",
                                                ["-- Choose employee --"] + [f"{e.get('name')} ({e.get('id')})" for e in employees],
                                                key="capacity_forecast_employee")
                
                if selected_employee and selected_employee != "-- Choose employee --" and "(" in selected_employee and st.button("📊 Generate Capacity Forecast"):
                    employee_id = selected_employee.split("(")[1].split(")")[0]
                    forecast = agents["predictive_analytics_agent"].forecast_capacity(employee_id, weeks)
                    
                    st.success("✅ Capacity forecast generated!")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Current Workload", forecast.get("current_workload", 0))
                    with col2:
                        st.metric("Tasks/Week", forecast.get("tasks_per_week", 0))
                    with col3:
                        st.metric("Forecasted Capacity", f"{forecast.get('forecasted_capacity', 0):.1f}")
                    with col4:
                        st.metric("Available Capacity", f"{forecast.get('available_capacity', 0):.1f}")
                    
                    st.metric("Utilization Rate", f"{forecast.get('utilization_rate', 0):.1f}%")
                    st.info(f"💡 **Recommendation:** {forecast.get('recommendation', 'N/A')}")
            else:
                if st.button("📊 Generate Team Capacity Forecast"):
                    forecast = agents["predictive_analytics_agent"].forecast_capacity(None, weeks)
                    
                    st.success("✅ Team capacity forecast generated!")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Employees", forecast.get("total_employees", 0))
                    with col2:
                        st.metric("Total Capacity", f"{forecast.get('total_capacity', 0):.1f}")
                    with col3:
                        st.metric("Total Workload", forecast.get("total_workload", 0))
                    with col4:
                        st.metric("Available Capacity", f"{forecast.get('total_available_capacity', 0):.1f}")
                    
                    st.metric("Team Utilization", f"{forecast.get('team_utilization_rate', 0):.1f}%")
                    
                    # Employee breakdown
                    if forecast.get("employee_forecasts"):
                        st.subheader("Employee Breakdown")
                        df_forecast = pd.DataFrame(forecast["employee_forecasts"])
                        st.dataframe(df_forecast[["employee_id", "current_workload", "forecasted_capacity", 
                                                 "available_capacity", "utilization_rate"]], use_container_width=True)
        
        with sub_tab2:
            st.markdown("#### Project Risk Forecasting")
            
            projects = st.session_state.data_manager.load_data("projects") or []
            selected_project = st.selectbox("Select Project",
                                           ["-- Choose project --"] + [f"{p.get('name')} (ID: {p.get('id')})" for p in projects],
                                           key="risk_forecast_project")
            
            if selected_project and selected_project != "-- Choose project --" and st.button("⚠️ Analyze Project Risk"):
                project_id = selected_project.split("ID: ")[1].split(")")[0]
                risk_forecast = agents["predictive_analytics_agent"].forecast_project_risk(project_id)
                
                if risk_forecast.get("success") is False:
                    st.error(risk_forecast.get("error", "Failed to analyze risk"))
                else:
                    st.success("✅ Risk analysis completed!")
                    
                    risk_level = risk_forecast.get("risk_level", "low")
                    risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Completion Rate", f"{risk_forecast.get('completion_rate', 0):.1f}%")
                    with col2:
                        st.metric("Risk Score", f"{risk_forecast.get('overall_risk_score', 0):.1f}/100")
                    with col3:
                        st.metric("Risk Level", f"{risk_emoji.get(risk_level, '⚪')} {risk_level.title()}")
                    
                    st.markdown("**Risk Breakdown:**")
                    st.write(f"- **Deadline Risk:** {risk_forecast.get('deadline_risk', 'N/A').title()}")
                    st.write(f"- **Resource Risk:** {risk_forecast.get('resource_risk', 'N/A').title()}")
                    
                    st.markdown("**Recommendations:**")
                    for rec in risk_forecast.get("recommendations", []):
                        st.write(f"- {rec}")
    
    with tab3:
        st.subheader("Correlation Analysis Between Metrics")
        st.markdown("Analyze relationships between different performance metrics")
        
        employees = st.session_state.data_manager.load_data("employees") or []
        selected_employees = st.multiselect("Select Employees (leave empty for all)",
                                            [e.get("id") for e in employees],
                                            key="correlation_employees_select")
        
        available_metrics = [
            "performance_score",
            "completion_rate",
            "on_time_rate",
            "total_tasks",
            "completed_tasks",
            "overdue_tasks"
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            metric1 = st.selectbox("First Metric", available_metrics, key="correlation_metric1")
        with col2:
            metric2 = st.selectbox("Second Metric", available_metrics, key="correlation_metric2")
        
        if metric1 == metric2:
            st.warning("⚠️ Please select two different metrics")
        elif st.button("🔗 Analyze Correlation"):
            correlation_result = agents["correlation_agent"].analyze_correlation(
                metric1, metric2, selected_employees if selected_employees else None
            )
            
            if correlation_result.get("success"):
                st.success("✅ Correlation analysis completed!")
                
                corr_coef = correlation_result.get("correlation_coefficient", 0)
                strength = correlation_result.get("correlation_strength", "unknown")
                direction = correlation_result.get("correlation_direction", "none")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Correlation Coefficient", f"{corr_coef:.4f}")
                with col2:
                    st.metric("Strength", strength.title())
                with col3:
                    st.metric("Direction", direction.title())
                
                st.info(f"💡 **Interpretation:** {correlation_result.get('interpretation', 'N/A')}")
                
                # Visualization
                if correlation_result.get("data"):
                    df_corr = pd.DataFrame(correlation_result["data"])
                    fig = px.scatter(df_corr, x=metric1, y=metric2,
                                    hover_data=["employee_name"],
                                    title=f"Correlation: {metric1} vs {metric2}",
                                    labels={metric1: metric1.replace("_", " ").title(),
                                           metric2: metric2.replace("_", " ").title()},
                                    color_discrete_sequence=['#00E0FF'])
                    fig.update_traces(marker=dict(size=10, color='#00E0FF'))
                    fig.update_layout(
                        plot_bgcolor='#111729',
                        paper_bgcolor='#111729',
                        font_color='#FFFFFF',
                        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Data table
                    st.subheader("Data Points")
                    st.dataframe(df_corr, use_container_width=True)
            else:
                st.error(correlation_result.get("error", "Failed to analyze correlation"))
    
    with tab4:
        st.subheader("Interactive Trend Analysis")
        st.markdown("View performance trends over time with drill-down capabilities")
        
        employees = st.session_state.data_manager.load_data("employees") or []
        selected_employee = st.selectbox("Select Employee",
                                        ["-- Choose employee --"] + [f"{e.get('name')} ({e.get('id')})" for e in employees],
                                        key="trend_analysis_employee")
        
        if selected_employee and selected_employee != "-- Choose employee --" and "(" in selected_employee:
            employee_id = selected_employee.split("(")[1].split(")")[0]
            
            # Get performance history
            history = agents["performance_agent"].get_employee_performance_history(employee_id)
            
            if len(history) > 1:
                df_history = pd.DataFrame(history)
                df_history['evaluated_at'] = pd.to_datetime(df_history['evaluated_at'])
                
                # Metric selection
                metric_options = {
                    "Performance Score": "performance_score",
                    "Completion Rate": "completion_rate",
                    "On-Time Rate": "on_time_rate",
                    "Total Tasks": "total_tasks",
                    "Completed Tasks": "completed_tasks"
                }
                
                selected_metric = st.selectbox("Select Metric to Analyze", list(metric_options.keys()), key="trend_metric_select")
                metric_key = metric_options[selected_metric]
                
                # Chart type
                chart_type = st.radio("Chart Type", ["Line", "Bar", "Area"], horizontal=True, key="chart_type_radio")
                
                # Generate chart
                if chart_type == "Line":
                    fig = px.line(df_history, x="evaluated_at", y=metric_key,
                                title=f"{selected_metric} Trend Over Time",
                                labels={"evaluated_at": "Date", metric_key: selected_metric},
                                color_discrete_sequence=['#00E0FF'])
                    fig.update_traces(mode='lines+markers', line=dict(width=3, color='#00E0FF'), marker=dict(size=8, color='#14F1FF'))
                elif chart_type == "Bar":
                    fig = px.bar(df_history, x="evaluated_at", y=metric_key,
                               title=f"{selected_metric} Trend Over Time",
                               labels={"evaluated_at": "Date", metric_key: selected_metric},
                               color_discrete_sequence=['#00E0FF'])
                else:  # Area
                    fig = px.area(df_history, x="evaluated_at", y=metric_key,
                                title=f"{selected_metric} Trend Over Time",
                                labels={"evaluated_at": "Date", metric_key: selected_metric},
                                color_discrete_sequence=['#00E0FF'])
                
                fig.update_layout(
                    hovermode='x unified', 
                    xaxis_title="Date", 
                    yaxis_title=selected_metric,
                    plot_bgcolor='#111729',
                    paper_bgcolor='#111729',
                    font_color='#FFFFFF',
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Multi-metric comparison
                st.subheader("Multi-Metric Comparison")
                selected_metrics = st.multiselect("Select Metrics to Compare",
                                                 list(metric_options.keys()),
                                                 default=["Performance Score", "Completion Rate"],
                                                 key="trend_metrics_multiselect")
                
                if selected_metrics:
                    fig_multi = go.Figure()
                    colors = ['#00E0FF', '#14F1FF', '#3B82F6', '#00FFA6']
                    for i, metric_name in enumerate(selected_metrics):
                        metric_key = metric_options[metric_name]
                        fig_multi.add_trace(go.Scatter(
                            x=df_history['evaluated_at'],
                            y=df_history[metric_key],
                            mode='lines+markers',
                            name=metric_name,
                            line=dict(width=3, color=colors[i % len(colors)]),
                            marker=dict(size=8, color=colors[i % len(colors)])
                        ))
                    
                    fig_multi.update_layout(
                        title="Multi-Metric Trend Comparison",
                        xaxis_title="Date",
                        yaxis_title="Value",
                        hovermode='x unified',
                        plot_bgcolor='#111729',
                        paper_bgcolor='#111729',
                        font_color='#FFFFFF',
                        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                    )
                    st.plotly_chart(fig_multi, use_container_width=True)
                
                # Export chart
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Export Chart Data (CSV)"):
                        csv = df_history.to_csv(index=False)
                        st.download_button("Download CSV", csv, 
                                         file_name=f"trend_data_{employee_id}_{datetime.now().strftime('%Y%m%d')}.csv",
                                         mime="text/csv")
            else:
                st.info("Not enough historical data for trend analysis")
    
    with tab5:
        employees = st.session_state.data_manager.load_data("employees") or []
        selected_employee = st.selectbox("Select Employee for Insights", 
                                        ["-- Choose employee --"] + [f"{e.get('name')} ({e.get('id')})" for e in employees],
                                        key="insights_employee")
        
        if selected_employee and selected_employee != "-- Choose employee --" and "(" in selected_employee:
            employee_id = selected_employee.split("(")[1].split(")")[0]
            if st.button("Generate Insights"):
                insights = agents["enhanced_ai_agent"].generate_growth_insights(employee_id)
                st.subheader("Growth Insights")
                display_as_table(insights)
        
        st.markdown("---")
        
        # Performance prediction
        employees = st.session_state.data_manager.load_data("employees") or []
        selected_employee = st.selectbox("Select Employee for Prediction", 
                                        ["-- Choose employee --"] + [f"{e.get('name')} ({e.get('id')})" for e in employees],
                                        key="pred_employee")
        months = st.slider("Months to Predict", 1, 6, 3, key="prediction_months_slider")
        
        if selected_employee and selected_employee != "-- Choose employee --" and "(" in selected_employee:
            employee_id = selected_employee.split("(")[1].split(")")[0]
            if st.button("Predict Performance"):
                prediction = agents["enhanced_ai_agent"].predict_performance_trend(employee_id, months)
                st.subheader("Performance Prediction")
                display_as_table(prediction)

# Risks page
def risks_page():
    """Risk detection page"""
    st.title("⚠️ Risk Detection")
    st.markdown("---")
    
    agents = initialize_agents()
    
    if st.button("Detect All Risks"):
        with st.spinner("Detecting risks..."):
            risks = agents["risk_agent"].detect_all_risks()
            
            st.metric("Total Risks Detected", len(risks))
            
            # Group by severity
            high_risks = [r for r in risks if r.get("severity") == "high"]
            medium_risks = [r for r in risks if r.get("severity") == "medium"]
            low_risks = [r for r in risks if r.get("severity") == "low"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("High", len(high_risks), delta=None)
            with col2:
                st.metric("Medium", len(medium_risks), delta=None)
            with col3:
                st.metric("Low", len(low_risks), delta=None)
            
            st.markdown("---")
            
            # Display risks
            for risk in risks:
                severity_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                st.markdown(f"{severity_color.get(risk.get('severity'), '⚪')} **{risk.get('type')}** - {risk.get('description')}")
                with st.expander("Details"):
                    display_as_table(risk)

# Goals page
def goals_page():
    """Goals management page"""
    st.title("🎯 Goals")
    st.markdown("---")
    
    # Role-based access control
    user_role = st.session_state.user.get("role", "employee")
    user_email = st.session_state.user.get("email")
    
    agents = initialize_agents()
    goal_agent = agents["goal_agent"]
    
    # Check if we should show view after creation
    show_view_after_create = st.session_state.get("show_goals_view", False)
    
    if show_view_after_create:
        st.session_state.show_goals_view = False
        st.success("✅ Goal created successfully! Viewing all goals below.")
        st.markdown("---")
        # Show view content immediately
        goals = goal_agent.get_all_goals()
        if goals:
            for goal in goals:
                progress = goal.get("progress_percentage", 0)
                st.progress(progress / 100)
                st.write(f"**{goal.get('title')}** - {goal.get('status')} ({progress:.1f}%)")
                with st.expander("Details"):
                    display_as_table(goal)
        st.markdown("---")
        st.markdown("### Or use tabs below to navigate")
    
    # Role-based tab visibility - Employees cannot create goals
    if user_role == "employee":
        tabs = st.tabs(["View Goals"])
        tab1 = tabs[0]
        tab2 = None
    else:
        tabs = st.tabs(["View Goals", "Create Goal"])
        tab1 = tabs[0]
        tab2 = tabs[1]
    
    with tab1:
        # Role-based goal filtering
        employee_id = None
        if user_role == "employee":
            # Employees only see their own goals
            employee = next((e for e in st.session_state.data_manager.load_data("employees") or [] if e.get("email") == user_email), None)
            if employee:
                employee_id = employee.get("id")
                goals = goal_agent.get_employee_goals(employee_id)
                st.info("👤 Showing only your goals")
            else:
                goals = []
                st.error("❌ Employee record not found.")
        else:
            # Managers and owners see all goals
            goals = goal_agent.get_all_goals()
        
        # Load employees for name lookup
        employees = st.session_state.data_manager.load_data("employees") or []
        employee_lookup = {e.get("id"): e.get("name", "Unknown") for e in employees}
        
        if goals:
            # Handle edit forms first
            for goal in goals:
                goal_id = goal.get('id')
                if st.session_state.get(f"editing_goal_{goal_id}", False):
                    with st.expander(f"✏️ Editing: {goal.get('title', 'Untitled Goal')}", expanded=True):
                        with st.form(f"edit_goal_form_{goal_id}"):
                            # Role-based editing restrictions
                            if user_role == "employee":
                                # Employees can only update current value (progress) and add notes
                                st.info("💡 You can update the progress (current value) and add progress notes for your goals.")
                                st.write(f"**Goal:** {goal.get('title', 'Untitled Goal')}")
                                st.write(f"**Target:** {goal.get('target_value', 0)}")
                                st.write(f"**Current Progress:** {goal.get('progress_percentage', 0):.1f}%")
                                edit_title = goal.get('title', '')
                                edit_description = goal.get('description', '')
                                edit_target = goal.get('target_value', 100)
                                edit_current = st.number_input("Current Value (Progress)", min_value=0.0, value=float(goal.get('current_value', 0)), help="Update how close you are to completing this goal")
                                progress_notes = st.text_area("Progress Notes (Optional)", placeholder="Add notes about your progress, achievements, or challenges...", help="Document your progress, achievements, or any challenges you're facing", key=f"progress_notes_{goal_id}")
                                edit_deadline = None
                            else:
                                # Managers and owners can edit all fields
                                edit_title = st.text_input("Goal Title", value=goal.get('title', ''))
                                edit_description = st.text_area("Description", value=goal.get('description', ''))
                                edit_target = st.number_input("Target Value", min_value=0.0, value=float(goal.get('target_value', 100)))
                                edit_current = st.number_input("Current Value", min_value=0.0, value=float(goal.get('current_value', 0)))
                                edit_deadline = st.date_input("Deadline",
                                                             value=datetime.fromisoformat(goal.get('deadline')) if goal.get('deadline') else None)
                                progress_notes = None  # Managers don't use progress notes in this form
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Save Changes"):
                                    # Role-based update restrictions
                                    if user_role == "employee":
                                        # Employees can update current value and add notes using goal_agent method
                                        result = goal_agent.update_goal_progress(goal_id, edit_current, progress_notes.strip() if progress_notes and progress_notes.strip() else None)
                                        if result.get("success"):
                                            st.success("✅ Goal progress updated!")
                                            st.session_state[f"editing_goal_{goal_id}"] = False
                                            st.rerun()
                                        else:
                                            st.error(f"Error: {result.get('error', 'Failed to update goal')}")
                                            st.rerun()
                                        return
                                    else:
                                        # Managers/owners can update all fields
                                        goal['title'] = edit_title
                                        goal['description'] = edit_description
                                        goal['target_value'] = edit_target
                                        goal['current_value'] = edit_current
                                        if edit_deadline:
                                            goal['deadline'] = edit_deadline.isoformat()
                                    # Recalculate progress
                                    if edit_target > 0:
                                        goal['progress_percentage'] = min(100, (edit_current / edit_target) * 100)
                                    else:
                                        goal['progress_percentage'] = 0
                                    # Update status
                                    if goal['progress_percentage'] >= 100:
                                        goal['status'] = "completed"
                                    elif goal.get('deadline') and datetime.fromisoformat(goal['deadline']) < datetime.now():
                                        goal['status'] = "overdue"
                                    else:
                                        goal['status'] = "active"
                                    goals = goal_agent.get_all_goals()
                                    for i, g in enumerate(goals):
                                        if g.get('id') == goal_id:
                                            goals[i] = goal
                                            break
                                    goal_agent.data_manager.save_data("goals", goals)
                                    st.session_state[f"editing_goal_{goal_id}"] = False
                                    st.success("Goal updated!")
                                    st.rerun()
                            with col_cancel:
                                if st.form_submit_button("❌ Cancel"):
                                    st.session_state[f"editing_goal_{goal_id}"] = False
                                    st.rerun()
            
            # For managers/owners: Group goals by employee
            if user_role != "employee":
                # Group goals by employee_id
                goals_by_employee = {}
                for goal in goals:
                    emp_id = goal.get("employee_id", "unknown")
                    if emp_id not in goals_by_employee:
                        goals_by_employee[emp_id] = []
                    goals_by_employee[emp_id].append(goal)
                
                # Display goals grouped by employee
                for emp_id, employee_goals in goals_by_employee.items():
                    employee_name = employee_lookup.get(emp_id, f"Employee {emp_id}")
                    with st.expander(f"👤 {employee_name} ({len(employee_goals)} goal(s))", expanded=True):
                        # Table header for this employee
                        header_cols = st.columns([2, 1, 1, 1, 1, 1.5])
                        with header_cols[0]:
                            st.markdown("**Title**")
                        with header_cols[1]:
                            st.markdown("**Status**")
                        with header_cols[2]:
                            st.markdown("**Progress**")
                        with header_cols[3]:
                            st.markdown("**Current/Target**")
                        with header_cols[4]:
                            st.markdown("**Deadline**")
                        with header_cols[5]:
                            st.markdown("**Actions**")
                        
                        st.markdown("---")
                        
                        # Table rows for this employee's goals
                        for goal in employee_goals:
                            goal_id = goal.get('id')
                            title = goal.get('title', 'Untitled Goal')
                            status = goal.get('status', 'N/A')
                            progress = goal.get("progress_percentage", 0)
                            current = goal.get('current_value', 0)
                            target = goal.get('target_value', 0)
                            deadline = goal.get('deadline', 'N/A')[:10] if goal.get('deadline') else 'N/A'
                            
                            row_cols = st.columns([2, 1, 1, 1, 1, 1.5])
                            with row_cols[0]:
                                st.write(f"**{title}**")
                                # Show notes indicator if notes exist
                                if goal.get('notes') and len(goal.get('notes', [])) > 0:
                                    st.caption(f"📝 {len(goal.get('notes', []))} progress note(s)")
                            with row_cols[1]:
                                st.write(status)
                            with row_cols[2]:
                                st.progress(progress / 100)
                                st.write(f"{progress:.1f}%")
                            with row_cols[3]:
                                st.write(f"{current}/{target}")
                            with row_cols[4]:
                                st.write(deadline)
                            with row_cols[5]:
                                # Managers and owners can edit/delete any goal
                                btn_col1, btn_col2 = st.columns(2)
                                with btn_col1:
                                    if st.button("✏️ Edit", key=f"edit_btn_{goal_id}", use_container_width=True):
                                        st.session_state[f"editing_goal_{goal_id}"] = True
                                        st.rerun()
                                with btn_col2:
                                    if st.button("🗑️ Del", key=f"delete_btn_{goal_id}", use_container_width=True, type="secondary"):
                                        if goal_agent.delete_goal(goal_id):
                                            st.success("Goal deleted!")
                                        st.rerun()
                            
                            # Show progress notes if they exist
                            if goal.get('notes') and len(goal.get('notes', [])) > 0:
                                with st.expander(f"> View Progress Notes ({len(goal.get('notes', []))} note(s))"):
                                    for note_entry in goal.get('notes', []):
                                        note_text = note_entry.get('note', '')
                                        note_time = note_entry.get('timestamp', 'N/A')
                                        note_author = note_entry.get('added_by', 'Employee')
                                        st.markdown(f"""
                                        <div style="background-color: rgba(0, 224, 255, 0.1); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #00E0FF;">
                                            <strong>{note_author}</strong> - <small>{note_time[:19] if note_time != 'N/A' else 'N/A'}</small><br>
                                            {note_text}
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            st.markdown("---")
            else:
                # For employees: Show their goals in a simple table (no grouping needed)
                # Table header
                header_cols = st.columns([2, 1, 1, 1, 1, 1.5])
                with header_cols[0]:
                    st.markdown("**Title**")
                with header_cols[1]:
                    st.markdown("**Status**")
                with header_cols[2]:
                    st.markdown("**Progress**")
                with header_cols[3]:
                    st.markdown("**Current/Target**")
                with header_cols[4]:
                    st.markdown("**Deadline**")
                with header_cols[5]:
                    st.markdown("**Actions**")
                
                st.markdown("---")
                
                # Table rows with action buttons
                for goal in goals:
                    goal_id = goal.get('id')
                    title = goal.get('title', 'Untitled Goal')
                    status = goal.get('status', 'N/A')
                    progress = goal.get("progress_percentage", 0)
                    current = goal.get('current_value', 0)
                    target = goal.get('target_value', 0)
                    deadline = goal.get('deadline', 'N/A')[:10] if goal.get('deadline') else 'N/A'
                    
                    row_cols = st.columns([2, 1, 1, 1, 1, 1.5])
                    with row_cols[0]:
                        st.write(f"**{title}**")
                        # Show notes indicator if notes exist
                        if goal.get('notes') and len(goal.get('notes', [])) > 0:
                            st.caption(f"📝 {len(goal.get('notes', []))} progress note(s)")
                    with row_cols[1]:
                        st.write(status)
                    with row_cols[2]:
                        st.progress(progress / 100)
                        st.write(f"{progress:.1f}%")
                    with row_cols[3]:
                        st.write(f"{current}/{target}")
                    with row_cols[4]:
                        st.write(deadline)
                    with row_cols[5]:
                        # Employees can only update progress of their own goals
                        if employee_id and goal.get("employee_id") == employee_id:
                            if st.button("✏️ Update Progress", key=f"edit_btn_{goal_id}", use_container_width=True):
                                st.session_state[f"editing_goal_{goal_id}"] = True
                                st.rerun()
                        else:
                            st.write("View Only")
                    
                    # Show progress notes if they exist
                    if goal.get('notes') and len(goal.get('notes', [])) > 0:
                        with st.expander(f"> View Progress Notes ({len(goal.get('notes', []))} note(s))"):
                            for note_entry in goal.get('notes', []):
                                note_text = note_entry.get('note', '')
                                note_time = note_entry.get('timestamp', 'N/A')
                                note_author = note_entry.get('added_by', 'Employee')
                                st.markdown(f"""
                                <div style="background-color: rgba(0, 224, 255, 0.1); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #00E0FF;">
                                    <strong>{note_author}</strong> - <small>{note_time[:19] if note_time != 'N/A' else 'N/A'}</small><br>
                                    {note_text}
                                </div>
                                """, unsafe_allow_html=True)
        else:
            st.info("No goals found")
    
    # Only show Create Goal tab for managers and owners
    if tab2 is not None:
        with tab2:
            employees = st.session_state.data_manager.load_data("employees") or []
            with st.form("create_goal"):
                # Managers and owners can select any employee - show names instead of IDs
                employee_options = {f"{e.get('name')} ({e.get('id')})": e.get("id") for e in employees}
                selected_employee_name = st.selectbox("Employee", ["-- Choose employee --"] + list(employee_options.keys()), key="create_goal_employee")
                employee_id = employee_options.get(selected_employee_name) if selected_employee_name and selected_employee_name != "-- Choose employee --" else ""
                
                title = st.text_input("Goal Title *")
                description = st.text_area("Description")
                target_value = st.number_input("Target Value", min_value=0.0, value=100.0)
                deadline = st.date_input("Deadline")
                
                if st.form_submit_button("Create Goal"):
                    if title and employee_id:
                        result = goal_agent.create_goal({
                            "employee_id": employee_id,
                            "title": title,
                            "description": description,
                            "target_value": target_value,
                            "deadline": deadline.isoformat() if deadline else None
                        })
                        if result.get("success"):
                            st.session_state.show_goals_view = True
                    st.rerun()
        
# Feedback page
def feedback_page():
    """Feedback management page"""
    st.title("💬 Feedback & Communication")
    st.markdown("---")
    
    agents = initialize_agents()
    feedback_agent = agents["feedback_agent"]
    user_role = st.session_state.user.get("role", "employee")
    user_email = st.session_state.user.get("email")
    
    # Check if we should show view after creation
    show_view_after_create = st.session_state.get("show_feedback_view", False)
    
    if show_view_after_create:
        st.session_state.show_feedback_view = False
        st.success("✅ Feedback created successfully! Employee will be notified.")
        st.markdown("---")
    
    # Different tabs based on role
    if user_role == "owner" or user_role == "manager":
        # Manager/Owner view
        tab1, tab2, tab3 = st.tabs(["All Feedback", "Create Feedback", "Communications"])
        
        with tab1:
            feedbacks = feedback_agent.get_all_feedbacks()
            if feedbacks:
                # Handle edit forms first
                for feedback in feedbacks:
                    feedback_id = feedback.get('id')
                    if st.session_state.get(f"editing_feedback_{feedback_id}", False):
                        with st.expander(f"✏️ Editing: {feedback.get('title', 'Untitled Feedback')}", expanded=True):
                            with st.form(f"edit_feedback_form_{feedback_id}"):
                                edit_title = st.text_input("Title", value=feedback.get('title', ''))
                                edit_content = st.text_area("Content", value=feedback.get('content', ''))
                                edit_category = st.selectbox("Category", ["performance", "behavior", "skills", "general"],
                                                            index=["performance", "behavior", "skills", "general"].index(feedback.get('category', 'general')),
                                                            key=f"edit_feedback_category_{feedback_id}")
                                edit_status = st.selectbox("Status", ["pending_response", "responded", "closed"],
                                                          index=["pending_response", "responded", "closed"].index(feedback.get('status', 'pending_response')),
                                                          key=f"edit_feedback_status_{feedback_id}")
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Save Changes"):
                                        feedback['title'] = edit_title
                                        feedback['content'] = edit_content
                                        feedback['category'] = edit_category
                                        feedback['status'] = edit_status
                                        feedback['updated_at'] = datetime.now().isoformat()
                                        feedbacks = feedback_agent.get_all_feedbacks()
                                        for i, f in enumerate(feedbacks):
                                            if f.get('id') == feedback_id:
                                                feedbacks[i] = feedback
                                                break
                                        feedback_agent.data_manager.save_data("feedback", feedbacks)
                                        st.session_state[f"editing_feedback_{feedback_id}"] = False
                                        st.success("Feedback updated!")
                                        st.rerun()
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel"):
                                        st.session_state[f"editing_feedback_{feedback_id}"] = False
                                        st.rerun()
                
                # Table header
                header_cols = st.columns([2, 1, 1, 1, 2, 1.5])
                with header_cols[0]:
                    st.markdown("**Title**")
                with header_cols[1]:
                    st.markdown("**Employee**")
                with header_cols[2]:
                    st.markdown("**Category**")
                with header_cols[3]:
                    st.markdown("**Status**")
                with header_cols[4]:
                    st.markdown("**Content**")
                with header_cols[5]:
                    st.markdown("**Actions**")
                
                st.markdown("---")
                
                # Load employees for name lookup
                employees = st.session_state.data_manager.load_data("employees") or []
                employee_lookup = {e.get("id"): e.get("name", "Unknown") for e in employees}
                
                # Table rows with action buttons
                for idx, feedback in enumerate(feedbacks):
                    feedback_id = feedback.get('id')
                    title = feedback.get('title', 'Untitled Feedback')
                    employee_id = feedback.get('employee_id', 'N/A')
                    employee_name = employee_lookup.get(employee_id, employee_id)  # Show name instead of ID
                    category = feedback.get('category', 'N/A')
                    status = feedback.get('status', 'N/A')
                    content = (feedback.get('content', '')[:50] + '...') if len(feedback.get('content', '')) > 50 else (feedback.get('content', '') or 'N/A')
                    
                    row_cols = st.columns([2, 1, 1, 1, 2, 1.5])
                    with row_cols[0]:
                        st.write(f"**{title}**")
                    with row_cols[1]:
                        st.write(employee_name)
                    with row_cols[2]:
                        st.write(category)
                    with row_cols[3]:
                        st.write(status)
                    with row_cols[4]:
                        st.write(content)
                    with row_cols[5]:
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("✏️ Edit", key=f"tab1_edit_btn_{idx}_{feedback_id}", use_container_width=True):
                                st.session_state[f"editing_feedback_{feedback_id}"] = True
                                st.rerun()
                        with btn_col2:
                            if st.button("🗑️ Del", key=f"tab1_delete_btn_{idx}_{feedback_id}", use_container_width=True, type="secondary"):
                                feedbacks = feedback_agent.get_all_feedbacks()
                                feedbacks = [f for f in feedbacks if f.get('id') != feedback_id]
                                feedback_agent.data_manager.save_data("feedback", feedbacks)
                                st.success("Feedback deleted!")
                                st.rerun()
            else:
                st.info("No feedback found")
        
        with tab2:
            employees = st.session_state.data_manager.load_data("employees") or []
            with st.form("create_feedback"):
                employee_id = st.selectbox("Employee", ["-- Choose employee --"] + [e.get("id") for e in employees], key="create_feedback_employee")
                employee_id = employee_id if employee_id and employee_id != "-- Choose employee --" else ""
                title = st.text_input("Title *")
                content = st.text_area("Content *")
                category = st.selectbox("Category", ["performance", "behavior", "skills", "general"], key="create_feedback_category")
                
                if st.form_submit_button("Create Feedback"):
                    if employee_id and title and content and st.session_state.user:
                        result = feedback_agent.create_feedback({
                            "employee_id": employee_id,
                            "given_by": st.session_state.user.get("email"),
                            "title": title,
                            "content": content,
                            "category": category
                        })
                        if result.get("success"):
                            st.session_state.show_feedback_view = True
                            st.success("✅ Feedback created! Employee has been notified.")
                            st.rerun()
                
        with tab3:
            st.subheader("All Communications")
            feedbacks = feedback_agent.get_all_feedbacks()
            feedbacks_with_comm = [f for f in feedbacks if f.get('communications')]
            if feedbacks_with_comm:
                for feedback in feedbacks_with_comm:
                    st.markdown(f"### {feedback.get('title')}")
                    for comm in feedback.get('communications', []):
                        sender_role = comm.get('sender_role', 'employee')
                        bg_color = "#2a4a6a" if sender_role == "manager" else "#4a6a2a"
                        st.markdown(f"""
                        <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0;">
                            <strong>{sender_role.title()}</strong> ({comm.get('sender_id')})<br>
                            {comm.get('message')}<br>
                            <small>{comm.get('timestamp', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.info("No communications yet")
    else:
        # Employee view
        tab1, tab2 = st.tabs(["My Feedback", "Ask Questions"])
        
        with tab1:
            my_feedbacks = feedback_agent.get_feedbacks_for_employee(user_email)
            if my_feedbacks:
                for feedback in my_feedbacks:
                    with st.container():
                        st.markdown(f"### {feedback.get('title', 'Untitled Feedback')}")
                        st.write(f"**From:** {feedback.get('given_by')} | **Category:** {feedback.get('category')} | **Status:** {feedback.get('status')}")
                        st.write(f"**Content:** {feedback.get('content', 'N/A')}")
                        
                        # Communication thread
                        communications = feedback.get('communications', [])
                        if communications:
                            st.markdown("#### 💬 Conversation:")
                            for comm in communications:
                                sender_role = comm.get('sender_role', 'employee')
                                bg_color = "#2a4a6a" if sender_role == "manager" else "#4a6a2a"
                                st.markdown(f"""
                                <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0;">
                                    <strong>{sender_role.title()}</strong> ({comm.get('sender_id')})<br>
                                    {comm.get('message')}<br>
                                    <small>{comm.get('timestamp', '')}</small>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Employee can ask question
                        with st.expander("Ask a Question to Manager"):
                            with st.form(f"ask_question_{feedback.get('id')}"):
                                question = st.text_area("Your Question", key=f"question_{feedback.get('id')}")
                                if st.form_submit_button("Send Question"):
                                    if question:
                                        result = feedback_agent.add_communication(
                                            feedback.get('id'),
                                            user_email,
                                            question,
                                            "employee"
                                        )
                                        if result.get("success"):
                                            st.success("✅ Question sent! Manager will be notified.")
                                st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No feedback received yet")
        
        with tab2:
            st.subheader("Ask Questions About Your Feedback")
            my_feedbacks = feedback_agent.get_feedbacks_for_employee(user_email)
            if my_feedbacks:
                selected_feedback = st.selectbox(
                    "Select Feedback",
                    ["-- Choose feedback --"] + [f"{f.get('title')} (ID: {f.get('id')})" for f in my_feedbacks]
                )
                
                if selected_feedback and selected_feedback != "-- Choose feedback --":
                    feedback_id = selected_feedback.split("ID: ")[1].split(")")[0]
                    feedback = feedback_agent.get_feedback(feedback_id)
                    
                    if feedback:
                        st.write(f"**Feedback:** {feedback.get('title')}")
                        st.write(f"**Content:** {feedback.get('content')}")
                        st.markdown("---")
                        
                        with st.form("ask_question_form"):
                            question = st.text_area("Ask your question to the manager *")
                            if st.form_submit_button("Send Question"):
                                if question:
                                    result = feedback_agent.add_communication(
                                        feedback_id,
                                        user_email,
                                        question,
                                        "employee"
                                    )
                                    if result.get("success"):
                                        st.success("✅ Question sent! Manager will be notified and can respond.")
                                        st.rerun()
                                    else:
                                        st.error(result.get("error"))
            else:
                st.info("You don't have any feedback yet to ask questions about.")

# Notifications & Alerts page (merged)
def notifications_page():
    """Unified Notifications & Alerts page"""
    st.title("🔔 Notifications")
    st.markdown("---")
    
    agents = initialize_agents()
    notification_agent = agents["notification_agent"]
    
    user_role = st.session_state.user.get("role", "employee")
    user_email = st.session_state.user.get("email")
    
    # Notifications display
    if st.session_state.user:
            # Get employee_id from email
            employees = st.session_state.data_manager.load_data("employees") or []
            employee = next((e for e in employees if e.get("email") == user_email), None)
            
            if employee:
                employee_id = employee.get("id")
                # Get notifications by employee_id (notifications use employee_id as recipient)
                all_notifications = notification_agent.get_notifications(recipient=employee_id, unread_only=False)
                unread_notifications = [n for n in all_notifications if not n.get("read", False)]
                
                st.metric("Unread Notifications", len(unread_notifications))
                
                # Show unread first, then read
                if unread_notifications:
                    st.subheader("📬 Unread Notifications")
                    for notification in unread_notifications:
                        with st.expander(f"> 🔴 {notification.get('title')} - {notification.get('notification_type', notification.get('type', 'info'))}"):
                            st.write(notification.get("message"))
                            st.caption(f"Created: {notification.get('created_at', 'N/A')}")
                            if st.button(f"Mark as Read", key=f"read_{notification.get('id')}"):
                                notification_agent.mark_as_read(notification.get("id"))
                                st.rerun()
                
                # Show read notifications
                read_notifications = [n for n in all_notifications if n.get("read", False)]
                if read_notifications:
                    st.markdown("---")
                    st.subheader("✓ Read Notifications")
                    for notification in read_notifications[:10]:  # Show last 10 read notifications
                        with st.expander(f"> ✓ {notification.get('title')} - {notification.get('notification_type', notification.get('type', 'info'))}"):
                            st.write(notification.get("message"))
                            st.caption(f"Read: {notification.get('read_at', 'N/A')}")
                
                if not all_notifications:
                    st.info("📭 No notifications found.")
            else:
                st.error("❌ Employee record not found.")
                
# Export page
def export_page():
    """Export page with enhanced features"""
    st.title("📤 Export & Reports")
    st.markdown("---")
    
    agents = initialize_agents()
    export_agent = agents["export_agent"]
    user_email = st.session_state.user.get("email")
    
    tab1, tab2, tab3 = st.tabs(["Export Data", "Performance Reports", "Scheduled Exports"])
    
    with tab1:
        st.subheader("Export Data to CSV or PDF")
        
        col1, col2 = st.columns(2)
        with col1:
            export_type = st.selectbox("Export Format", ["CSV", "PDF"], key="export_data_format")
        with col2:
            data_type = st.selectbox("Data Type", ["Projects", "Tasks", "Employees", "Performance"], key="export_data_type")
        
        # CSV-specific options
        if export_type == "CSV":
            include_metadata = st.checkbox("Include metadata header", value=True)
        
        # PDF-specific options
        if export_type == "PDF":
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name", value="Company")
            with col2:
                include_branding = st.checkbox("Include company branding", value=True)
        
        if st.button("📥 Export Now", use_container_width=True):
            data_manager = st.session_state.data_manager
            if data_type == "Projects":
                data = data_manager.load_data("projects") or []
            elif data_type == "Tasks":
                data = data_manager.load_data("tasks") or []
            elif data_type == "Employees":
                data = data_manager.load_data("employees") or []
            else:
                data = data_manager.load_data("performances") or []
            
            if data:
                if export_type == "CSV":
                    result = export_agent.export_to_csv(data, include_metadata=include_metadata)
                    if result.get("success"):
                        st.success("✅ CSV export generated successfully!")
                        st.download_button("📥 Download CSV", result["content"], 
                                         file_name=result["filename"], mime="text/csv")
                    else:
                        st.error(result.get("error", "Failed to export"))
                else:
                    result = export_agent.export_to_pdf(
                        data, 
                        title=f"{data_type} Report",
                        company_name=company_name,
                        include_branding=include_branding
                    )
                    if result.get("success"):
                        st.success("✅ PDF report generated successfully!")
                        st.download_button("📥 Download PDF", result["content"],
                                         file_name=result["filename"], mime="application/pdf")
                    else:
                        st.error(result.get("error", "Failed to export"))
            else:
                st.warning("⚠️ No data available to export")
    
    with tab2:
        st.subheader("Performance Reports")
        
        employees = st.session_state.data_manager.load_data("employees") or []
        selected_employee = st.selectbox("Select Employee", 
                                         ["-- Choose employee --"] + [f"{e.get('name')} ({e.get('id')})" for e in employees],
                                         key="export_performance_employee")
        
        if selected_employee and selected_employee != "-- Choose employee --" and "(" in selected_employee:
            employee_id = selected_employee.split("(")[1].split(")")[0]
            
            col1, col2 = st.columns(2)
            with col1:
                report_format = st.selectbox("Report Format", ["JSON", "PDF"], key="performance_report_format")
            with col2:
                if report_format == "PDF":
                    company_name = st.text_input("Company Name", value="Company", key="perf_company")
            
            # Show preview of report data
            if st.button("📊 Generate Performance Report", use_container_width=True):
                if report_format == "JSON":
                    result = export_agent.export_performance_report(employee_id, format="json")
                else:
                    result = export_agent.export_performance_report(employee_id, format="pdf")
                
                if result.get("success"):
                    st.success("✅ Performance report generated successfully!")
                    
                    if report_format == "JSON":
                        # Display JSON preview as table
                        st.subheader("Report Preview")
                        display_as_table(result.get("report_data", {}))
                        
                        # Download button
                        st.download_button(
                            "📥 Download JSON Report",
                            result["content"],
                            file_name=result["filename"],
                            mime="application/json"
                        )
                    else:
                        st.download_button(
                            "📥 Download PDF Report",
                            result["content"],
                            file_name=result["filename"],
                            mime="application/pdf"
                        )
                else:
                    st.error(result.get("error", "Failed to generate report"))
    
    with tab3:
        st.subheader("Scheduled Exports")
        st.markdown("Schedule automated exports for compliance and HR systems")
        
        # Show existing schedules
        schedules = export_agent.get_export_schedules(user_email)
        
        if schedules:
            st.markdown("#### Existing Schedules")
            for schedule in schedules:
                with st.expander(f"📅 {schedule.get('name')} - {schedule.get('frequency', 'N/A').title()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Type:** {schedule.get('export_type')} | **Data:** {schedule.get('data_type')}")
                        st.write(f"**Frequency:** {schedule.get('frequency', 'N/A').title()}")
                        st.write(f"**Next Run:** {schedule.get('next_run', 'N/A')}")
                        if schedule.get('last_run'):
                            st.write(f"**Last Run:** {schedule.get('last_run')}")
                    with col2:
                        status = "✅ Enabled" if schedule.get('enabled') else "❌ Disabled"
                        st.write(f"**Status:** {status}")
                        if schedule.get('hr_system_integration'):
                            st.write("🔗 HR System Integration: Enabled")
                        if schedule.get('failure_count', 0) > 0:
                            st.warning(f"⚠️ {schedule.get('failure_count')} failure(s)")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_sched_{schedule.get('id')}"):
                            st.session_state[f"editing_schedule_{schedule.get('id')}"] = True
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Del", key=f"del_sched_{schedule.get('id')}", type="secondary"):
                            if export_agent.delete_export_schedule(schedule.get('id')):
                                st.success("Schedule deleted!")
                    st.rerun()
                    with col3:
                        new_status = not schedule.get('enabled')
                        if st.button("🔄 Toggle", key=f"toggle_{schedule.get('id')}"):
                            export_agent.update_export_schedule(schedule.get('id'), {"enabled": new_status})
                    st.rerun()
    
        st.markdown("---")
        st.markdown("#### Create New Schedule")
        
        with st.form("create_schedule_form"):
            schedule_name = st.text_input("Schedule Name *")
            
            col1, col2 = st.columns(2)
            with col1:
                export_type = st.selectbox("Export Format", ["CSV", "PDF", "JSON"], key="schedule_export_format")
                data_type = st.selectbox("Data Type", ["Projects", "Tasks", "Employees", "Performance"], key="schedule_data_type")
            with col2:
                frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"], key="schedule_frequency")
                time_input = st.time_input("Time", value=datetime.strptime("09:00", "%H:%M").time())
            
            # Frequency-specific options
            if frequency == "weekly":
                day_of_week = st.selectbox("Day of Week", 
                                          ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                          index=0,
                                          key="schedule_day_of_week")
                day_of_week_num = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day_of_week)
            elif frequency == "monthly":
                day_of_month = st.number_input("Day of Month", min_value=1, max_value=31, value=1)
            else:
                day_of_week_num = None
                day_of_month = None
            
            hr_integration = st.checkbox("HR System Integration (for compliance)")
            if hr_integration:
                hr_endpoint = st.text_input("HR System Endpoint URL", placeholder="https://hr-system.com/api/import")
            else:
                hr_endpoint = None
            
            recipient_email = st.text_input("Recipient Email", placeholder="recipient@company.com")
            
            if st.form_submit_button("💾 Create Schedule"):
                if schedule_name:
                    schedule_data = {
                        "name": schedule_name,
                        "export_type": export_type,
                        "data_type": data_type,
                        "frequency": frequency,
                        "time": time_input.strftime("%H:%M"),
                        "day_of_week": day_of_week_num if frequency == "weekly" else None,
                        "day_of_month": day_of_month if frequency == "monthly" else None,
                        "recipient_email": recipient_email if recipient_email else None,
                        "hr_system_integration": hr_integration,
                        "hr_system_endpoint": hr_endpoint if hr_integration else None,
                        "created_by": user_email
                    }
                    
                    result = export_agent.create_export_schedule(schedule_data)
                    if result.get("success"):
                        st.success(f"✅ Schedule '{schedule_name}' created successfully!")
                        st.info(f"Next run: {result.get('schedule', {}).get('next_run', 'N/A')}")
                        st.rerun()
                    else:
                        st.error("Failed to create schedule")
                else:
                    st.error("Schedule name is required")

# Comparison page
def comparison_page():
    """Team comparison page"""
    st.title("⚖️ Team Comparison")
    st.markdown("---")
    
    agents = initialize_agents()
    comparison_agent = agents["comparison_agent"]
    
    employees = st.session_state.data_manager.load_data("employees") or []
    # Create options with names for display, but store IDs
    employee_options = {f"{e.get('name')} ({e.get('id')})": e.get("id") for e in employees}
    
    selected_employee_names = st.multiselect("Select Employees to Compare",
                                            list(employee_options.keys()),
                                            key="comparison_employees_select")
    
    # Convert selected names back to IDs
    selected_employees = [employee_options[name] for name in selected_employee_names]
    
    if selected_employees and st.button("Compare"):
        comparison = comparison_agent.compare_team_performance(selected_employees)
        
        st.subheader("Comparison Results")
        # Remove department column from comparison data
        comparison_data = comparison["comparison"]
        for item in comparison_data:
            if "department" in item:
                del item["department"]
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
        
        # Chart
        chart = comparison_agent.generate_comparison_chart(comparison, "bar")
        if chart and chart.get("figure"):
            st.plotly_chart(chart["figure"], use_container_width=True)


# Employee Development page (Skills, Workload, Attendance, Engagement, 360 Reviews, Promotion, Badges)
def employee_development_page():
    """Comprehensive employee development page with all new features"""
    st.title("🚀 Employee Development")
    st.markdown("---")
    
    user_role = st.session_state.user.get("role", "employee")
    user_email = st.session_state.user.get("email")
    
    agents = initialize_agents()
    skill_agent = agents["skill_agent"]
    workload_agent = agents["workload_agent"]
    attendance_agent = agents["attendance_agent"]
    engagement_agent = agents["engagement_agent"]
    review_360_agent = agents["review_360_agent"]
    promotion_agent = agents["promotion_agent"]
    badge_agent = agents["badge_agent"]
    
    employees = st.session_state.data_manager.load_data("employees") or []
    
    # Get employee ID
    if user_role == "employee":
        employee = next((e for e in employees if e.get("email") == user_email), None)
        if not employee:
            st.error("❌ Employee record not found.")
            return
        selected_employee_id = employee.get("id")
        selected_employee_name = employee.get("name")
    else:
        # Managers/Owners can select employee
        employee_options = {f"{e.get('name')} ({e.get('id')})": e.get("id") for e in employees}
        if not employee_options:
            st.warning("No employees found.")
            return
        
        selected_employee_name = st.selectbox("Select Employee", ["-- Choose employee --"] + list(employee_options.keys()), key="dev_select_employee")
        selected_employee_id = employee_options.get(selected_employee_name) if selected_employee_name and selected_employee_name != "-- Choose employee --" else None
        
        if not selected_employee_id:
            st.info("👆 Please select an employee to view their development metrics.")
            return
    
    # Create tabs for different features
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🎯 Skills", "📊 Workload", "📅 Attendance", "💡 Engagement", 
        "🔄 360° Review", "⭐ Promotion", "🏆 Badges"
    ])
    
    # Tab 1: Skills
    with tab1:
        st.subheader("🎯 Skill Tracking")
        
        skills = skill_agent.get_employee_skills(selected_employee_id)
        strong_skills = skill_agent.get_strong_skills(selected_employee_id)
        weak_skills = skill_agent.get_weak_skills(selected_employee_id)
        needs_improvement = skill_agent.get_skills_needing_improvement(selected_employee_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Skills", len(skills))
        with col2:
            st.metric("Strong Skills", len(strong_skills))
        with col3:
            st.metric("Skills to Improve", len(needs_improvement))
        
        st.markdown("---")
        
        # Add/Edit Skills (Managers/Owners or self)
        if user_role in ["owner", "manager"] or user_role == "employee":
            with st.expander("➕ Add/Update Skill", expanded=False):
                with st.form("add_skill_form"):
                    skill_name = st.text_input("Skill Name", key="skill_name_input")
                    skill_level = st.slider("Skill Level (1-5)", 1, 5, 3, key="skill_level_slider")
                    
                    if st.form_submit_button("💾 Save Skill"):
                        if skill_name:
                            result = skill_agent.add_skill(selected_employee_id, skill_name, skill_level)
                            if result.get("success"):
                                st.success(f"✅ Skill '{skill_name}' added/updated!")
                                st.rerun()
                            else:
                                st.error(result.get("error"))
        
        # Display Skills
        if skills:
            st.subheader("Current Skills")
            
            # Display skills as visual cards with progress bars
            if skills:
                for skill, level in skills.items():
                    # Determine status and color
                    if level >= 4:
                        status = "Strong"
                        status_color = "#3DDF85"
                        status_emoji = "🟢"
                    elif level == 3:
                        status = "Medium"
                        status_color = "#FACC15"
                        status_emoji = "🟡"
                    else:
                        status = "Needs Improvement"
                        status_color = "#FF5277"
                        status_emoji = "🔴"
                    
                    # Calculate progress percentage (level out of 5)
                    progress_percent = (level / 5) * 100
                    
                    # Create skill card
                    st.markdown(f"""
                        <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                    border-radius: 16px; padding: 20px; margin-bottom: 15px; 
                                    box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <div style="font-size: 1.1rem; font-weight: 600; color: #FFFFFF;">{skill}</div>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <div style="font-size: 0.9rem; color: {status_color}; font-weight: 500;">
                                        {status_emoji} {status}
                                    </div>
                                    <div style="font-size: 1.2rem; font-weight: 700; color: #00E0FF;">{level}/5</div>
                                </div>
                            </div>
                            <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; height: 12px; overflow: hidden; margin-top: 8px;">
                                <div style="background: linear-gradient(90deg, {status_color}, {status_color}dd); 
                                            height: 100%; width: {progress_percent}%; 
                                            transition: width 0.5s ease; border-radius: 10px;"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No skills recorded yet.")
            
            # Strong Skills Section
            if strong_skills:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### ✅ Strong Skills")
                strong_cols = st.columns(min(len(strong_skills), 3))
                for idx, skill in enumerate(strong_skills):
                    level = skills[skill]
                    with strong_cols[idx % 3]:
                        st.markdown(f"""
                            <div style="background-color: rgba(61, 223, 133, 0.1); border: 1px solid #3DDF85; 
                                        border-radius: 12px; padding: 15px; text-align: center;">
                                <div style="font-size: 1.5rem; margin-bottom: 5px;">⭐</div>
                                <div style="font-weight: 600; color: #3DDF85; margin-bottom: 5px;">{skill}</div>
                                <div style="color: #94A3B8; font-size: 0.9rem;">Level {level}/5</div>
                            </div>
                        """, unsafe_allow_html=True)
            
            # Skills Needing Improvement Section
            if needs_improvement:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📈 Skills Needing Improvement")
                improvement_cols = st.columns(min(len(needs_improvement), 3))
                for idx, skill in enumerate(needs_improvement):
                    level = skills[skill]
                    with improvement_cols[idx % 3]:
                        st.markdown(f"""
                            <div style="background-color: rgba(255, 82, 119, 0.1); border: 1px solid #FF5277; 
                                        border-radius: 12px; padding: 15px; text-align: center;">
                                <div style="font-size: 1.5rem; margin-bottom: 5px;">📈</div>
                                <div style="font-weight: 600; color: #FF5277; margin-bottom: 5px;">{skill}</div>
                                <div style="color: #94A3B8; font-size: 0.9rem;">Level {level}/5</div>
                                <div style="color: #FACC15; font-size: 0.85rem; margin-top: 5px;">Consider training</div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No skills recorded yet. Add skills to track employee capabilities.")
    
    # Tab 2: Workload
    with tab2:
        st.subheader("📊 Workload Assessment")
        
        workload = workload_agent.assess_workload(selected_employee_id)
        status_emoji = workload_agent.get_workload_status_emoji(workload.get("status"))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Status", f"{status_emoji} {workload.get('status', 'N/A').title()}")
        with col2:
            st.metric("Active Tasks", workload.get("task_count", 0))
        with col3:
            st.metric("Overdue Tasks", workload.get("overdue_tasks", 0))
        with col4:
            st.metric("Due Soon", workload.get("tasks_due_soon", 0))
        
        st.markdown("---")
        
        # Recommendations
        recommendations = workload.get("recommendations", [])
        if recommendations:
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")
        else:
            st.info("✅ Workload is well-balanced!")
    
    # Tab 3: Attendance
    with tab3:
        st.subheader("📅 Attendance Tracking")
        
        attendance_percentage = attendance_agent.calculate_attendance_percentage(selected_employee_id, days=30)
        today_attendance = attendance_agent.get_today_attendance(selected_employee_id)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("30-Day Attendance", f"{attendance_percentage:.1f}%")
        with col2:
            if today_attendance:
                status_emoji = "✅" if today_attendance.get("status") == "present" else "❌"
                st.metric("Today", f"{status_emoji} {today_attendance.get('status', 'N/A').title()}")
            else:
                st.metric("Today", "Not Marked")
        
        st.markdown("---")
        
        # Mark Attendance (Employees can mark their own, Managers can mark for others)
        if user_role == "employee" or user_role in ["owner", "manager"]:
            with st.expander("📝 Mark Attendance", expanded=False):
                with st.form("attendance_form"):
                    status = st.radio("Status", ["present", "absent"], key="attendance_status")
                    notes = st.text_area("Notes (Optional)", key="attendance_notes")
                    
                    if st.form_submit_button("💾 Mark Attendance"):
                        result = attendance_agent.mark_attendance(selected_employee_id, status, notes=notes)
                        if result.get("success"):
                            st.success(f"✅ Attendance marked as {status}!")
                            st.rerun()
        
        # How Check-In/Check-Out Works
        with st.expander("ℹ️ How Check-In/Check-Out is Calculated", expanded=False):
            st.markdown("""
            **Check-In Time:**
            - When you mark attendance as "Present", the system automatically records the current time as check-in
            - You can also manually specify a check-in time when marking attendance
            - Format: Stored as ISO timestamp (YYYY-MM-DDTHH:MM:SS)
            
            **Check-Out Time:**
            - Check-out time is optional and can be set when marking attendance
            - If not provided, it remains "N/A"
            - Format: Stored as ISO timestamp (YYYY-MM-DDTHH:MM:SS)
            
            **Work Hours Calculation:**
            - Work hours = Check-Out Time - Check-In Time
            - Displayed in hours (e.g., "8.5 hrs")
            - Only calculated when both check-in and check-out times are available
            """)
        
        # Attendance History
        attendance_history = attendance_agent.get_employee_attendance(selected_employee_id)
        if attendance_history:
            st.subheader("Recent Attendance History")
            
            # Calculate summary statistics
            total_work_hours = 0
            present_days = 0
            absent_days = 0
            
            for attendance in attendance_history[:30]:
                if attendance.get("status") == "present":
                    present_days += 1
                    check_in = attendance.get("check_in_time")
                    check_out = attendance.get("check_out_time")
                    if check_in and check_out:
                        try:
                            check_in_dt = datetime.fromisoformat(check_in)
                            check_out_dt = datetime.fromisoformat(check_out)
                            time_diff = check_out_dt - check_in_dt
                            total_work_hours += time_diff.total_seconds() / 3600
                        except:
                            pass
                else:
                    absent_days += 1
            
            # Display summary card
            if present_days > 0:
                avg_hours = total_work_hours / present_days if present_days > 0 else 0
                st.markdown(f"""
                    <div style="background-color: #111729; border: 1px solid rgba(0, 224, 255, 0.3); 
                                border-radius: 16px; padding: 20px; margin-bottom: 20px; 
                                box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.1);">
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; text-align: center;">
                            <div>
                                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 5px;">Total Work Hours</div>
                                <div style="font-size: 1.8rem; font-weight: 700; color: #00E0FF;">{total_work_hours:.1f} hrs</div>
                            </div>
                            <div>
                                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 5px;">Average Daily</div>
                                <div style="font-size: 1.8rem; font-weight: 700; color: #3DDF85;">{avg_hours:.1f} hrs</div>
                            </div>
                            <div>
                                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 5px;">Present Days</div>
                                <div style="font-size: 1.8rem; font-weight: 700; color: #FFFFFF;">{present_days}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Display attendance as visual cards
            for attendance in attendance_history[:30]:  # Last 30 records
                date_str = attendance.get("date", "N/A")
                status = attendance.get("status", "N/A").title()
                check_in = attendance.get("check_in_time")
                check_out = attendance.get("check_out_time")
                
                # Format times
                check_in_time_str = "N/A"
                check_out_time_str = "N/A"
                work_hours = "N/A"
                
                if check_in:
                    try:
                        check_in_dt = datetime.fromisoformat(check_in)
                        check_in_time_str = check_in_dt.strftime("%I:%M %p")
                    except:
                        check_in_time_str = check_in[:19] if len(check_in) > 19 else check_in
                
                if check_out:
                    try:
                        check_out_dt = datetime.fromisoformat(check_out)
                        check_out_time_str = check_out_dt.strftime("%I:%M %p")
                        
                        # Calculate work hours
                        if check_in:
                            try:
                                check_in_dt = datetime.fromisoformat(check_in)
                                time_diff = check_out_dt - check_in_dt
                                hours = time_diff.total_seconds() / 3600
                                work_hours = f"{hours:.1f} hrs"
                            except:
                                pass
                    except:
                        check_out_time_str = check_out[:19] if len(check_out) > 19 else check_out
                
                # Status color and emoji
                if status.lower() == "present":
                    status_color = "#3DDF85"
                    status_emoji = "✅"
                    status_bg = "rgba(61, 223, 133, 0.1)"
                else:
                    status_color = "#FF5277"
                    status_emoji = "❌"
                    status_bg = "rgba(255, 82, 119, 0.1)"
                
                # Create attendance card
                st.markdown(f"""
                    <div style="background-color: #111729; border: 1px solid rgba(255, 255, 255, 0.08); 
                                border-radius: 16px; padding: 20px; margin-bottom: 15px; 
                                box-shadow: 0px 4px 20px rgba(0, 255, 255, 0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div>
                                <div style="font-size: 1.1rem; font-weight: 600; color: #FFFFFF; margin-bottom: 5px;">
                                    {date_str}
                                </div>
                                <div style="display: inline-block; background-color: {status_bg}; 
                                            border: 1px solid {status_color}; border-radius: 8px; 
                                            padding: 4px 12px; font-size: 0.9rem; color: {status_color};">
                                    {status_emoji} {status}
                                </div>
                            </div>
                            {f'<div style="font-size: 1rem; color: #00E0FF; font-weight: 600;">{work_hours}</div>' if work_hours != "N/A" else ''}
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px;">
                            <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 12px;">
                                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 5px;">Check-In</div>
                                <div style="font-size: 1rem; color: #FFFFFF; font-weight: 500;">🕐 {check_in_time_str}</div>
                            </div>
                            <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 12px;">
                                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 5px;">Check-Out</div>
                                <div style="font-size: 1rem; color: #FFFFFF; font-weight: 500;">🕐 {check_out_time_str}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No attendance records found.")
    
    # Tab 4: Engagement
    with tab4:
        st.subheader("💡 Employee Engagement Score")
        
        engagement = engagement_agent.calculate_engagement_score(selected_employee_id)
        engagement_level = engagement_agent.get_engagement_level(engagement.get("engagement_score", 0))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Engagement Score", f"{engagement.get('engagement_score', 0):.1f}/100", delta=None)
            st.write(f"**Level:** {engagement_level}")
        with col2:
            st.write("**Breakdown:**")
            st.write(f"• Goals: {engagement.get('goal_score', 0):.1f} points")
            st.write(f"• Feedback: {engagement.get('feedback_score', 0):.1f} points")
            st.write(f"• Tasks: {engagement.get('task_score', 0):.1f} points")
            st.write(f"• Participation: {engagement.get('participation_score', 0):.1f} points")
        
        st.markdown("---")
        st.info("💡 Engagement score is calculated based on goal completion, feedback participation, task performance, and overall activity.")
    
    # Tab 5: 360° Review
    with tab5:
        st.subheader("🔄 360° Performance Review")
        
        # Get average ratings
        avg_ratings = review_360_agent.calculate_average_rating(selected_employee_id)
        reviews = review_360_agent.get_employee_reviews(selected_employee_id)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Average", f"{avg_ratings.get('overall_average', 0):.1f}/100")
        with col2:
            self_rating = avg_ratings.get('self_rating')
            st.metric("Self Rating", f"{self_rating:.1f}/100" if self_rating else "N/A")
        with col3:
            peer_avg = avg_ratings.get('peer_average')
            st.metric("Peer Average", f"{peer_avg:.1f}/100" if peer_avg else "N/A")
        with col4:
            manager_avg = avg_ratings.get('manager_average')
            st.metric("Manager Average", f"{manager_avg:.1f}/100" if manager_avg else "N/A")
        
        st.markdown("---")
        
        # Submit Review
        if user_role in ["owner", "manager"] or user_role == "employee":
            with st.expander("➕ Submit Review", expanded=False):
                with st.form("submit_review_form"):
                    reviewer_type = st.selectbox("Reviewer Type", ["self", "peer", "manager"], 
                                                 index=0 if user_role == "employee" else 2,
                                                 key="reviewer_type_select")
                    rating = st.slider("Rating (1-100)", 1, 100, 50, key="review_rating_slider")
                    comments = st.text_area("Comments", key="review_comments")
                    
                    if st.form_submit_button("💾 Submit Review"):
                        # Get reviewer ID
                        if reviewer_type == "self":
                            reviewer_id = selected_employee_id
                        elif reviewer_type == "peer":
                            reviewer_id = user_email  # Use email for peers
                        else:
                            reviewer_id = user_email  # Manager email
                        
                        result = review_360_agent.submit_review(
                            selected_employee_id, reviewer_id, reviewer_type, rating, comments
                        )
                        if result.get("success"):
                            st.success("✅ Review submitted successfully!")
                            st.rerun()
        
        # Review History
        if reviews:
            st.subheader("Review History")
            review_df = pd.DataFrame([
                {
                    "Type": r.get("reviewer_type", "N/A").title(),
                    "Rating": r.get("rating", 0),
                    "Comments": r.get("comments", "N/A")[:50] + "..." if r.get("comments") and len(r.get("comments", "")) > 50 else (r.get("comments", "N/A") or "N/A"),
                    "Date": r.get("created_at", "N/A")[:10]
                }
                for r in reviews
            ])
            st.dataframe(review_df, use_container_width=True, hide_index=True)
    
    # Tab 6: Promotion
    with tab6:
        st.subheader("⭐ Promotion Eligibility")
        
        eligibility = promotion_agent.check_promotion_eligibility(selected_employee_id)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Performance", f"{eligibility.get('performance_score', 0):.1f}", 
                    delta="✅" if eligibility.get('meets_performance') else "❌")
        with col2:
            st.metric("Attendance", f"{eligibility.get('attendance_percentage', 0):.1f}%",
                    delta="✅" if eligibility.get('meets_attendance') else "❌")
        with col3:
            st.metric("Goals", f"{eligibility.get('goal_completion_rate', 0):.1f}%",
                    delta="✅" if eligibility.get('meets_goals') else "❌")
        with col4:
            is_eligible = eligibility.get('is_eligible')
            st.metric("Status", "✅ Ready" if is_eligible else "⏳ Not Ready",
                    delta=eligibility.get('recommendation'))
        
        st.markdown("---")
        
        if is_eligible:
            st.success(f"🎉 **{selected_employee_name}** is ready for promotion!")
            st.write("**Criteria Met:**")
            st.write("✅ Performance Score > 80")
            st.write("✅ Attendance > 90%")
            st.write("✅ Goal Completion > 70%")
        else:
            st.info("📋 Promotion Criteria:")
            st.write(f"• Performance: {'✅' if eligibility.get('meets_performance') else '❌'} {eligibility.get('performance_score', 0):.1f}/80 required")
            st.write(f"• Attendance: {'✅' if eligibility.get('meets_attendance') else '❌'} {eligibility.get('attendance_percentage', 0):.1f}%/90 required")
            st.write(f"• Goals: {'✅' if eligibility.get('meets_goals') else '❌'} {eligibility.get('goal_completion_rate', 0):.1f}%/70 required")
        
        # Show all eligible employees (for managers/owners)
        if user_role in ["owner", "manager"]:
            st.markdown("---")
            st.subheader("📋 All Eligible Employees")
            eligible_employees = promotion_agent.get_all_eligible_employees()
            if eligible_employees:
                eligible_df = pd.DataFrame([
                    {
                        "Employee": e.get("employee_name", "N/A"),
                        "Performance": f"{e.get('performance_score', 0):.1f}",
                        "Attendance": f"{e.get('attendance_percentage', 0):.1f}%",
                        "Goals": f"{e.get('goal_completion_rate', 0):.1f}%"
                    }
                    for e in eligible_employees
                ])
                st.dataframe(eligible_df, use_container_width=True, hide_index=True)
            else:
                st.info("No employees currently meet all promotion criteria.")
    
    # Tab 7: Badges
    with tab7:
        st.subheader("🏆 Badges & Rewards")
        
        badges = badge_agent.get_employee_badges(selected_employee_id)
        
        st.metric("Total Badges", len(badges))
        
        st.markdown("---")
        
        # Auto-check and award badges
        if user_role in ["owner", "manager"]:
            if st.button("🔍 Check & Award Badges", use_container_width=True):
                with st.spinner("Checking eligibility for badges..."):
                    awarded = badge_agent.check_and_award_badges(selected_employee_id)
                    if awarded:
                        st.success(f"✅ Awarded {len(awarded)} new badge(s)!")
                        for badge in awarded:
                            st.write(f"🎉 {badge.get('badge_emoji')} {badge.get('badge_name')}")
                        st.rerun()
                    else:
                        st.info("No new badges to award at this time.")
        
        # Display Badges
        if badges:
            st.subheader("Earned Badges")
            badge_cols = st.columns(3)
            for idx, badge in enumerate(badges):
                with badge_cols[idx % 3]:
                    with st.container():
                        st.markdown(f"### {badge.get('badge_emoji')} {badge.get('badge_name')}")
                        st.write(badge.get('reason', 'N/A'))
                        st.caption(f"Awarded: {badge.get('awarded_at', 'N/A')[:10]}")
        else:
            st.info("No badges earned yet. Complete goals, maintain performance, and stay engaged to earn badges!")
        
        # Manual Badge Awarding (Managers/Owners only)
        if user_role in ["owner", "manager"]:
            st.markdown("---")
            with st.expander("➕ Manually Award Badge", expanded=False):
                with st.form("award_badge_form"):
                    badge_type = st.selectbox("Badge Type", list(badge_agent.BADGE_TYPES.keys()), key="badge_type_select")
                    reason = st.text_area("Reason", key="badge_reason")
                    
                    if st.form_submit_button("🏆 Award Badge"):
                        result = badge_agent.award_badge(selected_employee_id, badge_type, reason)
                        if result.get("success"):
                            st.success(f"✅ {result['badge']['badge_name']} awarded!")
                            st.rerun()


# Main app
def main():
    """Main application"""
    # Sidebar navigation
    if not st.session_state.authenticated:
        login_page()
    else:
        # Get user role first - needed for page initialization
        user_role = st.session_state.user.get("role", "employee")
        
        # Initialize current page in session state - employees default to "My Dashboard"
        if "current_page" not in st.session_state:
            if user_role == "employee":
                st.session_state.current_page = "My Dashboard"
            else:
                st.session_state.current_page = "Dashboard"
        
        # Redirect employees away from "Dashboard" to "My Dashboard"
        if user_role == "employee" and st.session_state.current_page == "Dashboard":
            st.session_state.current_page = "My Dashboard"
        
        # Compact sidebar header
        st.sidebar.markdown("### 📊 Performance System")
        st.sidebar.markdown(f"**{st.session_state.user.get('name', 'User')}** ({st.session_state.user.get('role', 'employee').title()})")
        st.sidebar.markdown("---")
        
        # Navigation buttons - role-based filtering
        all_pages = [
            ("Dashboard", "📊", ["owner", "manager"]),  # Employees see "My Dashboard" instead
            ("My Dashboard", "👤", ["employee"]),  # Only for employees
            ("Projects", "📁", ["owner", "manager"]),  # Employees can't access
            ("Tasks", "✅", ["owner", "manager", "employee"]),  # Employees see "My Tasks" only
            ("Employees", "👥", ["owner", "manager"]),  # Employees can't access
            ("Performance", "📈", ["owner", "manager", "employee"]),  # Employees see own only
            ("Employee Development", "🚀", ["owner", "manager", "employee"]),  # New comprehensive page
            ("Analytics", "🔍", ["owner", "manager"]),  # Employees can't access
            ("Risks", "⚠️", ["owner", "manager"]),  # Employees can't access
            ("Goals", "🎯", ["owner", "manager", "employee"]),  # Employees see own only
            ("Feedback", "💬", ["owner", "manager", "employee"]),
            ("Notifications", "🔔", ["owner", "manager", "employee"]),
            ("Export", "📤", ["owner", "manager"]),  # Employees can't access
            ("Comparison", "⚖️", ["owner", "manager"])  # Employees can't access
        ]
        
        # Filter pages based on role
        pages = [(name, icon) for name, icon, roles in all_pages if user_role in roles]
        
        for page_name, icon in pages:
            if st.sidebar.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()
        
        # Logout button at bottom - compact spacing
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.current_page = None  # Will be set on next login based on role
            st.rerun()
        
        # Display current page
        current_page = st.session_state.current_page
        
        if current_page == "Dashboard":
            dashboard()
        elif current_page == "My Dashboard":
            employee_dashboard_page()
        elif current_page == "Projects":
            projects_page()
        elif current_page == "Tasks":
            tasks_page()
        elif current_page == "Employees":
            employees_page()
        elif current_page == "Performance":
            performance_page()
        elif current_page == "Employee Development":
            employee_development_page()
        elif current_page == "Analytics":
            analytics_page()
        elif current_page == "Risks":
            risks_page()
        elif current_page == "Goals":
            goals_page()
        elif current_page == "Feedback":
            feedback_page()
        elif current_page == "Notifications":
            notifications_page()
        elif current_page == "Export":
            export_page()
        elif current_page == "Comparison":
            comparison_page()

if __name__ == "__main__":
    main()
