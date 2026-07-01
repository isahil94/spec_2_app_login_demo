"""
Workflow Summary Generator

Generates comprehensive reports about workflow execution:
- Execution summary
- Timeline of events
- Artifact inventory
- Approval decisions
- Performance metrics
- Blockers and issues
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict


class WorkflowSummaryGenerator:
    """Generates workflow execution summaries"""

    def __init__(self, log_dir: Path, artifact_dir: Path, approval_dir: Path):
        """Initialize summary generator"""
        self.log_dir = log_dir
        self.artifact_dir = artifact_dir
        self.approval_dir = approval_dir

    def generate_execution_summary(self, workflow_id: str) -> Dict[str, Any]:
        """Generate comprehensive execution summary"""
        summary_file = self.log_dir / f"{workflow_id}-summary.json"

        if summary_file.exists():
            with open(summary_file, "r") as f:
                return json.load(f)

        return self._build_summary(workflow_id)

    def generate_markdown_report(self, workflow_id: str) -> str:
        """Generate markdown-formatted summary report"""
        summary = self.generate_execution_summary(workflow_id)

        report = f"""# Workflow Execution Report

**Workflow ID:** {workflow_id}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Status:** {summary.get('status', 'unknown').upper()}
- **Total Events:** {summary.get('total_events', 0)}
- **Critical Issues:** {len(summary.get('critical_events', []))}
- **Approval Requests:** {len(summary.get('approval_requests', []))}

## Timeline

### Event Summary by Type

