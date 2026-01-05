"""
Export CLI Commands

Handles CLI operations for exporting data.
"""

import sys
from pathlib import Path
from typing import List

from ...application.services import VariableManagementService, ProcessInvestigationService


def add_export_subparsers(subparsers, var_service: VariableManagementService, process_service: ProcessInvestigationService):
    """Add export subcommands to the parser."""

    # export env
    env_parser = subparsers.add_parser(
        'env',
        help='Export environment variables'
    )
    env_parser.add_argument(
        '--scope',
        choices=['system', 'user', 'process', 'all'],
        default='user',
        help='Scope to export (default: user)'
    )
    env_parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'shell'],
        default='json',
        help='Export format (default: json)'
    )
    env_parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output file path (default: stdout)'
    )

    # export processes
    processes_parser = subparsers.add_parser(
        'processes',
        help='Export process information'
    )
    processes_parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'table'],
        default='markdown',
        help='Export format (default: markdown)'
    )
    processes_parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output file path (default: stdout)'
    )

    # export all-envs
    all_envs_parser = subparsers.add_parser(
        'all-envs',
        help='Export all process environments'
    )
    all_envs_parser.add_argument(
        '--format',
        choices=['json', 'markdown'],
        default='markdown',
        help='Export format (default: markdown)'
    )
    all_envs_parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output file path (default: stdout)'
    )


def handle_export_command(args, var_service: VariableManagementService, process_service: ProcessInvestigationService) -> int:
    """Handle export commands."""

    if hasattr(args, 'env') and args.env:
        return _handle_export_env(args, var_service)
    elif hasattr(args, 'processes') and args.processes:
        return _handle_export_processes(args, process_service)
    elif hasattr(args, 'all_envs') and args.all_envs:
        return _handle_export_all_envs(args, process_service)
    else:
        print("Error: No export subcommand specified", file=sys.stderr)
        return 1


def _handle_export_env(args, var_service: VariableManagementService) -> int:
    """Handle export env command."""
    try:
        # Get variables based on scope
        if args.scope == 'all':
            variables = var_service.get_all_variables()
        else:
            variables = var_service.get_variables_by_scope(args.scope)

        if not variables:
            print(f"No environment variables found in {args.scope} scope.")
            return 0

        # Generate output based on format
        if args.format == 'json':
            output = _generate_env_json(variables)
        elif args.format == 'markdown':
            output = _generate_env_markdown(variables, args.scope)
        elif args.format == 'shell':
            output = _generate_env_shell(variables)

        # Write to file or stdout
        _write_output(output, args.output)
        return 0

    except Exception as e:
        print(f"Error exporting environment variables: {e}", file=sys.stderr)
        return 1


def _handle_export_processes(args, process_service: ProcessInvestigationService) -> int:
    """Handle export processes command."""
    try:
        processes = process_service.get_all_processes()

        if not processes:
            print("No processes found.")
            return 0

        # Generate output based on format
        if args.format == 'json':
            output = _generate_processes_json(processes)
        elif args.format == 'markdown':
            output = _generate_processes_markdown(processes)
        elif args.format == 'table':
            output = _generate_processes_table(processes)

        # Write to file or stdout
        _write_output(output, args.output)
        return 0

    except Exception as e:
        print(f"Error exporting processes: {e}", file=sys.stderr)
        return 1


def _handle_export_all_envs(args, process_service: ProcessInvestigationService) -> int:
    """Handle export all-envs command."""
    try:
        # This would be a comprehensive export of all process environments
        # For now, we'll create a simplified version
        processes = process_service.get_all_processes()

        if args.format == 'json':
            # Collect all accessible environments
            all_envs = {}
            for proc in processes:
                report = process_service.get_process_environment_report(proc.pid)
                if report and report.all_variables:
                    all_envs[str(proc.pid)] = {
                        'name': proc.name,
                        'command': proc.command_line,
                        'user': proc.username,
                        'environment': report.all_variables
                    }

            import json
            output = json.dumps(all_envs, indent=2)

        elif args.format == 'markdown':
            # Generate markdown with all process environments
            lines = ["# Complete System Environment Variables Export\n"]
            lines.append(f"**Total Processes:** {len(processes)}\n")

            accessible_count = 0
            for proc in processes:
                report = process_service.get_process_environment_report(proc.pid)
                if report and report.all_variables:
                    accessible_count += 1
                    lines.append(f"## Process: {proc.name} (PID: {proc.pid})")
                    lines.append(f"**Command:** {proc.command_line}")
                    lines.append(f"**User:** {proc.username}")
                    lines.append(f"**Variables:** {len(report.all_variables)}\n")

                    lines.append("### Environment Variables")
                    lines.append("```bash")
                    for name, value in sorted(report.all_variables.items())[:20]:  # Limit for readability
                        safe_value = value[:50] + '...' if len(value) > 50 else value
                        lines.append(f'{name}="{safe_value}"')
                    lines.append("```\n")

            lines.append("## Summary")
            lines.append(f"- **Total Processes:** {len(processes)}")
            lines.append(f"- **Processes with Environments:** {accessible_count}")

            output = "\n".join(lines)

        # Write to file or stdout
        _write_output(output, args.output)
        return 0

    except Exception as e:
        print(f"Error exporting all environments: {e}", file=sys.stderr)
        return 1


