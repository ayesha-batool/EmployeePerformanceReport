"""
Professional Report Generator - Creates professional PDF documents
"""
import io
from datetime import datetime
from typing import Dict, Any, Optional, List
from components.managers.data_manager import DataManager

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
        PageBreak, Image, KeepTogether
    )
    from reportlab.lib.units import inch, cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ProfessionalReportGenerator:
    """Generate professional PDF reports with charts, tables, and formatting"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def generate_performance_report_pdf(self, employee_id: str) -> Dict[str, Any]:
        """Generate professional performance report PDF"""
        if not REPORTLAB_AVAILABLE:
            return {"success": False, "error": "ReportLab not installed. Install with: pip install reportlab"}
        
        employees = self.data_manager.load_data("employees") or []
        employee = next((e for e in employees if str(e.get("id", "")) == str(employee_id)), None)
        if not employee:
            return {"success": False, "error": "Employee not found"}
        
        # Get performance data
        from components.agents.performance_agent import EnhancedPerformanceAgent
        performance_agent = EnhancedPerformanceAgent(self.data_manager)
        eval_data = performance_agent.evaluate_employee(employee_id, save=False)
        
        # Get tasks and goals
        tasks = self.data_manager.load_data("tasks") or []
        goals = self.data_manager.load_data("goals") or []
        feedback = self.data_manager.load_data("feedback") or []
        
        employee_tasks = [t for t in tasks if str(t.get("assigned_to", "")) == str(employee_id)]
        employee_goals = [g for g in goals if str(g.get("employee_id", "")) == str(employee_id) or str(g.get("user_id", "")) == str(employee_id)]
        employee_feedback = [f for f in feedback if str(f.get("employee_id", "")) == str(employee_id)]
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1a365d"),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold"
        )
        
        # Subtitle style
        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=12,
            textColor=colors.HexColor("#4a5568"),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Section header
        section_style = ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#2d3748"),
            spaceAfter=12,
            spaceBefore=20,
            fontName="Helvetica-Bold",
            borderWidth=1,
            borderColor=colors.HexColor("#e2e8f0"),
            borderPadding=10,
            backColor=colors.HexColor("#f7fafc")
        )
        
        # Header
        elements.append(Paragraph("Employee Performance Report", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                                  styles["Normal"]))
        elements.append(Spacer(1, 0.5*inch))
        
        # Employee Information
        elements.append(Paragraph("Employee Information", section_style))
        emp_info_data = [
            ["Name:", employee.get("name", "N/A")],
            ["Email:", employee.get("email", "N/A")],
            ["Position:", employee.get("position", employee.get("role", "N/A"))],
            ["Report Date:", datetime.now().strftime("%Y-%m-%d")]
        ]
        emp_table = Table(emp_info_data, colWidths=[2*inch, 4*inch])
        emp_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf2f7")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(emp_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Performance Summary
        if eval_data:
            elements.append(Paragraph("Performance Summary", section_style))
            perf_data = [
                ["Metric", "Score", "Status"],
                ["Overall Performance", f"{eval_data.get('performance_score', 0):.1f}%", 
                 self._get_performance_status(eval_data.get('performance_score', 0))],
                ["Task Completion Rate", f"{eval_data.get('completion_rate', 0):.1f}%",
                 self._get_performance_status(eval_data.get('completion_rate', 0))],
                ["On-Time Delivery", f"{eval_data.get('on_time_rate', 0):.1f}%",
                 self._get_performance_status(eval_data.get('on_time_rate', 0))],
                ["Rank", eval_data.get('rank', 'N/A'), ""],
                ["Trend", eval_data.get('trend', 'N/A'), ""]
            ]
            perf_table = Table(perf_data, colWidths=[2.5*inch, 2*inch, 2*inch])
            perf_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))
            elements.append(perf_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Tasks Summary
        if employee_tasks:
            elements.append(Paragraph("Tasks Summary", section_style))
            completed = len([t for t in employee_tasks if t.get("status") == "completed"])
            in_progress = len([t for t in employee_tasks if t.get("status") == "in_progress"])
            pending = len([t for t in employee_tasks if t.get("status") == "pending"])
            
            task_summary = [
                ["Status", "Count", "Percentage"],
                ["Completed", str(completed), f"{(completed/len(employee_tasks)*100):.1f}%"],
                ["In Progress", str(in_progress), f"{(in_progress/len(employee_tasks)*100):.1f}%"],
                ["Pending", str(pending), f"{(pending/len(employee_tasks)*100):.1f}%"],
                ["Total", str(len(employee_tasks)), "100%"]
            ]
            task_table = Table(task_summary, colWidths=[2*inch, 2*inch, 2*inch])
            task_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(task_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Goals Summary
        if employee_goals:
            elements.append(Paragraph("Goals Summary", section_style))
            goals_data = [["Goal", "Status", "Progress", "Deadline"]]
            for goal in employee_goals[:10]:  # Limit to 10 goals
                progress = goal.get('progress_percentage', 0) if 'progress_percentage' in goal else (
                    (goal.get('current_value', 0) / goal.get('target_value', 1) * 100) if goal.get('target_value', 0) > 0 else 0
                )
                deadline = goal.get('deadline') or goal.get('target_date') or 'N/A'
                goals_data.append([
                    goal.get('title', 'Untitled')[:40],
                    goal.get('status', 'active').title(),
                    f"{progress:.1f}%",
                    str(deadline)[:10] if deadline != 'N/A' else 'N/A'
                ])
            
            goals_table = Table(goals_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            goals_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("ALIGN", (2, 1), (2, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(goals_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Feedback Summary
        if employee_feedback:
            elements.append(Paragraph("Recent Feedback", section_style))
            avg_rating = sum([f.get('rating', 0) for f in employee_feedback if f.get('rating')]) / len([f for f in employee_feedback if f.get('rating')]) if [f for f in employee_feedback if f.get('rating')] else 0
            elements.append(Paragraph(f"Average Rating: {avg_rating:.1f}/5.0", styles["Normal"]))
            elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#718096"),
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Confidential - Performance Management System", footer_style))
        elements.append(Paragraph(f"Page 1 | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
        
        # Build PDF
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f"performance_report_{employee.get('name', 'employee').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return {
            "success": True,
            "content": pdf_content,
            "filename": filename
        }
    
    def generate_project_report_pdf(self, project_id: str) -> Dict[str, Any]:
        """Generate professional project report PDF"""
        if not REPORTLAB_AVAILABLE:
            return {"success": False, "error": "ReportLab not installed"}
        
        from components.agents.reporting_agent import ReportingAgent
        reporting_agent = ReportingAgent(self.data_manager)
        report_data = reporting_agent.generate_project_report(project_id)
        
        if report_data.get("error"):
            return {"success": False, "error": report_data.get("error")}
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "Title", parent=styles["Heading1"],
            fontSize=20, textColor=colors.HexColor("#1a365d"),
            spaceAfter=20, alignment=TA_CENTER, fontName="Helvetica-Bold"
        )
        
        section_style = ParagraphStyle(
            "Section", parent=styles["Heading2"],
            fontSize=14, textColor=colors.HexColor("#2d3748"),
            spaceAfter=10, spaceBefore=15, fontName="Helvetica-Bold"
        )
        
        # Header
        elements.append(Paragraph("Project Report", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles["Normal"]))
        elements.append(Spacer(1, 0.3*inch))
        
        # Project Information
        elements.append(Paragraph("Project Overview", section_style))
        project_info = [
            ["Project Name:", report_data.get("project_name", "N/A")],
            ["Status:", report_data.get("status", "N/A").title()],
            ["Total Tasks:", str(report_data.get("total_tasks", 0))],
            ["Completed Tasks:", str(report_data.get("completed_tasks", 0))],
            ["Completion Rate:", f"{report_data.get('completion_rate', 0):.1f}%"],
            ["Health Score:", f"{report_data.get('health_score', 0):.1f}/100"]
        ]
        info_table = Table(project_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf2f7")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Risks
        if report_data.get("risks"):
            elements.append(Paragraph("Identified Risks", section_style))
            risks_data = [["Risk", "Severity", "Description"]]
            for risk in report_data.get("risks", [])[:5]:
                risks_data.append([
                    risk.get("type", "Unknown"),
                    risk.get("severity", "Medium"),
                    risk.get("description", "No description")[:50]
                ])
            risks_table = Table(risks_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
            risks_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
            ]))
            elements.append(risks_table)
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle("Footer", parent=styles["Normal"],
                                     fontSize=8, textColor=colors.HexColor("#718096"),
                                     alignment=TA_CENTER)
        elements.append(Paragraph("Confidential - Performance Management System", footer_style))
        
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f"project_report_{report_data.get('project_name', 'project').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return {
            "success": True,
            "content": pdf_content,
            "filename": filename
        }
    
    def _get_performance_status(self, score: float) -> str:
        """Get performance status based on score"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Needs Improvement"
        else:
            return "Poor"




