#!/usr/bin/env python3
"""
Specs → Running App Platform Entry Point

Demo launcher and validator for GitHub Copilot Agent Mode.
- Validates project structure
- Displays available workflows
- Launches demo application

NOTE: The actual agent orchestration is handled via:
- GitHub Copilot Chat Modes (.github/chatmodes/)
- Supervisor chat mode as the single workflow orchestrator
- Not a custom Python orchestration engine
"""

import argparse
import logging
import sys
from pathlib import Path

from orchestration.supervisor.supervisor import Supervisor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("platform.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SpecsToAppPlatform:
    """Demo launcher for Specs → Running App platform."""

    def __init__(self, output_dir: Path = None):
        """
        Initialize platform.

        Args:
            output_dir: Output directory for artifacts (default: artifacts/)
        """
        self.output_dir = Path(output_dir or "artifacts")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.supervisor = Supervisor(self.output_dir)

        logger.info("Platform initialized")

    def validate_project(self) -> bool:
        """Validate project structure."""
        logger.info("Validating project structure...")

        required_paths = [
            Path(".github/copilot-instructions.md"),
            Path(".github/agents"),
            Path("ai/prompts"),
            Path("ai/skills"),
            Path("ai/contracts"),
            Path(".vscode/tasks.json"),
        ]

        all_valid = True
        for path in required_paths:
            if path.exists():
                logger.info(f"✓ {path}")
            else:
                logger.warning(f"✗ {path} not found")
                all_valid = False

        if all_valid:
            logger.info("✓ Project structure validated")
        else:
            logger.warning("Some project files are missing")

        return all_valid

    def display_menu(self) -> int:
        """Display main menu and get user choice."""
        print("\n" + "=" * 70)
        print("SPECS → RUNNING APP PLATFORM")
        print("=" * 70)
        print("\nGitHub Copilot Agent Mode Demo Launcher")
        print("\nThis platform extends GitHub Copilot with:")
        print("  • 10 specialized agent chat modes")
        print("  • Supervisor-led chat mode orchestration")
        print("  • Spec → App generation pipeline")
        print("\n" + "=" * 70)
        print("\nOptions:")
        print("  1. Show workflow diagram")
        print("  2. Show chat modes")
        print("  3. Validate project")
        print("  4. Exit")
        print("\n" + "=" * 70)

        while True:
            try:
                choice = input("\nEnter choice (1-4): ").strip()

                if choice in ["1", "2", "3", "4"]:
                    return int(choice)
                else:
                    print("Invalid choice. Please enter 1-4.")

            except KeyboardInterrupt:
                return 4
            except EOFError:
                return 4

    def show_workflow(self) -> None:
        """Display workflow diagram."""
        self.supervisor.display_workflow()

    def show_chat_modes(self) -> None:
        """Display available chat modes."""
        print("\n" + "=" * 70)
        print("AVAILABLE CHAT MODES")
        print("=" * 70)
        print("\nOpen .github/chatmodes/ directory in VS Code")
        print("\nChat modes provide entry points for each agent:")
        print()

        for agent in self.supervisor.get_workflow_dag():
            mode_file = f"{agent['name']}.chatmode.md"
            print(f"  • {mode_file}")
            print(f"    {agent['description']}")
            print()

        print("=" * 70)
        print("\nUsage in Copilot Chat:")
        print('  @chatmode business-analyst "Analyze the requirements"')
        print("=" * 70 + "\n")

    def run(self) -> int:
        """Run the platform demo launcher."""
        try:
            # Validate project
            if not self.validate_project():
                logger.warning("Project validation incomplete")

            # Show menu
            while True:
                choice = self.display_menu()

                if choice == 1:
                    self.show_workflow()
                elif choice == 2:
                    self.show_chat_modes()
                elif choice == 3:
                    self.validate_project()
                elif choice == 4:
                    print("\nGoodbye!\n")
                    return 0

        except KeyboardInterrupt:
            logger.info("User cancelled")
            print("\n\nCancelled")
            return 0
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Specs → Running App Platform Demo Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --output=build/

For full workflow orchestration, use GitHub Copilot chat modes:
  @chatmode business-analyst
  @chatmode solution-architect
  ... etc

    Note: Agent orchestration is handled via:
    - Supervisor chat mode + agent chat modes (.github/chatmodes/)
    - Markdown agent definitions (.github/agents/*.md)
    - Not a custom Python orchestration engine
        """,
    )

    parser.add_argument(
        "--output",
        type=str,
        default="artifacts",
        help="Output directory for artifacts (default: artifacts/)",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Run platform
    platform = SpecsToAppPlatform(output_dir=args.output)
    return platform.run()


if __name__ == "__main__":
    sys.exit(main())
