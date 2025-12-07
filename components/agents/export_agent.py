"""
Export Agent - Data export in multiple formats with scheduling
"""
import csv
import io
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from components.managers.data_manager import DataManager

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ExportAgent:
    """Data export agent for CSV and PDF formats"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def export_to_csv(self, data: List[Dict[str, Any]], filename: Optional[str] = None,
                      include_metadata: bool = True) -> Dict[str, Any]:
        """Export data to CSV format with enhanced formatting"""
        if not data:
            return {"success": False, "error": "No data to export"}
        
        output = io.StringIO()
        
        # Write metadata header if requested
        if include_metadata:
            output.write(f"# Export Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            output.write(f"# Total Records: {len(data)}\n")
            output.write("#\n")
        
        # Get all unique fieldnames from all records
        fieldnames = set()
        for record in data:
            fieldnames.update(record.keys())
        fieldnames = sorted(list(fieldnames))
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        # Write data rows with proper formatting
        for row in data:
            formatted_row = {}
            for key in fieldnames:
                value = row.get(key, "")
                # Format dates and timestamps
                if isinstance(value, str) and ("date" in key.lower() or "time" in key.lower() or "at" in key.lower()):
                    try:
                        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        formatted_row[key] = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        formatted_row[key] = value
                else:
                    formatted_row[key] = str(value) if value is not None else ""
            writer.writerow(formatted_row)
        
        csv_content = output.getvalue()
        output.close()
        
        if filename:
            filepath = f"exports/{filename}.csv"
            import os
            os.makedirs("exports", exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(csv_content)
        
        return {
            "success": True,
            "content": csv_content,
            "filename": filename or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    
    def export_to_pdf(self, data: List[Dict[str, Any]], title: str = "Report",
                     filename: Optional[str] = None, company_name: str = "Company",
                     include_branding: bool = True) -> Dict[str, Any]:
        """Export data to PDF format with professional templates and branding"""
        if not REPORTLAB_AVAILABLE:
            return {"success": False, "error": "ReportLab not installed"}
        
        if not data:
            return {"success": False, "error": "No data to export"}
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#1f4788"),
            spaceAfter=20,
            alignment=1  # Center alignment
        )
        
        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#666666"),
            spaceAfter=30,
            alignment=1
        )
        
        # Company branding header
        if include_branding:
            elements.append(Paragraph(company_name, title_style))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
            elements.append(Spacer(1, 0.3 * inch))
        
        # Title
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Convert data to table
        if data:
            # Headers
            headers = list(data[0].keys())
            table_data = [headers]
            
            # Data rows
            for row in data:
                table_data.append([str(row.get(key, "")) for key in headers])
            
            # Create table with professional styling
            table = Table(table_data, repeatRows=1)  # Repeat header on each page
            table.setStyle(TableStyle([
                # Header row
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4788")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 12),
                # Data rows
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            
            elements.append(table)
            
            # Footer
            elements.append(Spacer(1, 0.3 * inch))
            footer_style = ParagraphStyle(
                "Footer",
                parent=styles["Normal"],
                fontSize=8,
                textColor=colors.HexColor("#999999"),
                alignment=1
            )
            elements.append(Paragraph(f"Report generated by {company_name} Performance System", footer_style))
        
        # Build PDF
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        if filename:
            filepath = f"exports/{filename}.pdf"
            import os
            os.makedirs("exports", exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(pdf_content)
        
        return {
            "success": True,
            "content": pdf_content,
            "filename": filename or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        }
    
    def export_performance_report(self, employee_id: str, format: str = "json") -> Dict[str, Any]:
        """Export personal performance report in JSON format"""
        employees = self.data_manager.load_data("employees") or []
        performance_data = self.data_manager.load_data("performances") or []
        tasks = self.data_manager.load_data("tasks") or []
        
        employee = next((e for e in employees if e.get("id") == employee_id), None)
        if not employee:
            return {"success": False, "error": "Employee not found"}
        
        # Get performance data
        emp_perf = [p for p in performance_data if p.get("employee_id") == employee_id]
        latest_perf = max(emp_perf, key=lambda x: x.get("evaluated_at", "")) if emp_perf else None
        
        # Get employee tasks
        emp_tasks = [t for t in tasks if t.get("assigned_to") == employee_id]
        
        # Calculate overdue tasks
        overdue_count = 0
        for task in emp_tasks:
            if task.get("status") != "completed" and task.get("due_date"):
                try:
                    due_date = datetime.fromisoformat(task["due_date"])
                    if due_date < datetime.now():
                        overdue_count += 1
                except:
                    pass
        
        # Get performance history
        performance_history = sorted(emp_perf, key=lambda x: x.get("evaluated_at", ""), reverse=True)
        
        # Prepare comprehensive JSON report data
        report_data = {
            "report_type": "performance_report",
            "employee_id": employee_id,
            "generated_at": datetime.now().isoformat(),
            "employee_info": {
                "id": employee.get("id"),
                "name": employee.get("name", ""),
                "email": employee.get("email", ""),
                "department": employee.get("department", "N/A"),
                "position": employee.get("position", "N/A"),
                "status": employee.get("status", "active")
            },
            "performance_metrics": {
                "current_performance": latest_perf.get("performance_score", 0) if latest_perf else 0,
                "completion_rate": latest_perf.get("completion_rate", 0) if latest_perf else 0,
                "on_time_rate": latest_perf.get("on_time_rate", 0) if latest_perf else 0,
                "rank": latest_perf.get("rank", "N/A") if latest_perf else "N/A",
                "trend": latest_perf.get("trend", "stable") if latest_perf else "stable",
                "total_tasks": latest_perf.get("total_tasks", 0) if latest_perf else 0,
                "completed_tasks": latest_perf.get("completed_tasks", 0) if latest_perf else 0,
                "average_completion_time": latest_perf.get("average_completion_time", 0) if latest_perf else 0,
                "high_priority_completed": latest_perf.get("high_priority_completed", 0) if latest_perf else 0
            } if latest_perf else {},
            "task_statistics": {
                "total": len(emp_tasks),
                "completed": len([t for t in emp_tasks if t.get("status") == "completed"]),
                "pending": len([t for t in emp_tasks if t.get("status") == "pending"]),
                "in_progress": len([t for t in emp_tasks if t.get("status") == "in_progress"]),
                "overdue": overdue_count
            },
            "performance_history": performance_history[:10] if performance_history else [],  # Last 10 evaluations
            "latest_evaluation": latest_perf if latest_perf else None,
            "evaluation_date": latest_perf.get("evaluated_at") if latest_perf else None
        }
        
        if format == "json":
            # Export as JSON
            json_content = json.dumps(report_data, indent=2, default=str)
            
            filename = f"performance_report_{employee_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Save to file
            import os
            os.makedirs("exports", exist_ok=True)
            filepath = os.path.join("exports", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(json_content)
            
            return {
                "success": True,
                "content": json_content,
                "filename": filename,
                "report_data": report_data,
                "format": "json"
            }
        else:
            # Fallback to PDF for other formats
            pdf_data = [
                {"Metric": "Employee Name", "Value": employee.get("name", "")},
                {"Metric": "Employee ID", "Value": employee_id},
                {"Metric": "Department", "Value": employee.get("department", "N/A")},
            ]
            
            if latest_perf:
                pdf_data.extend([
                    {"Metric": "Performance Score", "Value": f"{latest_perf.get('performance_score', 0):.2f}"},
                    {"Metric": "Rank", "Value": str(latest_perf.get("rank", "N/A"))},
                    {"Metric": "Trend", "Value": latest_perf.get("trend", "N/A")},
                    {"Metric": "Completion Rate", "Value": f"{latest_perf.get('completion_rate', 0):.2f}%"},
                ])
            
            pdf_data.extend([
                {"Metric": "Total Tasks", "Value": str(len(emp_tasks))},
                {"Metric": "Completed Tasks", "Value": str(len([t for t in emp_tasks if t.get("status") == "completed"]))},
            ])
            
            result = self.export_to_pdf(
                pdf_data,
                title=f"Performance Report - {employee.get('name', employee_id)}",
                filename=f"performance_report_{employee_id}_{datetime.now().strftime('%Y%m%d')}"
            )
            
            result["report_data"] = report_data
            return result
    
    def create_export_schedule(self, schedule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a scheduled export job"""
        schedules = self.data_manager.load_data("export_schedules") or []
        
        schedule = {
            "id": f"schedule_{len(schedules) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": schedule_data.get("name", "Scheduled Export"),
            "export_type": schedule_data.get("export_type", "CSV"),  # CSV, PDF, JSON
            "data_type": schedule_data.get("data_type", "Performance"),  # Projects, Tasks, Employees, Performance
            "frequency": schedule_data.get("frequency", "daily"),  # daily, weekly, monthly
            "day_of_week": schedule_data.get("day_of_week"),  # For weekly: 0=Monday, 6=Sunday
            "day_of_month": schedule_data.get("day_of_month"),  # For monthly: 1-31
            "time": schedule_data.get("time", "09:00"),  # HH:MM format
            "recipient_email": schedule_data.get("recipient_email"),
            "hr_system_integration": schedule_data.get("hr_system_integration", False),
            "hr_system_endpoint": schedule_data.get("hr_system_endpoint"),
            "enabled": schedule_data.get("enabled", True),
            "created_by": schedule_data.get("created_by"),
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": self._calculate_next_run(schedule_data),
            "failure_count": 0,
            "last_error": None
        }
        
        schedules.append(schedule)
        self.data_manager.save_data("export_schedules", schedules)
        
        return {"success": True, "schedule": schedule}
    
    def _calculate_next_run(self, schedule_data: Dict[str, Any]) -> str:
        """Calculate next run time for scheduled export"""
        now = datetime.now()
        frequency = schedule_data.get("frequency", "daily")
        time_str = schedule_data.get("time", "09:00")
        
        try:
            hour, minute = map(int, time_str.split(":"))
        except:
            hour, minute = 9, 0
        
        if frequency == "daily":
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        elif frequency == "weekly":
            day_of_week = schedule_data.get("day_of_week", 0)  # Monday
            days_ahead = day_of_week - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
        elif frequency == "monthly":
            day_of_month = schedule_data.get("day_of_month", 1)
            next_run = now.replace(day=day_of_month, hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                # Move to next month
                if now.month == 12:
                    next_run = next_run.replace(year=now.year + 1, month=1)
                else:
                    next_run = next_run.replace(month=now.month + 1)
        else:
            next_run = now + timedelta(days=1)
        
        return next_run.isoformat()
    
    def get_export_schedules(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get export schedules"""
        schedules = self.data_manager.load_data("export_schedules") or []
        
        if user_id:
            schedules = [s for s in schedules if s.get("created_by") == user_id]
        
        return schedules
    
    def update_export_schedule(self, schedule_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an export schedule"""
        schedules = self.data_manager.load_data("export_schedules") or []
        
        for i, schedule in enumerate(schedules):
            if schedule.get("id") == schedule_id:
                schedules[i].update(updates)
                schedules[i]["updated_at"] = datetime.now().isoformat()
                if "frequency" in updates or "time" in updates or "day_of_week" in updates or "day_of_month" in updates:
                    schedules[i]["next_run"] = self._calculate_next_run(schedules[i])
                self.data_manager.save_data("export_schedules", schedules)
                return {"success": True, "schedule": schedules[i]}
        
        return {"success": False, "error": "Schedule not found"}
    
    def delete_export_schedule(self, schedule_id: str) -> bool:
        """Delete an export schedule"""
        schedules = self.data_manager.load_data("export_schedules") or []
        original_count = len(schedules)
        schedules = [s for s in schedules if s.get("id") != schedule_id]
        
        if len(schedules) < original_count:
            self.data_manager.save_data("export_schedules", schedules)
            return True
        return False

