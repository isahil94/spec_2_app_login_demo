"""
Event Bus for autonomous workflow coordination.

Implements event-driven architecture for agent communication:
- Agents publish events when they complete
- Supervisor subscribes to events
- Chat integration receives progress updates
- Approval service listens for user decisions
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional


logger = logging.getLogger(__name__)


class EventType(Enum):
    """Event types in the workflow."""

    # Agent lifecycle
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"

    # Approval gates
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_APPROVED = "approval_approved"
    APPROVAL_REJECTED = "approval_rejected"

    # Workflow
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"

    # Validation
    VALIDATION_PASSED = "validation_passed"
    VALIDATION_FAILED = "validation_failed"

    # Progress
    PROGRESS_UPDATE = "progress_update"


@dataclass
class Event:
    """Base event class."""

    event_type: EventType
    timestamp: str
    agent_name: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Dict] = None

    def __post_init__(self):
        """Auto-set timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert event to dictionary."""
        data = asdict(self)
        data["event_type"] = self.event_type.value
        return data

    def to_json(self) -> str:
        """Convert event to JSON."""
        data = self.to_dict()
        return json.dumps(data, indent=2)


class EventBus:
    """Central event bus for workflow coordination."""

    def __init__(self, log_file: Optional[Path] = None):
        """
        Initialize event bus.

        Args:
            log_file: Optional path to persist event log
        """
        self.log_file = log_file or Path("events.jsonl")
        self.subscribers: Dict[EventType, List[Callable]] = {}
        self.event_history: List[Event] = []

        logger.info(f"EventBus initialized (log: {self.log_file})")

    def subscribe(self, event_type: EventType, callback: Callable) -> None:
        """
        Subscribe to event type.

        Args:
            event_type: Event type to subscribe to
            callback: Function to call when event is published
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed {callback.__name__} to {event_type.value}")

    def publish(self, event: Event) -> None:
        """
        Publish event.

        Args:
            event: Event to publish
        """
        # Add to history
        self.event_history.append(event)

        # Log to file
        self._log_event(event)

        # Notify subscribers
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(
                        f"Error in event subscriber for {event.event_type.value}: {e}"
                    )

        # Log to console
        self._log_to_console(event)

    def _log_event(self, event: Event) -> None:
        """Log event to file (JSONL format)."""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(event.to_json() + "\n")
        except IOError as e:
            logger.error(f"Failed to log event: {e}")

    def _log_to_console(self, event: Event) -> None:
        """Log event to console with formatting."""
        emoji = {
            EventType.AGENT_STARTED: "▶️",
            EventType.AGENT_COMPLETED: "✅",
            EventType.AGENT_FAILED: "❌",
            EventType.APPROVAL_REQUESTED: "⏸️",
            EventType.APPROVAL_APPROVED: "👍",
            EventType.APPROVAL_REJECTED: "👎",
            EventType.WORKFLOW_STARTED: "🚀",
            EventType.WORKFLOW_COMPLETED: "🎉",
            EventType.WORKFLOW_FAILED: "💥",
            EventType.VALIDATION_PASSED: "✓",
            EventType.VALIDATION_FAILED: "✗",
            EventType.PROGRESS_UPDATE: "📊",
        }.get(event.event_type, "•")

        message = event.message or event.event_type.value
        agent = f" [{event.agent_name}]" if event.agent_name else ""

        print(f"{emoji}  {message}{agent}")

        # Also log at appropriate level
        if "failed" in event.event_type.value.lower():
            logger.error(f"{event.event_type.value}: {message}")
        else:
            logger.info(f"{event.event_type.value}: {message}")

    def get_history(self) -> List[Event]:
        """Get event history."""
        return self.event_history.copy()

    def get_events_by_agent(self, agent_name: str) -> List[Event]:
        """Get all events for specific agent."""
        return [e for e in self.event_history if e.agent_name == agent_name]

    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """Get all events of specific type."""
        return [e for e in self.event_history if e.event_type == event_type]

    def clear_history(self) -> None:
        """Clear in-memory history (file remains)."""
        self.event_history.clear()
        logger.info("Event history cleared")


# Helper functions for publishing common events
def agent_started(event_bus: EventBus, agent_name: str) -> None:
    """Publish agent started event."""
    event = Event(
        event_type=EventType.AGENT_STARTED,
        timestamp=datetime.now().isoformat(),
        agent_name=agent_name,
        message=f"Agent {agent_name} started",
    )
    event_bus.publish(event)


def agent_completed(event_bus: EventBus, agent_name: str, artifacts: Dict) -> None:
    """Publish agent completed event."""
    event = Event(
        event_type=EventType.AGENT_COMPLETED,
        timestamp=datetime.now().isoformat(),
        agent_name=agent_name,
        message=f"Agent {agent_name} completed",
        data={"artifacts": artifacts},
    )
    event_bus.publish(event)


def agent_failed(event_bus: EventBus, agent_name: str, error: str) -> None:
    """Publish agent failed event."""
    event = Event(
        event_type=EventType.AGENT_FAILED,
        timestamp=datetime.now().isoformat(),
        agent_name=agent_name,
        message=f"Agent {agent_name} failed: {error}",
    )
    event_bus.publish(event)


def approval_requested(
    event_bus: EventBus, gate_name: str, message: str, artifacts: Dict
) -> None:
    """Publish approval requested event."""
    event = Event(
        event_type=EventType.APPROVAL_REQUESTED,
        timestamp=datetime.now().isoformat(),
        message=message,
        data={"gate": gate_name, "artifacts": artifacts},
    )
    event_bus.publish(event)


def approval_approved(event_bus: EventBus, gate_name: str) -> None:
    """Publish approval approved event."""
    event = Event(
        event_type=EventType.APPROVAL_APPROVED,
        timestamp=datetime.now().isoformat(),
        message=f"Gate '{gate_name}' approved",
        data={"gate": gate_name},
    )
    event_bus.publish(event)


def approval_rejected(event_bus: EventBus, gate_name: str, reason: str = "") -> None:
    """Publish approval rejected event."""
    event = Event(
        event_type=EventType.APPROVAL_REJECTED,
        timestamp=datetime.now().isoformat(),
        message=f"Gate '{gate_name}' rejected: {reason}",
        data={"gate": gate_name, "reason": reason},
    )
    event_bus.publish(event)


def workflow_started(event_bus: EventBus, spec_file: str) -> None:
    """Publish workflow started event."""
    event = Event(
        event_type=EventType.WORKFLOW_STARTED,
        timestamp=datetime.now().isoformat(),
        message=f"Workflow started for spec: {spec_file}",
        data={"spec_file": spec_file},
    )
    event_bus.publish(event)


def workflow_completed(event_bus: EventBus) -> None:
    """Publish workflow completed event."""
    event = Event(
        event_type=EventType.WORKFLOW_COMPLETED,
        timestamp=datetime.now().isoformat(),
        message="Workflow completed successfully",
    )
    event_bus.publish(event)


def workflow_failed(event_bus: EventBus, error: str) -> None:
    """Publish workflow failed event."""
    event = Event(
        event_type=EventType.WORKFLOW_FAILED,
        timestamp=datetime.now().isoformat(),
        message=f"Workflow failed: {error}",
    )
    event_bus.publish(event)
