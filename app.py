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
from components.managers.event_bus import get_event_bus, set_event_bus, EventBus

# Check if we should use API backend
USE_API_BACKEND = os.getenv("USE_API_BACKEND", "false").lower() == "true"

# Conditionally import API client (only if needed)
# Use lazy import to avoid issues if module doesn't exist
APIClient = None
if USE_API_BACKEND:
    try:
        import importlib
        api_client_module = importlib.import_module("components.managers.api_client")
        APIClient = api_client_module.APIClient
    except (ImportError, ModuleNotFoundError, AttributeError) as e:
        print(f"Warning: API client not available: {e}")
        print("To use API backend, install httpx: pip install httpx")
        USE_API_BACKEND = False
        APIClient = None

if not USE_API_BACKEND:
    # Direct agent imports (legacy mode)
    from components.agents.performance_agent import EnhancedPerformanceAgent
    from components.agents.reporting_agent import ReportingAgent
    from components.agents.notification_agent import NotificationAgent
    from components.agents.export_agent import ExportAgent
    from components.agents.goal_agent import GoalAgent
    from components.agents.feedback_agent import FeedbackAgent
    from components.agents.promotion_agent import PromotionAgent
    from components.agents.event_handlers import EventHandlers

# Page configuration
st.set_page_config(
    page_title="Employee Performance Report System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Black & Orange Theme
st.markdown("""
    <script>
    (function() {
        function forceDarkInputs() {
            const inputs = document.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                // Always force the dark background, regardless of current style
                input.style.setProperty('background-color', '#0A0A0A', 'important');
                input.style.setProperty('background', '#0A0A0A', 'important');
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
        
        // Ensure select elements are clickable and styled properly
        function styleSelectboxes() {
            const selectElements = document.querySelectorAll('select');
            selectElements.forEach(select => {
                select.style.cursor = 'pointer';
            });
            
            // Style selectbox inputs for better UX
            const selectboxInputs = document.querySelectorAll('[data-baseweb="select"] input, .stSelectbox input');
            selectboxInputs.forEach(input => {
                input.style.cursor = 'pointer';
            });
        }
        
        // Run styling function
        styleSelectboxes();
        setInterval(styleSelectboxes, 1000);
        
        // Watch for new selectboxes
        const selectObserver = new MutationObserver(function(mutations) {
            styleSelectboxes();
        });
        selectObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Fix dropdown menu backgrounds (override blue backgrounds)
        function fixDropdownStyles() {
            // Find all dropdown popovers
            const popovers = document.querySelectorAll('[data-baseweb="popover"]');
            popovers.forEach(popover => {
                popover.style.backgroundColor = '#0A0A0A';
                popover.style.background = '#0A0A0A';
                popover.style.color = '#FFFFFF';
                
                // Fix all options inside
                const options = popover.querySelectorAll('[role="option"], li, div[role="option"]');
                options.forEach(option => {
                    option.style.backgroundColor = '#0A0A0A';
                    option.style.background = '#0A0A0A';
                    option.style.color = '#FFFFFF';
                });
            });
            
            // Find any divs with blue backgrounds that might be dropdowns
            const allDivs = document.querySelectorAll('div[style*="position: absolute"]');
            allDivs.forEach(div => {
                const style = div.getAttribute('style') || '';
                if (style.includes('background') && (style.includes('rgb(255') || style.includes('rgba(255') || style.includes('rgb(240') || style.includes('rgba(240'))) {
                    div.style.backgroundColor = '#0A0A0A';
                    div.style.background = '#0A0A0A';
                    div.style.color = '#FFFFFF';
                }
            });
        }
        
        // Run immediately and on intervals
        fixDropdownStyles();
        setInterval(fixDropdownStyles, 500);
        
        // Watch for new dropdowns
        const dropdownObserver = new MutationObserver(fixDropdownStyles);
        dropdownObserver.observe(document.body, { childList: true, subtree: true });
        
        // Fix calendar/date picker styling
        function fixCalendarStyles() {
            // Find all calendar popovers
            const calendars = document.querySelectorAll('[data-baseweb="popover"], [data-baseweb="calendar"]');
            calendars.forEach(calendar => {
                calendar.style.backgroundColor = '#0A0A0A';
                calendar.style.background = '#0A0A0A';
                calendar.style.color = '#FFFFFF';
                
                // Fix all tables inside calendar
                const tables = calendar.querySelectorAll('table');
                tables.forEach(table => {
                    table.style.backgroundColor = '#0A0A0A';
                    table.style.background = '#0A0A0A';
                    table.style.color = '#FFFFFF';
                    
                    // Fix all cells
                    const cells = table.querySelectorAll('td, th');
                    cells.forEach(cell => {
                        const style = cell.getAttribute('style') || '';
                        // Override any light backgrounds
                        if (style.includes('background') && (style.includes('rgb(255') || style.includes('rgba(255') || style.includes('rgb(240'))) {
                            if (cell.getAttribute('aria-selected') === 'true') {
                                cell.style.backgroundColor = '#FF6B35';
                                cell.style.color = '#000000';
                            } else {
                                cell.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
                                cell.style.color = '#FFFFFF';
                            }
                        }
                    });
                });
            });
            
            // Find any divs with tables that might be calendars
            const allDivs = document.querySelectorAll('div[style*="position: absolute"], div[style*="position: fixed"]');
            allDivs.forEach(div => {
                const hasTable = div.querySelector('table');
                if (hasTable) {
                    const style = div.getAttribute('style') || '';
                    if (style.includes('background') && (style.includes('rgb(255') || style.includes('rgba(255') || style.includes('rgb(240'))) {
                        div.style.backgroundColor = '#000000';
                        div.style.background = '#000000';
                        div.style.color = '#FFFFFF';
                    }
                }
            });
        }
        
        // Run immediately and on intervals
        fixCalendarStyles();
        setInterval(fixCalendarStyles, 500);
        
        // Watch for new calendars
        const calendarObserver = new MutationObserver(fixCalendarStyles);
        calendarObserver.observe(document.body, { childList: true, subtree: true });
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
        background-color: #000000 !important;
        background: #000000 !important;
    }
    
    /* Override any element with light gray background */
    *[style*="240, 242, 246"],
    *[style*="rgb(240, 242, 246)"] {
        background-color: #000000 !important;
        background: #000000 !important;
    }
    
    /* ===== MAIN APP BACKGROUND ===== */
    .stApp {
        background-color: #000000 !important;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 107, 53, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 140, 66, 0.03) 0%, transparent 50%);
        color: #FFFFFF !important;
    }
    
    /* ===== HEADER & NAVBAR ===== */
    [data-testid="stHeader"] {
        background-color: #0A0A0A !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(14px);
        box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.1);
    }
    
    [data-testid="stToolbar"] {
        background-color: #0A0A0A !important;
    }
    
    [data-testid="stDecoration"] {
        background-color: #0A0A0A !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: #0A0A0A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #20477d !important;
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
        color: #FFFFFF !important;
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
        background-color: rgba(255, 107, 53, 0.15) !important;
        border-color: #FF6B35 !important;
        color: #FF6B35 !important;
        box-shadow: 0 0 12px rgba(255, 107, 53, 0.4) !important;
        transform: translateX(5px) scale(1.02) !important;
    }
    
    /* Active sidebar button */
    .stSidebar .stButton > button:focus,
    .stSidebar .stButton > button:active {
        background-color: rgba(255, 107, 53, 0.2) !important;
        border-color: #FF6B35 !important;
        color: #FF6B35 !important;
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
        border-bottom: 2px solid rgba(255, 107, 53, 0.3) !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
    }
    
    /* Remove any orange/red borders from headers and tabs */
    h1, h2, h3, h4, h5, h6 {
        border-color: rgba(255, 107, 53, 0.3) !important;
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
        border-bottom: 2px solid #FF6B35 !important;
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
        color: #CCCCCC !important;
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
        background-color: #0A0A0A !important;
        background: #0A0A0A !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        caret-color: #FF6B35 !important;
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
        background-color: #0A0A0A !important;
        background: #0A0A0A !important;
    }
    
    /* Force dark background on ALL input elements - most aggressive override */
    input,
    textarea,
    select {
        background-color: #0A0A0A !important;
        background: #0A0A0A !important;
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
        background-color: #0A0A0A !important;
        background: #0A0A0A !important;
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
        border-color: #FF6B35 !important;
        outline: none !important;
        box-shadow: 0 0 10px rgba(255, 107, 53, 0.4) !important;
        background-color: rgb(25, 18, 24) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder,
    .stNumberInput > div > div > input::placeholder,
    .stDateInput > div > div > input::placeholder {
        color: #CCCCCC !important;
        opacity: 0.8 !important;
    }
    
    /* ===== CALENDAR/DATE PICKER STYLING ===== */
    /* Calendar popover container */
    [data-baseweb="popover"][role="dialog"],
    div[data-baseweb="popover"][role="dialog"],
    /* Calendar widget container */
    [data-baseweb="calendar"],
    div[data-baseweb="calendar"],
    /* Any div that contains a calendar */
    div[style*="position: absolute"][style*="z-index"]:has(table),
    div[style*="position: fixed"][style*="z-index"]:has(table) {
        background-color: #000000 !important;
        background: #000000 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        color: #FFFFFF !important;
    }
    
    /* Calendar table */
    table[role="grid"],
    [data-baseweb="calendar"] table,
    div[data-baseweb="popover"] table,
    /* Streamlit calendar tables */
    .stDateInput table,
    [data-baseweb="calendar"] > div > table {
        background-color: #000000 !important;
        background: #000000 !important;
        color: #FFFFFF !important;
        border-collapse: separate !important;
        border-spacing: 4px !important;
    }
    
    /* Calendar header (month/year) */
    [data-baseweb="calendar"] th,
    [data-baseweb="popover"] th,
    table[role="grid"] th,
    .stDateInput th,
    [data-baseweb="calendar"] > div > table th {
        background-color: transparent !important;
        background: transparent !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        padding: 10px !important;
        border: none !important;
    }
    
    /* Calendar day names (Su, Mo, Tu, etc.) */
    [data-baseweb="calendar"] th[role="columnheader"],
    [data-baseweb="popover"] th[role="columnheader"],
    table[role="grid"] th[role="columnheader"],
    .stDateInput th[role="columnheader"] {
        background-color: rgba(255, 107, 53, 0.1) !important;
        background: rgba(255, 107, 53, 0.1) !important;
        color: #FF6B35 !important;
        font-weight: 500 !important;
        padding: 8px 4px !important;
        border-radius: 6px !important;
    }
    
    /* Calendar day cells */
    [data-baseweb="calendar"] td,
    [data-baseweb="popover"] td,
    table[role="grid"] td,
    .stDateInput td,
    [data-baseweb="calendar"] > div > table td {
        background-color: rgba(255, 255, 255, 0.05) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
        padding: 8px !important;
        border-radius: 6px !important;
        text-align: center !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    
    /* Calendar day cells - hover state */
    [data-baseweb="calendar"] td:hover,
    [data-baseweb="popover"] td:hover,
    table[role="grid"] td:hover,
    .stDateInput td:hover,
    [data-baseweb="calendar"] > div > table td:hover {
        background-color: rgba(255, 107, 53, 0.2) !important;
        background: rgba(255, 107, 53, 0.2) !important;
        color: #FF6B35 !important;
        transform: scale(1.05) !important;
    }
    
    /* Selected date */
    [data-baseweb="calendar"] td[aria-selected="true"],
    [data-baseweb="popover"] td[aria-selected="true"],
    table[role="grid"] td[aria-selected="true"],
    .stDateInput td[aria-selected="true"],
    [data-baseweb="calendar"] > div > table td[aria-selected="true"],
    /* Also target cells with selected class or style */
    td[class*="selected"],
    td[style*="background"][style*="rgb(255"] {
        background-color: #FF6B35 !important;
        background: #FF6B35 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        box-shadow: 0 0 10px rgba(255, 107, 53, 0.5) !important;
    }
    
    /* Today's date (if different from selected) */
    [data-baseweb="calendar"] td[aria-label*="today"],
    [data-baseweb="popover"] td[aria-label*="today"],
    table[role="grid"] td[aria-label*="today"],
    .stDateInput td[aria-label*="today"] {
        border: 2px solid #FF6B35 !important;
        background-color: rgba(255, 107, 53, 0.1) !important;
    }
    
    /* Disabled/out-of-range dates */
    [data-baseweb="calendar"] td[aria-disabled="true"],
    [data-baseweb="popover"] td[aria-disabled="true"],
    table[role="grid"] td[aria-disabled="true"],
    .stDateInput td[aria-disabled="true"],
    td[class*="disabled"],
    td[style*="opacity"][style*="0.5"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: rgba(255, 255, 255, 0.3) !important;
        cursor: not-allowed !important;
    }
    
    /* Calendar navigation buttons (prev/next month) */
    [data-baseweb="calendar"] button,
    [data-baseweb="popover"] button,
    [data-baseweb="calendar"] > div > button,
    /* Arrow buttons in calendar */
    button[aria-label*="previous"],
    button[aria-label*="next"],
    button[aria-label*="Previous"],
    button[aria-label*="Next"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    
    [data-baseweb="calendar"] button:hover,
    [data-baseweb="popover"] button:hover,
    button[aria-label*="previous"]:hover,
    button[aria-label*="next"]:hover {
        background-color: rgba(255, 107, 53, 0.2) !important;
        border-color: #FF6B35 !important;
        color: #FF6B35 !important;
    }
    
    /* Calendar month/year selector */
    [data-baseweb="calendar"] select,
    [data-baseweb="popover"] select,
    [data-baseweb="calendar"] > div > select {
        background-color: #000000 !important;
        background: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
    }
    
    /* Override any inline styles on calendar elements */
    [data-baseweb="calendar"] *,
    [data-baseweb="popover"] *,
    table[role="grid"] * {
        color: inherit !important;
    }
    
    /* Force dark background on calendar popover - override inline styles */
    div[style*="position: absolute"][style*="z-index"]:has(table),
    div[style*="position: fixed"][style*="z-index"]:has(table),
    div[style*="background"][style*="rgb(255"]:has(table),
    div[style*="background"][style*="rgba(255"]:has(table) {
        background-color: #000000 !important;
        background: #000000 !important;
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
    
    /* Ensure select elements are clickable and focusable */
    select:focus {
        outline: 2px solid #FF6B35 !important;
        outline-offset: 2px !important;
    }
    
    /* Make sure selectbox container allows clicks */
    [data-baseweb="select"] {
        cursor: pointer !important;
    }
    
    /* Allow clicks on selectbox inputs to open dropdown */
    [data-baseweb="select"] input {
        cursor: pointer !important;
        pointer-events: auto !important;
    }
    
    input, textarea, select {
        color: #FFFFFF !important;
        caret-color: #FF6B35 !important;
        background-color: rgb(25, 18, 24) !important;
    }
    
    /* Style dropdown menu options (the actual dropdown list) - OVERRIDE ALL BLUE BACKGROUNDS */
    [data-baseweb="select"] [role="listbox"],
    [data-baseweb="select"] [role="option"],
    [data-baseweb="select"] ul,
    [data-baseweb="select"] li,
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] [role="listbox"],
    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li,
    /* Streamlit's dropdown menu */
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] > div > div > div,
    /* Baseweb popover (dropdown container) */
    [data-baseweb="popover"],
    div[style*="position: absolute"][style*="z-index"],
    /* Override any blue/rgb backgrounds */
    div[style*="background-color: rgb"][style*="position: absolute"],
    div[style*="background: rgb"][style*="position: absolute"],
    div[style*="background-color: rgba"][style*="position: absolute"],
    div[style*="background: rgba"][style*="position: absolute"] {
        background-color: #000000 !important;
        background: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Dropdown option items */
    [data-baseweb="select"] [role="option"],
    [data-baseweb="popover"] [role="option"],
    li[role="option"],
    div[role="option"],
    [data-baseweb="select"] li,
    [data-baseweb="popover"] li {
        background-color: #000000 !important;
        background: #000000 !important;
        color: #FFFFFF !important;
        padding: 10px 14px !important;
    }
    
    /* Hover state for dropdown options */
    [data-baseweb="select"] [role="option"]:hover,
    [data-baseweb="popover"] [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover,
    [data-baseweb="select"] li:hover,
    [data-baseweb="popover"] li:hover {
        background-color: rgba(255, 107, 53, 0.1) !important;
        background: rgba(255, 107, 53, 0.1) !important;
        color: #FF6B35 !important;
    }
    
    /* Selected option in dropdown */
    [data-baseweb="select"] [role="option"][aria-selected="true"],
    [data-baseweb="popover"] [role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background-color: rgba(255, 107, 53, 0.2) !important;
        background: rgba(255, 107, 53, 0.2) !important;
        color: #FF6B35 !important;
    }
    
    /* Override any blue backgrounds in dropdowns - most aggressive */
    [data-baseweb="select"] *,
    [data-baseweb="popover"] * {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    [data-baseweb="select"] [role="listbox"],
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="select"] ul,
    [data-baseweb="popover"] ul {
        background-color: #000000 !important;
        background: #000000 !important;
    }
    
    /* Force black background on all dropdown containers - override inline styles */
    div[data-baseweb="popover"],
    div[style*="position: absolute"][style*="z-index"][style*="background"],
    [data-baseweb="select"] > div[style*="background"],
    /* Target any div with blue/light background that's a dropdown */
    div[style*="rgb(255"][style*="position"],
    div[style*="rgba(255"][style*="position"],
    div[style*="rgb(240"][style*="position"],
    div[style*="rgba(240"][style*="position"] {
        background-color: #000000 !important;
        background: #000000 !important;
    }
    
    /* Override any inline style backgrounds on dropdown elements */
    [data-baseweb="popover"][style*="background"],
    [data-baseweb="select"][style*="background"],
    [role="listbox"][style*="background"],
    [role="option"][style*="background"] {
        background-color: #000000 !important;
        background: #000000 !important;
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
        background-color: #0A0A0A !important;
        background: #0A0A0A !important;
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
        background-color: #0A0A0A !important;
        background: #0A0A0A !important;
    }
    
    /* ===== BUTTONS ===== */
    /* Primary Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #FF6B35, #FF8C42) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        font-weight: 600 !important;
        text-transform: none !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
        letter-spacing: 0.2px;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 18px rgba(255, 107, 53, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 24px rgba(255, 107, 53, 0.6) !important;
        background: linear-gradient(90deg, #FF8C42, #FF6B35) !important;
        color: #000000 !important;
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
    
    /* Dark blue text for gradient buttons */
    .stButton > button,
    .stButton > button *,
    .stForm button[type="submit"],
    .stForm button[type="submit"] *,
    .stForm .stButton > button,
    .stForm .stButton > button * {
        color: #000000 !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: #FF6B35 !important;
        color: #FF6B35 !important;
        box-shadow: 0 0 12px rgba(255, 107, 53, 0.3) !important;
        transform: scale(1.01) !important;
    }
    
    /* Form Submit Buttons */
    .stForm button[type="submit"],
    .stForm .stButton > button {
        background: linear-gradient(90deg, #FF6B35, #FF8C42) !important;
        color: #000000 !important;
        border: none !important;
    }
    
    .stForm button[type="submit"]:hover,
    .stForm .stButton > button:hover {
        background: linear-gradient(90deg, #FF8C42, #FF6B35) !important;
        box-shadow: 0 0 24px rgba(255, 107, 53, 0.6) !important;
        color: #000000 !important;
    }
    
    /* Force dark background on form inputs - override any inline styles */
    .stForm input[type="text"],
    .stForm input[type="email"],
    .stForm input[type="password"],
    .stForm input[type="number"],
    .stForm textarea,
    .stForm select {
        background-color: #0A0A0A !important;
        background: #0A0A0A !important;
        color: #FFFFFF !important;
    }
    
    
    /* ===== CARDS & CONTAINERS ===== */
    .dashboard-card, .content-card, .achievement-card {
        background-color: #1A1A1A !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(14px);
    }
    
    .dashboard-card:hover, .content-card:hover, .achievement-card:hover {
        box-shadow: 0 0 12px rgba(255, 107, 53, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
        border-color: rgba(255, 107, 53, 0.3) !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetricContainer"] {
        background-color: #1A1A1A !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stMetricContainer"]:hover {
        box-shadow: 0 0 12px rgba(255, 107, 53, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
        border-color: rgba(255, 107, 53, 0.3) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #FF6B35 !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #CCCCCC !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* ===== TABLES & DATAFRAMES ===== */
    .dataframe {
        background-color: #1A1A1A !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        overflow-x: auto !important;
        box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05) !important;
    }
    
    .dataframe th {
        background-color: #1A2337 !important;
        color: #FF6B35 !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    .dataframe td {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        padding: 10px 12px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(255, 107, 53, 0.05) !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #1A1A1A !important;
    }
    
    .dataframe tbody tr:nth-child(odd) {
        background-color: #0A0A0A !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: #1A1A1A !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05) !important;
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
        color: #CCCCCC !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        margin-right: 0.5rem !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1A1A1A !important;
        color: #FF6B35 !important;
        font-weight: 600 !important;
        border-bottom: none !important;
    }
    
    .stTabs [aria-selected="false"]:hover {
        background-color: rgba(255, 107, 53, 0.1) !important;
        color: #FF6B35 !important;
    }
    
    /* Tab highlight indicator - primary blue background */
    [data-baseweb="tab-highlight"] {
        background-color: #FF6B35 !important;
        border-radius: 10px !important;
        opacity: 1 !important;
    }
    
    /* ===== FORMS ===== */
    .stForm {
        background-color: #1A1A1A !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05) !important;
    }
    
    label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-family: 'Inter', 'Poppins', sans-serif !important;
    }
    
    /* ===== ALERTS & MESSAGES ===== */
    .stInfo {
        background-color: rgba(255, 140, 66, 0.1) !important;
        border-left: 4px solid #FF6B35 !important;
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
        background-color: rgba(255, 107, 53, 0.1) !important;
        border-left: 4px solid #FF6B35 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background-color: rgba(255, 107, 53, 0.1) !important;
        border-left: 4px solid #FF6B35 !important;
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
        background: #FF6B35;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #FF8C42;
    }
    
    /* ===== PROGRESS BARS ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FF6B35, #FF8C42) !important;
    }
    
    .stProgress > div {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border-radius: 10px !important;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background-color: #1A1A1A !important;
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
        color: #FF6B35 !important;
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
        background-color: #0A0A0A !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 20px !important;
    }
    
    /* ===== CODE BLOCKS ===== */
    code {
        background-color: #1A1A1A !important;
        color: #FF6B35 !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        font-family: 'Courier New', monospace !important;
    }
    
    pre {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 16px !important;
        overflow-x: auto;
    }
    
    /* ===== LINKS ===== */
    a {
        color: #FF6B35 !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
    }
    
    a:hover {
        color: #FF8C42 !important;
        text-decoration: underline !important;
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin: 24px 0 !important;
    }
    
    /* ===== SELECTBOX DROPDOWN ===== */
    /* Dark background for selectbox dropdown menu */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"],
    [data-baseweb="select"] [role="listbox"],
    ul[role="listbox"],
    div[role="listbox"],
    /* BaseWeb dropdown menu */
    [data-baseweb="select"] ~ div[data-baseweb="popover"],
    /* Streamlit selectbox dropdown */
    .stSelectbox [data-baseweb="popover"],
    .stSelectbox [data-baseweb="menu"],
    .stSelectbox ul[role="listbox"],
    .stSelectbox div[role="listbox"] {
        background-color: #1A1A1A !important;
        background: #1A1A1A !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.1) !important;
    }
    
    /* Dark background for dropdown options */
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"],
    [role="listbox"] li,
    [role="listbox"] [role="option"],
    ul[role="listbox"] li,
    div[role="listbox"] [role="option"],
    /* BaseWeb option items */
    [data-baseweb="select"] ~ div [role="option"],
    [data-baseweb="select"] ~ div li {
        background-color: #1A1A1A !important;
        background: #1A1A1A !important;
        color: #FFFFFF !important;
    }
    
    /* Hover state for dropdown options */
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [role="listbox"] li:hover,
    [role="listbox"] [role="option"]:hover,
    ul[role="listbox"] li:hover,
    div[role="listbox"] [role="option"]:hover,
    [data-baseweb="select"] ~ div [role="option"]:hover,
    [data-baseweb="select"] ~ div li:hover {
        background-color: rgba(255, 107, 53, 0.15) !important;
        color: #FF6B35 !important;
    }
    
    /* Selected option in dropdown */
    [data-baseweb="menu"] li[aria-selected="true"],
    [role="listbox"] [role="option"][aria-selected="true"],
    [data-baseweb="select"] ~ div [role="option"][aria-selected="true"] {
        background-color: rgba(255, 107, 53, 0.2) !important;
        color: #FF6B35 !important;
    }
    
    /* Selectbox input field */
    [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
    }
    
    /* Selectbox input text color */
    [data-baseweb="select"] input,
    .stSelectbox input,
    [data-baseweb="select"] > div > div {
        color: #FFFFFF !important;
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
        color: #FF6B35 !important;
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
        background-color: #0A0A0A !important;
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
    
    /* ===== MULTISELECT TAGS ===== */
    /* Change multiselect selected item tags from red to blue */
    [data-baseweb="tag"] {
        background-color: #FF6B35 !important;
        background: #FF6B35 !important;
        color: #FFFFFF !important;
        border-color: #FF6B35 !important;
    }
    
    /* Multiselect tag hover state */
    [data-baseweb="tag"]:hover {
        background-color: #FF8C42 !important;
        border-color: #FF8C42 !important;
    }
    
    /* Multiselect input container */
    [data-baseweb="select"] [data-baseweb="tag"] {
        background-color: #FF6B35 !important;
        background: #FF6B35 !important;
        color: #FFFFFF !important;
    }
    
    /* Override any red/error colors in multiselect */
    [data-baseweb="tag"][style*="rgb(255"],
    [data-baseweb="tag"][style*="red"],
    [data-baseweb="tag"][style*="#ff"] {
        background-color: #FF6B35 !important;
        background: #FF6B35 !important;
        border-color: #FF6B35 !important;
    }
    
    /* Streamlit multiselect specific classes */
    .stMultiSelect [data-baseweb="tag"],
    .stMultiSelect [role="option"][aria-selected="true"] {
        background-color: #FF6B35 !important;
        background: #FF6B35 !important;
        color: #FFFFFF !important;
        border-color: #FF6B35 !important;
    }
    
    /* Override orange color for .st-dw class */
    .st-dw {
        background-color: rgb(7, 16, 79) !important;
        background: rgb(7, 16, 79) !important;
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
    st.dataframe(df, hide_index=True)
    
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
                if st.button("✏️ Edit", key=f"edit_btn_{item_id}"):
                    edit_callback(item)
            with btn_col2:
                if st.button("🗑️ Del", key=f"delete_btn_{item_id}", type="secondary"):
                    delete_callback(item)

# Helper function to convert JSON/dict to table
def _display_formatted_summary(data_list):
    """Display data as formatted summary with metrics instead of raw table"""
    if not data_list or len(data_list) == 0:
        return
    
    # Determine data type from first item
    first_item = data_list[0]
    
    # Goals summary
    if "goal_type" in first_item or "target_value" in first_item:
        total = len(data_list)
        completed = len([g for g in data_list if g.get("status") == "completed"])
        in_progress = len([g for g in data_list if g.get("status") == "in_progress"])
        overdue = len([g for g in data_list if g.get("deadline") and datetime.fromisoformat(g.get("deadline", "")) < datetime.now() and g.get("status") != "completed"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Goals", total)
        with col2:
            st.metric("Completed", completed)
        with col3:
            st.metric("In Progress", in_progress)
        with col4:
            st.metric("Overdue", overdue)
        
        # Show top 3 goals
        if len(data_list) > 0:
            st.markdown("#### Top Goals")
            for i, goal in enumerate(data_list[:3], 1):
                progress = goal.get("progress_percentage", 0)
                st.write(f"**{i}. {goal.get('title', 'Untitled')}** - {progress:.1f}% complete")
    
    # Tasks summary
    elif "priority" in first_item or "due_date" in first_item:
        total = len(data_list)
        completed = len([t for t in data_list if t.get("status") == "completed"])
        pending = len([t for t in data_list if t.get("status") == "pending"])
        in_progress = len([t for t in data_list if t.get("status") == "in_progress"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", total)
        with col2:
            st.metric("Completed", completed)
        with col3:
            st.metric("Pending", pending)
        with col4:
            st.metric("In Progress", in_progress)
        
        # Show top 3 tasks
        if len(data_list) > 0:
            st.markdown("#### Recent Tasks")
            for i, task in enumerate(data_list[:3], 1):
                status_emoji = {"completed": "✅", "in_progress": "🔄", "pending": "⏳"}
                st.write(f"**{i}. {task.get('title', 'Untitled')}** {status_emoji.get(task.get('status'), '📋')} {task.get('status', 'N/A')}")
    
    # Performance summary
    elif "performance_score" in first_item:
        avg_score = sum(p.get("performance_score", 0) for p in data_list) / len(data_list) if data_list else 0
        st.metric("Average Performance Score", f"{avg_score:.1f}")
    
    # Default: show count and key metrics
    else:
        st.metric("Total Items", len(data_list))
        if len(data_list) > 0:
            st.info(f"Showing {len(data_list)} item(s). Use specific queries to see detailed information.")

def _display_formatted_metrics(data_dict):
    """Display dictionary data as formatted metrics"""
    if not data_dict:
        return
    
    # Create columns for metrics
    cols = st.columns(min(4, len(data_dict)))
    for idx, (key, value) in enumerate(data_dict.items()):
        if idx < len(cols):
            with cols[idx]:
                # Format key name
                display_key = key.replace("_", " ").title()
                if isinstance(value, (int, float)):
                    st.metric(display_key, f"{value:.1f}" if isinstance(value, float) else value)
                else:
                    st.metric(display_key, str(value))

def display_as_table(data):
    """Convert JSON/dict data to a representative visual format"""
    if not data:
        st.info("No data to display")
        return
    
    if isinstance(data, dict):
        # Display as metric cards or key-value pairs in a more visual way
        num_items = len(data)
        if num_items <= 6:
            # Use columns for small datasets
            cols = st.columns(min(3, num_items))
            for idx, (key, value) in enumerate(data.items()):
                with cols[idx % len(cols)]:
                    # Format value for display
                    if isinstance(value, dict):
                        # Display nested dictionary as formatted string
                        nested_items = []
                        for k, v in value.items():
                            if isinstance(v, (int, float)):
                                formatted_v = f"{v:,.2f}" if isinstance(v, float) else f"{v:,}"
                            else:
                                formatted_v = str(v)
                            nested_items.append(f"{str(k).replace('_', ' ').title()}: {formatted_v}")
                        display_value = "<br>".join(nested_items)
                        st.markdown(f"""
                            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); 
                                        border-radius: 12px; padding: 15px; margin-bottom: 10px;">
                                <div style="font-size: 0.85rem; color: #CCCCCC; margin-bottom: 8px; font-weight: 600;">{str(key).replace('_', ' ').title()}</div>
                                <div style="font-size: 0.95rem; color: #FF6B35; line-height: 1.6;">{display_value}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif isinstance(value, list):
                        display_value = f"{len(value)} items"
                        st.markdown(f"""
                            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); 
                                        border-radius: 12px; padding: 15px; margin-bottom: 10px;">
                                <div style="font-size: 0.85rem; color: #CCCCCC; margin-bottom: 5px;">{str(key).replace('_', ' ').title()}</div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: #FF6B35;">{display_value}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Format numeric values
                        if isinstance(value, (int, float)):
                            display_value = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
                        elif isinstance(value, str) and 'T' in value:
                            # Handle datetime strings - show only date
                            display_value = value.split('T')[0] if 'T' in value else value
                        else:
                            display_value = str(value)
                        
                        st.markdown(f"""
                            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); 
                                        border-radius: 12px; padding: 15px; margin-bottom: 10px;">
                                <div style="font-size: 0.85rem; color: #CCCCCC; margin-bottom: 5px;">{str(key).replace('_', ' ').title()}</div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: #FF6B35;">{display_value}</div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            # For larger datasets, use a grid layout
            items_per_row = 3
            items = list(data.items())
            for i in range(0, len(items), items_per_row):
                row_items = items[i:i+items_per_row]
                cols = st.columns(len(row_items))
                for col_idx, (key, value) in enumerate(row_items):
                    with cols[col_idx]:
                        if isinstance(value, (dict, list)):
                            display_value = f"{len(value)} items" if isinstance(value, list) else "Nested data"
                        else:
                            display_value = f"{value:,.2f}" if isinstance(value, float) else (f"{value:,}" if isinstance(value, int) else str(value))
                        
                        st.markdown(f"""
                            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); 
                                        border-radius: 12px; padding: 15px; margin-bottom: 10px;">
                                <div style="font-size: 0.85rem; color: #CCCCCC; margin-bottom: 5px;">{str(key).replace('_', ' ').title()}</div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: #FF6B35;">{display_value}</div>
                            </div>
                        """, unsafe_allow_html=True)
    elif isinstance(data, list):
        if data and isinstance(data[0], dict):
            # List of dictionaries - display as table with index
            data_with_index = []
            for idx, item in enumerate(data, start=1):
                item_copy = item.copy()
                item_copy['#'] = idx
                # Move index to first position
                data_with_index.append({'#': idx, **{k: v for k, v in item_copy.items() if k != '#'}})
            df = pd.DataFrame(data_with_index)
            # Reorder columns to put # first
            cols = ['#'] + [col for col in df.columns if col != '#']
            df = df[cols]
            st.dataframe(df, hide_index=True)
        else:
            # Simple list - display as cards
            cols = st.columns(min(3, len(data)))
            for idx, val in enumerate(data):
                with cols[idx % len(cols)]:
                    st.markdown(f"""
                        <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); 
                                    border-radius: 12px; padding: 15px; margin-bottom: 10px;">
                            <div style="font-size: 0.85rem; color: #CCCCCC; margin-bottom: 5px;">Item #{idx + 1}</div>
                            <div style="font-size: 1.2rem; font-weight: 600; color: #FF6B35;">{str(val)}</div>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        # Simple value - display as metric card
        st.markdown(f"""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); 
                        border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 600; color: #FF6B35;">{str(data)}</div>
            </div>
        """, unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

if USE_API_BACKEND:
    # API mode - use API client
    if "api_client" not in st.session_state:
        if APIClient is None:
            st.error("⚠️ API client not available. Please install httpx: `pip install httpx`")
            USE_API_BACKEND = False
        else:
            st.session_state.api_client = APIClient()
else:
    # Direct mode - use agents directly
    if "data_manager" not in st.session_state:
        st.session_state.data_manager = DataManager()
    if "auth_manager" not in st.session_state:
        st.session_state.auth_manager = AuthManager(st.session_state.data_manager)
    # Initialize event bus and handlers (event-driven architecture)
    if "event_bus" not in st.session_state:
        st.session_state.event_bus = EventBus()
        set_event_bus(st.session_state.event_bus)
    if "event_handlers" not in st.session_state:
        from components.agents.event_handlers import EventHandlers
        st.session_state.event_handlers = EventHandlers(st.session_state.data_manager)

# Initialize agents
def initialize_agents():
    """Initialize essential agents for performance reports and feedback (6 agents only)"""
    data_manager = st.session_state.data_manager
    notification_agent = NotificationAgent(data_manager)
    performance_agent = EnhancedPerformanceAgent(data_manager)
    reporting_agent = ReportingAgent(data_manager)
    
    return {
        "performance_agent": performance_agent,
        "reporting_agent": reporting_agent,
        "notification_agent": notification_agent,
        "export_agent": ExportAgent(data_manager),
        "goal_agent": GoalAgent(data_manager, notification_agent),
        "feedback_agent": FeedbackAgent(data_manager, notification_agent),
        "promotion_agent": PromotionAgent(data_manager)
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
            
            # Simple password field
            password = st.text_input(
                "Password", 
                type="password",
                placeholder="Enter your password",
                key="password_input"
            )
            
            submit = st.form_submit_button("Login")
            
            if submit:
                if email and password:
                    if USE_API_BACKEND:
                        # Use API
                        try:
                            result = st.session_state.api_client.login(email, password)
                            if result.get("success"):
                                st.session_state.authenticated = True
                                st.session_state.user = result.get("user")
                                st.success("Login successful!")
                                st.rerun()
                            else:
                                st.error("Invalid credentials")
                        except Exception as e:
                            st.error(f"Login failed: {str(e)}")
                    else:
                        # Use direct auth
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
    """Main dashboard with enhanced styling - Role-based dashboard"""
    user_role = st.session_state.user.get("role", "employee")
    user_id = st.session_state.user.get("id")
    user_email = st.session_state.user.get("email")
    
    # Role-based title
    if user_role in ["owner", "manager"]:
        title = "Team Performance Dashboard"
        description = "Monitor and track your team's performance metrics, KPIs, and analytics"
    else:
        title = "My Performance Dashboard"
        description = "Track your personal performance, tasks, and goals"
    
    st.markdown(f"""
        <style>
        .performance-overview {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.5rem;
        }}
        .performance-description {{
            color: #CCCCCC;
            opacity: 0.9;
            margin-bottom: 2rem;
        }}
        </style>
        <div class="performance-overview">{title}</div>
        <div class="performance-description">{description}</div>
    """, unsafe_allow_html=True)
    
    agents = initialize_agents()
    performance_agent = agents["performance_agent"]
    goal_agent = agents["goal_agent"]
    
    # Get data
    employees = st.session_state.data_manager.load_data("employees") or []
    tasks = st.session_state.data_manager.load_data("tasks") or []
    goals = goal_agent.get_all_goals()
    performance_data = st.session_state.data_manager.load_data("performances") or []
    
    # For employees: show only their data
    if user_role == "employee":
        # Get current employee
        current_employee = next((e for e in employees if e.get("id") == user_id or e.get("email") == user_email), None)
        if not current_employee:
            st.error("Employee data not found. Please contact administrator.")
            return
        
        # Get employee's performance
        eval_data = performance_agent.evaluate_employee(current_employee.get("id"), save=False)
        
        # Personal KPI Cards
        st.markdown("### 📊 My Performance")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            perf_score = eval_data.get('performance_score', 0) if eval_data else 0
            st.markdown(f"""
                <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">Performance Score</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{perf_score:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi_col2:
            completion_rate = eval_data.get('completion_rate', 0) if eval_data else 0
            st.markdown(f"""
                <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">Completion Rate</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{completion_rate:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi_col3:
            on_time_rate = eval_data.get('on_time_rate', 0) if eval_data else 0
            st.markdown(f"""
                <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">On-Time Rate</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{on_time_rate:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi_col4:
            my_tasks = [t for t in tasks if t.get("assigned_to") == current_employee.get("id")]
            active_tasks = len([t for t in my_tasks if t.get("status") in ["pending", "in_progress"]])
            st.markdown(f"""
                <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">Active Tasks</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{active_tasks}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # My Tasks Summary
        st.markdown("### ✅ My Tasks")
        my_tasks = [t for t in tasks if t.get("assigned_to") == current_employee.get("id")]
        if my_tasks:
            completed = len([t for t in my_tasks if t.get("status") == "completed"])
            pending = len([t for t in my_tasks if t.get("status") == "pending"])
            in_progress = len([t for t in my_tasks if t.get("status") == "in_progress"])
            
            task_col1, task_col2, task_col3 = st.columns(3)
            with task_col1:
                st.metric("Completed", completed)
            with task_col2:
                st.metric("In Progress", in_progress)
            with task_col3:
                st.metric("Pending", pending)
        else:
            st.info("No tasks assigned yet.")
        
        # My Goals Summary
        st.markdown("### 🎯 My Goals")
        # Try multiple matching strategies for goals
        employee_id_str = str(current_employee.get("id", ""))
        my_goals = [g for g in goals if 
                   str(g.get("employee_id", "")) == employee_id_str or 
                   str(g.get("user_id", "")) == employee_id_str]
        
        if my_goals:
            completed_goals = len([g for g in my_goals if g.get("status") in ["completed", "achieved"]])
            in_progress_goals = len([g for g in my_goals if g.get("status") in ["in_progress", "active"]])
            active_goals = len([g for g in my_goals if g.get("status") in ["active", "in_progress"]])
            
            goal_col1, goal_col2, goal_col3 = st.columns(3)
            with goal_col1:
                st.metric("Total Goals", len(my_goals))
            with goal_col2:
                st.metric("Completed", completed_goals)
            with goal_col3:
                st.metric("In Progress", in_progress_goals)
            
            # Show recent goals (top 3)
            st.markdown("#### Recent Goals")
            for goal in my_goals[:3]:
                progress = goal.get('progress_percentage', 0) if 'progress_percentage' in goal else (
                    (goal.get('current_value', 0) / goal.get('target_value', 1) * 100) if goal.get('target_value', 0) > 0 else 0
                )
                status_emoji = {"completed": "✅", "achieved": "✅", "in_progress": "🔄", "active": "🎯", "overdue": "⚠️"}.get(goal.get('status', 'active'), "🎯")
                st.write(f"{status_emoji} **{goal.get('title', 'Untitled')}** - {progress:.1f}% complete ({goal.get('status', 'active').title()})")
        else:
            st.info("No goals set yet.")
            st.markdown("💡 **Tip:** Go to the **Goals** page to create your first goal!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recent Feedback Summary
        st.markdown("### 💬 Recent Feedback")
        feedback = st.session_state.data_manager.load_data("feedback") or []
        my_feedback = [f for f in feedback if str(f.get("employee_id", "")) == employee_id_str]
        if my_feedback:
            avg_rating = sum([f.get('rating', 0) for f in my_feedback if f.get('rating')]) / len([f for f in my_feedback if f.get('rating')]) if [f for f in my_feedback if f.get('rating')] else 0
            positive_count = len([f for f in my_feedback if f.get('type') == 'positive' or (f.get('rating', 0) > 3)])
            
            feedback_col1, feedback_col2 = st.columns(2)
            with feedback_col1:
                st.metric("Total Feedback", len(my_feedback))
            with feedback_col2:
                if avg_rating > 0:
                    st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
                else:
                    st.metric("Positive Feedback", positive_count)
            
            # Show most recent feedback
            if my_feedback:
                latest_feedback = sorted(my_feedback, key=lambda x: x.get('created_at', ''), reverse=True)[0]
                feedback_type = latest_feedback.get('type', 'general')
                feedback_emoji = {"positive": "👍", "constructive": "💡", "general": "💬"}.get(feedback_type, "💬")
                st.write(f"{feedback_emoji} **Latest:** {latest_feedback.get('content', latest_feedback.get('feedback_text', 'No content'))[:100]}...")
        else:
            st.info("No feedback received yet.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Performance Trend (if available)
        if performance_data:
            my_perf_history = [p for p in performance_data if str(p.get("employee_id", "")) == employee_id_str]
            if len(my_perf_history) >= 2:
                st.markdown("### 📈 Performance Trend")
                recent_scores = [p.get('performance_score', 0) for p in sorted(my_perf_history, key=lambda x: x.get('evaluated_at', ''), reverse=True)[:5]]
                if len(recent_scores) >= 2:
                    trend = "📈 Improving" if recent_scores[0] > recent_scores[-1] else "📉 Declining" if recent_scores[0] < recent_scores[-1] else "➡️ Stable"
                    st.info(f"{trend} - Current: {recent_scores[0]:.1f}% | Previous: {recent_scores[-1]:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Performance Report Section (merged from Reports page)
        st.markdown("---")
        st.markdown("### 📊 Performance Report")
        st.markdown("Generate a detailed performance report with AI feedback and download as PDF")
        
        # Import professional report generator
        from components.agents.professional_report_generator import ProfessionalReportGenerator
        report_generator = ProfessionalReportGenerator(st.session_state.data_manager)
        
        report_col1, report_col2 = st.columns(2)
        
        with report_col1:
            if st.button("📊 Preview Detailed Report", use_container_width=True, type="primary"):
                st.session_state.show_report_preview = True
                st.rerun()
        
        with report_col2:
            if st.button("📥 Generate PDF Report", use_container_width=True):
                result = report_generator.generate_performance_report_pdf(current_employee.get("id"))
                if result.get("success"):
                    st.success("✅ Professional PDF report generated!")
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=result.get("content"),
                        file_name=result.get("filename"),
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        # Show detailed report preview if requested
        if st.session_state.get("show_report_preview", False):
            st.markdown("---")
            st.markdown("### 📊 Detailed Performance Report Preview")
            
            # Debug information section
            with st.expander("🔍 Debug Information - Performance Calculation Method", expanded=False):
                st.markdown("### AI/ML Status Check")
                
                # Check ML model
                ml_trained = performance_agent.ml_scorer.is_trained
                ml_status = "✅ Trained" if ml_trained else "❌ Not Trained"
                st.write(f"**ML Model Status:** {ml_status}")
                
                if ml_trained:
                    st.write(f"**ML Model Type:** {performance_agent.ml_scorer.model_type}")
                    try:
                        import os
                        model_path = "models/performance_scorer.pkl"
                        if os.path.exists(model_path):
                            st.write(f"**Model File:** ✅ Found at `{model_path}`")
                        else:
                            st.write(f"**Model File:** ❌ Not found at `{model_path}`")
                    except:
                        pass
                
                # Check AI client
                ai_enabled = performance_agent.ai_client.enabled
                ai_status = "✅ Enabled" if ai_enabled else "❌ Disabled"
                st.write(f"**AI Client Status:** {ai_status}")
                
                if ai_enabled:
                    provider = getattr(performance_agent.ai_client, 'provider', 'N/A')
                    model = getattr(performance_agent.ai_client, 'model', 'N/A')
                    st.write(f"**AI Provider:** {provider}")
                    st.write(f"**AI Model:** {model}")
                else:
                    st.info("💡 To enable AI: Set `USE_AI=true` in `.env` file and configure API key")
                
                # Determine which method will be used
                st.markdown("---")
                st.markdown("### Calculation Method")
                if ml_trained:
                    method = "**ML Model** (Random Forest/XGBoost)"
                    st.success(f"Will use: {method}")
                elif ai_enabled:
                    method = "**AI Fallback** (AI API)"
                    st.warning(f"Will use: {method}")
                else:
                    method = "**Simple Fallback** (Weighted Formula)"
                    st.info(f"Will use: {method}")
                
                st.markdown("---")
                st.markdown("### Environment Variables")
                import os
                use_ai = os.getenv("USE_AI", "false")
                has_openai_key = "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Not Set"
                has_anthropic_key = "✅ Set" if os.getenv("ANTHROPIC_API_KEY") else "❌ Not Set"
                has_gemini_key = "✅ Set" if os.getenv("GEMINI_API_KEY") else "❌ Not Set"
                
                st.write(f"**USE_AI:** `{use_ai}`")
                st.write(f"**OPENAI_API_KEY:** {has_openai_key}")
                st.write(f"**ANTHROPIC_API_KEY:** {has_anthropic_key}")
                st.write(f"**GEMINI_API_KEY:** {has_gemini_key}")
            
            # Get detailed evaluation data
            detailed_eval_data = performance_agent.evaluate_employee(current_employee.get("id"), save=False)
            
            # Get additional data
            all_tasks = st.session_state.data_manager.load_data("tasks") or []
            all_goals = goal_agent.get_all_goals()
            all_feedback = st.session_state.data_manager.load_data("feedback") or []
            
            detailed_employee_tasks = [t for t in all_tasks if str(t.get("assigned_to", "")) == str(current_employee.get("id"))]
            detailed_employee_goals = [g for g in all_goals if str(g.get("employee_id", "")) == employee_id_str or str(g.get("user_id", "")) == employee_id_str]
            detailed_employee_feedback = [f for f in all_feedback if str(f.get("employee_id", "")) == employee_id_str]
            
            if detailed_eval_data:
                # Employee Info
                st.markdown(f"**Employee:** {current_employee.get('name', 'N/A')} ({current_employee.get('email', 'N/A')})")
                st.markdown(f"**Position:** {current_employee.get('position', 'N/A')}")
                st.markdown("---")
                
                # Key Metrics
                st.markdown("#### Key Performance Metrics")
                col_preview1, col_preview2, col_preview3, col_preview4 = st.columns(4)
                with col_preview1:
                    st.metric("Performance Score", f"{detailed_eval_data.get('performance_score', 0):.1f}%")
                with col_preview2:
                    st.metric("Completion Rate", f"{detailed_eval_data.get('completion_rate', 0):.1f}%")
                with col_preview3:
                    st.metric("On-Time Rate", f"{detailed_eval_data.get('on_time_rate', 0):.1f}%")
                with col_preview4:
                    st.metric("Rank", detailed_eval_data.get('rank', 'N/A'))
                
                st.markdown("---")
                
                # Tasks Summary
                if detailed_employee_tasks:
                    st.markdown("#### Tasks Summary")
                    completed_tasks = len([t for t in detailed_employee_tasks if t.get("status") == "completed"])
                    in_progress_tasks = len([t for t in detailed_employee_tasks if t.get("status") == "in_progress"])
                    pending_tasks = len([t for t in detailed_employee_tasks if t.get("status") == "pending"])
                    
                    task_col1, task_col2, task_col3, task_col4 = st.columns(4)
                    with task_col1:
                        st.metric("Total Tasks", len(detailed_employee_tasks))
                    with task_col2:
                        st.metric("Completed", completed_tasks)
                    with task_col3:
                        st.metric("In Progress", in_progress_tasks)
                    with task_col4:
                        st.metric("Pending", pending_tasks)
                    st.markdown("---")
                
                # Goals Summary
                if detailed_employee_goals:
                    st.markdown("#### Goals Summary")
                    achieved_goals = len([g for g in detailed_employee_goals if g.get("status") == "achieved"])
                    active_goals = len([g for g in detailed_employee_goals if g.get("status") in ["active", "in_progress"]])
                    
                    goal_col1, goal_col2, goal_col3 = st.columns(3)
                    with goal_col1:
                        st.metric("Total Goals", len(detailed_employee_goals))
                    with goal_col2:
                        st.metric("Achieved", achieved_goals)
                    with goal_col3:
                        st.metric("Active", active_goals)
                    st.markdown("---")
                
                # Feedback Summary
                if detailed_employee_feedback:
                    st.markdown("#### Feedback Summary")
                    avg_rating = sum([f.get('rating', 0) for f in detailed_employee_feedback if f.get('rating')]) / len([f for f in detailed_employee_feedback if f.get('rating')]) if [f for f in detailed_employee_feedback if f.get('rating')] else 0
                    feedback_col1, feedback_col2 = st.columns(2)
                    with feedback_col1:
                        st.metric("Total Feedback", len(detailed_employee_feedback))
                    with feedback_col2:
                        st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
                    st.markdown("---")
                
                # Performance Trend
                st.markdown("#### Performance Trend")
                trend = detailed_eval_data.get('trend', 'N/A')
                trend_emoji = "📈" if trend == "improving" else "📉" if trend == "declining" else "➡️"
                st.info(f"{trend_emoji} **Trend:** {trend.title()}")
                
                st.markdown("---")
                
                # AI-Generated Feedback
                ai_feedback = detailed_eval_data.get('ai_feedback')
                if ai_feedback:
                    st.markdown("#### 💬 AI Performance Feedback")
                    st.markdown(f"""
                    <div style="background-color: #1e1e1e; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF6B35; margin: 1rem 0;">
                        <p style="color: #e0e0e0; line-height: 1.6; margin: 0;">{ai_feedback}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("#### 💬 Performance Feedback")
                    st.info("Feedback generation is not available. Enable AI in your .env file to receive personalized performance feedback.")
            
            # Close preview button
            if st.button("❌ Close Preview"):
                st.session_state.show_report_preview = False
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            if st.button("🎯 Manage Goals", use_container_width=True):
                st.session_state.current_page = "Goals"
                st.rerun()
        with action_col2:
            if st.button("📋 View Projects", use_container_width=True):
                st.session_state.current_page = "Projects"
                st.rerun()
        with action_col3:
            if st.button("💬 View Feedback", use_container_width=True):
                st.session_state.current_page = "Feedback"
                st.rerun()
        
        return
    
    # For managers/owners: show team data
    # Overview metrics
    overview = agents["reporting_agent"].generate_overview_report()
    
    # Calculate team KPIs
    team_employees = employees
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
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">Average Team Performance</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{avg_team_performance:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">Average Completion Rate</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{avg_completion_rate:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">Average On-Time Rate</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{avg_on_time_rate:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">Team Size</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{len(team_employees)}</div>
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
                title_font_color='#FF6B35',
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                height=400
            )
            st.plotly_chart(fig_bar)
        
        with chart_col2:
            # Radar/Spider Chart for Top 3 Employees
            top_3 = employee_rankings[:3]
            if len(top_3) > 0:
                categories = ['Performance', 'Completion', 'On-Time']
                
                fig_radar = go.Figure()
                
                colors = ['#FF6B35', '#FF8C42', '#FF6B35']
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
                            tickfont=dict(color='#CCCCCC')
                        ),
                        angularaxis=dict(
                            gridcolor='rgba(255,255,255,0.2)',
                            tickfont=dict(color='#CCCCCC')
                        ),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#FFFFFF',
                    title='Top 3 Employees - Multi-Metric Comparison',
                    title_font_color='#FF6B35',
                    height=400,
                    legend=dict(font=dict(color='#FFFFFF'))
                )
                st.plotly_chart(fig_radar)
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
            marker_color='#FF6B35',
            text=metrics_df['Completion Rate'].round(1),
            textposition='outside'
        ))
        
        fig_grouped.add_trace(go.Bar(
            name='On-Time Rate',
            x=metrics_df['Employee'],
            y=metrics_df['On-Time Rate'],
            marker_color='#FF8C42',
            text=metrics_df['On-Time Rate'].round(1),
            textposition='outside'
        ))
        
        fig_grouped.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF',
            title='Completion Rate vs On-Time Rate',
            title_font_color='#FF6B35',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
            legend=dict(font=dict(color='#FFFFFF')),
            height=400
        )
        st.plotly_chart(fig_grouped)
        
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
                color = "#3DDF85" if score >= 80 else "#FF6B35" if score >= 60 else "#FF6B35"
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
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem; opacity: 0.9;">Overall Team Score</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{avg_performance:.0f}%</div>
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
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem; opacity: 0.9;">Top Performer</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #FF6B35;">{top_name}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem; opacity: 0.9;">Average Goal Completion</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{task_completion:.0f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate feedback score (mock for now)
        feedback_score = 4.5
        st.markdown(f"""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem; opacity: 0.9;">Feedback Score</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FF6B35;">{feedback_score}/5</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts section with card styling
    st.markdown("""
        <style>
        .chart-card {
            background-color: #1A1A1A;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.1);
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
                    color_discrete_sequence=['#FF6B35']
                )
                fig.update_layout(
                    plot_bgcolor='#1A1A1A',
                    paper_bgcolor='#1A1A1A',
                    font_color='#FFFFFF',
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=8, color='#FF6B35'))
                st.plotly_chart(fig)
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
            color_discrete_sequence=['#FF6B35']
        )
        fig.update_layout(
            plot_bgcolor='#1A1A1A',
            paper_bgcolor='#1A1A1A',
            font_color='#FFFFFF',
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.04)', linecolor='rgba(255, 255, 255, 0.08)')
        )
        fig.update_traces(marker_color='#FF6B35')
        st.plotly_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Reports section
    st.markdown("#### Recent Reports")
    reports_col1, reports_col2, reports_col3 = st.columns(3)
    with reports_col1:
        st.markdown("""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="color: #FF6B35; font-weight: 600; margin-bottom: 0.5rem;">Performance Report</div>
                <div style="color: #CCCCCC; opacity: 0.7; font-size: 0.9rem;">Last updated: Today</div>
            </div>
        """, unsafe_allow_html=True)
    with reports_col2:
        st.markdown("""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="color: #FF6B35; font-weight: 600; margin-bottom: 0.5rem;">Team Analysis</div>
                <div style="color: #CCCCCC; opacity: 0.7; font-size: 0.9rem;">Last updated: Yesterday</div>
            </div>
        """, unsafe_allow_html=True)
    with reports_col3:
        st.markdown("""
            <div style="background-color: #1A1A1A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0px 4px 20px rgba(255, 107, 53, 0.05);">
                <div style="color: #FF6B35; font-weight: 600; margin-bottom: 0.5rem;">Monthly Summary</div>
                <div style="color: #CCCCCC; opacity: 0.7; font-size: 0.9rem;">Last updated: This week</div>
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
    
    # Performance Report Section for Managers/Owners (merged from Reports page)
    st.markdown("---")
    st.markdown("### 📊 Generate Employee Performance Reports")
    st.markdown("Generate detailed performance reports for any team member with AI feedback and download as PDF")
    
    # Import professional report generator
    from components.agents.professional_report_generator import ProfessionalReportGenerator
    report_generator = ProfessionalReportGenerator(st.session_state.data_manager)
    
    # Employee selection for managers/owners
    if employees:
        selected_employee_id = st.selectbox(
            "Select Employee",
            options=[e.get("id") for e in employees],
            format_func=lambda x: next((e.get("name", "Unknown") for e in employees if e.get("id") == x), "Unknown"),
            key="manager_report_employee_select"
        )
        
        selected_employee = next((e for e in employees if e.get("id") == selected_employee_id), None)
        
        if selected_employee:
            report_col1, report_col2 = st.columns(2)
            
            with report_col1:
                if st.button("📊 Preview Detailed Report", use_container_width=True, type="primary", key="manager_preview_report"):
                    st.session_state.show_manager_report_preview = True
                    st.session_state.selected_report_employee_id = selected_employee_id
                    st.rerun()
            
            with report_col2:
                if st.button("📥 Generate PDF Report", use_container_width=True, key="manager_generate_pdf"):
                    result = report_generator.generate_performance_report_pdf(selected_employee_id)
                    if result.get("success"):
                        st.success("✅ Professional PDF report generated!")
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=result.get("content"),
                            file_name=result.get("filename"),
                            mime="application/pdf",
                            use_container_width=True,
                            key="manager_download_pdf"
                        )
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            # Show detailed report preview if requested
            if st.session_state.get("show_manager_report_preview", False) and st.session_state.get("selected_report_employee_id") == selected_employee_id:
                st.markdown("---")
                st.markdown(f"### 📊 Detailed Performance Report Preview: {selected_employee.get('name', 'Employee')}")
                
                # Get detailed evaluation data
                detailed_eval_data = performance_agent.evaluate_employee(selected_employee_id, save=False)
                
                # Get additional data
                all_tasks = st.session_state.data_manager.load_data("tasks") or []
                all_goals = goal_agent.get_all_goals()
                all_feedback = st.session_state.data_manager.load_data("feedback") or []
                
                detailed_employee_tasks = [t for t in all_tasks if str(t.get("assigned_to", "")) == str(selected_employee_id)]
                detailed_employee_goals = [g for g in all_goals if str(g.get("employee_id", "")) == str(selected_employee_id) or str(g.get("user_id", "")) == str(selected_employee_id)]
                detailed_employee_feedback = [f for f in all_feedback if str(f.get("employee_id", "")) == str(selected_employee_id)]
                
                if detailed_eval_data:
                    # Employee Info
                    st.markdown(f"**Employee:** {selected_employee.get('name', 'N/A')} ({selected_employee.get('email', 'N/A')})")
                    st.markdown(f"**Position:** {selected_employee.get('position', 'N/A')}")
                    st.markdown("---")
                    
                    # Key Metrics
                    st.markdown("#### Key Performance Metrics")
                    col_preview1, col_preview2, col_preview3, col_preview4 = st.columns(4)
                    with col_preview1:
                        st.metric("Performance Score", f"{detailed_eval_data.get('performance_score', 0):.1f}%")
                    with col_preview2:
                        st.metric("Completion Rate", f"{detailed_eval_data.get('completion_rate', 0):.1f}%")
                    with col_preview3:
                        st.metric("On-Time Rate", f"{detailed_eval_data.get('on_time_rate', 0):.1f}%")
                    with col_preview4:
                        st.metric("Rank", detailed_eval_data.get('rank', 'N/A'))
                    
                    st.markdown("---")
                    
                    # Tasks Summary
                    if detailed_employee_tasks:
                        st.markdown("#### Tasks Summary")
                        completed_tasks = len([t for t in detailed_employee_tasks if t.get("status") == "completed"])
                        in_progress_tasks = len([t for t in detailed_employee_tasks if t.get("status") == "in_progress"])
                        pending_tasks = len([t for t in detailed_employee_tasks if t.get("status") == "pending"])
                        
                        task_col1, task_col2, task_col3, task_col4 = st.columns(4)
                        with task_col1:
                            st.metric("Total Tasks", len(detailed_employee_tasks))
                        with task_col2:
                            st.metric("Completed", completed_tasks)
                        with task_col3:
                            st.metric("In Progress", in_progress_tasks)
                        with task_col4:
                            st.metric("Pending", pending_tasks)
                        st.markdown("---")
                    
                    # Goals Summary
                    if detailed_employee_goals:
                        st.markdown("#### Goals Summary")
                        achieved_goals = len([g for g in detailed_employee_goals if g.get("status") == "achieved"])
                        active_goals = len([g for g in detailed_employee_goals if g.get("status") in ["active", "in_progress"]])
                        
                        goal_col1, goal_col2, goal_col3 = st.columns(3)
                        with goal_col1:
                            st.metric("Total Goals", len(detailed_employee_goals))
                        with goal_col2:
                            st.metric("Achieved", achieved_goals)
                        with goal_col3:
                            st.metric("Active", active_goals)
                        st.markdown("---")
                    
                    # Feedback Summary
                    if detailed_employee_feedback:
                        st.markdown("#### Feedback Summary")
                        avg_rating = sum([f.get('rating', 0) for f in detailed_employee_feedback if f.get('rating')]) / len([f for f in detailed_employee_feedback if f.get('rating')]) if [f for f in detailed_employee_feedback if f.get('rating')] else 0
                        feedback_col1, feedback_col2 = st.columns(2)
                        with feedback_col1:
                            st.metric("Total Feedback", len(detailed_employee_feedback))
                        with feedback_col2:
                            st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
                        st.markdown("---")
                    
                    # Performance Trend
                    st.markdown("#### Performance Trend")
                    trend = detailed_eval_data.get('trend', 'N/A')
                    trend_emoji = "📈" if trend == "improving" else "📉" if trend == "declining" else "➡️"
                    st.info(f"{trend_emoji} **Trend:** {trend.title()}")
                    
                    st.markdown("---")
                    
                    # AI-Generated Feedback
                    ai_feedback = detailed_eval_data.get('ai_feedback')
                    if ai_feedback:
                        st.markdown("#### 💬 AI Performance Feedback")
                        st.markdown(f"""
                        <div style="background-color: #1e1e1e; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF6B35; margin: 1rem 0;">
                            <p style="color: #e0e0e0; line-height: 1.6; margin: 0;">{ai_feedback}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("#### 💬 Performance Feedback")
                        st.info("Feedback generation is not available. Enable AI in your .env file to receive personalized performance feedback.")
                
                # Close preview button
                if st.button("❌ Close Preview", key="manager_close_preview"):
                    st.session_state.show_manager_report_preview = False
                    st.session_state.selected_report_employee_id = None
                    st.rerun()
    else:
        st.warning("⚠️ No employees available to generate reports.")
        st.info("💡 Add employees through the **👥 Employees** page to generate performance reports.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions for Managers
    st.markdown("### ⚡ Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        if st.button("🎯 Manage Goals", use_container_width=True):
            st.session_state.current_page = "Goals"
            st.rerun()
    with action_col2:
        if st.button("📋 View Projects", use_container_width=True):
            st.session_state.current_page = "Projects"
            st.rerun()
    with action_col3:
        if st.button("💬 View Feedback", use_container_width=True):
            st.session_state.current_page = "Feedback"
            st.rerun()

# Projects page
def projects_page():
    """Projects management page - Modern redesign"""
    # Header with gradient
    st.markdown("""
        <style>
        .projects-header {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            color: white;
        }
        .project-card {
            background: #1A1A1A;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        .project-card:hover {
            border-color: #FF6B35;
            box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
        }
        .task-card {
            background: rgba(255, 107, 53, 0.05);
            border-left: 4px solid #FF6B35;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .status-active { background: #10b981; color: white; }
        .status-in_progress { background: #FF6B35; color: white; }
        .status-completed { background: #6b7280; color: white; }
        .status-on_hold { background: #f59e0b; color: white; }
        .priority-high { color: #ef4444; }
        .priority-medium { color: #f59e0b; }
        .priority-low { color: #10b981; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="projects-header">
            <h1 style="margin: 0; font-size: 2.5rem;">📁 Projects & Tasks</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Manage your projects and track task progress</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Role-based access control
    user_role = st.session_state.user.get("role", "employee")
    user_email = st.session_state.user.get("email")
    
    if USE_API_BACKEND:
        data_manager = None
        api_client = st.session_state.api_client
        try:
            projects_data = api_client.get_projects(
                user_id=st.session_state.user.get("id"),
                user_role=user_role
            )
            projects = projects_data if isinstance(projects_data, list) else projects_data.get("projects", [])
            all_tasks = []
            for project in projects:
                all_tasks.extend(project.get("tasks", []))
        except:
            projects = []
            all_tasks = []
    else:
        data_manager = st.session_state.data_manager
        projects = data_manager.load_data("projects") or []
        all_tasks = data_manager.load_data("tasks") or []
    
    # Role-based tabs
    if user_role in ["owner", "manager"]:
        tab1, tab2, tab3 = st.tabs(["📊 Projects", "➕ Create Project", "📈 Reports"])
    else:
        tab1, tab3 = st.tabs(["📊 My Projects", "📈 Reports"])
        tab2 = None
    
    with tab1:
        # Get employee ID for filtering
        if not USE_API_BACKEND:
            employees = data_manager.load_data("employees") or []
            current_employee = None
            if user_email:
                current_employee = next((e for e in employees if e.get("email") == user_email), None)
            employee_id = current_employee.get("id") if current_employee else None
            
            # Filter projects for employees
            if user_role == "employee" and employee_id:
                employee_project_ids = set()
                for task in all_tasks:
                    if str(task.get("assigned_to", "")) == str(employee_id):
                        project_id = task.get("project_id")
                        if project_id:
                            employee_project_ids.add(str(project_id))
                projects = [p for p in projects if str(p.get("id", "")) in employee_project_ids]
        else:
            employee_id = st.session_state.user.get("id")
        
        if not projects:
            st.markdown("""
                <div style="text-align: center; padding: 3rem; background: #1A1A1A; border-radius: 16px; border: 2px dashed rgba(255,255,255,0.1);">
                    <h2 style="color: #CCCCCC;">📭 No Projects Found</h2>
                    <p style="color: #64748B;">Get started by creating your first project!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Projects overview stats
            total_tasks = sum(len([t for t in all_tasks if str(t.get("project_id", "")) == str(p.get("id", ""))]) for p in projects)
            completed_tasks = sum(len([t for t in all_tasks if str(t.get("project_id", "")) == str(p.get("id", "")) and t.get("status") == "completed"]) for p in projects)
            active_projects = len([p for p in projects if p.get("status") in ["active", "in_progress"]])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Projects", len(projects))
            with col2:
                st.metric("Active Projects", active_projects)
            with col3:
                st.metric("Total Tasks", total_tasks)
            with col4:
                st.metric("Completed Tasks", completed_tasks)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Modern project cards
            for project in projects:
                project_id = str(project.get("id", ""))
                project_name = project.get("name", "Unnamed Project")
                project_status = project.get("status", "unknown")
                project_description = project.get("description", "")
                
                # Get tasks for this project
                project_tasks = [t for t in all_tasks if str(t.get("project_id", "")) == project_id]
                
                # Calculate project progress
                total_project_tasks = len(project_tasks)
                completed_project_tasks = len([t for t in project_tasks if t.get("status") == "completed"])
                progress = (completed_project_tasks / total_project_tasks * 100) if total_project_tasks > 0 else 0
                
                # Status colors
                status_colors = {
                    "active": "#10b981",
                    "in_progress": "#FF6B35",
                    "completed": "#6b7280",
                    "on_hold": "#f59e0b"
                }
                status_color = status_colors.get(project_status, "#64748B")
                
                # Project card
                st.markdown(f"""
                    <div class="project-card">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                            <div>
                                <h2 style="margin: 0; color: #FF6B35; font-size: 1.5rem;">📁 {project_name}</h2>
                                <span class="status-badge status-{project_status}" style="background: {status_color}; margin-top: 0.5rem;">
                                    {project_status.replace('_', ' ').title()}
                                </span>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.9rem; color: #CCCCCC;">Progress</div>
                                <div style="font-size: 1.5rem; font-weight: bold; color: #FF6B35;">{progress:.0f}%</div>
                            </div>
                        </div>
                        <p style="color: #CCCCCC; margin: 0.5rem 0;">{project_description or 'No description'}</p>
                """, unsafe_allow_html=True)
                
                # Project metadata
                col_meta1, col_meta2, col_meta3 = st.columns(3)
                with col_meta1:
                    if project.get("deadline"):
                        try:
                            deadline = datetime.fromisoformat(project["deadline"]) if isinstance(project["deadline"], str) else project["deadline"]
                            days_left = (deadline.date() - datetime.now().date()).days
                            st.caption(f"📅 Deadline: {deadline.strftime('%Y-%m-%d')}")
                            if days_left >= 0:
                                st.caption(f"⏰ {days_left} days remaining")
                            else:
                                st.caption(f"⚠️ {abs(days_left)} days overdue")
                        except:
                            st.caption(f"📅 Deadline: {project.get('deadline')}")
                
                with col_meta2:
                    st.caption(f"📋 {total_project_tasks} tasks")
                
                with col_meta3:
                    st.caption(f"✅ {completed_project_tasks} completed")
                
                # Progress bar
                st.progress(progress / 100)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Tasks section
                if project_tasks:
                    st.markdown("#### 📝 Tasks")
                    
                    # Kanban-style task view
                    task_col1, task_col2, task_col3 = st.columns(3)
                    
                    pending_tasks = [t for t in project_tasks if t.get("status") == "pending"]
                    in_progress_tasks = [t for t in project_tasks if t.get("status") == "in_progress"]
                    completed_tasks_list = [t for t in project_tasks if t.get("status") == "completed"]
                    
                    # Helper function to render task card
                    def render_task_card(task, column_name):
                        task_id = str(task.get("id", ""))
                        task_title = task.get("title", "Untitled Task")
                        task_priority = task.get("priority", "medium")
                        task_due_date = task.get("due_date", "")
                        task_description = task.get("description", "")
                        
                        priority_colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#10b981"}
                        priority_color = priority_colors.get(task_priority, "#64748B")
                        
                        with st.container():
                            st.markdown(f"""
                                <div class="task-card" style="margin-bottom: 1rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: start;">
                                        <h4 style="margin: 0; color: #FFFFFF;">{task_title}</h4>
                                        <span style="background: {priority_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">
                                            {task_priority.upper()}
                                        </span>
                                    </div>
                                    {f'<p style="color: #CCCCCC; font-size: 0.85rem; margin: 0.5rem 0;">{task_description[:100]}{"..." if len(task_description) > 100 else ""}</p>' if task_description else ''}
                                    {f'<div style="color: #64748B; font-size: 0.75rem; margin-top: 0.5rem;">📅 {task_due_date}</div>' if task_due_date else ''}
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Update button for employees
                            if user_role == "employee" and str(task.get("assigned_to", "")) == str(employee_id):
                                if st.button("✏️ Update", key=f"update_{task_id}_{column_name}"):
                                    st.session_state[f"updating_{task_id}"] = True
                                    st.rerun()
                            
                            # Update form
                            if st.session_state.get(f"updating_{task_id}", False):
                                with st.form(f"update_form_{task_id}"):
                                    new_status = st.selectbox("Status", ["pending", "in_progress", "completed"], 
                                                              index=["pending", "in_progress", "completed"].index(task.get("status", "pending")) 
                                                              if task.get("status") in ["pending", "in_progress", "completed"] else 0,
                                                              key=f"status_{task_id}")
                                    new_priority = st.selectbox("Priority", ["low", "medium", "high"],
                                                               index=["low", "medium", "high"].index(task_priority) 
                                                               if task_priority in ["low", "medium", "high"] else 1,
                                                               key=f"priority_{task_id}")
                                    
                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        if st.form_submit_button("💾 Save"):
                                            try:
                                                if not USE_API_BACKEND:
                                                    for t in all_tasks:
                                                        if str(t.get("id")) == task_id:
                                                            t["status"] = new_status
                                                            t["priority"] = new_priority
                                                            t["updated_at"] = datetime.now().isoformat()
                                                            data_manager.save_data("tasks", all_tasks)
                                                            
                                                            # Publish event
                                                            event_bus = st.session_state.get("event_bus")
                                                            if event_bus:
                                                                from components.managers.event_bus import EventType
                                                                event_bus.publish_event(EventType.TASK_UPDATED, {"task": t}, source="app.py")
                                                                if new_status == "completed":
                                                                    event_bus.publish_event(EventType.TASK_COMPLETED, {"task": t}, source="app.py")
                                                else:
                                                    st.session_state.api_client.update_task(task_id, {"status": new_status, "priority": new_priority})
                                                
                                                st.success("✅ Updated!")
                                                st.session_state[f"updating_{task_id}"] = False
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Error: {str(e)}")
                                    with col_cancel:
                                        if st.form_submit_button("❌ Cancel"):
                                            st.session_state[f"updating_{task_id}"] = False
                                            st.rerun()
                    
                    with task_col1:
                        st.markdown(f"<h3 style='color: #f59e0b;'>⏳ Pending ({len(pending_tasks)})</h3>", unsafe_allow_html=True)
                        if pending_tasks:
                            for task in pending_tasks:
                                render_task_card(task, "pending")
                        else:
                            st.info("No pending tasks")
                    
                    with task_col2:
                        st.markdown(f"<h3 style='color: #3b82f6;'>🔄 In Progress ({len(in_progress_tasks)})</h3>", unsafe_allow_html=True)
                        if in_progress_tasks:
                            for task in in_progress_tasks:
                                render_task_card(task, "in_progress")
                        else:
                            st.info("No tasks in progress")
                    
                    with task_col3:
                        st.markdown(f"<h3 style='color: #10b981;'>✅ Completed ({len(completed_tasks_list)})</h3>", unsafe_allow_html=True)
                        if completed_tasks_list:
                            for task in completed_tasks_list:
                                render_task_card(task, "completed")
                        else:
                            st.info("No completed tasks")
                else:
                    st.info("📝 No tasks assigned to this project yet.")
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    # Create Project tab (for managers/owners)
    if tab2:
        with tab2:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
                    <h2 style="color: white; margin: 0;">➕ Create New Project</h2>
                    <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">Start a new project and assign tasks to your team</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("create_project_form"):
                col1, col2 = st.columns(2)
                with col1:
                    project_name = st.text_input("Project Name *", placeholder="e.g., Website Redesign", help="Enter a descriptive project name")
                    project_status = st.selectbox("Initial Status", ["active", "in_progress", "on_hold"], 
                                                   help="Set the starting status for this project")
                with col2:
                    project_deadline = st.date_input("Deadline", value=datetime.now().date() + timedelta(days=30),
                                                     help="Set the project deadline")
                    if not USE_API_BACKEND:
                        employees_list = data_manager.load_data("employees") or []
                        project_manager = st.selectbox("Project Manager", 
                                                      [e.get("email") for e in employees_list if e.get("role") in ["owner", "manager"]],
                                                      help="Select the manager responsible for this project")
                
                project_description = st.text_area("Description", placeholder="Describe the project goals, scope, and key deliverables...", 
                                                   height=100, help="Provide a detailed description of the project")
                
                st.markdown("---")
                
                col_submit, col_clear = st.columns([1, 4])
                with col_submit:
                    submit = st.form_submit_button("🚀 Create Project", type="primary")
                
                if submit:
                    if project_name:
                        try:
                            if not USE_API_BACKEND:
                                new_project = {
                                    "id": str(len(projects) + 1),
                                    "name": project_name,
                                    "description": project_description,
                                    "status": project_status,
                                    "deadline": project_deadline.isoformat(),
                                    "manager": project_manager if not USE_API_BACKEND else None,
                                    "created_at": datetime.now().isoformat(),
                                    "updated_at": datetime.now().isoformat()
                                }
                                projects.append(new_project)
                                data_manager.save_data("projects", projects)
                            else:
                                # Use API to create project
                                st.info("API project creation not yet implemented")
                            
                            st.success("✅ Project created successfully!")
                            st.balloons()
                            st.session_state.show_projects_view = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error creating project: {str(e)}")
                    else:
                        st.error("⚠️ Please enter a project name.")
    
    # Project Reports tab
    with tab3:
        st.markdown("### 📊 Project Reports")
        st.info("Project reports feature coming soon.")

# Goals page
def goals_page():
    """Goals management page"""
    st.title("🎯 Goals")
    st.markdown("---")
    
    agents = initialize_agents()
    goal_agent = agents["goal_agent"]
    data_manager = st.session_state.data_manager
    user_role = st.session_state.user.get("role", "employee")
    user_id = st.session_state.user.get("id")
    user_email = st.session_state.user.get("email")
    
    employees = data_manager.load_data("employees") or []
    current_employee = next((e for e in employees if e.get("id") == user_id or e.get("email") == user_email), None)
    
    # Get goals
    all_goals = goal_agent.get_all_goals()
    
    if user_role == "employee":
        # Show only employee's goals
        my_goals = [g for g in all_goals if str(g.get("employee_id", "")) == str(current_employee.get("id") if current_employee else "") or str(g.get("user_id", "")) == str(current_employee.get("id") if current_employee else "")]
        
        st.markdown("### My Goals")
        if my_goals:
            for goal in my_goals:
                goal_id = str(goal.get("id", ""))
                goal_title = goal.get('title', 'Untitled')
                editing_key = f"editing_goal_{goal_id}"
                
                # Check if this goal is being edited
                if st.session_state.get(editing_key, False):
                    st.markdown("---")
                    st.markdown(f"### ✏️ Edit Goal: {goal_title}")
                    
                    with st.form(f"edit_goal_form_{goal_id}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            edit_title = st.text_input("Goal Title *", value=goal.get('title', ''), key=f"edit_title_{goal_id}")
                            edit_description = st.text_area("Description", value=goal.get('description', '') or '', key=f"edit_description_{goal_id}", height=100)
                            edit_target = st.number_input("Target Value", min_value=1, value=int(goal.get('target_value', 100)), key=f"edit_target_{goal_id}")
                        
                        with col2:
                            # Parse deadline if it exists
                            deadline_value = datetime.now().date() + timedelta(days=30)
                            if goal.get('deadline') or goal.get('target_date'):
                                try:
                                    deadline_str = goal.get('deadline') or goal.get('target_date')
                                    if isinstance(deadline_str, str):
                                        deadline_value = datetime.fromisoformat(deadline_str.split('T')[0]).date()
                                    else:
                                        deadline_value = deadline_str
                                except:
                                    pass
                            
                            edit_deadline = st.date_input("Deadline", value=deadline_value, key=f"edit_deadline_{goal_id}")
                            edit_current = st.number_input("Current Value", min_value=0.0, value=float(goal.get('current_value', 0)), key=f"edit_current_{goal_id}")
                            
                            # Status selection
                            status_options = ["active", "in_progress", "completed", "overdue", "at_risk", "on_hold"]
                            current_status = goal.get('status', 'active')
                            if current_status not in status_options:
                                current_status = "active"
                            edit_status = st.selectbox("Status", status_options, index=status_options.index(current_status) if current_status in status_options else 0, key=f"edit_status_{goal_id}")
                        
                        st.markdown("---")
                        
                        col_save, col_cancel = st.columns([1, 4])
                        with col_save:
                            save_btn = st.form_submit_button("💾 Save Changes", type="primary")
                        with col_cancel:
                            cancel_btn = st.form_submit_button("❌ Cancel")
                        
                        if save_btn:
                            if not edit_title:
                                st.error("⚠️ Please enter a goal title.")
                            else:
                                try:
                                    # Prepare update data
                                    update_data = {
                                        "title": edit_title,
                                        "description": edit_description if edit_description else None,
                                        "target_value": edit_target,
                                        "current_value": edit_current,
                                        "target_date": edit_deadline.isoformat() if edit_deadline else None,
                                        "status": edit_status
                                    }
                                    
                                    # Update goal using data manager
                                    data_manager.update_goal(goal_id, update_data)
                                    
                                    st.success(f"✅ Goal '{edit_title}' updated successfully!")
                                    st.session_state[editing_key] = False
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error updating goal: {str(e)}")
                                    st.exception(e)
                        
                        if cancel_btn:
                            st.session_state[editing_key] = False
                            st.rerun()
                
                # Normal view with edit button
                else:
                    with st.expander(f"🎯 {goal_title} - {goal.get('status', 'active').title()}"):
                        col_info, col_actions = st.columns([3, 1])
                        with col_info:
                            st.write(f"**Description:** {goal.get('description', 'No description')}")
                            progress = goal.get('progress_percentage', 0) if 'progress_percentage' in goal else (
                                (goal.get('current_value', 0) / goal.get('target_value', 1) * 100) if goal.get('target_value', 0) > 0 else 0
                            )
                            st.progress(progress / 100)
                            st.write(f"**Progress:** {progress:.1f}% ({goal.get('current_value', 0)} / {goal.get('target_value', 100)})")
                            if goal.get('deadline') or goal.get('target_date'):
                                deadline = goal.get('deadline') or goal.get('target_date')
                                st.write(f"**Deadline:** {deadline}")
                            st.write(f"**Status:** {goal.get('status', 'active').title()}")
                        with col_actions:
                            if st.button("✏️ Edit", key=f"edit_goal_btn_{goal_id}"):
                                st.session_state[editing_key] = True
                                st.rerun()
        else:
            st.info("No goals set yet.")
        
        # Create new goal
        st.markdown("---")
        st.markdown("### Create New Goal")
        with st.form("create_goal_form"):
            goal_title = st.text_input("Goal Title *")
            goal_description = st.text_area("Description")
            target_value = st.number_input("Target Value", min_value=1, value=100)
            deadline = st.date_input("Deadline", value=datetime.now().date() + timedelta(days=30))
            
            if st.form_submit_button("Create Goal"):
                if goal_title and current_employee:
                    goal_data = {
                        "employee_id": current_employee.get("id"),
                        "title": goal_title,
                        "description": goal_description,
                        "target_value": target_value,
                        "deadline": deadline.isoformat()
                    }
                    result = goal_agent.create_goal(goal_data)
                    if result.get("success"):
                        st.success("✅ Goal created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
    else:
        # Managers/owners can create goals for employees and view all goals
        st.markdown("### ➕ Create Goal for Employee")
        with st.form("create_goal_manager_form"):
            col1, col2 = st.columns(2)
            with col1:
                # Employee selection
                employee_options = {f"{e.get('name', 'Unknown')} ({e.get('email', 'N/A')})": e.get("id") for e in employees}
                if employee_options:
                    selected_employee = st.selectbox("Select Employee *", list(employee_options.keys()), 
                                                     help="Choose the employee for this goal")
                    selected_employee_id = employee_options[selected_employee]
                else:
                    st.warning("No employees found")
                    selected_employee_id = None
                
                goal_title = st.text_input("Goal Title *", placeholder="e.g., Complete training course", 
                                          help="Enter a clear, measurable goal title")
                target_value = st.number_input("Target Value", min_value=1, value=100, 
                                              help="The target number to achieve")
            
            with col2:
                goal_type = st.selectbox("Goal Type", ["quantitative", "qualitative", "skill_based"],
                                        help="Type of goal: quantitative (numbers), qualitative (quality), or skill-based")
                deadline = st.date_input("Deadline", value=datetime.now().date() + timedelta(days=30),
                                       help="When should this goal be completed?")
            
            goal_description = st.text_area("Description", placeholder="Describe what needs to be achieved, why it's important, and how success will be measured...",
                                          height=100, help="Detailed description of the goal")
            
            st.markdown("---")
            
            if st.form_submit_button("🎯 Create Goal", type="primary"):
                if goal_title and selected_employee_id:
                    goal_data = {
                        "employee_id": selected_employee_id,
                        "title": goal_title,
                        "description": goal_description,
                        "target_value": target_value,
                        "deadline": deadline.isoformat(),
                        "goal_type": goal_type
                    }
                    result = goal_agent.create_goal(goal_data)
                    if result.get("success"):
                        st.success("✅ Goal created successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                else:
                    st.error("⚠️ Please select an employee and enter a goal title.")
        
        st.markdown("---")
        st.markdown("### 📊 All Employee Goals")
        
        if all_goals:
            # Group goals by employee
            goals_by_employee = {}
            for goal in all_goals:
                emp_id = str(goal.get("employee_id", "")) or str(goal.get("user_id", ""))
                if emp_id not in goals_by_employee:
                    goals_by_employee[emp_id] = []
                goals_by_employee[emp_id].append(goal)
            
            for emp_id, emp_goals in goals_by_employee.items():
                emp = next((e for e in employees if str(e.get("id")) == emp_id), None)
                emp_name = emp.get("name", "Unknown") if emp else "Unknown"
                emp_email = emp.get("email", "N/A") if emp else "N/A"
                
                st.markdown(f"#### 👤 {emp_name} ({emp_email})")
                
                for goal in emp_goals:
                    goal_id = str(goal.get("id", ""))
                    goal_title = goal.get('title', 'Untitled')
                    editing_key = f"editing_goal_{goal_id}"
                    
                    # Check if this goal is being edited
                    if st.session_state.get(editing_key, False):
                        st.markdown("---")
                        st.markdown(f"### ✏️ Edit Goal: {goal_title}")
                        
                        with st.form(f"edit_goal_form_{goal_id}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_title = st.text_input("Goal Title *", value=goal.get('title', ''), key=f"edit_title_{goal_id}")
                                edit_description = st.text_area("Description", value=goal.get('description', '') or '', key=f"edit_description_{goal_id}", height=100)
                                edit_target = st.number_input("Target Value", min_value=1, value=int(goal.get('target_value', 100)), key=f"edit_target_{goal_id}")
                            
                            with col2:
                                # Parse deadline if it exists
                                deadline_value = datetime.now().date() + timedelta(days=30)
                                if goal.get('deadline') or goal.get('target_date'):
                                    try:
                                        deadline_str = goal.get('deadline') or goal.get('target_date')
                                        if isinstance(deadline_str, str):
                                            deadline_value = datetime.fromisoformat(deadline_str.split('T')[0]).date()
                                        else:
                                            deadline_value = deadline_str
                                    except:
                                        pass
                                
                                edit_deadline = st.date_input("Deadline", value=deadline_value, key=f"edit_deadline_{goal_id}")
                                edit_current = st.number_input("Current Value", min_value=0.0, value=float(goal.get('current_value', 0)), key=f"edit_current_{goal_id}")
                                
                                # Status selection
                                status_options = ["active", "in_progress", "completed", "overdue", "at_risk", "on_hold"]
                                current_status = goal.get('status', 'active')
                                if current_status not in status_options:
                                    current_status = "active"
                                edit_status = st.selectbox("Status", status_options, index=status_options.index(current_status) if current_status in status_options else 0, key=f"edit_status_{goal_id}")
                            
                            st.markdown("---")
                            
                            col_save, col_cancel = st.columns([1, 4])
                            with col_save:
                                save_btn = st.form_submit_button("💾 Save Changes", type="primary")
                            with col_cancel:
                                cancel_btn = st.form_submit_button("❌ Cancel")
                            
                            if save_btn:
                                if not edit_title:
                                    st.error("⚠️ Please enter a goal title.")
                                else:
                                    try:
                                        # Prepare update data
                                        update_data = {
                                            "title": edit_title,
                                            "description": edit_description if edit_description else None,
                                            "target_value": edit_target,
                                            "current_value": edit_current,
                                            "target_date": edit_deadline.isoformat() if edit_deadline else None,
                                            "status": edit_status
                                        }
                                        
                                        # Update goal using data manager
                                        data_manager.update_goal(goal_id, update_data)
                                        
                                        st.success(f"✅ Goal '{edit_title}' updated successfully!")
                                        st.session_state[editing_key] = False
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error updating goal: {str(e)}")
                                        st.exception(e)
                            
                            if cancel_btn:
                                st.session_state[editing_key] = False
                                st.rerun()
                    
                    # Normal view with edit button
                    else:
                        with st.expander(f"🎯 {goal_title} - {goal.get('status', 'active').title()}", expanded=False):
                            col_info1, col_info2, col_actions = st.columns([2, 2, 1])
                            with col_info1:
                                st.write(f"**Description:** {goal.get('description', 'No description')}")
                                st.write(f"**Type:** {goal.get('goal_type', 'quantitative').title()}")
                                st.write(f"**Status:** {goal.get('status', 'active').title()}")
                            with col_info2:
                                progress = goal.get('progress_percentage', 0) if 'progress_percentage' in goal else (
                                    (goal.get('current_value', 0) / goal.get('target_value', 1) * 100) if goal.get('target_value', 0) > 0 else 0
                                )
                                st.progress(progress / 100)
                                st.write(f"**Progress:** {progress:.1f}% ({goal.get('current_value', 0)} / {goal.get('target_value', 100)})")
                                if goal.get('deadline') or goal.get('target_date'):
                                    deadline_str = goal.get('deadline') or goal.get('target_date')
                                    st.write(f"**Deadline:** {deadline_str}")
                            with col_actions:
                                if st.button("✏️ Edit", key=f"edit_goal_btn_{goal_id}"):
                                    st.session_state[editing_key] = True
                                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("📭 No goals found. Create goals for your team members above.")

# Feedback page
def feedback_page():
    """Feedback management page"""
    st.title("💬 Feedback")
    st.markdown("---")
    
    agents = initialize_agents()
    feedback_agent = agents["feedback_agent"]
    data_manager = st.session_state.data_manager
    user_role = st.session_state.user.get("role", "employee")
    user_id = st.session_state.user.get("id")
    user_email = st.session_state.user.get("email")
    
    employees = data_manager.load_data("employees") or []
    current_employee = next((e for e in employees if e.get("id") == user_id or e.get("email") == user_email), None)
    
    if user_role == "employee":
        # Show feedback received
        st.markdown("### Feedback Received")
        
        # Try multiple ways to find employee ID for feedback matching
        employee_id_for_feedback = None
        if current_employee:
            employee_id_for_feedback = current_employee.get("id")
        elif user_id:
            employee_id_for_feedback = user_id
        
        # Also try to match by email if employee not found
        if not employee_id_for_feedback and user_email:
            # Try to find employee by email
            email_match = next((e for e in employees if e.get("email", "").lower() == user_email.lower()), None)
            if email_match:
                employee_id_for_feedback = email_match.get("id")
        
        # Get all feedbacks and try multiple matching strategies
        all_feedbacks = data_manager.load_data("feedback") or []
        my_feedbacks = []
        
        if employee_id_for_feedback:
            # Try exact match with employee_id
            my_feedbacks = [f for f in all_feedbacks if str(f.get("employee_id", "")) == str(employee_id_for_feedback)]
            
            # If no matches, try with user_id field
            if not my_feedbacks:
                my_feedbacks = [f for f in all_feedbacks if str(f.get("user_id", "")) == str(employee_id_for_feedback)]
        
        # Also try matching by email if still no matches
        if not my_feedbacks and user_email:
            # Check if feedback has email field or if we can match through employee lookup
            for feedback in all_feedbacks:
                feedback_emp_id = feedback.get("employee_id") or feedback.get("user_id")
                if feedback_emp_id:
                    feedback_emp = next((e for e in employees if str(e.get("id")) == str(feedback_emp_id)), None)
                    if feedback_emp and feedback_emp.get("email", "").lower() == user_email.lower():
                        my_feedbacks.append(feedback)
        
        # Use feedback_agent method as fallback
        if not my_feedbacks and employee_id_for_feedback:
            my_feedbacks = feedback_agent.get_feedbacks_for_employee(employee_id_for_feedback)
        
        # Debug information (can be removed later)
        if not my_feedbacks:
            # Show debug info to help identify the issue
            with st.expander("🔍 Debug Information (Click to see why feedback isn't showing)", expanded=False):
                st.write(f"**Current Employee ID:** {employee_id_for_feedback}")
                st.write(f"**User ID:** {user_id}")
                st.write(f"**User Email:** {user_email}")
                st.write(f"**Current Employee Found:** {current_employee is not None}")
                if current_employee:
                    st.write(f"**Employee Name:** {current_employee.get('name', 'N/A')}")
                    st.write(f"**Employee Email:** {current_employee.get('email', 'N/A')}")
                    st.write(f"**Employee ID from DB:** {current_employee.get('id', 'N/A')}")
                
                st.markdown("---")
                st.write(f"**Total Feedback in Database:** {len(all_feedbacks)}")
                if all_feedbacks:
                    st.write("**Sample Feedback IDs and Employee IDs:**")
                    for i, fb in enumerate(all_feedbacks[:5]):  # Show first 5
                        st.write(f"- Feedback {i+1}: ID={fb.get('id')}, employee_id={fb.get('employee_id')}, user_id={fb.get('user_id')}, reviewer_id={fb.get('reviewer_id')}")
        
        if my_feedbacks:
            for feedback in my_feedbacks:
                reviewer = next((e for e in employees if str(e.get("id")) == str(feedback.get("given_by", "")) or str(e.get("id")) == str(feedback.get("reviewer_id", ""))), None)
                reviewer_name = reviewer.get("name", "Unknown") if reviewer else (feedback.get("given_by", "Unknown") if feedback.get("is_anonymous") else "Unknown")
                
                with st.expander(f"💬 {feedback.get('title', 'Feedback')} from {reviewer_name} - {feedback.get('status', 'pending').title()}"):
                    st.write(f"**Type:** {feedback.get('type', feedback.get('feedback_type', 'general')).title()}")
                    if feedback.get('rating'):
                        st.write(f"**Rating:** {feedback.get('rating')}/5")
                    st.write(f"**Content:** {feedback.get('content', feedback.get('feedback_text', 'No content'))}")
                    
                    if feedback.get('status') == 'pending_response':
                        st.markdown("---")
                        with st.form(f"respond_feedback_{feedback.get('id')}"):
                            response = st.text_area("Your Response")
                            acknowledged = st.checkbox("I acknowledge this feedback")
                            action_plan = st.text_area("Action Plan (optional)")
                            
                            if st.form_submit_button("Submit Response"):
                                result = feedback_agent.respond_to_feedback(
                                    feedback.get("id"),
                                    {"response": response, "acknowledged": acknowledged, "action_plan": action_plan}
                                )
                                if result.get("success"):
                                    st.success("✅ Response submitted!")
                                    st.rerun()
        else:
            st.info("No feedback received yet.")
    else:
        # Managers can view all feedback and create new
        st.markdown("### All Feedback")
        all_feedbacks = feedback_agent.get_all_feedbacks()
        
        if all_feedbacks:
            for feedback in all_feedbacks:
                emp = next((e for e in employees if str(e.get("id")) == str(feedback.get("employee_id", ""))), None)
                emp_name = emp.get("name", "Unknown") if emp else "Unknown"
                
                with st.expander(f"💬 {feedback.get('title', 'Feedback')} for {emp_name}"):
                    st.write(f"**Employee:** {emp_name}")
                    st.write(f"**Status:** {feedback.get('status', 'pending').title()}")
                    st.write(f"**Content:** {feedback.get('content', feedback.get('feedback_text', 'No content'))}")
        else:
            st.info("No feedback found.")
        
        # Create feedback
        st.markdown("---")
        st.markdown("### Create Feedback")
        with st.form("create_feedback_form"):
            emp_options = {e.get("name", e.get("email", "Unknown")): e.get("id") for e in employees}
            selected_emp = st.selectbox("Employee *", list(emp_options.keys()))
            feedback_type = st.selectbox("Type", ["positive", "constructive", "general"])
            rating = st.slider("Rating", 1, 5, 3)
            content = st.text_area("Feedback Content *")
            
            if st.form_submit_button("Submit Feedback"):
                if content:
                    feedback_data = {
                        "employee_id": emp_options[selected_emp],
                        "given_by": current_employee.get("id") if current_employee else user_id,
                        "type": feedback_type,
                        "rating": rating,
                        "content": content
                    }
                    result = feedback_agent.create_feedback(feedback_data)
                    if result.get("success"):
                        st.success("✅ Feedback submitted!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")

# Reports page
def reports_page():
    """Employee Performance Reports page"""
    st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">📊 Employee Performance Report</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">Generate professional performance reports based on employee performance metrics</p>
        </div>
    """, unsafe_allow_html=True)
    
    data_manager = st.session_state.data_manager
    user_role = st.session_state.user.get("role", "employee")
    
    # Import professional report generator
    from components.agents.professional_report_generator import ProfessionalReportGenerator
    report_generator = ProfessionalReportGenerator(data_manager)
    
    st.markdown("### 📄 Generate Performance Report")
    
    employees = data_manager.load_data("employees") or []
    user_email = st.session_state.user.get("email", "")
    user_id = st.session_state.user.get("id", "")
    
    if user_role == "employee":
        # Employee can only generate their own report - no selection needed
        # Try to find employee by ID first, then by email
        current_employee = None
        if user_id:
            current_employee = next((e for e in employees if str(e.get("id", "")) == str(user_id)), None)
        
        if not current_employee and user_email:
            current_employee = next((e for e in employees if e.get("email", "").lower() == user_email.lower()), None)
        
        if not current_employee:
            st.error("❌ Employee data not found. Please contact administrator.")
            st.info("💡 If you just created your account, please wait a moment and refresh the page.")
            return
        
        # Automatically use the current employee - no selection needed
        employee_id = current_employee.get("id")
        employee_name = current_employee.get("name", "You")
        
        st.info(f"📋 Generating report for: **{employee_name}**")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Preview Report"):
                # Show detailed preview
                # employee_id is already set above for employees
                from components.agents.performance_agent import EnhancedPerformanceAgent
                perf_agent = EnhancedPerformanceAgent(data_manager)
                
                # Debug information section
                with st.expander("🔍 Debug Information - Performance Calculation Method", expanded=True):
                    st.markdown("### AI/ML Status Check")
                    
                    # Check ML model
                    ml_trained = perf_agent.ml_scorer.is_trained
                    ml_status = "✅ Trained" if ml_trained else "❌ Not Trained"
                    st.write(f"**ML Model Status:** {ml_status}")
                    
                    if ml_trained:
                        st.write(f"**ML Model Type:** {perf_agent.ml_scorer.model_type}")
                        try:
                            import os
                            model_path = "models/performance_scorer.pkl"
                            if os.path.exists(model_path):
                                st.write(f"**Model File:** ✅ Found at `{model_path}`")
                            else:
                                st.write(f"**Model File:** ❌ Not found at `{model_path}`")
                        except:
                            pass
                    
                    # Check AI client
                    ai_enabled = perf_agent.ai_client.enabled
                    ai_status = "✅ Enabled" if ai_enabled else "❌ Disabled"
                    st.write(f"**AI Client Status:** {ai_status}")
                    
                    if ai_enabled:
                        provider = getattr(perf_agent.ai_client, 'provider', 'N/A')
                        model = getattr(perf_agent.ai_client, 'model', 'N/A')
                        st.write(f"**AI Provider:** {provider}")
                        st.write(f"**AI Model:** {model}")
                    else:
                        st.info("💡 To enable AI: Set `USE_AI=true` in `.env` file and configure API key")
                    
                    # Determine which method will be used
                    st.markdown("---")
                    st.markdown("### Calculation Method")
                    if ml_trained:
                        method = "**ML Model** (Random Forest/XGBoost)"
                        st.success(f"Will use: {method}")
                    elif ai_enabled:
                        method = "**AI Fallback** (AI API)"
                        st.warning(f"Will use: {method}")
                    else:
                        method = "**Simple Fallback** (Weighted Formula)"
                        st.info(f"Will use: {method}")
                    
                    st.markdown("---")
                    st.markdown("### Environment Variables")
                    import os
                    use_ai = os.getenv("USE_AI", "false")
                    has_openai_key = "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Not Set"
                    has_anthropic_key = "✅ Set" if os.getenv("ANTHROPIC_API_KEY") else "❌ Not Set"
                    has_gemini_key = "✅ Set" if os.getenv("GEMINI_API_KEY") else "❌ Not Set"
                    
                    st.write(f"**USE_AI:** `{use_ai}`")
                    st.write(f"**OPENAI_API_KEY:** {has_openai_key}")
                    st.write(f"**ANTHROPIC_API_KEY:** {has_anthropic_key}")
                    st.write(f"**GEMINI_API_KEY:** {has_gemini_key}")
                
                eval_data = perf_agent.evaluate_employee(employee_id, save=False)
                
                # Get employee details
                employee = next((e for e in employees if str(e.get("id", "")) == str(employee_id)), None)
                
                # Get additional data
                tasks = data_manager.load_data("tasks") or []
                goals = data_manager.load_data("goals") or []
                feedback = data_manager.load_data("feedback") or []
                
                employee_tasks = [t for t in tasks if str(t.get("assigned_to", "")) == str(employee_id)]
                employee_goals = [g for g in goals if str(g.get("employee_id", "")) == str(employee_id) or str(g.get("user_id", "")) == str(employee_id)]
                employee_feedback = [f for f in feedback if str(f.get("employee_id", "")) == str(employee_id)]
                
                if eval_data:
                    st.markdown("### 📊 Performance Report Preview")
                    
                    # Employee Info
                    if employee:
                        st.markdown(f"**Employee:** {employee.get('name', 'N/A')} ({employee.get('email', 'N/A')})")
                        st.markdown(f"**Position:** {employee.get('position', 'N/A')}")
                        st.markdown("---")
                    
                    # Key Metrics
                    st.markdown("#### Key Performance Metrics")
                    col_preview1, col_preview2, col_preview3, col_preview4 = st.columns(4)
                    with col_preview1:
                        st.metric("Performance Score", f"{eval_data.get('performance_score', 0):.1f}%")
                    with col_preview2:
                        st.metric("Completion Rate", f"{eval_data.get('completion_rate', 0):.1f}%")
                    with col_preview3:
                        st.metric("On-Time Rate", f"{eval_data.get('on_time_rate', 0):.1f}%")
                    with col_preview4:
                        st.metric("Rank", eval_data.get('rank', 'N/A'))
                    
                    st.markdown("---")
                    
                    # Tasks Summary
                    if employee_tasks:
                        st.markdown("#### Tasks Summary")
                        completed_tasks = len([t for t in employee_tasks if t.get("status") == "completed"])
                        in_progress_tasks = len([t for t in employee_tasks if t.get("status") == "in_progress"])
                        pending_tasks = len([t for t in employee_tasks if t.get("status") == "pending"])
                        
                        task_col1, task_col2, task_col3, task_col4 = st.columns(4)
                        with task_col1:
                            st.metric("Total Tasks", len(employee_tasks))
                        with task_col2:
                            st.metric("Completed", completed_tasks)
                        with task_col3:
                            st.metric("In Progress", in_progress_tasks)
                        with task_col4:
                            st.metric("Pending", pending_tasks)
                        st.markdown("---")
                    
                    # Goals Summary
                    if employee_goals:
                        st.markdown("#### Goals Summary")
                        achieved_goals = len([g for g in employee_goals if g.get("status") == "achieved"])
                        active_goals = len([g for g in employee_goals if g.get("status") in ["active", "in_progress"]])
                        
                        goal_col1, goal_col2, goal_col3 = st.columns(3)
                        with goal_col1:
                            st.metric("Total Goals", len(employee_goals))
                        with goal_col2:
                            st.metric("Achieved", achieved_goals)
                        with goal_col3:
                            st.metric("Active", active_goals)
                        st.markdown("---")
                    
                    # Feedback Summary
                    if employee_feedback:
                        st.markdown("#### Feedback Summary")
                        avg_rating = sum([f.get('rating', 0) for f in employee_feedback if f.get('rating')]) / len([f for f in employee_feedback if f.get('rating')]) if [f for f in employee_feedback if f.get('rating')] else 0
                        feedback_col1, feedback_col2 = st.columns(2)
                        with feedback_col1:
                            st.metric("Total Feedback", len(employee_feedback))
                        with feedback_col2:
                            st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
                        st.markdown("---")
                    
                    # Performance Trend
                    st.markdown("#### Performance Trend")
                    trend = eval_data.get('trend', 'N/A')
                    trend_emoji = "📈" if trend == "improving" else "📉" if trend == "declining" else "➡️"
                    st.info(f"{trend_emoji} **Trend:** {trend.title()}")
                    
                    st.markdown("---")
                    
                    # AI-Generated Feedback
                    ai_feedback = eval_data.get('ai_feedback')
                    if ai_feedback:
                        st.markdown("#### 💬 AI Performance Feedback")
                        st.markdown(f"""
                        <div style="background-color: #1e1e1e; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF6B35; margin: 1rem 0;">
                            <p style="color: #e0e0e0; line-height: 1.6; margin: 0;">{ai_feedback}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("#### 💬 Performance Feedback")
                        st.info("Feedback generation is not available. Enable AI in your .env file to receive personalized performance feedback.")
        
        with col2:
            if st.button("📥 Generate PDF Report", type="primary"):
                # employee_id is already set above for employees
                result = report_generator.generate_performance_report_pdf(employee_id)
                
                if result.get("success"):
                    st.success("✅ Professional PDF report generated!")
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=result.get("content"),
                        file_name=result.get("filename"),
                        mime="application/pdf",
                    )
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    else:
        st.warning("⚠️ No employees available to generate reports.")
        st.markdown("---")
        st.markdown("### 📝 To Generate Performance Reports:")
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown("""
            **For Owners/Managers:**
            1. Go to **👥 Employees** page (left sidebar)
            2. Click **➕ Add Employee** tab
            3. Fill in employee details
            4. Click **🚀 Add Employee**
            5. Return here to generate reports
            """)
            
            if user_role in ["owner", "manager"]:
                if st.button("➡️ Go to Employees Page", type="primary"):
                    st.session_state.current_page = "Employees"
                    st.rerun()
        
        with col_info2:
            st.markdown("""
            **For Employees:**
            - Your employee record needs to be created by an Owner/Manager
            - Contact your administrator to add you to the system
            - Once added, you'll be able to generate your own performance report
            """)
        
        st.markdown("---")
        st.info("💡 **Tip:** After adding employees, they will appear in the dropdown above and you can generate their performance reports.")

# Employees page (for managers/owners only)
def employees_page():
    """Employees management page"""
    st.title("👥 Employees")
    st.markdown("---")
    
    agents = initialize_agents()
    performance_agent = agents["performance_agent"]
    data_manager = st.session_state.data_manager
    
    # Create tabs for View Employees and Add Employee
    tab1, tab2 = st.tabs(["📋 View Employees", "➕ Add Employee"])
    
    # View Employees tab
    with tab1:
        employees = data_manager.load_data("employees") or []
        
        if employees:
            st.markdown("### Employee List")
            for emp in employees:
                emp_id = str(emp.get("id", ""))
                emp_name = emp.get('name', 'Unknown')
                
                # Check if this employee is being edited
                editing_key = f"editing_employee_{emp_id}"
                deleting_key = f"deleting_employee_{emp_id}"
                
                # Show edit form if editing
                if st.session_state.get(editing_key, False):
                    st.markdown("---")
                    st.markdown(f"### ✏️ Edit Employee: {emp_name}")
                    
                    with st.form(f"edit_employee_form_{emp_id}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            edit_name = st.text_input("Name *", value=emp.get('name', ''), key=f"edit_name_{emp_id}")
                            edit_email = st.text_input("Email *", value=emp.get('email', ''), key=f"edit_email_{emp_id}")
                            edit_position = st.text_input("Position", value=emp.get('position', '') or '', key=f"edit_position_{emp_id}")
                        
                        with col2:
                            # Parse hire_date if it exists
                            hire_date_value = datetime.now().date()
                            if emp.get('hire_date'):
                                try:
                                    if isinstance(emp.get('hire_date'), str):
                                        hire_date_value = datetime.fromisoformat(emp.get('hire_date').split('T')[0]).date()
                                    else:
                                        hire_date_value = emp.get('hire_date')
                                except:
                                    pass
                            
                            edit_hire_date = st.date_input("Hire Date", value=hire_date_value, key=f"edit_hire_date_{emp_id}")
                        
                        # Skills
                        current_skills = emp.get('skills', {})
                        if isinstance(current_skills, str):
                            try:
                                current_skills = json.loads(current_skills)
                            except:
                                current_skills = {}
                        skills_json = json.dumps(current_skills, indent=2) if current_skills else ""
                        edit_skills = st.text_area("Skills (JSON format, optional)", 
                                                   value=skills_json,
                                                   key=f"edit_skills_{emp_id}",
                                                   height=100)
                        
                        st.markdown("---")
                        
                        col_save, col_cancel = st.columns([1, 4])
                        with col_save:
                            save_btn = st.form_submit_button("💾 Save Changes", type="primary")
                        with col_cancel:
                            cancel_btn = st.form_submit_button("❌ Cancel")
                        
                        if save_btn:
                            if not edit_name or not edit_email:
                                st.error("⚠️ Please enter both name and email.")
                            else:
                                try:
                                    # Check if email already exists for another employee
                                    existing_employees = data_manager.load_data("employees") or []
                                    email_exists = any(
                                        e.get('email', '').lower() == edit_email.lower() 
                                        and str(e.get('id', '')) != emp_id 
                                        for e in existing_employees
                                    )
                                    
                                    if email_exists:
                                        st.error(f"❌ An employee with email '{edit_email}' already exists.")
                                    else:
                                        # Prepare update data
                                        update_data = {
                                            "name": edit_name,
                                            "email": edit_email,
                                            "position": edit_position if edit_position else None,
                                            "hire_date": edit_hire_date.isoformat() if edit_hire_date else None
                                        }
                                        
                                        # Parse skills if provided
                                        if edit_skills.strip():
                                            try:
                                                skills_dict = json.loads(edit_skills)
                                                update_data["skills"] = skills_dict
                                            except json.JSONDecodeError:
                                                st.warning("⚠️ Invalid JSON format for skills. Skills will not be updated.")
                                        
                                        # Update employee
                                        data_manager.update_employee(emp_id, update_data)
                                        
                                        st.success(f"✅ Employee '{edit_name}' updated successfully!")
                                        st.session_state[editing_key] = False
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error updating employee: {str(e)}")
                                    st.exception(e)
                        
                        if cancel_btn:
                            st.session_state[editing_key] = False
                            st.rerun()
                
                # Show delete confirmation if deleting
                elif st.session_state.get(deleting_key, False):
                    st.markdown("---")
                    st.warning(f"⚠️ Are you sure you want to delete employee '{emp_name}'? This action cannot be undone.")
                    col_confirm, col_cancel_del = st.columns(2)
                    with col_confirm:
                        if st.button("✅ Yes, Delete", key=f"confirm_delete_{emp_id}", type="primary"):
                            try:
                                data_manager.delete_employee(emp_id)
                                st.success(f"✅ Employee '{emp_name}' deleted successfully!")
                                st.session_state[deleting_key] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error deleting employee: {str(e)}")
                                st.session_state[deleting_key] = False
                    with col_cancel_del:
                        if st.button("❌ Cancel", key=f"cancel_delete_{emp_id}"):
                            st.session_state[deleting_key] = False
                            st.rerun()
                
                # Normal view with edit/delete buttons
                else:
                    with st.expander(f"👤 {emp_name} - {emp.get('role', 'employee').title()}"):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**Email:** {emp.get('email', 'N/A')}")
                            st.write(f"**Position:** {emp.get('position', 'N/A')}")
                            st.write(f"**Role:** {emp.get('role', 'employee').title()}")
                            if emp.get('hire_date'):
                                st.write(f"**Hire Date:** {emp.get('hire_date', 'N/A')}")
                        with col2:
                            # Get performance
                            eval_data = performance_agent.evaluate_employee(emp.get("id"), save=False)
                            if eval_data:
                                st.write(f"**Performance Score:** {eval_data.get('performance_score', 0):.1f}%")
                                st.write(f"**Rank:** {eval_data.get('rank', 'N/A')}")
                        with col3:
                            if st.button("✏️ Edit", key=f"edit_btn_{emp_id}"):
                                st.session_state[editing_key] = True
                                st.rerun()
                            
                            if st.button("🗑️ Delete", key=f"delete_btn_{emp_id}", type="secondary"):
                                st.session_state[deleting_key] = True
                                st.rerun()
        else:
            st.info("No employees found.")
    
    # Add Employee tab
    with tab2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
                <h2 style="color: white; margin: 0;">➕ Add New Employee</h2>
                <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">Add a new employee to the system</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("create_employee_form"):
            col1, col2 = st.columns(2)
            with col1:
                employee_name = st.text_input("Name *", placeholder="e.g., John Doe", help="Enter the employee's full name")
                employee_email = st.text_input("Email *", placeholder="e.g., john@company.com", help="Enter the employee's email address")
                employee_position = st.text_input("Position", placeholder="e.g., Software Engineer", help="Enter the employee's job position")
            
            with col2:
                hire_date = st.date_input("Hire Date", value=datetime.now().date(),
                                         help="Select the employee's hire date")
            
            skills_input = st.text_area("Skills (JSON format, optional)", 
                                       placeholder='{"programming": ["Python", "JavaScript"], "languages": ["English"]}',
                                       help="Enter skills as JSON object (optional)")
            
            st.markdown("---")
            
            col_submit, col_clear = st.columns([1, 4])
            with col_submit:
                submit = st.form_submit_button("🚀 Add Employee", type="primary")
            
            if submit:
                if not employee_name or not employee_email:
                    st.error("⚠️ Please enter both name and email.")
                else:
                    try:
                        # Check if email already exists
                        existing_employees = data_manager.load_data("employees") or []
                        if any(emp.get('email', '').lower() == employee_email.lower() for emp in existing_employees):
                            st.error(f"❌ An employee with email '{employee_email}' already exists.")
                        else:
                            # Prepare employee data
                            employee_data = {
                                "name": employee_name,
                                "email": employee_email,
                                "position": employee_position if employee_position else None,
                                "hire_date": hire_date.isoformat() if hire_date else None
                            }
                            
                            # Parse skills if provided
                            if skills_input.strip():
                                try:
                                    skills_dict = json.loads(skills_input)
                                    employee_data["skills"] = skills_dict
                                except json.JSONDecodeError:
                                    st.warning("⚠️ Invalid JSON format for skills. Employee will be created without skills.")
                            
                            # Create employee using data manager
                            new_employee = data_manager.create_employee(employee_data)
                            
                            st.success(f"✅ Employee '{employee_name}' added successfully!")
                            st.balloons()
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error adding employee: {str(e)}")
                        st.exception(e)

# Main routing logic
if not st.session_state.authenticated:
    login_page()
else:
    # Sidebar navigation
    with st.sidebar:
        st.title("📊 Performance System")
        st.markdown("---")
        
        user = st.session_state.user
        if user:
            st.markdown(f"**Welcome, {user.get('name', user.get('email', 'User'))}**")
            st.markdown(f"*{user.get('role', 'employee').title()}*")
            st.markdown("---")
        
        # Navigation
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"
        
        if st.button("🏠 Dashboard"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        
        if st.button("📁 Projects"):
            st.session_state.current_page = "Projects"
            st.rerun()
        
        # Only show Employees button for managers/owners
        if user and user.get('role') in ['owner', 'manager']:
            if st.button("👥 Employees"):
                st.session_state.current_page = "Employees"
                st.rerun()
        
        # Tasks are shown within Projects, so no separate Tasks page needed
        
        if st.button("🎯 Goals"):
            st.session_state.current_page = "Goals"
            st.rerun()
        
        if st.button("💬 Feedback"):
            st.session_state.current_page = "Feedback"
            st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.current_page = "Dashboard"
            st.rerun()
    
    # Route to appropriate page
    current_page = st.session_state.get("current_page", "Dashboard")
    
    if current_page == "Dashboard":
        dashboard()
    elif current_page == "Projects":
        projects_page()
    elif current_page == "Goals":
        goals_page()
    elif current_page == "Feedback":
        feedback_page()
    elif current_page == "Reports":
        # Redirect Reports to Dashboard (merged functionality)
        st.session_state.current_page = "Dashboard"
        st.rerun()
    elif current_page == "Employees":
        employees_page()
    else:
        st.title(f"📄 {current_page}")
        st.info(f"{current_page} page is coming soon.")
