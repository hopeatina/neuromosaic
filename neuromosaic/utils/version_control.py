"""
Version control utilities for tracking experiment code versions.
"""

from typing import Dict, Any, Optional
import subprocess
from pathlib import Path
import logging
import tempfile
import os

logger = logging.getLogger(__name__)


class VersionControl:
    """
    Utilities for version control operations.
    """

    def __init__(self, code_dir: Optional[str] = None):
        """Initialize with optional code directory."""
        self.code_dir = code_dir or "generated_code"
        os.makedirs(self.code_dir, exist_ok=True)

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

    async def commit_code(self, code: str) -> str:
        """
        Save and commit generated code.

        Args:
            code: The generated code to commit

        Returns:
            str: The commit hash of the saved code

        Raises:
            RuntimeError: If git operations fail
        """
        try:
            # Create a unique filename
            filename = f"model_{self.get_current_commit()[:8]}.py"
            filepath = os.path.join(self.code_dir, filename)

            # Save and commit the code
            return self.save_code_snapshot(
                code, filepath, message=f"Generated model code: {filename}"
            )

        except Exception as e:
            logger.error(f"Failed to commit code: {str(e)}")
            raise RuntimeError(f"Failed to commit code: {str(e)}")