"""
        for event_type, count in summary.get('events_by_type', {}).items():
            report += f"- **{event_type}:** {count} events\n"

        report += "\n### Event Summary by Stage\n\n"
        for stage, count in summary.get('events_by_stage', {}).items():
            report += f"- **{stage}:** {count} events\n"

        # Critical events
        if summary.get('critical_events'):
            report += "\n## Critical Events\n\n"
            for event in summary['critical_events']:
                report += f"### {event['event_type']}\n"
                report += f"- **Stage:** {event.get('stage', 'N/A')}\n"
                report += f"- **Message:** {event['message']}\n"
                report += f"- **Time:** {event['timestamp']}\n\n"

        # Artifacts
        if summary.get('artifacts', {}).get('stages'):
            report += "\n## Generated Artifacts\n\n"
            for stage, artifacts in summary['artifacts']['stages'].items():
                count = artifacts.get('artifact_count', 0)
                if count > 0:
                    report += f"### {stage}\n"
                    report += f"- **Count:** {count}\n"
                    for artifact in artifacts.get('artifacts', [])[:5]:
                        report += f"- {artifact['name']} ({artifact['size_bytes']} bytes)\n"
                    if count > 5:
                        report += f"- ... and {count - 5} more\n"
                    report += "\n"

        # Approvals
        if summary.get('approvals', {}).get('pending_count', 0) > 0:
            report += "\n## Pending Approvals\n\n"
            report += f"- **Pending:** {summary['approvals']['pending_count']}\n"
            report += f"- **Approved:** {summary['approvals']['approved_count']}\n"
            report += f"- **Rejected:** {summary['approvals']['rejected_count']}\n"

        # Performance
        if summary.get('performance'):
            report += "\n## Performance Metrics\n\n"
            perf = summary['performance']
            report += f"- **Total Duration:** {perf.get('total_duration_seconds', 0):.2f}s\n"
            report += f"- **Average Stage Duration:** {perf.get('average_stage_duration_seconds', 0):.2f}s\n"
            report += f"- **Slowest Stage:** {perf.get('slowest_stage', 'N/A')}\n"
            report += f"- **Slowest Stage Duration:** {perf.get('slowest_stage_duration_seconds', 0):.2f}s\n"

        report += "\n---\n"
        report += f"\n*Report generated: {datetime.now().isoformat()}*\n"

        return report

    def generate_blockers_report(self, workflow_id: str) -> str:
        """Generate report of blockers and issues"""
        summary = self.generate_execution_summary(workflow_id)

        report = f"# Blockers & Issues Report\n\n"
        report += f"**Workflow ID:** {workflow_id}\n\n"

        critical_events = summary.get('critical_events', [])

        if not critical_events:
            report += "✓ No critical issues found\n"
            return report

        report += f"## {len(critical_events)} Critical Issues Found\n\n"

        by_stage = defaultdict(list)
        for event in critical_events:
            stage = event.get('stage', 'unknown')
            by_stage[stage].append(event)

        for stage in sorted(by_stage.keys()):
            events = by_stage[stage]
            report += f"### Stage: {stage}\n\n"
            for event in events:
                report += f"- **{event['type']}**\n"
                report += f"  - {event['message']}\n"
                report += f"  - Time: {event['timestamp']}\n\n"

        return report

    def generate_artifacts_report(self, workflow_id: str) -> str:
        """Generate report of generated artifacts"""
        report = f"# Artifacts Report\n\n"
        report += f"**Workflow ID:** {workflow_id}\n\n"

        # Scan artifact directory
        if not self.artifact_dir.exists():
            report += "No artifacts found.\n"
            return report

        total_size = 0
        total_count = 0
        by_stage = defaultdict(list)

        for stage_dir in self.artifact_dir.iterdir():
            if stage_dir.is_dir():
                stage_name = stage_dir.name
                for artifact_file in stage_dir.iterdir():
                    if artifact_file.is_file():
                        size = artifact_file.stat().st_size
                        total_size += size
                        total_count += 1
                        by_stage[stage_name].append({
                            'name': artifact_file.name,
                            'size': size,
                        })

        report += f"## Summary\n\n"
        report += f"- **Total Artifacts:** {total_count}\n"
        report += f"- **Total Size:** {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)\n\n"

        report += f"## Artifacts by Stage\n\n"
        for stage in sorted(by_stage.keys()):
            artifacts = by_stage[stage]
            stage_size = sum(a['size'] for a in artifacts)
            report += f"### {stage}\n\n"
            report += f"- **Count:** {len(artifacts)}\n"
            report += f"- **Size:** {stage_size:,} bytes\n"
            report += f"- **Files:**\n"
            for artifact in sorted(artifacts, key=lambda a: a['name']):
                report += f"  - {artifact['name']} ({artifact['size']:,} bytes)\n"
            report += "\n"

        return report

    def generate_approvals_report(self, workflow_id: str) -> str:
        """Generate report of approval decisions"""
        summary = self.generate_execution_summary(workflow_id)

        report = f"# Approvals Report\n\n"
        report += f"**Workflow ID:** {workflow_id}\n\n"

        approvals = summary.get('approvals', {})

        report += f"## Summary\n\n"
        report += f"- **Pending:** {approvals.get('pending_count', 0)}\n"
        report += f"- **Approved:** {approvals.get('approved_count', 0)}\n"
        report += f"- **Rejected:** {approvals.get('rejected_count', 0)}\n\n"

        # Pending approvals
        pending = approvals.get('pending', [])
        if pending:
            report += f"## Pending Approvals ({len(pending)})\n\n"
            for approval in pending:
                report += f"### {approval.get('stage', 'unknown')}\n\n"
                report += f"- **ID:** {approval.get('approval_id', 'N/A')}\n"
                report += f"- **Created:** {approval.get('created_at', 'N/A')}\n"
                report += f"- **Blocker Type:** {approval.get('blocker_type', 'unknown')}\n"
                report += f"- **Severity:** {approval.get('severity', 'unknown')}\n"
                report += "\n"

        # Approved
        approved = approvals.get('approved', [])
        if approved:
            report += f"## Approved ({len(approved)})\n\n"
            for approval in approved[-5:]:  # Last 5
                report += f"- **{approval.get('stage', 'unknown')}** - Approved by {approval.get('approved_by', 'unknown')} on {approval.get('approved_at', 'N/A')}\n"

        # Rejected
        rejected = approvals.get('rejected', [])
        if rejected:
            report += f"\n## Rejected ({len(rejected)})\n\n"
            for approval in rejected[-5:]:  # Last 5
                report += f"- **{approval.get('stage', 'unknown')}** - Rejected by {approval.get('approved_by', 'unknown')}\n"

        return report

    def _build_summary(self, workflow_id: str) -> Dict[str, Any]:
        """Build summary from available data"""
        return {
            "workflow_id": workflow_id,
            "generated_at": datetime.now().isoformat(),
            "status": "unknown",
            "total_events": 0,
            "events_by_type": {},
            "events_by_stage": {},
            "critical_events": [],
            "artifacts": {
                "stages": {}
            },
            "approvals": {
                "pending_count": 0,
                "approved_count": 0,
                "rejected_count": 0,
            },
            "performance": {
                "total_duration_seconds": 0,
                "average_stage_duration_seconds": 0,
            },
        }
