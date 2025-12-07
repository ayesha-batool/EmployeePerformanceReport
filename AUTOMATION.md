# Automation Guide

This project now includes comprehensive automation capabilities through an MCP (Model Context Protocol) server and standalone scripts.

## Quick Start

### Option 1: Standalone Script (Simplest)

Use the standalone automation script for quick tasks:

```bash
# Evaluate all employees
python automate.py evaluate

# Detect all risks
python automate.py risks

# Check overdue tasks
python automate.py overdue-tasks

# Check overdue goals
python automate.py overdue-goals

# Run all daily checks
python automate.py daily
```

### Option 2: MCP Server (Advanced)

Use the MCP server for integration with AI assistants and other tools:

```bash
# Run example usage
python -m mcp_server.example_usage

# Use CLI tool
python -m mcp_server.cli evaluate_all_employees --args '{"save_results": true}'

# Run scheduled daily checks
python -m mcp_server.scheduler
```

## Available Automation Tasks

### 1. Performance Evaluation
- **Evaluate all employees**: Automatically calculate performance scores for all employees
- **Generate reports**: Create performance reports in JSON, PDF, or CSV format
- **Get employee stats**: Retrieve comprehensive statistics for any employee

### 2. Risk Detection
- **Detect all risks**: Automatically identify risks in:
  - Employee performance
  - Project status
  - Task completion
  - System health

### 3. Monitoring & Alerts
- **Check overdue tasks**: Find tasks past their due date and optionally send notifications
- **Check overdue goals**: Find goals past their deadline and optionally send notifications
- **Assess workload**: Identify employees with excessive workload

### 4. Daily Automation
- **Automated daily check**: Runs all checks at once:
  - Performance evaluation
  - Risk detection
  - Overdue task checking
  - Overdue goal checking

## Scheduling

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `automate.py daily`
7. Start in: `C:\path\to\project`

### Linux/Mac Cron

Add to crontab (`crontab -e`):

```bash
# Run daily checks at 9 AM
0 9 * * * cd /path/to/project && python automate.py daily

# Run every hour
0 * * * * cd /path/to/project && python automate.py overdue-tasks
```

### Cloud Functions

You can deploy the automation scripts to:
- AWS Lambda
- Google Cloud Functions
- Azure Functions
- Heroku Scheduler

## Integration Examples

### With CI/CD Pipelines

```yaml
# GitHub Actions example
name: Daily Performance Check
on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run daily checks
        run: python automate.py daily
```

### With Monitoring Tools

Integrate with monitoring tools like:
- Prometheus
- Grafana
- Datadog
- New Relic

## MCP Server Integration

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "employee-performance-automation": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

### Custom MCP Client

The server follows the MCP protocol and can be integrated with any MCP-compatible client.

## API Reference

### Standalone Script

```bash
python automate.py <action> [options]

Actions:
  evaluate       - Evaluate all employees
  risks          - Detect all risks
  overdue-tasks  - Check overdue tasks
  overdue-goals  - Check overdue goals
  daily          - Run all daily checks

Options:
  --no-save      - Don't save evaluation results
  --no-notify    - Don't send notifications
```

### MCP Tools

See `mcp_server/README.md` for complete MCP tool documentation.

## Troubleshooting

### Import Errors

Make sure you're running from the project root:

```bash
cd /path/to/project
python automate.py daily
```

### Permission Errors

Ensure the script has write permissions to the `data/` directory.

### Notification Errors

Check that the notification system is properly configured in `components/agents/notification_agent.py`.

## Best Practices

1. **Schedule Daily Checks**: Run `daily` check once per day during off-peak hours
2. **Monitor Logs**: Check output for errors and warnings
3. **Backup Data**: Ensure data backups are in place before running evaluations
4. **Test First**: Test automation scripts in a development environment first
5. **Gradual Rollout**: Start with non-critical tasks before automating everything

## Security Considerations

- Automation scripts run with the same permissions as the user
- Ensure proper access controls for data files
- Consider running in a restricted environment for production
- Review notification settings to avoid spam
- Monitor for unusual activity

## Next Steps

1. Set up scheduled daily checks
2. Integrate with your monitoring tools
3. Customize automation tasks for your needs
4. Set up alerts for critical issues
5. Review and optimize automation frequency



