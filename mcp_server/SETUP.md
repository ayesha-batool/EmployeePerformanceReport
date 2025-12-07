# MCP Server Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The MCP package will be installed automatically. If you encounter issues, install it separately:

```bash
pip install mcp
```

### 2. Test the Server

Run the example usage script to test:

```bash
python -m mcp_server.example_usage
```

### 3. Use the CLI Tool

Run individual automation tasks:

```bash
# Evaluate all employees
python -m mcp_server.cli evaluate_all_employees --args '{"save_results": true}'

# Check overdue tasks
python -m mcp_server.cli check_overdue_tasks --args '{"send_notifications": true}'

# Run automated daily check
python -m mcp_server.cli automated_daily_check --args '{"evaluate_performance": true, "detect_risks": true, "check_overdue": true}'
```

### 4. Schedule Daily Checks

#### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily" at desired time
4. Action: Start a program
5. Program: `python`
6. Arguments: `-m mcp_server.scheduler`
7. Start in: `C:\path\to\project`

#### Linux/Mac (Cron)

Add to crontab (`crontab -e`):

```bash
# Run daily checks at 9 AM every day
0 9 * * * cd /path/to/project && python -m mcp_server.scheduler
```

### 5. Configure MCP Client (Optional)

If you want to use this with an MCP client (like Claude Desktop):

#### Claude Desktop Configuration

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "employee-performance-automation": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

## Available Tools

### Performance Management
- `evaluate_all_employees` - Evaluate all employees at once
- `generate_performance_report` - Generate reports (JSON/PDF/CSV)
- `get_employee_stats` - Get comprehensive employee statistics

### Monitoring
- `detect_all_risks` - Detect all system risks
- `check_overdue_tasks` - Find and notify about overdue tasks
- `check_overdue_goals` - Find and notify about overdue goals
- `assess_workload` - Check employee workload

### Automation
- `automated_daily_check` - Run all daily checks at once

### Other Tools
- `send_notification` - Send notifications
- `generate_project_report` - Generate project reports
- `export_data` - Export data to CSV/PDF
- `record_attendance` - Record attendance

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the project root:

```bash
cd /path/to/project
python -m mcp_server.server
```

### MCP Library Not Found

If the MCP library is not available, the server will still work for CLI usage. Install it with:

```bash
pip install mcp
```

### Path Issues

Make sure all paths in configuration files use absolute paths, not relative paths.

## Next Steps

1. Test individual tools using the CLI
2. Set up scheduled daily checks
3. Integrate with your MCP client if needed
4. Customize automation tasks as needed