def _generate_env_json(variables):
    """Generate JSON output for environment variables."""
    import json

    env_dict = {}
    for var in variables:
        env_dict[var.name.value] = {
            'value': var.value.value,
            'scope': str(var.scope),
            'created': var.created_at.isoformat(),
            'updated': var.updated_at.isoformat()
        }

    return json.dumps(env_dict, indent=2)


def _generate_env_markdown(variables, scope):
    """Generate markdown output for environment variables."""
    from datetime import datetime

    lines = []
    lines.append("# Environment Variables Export\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Scope:** {scope}")
    lines.append(f"**Total Variables:** {len(variables)}\n")

    lines.append("## Environment Variables\n")
    lines.append("| Name | Value | Created | Updated |")
    lines.append("|------|-------|---------|---------|")

    for var in variables:
        name = var.name.value
        value = var.value.value[:50] + '...' if len(var.value.value) > 50 else var.value.value
        created = var.created_at.strftime("%Y-%m-%d %H:%M")
        updated = var.updated_at.strftime("%Y-%m-%d %H:%M")

        lines.append(f"| {name} | {value} | {created} | {updated} |")

    lines.append("\n---")
    lines.append("*Generated by Environment Variable Editor*")

    return "\n".join(lines)


def _generate_env_shell(variables):
    """Generate shell export output for environment variables."""
    lines = []
    for var in variables:
        safe_value = var.value.value.replace('"', '\\"').replace('`', '\\`').replace('$', '\\$')
        lines.append(f'export {var.name.value}="{safe_value}"')

    return "\n".join(lines)


def _generate_processes_json(processes):
    """Generate JSON output for processes."""
    import json

    process_list = []
    for proc in processes:
        process_list.append({
            'pid': proc.pid,
            'name': proc.name,
            'command_line': proc.command_line,
            'username': proc.username,
            'parent_pid': proc.parent_pid,
            'variable_count': proc.variable_count
        })

    return json.dumps(process_list, indent=2)


def _generate_processes_markdown(processes):
    """Generate markdown output for processes."""
    from datetime import datetime

    lines = []
    lines.append("# Process Information Export\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Total Processes:** {len(processes)}\n")

    lines.append("## Running Processes\n")
    lines.append("| PID | Name | Command Line | User | Parent PID | Variables |")
    lines.append("|-----|------|--------------|------|------------|-----------|")

    for proc in processes[:100]:  # Limit for readability
        pid = str(proc.pid)
        name = proc.name[:20] if len(proc.name) > 20 else proc.name
        cmd = proc.command_line[:40] + '...' if len(proc.command_line) > 40 else proc.command_line
        user = proc.username[:10] if len(proc.username) > 10 else proc.username
        parent = str(proc.parent_pid) if proc.parent_pid else ''
        vars_count = str(proc.variable_count)

        lines.append(f"| {pid} | {name} | {cmd} | {user} | {parent} | {vars_count} |")

    if len(processes) > 100:
        lines.append(f"\n*... and {len(processes) - 100} more processes*")

    lines.append("\n---")
    lines.append("*Generated by Environment Variable Editor*")

    return "\n".join(lines)


def _generate_processes_table(processes):
    """Generate table output for processes."""
    lines = []
    lines.append(f"{'PID':<8} {'Name':<20} {'Command':<40} {'User':<12} {'Parent':<8} {'Vars':<5}")
    lines.append("-" * 95)

    for proc in processes[:50]:  # Limit for readability
        pid = str(proc.pid)[:7]
        name = proc.name[:19] if len(proc.name) > 19 else proc.name
        cmd = proc.command_line[:39] if len(proc.command_line) > 39 else proc.command_line
        user = proc.username[:11] if len(proc.username) > 11 else proc.username
        parent = str(proc.parent_pid)[:7] if proc.parent_pid else ''
        vars_count = str(proc.variable_count)[:4]

        lines.append(f"{pid:<8} {name:<20} {cmd:<40} {user:<12} {parent:<8} {vars_count:<5}")

    if len(processes) > 50:
        lines.append(f"\n... and {len(processes) - 50} more processes")

    return "\n".join(lines)


def _write_output(content: str, output_path: Path = None):
    """Write content to file or stdout."""
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Output written to {output_path}")
    else:
        print(content)
