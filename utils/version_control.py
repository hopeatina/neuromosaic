"""
Version control utilities for tracking experiment code versions.
"""

from typing import Dict, Any, Optional
import subprocess
from pathlib import Path


class VersionControl:
    """
    Utilities for version control operations.
    """

    @staticmethod
    def get_current_commit() -> str:
        """Get the current commit hash."""
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True
        )
        return result.stdout.strip()

    @staticmethod
    def save_code_snapshot(
        code: str, path: str, message: str = "Auto-generated code snapshot"
    ) -> str:
        """
        Save generated code to a file and commit it.
        Returns the commit hash.
        """
        # Write code to file
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(code)

        # Stage and commit
        subprocess.run(["git", "add", path])
        subprocess.run(["git", "commit", "-m", message])

        return VersionControl.get_current_commit()
