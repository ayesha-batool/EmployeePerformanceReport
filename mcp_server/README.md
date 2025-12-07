# MCP Server for Employee Performance Report System

This MCP (Model Context Protocol) server provides automation tools for the Employee Performance Report System.

## Features

The MCP server exposes the following automation tools:

### Performance Management
- **evaluate_all_employees**: Automatically evaluate performance for all employees
- **generate_performance_report**: Generate performance reports in JSON, PDF, or CSV format
- **get_employee_stats**: Get comprehensive statistics for an employee

### Risk & Monitoring
- **detect_all_risks**: Automatically detect all risks in the system
- **check_overdue_tasks**: Check for overdue tasks and optionally send notifications
- **check_overdue_goals**: Check for overdue goals and optionally send notifications
- **assess_workload**: Assess workload for all employees and identify overloaded employees

### Notifications
- **send_notification**: Send notifications to employees

### Reporting
- **generate_project_report**: Generate comprehensive reports for projects
- **export_data**: Export data to CSV or PDF format

### Attendance
- **record_attendance**: Record employee check-in/check-out

### Automation
- **automated_daily_check**: Run automated daily checks (performance evaluation, risk detection, overdue items)

## Installation

1. Install MCP dependencies:
```bash
pip install mcp
```

2. The server is configured to run via stdio. Add it to your MCP client configuration.

## Usage

### Using with Claude Desktop

Add to your Claude Desktop configuration file (`claude_desktop_config.json` on macOS or `claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "employee-performance-automation": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "cwd": "/path/to/project"
    }
  }
}
```

### Using with Other MCP Clients

The server communicates via stdio and follows the MCP protocol. Configure your MCP client to run:

```bash
python -m mcp_server.server
```

## Example Usage

### Evaluate All Employees
```json
{
  "tool": "evaluate_all_employees",
  "arguments": {
    "save_results": true
  }
}
```

### Check Overdue Tasks
```json
{
  "tool": "check_overdue_tasks",
  "arguments": {
    "send_notifications": true
  }
}
```

### Automated Daily Check
```json
{
  "tool": "automated_daily_check",
  "arguments": {
    "evaluate_performance": true,
    "detect_risks": true,
    "check_overdue": true
  }
}
```

## Scheduling

You can schedule the `automated_daily_check` tool to run daily using:
- Cron jobs (Linux/Mac)
- Task Scheduler (Windows)
- CI/CD pipelines
- Cloud functions (AWS Lambda, Google Cloud Functions, etc.)

### Example Cron Job (Daily at 9 AM)
```bash
0 9 * * * cd /path/to/project && python -m mcp_server.server --tool automated_daily_check
```

## Error Handling

All tools return structured JSON responses with:
- `status`: "success" or error information
- `message`: Human-readable message
- Tool-specific data

## Security

- The server runs with the same permissions as the user running it
- Ensure proper access controls for data files
- Consider running in a restricted environment for production use



